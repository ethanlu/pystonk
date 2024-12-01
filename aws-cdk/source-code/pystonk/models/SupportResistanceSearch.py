from pystonk.models.CandleStick import CandleStick

from typing import Dict, List


class SupportResistanceSearch(object):
    def __init__(self, data: List[CandleStick]):
        self._data = data

    def _is_consecutive_sequence(self, start: int, end: int, increasing: bool) -> bool:
        i = start + 1
        while i <= end:
            if increasing and self._data[i - 1].close_price >= self._data[i].close_price:
                return False
            elif not increasing and self._data[i - 1].close_price <= self._data[i].close_price:
                return False
            i = i + 1
        return True

    def _get_prices(self, is_support: bool = True):
        prices = []
        i = 6
        while i < len(self._data):
            if self._is_consecutive_sequence(i - 6, i - 3, not is_support) and self._is_consecutive_sequence(i - 3, i, is_support):
                prices.append(self._data[i - 3])
            i = i + 1
        return prices

    def group_prices(self, prices: List[CandleStick], threshold: float) -> Dict[str, List[CandleStick]]:
        grouped_prices = {}
        current_key = None
        current_group = []
        for c in sorted(prices, key=lambda x: x.close_price):
            if current_key is None or abs(current_key - c.close_price) <= threshold:
                current_group.append(c)
                current_key = c.close_price if current_key is None else round(((current_key * (len(current_group) - 1)) + c.close_price) / len(current_group), 2)
            else:
                grouped_prices[str(current_key)] = sorted(current_group, key=lambda x: x.start_datetime)
                current_key = c.close_price
                current_group = [c]
        if current_group:
            grouped_prices[str(current_key)] = sorted(current_group, key=lambda x: x.start_datetime)
        return grouped_prices

    def supports(self) -> List[CandleStick]:
        return self._get_prices(True)

    def resistances(self) -> List[CandleStick]:
        return self._get_prices(False)
