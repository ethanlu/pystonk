from pystonk.view import View

from typing import List

import random


class ErrorView(View):
    def __init__(self, e: str):
        super().__init__()
        self._error_message = e

    def show(self) -> List:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_FAIL_EMOJI)} \n Unexpected error : {self._error_message}"
                }
            }
        ]
