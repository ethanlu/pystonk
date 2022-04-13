from pystonk.api.PriceHistory import PriceHistory
from pystonk.api.Types import FrequencyType, PeriodType
from pystonk.models.CandleStick import CandleStick

from datetime import datetime
from mock import MagicMock, patch
from typing import List
from unittest import TestCase


class PriceHistoryTest(TestCase):
    def setUp(self) -> None:
        self._mock_pricehistory_response = MagicMock()
        self._mock_pricehistory_response.json.return_value = {
            "candles": [
                {
                  "open": 10.00,
                  "high": 20.00,
                  "low": 5.00,
                  "close": 15.00,
                  "volume": 1000,
                  "datetime": 1577861060000
                },
                {
                    "open": 11.00,
                    "high": 21.00,
                    "low": 6.00,
                    "close": 16.00,
                    "volume": 1000,
                    "datetime": 1578465860000
                },
                {
                    "open": 12.00,
                    "high": 22.00,
                    "low": 7.00,
                    "close": 17.00,
                    "volume": 1000,
                    "datetime": 1579070660000
                },
                {
                    "open": 13.00,
                    "high": 23.00,
                    "low": 8.00,
                    "close": 18.00,
                    "volume": 1000,
                    "datetime": 1579675460000
                }
            ],
            "symbol": "TEST",
            "empty": False
        }

    def testPriceHistoryInvalidApiKey(self):
        self.assertRaisesRegex(ValueError, 'Invalid API Key : ', PriceHistory, '')

    @patch('pystonk.api.PriceHistory.requests')
    def testPriceHistory(self, requests_mock):
        requests_mock.get.return_value = self._mock_pricehistory_response
        o = PriceHistory('some key')
        r = o.getPriceHistory(
            symbol='test',
            period_type=PeriodType.MONTH,
            period=1,
            frequency_type=FrequencyType.WEEKLY,
            frequency=1
        )

        self.assertEqual(requests_mock.get.call_count, 1, "Mocked requests not called")
        self.assertIsInstance(r, List, "PriceHistory did not return list")
        self.assertEqual(4, len(r), "PriceHistory did not return expected number of items")
        for k, v in enumerate(r):
            self.assertIsInstance(v, CandleStick, f"PriceHistory did not return CandleStick for item {k}")

    @patch('pystonk.api.PriceHistory.requests')
    def testPriceHistoryWithDateRange(self, requests_mock):
        requests_mock.get.return_value = self._mock_pricehistory_response
        o = PriceHistory('some key')
        r = o.getPriceHistoryWithDateRange(
            symbol='test',
            start=datetime.strptime('2020-01-01', '%Y-%m-%d'),
            end=datetime.strptime('2020-02-01', '%Y-%m-%d'),
            period_type=PeriodType.MONTH,
            frequency_type=FrequencyType.WEEKLY,
            frequency=1
        )

        self.assertEqual(requests_mock.get.call_count, 1, "Mocked requests not called")
        self.assertIsInstance(r, List, "PriceHistory did not return list")
        self.assertEqual(4, len(r), "PriceHistory did not return expected number of items")
        for k, v in enumerate(r):
            self.assertIsInstance(v, CandleStick, f"PriceHistory did not return CandleStick for item {k}")