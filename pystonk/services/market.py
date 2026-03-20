from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Tuple

from pystonk import configuration
from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.api.Types import FrequencyType, PeriodType
from pystonk.models.CandleStick import CandleStick
from pystonk.models.OptionContract import OptionContract
from pystonk.models.OptionsChain import OptionsChain
from pystonk.models.PriceHistory import PriceHistory
from pystonk.models.PriceHistoryEstimate import PriceHistoryEstimate
from pystonk.models.Quote import Quote
from pystonk.utils import get_closest_monday_wednesday_friday_of_date, get_third_friday_of_month


MIN_OPTION_OPEN_INTEREST = 100
MAX_SPREAD_PERCENT_OF_MID = 20.0


def _shift_month(year: int, month: int, delta: int) -> Tuple[int, int]:
    absolute_month = (year * 12) + (month - 1) + delta
    return absolute_month // 12, (absolute_month % 12) + 1


def _next_anchor_month(d: date, anchors: Tuple[int, ...]) -> date:
    next_month = next((month for month in anchors if month > d.month), anchors[0])
    year = d.year if next_month > d.month else d.year + 1
    return date(year, next_month, 1)


def _upcoming_friday(d: date) -> date:
    return d + timedelta(days=((4 - d.weekday()) % 7))


def resolve_option_expiration(symbol: str, expiration: str, today: Optional[date] = None) -> date:
    today = today or date.today()
    symbol = symbol.upper()

    if expiration == "current":
        if symbol == "SPY":
            return get_closest_monday_wednesday_friday_of_date(today)
        return _upcoming_friday(today)

    if expiration == "week":
        return _upcoming_friday(today) + timedelta(days=7)

    if expiration == "month":
        year, month = _shift_month(today.year, today.month, 1)
        return get_third_friday_of_month(date(year, month, 1))

    if expiration == "quarter":
        return get_third_friday_of_month(_next_anchor_month(today, (3, 6, 9, 12)))

    if expiration == "half":
        return get_third_friday_of_month(_next_anchor_month(today, (6, 12)))

    if expiration == "year":
        year, month = _shift_month(today.year, today.month, 12)
        return get_third_friday_of_month(date(year, month, 1))

    raise ValueError(f"Unsupported expiration value: {expiration}")


def _serialize_quote(quote: Quote) -> Dict[str, Any]:
    return {
        "symbol": quote.symbol,
        "price": quote.price,
        "last_price": quote.last_price,
        "high_price": quote.high_price,
        "low_price": quote.low_price,
        "high_price_52week": quote.high_price_52week,
        "low_price_52week": quote.low_price_52week,
        "bid_price": quote.bid_price,
        "ask_price": quote.ask_price,
        "bid_size": quote.bid_size,
        "ask_size": quote.ask_size,
        "volume": quote.volume,
    }


def _serialize_candlestick(candlestick: CandleStick, percent_change: float) -> Dict[str, Any]:
    return {
        "open_price": candlestick.open_price,
        "high_price": candlestick.high_price,
        "low_price": candlestick.low_price,
        "close_price": candlestick.close_price,
        "volume": candlestick.volume,
        "start_datetime": candlestick.start_datetime.isoformat(),
        "frequency_type": candlestick.frequency_type.value,
        "percent_change": percent_change,
    }


def _serialize_contract(contract: OptionContract) -> Dict[str, Any]:
    spread = round(max(contract.ask - contract.bid, 0), 2)
    mid_price = round((contract.bid + contract.ask) / 2, 2)
    spread_percent_of_mid = round((spread / mid_price) * 100, 2) if mid_price > 0 else None

    return {
        "contract_type": contract.contract_type.value,
        "symbol": contract.symbol,
        "description": contract.description,
        "strike_price": contract.strike_price,
        "bid": contract.bid,
        "ask": contract.ask,
        "bid_size": contract.bid_size,
        "ask_size": contract.ask_size,
        "volatility": contract.volatility,
        "delta": contract.delta,
        "gamma": contract.gamma,
        "theta": contract.theta,
        "vega": contract.vega,
        "rho": contract.rho,
        "open_interest": contract.open_interest,
        "mid_price": mid_price,
        "spread": spread,
        "spread_percent_of_mid": spread_percent_of_mid,
        "is_itm": contract.is_itm,
        "is_nonstandard": contract.is_nonstandard,
        "expiration_datetime": contract.expiration_datetime.isoformat(),
        "last_trading_datetime": contract.last_trading_datetime.isoformat(),
    }


