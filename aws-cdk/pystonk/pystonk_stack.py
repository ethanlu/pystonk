import os
import platform

from aws_cdk import (
    BundlingOptions,
    Stack,
    Duration,
    aws_lambda as _lambda,
)
from constructs import Construct
from os import path
from dotenv import load_dotenv


load_dotenv(path.abspath(path.dirname(__file__)) + "/../")


class PystonkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        match platform.machine().lower():
            case a if a in ('amd64', 'x86_64'): build_arch = _lambda.Architecture.X86_64
            case a if a in ('arm64'): build_arch = _lambda.Architecture.ARM_64
            case _: raise Exception("Unrecognized machine architecture")

        func = _lambda.Function(self, 'PystonkLambda',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset(path.join(path.dirname(__file__), "../../"),
                    bundling=BundlingOptions(
                        image=_lambda.Runtime.PYTHON_3_10.bundling_image,
                        command=["bash", "-c",
                                 "pip install . -t /asset-output && " +
                                 "cp -au pystonk /asset-output && " +
                                 "rm /asset-output/pystonk/conf/app.conf"
                        ]
                    )
                ), 
            handler='pystonk.slack_app.start_lambda',
            architecture=build_arch,
            environment={
                "PYSTONK_SLACK_SECRET": os.getenv('PYSTONK_SLACK_SECRET'),
                "PYSTONK_SLACK_TOKEN": os.getenv('PYSTONK_SLACK_TOKEN'),
                "PYSTONK_SCHWAB_KEY": os.getenv('PYSTONK_SCHWAB_KEY'),
                "PYSTONK_SCHWAB_SECRET": os.getenv('PYSTONK_SCHWAB_SECRET'),
                "PYSTONK_LOG_LEVEL": os.getenv('PYSTONK_LOG_LEVEL')
            },
            timeout=Duration.seconds(5)
        )

        func.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)
