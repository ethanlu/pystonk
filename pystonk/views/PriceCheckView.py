from pystonk.views import View

from typing import Dict, List, Optional

import random


class PriceCheckView(View):
    def __init__(self, symbol: str, price: Optional[float]):
        super().__init__()

        self._symbol = symbol
        self._price = price

    def show_text(self) -> str:
        return f"{self._symbol} is currently {round(float(self._price), 2) if self._price else 'not found'}"

    def show(self) -> List[Dict]:
        if self._price:
            msg = f"{random.choice(self.SLACK_OK_EMOJI)} \n `{self._symbol}` is currently `{round(self._price, 2)}`"
        else:
            msg = f"{random.choice(self.SLACK_FAIL_EMOJI)} \n `{self._symbol}` is not found..."
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": msg
                }
            }
        ]
