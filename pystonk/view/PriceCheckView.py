from pystonk.view import View

from typing import List, Optional

import random


class PriceCheckView(View):
    def __init__(self, symbol: str, price: Optional[float]):
        super().__init__()
        self._symbol = symbol
        self._price = price

    def show(self) -> List:
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