def _market_quality(contract: Dict[str, Any]) -> Dict[str, Any]:
    flags: List[str] = []

    if contract["bid"] <= 0:
        flags.append("No live bid")
    if contract["ask"] <= 0:
        flags.append("No live ask")
    if contract["open_interest"] < MIN_OPTION_OPEN_INTEREST:
        flags.append(f"Open interest below {MIN_OPTION_OPEN_INTEREST}")
    if contract["spread_percent_of_mid"] is not None and contract["spread_percent_of_mid"] >= MAX_SPREAD_PERCENT_OF_MID:
        flags.append(f"Spread above {int(MAX_SPREAD_PERCENT_OF_MID)}% of mid")

    return {
        "mid_price": contract["mid_price"],
        "spread": contract["spread"],
        "spread_percent_of_mid": contract["spread_percent_of_mid"],
        "open_interest": contract["open_interest"],
        "flags": flags,
    }


def _serialize_selection(selection: Optional[Tuple], is_sell: bool) -> Optional[Dict[str, Any]]:
    if not selection:
        return None

    contract, strike_diff, percent_change = selection
    premium = contract.bid if is_sell else contract.ask
    serialized_contract = _serialize_contract(contract)

    return {
        "premium": premium,
        "premium_side": "bid" if is_sell else "ask",
        "strike_diff": strike_diff,
        "percent_change": percent_change,
        "contract": serialized_contract,
        "market_quality": _market_quality(serialized_contract),
    }


def _selection_warnings(selection: Optional[Dict[str, Any]]) -> List[str]:
    if not selection:
        return []

    contract = selection["contract"]
    market_quality = selection["market_quality"]
    warnings: List[str] = []

    if selection["premium_side"] == "bid" and contract["bid"] <= 0:
        warnings.append(f"{contract['symbol']} has no live bid, so premium-selling inputs are not actionable.")
    if contract["open_interest"] < MIN_OPTION_OPEN_INTEREST:
        warnings.append(
            f"{contract['symbol']} has open interest {contract['open_interest']}, below the "
            f"{MIN_OPTION_OPEN_INTEREST}-contract liquidity floor."
        )
    if market_quality["spread_percent_of_mid"] is not None and market_quality["spread_percent_of_mid"] >= MAX_SPREAD_PERCENT_OF_MID:
        warnings.append(
            f"{contract['symbol']} has a {market_quality['spread_percent_of_mid']:.2f}% bid/ask spread, "
            "which is wide for weekly entries."
        )

    return warnings


def _event_risk_placeholder(symbol: str) -> Dict[str, str]:
    return {
        "symbol": symbol,
        "status": "unavailable",
        "message": "Event risk integration is not configured yet. Review earnings, ex-dividend, and macro catalysts before using a weekly setup.",
    }


