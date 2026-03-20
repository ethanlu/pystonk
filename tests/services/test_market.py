from datetime import date, datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from pystonk.api.Types import FrequencyType, PeriodType
from pystonk.models.CandleStick import CandleStick
from pystonk.models.OptionContract import OptionContract
from pystonk.models.Quote import Quote
from pystonk.services.market import MarketService, resolve_option_expiration


class ResolveOptionExpirationTest(TestCase):
    def testCurrentSpyUsesNextMondayWednesdayFriday(self):
        self.assertEqual(resolve_option_expiration("SPY", "current", date(2026, 3, 21)), date(2026, 3, 23))

    def testQuarterHalfAndYearResolveToFutureAnchors(self):
        self.assertEqual(resolve_option_expiration("QQQ", "quarter", date(2026, 9, 15)), date(2026, 12, 18))
        self.assertEqual(resolve_option_expiration("QQQ", "half", date(2026, 8, 15)), date(2026, 12, 18))
        self.assertEqual(resolve_option_expiration("QQQ", "year", date(2026, 3, 20)), date(2027, 3, 19))


class MarketServiceTest(TestCase):
    def setUp(self) -> None:
        self.quote_api = MagicMock()
        self.price_history_api = MagicMock()
        self.options_chain_api = MagicMock()
        self.service = MarketService(self.quote_api, self.price_history_api, self.options_chain_api)
        self.quote = Quote(
            symbol="SPY",
            price=100.25,
            last_price=100.10,
            high_price=101.20,
            low_price=99.30,
            high_price_52=120.00,
            low_price_52=80.00,
            bid=100.20,
            ask=100.30,
            bid_size=10,
            ask_size=12,
            volume=1_000_000,
        )

    def _candlesticks(self):
        return [
            CandleStick(100.00, 101.00, 98.00, 99.00, 1000, 1704067200000, FrequencyType.DAILY),
            CandleStick(99.00, 102.00, 97.00, 101.00, 1200, 1704153600000, FrequencyType.DAILY),
            CandleStick(101.00, 104.00, 100.00, 103.00, 1500, 1704240000000, FrequencyType.DAILY),
        ]

    def _contracts(self):
        now = datetime(2026, 3, 20, 12, 0, 0)
        epoch = int(now.timestamp()) * 1000
        expiration = now.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")
        return {
            "95.00": (
                OptionContract("CALL", "SPY_C95", "SPY 95 Call", 95.00, 5.10, 5.25, "3X4", 10.0, 0.5, 0.1, -0.1, 0.2, 0.0, 100, True, False, expiration, epoch),
                OptionContract("PUT", "SPY_P95", "SPY 95 Put", 95.00, 1.10, 1.25, "3X4", 10.0, -0.5, 0.1, -0.1, 0.2, 0.0, 100, False, False, expiration, epoch),
            ),
            "100.00": (
                OptionContract("CALL", "SPY_C100", "SPY 100 Call", 100.00, 2.10, 2.25, "3X4", 10.0, 0.4, 0.1, -0.1, 0.2, 0.0, 100, True, False, expiration, epoch),
                OptionContract("PUT", "SPY_P100", "SPY 100 Put", 100.00, 2.20, 2.35, "3X4", 10.0, -0.4, 0.1, -0.1, 0.2, 0.0, 100, False, False, expiration, epoch),
            ),
            "105.00": (
                OptionContract("CALL", "SPY_C105", "SPY 105 Call", 105.00, 0.90, 1.05, "3X4", 10.0, 0.3, 0.1, -0.1, 0.2, 0.0, 100, False, False, expiration, epoch),
                OptionContract("PUT", "SPY_P105", "SPY 105 Put", 105.00, 5.40, 5.55, "3X4", 10.0, -0.3, 0.1, -0.1, 0.2, 0.0, 100, True, False, expiration, epoch),
            ),
            "110.00": (
                OptionContract("CALL", "SPY_C110", "SPY 110 Call", 110.00, 0.35, 0.45, "3X4", 10.0, 0.2, 0.1, -0.1, 0.2, 0.0, 100, False, False, expiration, epoch),
                OptionContract("PUT", "SPY_P110", "SPY 110 Put", 110.00, 10.10, 10.30, "3X4", 10.0, -0.2, 0.1, -0.1, 0.2, 0.0, 100, True, False, expiration, epoch),
            ),
        }

    def _contracts_with_liquidity_issues(self):
        now = datetime(2026, 3, 20, 12, 0, 0)
        epoch = int(now.timestamp()) * 1000
        expiration = now.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")
        return {
            "95.00": (
                OptionContract("CALL", "SPY_C95", "SPY 95 Call", 95.00, 5.10, 5.25, "3X4", 10.0, 0.5, 0.1, -0.1, 0.2, 0.0, 100, True, False, expiration, epoch),
                OptionContract("PUT", "SPY_P95", "SPY 95 Put", 95.00, 1.00, 1.60, "3X4", 10.0, -0.5, 0.1, -0.1, 0.2, 0.0, 35, False, False, expiration, epoch),
            ),
            "100.00": (
                OptionContract("CALL", "SPY_C100", "SPY 100 Call", 100.00, 2.10, 2.25, "3X4", 10.0, 0.4, 0.1, -0.1, 0.2, 0.0, 100, True, False, expiration, epoch),
                OptionContract("PUT", "SPY_P100", "SPY 100 Put", 100.00, 2.20, 2.35, "3X4", 10.0, -0.4, 0.1, -0.1, 0.2, 0.0, 100, False, False, expiration, epoch),
            ),
            "105.00": (
                OptionContract("CALL", "SPY_C105", "SPY 105 Call", 105.00, 0.90, 1.05, "3X4", 10.0, 0.3, 0.1, -0.1, 0.2, 0.0, 100, False, False, expiration, epoch),
                OptionContract("PUT", "SPY_P105", "SPY 105 Put", 105.00, 5.40, 5.55, "3X4", 10.0, -0.3, 0.1, -0.1, 0.2, 0.0, 100, True, False, expiration, epoch),
            ),
            "110.00": (
                OptionContract("CALL", "SPY_C110", "SPY 110 Call", 110.00, 0.35, 0.45, "3X4", 10.0, 0.2, 0.1, -0.1, 0.2, 0.0, 100, False, False, expiration, epoch),
                OptionContract("PUT", "SPY_P110", "SPY 110 Put", 110.00, 10.10, 10.30, "3X4", 10.0, -0.2, 0.1, -0.1, 0.2, 0.0, 100, True, False, expiration, epoch),
            ),
        }

    def testGetQuoteSerializesQuote(self):
        self.quote_api.get_quote.return_value = self.quote

        result = self.service.get_quote("spy")

        self.assertEqual(result["symbol"], "SPY")
        self.assertEqual(result["price"], 100.25)
        self.assertEqual(result["bid_price"], 100.20)
        self.assertEqual(result["volume"], 1_000_000)

    @patch("pystonk.services.market.PriceHistoryEstimate")
    def testGetPriceHistoryAdjustsDailyFivePeriodToSixMonths(self, estimate_cls):
        self.quote_api.get_quote.return_value = self.quote
        self.price_history_api.get_price_history.return_value = self._candlesticks()

        estimate = MagicMock()
        estimate.min.return_value = -2.0
        estimate.max.return_value = 3.0
        estimate.mean.return_value = 0.5
        estimate.std.return_value = 1.2
        estimate.skew.return_value = 0.1
        estimate.kurtosis.return_value = -0.2
        estimate.percent_probability.return_value = 18.5
        estimate_cls.return_value = estimate

        result = self.service.get_price_history("spy", percent=3.0, frequency="daily", period=5, start_to_end=True)

        call_kwargs = self.price_history_api.get_price_history.call_args.kwargs
        self.assertEqual(call_kwargs["period_type"], PeriodType.MONTH)
        self.assertEqual(call_kwargs["period"], 6)
        self.assertEqual(result["frequency"], "daily")
        self.assertEqual(result["period"], 6)
        self.assertTrue(result["start_to_end"])
        self.assertEqual(result["summary"]["probability_exceeding_threshold"], 18.5)

    @patch("pystonk.services.market.resolve_option_expiration", return_value=date(2026, 3, 27))
    def testGetOptionsSetupPercentModeExposesSellBidAndBuyAsk(self, expiration_mock):
        self.quote_api.get_quote.return_value = self.quote
        self.options_chain_api.get_single_option_chain.return_value = self._contracts()

        result = self.service.get_options_setup("spy", target=5.0, expiration="week", use_percent=True)

        sell_put = result["recommendations"]["sell"]["put"]
        buy_put = result["recommendations"]["buy"]["put"]
        self.assertEqual(result["expiration_date"], "2026-03-27")
        self.assertEqual(sell_put["premium_side"], "bid")
        self.assertEqual(buy_put["premium_side"], "ask")
        self.assertEqual(sell_put["contract"]["symbol"], "SPY_P95")
        self.assertEqual(buy_put["contract"]["symbol"], "SPY_P95")
        self.assertNotEqual(sell_put["premium"], buy_put["premium"])
        self.assertEqual(sell_put["market_quality"]["spread"], 0.15)
        self.assertEqual(result["event_risk"]["status"], "unavailable")
        expiration_mock.assert_called_once()

    @patch("pystonk.services.market.resolve_option_expiration", return_value=date(2026, 3, 27))
    def testGetOptionsSetupWarnsWhenNoTargetMatches(self, expiration_mock):
        self.quote_api.get_quote.return_value = self.quote
        self.options_chain_api.get_single_option_chain.return_value = self._contracts()

        result = self.service.get_options_setup("spy", target=50.0, expiration="week", use_percent=False)

        self.assertEqual(result["warnings"], ["No matching option contracts were found for the requested target."])
        self.assertIsNone(result["recommendations"]["sell"]["put"])
        self.assertIsNone(result["recommendations"]["sell"]["call"])

    @patch("pystonk.services.market.resolve_option_expiration", return_value=date(2026, 3, 27))
    def testGetOptionsSetupAddsLiquidityWarningsToRecommendations(self, expiration_mock):
        self.quote_api.get_quote.return_value = self.quote
        self.options_chain_api.get_single_option_chain.return_value = self._contracts_with_liquidity_issues()

        result = self.service.get_options_setup("spy", target=1.0, expiration="week", use_percent=False)

        sell_put = result["recommendations"]["sell"]["put"]
        self.assertEqual(sell_put["contract"]["symbol"], "SPY_P95")
        self.assertIn("Open interest below 100", sell_put["market_quality"]["flags"])
        self.assertIn("Spread above 20% of mid", sell_put["market_quality"]["flags"])
        self.assertEqual(result["event_risk"]["status"], "unavailable")
        self.assertIn("SPY_P95 has open interest 35, below the 100-contract liquidity floor.", result["warnings"])
        self.assertIn("SPY_P95 has a 46.15% bid/ask spread, which is wide for weekly entries.", result["warnings"])
        expiration_mock.assert_called_once()
