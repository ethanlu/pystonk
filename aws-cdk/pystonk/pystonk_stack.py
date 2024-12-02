from aws_cdk import (
    BundlingOptions,
    Stack,
    Duration,
    aws_lambda as _lambda,
)
from constructs import Construct
from pyhocon import ConfigFactory
from os import path


PYSTONK_ROOT = path.abspath(path.dirname(__file__)) + "/../../pystonk/"


def get_conf_path(filename: str = 'app.conf') -> str:
    filepath = path.join(PYSTONK_ROOT, 'conf', filename)
    if path.exists(filepath):
        return filepath
    else:
        return path.join(PYSTONK_ROOT, 'conf', 'default.conf')


# TODO : introduce app-aws.conf?
config = ConfigFactory.parse_file(get_conf_path("default.conf"))


class PystonkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        func = _lambda.Function(self, 'PystonkLambda',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(path.join(path.dirname(__file__), "../../"),
                    bundling=BundlingOptions(
                        image=_lambda.Runtime.PYTHON_3_9.bundling_image,
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
                "PYSTONK_SLACK_SECRET": config['slack']['secret'],
                "PYSTONK_SLACK_TOKEN": config['slack']['token'],
                "PYSTONK_SCHWAB_KEY": config['app_key'],
                "PYSTONK_SCHWAB_SECRET": config['app_secret'],
                "PYSTONK_LOG_LEVEL": config['log']['loggers']['pystonk']['level']
            },
            timeout=Duration.seconds(5)
        )

        func.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)