class MarketService:
    VALID_HISTORY_FREQUENCIES = (
        FrequencyType.DAILY.value,
        FrequencyType.WEEKLY.value,
        FrequencyType.MONTHLY.value,
    )
    VALID_HISTORY_PERIODS = (1, 2, 3, 5)
    VALID_OPTION_EXPIRATIONS = ("current", "week", "month", "quarter", "half", "year")

    def __init__(self, quote_api: QuoteApi, price_history_api: PriceHistoryApi, options_chain_api: OptionsChainApi):
        self._quote_api = quote_api
        self._price_history_api = price_history_api
        self._options_chain_api = options_chain_api

    @classmethod
    def from_configuration(cls) -> "MarketService":
        app_key = configuration["app_key"]
        app_secret = configuration["app_secret"]

        if not app_key or not app_secret:
            raise ValueError("Missing Schwab credentials. Set PYSTONK_SCHWAB_KEY and PYSTONK_SCHWAB_SECRET.")

        return cls(
            quote_api=QuoteApi(app_key, app_secret),
            price_history_api=PriceHistoryApi(app_key, app_secret),
            options_chain_api=OptionsChainApi(app_key, app_secret),
        )

    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        quote = self._quote_api.get_quote(symbol.upper())
        return _serialize_quote(quote) if quote else None

    def get_price_history(
        self,
        symbol: str,
        percent: float,
        frequency: str = FrequencyType.WEEKLY.value,
        period: int = 1,
        start_to_end: bool = False,
    ) -> Optional[Dict[str, Any]]:
        symbol = symbol.upper()
        frequency = frequency.lower()

        if frequency not in self.VALID_HISTORY_FREQUENCIES:
            raise ValueError(f"Unsupported frequency value: {frequency}")
        if period not in self.VALID_HISTORY_PERIODS:
            raise ValueError(f"Unsupported period value: {period}")

        quote = self._quote_api.get_quote(symbol)
        if not quote:
            return None

        frequency_type = FrequencyType(frequency)
        adjusted_period = period
        period_type = PeriodType.YEAR
        if frequency_type == FrequencyType.DAILY:
            period_type = PeriodType.MONTH
            adjusted_period = 6 if period == 5 else period

        price_history = PriceHistory(
            self._price_history_api.get_price_history(
                symbol=symbol,
                period_type=period_type,
                period=adjusted_period,
                frequency_type=frequency_type,
                frequency=1,
            ),
            start_to_end,
        )
        estimate = PriceHistoryEstimate(price_history.percent_change_intervals())

        intervals = [
            _serialize_candlestick(candlestick, percent_change)
            for percent_change, candlestick in zip(price_history.percent_change_intervals(), price_history.intervals())
        ]

        return {
            "symbol": symbol,
            "quote": _serialize_quote(quote),
            "threshold_percent": round(percent, 2),
            "frequency": frequency_type.value,
            "period": adjusted_period,
            "period_type": period_type.value,
            "start_to_end": start_to_end,
            "intervals": intervals,
            "summary": {
                "interval_count": price_history.count_intervals(),
                "intervals_exceeding_threshold": price_history.count_intervals_exceed_percent_threshold(percent),
                "exceedance_rate": price_history.percent_rate(percent),
                "min": estimate.min(),
                "max": estimate.max(),
                "mean": estimate.mean(),
                "std": estimate.std(),
                "skew": estimate.skew(),
                "kurtosis": estimate.kurtosis(),
                "probability_exceeding_threshold": estimate.percent_probability(percent),
            },
        }

    def get_options_setup(
        self,
        symbol: str,
        target: float,
        expiration: str = "week",
        use_percent: bool = False,
    ) -> Optional[Dict[str, Any]]:
        symbol = symbol.upper()
        expiration = expiration.lower()

        if expiration not in self.VALID_OPTION_EXPIRATIONS:
            raise ValueError(f"Unsupported expiration value: {expiration}")

        quote = self._quote_api.get_quote(symbol)
        if not quote:
            return None

        expiration_date = resolve_option_expiration(symbol, expiration)
        chain = OptionsChain(
            quote.price,
            self._options_chain_api.get_single_option_chain(
                symbol=symbol,
                expire_date=expiration_date,
                strike_count=500,
            ),
        )

        rows: List[Dict[str, Any]] = []
        for strike_price, percent_change, call_option, put_option in chain.matrix():
            rows.append(
                {
                    "strike_price": float(strike_price),
                    "percent_change": percent_change,
                    "call": _serialize_contract(call_option),
                    "put": _serialize_contract(put_option),
                }
            )

        normalized_target = abs(round(target, 2))
        if use_percent:
            call_selection = chain.closest_call_option_by_percent(normalized_target)
            put_selection = chain.closest_put_option_by_percent(normalized_target)
            sell_call = _serialize_selection(call_selection, is_sell=True)
            buy_call = _serialize_selection(call_selection, is_sell=False)
            sell_put = _serialize_selection(put_selection, is_sell=True)
            buy_put = _serialize_selection(put_selection, is_sell=False)
        else:
            sell_call = _serialize_selection(chain.closest_call_option_by_premium(normalized_target), is_sell=True)
            buy_call = _serialize_selection(chain.closest_call_option_by_premium(normalized_target, is_sell=False), is_sell=False)
            sell_put = _serialize_selection(chain.closest_put_option_by_premium(normalized_target), is_sell=True)
            buy_put = _serialize_selection(chain.closest_put_option_by_premium(normalized_target, is_sell=False), is_sell=False)

        warnings = []
        if not any((sell_call, sell_put, buy_call, buy_put)):
            warnings.append("No matching option contracts were found for the requested target.")
        else:
            for selection in (sell_call, sell_put, buy_call, buy_put):
                warnings.extend(_selection_warnings(selection))

        return {
            "symbol": symbol,
            "quote": _serialize_quote(quote),
            "target": normalized_target,
            "target_mode": "percent" if use_percent else "premium",
            "expiration": expiration,
            "expiration_date": expiration_date.isoformat(),
            "rows": rows,
            "recommendations": {
                "sell": {"call": sell_call, "put": sell_put},
                "buy": {"call": buy_call, "put": buy_put},
            },
            "warnings": list(dict.fromkeys(warnings)),
            "event_risk": _event_risk_placeholder(symbol),
        }
