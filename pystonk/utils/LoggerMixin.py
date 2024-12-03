from pystonk import logger
from logging import getLogger, Logger

class LoggerMixin(object):
    @property
    def logger(self) -> Logger:
        return logger
