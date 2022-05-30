from pystonk.api.Types import FrequencyType
from pystonk.models.CandleStick import CandleStick
from pystonk.reports.WeeklyPriceChangeReport import WeeklyPriceChangeReport


from datetime import datetime
from mock import MagicMock
from unittest import TestCase


class WeeklyPriceChangeReportTest(TestCase):
    def setUp(self) -> None:
        self._mock_api = MagicMock()
        self._mock_api.getPriceHistory.return_value = self.fixture3MonthApiResponse()

    def fixture3MonthApiResponse(self):
        return [
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

    def testRetrieveData(self):
        o = WeeklyPriceChangeReport(self._mock_api)
        o.retrieveData('test')
        self.assertEqual(self._mock_api.getPriceHistory.call_count, 1, "Mocked api not called expected amount of times")

    def testReport(self):
        percent = 4.0
        o = WeeklyPriceChangeReport(self._mock_api)
        o.retrieveData('test')
        r = list(o.generate(percent))

        self.assertEqual(o.totalWeeks(), len(self.fixture3MonthApiResponse()), "WeeklyPriceChangeReport did not return expected number of weeks")
        self.assertEqual(o.thresholdExceededWeeksTotal(percent), 10, "WeeklyPriceChangeReport did not return expected number of weeks that exceeded threshold")
        self.assertEqual(len(o.longestThresholdExceededWeeks(percent)), 4, "WeeklyPriceChangeReport did not return expected number for longest consecutive weeks that exceeded threshold")

        nd = o.normalDistribution(percent)
        self.assertEqual(-1, nd.mean, "WeeklyPriceChangeReport did not return expected normal distribution mean")
        self.assertEqual(5.55, round(nd.std, 2), "WeeklyPriceChangeReport did not return expected normal distribution std")
        self.assertEqual(.18, round(nd.pp, 2), "WeeklyPriceChangeReport did not return expected normal distribution percent probability")

    def testEmptyReport(self):
        percent = 11.0
        o = WeeklyPriceChangeReport(self._mock_api)
        o.retrieveData('test')
        r = list(o.generate(percent))

        self.assertEqual(o.totalWeeks(), len(self.fixture3MonthApiResponse()), "WeeklyPriceChangeReport did not return expected number of weeks")
        self.assertEqual(o.thresholdExceededWeeksTotal(percent), 0, "WeeklyPriceChangeReport did not return expected number of weeks that exceeded threshold")
        self.assertIsNone(o.longestThresholdExceededWeeks(percent), "WeeklyPriceChangeReport did not return expected None for longest consecutive weeks that exceeded threshold")