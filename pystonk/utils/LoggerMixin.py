from pystonk import get_conf_path

from logging import config, getLogger, Logger
from pyhocon import ConfigFactory

config.dictConfig(ConfigFactory.parse_file(get_conf_path('app.conf'))['log'])

class LoggerMixin(object):
    @property
    def logger(self) -> Logger:
        return getLogger('pystonk')
