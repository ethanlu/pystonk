from pystonk.api.Types import ContractType
from pystonk.models.OptionContract import OptionContract

from unittest import TestCase


class OptionContractTest(TestCase):
    def testOptionContractInstantiation(self):
        o = OptionContract(**{
            "put_call": 'CALL',
            "symbol": "test_010122C100",
            "description": "TEST Jan 01 2022 100 Call",
            "bid": 100.7,
            "ask": 103.4,
            "bid_ask_size": "3X4",
            "volatility": 127.504,
            "delta": 1,
            "gamma": 0,
            "theta": -0.144,
            "vega": 0,
            "rho": 0.005,
            "open_interest": 5,
            "strike_price": 100,
            "expiration_datetime": 1641603600000,
            "last_trading_datetime": 1641690000000,
            "in_the_money": True,
            "non_standard": False
        })

        self.assertIsInstance(o, OptionContract)
        self.assertEqual(o.symbol, 'TEST_010122C100', 'OptionContract did not normalize symbol')
        self.assertEqual(o.contractType, ContractType.CALL, 'OptionContract did not normalize contract type')
        self.assertEqual(o.description, 'TEST Jan 01 2022 100 Call', 'OptionContract did not normalize description')
        self.assertEqual(o.bid, 100.70, 'OptionContract did not normalize bid')
        self.assertEqual(o.ask, 103.40, 'OptionContract did not normalize ask')
        self.assertEqual(o.bidSize, 3, 'OptionContract did not normalize bid size')
        self.assertEqual(o.askSize, 4, 'OptionContract did not normalize ask size')
        self.assertEqual(o.volatility, 127.50, 'OptionContract did not normalize volatility')
        self.assertEqual(o.delta, 1.00, 'OptionContract did not normalize delta')
        self.assertEqual(o.gamma, 0.00, 'OptionContract did not normalize gamma')
        self.assertEqual(o.theta, -0.14, 'OptionContract did not normalize theta')
        self.assertEqual(o.vega, 0.00, 'OptionContract did not normalize vega')
        self.assertEqual(o.rho, .01, 'OptionContract did not normalize rho')
        self.assertEqual(o.openInterest, 5, 'OptionContract did not normalize open interest')
        self.assertEqual(o.strikePrice, 100.00, 'OptionContract did not normalize strike price')
        self.assertTrue(o.isITM, 'OptionContract did not normalize ITM')
        self.assertFalse(o.isNonstandard, 'OptionContract did not normalize non-standard')
        self.assertEqual(o._expiration_datetime.timestamp(), 1641603600, 'OptionContract did not normalize expiration datetime')
        self.assertEqual(o._last_trading_datetime.timestamp(), 1641690000, 'OptionContract did not normalize last trading datetime')

class OptionContractNaNTest(TestCase):
    def testOptionContractInstantiation(self):
        o = OptionContract(**{
            "put_call": 'CALL',
            "symbol": "test_010122C100",
            "description": "TEST Jan 01 2022 100 Call",
            "bid": 100.7,
            "ask": 103.4,
            "bid_ask_size": "3X4",
            "volatility": "NaN",
            "delta": "NaN",
            "gamma": "NaN",
            "theta": "NaN",
            "vega": "NaN",
            "rho": "NaN",
            "open_interest": 5,
            "strike_price": 100,
            "expiration_datetime": 1641603600000,
            "last_trading_datetime": 1641690000000,
            "in_the_money": True,
            "non_standard": False
        })

        self.assertIsInstance(o, OptionContract)
        self.assertEqual(o.volatility, 0.00, 'OptionContract did not normalize NaN volatility')
        self.assertEqual(o.delta, 0.00, 'OptionContract did not normalize NaN delta')
        self.assertEqual(o.gamma, 0.00, 'OptionContract did not normalize NaN gamma')
        self.assertEqual(o.theta, 0.00, 'OptionContract did not normalize NaN theta')
        self.assertEqual(o.vega, 0.00, 'OptionContract did not normalize NaN vega')
        self.assertEqual(o.rho, 0.00, 'OptionContract did not normalize NaN rho')