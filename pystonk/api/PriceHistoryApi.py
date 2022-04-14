from pystonk.api import Api
from pystonk.api.Types import PeriodType, FrequencyType
from pystonk.models.CandleStick import CandleStick

from datetime import datetime
from typing import Any, Dict, List

import requests


class PriceHistoryApi(Api):
    ENDPOINT = "https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory"

    def __init__(self, api_key: str):
        super().__init__(api_key)

    def _buildResponse(self, candlesticks: List[Dict[str, Any]], frequency_type: FrequencyType) -> List[CandleStick]:
        return [CandleStick(data['open'], data['high'], data['low'], data['close'], data['volume'], data['datetime'], frequency_type) for data in candlesticks]

    def getPriceHistory(self, symbol: str,
            period_type: PeriodType = PeriodType.YTD,
            period: int = 1,
            frequency_type: FrequencyType = FrequencyType.DAILY,
            frequency: int = 1) -> List[CandleStick]:
        params = {
            'apikey': self._api_key,
            'periodType': period_type.value,
            'period': period,
            'frequencyType': frequency_type.value,
            'frequency': frequency,
            'needExtendedHoursData': False
        }
        self.logger.debug(f"getting price history for {symbol} with params : {params}")
        response = requests.get(
            self.ENDPOINT.format(symbol=symbol),
            params=params
        )
        self.logger.debug(f"request : {response.url}")
        self.logger.debug(f"response : {response.status_code}")
        return self._buildResponse(response.json()['candles'], frequency_type)

    def getPriceHistoryWithDateRange(self, symbol: str,
            start: datetime,
            end: datetime,
            period_type: PeriodType = PeriodType.YTD,
            frequency_type: FrequencyType = FrequencyType.DAILY,
            frequency: int = 1) -> List[CandleStick]:
        params = {
            'apikey': self._api_key,
            'periodType': period_type.value,
            'frequencyType': frequency_type.value,
            'frequency': frequency,
            'startDate': start.timestamp() * 1000,
            'endDate': end.timestamp() * 1000,
            'needExtendedHoursData': False
        }
        self.logger.debug(f"getting date ranged price history for {symbol} with params : {params}")
        response = requests.get(self.ENDPOINT.format(symbol=symbol), params=params)
        self.logger.debug(f"request : {response.url}")
        self.logger.debug(f"response : {response.status_code}")
        return self._buildResponse(response.json()['candles'], frequency_type)

