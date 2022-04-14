from pystonk.api.Types import ContractType

from datetime import datetime


class OptionContract(object):
    def __init__(self,
                 put_call: str,
                 symbol: str,
                 description: str,
                 strike_price: float,
                 bid: float,
                 ask: float,
                 bid_ask_size: str,
                 volatility: float,
                 delta: float,
                 gamma: float,
                 theta: float,
                 vega: float,
                 rho: float,
                 open_interest: int,
                 in_the_money: bool,
                 non_standard: bool,
                 expiration_datetime: int,
                 last_trading_datetime: int
    ):
        self._contract_type = ContractType.CALL if put_call == ContractType.CALL.value else ContractType.PUT
        self._symbol = symbol.upper()
        self._description = description
        self._strike_price = round(strike_price, 2)
        self._bid = round(bid, 2)
        self._ask = round(ask, 2)
        self._bid_ask_size = tuple(map(lambda x: int(x), bid_ask_size.split('X')))
        self._volatility = round(volatility, 2)
        self._delta = round(delta, 2)
        self._gamma = round(gamma, 2)
        self._theta = round(theta, 2)
        self._vega = round(vega, 2)
        self._rho = round(rho, 2)
        self._open_interest = open_interest
        self._in_the_money = in_the_money
        self._non_standard = non_standard
        self._expiration_datetime = datetime.fromtimestamp(expiration_datetime / 1000)
        self._last_trading_datetime = datetime.fromtimestamp(last_trading_datetime / 1000)

    @property
    def contractType(self) -> ContractType:
        return self._contract_type

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def description(self) -> str:
        return self._description

    @property
    def strikePrice(self) -> float:
        return self._strike_price

    @property
    def bid(self) -> float:
        return self._bid

    @property
    def ask(self) -> float:
        return self._ask

    @property
    def bidSize(self) -> int:
        return self._bid_ask_size[0]

    @property
    def askSize(self) -> int:
        return self._bid_ask_size[1]

    @property
    def volatility(self) -> float:
        return self._volatility

    @property
    def delta(self) -> float:
        return self._delta

    @property
    def gamma(self) -> float:
        return self._gamma

    @property
    def theta(self) -> float:
        return self._theta

    @property
    def vega(self) -> float:
        return self._vega

    @property
    def rho(self) -> float:
        return self._rho

    @property
    def openInterest(self) -> int:
        return self._open_interest

    @property
    def isITM(self) -> bool:
        return self._in_the_money

    @property
    def isNonstandard(self) -> bool:
        return self._non_standard

    @property
    def expirationDateTime(self) -> datetime:
        return self._expiration_datetime

    @property
    def lastTradingDateTime(self) -> datetime:
        return self._last_trading_datetime