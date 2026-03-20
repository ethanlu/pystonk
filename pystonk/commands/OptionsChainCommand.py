from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.commands import Command
from pystonk.models.OptionsChain import OptionsChain
from pystonk.services import resolve_option_expiration
from pystonk.utils.CustomArgParser import CustomArgParser
from pystonk.views import View
from pystonk.views.ErrorView import ErrorView
from pystonk.views.OptionsChainView import OptionsChainView

from argparse import Namespace
from datetime import date
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
            expire_date = resolve_option_expiration(symbol, expiration, date.today())

            return OptionsChainView(
                symbol=symbol,
                target=target,
                use_percent=use_percent,
                latest_price=quote.price,
                expiration=expiration,
                expiration_date=expire_date,
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
