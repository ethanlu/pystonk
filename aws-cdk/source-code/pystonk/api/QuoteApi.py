from pystonk.api import Api
from pystonk.models.Quote import Quote
from pystonk.utils import coalesce

from typing import Optional


class QuoteApi(Api):
    ENDPOINT = "https://api.schwabapi.com/marketdata/v1/{symbol}/quotes"

    def __init__(self, app_key: str, app_secret: str):
        super().__init__(app_key, app_secret)

    def get_quote(self, symbol: str) -> Optional[Quote]:
        symbol = symbol.upper()
        self.logger.debug(f"getting quote for {symbol}")
        data = self._get(
            self.ENDPOINT.format(symbol=symbol),
            params={'fields': 'quote,reference'},
            headers={'Authorization': f"Bearer {self.get_access_token()}"}
        )

        if data and data[symbol] and data[symbol]['quote']:
            return Quote(
                symbol=symbol,
                price=coalesce(data[symbol]['quote'], ('mark', 'openPrice', 'closePrice')),
                last_price=coalesce(data[symbol]['quote'], ('lastPrice', 'openPrice', 'closePrice')),
                high_price=coalesce(data[symbol]['quote'], ('highPrice', '52WkHigh')),
                low_price=coalesce(data[symbol]['quote'], ('lowPrice', '52WkLow')),
                high_price_52=coalesce(data[symbol]['quote'], ('52WkHigh', 'highPrice')),
                low_price_52=coalesce(data[symbol]['quote'], ('52WkLow', 'lowPrice')),
                bid=coalesce(data[symbol]['quote'], ('bidPrice', 'lastPrice', 'closePrice')),
                ask=coalesce(data[symbol]['quote'], ('askPrice', 'lastPrice', 'closePrice')),
                bid_size=coalesce(data[symbol]['quote'], ('bidSize', )),
                ask_size=coalesce(data[symbol]['quote'], ('askSize', )),
                volume=coalesce(data[symbol]['quote'], ('totalVolume', ))
            )

        self.logger.debug(f"symbol {symbol} was not found!")
        return None
