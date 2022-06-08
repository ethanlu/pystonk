from pystonk.models.Quote import Quote

from unittest import TestCase


class QuoteTest(TestCase):
    def setUp(self):
        self._quote_data = {
            'symbol': 'TEST',
            'price': 1.234,
            'last_price': 5.678,
            'high_price': 5.001,
            'low_price': 10.002,
            'high_price_52': 1.03,
            'low_price_52': .33,
            'bid': 10.01,
            'ask': .52,
            'bid_size': 10,
            'ask_size': 3,
            'volume': 100
        }

    def testQuoteInstantiation(self):
        o = Quote(**self._quote_data)

        self.assertIsInstance(o, Quote)
        self.assertEqual(o.symbol, 'TEST')
        self.assertEqual(o.price, 1.23)
        self.assertEqual(o.last_price, 5.68)
        self.assertEqual(o.high_price, 5.00)
        self.assertEqual(o.low_price, 10.00)
        self.assertEqual(o.high_price_52week, 1.03)
        self.assertEqual(o.low_price_52week, .33)
        self.assertEqual(o.bid_price, 10.01)
        self.assertEqual(o.ask_price, .52)
        self.assertEqual(o.bid_size, 10)
        self.assertEqual(o.ask_size, 3)
        self.assertEqual(o.volume, 100)
