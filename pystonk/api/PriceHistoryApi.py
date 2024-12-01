from pystonk.api import Api
from pystonk.api.Types import PeriodType, FrequencyType
from pystonk.models.CandleStick import CandleStick

from typing import Any, Dict, List


def build_response(candlesticks: List[Dict[str, Any]], frequency_type: FrequencyType) -> List[CandleStick]:
    return [CandleStick(data['open'], data['high'], data['low'], data['close'], data['volume'], data['datetime'], frequency_type) for data in candlesticks]


class PriceHistoryApi(Api):
    ENDPOINT = "https://api.schwabapi.com/marketdata/v1/pricehistory"

    def __init__(self, app_key: str, app_secret: str):
        super().__init__(app_key, app_secret)

    def get_price_history(self, symbol: str,
                          period_type: PeriodType = PeriodType.YTD,
                          period: int = 1,
                          frequency_type: FrequencyType = FrequencyType.DAILY,
                          frequency: int = 1) -> List[CandleStick]:
        symbol = symbol.upper()
        self.logger.debug(f"getting price history for {symbol}")
        data = self._get(
            self.ENDPOINT,
            params={
                'symbol': symbol,
                'periodType': period_type.value,
                'period': period,
                'frequencyType': frequency_type.value,
                'frequency': frequency,
                'needExtendedHoursData': False,
                'needPreviousClose': False
            },
            headers={'Authorization': f"Bearer {self.get_access_token()}"}
        )
        return build_response(data['candles'], frequency_type)
