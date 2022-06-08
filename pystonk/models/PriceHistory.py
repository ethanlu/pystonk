from pystonk.models.CandleStick import CandleStick
from pystonk.utils.LoggerMixin import LoggerMixin

from typing import List


class PriceHistory(LoggerMixin):
    def __init__(self, candlesticks: List[CandleStick]):
        self._candlesticks = candlesticks

    def intervals(self) -> List[CandleStick]:
        return self._candlesticks

    def count_intervals(self) -> int:
        return len(self._candlesticks)

    def count_intervals_exceed_percent_threshold(self, percent: float) -> int:
        return len([1 for c in self._candlesticks if abs(c.percent_change) >= percent])

    def percent_rate(self, percent: float):
        return round((self.count_intervals_exceed_percent_threshold(percent)/self.count_intervals()) * 100, 2)
