from aws_cdk import BundlingOptions, Stack, Duration, aws_lambda as _lambda, aws_iam as _iam, aws_s3 as _s3, RemovalPolicy
from constructs import Construct
from os import path
from dotenv import load_dotenv

import hashlib
import os
import platform


load_dotenv(path.abspath(path.dirname(__file__)) + "/../")


class PyStonkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO: once https://github.com/aws/aws-cdk/issues/20907 is resolved, remove below logic
        match platform.machine().lower():
            case a if a in ('amd64', 'x86_64'): architecture = _lambda.Architecture.X86_64
            case a if a in ('arm64'): architecture = _lambda.Architecture.ARM_64
            case _: raise Exception("Unrecognized machine architecture")

        runtime_python = _lambda.Runtime.PYTHON_3_13

        # required environment variables
        environment_variables = {
            "PYSTONK_AWS_REGION": os.getenv('PYSTONK_AWS_REGION'),
            "PYSTONK_SLACK_SECRET": os.getenv('PYSTONK_SLACK_SECRET'),
            "PYSTONK_SLACK_TOKEN": os.getenv('PYSTONK_SLACK_TOKEN'),
            "PYSTONK_SCHWAB_KEY": os.getenv('PYSTONK_SCHWAB_KEY'),
            "PYSTONK_SCHWAB_SECRET": os.getenv('PYSTONK_SCHWAB_SECRET'),
            "PYSTONK_LOG_LEVEL": os.getenv('PYSTONK_LOG_LEVEL')
        }

        # optional environment variables
        if os.getenv('PYSTONK_SLACK_SUCCESS_EMOJIS'):
            environment_variables['PYSTONK_SLACK_SUCCESS_EMOJIS'] = os.getenv('PYSTONK_SLACK_SUCCESS_EMOJIS')
        if os.getenv('PYSTONK_SLACK_FAIL_EMOJIS'):
            environment_variables['PYSTONK_SLACK_FAIL_EMOJIS'] = os.getenv('PYSTONK_SLACK_FAIL_EMOJIS')

        h = hashlib.sha256((os.getenv('PYSTONK_SLACK_SECRET') + os.getenv('PYSTONK_SCHWAB_SECRET')).encode('utf-8'))
        bucket_hash = h.hexdigest()[:8]
        environment_variables["PYSTONK_AWS_S3_HASH"] = bucket_hash

        # main lambda installs everything
        responder_lambda = _lambda.Function(self, 'PyStonkResponder',
                                      runtime=runtime_python,
                                      code=_lambda.Code.from_asset(path.join(path.dirname(__file__), "../../"),
                                                                   bundling=BundlingOptions(
                                                                       image=runtime_python.bundling_image,
                                                                       command=[
                                                                           "bash", "-c",
                                                                           "pip install . -t /asset-output && " +
                                                                           "cp -au pystonk /asset-output && " +
                                                                           "rm /asset-output/pystonk/conf/app.conf"
                                                                       ])
                                                                   ),
                                      handler='pystonk.lambda_responder.start',
                                      architecture=architecture,
                                      environment=environment_variables,
                                      timeout=Duration.seconds(30)
                                      )
        responder_lambda.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)

        # main lambda's arn is needed for receiver lambda
        environment_variables["PYSTONK_AWS_LAMBDA_ARN"] = responder_lambda.function_arn

        # receiver lambda only needs bare mininum modules in order to spin up and respond as fast as possible
        receiver_lambda = _lambda.Function(self, 'PyStonkReceiver',
                                           runtime=runtime_python,
                                           code=_lambda.Code.from_asset(path.join(path.dirname(__file__), "../../"),
                                                                        bundling=BundlingOptions(
                                                                            image=runtime_python.bundling_image,
                                                                            command=[
                                                                                "bash", "-c",
                                                                                "export PYSTONK_RECEIVER_DEPLOY=1 && " +
                                                                                "pip install . -t /asset-output && " +
                                                                                "cp -au pystonk /asset-output && " +
                                                                                "rm /asset-output/pystonk/conf/app.conf"
                                                                            ])
                                                                        ),
                                           handler='pystonk.lambda_receiver.start',
                                           architecture=architecture,
                                           environment=environment_variables,
                                           timeout=Duration.seconds(5)
                                           )
        receiver_lambda.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)
        receiver_lambda.add_to_role_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                actions=[
                    "lambda:InvokeFunction",
                    "lambda:GetFunction"
                ],
                resources=["*"]
            )
        )

        # s3 bucket for storing/serving generated charts
        image_bucket = _s3.Bucket(self, 'PyStonkS3',
                   bucket_name=f"pystonk-images-{bucket_hash}",
                   block_public_access=_s3.BlockPublicAccess(
                       block_public_acls=True,
                       block_public_policy=False,
                       ignore_public_acls=True,
                       restrict_public_buckets=False
                   ),
                   public_read_access=True,
                   encryption=_s3.BucketEncryption.S3_MANAGED,
                   lifecycle_rules=[_s3.LifecycleRule(
                       id="DeleteAfterThreeDays",
                       expiration=Duration.days(3)
                   )],
                   removal_policy=RemovalPolicy.DESTROY,
                   versioned=False
                   )
        image_bucket.grant_write(responder_lambda)
