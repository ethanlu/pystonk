from pystonk.api.QuoteApi import QuoteApi

from unittest import TestCase
from mock import MagicMock, patch

class QuoteTest(TestCase):
    @patch('pystonk.api.QuoteApi.requests')
    def testQuote(self, requests_mock):
        response_mock = MagicMock()
        response_mock.json.return_value = {
            "TEST": {
                "mark": 100.00
            }
        }
        requests_mock.get.return_value = response_mock

        o = QuoteApi('some key')
        r = o.getQuote(
            symbol='test'
        )

        self.assertEqual(requests_mock.get.call_count, 1, "Mocked requests not called")
        self.assertEqual(r, 100.00, "Quote did not return expected mark")

    @patch('pystonk.api.QuoteApi.requests')
    def testQuoteEmpty(self, requests_mock):
        response_mock = MagicMock()
        response_mock.json.return_value = {}
        requests_mock.get.return_value = response_mock

        o = QuoteApi('some key')
        r = o.getQuote(
            symbol='test'
        )

        self.assertEqual(requests_mock.get.call_count, 1, "Mocked requests not called")
        self.assertIsNone(r, "Quote did not return expected None")