from pystonk.api.QuoteApi import QuoteApi
from pystonk.commands import Command
from pystonk.utils.CustomArgParser import CustomArgParser
from pystonk.views import View
from pystonk.views.PriceCheckView import PriceCheckView

from argparse import Namespace
from typing import Type

import re


class PriceCheckCommand(Command):
    def __init__(self, quote_api: QuoteApi):
        super().__init__()

        self._parser = CustomArgParser(
            add_help=False,
            description='get current price of stock',
            exit_on_error=False,
            parents=[self.common_parser],
            prog='pc'
        )
        self._parser.add_argument(
            'symbol',
            type=str,
            help='stock symbol'
        )

        self._quote_api = quote_api

    @property
    def command_regex(self) -> re.Pattern:
        return re.compile(r"^pc\s", re.IGNORECASE | re.ASCII)

    @property
    def parser(self) -> CustomArgParser:
        return self._parser

    def process(self, args: Namespace) -> Type[View]:
        symbol = args.symbol.upper()
        return PriceCheckView(symbol, self._quote_api.getQuote(symbol))
