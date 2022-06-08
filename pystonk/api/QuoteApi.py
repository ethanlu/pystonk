from pystonk.api import Api
from pystonk.models.Quote import Quote
from pystonk.utils import coalesce

from typing import Optional

import requests


class QuoteApi(Api):
    ENDPOINT = "https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes"

    def __init__(self, api_key: str):
        super().__init__(api_key)

    def get_quote(self, symbol: str) -> Optional[Quote]:
        symbol = symbol.upper()
        params = {
            'apikey': self._api_key,
        }
        self.logger.debug(f"getting quote for {symbol} with params : {params}")
        response = requests.get(
            self.ENDPOINT.format(symbol=symbol),
            params=params
        )
        self.logger.debug(f"request : {response.url}")
        self.logger.debug(f"response : {response.status_code}")

        data = response.json()

        if data and data[symbol]:
            return Quote(
                symbol=symbol,
                price=coalesce(data[symbol], ('mark', 'openPrice', 'closePrice')),
                last_price=coalesce(data[symbol], ('lastPrice', 'lastPriceInDouble', 'closePrice')),
                high_price=coalesce(data[symbol], ('highPrice', 'highPriceInDouble', '52WkHigh')),
                low_price=coalesce(data[symbol], ('lowPrice', 'lowPriceInDouble', '52WkLow')),
                high_price_52=coalesce(data[symbol], ('52WkHigh', '52WkHighInDouble', 'highPrice', 'highPriceInDouble')),
                low_price_52=coalesce(data[symbol], ('52WkLow', '52WkLowInDouble', 'lowPrice', 'lowPriceInDouble')),
                bid=coalesce(data[symbol], ('bidPrice', 'bidPriceInDouble', 'lastPrice', 'closePrice')),
                ask=coalesce(data[symbol], ('askPrice', 'askPriceInDouble', 'lastPrice', 'closePrice')),
                bid_size=coalesce(data[symbol], ('bidSize', )),
                ask_size=coalesce(data[symbol], ('askSize', )),
                volume=coalesce(data[symbol], ('totalVolume', ))
            )

        return None
