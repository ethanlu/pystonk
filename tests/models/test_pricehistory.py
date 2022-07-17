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

        self.assertEqual(o.count_intervals(), len(self._candlesticks), "PriceHistory did not return expected number of intervals")
        self.assertEqual(o.count_intervals_exceed_percent_threshold(percent), 5, "PriceHistory did not return expected number of intervals that exceeded threshold")
        self.assertEqual(o.percent_rate(percent), 38.46, "PriceHistory did not return expected percent probability")

    def testEmptyReport(self):
        percent = 11.0
        o = PriceHistory(self._candlesticks)

        self.assertEqual(o.count_intervals(), len(self._candlesticks), "PriceHistory did not return expected number of intervals")
        self.assertEqual(o.count_intervals_exceed_percent_threshold(percent), 0, "PriceHistory did not return expected number of intervals that exceeded threshold")
        self.assertEqual(o.percent_rate(percent), 0, "PriceHistory did not return expected percent probability")

    def testCloseToClosePercentDifference(self):
        o = PriceHistory(self._candlesticks, False)
        self.assertEqual([5.0, -9.52, 8.42, 0.0, 0.97, 0.0, 0.0, 0.0, -5.77, -8.16, 2.22, 0.0, 1.09], o.percent_change_intervals(),
                         "PriceHistory did not return expected percent change intervals for close-to-close")

    def testOpenToClosePercentDifference(self):
        o = PriceHistory(self._candlesticks, True)
        self.assertEqual([5.0, -5.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, -2.0, -10.0, -8.0, -8.0, -7.0], o.percent_change_intervals(),
                         "PriceHistory did not return expected percent change intervals for start-to-close")