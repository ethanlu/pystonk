from logging import config, getLogger
from pyhocon import ConfigFactory

import os


PYSTONK_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_conf_path(filename: str = 'app.conf') -> str:
    filepath = os.path.join(PYSTONK_ROOT, 'conf', filename)
    if os.path.exists(filepath):
        return filepath
    else:
        return os.path.join(PYSTONK_ROOT, 'conf', 'default.conf')

# load configuration for pystonk
configuration = ConfigFactory.parse_file(get_conf_path())

# init logger
config.dictConfig(ConfigFactory.parse_file(get_conf_path())['log'])
logger = getLogger("pystonk")