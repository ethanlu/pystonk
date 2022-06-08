from pystonk.models.Quote import Quote
from pystonk.views import View

from typing import Dict, List

import random


class PriceCheckView(View):
    def __init__(self, symbol: str, quote: Quote):
        super().__init__()

        self._symbol = symbol
        self._quote = quote

    def show_text(self) -> str:
        return f"{self._symbol} is currently {round(float(self._quote.price), 2)}"

    def show(self) -> List[Dict]:
        info = [
            f"*Price*: `{round(self._quote.price, 2)}`"
        ]

        if self._verbose:
            info.append(f"*Last Price*: `{self._quote.last_price}`")
            info.append(f"*Low/High Price*: `{self._quote.low_price}`/`{self._quote.high_price}`")
            info.append(f"*52 Week Low/High Price*: `{self._quote.low_price_52week}`/`{self._quote.high_price_52week}`")
            info.append(f"*Bid/Ask*: `{self._quote.bid_price}`/`{self._quote.ask_price}`")
            info.append(f"*Volume*: `{self._quote.volume}`")

        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n\n Here is the quote on `{self._symbol}`"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n".join(info)
                }
            }
        ]

        return response
