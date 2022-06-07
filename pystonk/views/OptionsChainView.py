from pystonk.reports.WeeklyOptionsReport import WeeklyOptionsReport
from pystonk.views import View

from prettytable import PrettyTable
from typing import Dict, Iterable, List, NamedTuple, Optional

import random


class OptionsChainView(View):
    def __init__(self, symbol: str, premium: float, report: WeeklyOptionsReport):
        super().__init__()

        self._symbol = symbol
        self._premium = premium
        self._report = report

        self._current_price = self._report.getMark(),
        self._data = self._report.generate()
        self._sell_options = self._report.getStrikePricesForTargetPremium(self._premium)
        self._buy_options = self._report.getStrikePricesForTargetPremium(premium, is_sell=False)

        # options table
        self._t = PrettyTable()
        self._t.field_names = ('  ', 'Call Bid', 'Call Ask', 'Put Bid', 'Put Ask', 'Strike', '% Change')

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