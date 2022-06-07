from pystonk.api.Types import FrequencyType
from pystonk.models.CandleStick import CandleStick
from pystonk.models.PriceHistoryEstimate import PriceHistoryEstimate

from datetime import datetime
from unittest import TestCase


class PriceHistoryEstimateTest(TestCase):
    def setUp(self):
        pass

    def fixtureCandleSticks(self):
        return [
            CandleStick(100.00, 120.00, 80.00, 105.00, 100, int(datetime.strptime('2022-01-03', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY), # +5%
            CandleStick(100.00, 120.00, 80.00, 95.00, 100, int(datetime.strptime('2022-01-10', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY), # -5%
            CandleStick(100.00, 120.00, 80.00, 103.00, 100, int(datetime.strptime('2022-01-17', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY), # +3%
            CandleStick(100.00, 120.00, 80.00, 103.00, 100, int(datetime.strptime('2022-01-24', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY), # +3%
            CandleStick(100.00, 120.00, 80.00, 104.00, 100, int(datetime.strptime('2022-01-31', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # +4%
            CandleStick(100.00, 120.00, 80.00, 93.00, 100, int(datetime.strptime('2022-02-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # +4%
            CandleStick(100.00, 120.00, 80.00, 91.00, 100, int(datetime.strptime('2022-02-14', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # +4%
            CandleStick(100.00, 120.00, 80.00, 110.00, 100, int(datetime.strptime('2022-02-21', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # +4%
            CandleStick(100.00, 120.00, 80.00, 98.00, 100, int(datetime.strptime('2022-02-28', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -2%
            CandleStick(100.00, 120.00, 80.00, 90.00, 100, int(datetime.strptime('2022-03-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -10%
        ]

    def testPriceChangeInstantiation(self):
        o = PriceHistoryEstimate(self.fixtureCandleSticks())

        self.assertIsInstance(o, PriceHistoryEstimate)
        self.assertEqual(o.mean(), -.8, "PriceHistoryEstimate did not calculate expected mean")
        self.assertEqual(o.std(), 6.42, "PriceHistoryEstimate did not calculate expected STD")

        bins = o.histogramBins()
        self.assertTrue(bins[0] < 0, "PriceHistoryEstimate did not start histogram bins at negative value")
        self.assertTrue(bins[-1] > 0, "PriceHistoryEstimate did not end histogram bins at positive value")

        h = o.histogram()
        self.assertEqual(len(h), len(bins), "PriceHistoryEstimate did not calculate expected number of histogram data")

        self.assertEqual(o.percentProbability(15), .69, "PriceHistoryEstimate did not calculate percent probability correctly for weighted and unweighted")

        x, y = o.pdf()
        self.assertEqual(len(x), len(y), "PriceHistoryEstimate did not calculate pdf with expected values")
