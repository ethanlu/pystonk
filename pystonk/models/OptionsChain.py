from pystonk.models.OptionContract import OptionContract
from pystonk.utils import percent_diff
from pystonk.utils.LoggerMixin import LoggerMixin

from typing import Dict, List, Optional, Tuple


class OptionsChain(LoggerMixin):
    def __init__(self, price: float, contracts: Dict[str, Tuple[OptionContract, OptionContract]]):
        self._price = price
        self._matrix = [(strike_price, percent_diff(self._price, float(strike_price)), contracts[0], contracts[1]) for strike_price, contracts in contracts.items()]

    def matrix(self) -> List[Tuple[str, float, OptionContract, OptionContract]]:
        return self._matrix

    def closest_call_option_by_percent(self, target: float) -> Optional[Tuple]:
        closest = None
        for strike_price, percent_change, call_option, _ in reversed(self._matrix):
            if percent_change >= target:
                closest = (call_option, round(float(strike_price) - self._price, 2), percent_change)

        return closest

    def closest_put_option_by_percent(self, target: float) -> Optional[Tuple]:
        target = -abs(target)
        closest = None
        for strike_price, percent_change, _, put_option in self._matrix:
            if percent_change <= target:
                closest = (put_option, round(float(strike_price) - self._price, 2), percent_change)

        return closest

    def closest_call_option_by_premium(self, target: float, is_sell: bool = True) -> Optional[Tuple]:
        closest = None
        for strike_price, percent_change, call_option, _ in self._matrix:
            call_price = call_option.bid if is_sell else call_option.ask

            if call_price >= target:
                closest = (call_option, round(float(strike_price) - self._price, 2), percent_change)

        return closest

    def closest_put_option_by_premium(self, target: float, is_sell: bool = True) -> Optional[Tuple]:
        closest = None
        for strike_price, percent_change, _, put_option in reversed(self._matrix):
            put_price = put_option.bid if is_sell else put_option.ask

            if put_price >= target:
                closest = (put_option, round(float(strike_price) - self._price, 2), percent_change)

        return closest
