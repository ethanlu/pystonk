from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.commands import Command
from pystonk.models.OptionsChain import OptionsChain
from pystonk.utils.CustomArgParser import CustomArgParser
from pystonk.views import View
from pystonk.views.OptionsChainView import OptionsChainView

from argparse import Namespace
from datetime import date
from typing import Type

import re


class OptionsChainCommand(Command):
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
            'premium',
            type=float,
            help='target premium price'
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
        premium = abs(round(args.premium, 2))

        latest_price = self._quote_api.getQuote(symbol)

        return OptionsChainView(
            symbol=symbol,
            premium=premium,
            latest_price=latest_price,
            options_chain=OptionsChain(
                latest_price,
                self._options_chain_api.getWeeklySingleOptionChain(
                    symbol=symbol,
                    week_date=date.today(),
                    strike_count=200
                )
            )
        )
