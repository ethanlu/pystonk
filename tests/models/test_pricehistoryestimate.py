from pystonk.api.Types import FrequencyType
from pystonk.models.CandleStick import CandleStick
from pystonk.models.PriceHistoryEstimate import PriceHistoryEstimate
from pystonk.utils import percent_diff

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
            CandleStick(100.00, 120.00, 80.00, 93.00, 100, int(datetime.strptime('2022-02-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -7%
            CandleStick(100.00, 120.00, 80.00, 91.00, 100, int(datetime.strptime('2022-02-14', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -9%
            CandleStick(100.00, 120.00, 80.00, 110.00, 100, int(datetime.strptime('2022-02-21', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # +10%
            CandleStick(100.00, 120.00, 80.00, 98.00, 100, int(datetime.strptime('2022-02-28', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -2%
            CandleStick(100.00, 120.00, 80.00, 90.00, 100, int(datetime.strptime('2022-03-07', '%Y-%m-%d').timestamp() * 1000), FrequencyType.WEEKLY),  # -10%
        ]

    def testPriceChangeInstantiation(self):
        o = PriceHistoryEstimate([percent_diff(d.open_price, d.close_price) for d in self.fixtureCandleSticks()])

        self.assertIsInstance(o, PriceHistoryEstimate)
        self.assertEqual(o.min(), -10.0, "PriceHistoryEstimate did not calculate expected min")
        self.assertEqual(o.max(), 10.0, "PriceHistoryEstimate did not calculate expected max")
        self.assertEqual(o.mean(), -.8, "PriceHistoryEstimate did not calculate expected mean")
        self.assertEqual(o.std(), 6.42, "PriceHistoryEstimate did not calculate expected STD")

        bins = o.histogram_bins()
        self.assertEqual(bins, [-10.5, -9.5, -8.5, -7.5, -6.5, -5.5, -4.5, -3.5, -2.5, -1.5, -.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5], "PriceHistoryEstimate did not calculate expected bins for histogram")
        self.assertTrue(bins[0] < 0, "PriceHistoryEstimate did not start histogram bins at negative value")
        self.assertTrue(bins[-1] > 0, "PriceHistoryEstimate did not end histogram bins at positive value")

        h = o.histogram()
        self.assertEqual(len(h), len(bins), "PriceHistoryEstimate did not calculate expected number of histogram data")
        self.assertEqual(1.0, o.histogram_bins_interval(), "PriceHistoryEstimate did not calculate expected histogram bin interval")

        self.assertEqual(o.percent_probability(15), .69, "PriceHistoryEstimate did not calculate percent probability correctly for weighted and unweighted")
        self.assertEqual(o.percent_probability(-15), 1.34, "PriceHistoryEstimate did not calculate percent probability correctly for weighted and unweighted")

        x, y = o.pdf()
        self.assertEqual(len(x), len(y), "PriceHistoryEstimate did not calculate pdf with expected values")
