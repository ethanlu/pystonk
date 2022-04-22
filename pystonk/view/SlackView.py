from typing import Any, Dict, Iterable, List, NamedTuple, Optional

class SlackView(object):
    def showAvailableCommands(self) -> Dict:
        return {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*I didn't understand your command* :ro-hmm:"
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
                        "text": "`ph {stock symbol} {percent change threshold (decimal)}` \n\n This command will show the weekly price changes for the stock in the past year. The second parameter will mark any week where the price change exceeded the threshold"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "`oc {stock symbol} {target premium price (decimal)}` \n\n This command shows next week's options chain for the stock and the strike prices for calls and puts that is closest to the given target premium price"
                    }
                }
            ]
        }

    def showPriceHistory(self, symbol: str, percent: float, total_weeks: int, exceeded_weeks: int, candlesticks: List, longest_weeks: Optional[List]):
        pass

    def showOptionsChain(self, symbol: str, premium: float, current_price: float, data: Iterable, target_options: Optional[NamedTuple]):
        pass