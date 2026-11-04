from pystonk.api.Types import FrequencyType
from pystonk.models.CandleStick import CandleStick
from pystonk.models.PriceHistoryAnalysis import PriceHistoryAnalysis
from pystonk.utils import percent_diff

from datetime import datetime
from io import BytesIO
from unittest import TestCase


class PriceHistoryAnalysisTest(TestCase):
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

    def testPriceChangePrivateFunctions(self):
        o = PriceHistoryAnalysis([percent_diff(d.open_price, d.close_price) for d in self.fixtureCandleSticks()])

        self.assertEqual(round(o._normal_cdf(-5, -.8, 6.42), 5), .25649, "PriceHistoryAnalysis._normal_cdf did not calculate expected value")
        self.assertEqual(round(o._normal_cdf(5, -.8, 6.42), 5), .81685, "PriceHistoryAnalysis._normal_cdf did not calculate expected value")

        self.assertEqual(round(o._normal_pdf(2.5, -.8, 6.42), 5), .05445, "PriceHistoryAnalysis._normal_pdf did not calculate expected value")
        self.assertEqual(round(o._normal_pdf(-2.5, -.8, 6.42), 5), .06000, "PriceHistoryAnalysis._normal_pdf did not calculate expected value")

        self.assertGreater(o._normal_ppf(.51), 0, "PriceHistoryAnalysis._normal_ppf did not calculate expected value")
        self.assertLess(o._normal_ppf(.5), 0, "PriceHistoryAnalysis._normal_ppf did not calculate expected value")
        self.assertLess(o._normal_ppf(.49), 0, "PriceHistoryAnalysis._normal_ppf did not calculate expected value")
        for v in (1.0, 1.1, 0.0, -.01):
            with self.assertRaises(ValueError):
                o._normal_ppf(v)
                self.assertFalse(f"PriceHistoryAnalysis._normal_ppf did not throw error for invalid input {v}")

    def testPriceChangeInstantiationAndGetters(self):
        o = PriceHistoryAnalysis([percent_diff(d.open_price, d.close_price) for d in self.fixtureCandleSticks()])

        self.assertIsInstance(o, PriceHistoryAnalysis)
        self.assertEqual(o.min(), -10.0, "PriceHistoryAnalysis did not calculate expected min")
        self.assertEqual(o.max(), 10.0, "PriceHistoryAnalysis did not calculate expected max")
        self.assertEqual(o.mean(), -.8, "PriceHistoryAnalysis did not calculate expected mean")
        self.assertEqual(o.std(), 6.42, "PriceHistoryAnalysis did not calculate expected STD")
        self.assertEqual(o.skew(), .01, "PriceHistoryAnalysis did not calculate expected skew")
        self.assertEqual(o.kurtosis(), -1.28, "PriceHistoryAnalysis did not calculate expected kurtosis")
        self.assertEqual(o.percent_probability(5.0), 18.31, "PriceHistoryAnalysis did not calculate expected percent_probability")
        self.assertEqual(o.percent_probability(-5.0), 25.65, "PriceHistoryAnalysis did not calculate expected percent_probability")

    def testPriceChangeImageGeneration(self):
        o = PriceHistoryAnalysis([percent_diff(d.open_price, d.close_price) for d in self.fixtureCandleSticks()])

        h = o.histogram()
        self.assertIsInstance(h, BytesIO)
        self.assertTrue(h.getvalue(), "PriceHistoryAnalysis did not generate a valid histogram chart")

        q = o.qq()
        self.assertIsInstance(q, BytesIO)
        self.assertTrue(q.getvalue(), "PriceHistoryAnalysis did not generate a valid q-q plot chart")
