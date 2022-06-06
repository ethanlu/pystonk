from pystonk.view import View

from prettytable import PrettyTable
from typing import Iterable, List, NamedTuple, Optional

import random


class OptionsChainView(View):
    def __init__(self, symbol: str, premium: float, current_price: float, data: Iterable, sell_options: Optional[NamedTuple], buy_options: Optional[NamedTuple]):
        super().__init__()
        self._symbol = symbol
        self._premium = premium
        self._current_price = current_price,
        self._data = data
        self._sell_options = sell_options
        self._buy_options = buy_options

    def show(self) -> List:
        t = PrettyTable()
        t.field_names = ('  ', 'Call Bid', 'Call Ask', 'Put Bid', 'Put Ask', 'Strike', '% Change')

        sell_call = sell_put = buy_call = buy_put = None
        if self._sell_options:
            sell_call = self._sell_options.call
            sell_put = self._sell_options.put
        if self._buy_options:
            buy_call = self._buy_options.call
            buy_put = self._buy_options.put

        for (strike_price, percent_change, call_option, put_option) in self._data:
            flag = ''
            if call_option == sell_call:
                flag += 'c'
            if call_option == buy_call:
                flag += 'C'
            if put_option == sell_put:
                flag += 'p'
            if put_option == buy_put:
                flag += 'P'

            t.add_row((
                flag,
                '%7.2f' % call_option.bid,
                '%7.2f' % call_option.ask,
                '%7.2f' % put_option.bid,
                '%7.2f' % put_option.ask,
                '%7.2f' % float(strike_price),
                '%7.2f' % percent_change,
            ))
        t.align = 'r'

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

        i = 0
        while i < len(t.rows):
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{t.get_string(start=i, end=i + self.SLACK_BLOCK_LIMIT)}```"
                    }
                }
            )
            i += self.SLACK_BLOCK_LIMIT

        if self._sell_options:
            response.append(
                {
                    "type": "divider"
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`c` : Closest `{self._sell_options.call.expirationDateTime.strftime('%Y-%m-%d')}` strike price for sell-call is `{self._sell_options.call.strikePrice}`\nWhich is `{self._sell_options.call_diff}` from current price of `{self._current_price}` (`{self._sell_options.call_diff_percent}%`)"
                    }
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`p` : Closest `{self._sell_options.put.expirationDateTime.strftime('%Y-%m-%d')}` strike price for sell-put is `{self._sell_options.put.strikePrice}`\nWhich is `{self._sell_options.put_diff}` from current price of `{self._current_price}` (`{self._sell_options.put_diff_percent}%`)"
                    }
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`{self._premium}` premium for sell options has a skew of `{round(self._sell_options.call_diff + self._sell_options.put_diff, 2)}`"
                    }
                }
            )

        if self._buy_options:
            response.append(
                {
                    "type": "divider"
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`C` : Closest `{self._buy_options.call.expirationDateTime.strftime('%Y-%m-%d')}` strike price for buy-call is `{self._buy_options.call.strikePrice}`\nWhich is `{self._buy_options.call_diff}` from current price of `{self._current_price}` (`{self._buy_options.call_diff_percent}%`)"
                    }
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`P` : Closest `{self._buy_options.put.expirationDateTime.strftime('%Y-%m-%d')}` strike price for buy-put is `{self._buy_options.put.strikePrice}`\nWhich is `{self._buy_options.put_diff}` from current price of `{self._current_price}` (`{self._buy_options.put_diff_percent}%`)"
                    }
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`{self._premium}` premium for buy options has a skew of `{round(self._buy_options.call_diff + self._buy_options.put_diff, 2)}`"
                    }
                }
            )

        if not self._sell_options and not self._buy_options:
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