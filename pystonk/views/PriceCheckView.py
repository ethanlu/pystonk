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
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n `{self._symbol}` is currently `{round(self._quote.price, 2)}`"
                }
            }
        ]
