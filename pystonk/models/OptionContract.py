from pystonk.api.Types import ContractType

from datetime import datetime
from typing import Any


def normalize_nan(input: Any) -> float:
    return round(input, 2) if input != 'NaN' else 0.0


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
                 expiration_datetime: str,
                 last_trading_datetime: int
    ):
        self._contract_type = ContractType.CALL if put_call == ContractType.CALL.value else ContractType.PUT
        self._symbol = symbol.upper()
        self._description = description
        self._strike_price = round(strike_price, 2)
        self._bid = round(bid, 2)
        self._ask = round(ask, 2)
        self._bid_ask_size = tuple(map(lambda x: int(x), bid_ask_size.split('X')))
        self._volatility = normalize_nan(volatility)
        self._delta = normalize_nan(delta)
        self._gamma = normalize_nan(gamma)
        self._theta = normalize_nan(theta)
        self._vega = normalize_nan(vega)
        self._rho = normalize_nan(rho)
        self._open_interest = open_interest
        self._in_the_money = in_the_money
        self._non_standard = non_standard
        self._expiration_datetime = datetime.strptime(expiration_datetime.split('.')[0], "%Y-%m-%dT%H:%M:%S")
        self._last_trading_datetime = datetime.fromtimestamp(last_trading_datetime / 1000)

    @property
    def contract_type(self) -> ContractType:
        return self._contract_type

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def description(self) -> str:
        return self._description

    @property
    def strike_price(self) -> float:
        return self._strike_price

    @property
    def bid(self) -> float:
        return self._bid

    @property
    def ask(self) -> float:
        return self._ask

    @property
    def bid_size(self) -> int:
        return self._bid_ask_size[0]

    @property
    def ask_size(self) -> int:
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
    def open_interest(self) -> int:
        return self._open_interest

    @property
    def is_itm(self) -> bool:
        return self._in_the_money

    @property
    def is_nonstandard(self) -> bool:
        return self._non_standard

    @property
    def expiration_datetime(self) -> datetime:
        return self._expiration_datetime

    @property
    def last_trading_datetime(self) -> datetime:
        return self._last_trading_datetime
