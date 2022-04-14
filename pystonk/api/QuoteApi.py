from pystonk.api import Api

from typing import Optional

import requests


class QuoteApi(Api):
    ENDPOINT = "https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes"

    def __init__(self, api_key: str):
        super().__init__(api_key)

    def getQuote(self, symbol: str) -> Optional[float]:
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

        response_data = response.json()

        return response_data[symbol]['mark'] if response_data else None