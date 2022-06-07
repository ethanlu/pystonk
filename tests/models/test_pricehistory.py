from pystonk.api.Types import FrequencyType
from pystonk.models.CandleStick import CandleStick
from pystonk.models.PriceHistory import PriceHistory


from datetime import datetime
from unittest import TestCase


class PriceHistoryTest(TestCase):
    def setUp(self) -> None:
        self._candlesticks = [
            CandleStick(100.00, 120.00, 80.00, 105.00, 100, int(datetime.strptime('2022-01-03', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY), # +5%
            CandleStick(100.00, 120.00, 80.00, 95.00, 100, int(datetime.strptime('2022-01-10', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY), # -5%
            CandleStick(100.00, 120.00, 80.00, 103.00, 100, int(datetime.strptime('2022-01-17', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY), # +3%
            CandleStick(100.00, 120.00, 80.00, 103.00, 100, int(datetime.strptime('2022-01-24', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY), # +3%
            CandleStick(100.00, 120.00, 80.00, 104.00, 100, int(datetime.strptime('2022-01-31', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # +4%
            CandleStick(100.00, 120.00, 80.00, 104.00, 100, int(datetime.strptime('2022-02-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # +4%
            CandleStick(100.00, 120.00, 80.00, 104.00, 100, int(datetime.strptime('2022-02-14', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # +4%
            CandleStick(100.00, 120.00, 80.00, 104.00, 100, int(datetime.strptime('2022-02-21', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # +4%
            CandleStick(100.00, 120.00, 80.00, 98.00, 100, int(datetime.strptime('2022-02-28', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -2%
            CandleStick(100.00, 120.00, 80.00, 90.00, 100, int(datetime.strptime('2022-03-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -10%
            CandleStick(100.00, 120.00, 80.00, 92.00, 100, int(datetime.strptime('2022-03-14', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -8%
            CandleStick(100.00, 120.00, 80.00, 92.00, 100, int(datetime.strptime('2022-03-21', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -8%
            CandleStick(100.00, 120.00, 80.00, 93.00, 100, int(datetime.strptime('2022-03-28', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -7%
        ]

    def testReport(self):
        percent = 4.0
        o = PriceHistory(self._candlesticks)

        self.assertEqual(o.countIntervals(), len(self._candlesticks), "PriceHistory did not return expected number of intervals")
        self.assertEqual(o.countIntervalsExceedPercentThreshold(percent), 10, "PriceHistory did not return expected number of intervals that exceeded threshold")
        self.assertEqual(o.percentProbability(percent), 76.92, "PriceHistory did not return expected percent probability")

    def testEmptyReport(self):
        percent = 11.0
        o = PriceHistory(self._candlesticks)

        self.assertEqual(o.countIntervals(), len(self._candlesticks), "PriceHistory did not return expected number of intervals")
        self.assertEqual(o.countIntervalsExceedPercentThreshold(percent), 0, "PriceHistory did not return expected number of intervals that exceeded threshold")
        self.assertEqual(o.percentProbability(percent), 0, "PriceHistory did not return expected percent probability")
