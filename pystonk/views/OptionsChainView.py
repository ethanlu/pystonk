from pystonk.models.OptionsChain import OptionsChain
from pystonk.views import View

from prettytable import PrettyTable
from typing import Dict, List

import random


class OptionsChainView(View):
    def __init__(self, symbol: str, premium: float, latest_price: float, options_chain: OptionsChain):
        super().__init__()

        self._symbol = symbol
        self._premium = premium
        self._latest_price = latest_price
        self._options_chain = options_chain

        self._sell_call = self._options_chain.closest_call_option(self._premium)
        self._buy_call = self._options_chain.closest_call_option(self._premium, is_sell=False)

        self._sell_put = self._options_chain.closest_put_option(self._premium)
        self._buy_put = self._options_chain.closest_put_option(self._premium, is_sell=False)

        # options table
        self._t = PrettyTable()
        self._t.field_names = ('  ', 'Call Bid', 'Call Ask', 'Put Bid', 'Put Ask', 'Strike', '% Change')

        for (strike_price, percent_change, call_option, put_option) in self._options_chain.matrix():
            flag = ''
            if call_option == self._sell_call[0]:
                flag += 'c'
            if call_option == self._buy_call[0]:
                flag += 'C'
            if put_option == self._sell_put[0]:
                flag += 'p'
            if put_option == self._buy_put[0]:
                flag += 'P'

            self._t.add_row((
                flag,
                '%7.2f' % call_option.bid,
                '%7.2f' % call_option.ask,
                '%7.2f' % put_option.bid,
                '%7.2f' % put_option.ask,
                '%7.2f' % float(strike_price),
                '%7.2f' % percent_change,
            ))
        self._t.align = 'r'

    def show_text(self) -> str:
        return f"option chain for {self._symbol} with {self._premium} premium cannot be shown in text-only mode"

    def show(self) -> List[Dict]:
        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n Here is next week's option chain for `{self._symbol}` with target premium price `{self._premium}` for buy-call, buy-put, sell-call, and sell-put marked as `C`, `P`, `c`, and `p` respectively:"
                }
            },
            {
                "type": "divider"
            },
        ]

        # paginate table view into sections
        i = 0
        while i < len(self._t.rows):
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{self._t.get_string(start=i, end=i + self.SLACK_BLOCK_LIMIT)}```"
                    }
                }
            )
            i += self.SLACK_BLOCK_LIMIT

        if self._sell_call or self._sell_put:
            response.append(
                {
                    "type": "divider"
                }
            )

            if self._sell_call:
                response.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"`c` : Closest `{self._sell_call[0].expiration_datetime.strftime('%Y-%m-%d')}` strike price for sell-call is `{self._sell_call[0].strike_price}`\nWhich is `{self._sell_call[1]}` from current price of `{self._latest_price}` (`{self._sell_call[2]}%`)"
                        }
                    }
                )

            if self._sell_put:
                response.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"`p` : Closest `{self._sell_put[0].expiration_datetime.strftime('%Y-%m-%d')}` strike price for sell-put is `{self._sell_put[0].strike_price}`\nWhich is `{self._sell_put[1]}` from current price of `{self._latest_price}` (`{self._sell_put[2]}%`)"
                        }
                    }
                )

            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`{self._premium}` premium for sell options has a skew of `{round(self._sell_call[1] + self._sell_put[1], 2)}`"
                    }
                }
            )

        if self._buy_call or self._buy_put:
            response.append(
                {
                    "type": "divider"
                }
            )

            if self._buy_call:
                response.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"`C` : Closest `{self._buy_call[0].expiration_datetime.strftime('%Y-%m-%d')}` strike price for buy-call is `{self._buy_call[0].strike_price}`\nWhich is `{self._buy_call[1]}` from current price of `{self._latest_price}` (`{self._buy_call[2]}%`)"
                        }
                    }
                )

            if self._buy_put:
                response.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"`P` : Closest `{self._buy_put[0].expiration_datetime.strftime('%Y-%m-%d')}` strike price for buy-put is `{self._buy_put[0].strike_price}`\nWhich is `{self._buy_put[1]}` from current price of `{self._latest_price}` (`{self._buy_put[2]}%`)"
                        }
                    }
                )

            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`{self._premium}` premium for buy options has a skew of `{round(self._buy_call[1] + self._buy_put[1], 2)}`"
                    }
                }
            )

        if not self._sell_call and not self._sell_put and not self._buy_call and not self._buy_put:
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"No Call/Put strike price exist for target premium : {self._premium}"
                    }
                }
            )

        return response