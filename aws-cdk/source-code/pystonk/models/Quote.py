from typing import Optional


class Quote(object):
    def __init__(self, symbol: str, price: float, last_price: float, high_price: float, low_price: float, high_price_52: float, low_price_52: float,
                 bid: float = None, ask: float = None, bid_size: int = None, ask_size: int = None, volume: int = None):
        self._symbol = symbol
        self._price = round(price, 2)
        self._last_price = round(last_price, 2)
        self._high_price = round(high_price, 2)
        self._low_price = round(low_price, 2)
        self._high_price_52 = round(high_price_52, 2)
        self._low_price_52 = round(low_price_52, 2)
        self._bid = round(bid, 2) if bid else None
        self._ask = round(ask, 2) if ask else None
        self._bid_size = round(bid_size) if bid_size else None
        self._ask_size = round(ask_size) if ask_size else None
        self._volume = round(volume) if volume else None

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def price(self) -> float:
        return self._price

    @property
    def last_price(self) -> float:
        return self._last_price

    @property
    def high_price(self) -> float:
        return self._high_price

    @property
    def low_price(self) -> float:
        return self._low_price

    @property
    def high_price_52week(self) -> float:
        return self._high_price_52

    @property
    def low_price_52week(self) -> float:
        return self._low_price_52

    @property
    def bid_price(self) -> Optional[float]:
        return self._bid

    @property
    def ask_price(self) -> Optional[float]:
        return self._ask

    @property
    def bid_size(self) -> Optional[int]:
        return self._bid_size

    @property
    def ask_size(self) -> Optional[int]:
        return self._ask_size

    @property
    def volume(self) -> Optional[int]:
        return self._volume
