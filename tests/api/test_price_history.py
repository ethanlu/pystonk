from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.Types import FrequencyType, PeriodType
from pystonk.models.CandleStick import CandleStick

from datetime import datetime
from mock import MagicMock, patch
from typing import List
from unittest import TestCase


class PriceHistoryApiTest(TestCase):
    @patch.object(PriceHistoryApi, '_get')
    @patch.object(PriceHistoryApi, 'get_access_token')
    def testPriceHistory(self, mock_get_access_token, mock_get):
        mock_get.return_value = {
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
        mock_get_access_token.return_value = "some token"
        o = PriceHistoryApi("some key", "some secret")
        r = o.get_price_history(
            symbol="test",
            period_type=PeriodType.MONTH,
            period=1,
            frequency_type=FrequencyType.WEEKLY,
            frequency=1
        )

        self.assertEqual(mock_get.call_count, 1, "_get method was not called")
        self.assertEqual(mock_get_access_token.call_count, 1, "get_access_token method was not called")
        self.assertIsInstance(r, List, "PriceHistoryApi did not return list")
        self.assertEqual(4, len(r), "PriceHistoryApi did not return expected number of items")
        for k, v in enumerate(r):
            self.assertIsInstance(v, CandleStick, f"PriceHistoryApi did not return CandleStick for item {k}")
