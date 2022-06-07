from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.commands import Command
from pystonk.reports.WeeklyOptionsReport import WeeklyOptionsReport
from pystonk.utils.CustomArgParser import CustomArgParser
from pystonk.views import View
from pystonk.views.OptionsChainView import OptionsChainView

from argparse import Namespace
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
        self._report = WeeklyOptionsReport(self._quote_api, self._options_chain_api)

    @property
    def command_regex(self) -> re.Pattern:
        return re.compile(r"^oc\s", re.IGNORECASE | re.ASCII)

    @property
    def parser(self) -> CustomArgParser:
        return self._parser

    def process(self, args: Namespace) -> Type[View]:
        symbol = args.symbol.upper()
        premium = abs(round(args.premium, 2))

        self._report.retrieveData(symbol)

        return OptionsChainView(
            symbol=symbol,
            premium=premium,
            report=self._report
        )
