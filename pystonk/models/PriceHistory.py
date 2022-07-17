from pystonk.models.CandleStick import CandleStick
from pystonk.utils import percent_diff
from pystonk.utils.LoggerMixin import LoggerMixin

from typing import List


class PriceHistory(LoggerMixin):
    def __init__(self, candlesticks: List[CandleStick], start_to_end: bool = False):
        self._candlesticks = candlesticks
        self._percent_changes = []

        open_price = None
        for c in self._candlesticks:
            if not start_to_end or not open_price:
                open_price = c.open_price
            close_price = c.close_price
            self._percent_changes.append(percent_diff(open_price, close_price))
            open_price = close_price

    def intervals(self) -> List[CandleStick]:
        return self._candlesticks

    def percent_change_intervals(self) -> List[float]:
        return self._percent_changes

    def count_intervals(self) -> int:
        return len(self._candlesticks)

    def count_intervals_exceed_percent_threshold(self, percent: float) -> int:
        return len([1 for pc in self._percent_changes if abs(pc) >= percent])

    def percent_rate(self, percent: float):
        return round((self.count_intervals_exceed_percent_threshold(percent)/self.count_intervals()) * 100, 2)
