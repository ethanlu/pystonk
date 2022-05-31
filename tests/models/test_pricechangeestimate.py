from pystonk.api.Types import FrequencyType
from pystonk.models.CandleStick import CandleStick
from pystonk.models.PriceChangeEstimate import PriceChangeEstimate

from datetime import datetime
from unittest import TestCase


class PriceChangeEstimateTest(TestCase):
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
        o = PriceChangeEstimate(self.fixtureCandleSticks())

        self.assertIsInstance(o, PriceChangeEstimate)
        self.assertEqual(o.mean(), -.8, "PricechangeEstimate did not calculate expected mean")
        self.assertEqual(o.std(), 6.42, "PricechangeEstimate did not calculate expected STD")

        bins = o.histogramBins()
        self.assertEqual(len(bins), len(PriceChangeEstimate.BINS) - 1, "PriceChangeEstimate did not calculate expected number of histogram bins")
        self.assertTrue(bins[0] < 0, "PriceChangeEstimate did not start histogram bins at negative value")
        self.assertTrue(bins[-1] > 0, "PriceChangeEstimate did not end histogram bins at positive value")

        h = o.histogram()
        self.assertEqual(len(h), len(PriceChangeEstimate.BINS) - 1, "PriceChangeEstimate did not calculate expected number of histogram data")

        nh = o.histogram(normalize=True)
        self.assertEqual(len([v for v in nh if v <= 1.0]), len(PriceChangeEstimate.BINS) - 1,  "PriceChangeEstimate did not calculate expected number of normalized histogram data")

        self.assertNotEqual(o.percentProbability(15), o.percentProbability(15, weighted=False), "PriceChangeEstimate did not calculate percent propbability correctly for weighted and unweighted")
