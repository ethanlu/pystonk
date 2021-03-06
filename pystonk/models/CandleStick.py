from pystonk.api.Types import FrequencyType

from datetime import datetime


class CandleStick(object):
    def __init__(self,
                 open_price: float,
                 high_price: float,
                 low_price: float,
                 close_price: float,
                 volume: int,
                 start_datetime: int,
                 frequency_type: FrequencyType):
        self._open_price = round(open_price, 2)
        self._high_price = round(high_price, 2)
        self._low_price = round(low_price, 2)
        self._close_price = round(close_price, 2)
        self._volume = volume
        self._start_datetime = datetime.fromtimestamp(start_datetime / 1000)
        self._frequency_type = frequency_type

    @property
    def open_price(self) -> float:
        return self._open_price

    @property
    def high_price(self) -> float:
        return self._high_price

    @property
    def low_price(self) -> float:
        return self._low_price

    @property
    def close_price(self) -> float:
        return self._close_price

    @property
    def volume(self) -> int:
        return self._volume

    @property
    def start_datetime(self) -> datetime:
        return self._start_datetime

    @property
    def frequency_type(self) -> FrequencyType:
        return self._frequency_type
