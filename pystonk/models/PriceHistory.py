from pystonk.models.CandleStick import CandleStick
from pystonk.utils.LoggerMixin import LoggerMixin

from typing import List


class PriceHistory(LoggerMixin):
    def __init__(self, candlesticks: List[CandleStick]):
        self._candlesticks = candlesticks

    def intervals(self) -> List[CandleStick]:
        return self._candlesticks

    def countIntervals(self) -> int:
        return len(self._candlesticks)

    def countIntervalsExceedPercentThreshold(self, percent: float) -> int:
        return len([1 for c in self._candlesticks if abs(c.percentChange) >= percent])

    def percentProbability(self, percent: float):
        return round((self.countIntervalsExceedPercentThreshold(percent)/self.countIntervals()) * 100, 2)
