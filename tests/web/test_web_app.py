from unittest import TestCase
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from pystonk.web_app import create_app


def _sample_history(symbol: str = "SPY"):
    return {
        "symbol": symbol,
        "quote": {
            "symbol": symbol,
            "price": 100.25,
            "last_price": 100.10,
            "high_price": 101.20,
            "low_price": 99.30,
            "high_price_52week": 120.00,
            "low_price_52week": 80.00,
            "bid_price": 100.20,
            "ask_price": 100.30,
            "bid_size": 10,
            "ask_size": 12,
            "volume": 1_000_000,
        },
        "threshold_percent": 3.0,
        "frequency": "weekly",
        "period": 1,
        "period_type": "year",
        "start_to_end": False,
        "intervals": [
            {
                "start_datetime": "2026-03-06T00:00:00",
                "open_price": 100.0,
                "high_price": 101.0,
                "low_price": 99.0,
                "close_price": 102.0,
                "volume": 1000,
                "frequency_type": "weekly",
                "percent_change": 2.0,
            },
            {
                "start_datetime": "2026-03-13T00:00:00",
                "open_price": 102.0,
                "high_price": 104.0,
                "low_price": 101.0,
                "close_price": 103.5,
                "volume": 1200,
                "frequency_type": "weekly",
                "percent_change": 1.47,
            },
        ],
        "summary": {
            "interval_count": 2,
            "intervals_exceeding_threshold": 0,
            "exceedance_rate": 0.0,
            "min": -2.0,
            "max": 3.0,
            "mean": 0.5,
            "std": 1.2,
            "skew": 0.1,
            "kurtosis": -0.2,
            "probability_exceeding_threshold": 18.5,
        },
    }


def _selection(symbol: str, strike_price: float, premium: float, premium_side: str, percent_change: float, spread: float = 0.15, open_interest: int = 150, flags=None):
    return {
        "premium": premium,
        "premium_side": premium_side,
        "strike_diff": strike_price - 100.25,
        "percent_change": percent_change,
        "contract": {
            "symbol": symbol,
            "strike_price": strike_price,
        },
        "market_quality": {
            "spread": spread,
            "spread_percent_of_mid": 12.77,
            "open_interest": open_interest,
            "flags": flags or [],
        },
    }


def _sample_options(symbol: str = "SPY"):
    return {
        "symbol": symbol,
        "quote": {
            "symbol": symbol,
            "price": 100.25,
            "last_price": 100.10,
            "high_price": 101.20,
            "low_price": 99.30,
            "high_price_52week": 120.00,
            "low_price_52week": 80.00,
            "bid_price": 100.20,
            "ask_price": 100.30,
            "bid_size": 10,
            "ask_size": 12,
            "volume": 1_000_000,
        },
        "target": 1.0,
        "target_mode": "premium",
        "expiration": "week",
        "expiration_date": "2026-03-27",
        "warnings": ["SPY_P95 has a 32.00% bid/ask spread, which is wide for weekly entries."],
        "event_risk": {
            "symbol": symbol,
            "status": "unavailable",
            "message": "Event risk integration is not configured yet.",
        },
        "recommendations": {
            "sell": {
                "call": _selection("SPY_C105", 105.0, 1.05, "bid", 4.74),
                "put": _selection("SPY_P95", 95.0, 1.10, "bid", -5.24, spread=0.32, open_interest=80, flags=["Open interest below 100", "Spread above 20% of mid"]),
            },
            "buy": {
                "call": _selection("SPY_C105", 105.0, 1.20, "ask", 4.74),
                "put": _selection("SPY_P95", 95.0, 1.25, "ask", -5.24, spread=0.32, open_interest=80, flags=["Open interest below 100", "Spread above 20% of mid"]),
            },
        },
        "rows": [
            {
                "strike_price": 95.0,
                "percent_change": -5.24,
                "call": {"symbol": "SPY_C95", "bid": 5.10, "ask": 5.25, "spread": 0.15, "open_interest": 150},
                "put": {"symbol": "SPY_P95", "bid": 1.10, "ask": 1.42, "spread": 0.32, "open_interest": 80},
            },
            {
                "strike_price": 105.0,
                "percent_change": 4.74,
                "call": {"symbol": "SPY_C105", "bid": 1.05, "ask": 1.20, "spread": 0.15, "open_interest": 200},
                "put": {"symbol": "SPY_P105", "bid": 5.40, "ask": 5.55, "spread": 0.15, "open_interest": 150},
            },
        ],
    }


