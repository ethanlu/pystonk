from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.Types import ContractType, OptionType, StrategyType
from pystonk.models.OptionContract import OptionContract

from datetime import date
from mock import MagicMock, patch
from typing import Dict, Tuple
from unittest import TestCase


class OptionsChainApiTest(TestCase):
    def setUp(self) -> None:
        self._mock_optionschain_response = MagicMock()
        self._mock_optionschain_response.json.return_value = {
            "callExpDateMap": {
                "2020-01-03:1": {
                    "90.00": [
                        {
                            "putCall": "CALL",
                            "symbol": "TEST_010320C90",
                            "description": "TEST Jan 03 2020 90 Call (Weekly)",
                            "bid": 0.01,
                            "ask": 0.02,
                            "bidAskSize": "9X9",
                            "volatility": 152.024,
                            "delta": -0.003,
                            "gamma": 0.001,
                            "theta": -0.004,
                            "vega": 0.001,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 90,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": True,
                            "nonStandard": False
                        }
                    ],
                    "95.00": [
                        {
                            "putCall": "CALL",
                            "symbol": "TEST_010320C95",
                            "description": "TEST Jan 03 2020 95 Call (Weekly)",
                            "bid": 0.02,
                            "ask": 0.03,
                            "bidAskSize": "10X10",
                            "volatility": 160.024,
                            "delta": -0.003,
                            "gamma": 0.001,
                            "theta": -0.004,
                            "vega": 0.002,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 95,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": True,
                            "nonStandard": False
                        }
                    ],
                    "100.00": [
                        {
                            "putCall": "CALL",
                            "symbol": "TEST_010320C100",
                            "description": "TEST Jan 03 2020 100 Call (Weekly)",
                            "bid": 0.03,
                            "ask": 0.04,
                            "bidAskSize": "10X10",
                            "volatility": 160.024,
                            "delta": -0.003,
                            "gamma": 0.001,
                            "theta": -0.004,
                            "vega": 0.002,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 100,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": True,
                            "nonStandard": False
                        }
                    ],
                    "105.00": [
                        {
                            "putCall": "CALL",
                            "symbol": "TEST_010320C105",
                            "description": "TEST Jan 03 2020 105 Call (Weekly)",
                            "bid": 4.98,
                            "ask": 4.85,
                            "bidAskSize": "5X8",
                            "volatility": 161.024,
                            "delta": -0.003,
                            "gamma": 0.001,
                            "theta": -0.004,
                            "vega": 0.002,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 105,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": False,
                            "nonStandard": False
                        }
                    ],
                    "110.00": [
                        {
                            "putCall": "CALL",
                            "symbol": "TEST_010320C110",
                            "description": "TEST Jan 03 2020 110 Call (Weekly)",
                            "bid": 9.98,
                            "ask": 9.85,
                            "bidAskSize": "11X12",
                            "volatility": 170.024,
                            "delta": -0.023,
                            "gamma": 0.02,
                            "theta": -0.03,
                            "vega": 0.012,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 110,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": False,
                            "nonStandard": False
                        }
                    ]
                }
            },
            "putExpDateMap": {
                "2020-01-03:1": {
                    "90.00": [
                        {
                            "putCall": "PUT",
                            "symbol": "TEST_010320P90",
                            "description": "TEST Jan 03 2020 90 Put (Weekly)",
                            "bid": 0.01,
                            "ask": 0.02,
                            "bidAskSize": "9X9",
                            "volatility": 152.024,
                            "delta": -0.003,
                            "gamma": 0.001,
                            "theta": -0.004,
                            "vega": 0.001,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 90,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": False,
                            "nonStandard": False
                        }
                    ],
                    "95.00": [
                        {
                            "putCall": "PUT",
                            "symbol": "TEST_010320P95",
                            "description": "TEST Jan 03 2020 95 Put (Weekly)",
                            "bid": 0.02,
                            "ask": 0.03,
                            "bidAskSize": "10X10",
                            "volatility": 160.024,
                            "delta": -0.003,
                            "gamma": 0.001,
                            "theta": -0.004,
                            "vega": 0.002,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 95,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": False,
                            "nonStandard": False
                        }
                    ],
                    "100.00": [
                        {
                            "putCall": "PUT",
                            "symbol": "TEST_010320P100",
                            "description": "TEST Jan 03 2020 100 Put (Weekly)",
                            "bid": 0.03,
                            "ask": 0.04,
                            "bidAskSize": "10X10",
                            "volatility": 160.024,
                            "delta": -0.003,
                            "gamma": 0.001,
                            "theta": -0.004,
                            "vega": 0.002,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 100,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": False,
                            "nonStandard": False
                        }
                    ],
                    "105.00": [
                        {
                            "putCall": "PUT",
                            "symbol": "TEST_010320P105",
                            "description": "TEST Jan 03 2020 105 Put (Weekly)",
                            "bid": 4.98,
                            "ask": 4.85,
                            "bidAskSize": "5X8",
                            "volatility": 161.024,
                            "delta": -0.003,
                            "gamma": 0.001,
                            "theta": -0.004,
                            "vega": 0.002,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 105,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": True,
                            "nonStandard": False
                        }
                    ],
                    "110.00": [
                        {
                            "putCall": "PUT",
                            "symbol": "TEST_010320P110",
                            "description": "TEST Jan 03 2020 110 Put (Weekly)",
                            "bid": 9.98,
                            "ask": 9.85,
                            "bidAskSize": "11X12",
                            "volatility": 170.024,
                            "delta": -0.023,
                            "gamma": 0.02,
                            "theta": -0.03,
                            "vega": 0.012,
                            "rho": 0,
                            "openInterest": 100,
                            "strikePrice": 110,
                            "expirationDate": 1578013200000,
                            "lastTradingDay": 1578099600000,
                            "inTheMoney": True,
                            "nonStandard": False
                        }
                    ]
                }
            }
        }

    @patch('pystonk.api.OptionsChainApi.requests')
    def testPriceHistory(self, requests_mock):
        requests_mock.get.return_value = self._mock_optionschain_response
        o = OptionsChainApi('some key')
        r = o.get_weekly_single_option_chain(
            symbol='test',
            week_date=date(2019, 12, 29)
        )

        self.assertEqual(requests_mock.get.call_count, 1, "Mocked requests not called")
        self.assertIsInstance(r, Dict, "OptionsChainApi did not return dict")
        self.assertEqual(5, len(r.keys()), "OptionsChainApi did not return expected number of options")
        self.assertListEqual(list(r.keys()), ['90.00', '95.00', '100.00', '105.00', '110.00'], "OptionsChainApi did not return expected strike price keys")

        for k, v in r.items():
            self.assertIsInstance(v, Tuple, f"OptionsChainApi did not return call and put contracts as a tuple for strike price {k}")
            self.assertIsInstance(v[0], OptionContract, f"OptionsChainApi did not return OptionContract for call strike price {k}")
            self.assertIsInstance(v[1], OptionContract, f"OptionsChainApi did not return OptionContract for put strike price {k}")
            self.assertEqual(v[0].contract_type, ContractType.CALL, f"OptionsChainApi did not return call OptionContract for strike price {k}")
            self.assertEqual(v[1].contract_type, ContractType.PUT, f"OptionsChainApi did not return call OptionContract for strike price {k}")
            self.assertListEqual([v[0].strike_price, v[1].strike_price], [float(k), float(k)], f"OptionsChainApi did not return correct OptionContract strike price pairs for strike price {k}")

    @patch('pystonk.api.OptionsChainApi.requests')
    def testPriceHistoryInvalid(self, requests_mock):
        requests_mock.get.return_value = self._mock_optionschain_response
        o = OptionsChainApi('some key')
        r = o.get_weekly_single_option_chain(
            symbol='test',
            week_date=date(2020, 1, 1)
        )

        self.assertEqual(requests_mock.get.call_count, 1, "Mocked requests not called")
        self.assertIsInstance(r, Dict, "OptionsChainApi did not return dict")
        self.assertEqual(0, len(r.keys()), "OptionsChainApi did not return expected number of options")