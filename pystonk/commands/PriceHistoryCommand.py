from pystonk.api.Types import FrequencyType, PeriodType
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.commands import Command
from pystonk.models.PriceHistory import PriceHistory
from pystonk.models.PriceHistoryEstimate import PriceHistoryEstimate
from pystonk.utils.CustomArgParser import CustomArgParser
from pystonk.views import View
from pystonk.views.ErrorView import ErrorView
from pystonk.views.PriceHistoryView import PriceHistoryView

from argparse import Namespace
from typing import Type

import re


class PriceHistoryCommand(Command):
    VALID_FREQUENCY_TYPES = (FrequencyType.DAILY.value, FrequencyType.WEEKLY.value, FrequencyType.MONTHLY.value)
    DEFAULT_FREQUENCY_TYPE = FrequencyType.WEEKLY.value
    VALID_PERIODS = (1, 2, 3, 5)
    DEFAULT_PERIOD = 1

    def __init__(self, quote_api: QuoteApi, price_history_api: PriceHistoryApi):
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
            help='percent threshold to exceed (greater than when positive, less than when negative)'
        )
        self._parser.add_argument(
            '-f', '--frequency',
            type=str,
            choices=self.VALID_FREQUENCY_TYPES,
            default=self.DEFAULT_FREQUENCY_TYPE,
            help=f"interval to use for displaying price changes " +
                 f"\n\t\t\t\tchoose: `{'`, `'.join(self.VALID_FREQUENCY_TYPES)}`" +
                 f"\n\t\t\t\tdefault: `{self.DEFAULT_FREQUENCY_TYPE}`"
        )
        self._parser.add_argument(
            '-p', '--period',
            type=int,
            choices=self.VALID_PERIODS,
            default=self.DEFAULT_PERIOD,
            help=f"time range of price changes (years or months)" +
                 f"\n\t\t\t\tchoose: `{'`, `'.join(map(str, self.VALID_PERIODS))}`" +
                 f"\n\t\t\t\tdefault : `{str(self.DEFAULT_PERIOD)}`" +
                 f"\n\t\t\t\tmonths for daily frequency, years for all others"
        )
        self._parser.add_argument(
            '-s', '--startend',
            action='store_true',
            help='calculate percent difference from interval start to interval end (instead of from previous interval end)'
        )

        self._quote_api = quote_api
        self._price_history_api = price_history_api

    @property
    def command_regex(self) -> re.Pattern:
        return re.compile(r"^ph\s", re.IGNORECASE | re.ASCII)

    @property
    def parser(self) -> CustomArgParser:
        return self._parser

    def process(self, args: Namespace) -> Type[View]:
        symbol = args.symbol.upper()
        percent = round(args.percent, 2)
        frequency_type = FrequencyType(args.frequency)
        period = args.period
        start_to_end = args.startend

        if self._quote_api.get_quote(symbol):
            period_type = PeriodType.YEAR
            if frequency_type == FrequencyType.DAILY:
                # switch to month period type if fequency is daily
                period_type = PeriodType.MONTH
                # period of 5 is only valid for weekly and monthly frequencies. for daily, period of 5 must be 6
                period = period if period != 5 else 6

            price_history = PriceHistory(self._price_history_api.get_price_history(
                symbol=symbol,
                period_type=period_type,
                period=period,
                frequency_type=frequency_type,
                frequency=1
            ), start_to_end)

            return PriceHistoryView(
                symbol=symbol,
                percent=percent,
                frequency_type=frequency_type,
                price_history=price_history,
                price_history_estimate=PriceHistoryEstimate(price_history.percent_change_intervals())
            )
        else:
            return ErrorView(f"{symbol} is not found...")