class WebAppTest(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())

    @patch("pystonk.web_app._create_market_service")
    def testQuoteEndpointReturnsNormalizedSuccess(self, service_factory):
        service = MagicMock()
        service.get_quote.return_value = {"symbol": "SPY", "price": 100.25}
        service_factory.return_value = service

        response = self.client.get("/api/quote", params={"symbol": "SPY"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertEqual(response.json()["data"]["symbol"], "SPY")

    @patch("pystonk.web_app._create_market_service")
    def testQuoteEndpointReturnsNormalizedNotFoundError(self, service_factory):
        service = MagicMock()
        service.get_quote.return_value = None
        service_factory.return_value = service

        response = self.client.get("/api/quote", params={"symbol": "MISSING"})

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(response.json()["error"]["code"], "not_found")

    @patch("pystonk.web_app._create_market_service")
    def testHistoryEndpointReturnsNormalizedValidationError(self, service_factory):
        service = MagicMock()
        service.get_price_history.side_effect = ValueError("Unsupported frequency value: intraday")
        service_factory.return_value = service

        response = self.client.get("/api/history", params={"symbol": "SPY", "percent": 3, "frequency": "intraday"})

        self.assertEqual(response.status_code, 422)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(response.json()["error"]["code"], "invalid_request")

    def testHistoryEndpointRequestValidationIsNormalized(self):
        response = self.client.get("/api/history", params={"symbol": "SPY"})

        self.assertEqual(response.status_code, 422)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(response.json()["error"]["code"], "invalid_request")
        self.assertIn("percent", response.json()["error"]["message"])

    @patch("pystonk.web_app._create_market_service")
    def testMissingCredentialsAreNormalized(self, service_factory):
        service_factory.side_effect = ValueError("Missing Schwab credentials. Set PYSTONK_SCHWAB_KEY and PYSTONK_SCHWAB_SECRET.")

        response = self.client.get("/api/options", params={"symbol": "SPY", "target": 1})

        self.assertEqual(response.status_code, 500)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(response.json()["error"]["code"], "missing_credentials")

    @patch("pystonk.web_app._create_workspace_store")
    def testHomeRendersWorkspaceState(self, store_factory):
        store = MagicMock()
        store.list_watchlist.return_value = [{"symbol": "SPY", "note": "Weekly put desk", "created_at": "2026-03-20 10:00:00"}]
        store.list_presets.return_value = [
            {
                "id": 1,
                "name": "SPY week 1.00premium",
                "symbol": "SPY",
                "history_percent": 3.0,
                "history_frequency": "weekly",
                "history_period": 1,
                "history_start_to_end": False,
                "options_target": 1.0,
                "options_expiration": "week",
                "options_use_percent": False,
                "created_at": "2026-03-20 10:00:00",
            }
        ]
        store_factory.return_value = store

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Saved symbols", response.text)
        self.assertIn("Weekly put desk", response.text)
        self.assertIn("Saved setup defaults", response.text)

    @patch("pystonk.web_app._create_workspace_store")
    @patch("pystonk.web_app._create_market_service")
    def testSymbolDashboardRendersServerSideView(self, service_factory, store_factory):
        service = MagicMock()
        service.get_price_history.return_value = _sample_history()
        service.get_options_setup.return_value = _sample_options()
        service_factory.return_value = service
        store = MagicMock()
        store.get_watchlist_entry.return_value = {"symbol": "SPY", "note": "Weekly put desk", "created_at": "2026-03-20 10:00:00"}
        store.list_presets.return_value = []
        store_factory.return_value = store

        response = self.client.get("/symbol/SPY")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Symbol Dashboard", response.text)
        self.assertIn("SPY_C105", response.text)
        self.assertIn("Threshold", response.text)
        self.assertIn("Event risk status", response.text)
        self.assertIn("Open interest below 100", response.text)

    @patch("pystonk.web_app._create_workspace_store")
    def testSaveWatchlistRedirectsBackWithNotice(self, store_factory):
        store = MagicMock()
        store.add_watchlist.return_value = {"symbol": "SPY", "note": "desk", "created_at": "2026-03-20 10:00:00"}
        store_factory.return_value = store

        response = self.client.post(
            "/watchlist",
            data={"symbol": "spy", "note": "desk", "redirect_to": "/symbol/SPY"},
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["location"], "/symbol/SPY?workspace_notice=Saved+SPY+to+the+watchlist.")
        store.add_watchlist.assert_called_once_with(symbol="spy", note="desk")

    @patch("pystonk.web_app._create_workspace_store")
    def testSavePresetRedirectsBackWithNotice(self, store_factory):
        store = MagicMock()
        store.save_preset.return_value = {"name": "SPY week 1.00premium"}
        store_factory.return_value = store

        response = self.client.post(
            "/presets",
            data={
                "preset_name": "SPY week 1.00premium",
                "symbol": "SPY",
                "history_percent": "3",
                "history_frequency": "weekly",
                "history_period": "1",
                "history_start_to_end": "false",
                "options_target": "1",
                "options_expiration": "week",
                "options_use_percent": "false",
                "redirect_to": "/symbol/SPY",
            },
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["location"], "/symbol/SPY?workspace_notice=Saved+preset+SPY+week+1.00premium.")
        store.save_preset.assert_called_once()
