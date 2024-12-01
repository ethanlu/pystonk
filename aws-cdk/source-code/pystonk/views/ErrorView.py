from pystonk.views import View

from typing import Dict, List

import random


class ErrorView(View):
    def __init__(self, e: str):
        super().__init__()

        self._error_message = e

    def show_text(self) -> str:
        return self._error_message

    def show(self) -> List[Dict]:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_FAIL_EMOJI)} \n {self._error_message}"
                }
            }
        ]
