from pystonk.view import View

from typing import List

import random


class HelpView(View):
    def __init__(self):
        super().__init__()

    def show(self) -> List:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_FAIL_EMOJI)} \n I didn't understand your command"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Here are the available commands:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "`pc {stock symbol}` \n\n This command will show the current market price the stock"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "`ph {stock symbol} {percent change threshold (decimal)}` \n\n This command will show the weekly price changes for the stock in the past year. The second parameter will mark any week where the price change exceeded the threshold"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "`oc {stock symbol} {target premium price (decimal)}` \n\n This command shows next week's options chain for the stock and the strike prices for calls and puts that is closest to the given target premium price"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "The above commands are also available with the `/pystonk` command, but the results will only be visible to you"
                }
            }
        ]
