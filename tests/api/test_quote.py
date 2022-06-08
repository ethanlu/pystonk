from pystonk.api.QuoteApi import QuoteApi
from pystonk.models.Quote import Quote

from unittest import TestCase
from mock import MagicMock, patch

class QuoteApiTest(TestCase):
    @patch('pystonk.api.QuoteApi.requests')
    def testQuote(self, requests_mock):
        response_mock = MagicMock()
        response_mock.json.return_value = {
            "TEST": {
                "mark": 100.00,
                "openPrice": 99.00,
                "closePrice": 101.00,
                "lastPrice": 99.99,
                "lastPriceInDouble": 99.994,
                "highPrice": 105.00,
                "highPriceInDouble": 105.003,
                "52WkHigh": 110.00,
                "52WkHighInDouble": 110.0001,
                "52WkLow": 93.00,
                "52WkLowInDouble": 93.0009,
                "bidPrice": 99.98,
                "bidPriceInDouble": 99.981,
                "askPrice": 100.50,
                "askPriceInDouble": 100.502,
                "bidSize": 10,
                "askSize": 9,
                "totalVolume": 100
            }
        }
        requests_mock.get.return_value = response_mock

        o = QuoteApi('some key')
        q = o.get_quote(symbol='TEST')

        self.assertEqual(requests_mock.get.call_count, 1, "Mocked requests not called")
        self.assertIsInstance(q, Quote, "QuoteApi did not return expected Quote object")

    @patch('pystonk.api.QuoteApi.requests')
    def testQuoteEmpty(self, requests_mock):
        response_mock = MagicMock()
        response_mock.json.return_value = {}
        requests_mock.get.return_value = response_mock

        o = QuoteApi('some key')
        q = o.get_quote(symbol='TEST')

        self.assertEqual(requests_mock.get.call_count, 1, "Mocked requests not called")
        self.assertIsNone(q, "Quote did not return expected None")
