from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.commands import Command
from pystonk.reports.WeeklyPriceChangeReport import WeeklyPriceChangeReport
from pystonk.utils.CustomArgParser import CustomArgParser
from pystonk.views import View
from pystonk.views.PriceHistoryView import PriceHistoryView

from argparse import Namespace
from typing import Type

import re


class PriceHistoryCommand(Command):
    def __init__(self, price_history_api: PriceHistoryApi):
        super().__init__()

        self._parser = CustomArgParser(
            add_help=False,
            description='get historical price changes of stock and makes note of any price change that exceeds the specified percent threshold',
            exit_on_error=False,
            parents=[self.common_parser],
            prog='ph'
        )
        self._parser.add_argument(
            'symbol',
            type=str,
            help='stock symbol'
        )
        self._parser.add_argument(
            'percent',
            type=float,
            help='percent threshold to exceed (absolute value)'
        )

        self._price_history_api = price_history_api
        self._report = WeeklyPriceChangeReport(self._price_history_api)

    @property
    def command_regex(self) -> re.Pattern:
        return re.compile(r"^ph\s", re.IGNORECASE | re.ASCII)

    @property
    def parser(self) -> CustomArgParser:
        return self._parser

    def process(self, args: Namespace) -> Type[View]:
        symbol = args.symbol.upper()
        percent = abs(round(args.percent, 2))

        self._report.retrieveData(symbol)

        return PriceHistoryView(
            symbol=symbol,
            percent=percent,
            report=self._report
        )
