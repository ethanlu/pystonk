import requests

from pystonk.api.QuoteApi import QuoteApi
from pystonk.models.Quote import Quote

from mock import MagicMock, patch
from pytest import mark
from requests import HTTPError
from unittest import TestCase



class QuoteApiTest(TestCase):
    @patch.object(QuoteApi, '_get')
    @patch.object(QuoteApi, 'get_access_token')
    def testQuote(self, mock_get_access_token, mock_get):
        mock_get.return_value = {
            'TEST': {
                'quote': {
                    'mark': 100.00,
                    'openPrice': 99.00,
                    'closePrice': 101.00,
                    'lastPrice': 99.99,
                    'lastPriceInDouble': 99.994,
                    'highPrice': 105.00,
                    'highPriceInDouble': 105.003,
                    '52WkHigh': 110.00,
                    '52WkHighInDouble': 110.0001,
                    '52WkLow': 93.00,
                    '52WkLowInDouble': 93.0009,
                    'bidPrice': 99.98,
                    'bidPriceInDouble': 99.981,
                    'askPrice': 100.50,
                    'askPriceInDouble': 100.502,
                    'bidSize': 10,
                    'askSize': 9,
                    'totalVolume': 100
                }
            }
        }
        mock_get_access_token.return_value = "some token"

        o = QuoteApi('some key', 'some secret')
        q = o.get_quote(symbol='TEST')

        self.assertEqual(mock_get.call_count, 1, "_get method was not called")
        self.assertEqual(mock_get_access_token.call_count, 1, "get_access_token method was not called")
        self.assertIsInstance(q, Quote, "QuoteApi did not return expected Quote object")
        self.assertEqual(q.price, 100.00, "Quote object did not return expected value")

    @patch.object(QuoteApi, '_get')
    @patch.object(QuoteApi, 'get_access_token')
    def testQuoteInvalid(self, mock_get_access_token, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.side_effect = HTTPError(400, response=mock_response)
        mock_get_access_token = "some token"

        o = QuoteApi('some key', 'some secret')
        q = o.get_quote(symbol='TEST')

        self.assertEqual(mock_get.call_count, 1, "_get method was not called")
        self.assertIsNone(q, "QuoteApi did not return expected empty")

    @patch.object(QuoteApi, '_get')
    @patch.object(QuoteApi, 'get_access_token')
    def testQuoteFail(self, mock_get_access_token, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.side_effect = HTTPError(500, response=mock_response)
        mock_get_access_token = "some token"

        with self.assertRaises(HTTPError):
            o = QuoteApi('some key', 'some secret')
            o.get_quote(symbol='TEST')
        self.assertTrue("QuoteApi did not throw expected error")
