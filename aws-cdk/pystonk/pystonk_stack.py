from aws_cdk import (
    BundlingOptions,
    Stack,
    Duration,
    aws_lambda as _lambda,
)
from constructs import Construct
from os import path

class PystonkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        func = _lambda.Function(self, 'PystonkLambda',
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset(path.join(path.dirname(__file__), "../../"),
                    bundling=BundlingOptions(
                        image=_lambda.Runtime.PYTHON_3_11.bundling_image,
                        command=["bash", "-c",
                                 "python -m pip install . -t /asset-output && " +
                                 "cp -au pystonk /asset-output && " +
                                 "rm /asset-output/pystonk/conf/app.conf"
                        ]
                    )
                ), 
            handler='pystonk.slack_app.start_lambda',
            architecture=_lambda.Architecture.ARM_64,
            environment={
                "PYSTONK_SLACK_SECRET": "",
                "PYSTONK_SLACK_TOKEN": "",
                "PYSTONK_SCHWAB_KEY": "",
                "PYSTONK_SCHWAB_SECRET": "",
                "PYSTONK_LOG_LEVEL": "INFO"
            },
            timeout=Duration.seconds(30)
        )

        func.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)
