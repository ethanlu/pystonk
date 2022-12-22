from pystonk.models.OptionsChain import OptionsChain
from pystonk.views import View

from datetime import date
from prettytable import PrettyTable
from typing import Dict, List, Tuple

import random


class OptionsChainView(View):
    def __init__(self, symbol: str, target: float, use_percent: bool, latest_price: float, expiration: str, expiration_date: date, options_chain: OptionsChain):
        super().__init__()

        self._symbol = symbol
        self._target = target
        self._use_percent = use_percent
        self._latest_price = latest_price
        self._expiration_date = expiration_date
        self._expiration = f"this {self._expiration_date.strftime('%A')}" if expiration == 'current' else f"next {expiration}"
        self._options_chain = options_chain

        if self._use_percent:
            self._buy_call = self._sell_call = self._options_chain.closest_call_option_by_percent(self._target)
            self._buy_put = self._sell_put = self._options_chain.closest_put_option_by_percent(self._target)
        else:
            self._sell_call = self._options_chain.closest_call_option_by_premium(self._target)
            self._buy_call = self._options_chain.closest_call_option_by_premium(self._target, is_sell=False)
            self._sell_put = self._options_chain.closest_put_option_by_premium(self._target)
            self._buy_put = self._options_chain.closest_put_option_by_premium(self._target, is_sell=False)

        # options table
        self._t = PrettyTable()
        self._t.field_names = ('  ', 'Call Bid', 'Call Ask', 'Put Bid', 'Put Ask', 'Strike', '% Change')
        self._t.align = 'r'

    def _format_target(self):
        return f"percent change `{self._target}%`" if self._use_percent else f"premium `${self._target}`"

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

    def _build_target_options(self, c: Tuple, p: Tuple, last_price: float, is_sell: bool = True) -> List[Dict]:
        if c or p:
            info = []
            if c:
                info.append(
                    f"*Call*: `${c[0].bid if is_sell else c[0].ask}` @ `{c[0].strike_price}` on `{c[0].expiration_datetime.strftime('%Y-%m-%d')}` (`{c[2]}%` from `{last_price}`)")
            if p:
                info.append(
                    f"*Put*: `${p[0].bid if is_sell else p[0].ask}` @ `{p[0].strike_price}` on `{p[0].expiration_datetime.strftime('%Y-%m-%d')}` (`{p[2]}%` from `{last_price}`)")

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
        return f"option chain for {self._symbol} with {self._target} target cannot be shown in text-only mode"

    def show(self) -> List[Dict]:
        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n Here is the options chain for `{self._symbol}` with target {self._format_target()} that expires `{self._expiration}` (on `{self._expiration_date.strftime('%Y-%m-%d')}`)"
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
                    "text": f"Closest options to sell at the target {self._format_target()}"
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
                    "text": f"Closest options to buy at the target {self._format_target()}"
                }
            }
        ]
        response += self._build_target_options(self._buy_call, self._buy_put, self._latest_price, is_sell=False)

        return response
