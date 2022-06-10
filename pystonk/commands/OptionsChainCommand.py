from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.commands import Command
from pystonk.models.OptionsChain import OptionsChain
from pystonk.utils.CustomArgParser import CustomArgParser
from pystonk.utils import get_friday_of_week, get_third_friday_of_month, get_third_friday_of_quarter, get_third_friday_of_half
from pystonk.views import View
from pystonk.views.ErrorView import ErrorView
from pystonk.views.OptionsChainView import OptionsChainView

from argparse import Namespace
from calendar import monthrange
from datetime import date, timedelta
from typing import Type

import re


class OptionsChainCommand(Command):
    VALID_FREQUENCY_TYPES = ('current', 'week', 'month', 'quarter', 'half', 'year')
    DEFAULT_FREQUENCY_TYPE = 'week'

    def __init__(self, quote_api: QuoteApi, options_chain_api: OptionsChainApi):
        super().__init__()

        self._parser = CustomArgParser(
            add_help=False,
            description='get options chain of stock and show details of the option closest to specified premium without going below',
            exit_on_error=False,
            parents=[self.common_parser],
            prog='oc'
        )
        self._parser.add_argument(
            'symbol',
            type=str,
            help='stock symbol'
        )
        self._parser.add_argument(
            'target',
            type=float,
            help='target premium price or strike price percent change'
        )
        self._parser.add_argument(
            '-e', '--expiration',
            type=str,
            choices=self.VALID_FREQUENCY_TYPES,
            default=self.DEFAULT_FREQUENCY_TYPE,
            help=f"the next option to pick based on current week" +
                 f"\n\t\t\t\tchoose: `{'`, `'.join(self.VALID_FREQUENCY_TYPES)}`" +
                 f"\n\t\t\t\tdefault: `{self.DEFAULT_FREQUENCY_TYPE}`"
        )
        self._parser.add_argument(
            '-p', '--percent',
            action='store_true',
            help='use strike price percent change instead of premium for selecting closest option'
        )

        self._options_chain_api = options_chain_api
        self._quote_api = quote_api

    @property
    def command_regex(self) -> re.Pattern:
        return re.compile(r"^oc\s", re.IGNORECASE | re.ASCII)

    @property
    def parser(self) -> CustomArgParser:
        return self._parser

    def process(self, args: Namespace) -> Type[View]:
        symbol = args.symbol.upper()
        target = abs(round(args.target, 2))
        use_percent = args.percent
        expiration = args.expiration

        quote = self._quote_api.get_quote(symbol)

        if quote:
            today = date.today()
            if expiration == 'current':
                expire_date = get_friday_of_week(today)
            if expiration == 'week':
                expire_date = get_friday_of_week(today + timedelta(weeks=1))
            if expiration == 'month':
                expire_date = get_third_friday_of_month(today + timedelta(days=(monthrange(today.year, today.month)[1] + 1 - today.day)))
            if expiration == 'quarter':
                next_q = today.month + 3
                expire_date = get_third_friday_of_quarter(date(today.year if next_q < 12 else (today.year + 1), next_q if next_q < 12 else 1, 1))
            if expiration == 'half':
                next_h = today.month + 6
                expire_date = get_third_friday_of_quarter(date(today.year if next_h < 12 else (today.year + 1), next_h if next_h < 12 else 1, 1))
            if expiration == 'year':
                expire_date = get_third_friday_of_quarter(date(today.year + 1, today.month, today.day))

            return OptionsChainView(
                symbol=symbol,
                target=target,
                use_percent=use_percent,
                latest_price=quote.price,
                expiration=expiration,
                options_chain=OptionsChain(
                    quote.price,
                    self._options_chain_api.get_single_option_chain(
                        symbol=symbol,
                        expire_date=expire_date,
                        strike_count=500
                    )
                )
            )
        else:
            return ErrorView(f"{symbol} is not found...")
