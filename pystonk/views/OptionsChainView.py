from pystonk.models.OptionsChain import OptionsChain
from pystonk.views import View

from prettytable import PrettyTable
from typing import Dict, List, Tuple

import random


class OptionsChainView(View):
    def __init__(self, symbol: str, premium: float, latest_price: float, expiration: str, options_chain: OptionsChain):
        super().__init__()

        self._symbol = symbol
        self._premium = premium
        self._latest_price = latest_price
        self._expiration = 'this week' if expiration == 'current' else f"next {expiration}"
        self._options_chain = options_chain

        self._sell_call = self._options_chain.closest_call_option(self._premium)
        self._buy_call = self._options_chain.closest_call_option(self._premium, is_sell=False)

        self._sell_put = self._options_chain.closest_put_option(self._premium)
        self._buy_put = self._options_chain.closest_put_option(self._premium, is_sell=False)

        # options table
        self._t = PrettyTable()
        self._t.field_names = ('  ', 'Call Bid', 'Call Ask', 'Put Bid', 'Put Ask', 'Strike', '% Change')
        self._t.align = 'r'

    def _build_table(self) -> List[Dict]:
        rows = []
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

            if self._verbose or flag:
                rows.append((
                    flag,
                    '%7.2f' % call_option.bid,
                    '%7.2f' % call_option.ask,
                    '%7.2f' % put_option.bid,
                    '%7.2f' % put_option.ask,
                    '%7.2f' % float(strike_price),
                    '%7.2f' % percent_change,
                ))
        self._t.add_rows(rows)

        return self.paginate(self._t)

    def _build_target_options(self, c: Tuple, p: Tuple, last_price: float) -> List[Dict]:
        if c or p:
            info = []
            if c:
                info.append(
                    f"*Call*: `${c[0].bid}` @ `{c[0].strike_price}` on `{c[0].expiration_datetime.strftime('%Y-%m-%d')}` (`{c[2]}%` from `{last_price}`)")
            if p:
                info.append(
                    f"*Put*: `${p[0].ask}` @ `{p[0].strike_price}` on `{p[0].expiration_datetime.strftime('%Y-%m-%d')}` (`{p[2]}%` from `{last_price}`)")

            if c and p:
                info.append(f"*Skew*: `{round(c[1] + p[1], 2)}`")

            return [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "\n".join(info)
                    }
                }
            ]
        else:
            return []

    def show_text(self) -> str:
        return f"option chain for {self._symbol} with {self._premium} premium cannot be shown in text-only mode"

    def show(self) -> List[Dict]:
        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n Here is the options chain for `{self._symbol}` with target premium `{self._premium}` that expires `{self._expiration}`"
                }
            },
            {
                "type": "divider"
            },
        ]
        response += self._build_table()

        response += [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Closest options to sell at the target premium `{self._premium}`"
                }
            }
        ]
        response += self._build_target_options(self._sell_call, self._sell_put, self._latest_price)

        response += [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Closest options to buy at the target premium `{self._premium}`"
                }
            }
        ]
        response += self._build_target_options(self._buy_call, self._buy_put, self._latest_price)

        return response
