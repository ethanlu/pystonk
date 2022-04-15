from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.models.OptionContract import OptionContract
from pystonk.utils import percent_diff
from pystonk.utils.LoggerMixin import LoggerMixin

from datetime import date
from typing import Any, Dict, Generator, Tuple


class WeeklyOptionsReport(LoggerMixin):
    def __init__(self, quote_api: QuoteApi, options_chain_api: OptionsChainApi):
        self._quote_api = quote_api
        self._options_chain_api = options_chain_api
        self._mark = None
        self._options_chain: Dict[str, Tuple[OptionContract, OptionContract]] = {}

    def retrieveData(self, symbol: str) -> bool:
        symbol = symbol.upper()

        # get last known price
        self._mark = self._quote_api.getQuote(symbol)

        # get next week's options chain
        self._options_chain = self._options_chain_api.getWeeklySingleOptionChain(
            symbol=symbol,
            week_date=date.today(),
            strike_count=200
        )

        return len(self._options_chain) > 0

    def generate(self) -> Generator[Tuple[str, float, OptionContract, OptionContract], Any, None]:
        '''
        generator that returns options chain for given symbol as a tuple of strike price, % change of strike price to market price, call option, and put option
        :return:
        '''
        return ((strike_price, percent_diff(self._mark, float(strike_price)), contracts[0], contracts[1]) for strike_price, contracts in self._options_chain.items())

    def getMark(self) -> float:
        return self._mark

    def getStrikePricesForTargetPremium(self, premium: float, is_sell: bool = True) -> Tuple[Tuple[OptionContract, float, float], Tuple[OptionContract, float, float]]:
        premium = round(premium, 2)
        target_call = None
        target_put = None
        for strike_price, percent_change, call_option, put_option in self.generate():
            call_price = call_option.bid if is_sell else call_option.ask
            put_price = put_option.bid if is_sell else put_option.ask

            if call_price >= premium:
                target_call = (call_option, round(float(strike_price) - self._mark, 2), percent_change)
            if put_price <= premium:
                target_put = (put_option, round(float(strike_price) - self._mark, 2), percent_change)

        return (target_call, target_put)