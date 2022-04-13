from pystonk.api.PriceHistory import PriceHistory
from pystonk.api.types.FrequencyType import FrequencyType
from pystonk.api.types.PeriodType import PeriodType
from pystonk.common.LoggerMixin import LoggerMixin
from pystonk.common.models.CandleStick import CandleStick

from itertools import groupby
from typing import Any, Generator, List, Optional, Tuple


class WeeklyPriceChangeReport(LoggerMixin):
    def __init__(self, api: PriceHistory):
        self._api = api
        self._candlesticks: List[CandleStick] = []

    def retrieveData(self, symbol: str) -> None:
        symbol = symbol.upper()

        # get last 1 year worth of weekly price changes
        self._candlesticks = self._api.getPriceHistory(
            symbol=symbol,
            period_type=PeriodType.YEAR,
            period=1,
            frequency_type=FrequencyType.WEEKLY,
            frequency=1
        )

    def generate(self, percent_threshold: float) -> Generator[Tuple[int, CandleStick], Any, None]:
        '''
        generator that returns at tuple of a group identifier and weekly price change data. group identifier is used to
        group consecutive weeks that exceed the given threshold. group identifier 0 indicates a week that did not exceed
        the threshold
        :param percent_threshold:
        :return:
        '''
        percent_threshold = round(abs(percent_threshold), 2)

        threshold_group = 0
        last_threshold_i = -1
        total_weeks = len(self._candlesticks)
        i = 0
        while i < total_weeks:
            if abs(self._candlesticks[i].percentChange) >= percent_threshold:
                if last_threshold_i < 0 or (i - last_threshold_i) != 1:
                    threshold_group += 1

                yield(threshold_group, self._candlesticks[i])

                last_threshold_i = i
            else:
                yield (0, self._candlesticks[i])
            i += 1

        return None

    def totalWeeks(self) -> int:
        return len(self._candlesticks)

    def thresholdExceededWeeksTotal(self, percent_threshold: float) -> int:
        return len([1 for (group, week) in self.generate(percent_threshold) if group > 0])

    def longestThresholdExceededWeeks(self, percent_threshold: float) -> Optional[List[Tuple[str, CandleStick]]]:
        grouped_threshold_weeks = [(k, list(v)) for k, v in groupby(((group, week) for (group, week) in self.generate(percent_threshold) if group > 0), lambda x: x[0])]

        if grouped_threshold_weeks:
            return max(grouped_threshold_weeks, key=lambda x: len(x[1]))[1]
        else:
            return None

