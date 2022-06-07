from pystonk.api.Types import FrequencyType, PeriodType
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.commands import Command
from pystonk.models.PriceHistory import PriceHistory
from pystonk.models.PriceHistoryEstimate import PriceHistoryEstimate
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

    @property
    def command_regex(self) -> re.Pattern:
        return re.compile(r"^ph\s", re.IGNORECASE | re.ASCII)

    @property
    def parser(self) -> CustomArgParser:
        return self._parser

    def process(self, args: Namespace) -> Type[View]:
        symbol = args.symbol.upper()
        percent = abs(round(args.percent, 2))

        candlesticks = self._price_history_api.getPriceHistory(
            symbol=symbol,
            period_type=PeriodType.YEAR,
            period=1,
            frequency_type=FrequencyType.WEEKLY,
            frequency=1
        )

        return PriceHistoryView(
            symbol=symbol,
            percent=percent,
            price_history=PriceHistory(candlesticks),
            price_history_estimate=PriceHistoryEstimate(candlesticks)
        )
