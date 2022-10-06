from pystonk.models.SupportResistanceSearch import SupportResistanceSearch
from pystonk.views import View

from datetime import date
from prettytable import PrettyTable
from typing import Dict, List, Tuple

import random


class SupportResistanceView(View):
    def __init__(self, symbol: str, time_frame: str, support_resistance_search: SupportResistanceSearch):
        super().__init__()

        self._symbol = symbol
        self._time_frame = time_frame
        self._sr = support_resistance_search

        self._t = PrettyTable()
        self._t.field_names = ('Type', 'Price', 'Datetime')
        self._t.align = 'r'

        self._grouped_t = PrettyTable()
        self._grouped_t.field_names = ('Type', 'Price', 'Datetime')
        self._grouped_t.align = 'r'

    def _build_sr_table(self) -> List[Dict]:
        rows = []
        for i, s in enumerate(reversed(self._sr.supports())):
            rows.append((
                'Support',
                s.close_price,
                s.start_datetime.strftime('%Y-%m-%d %H:%M:%S')
            ))
            if not self._verbose and i > 3:
                break
        for i, r in enumerate(reversed(self._sr.resistances())):
            rows.append((
                'Resistance',
                r.close_price,
                r.start_datetime.strftime('%Y-%m-%d %H:%M:%S')
            ))
            if not self._verbose and i > 3:
                break
        self._t.add_rows(rows)

        return self.paginate(self._t)

    def show_text(self) -> str:
        return f"supports and resistances for {self._symbol} with cannot be shown in text-only mode"

    def show(self) -> List[Dict]:
        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n Here are the `{self._time_frame}` supports and resistances for `{self._symbol}`)"
                }
            },
            {
                "type": "divider"
            },
        ]
        response += self._build_sr_table()

        return response
