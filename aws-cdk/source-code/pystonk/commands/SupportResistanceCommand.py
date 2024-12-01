from pystonk.api.Types import FrequencyType, PeriodType
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.commands import Command
from pystonk.models.SupportResistanceSearch import SupportResistanceSearch
from pystonk.utils.CustomArgParser import CustomArgParser
from pystonk.views import View
from pystonk.views.SupportResistanceView import SupportResistanceView

from argparse import Namespace
from typing import Type

import re


class SupportResistanceCommand(Command):
    VALID_TIME_FRAME_TYPE = ('minute', 'daily', 'weekly')
    DEFAULT_TIME_FRAME_TYPE = 'daily'

    def __init__(self, price_history_api: PriceHistoryApi):
        super().__init__()

        self._parser = CustomArgParser(
            add_help=False,
            description='get support & resistance prices of stock in the specified timeframe',
            exit_on_error=False,
            parents=[self.common_parser],
            prog='sr'
        )
        self._parser.add_argument(
            'symbol',
            type=str,
            help='stock symbol'
        )
        self._parser.add_argument(
            'time_frame',
            type=str,
            choices=self.VALID_TIME_FRAME_TYPE,
            default=self.DEFAULT_TIME_FRAME_TYPE,
            help=f"time frame to look for support and resistance prices" +
                 f"\n\t\t\t\tchoose: `{'`, `'.join(map(str, self.VALID_TIME_FRAME_TYPE))}`" +
                 f"\n\t\t\t\tdefault : `{str(self.DEFAULT_TIME_FRAME_TYPE)}`"
                 f"\n\t\t\t\tminute time frame looks for the last 24 hours worth of price changes in 5 minute intervals" +
                 f"\n\t\t\t\tdaily time frame looks for the last 3 months worth of price changes in 1 day intervals" +
                 f"\n\t\t\t\tweekly time frame looks for the last 1 year worth of price changes in 1 week intervals"
        )

        self._price_history_api = price_history_api

    @property
    def command_regex(self) -> re.Pattern:
        return re.compile(r"^sr\s", re.IGNORECASE | re.ASCII)

    @property
    def parser(self) -> CustomArgParser:
        return self._parser

    def process(self, args: Namespace) -> Type[View]:
        symbol = args.symbol.upper()
        time_frame = args.time_frame.lower()

        if time_frame == 'minute':
            period_type = PeriodType.DAY
            period = 1
            frequency_type = FrequencyType.MINUTE
            frequency = 5
        if time_frame == 'daily':
            period_type = PeriodType.MONTH
            period = 3
            frequency_type = FrequencyType.DAILY
            frequency = 1
        if time_frame == 'weekly':
            period_type = PeriodType.YEAR
            period = 1
            frequency_type = FrequencyType.WEEKLY
            frequency = 1

        return SupportResistanceView(
            symbol=symbol,
            time_frame=time_frame,
            support_resistance_search=SupportResistanceSearch(self._price_history_api.get_price_history(
                symbol=symbol,
                period_type=period_type,
                period=period,
                frequency_type=frequency_type,
                frequency=frequency
            ))
        )
