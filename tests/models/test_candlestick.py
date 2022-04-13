from pystonk.api.Types import FrequencyType
from pystonk.models.CandleStick import CandleStick

from datetime import datetime
from unittest import TestCase


class CandleStickTest(TestCase):
    def setUp(self):
        self._weekly_candlestick_data = {
            'open_price': 5.001,
            'high_price': 10.002,
            'low_price': 1.003,
            'close_price': 7.504,
            'volume': 100,
            'start_datetime': datetime.strptime('2020-01-01', '%Y-%m-%d').timestamp() * 1000,
            'frequency_type': FrequencyType.WEEKLY
        }

    def testCandleStickInstantiation(self):
        o = CandleStick(**self._weekly_candlestick_data)

        self.assertIsInstance(o, CandleStick)
        self.assertEqual(o.openPrice, 5.00, "CandleStick did not normalize open price")
        self.assertEqual(o.highPrice, 10.00, "CandleStick did not normalize high price")
        self.assertEqual(o.lowPrice, 1.00, "CandleStick did not normalize low price")
        self.assertEqual(o.closePrice, 7.50, "CandleStick did not normalize close price")
        self.assertEqual(o.volume, 100, "CandleStick did not normalize volume")
        self.assertEqual(
            o.startDateTime.timestamp(), datetime.strptime('2020-01-01','%Y-%m-%d').timestamp(),
            "CandleStick did not normalize start datetime"
        )
        self.assertEqual(o.frequencyType, FrequencyType.WEEKLY, "CandleStick did not normalize frequency type")
        self.assertEqual(o.percentChange, 50.00, "CandleStick did not calculate percent change correctly")