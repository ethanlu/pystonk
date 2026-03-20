from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from fastapi import FastAPI, Form, Query, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from pystonk import configuration
from pystonk.services import MarketService
from pystonk.storage import WorkspaceStore

import uvicorn


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "web" / "templates"))


def _create_market_service() -> MarketService:
    return MarketService.from_configuration()


def _create_workspace_store() -> WorkspaceStore:
    return WorkspaceStore.from_configuration()


def _api_success(data: Dict[str, Any], status_code: int = 200) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"ok": True, "data": data})


def _api_error(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "ok": False,
            "error": {
                "code": code,
                "message": message,
            },
        },
    )


def _validation_message(exc: RequestValidationError) -> str:
    messages = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"][1:])
        if location:
            messages.append(f"{location}: {error['msg']}")
        else:
            messages.append(error["msg"])
    return "; ".join(messages) if messages else "Request validation failed."


def _extract_contract_symbol(selection: Optional[Dict[str, Any]]) -> Optional[str]:
    return selection["contract"]["symbol"] if selection else None


def _request_target(request: Request) -> str:
    return request.url.path if not request.url.query else f"{request.url.path}?{request.url.query}"


def _safe_redirect_target(target: Optional[str]) -> str:
    if target and target.startswith("/") and not target.startswith("//"):
        return target
    return "/"


def _redirect_with_message(target: Optional[str], key: str, message: str) -> RedirectResponse:
    safe_target = _safe_redirect_target(target)
    split_target = urlsplit(safe_target)
    query = dict(parse_qsl(split_target.query, keep_blank_values=True))
    query.pop("workspace_notice", None)
    query.pop("workspace_error", None)
    query[key] = message

    return RedirectResponse(
        url=urlunsplit(("", "", split_target.path, urlencode(query), split_target.fragment)),
        status_code=303,
    )


def _decorate_watchlist_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **entry,
        "url": f"/symbol/{entry['symbol']}",
    }


def _decorate_preset(preset: Dict[str, Any]) -> Dict[str, Any]:
    query = urlencode(
        {
            "history_percent": preset["history_percent"],
            "history_frequency": preset["history_frequency"],
            "history_period": preset["history_period"],
            "history_start_to_end": "true" if preset["history_start_to_end"] else "false",
            "options_target": preset["options_target"],
            "options_expiration": preset["options_expiration"],
            "options_use_percent": "true" if preset["options_use_percent"] else "false",
        }
    )
    target_label = (
        f"{preset['options_target']:.2f}% distance"
        if preset["options_use_percent"]
        else f"${preset['options_target']:.2f} premium"
    )

    return {
        **preset,
        "url": f"/symbol/{preset['symbol']}?{query}",
        "target_label": target_label,
    }


def _suggest_preset_name(symbol: str, options_expiration: str, options_target: float, options_use_percent: bool) -> str:
    target_label = f"{options_target:.2f}pct" if options_use_percent else f"{options_target:.2f}premium"
    return f"{symbol.upper()} {options_expiration} {target_label}"


def _build_option_rows(options_setup: Dict[str, Any]) -> list[Dict[str, Any]]:
    sell_call_symbol = _extract_contract_symbol(options_setup["recommendations"]["sell"]["call"])
    sell_put_symbol = _extract_contract_symbol(options_setup["recommendations"]["sell"]["put"])
    buy_call_symbol = _extract_contract_symbol(options_setup["recommendations"]["buy"]["call"])
    buy_put_symbol = _extract_contract_symbol(options_setup["recommendations"]["buy"]["put"])

    rows = sorted(options_setup["rows"], key=lambda row: abs(row["percent_change"]))[:16]
    rows.sort(key=lambda row: row["strike_price"])

    decorated_rows = []
    for row in rows:
        flags = []
        if row["call"]["symbol"] == sell_call_symbol:
            flags.append("Sell call")
        if row["call"]["symbol"] == buy_call_symbol:
            flags.append("Buy call")
        if row["put"]["symbol"] == sell_put_symbol:
            flags.append("Sell put")
        if row["put"]["symbol"] == buy_put_symbol:
            flags.append("Buy put")

        decorated_rows.append(
            {
                **row,
                "flags": flags,
                "flag_label": " / ".join(flags),
                "is_highlighted": bool(flags),
            }
        )

    return decorated_rows


def _build_dashboard_context(
    service: MarketService,
    symbol: str,
    history_percent: float,
    history_frequency: str,
    history_period: int,
    history_start_to_end: bool,
    options_target: float,
    options_expiration: str,
    options_use_percent: bool,
) -> Dict[str, Any]:
    symbol = symbol.upper()

    history = service.get_price_history(
        symbol=symbol,
        percent=history_percent,
        frequency=history_frequency,
        period=history_period,
        start_to_end=history_start_to_end,
    )
    if not history:
        raise LookupError(f"{symbol} was not found.")

    options = service.get_options_setup(
        symbol=symbol,
        target=options_target,
        expiration=options_expiration,
        use_percent=options_use_percent,
    )
    if not options:
        raise LookupError(f"Options setup for {symbol} was not found.")

    return {
        "symbol": symbol,
        "quote": options["quote"],
        "history": history,
        "history_rows": list(reversed(history["intervals"][-8:])),
        "options": options,
        "option_rows": _build_option_rows(options),
    }


def _render_symbol_dashboard(
    request: Request,
    symbol: str,
    history_percent: float = 3.0,
    history_frequency: str = "weekly",
    history_period: int = 1,
    history_start_to_end: bool = False,
    options_target: float = 1.0,
    options_expiration: str = "week",
    options_use_percent: bool = False,
    workspace_notice: Optional[str] = None,
    workspace_error: Optional[str] = None,
) -> HTMLResponse:
    context = {
        "request": request,
        "symbol": symbol.upper(),
        "history_percent": history_percent,
        "history_frequency": history_frequency,
        "history_period": history_period,
        "history_start_to_end": history_start_to_end,
        "options_target": options_target,
        "options_expiration": options_expiration,
        "options_use_percent": options_use_percent,
        "history_frequencies": MarketService.VALID_HISTORY_FREQUENCIES,
        "history_periods": MarketService.VALID_HISTORY_PERIODS,
        "option_expirations": MarketService.VALID_OPTION_EXPIRATIONS,
        "page_error": None,
        "workspace_notice": workspace_notice,
        "workspace_error": workspace_error,
        "current_target": _request_target(request),
        "watchlist_entry": None,
        "symbol_presets": [],
        "suggested_preset_name": _suggest_preset_name(symbol, options_expiration, options_target, options_use_percent),
        "dashboard": None,
    }
    status_code = 200

    try:
        workspace_store = _create_workspace_store()
        context["watchlist_entry"] = workspace_store.get_watchlist_entry(symbol)
        context["symbol_presets"] = [_decorate_preset(preset) for preset in workspace_store.list_presets(symbol)]
    except Exception:
        if not context["workspace_error"]:
            context["workspace_error"] = "Workspace storage is unavailable."

    try:
        service = _create_market_service()
        context["dashboard"] = _build_dashboard_context(
            service=service,
            symbol=symbol,
            history_percent=history_percent,
            history_frequency=history_frequency,
            history_period=history_period,
            history_start_to_end=history_start_to_end,
            options_target=options_target,
            options_expiration=options_expiration,
            options_use_percent=options_use_percent,
        )
    except ValueError as exc:
        context["page_error"] = str(exc)
        status_code = 500
    except LookupError as exc:
        context["page_error"] = str(exc)
        status_code = 404
    except Exception:
        context["page_error"] = "Unexpected error while loading the symbol dashboard."
        status_code = 500

    return templates.TemplateResponse("symbol.html", context, status_code=status_code)


def create_app() -> FastAPI:
    app = FastAPI(
        title="PyStonk Web",
        description="Web interface for quote, price history, and options setup workflows.",
        version="0.1.0",
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        if request.url.path.startswith("/api/"):
            return _api_error(422, "invalid_request", _validation_message(exc))
        return await request_validation_exception_handler(request, exc)

    @app.get("/", response_class=HTMLResponse)
    def home(
        request: Request,
        workspace_notice: Optional[str] = Query(None),
        workspace_error: Optional[str] = Query(None),
    ):
        context = {
            "request": request,
            "workspace_notice": workspace_notice,
            "workspace_error": workspace_error,
            "watchlist": [],
            "presets": [],
        }

        try:
            workspace_store = _create_workspace_store()
            context["watchlist"] = [_decorate_watchlist_entry(entry) for entry in workspace_store.list_watchlist()]
            context["presets"] = [_decorate_preset(preset) for preset in workspace_store.list_presets()]
        except Exception:
            if not context["workspace_error"]:
                context["workspace_error"] = "Workspace storage is unavailable."

        return templates.TemplateResponse(
            "index.html",
            context,
        )

    @app.get("/health")
    def health():
        return _api_success({"status": "ok"})

    @app.get("/symbol", response_class=HTMLResponse)
    def symbol_dashboard(
        request: Request,
        symbol: str = Query(..., min_length=1),
        history_percent: float = Query(3.0),
        history_frequency: str = Query("weekly"),
        history_period: int = Query(1),
        history_start_to_end: bool = Query(False),
        options_target: float = Query(1.0),
        options_expiration: str = Query("week"),
        options_use_percent: bool = Query(False),
        workspace_notice: Optional[str] = Query(None),
        workspace_error: Optional[str] = Query(None),
    ):
        return _render_symbol_dashboard(
            request=request,
            symbol=symbol,
            history_percent=history_percent,
            history_frequency=history_frequency,
            history_period=history_period,
            history_start_to_end=history_start_to_end,
            options_target=options_target,
            options_expiration=options_expiration,
            options_use_percent=options_use_percent,
            workspace_notice=workspace_notice,
            workspace_error=workspace_error,
        )

    @app.get("/symbol/{symbol}", response_class=HTMLResponse)
    def symbol_dashboard_path(
        request: Request,
        symbol: str,
        history_percent: float = Query(3.0),
        history_frequency: str = Query("weekly"),
        history_period: int = Query(1),
        history_start_to_end: bool = Query(False),
        options_target: float = Query(1.0),
        options_expiration: str = Query("week"),
        options_use_percent: bool = Query(False),
        workspace_notice: Optional[str] = Query(None),
        workspace_error: Optional[str] = Query(None),
    ):
        return _render_symbol_dashboard(
            request=request,
            symbol=symbol,
            history_percent=history_percent,
            history_frequency=history_frequency,
            history_period=history_period,
            history_start_to_end=history_start_to_end,
            options_target=options_target,
            options_expiration=options_expiration,
            options_use_percent=options_use_percent,
            workspace_notice=workspace_notice,
            workspace_error=workspace_error,
        )

    @app.post("/watchlist")
    def save_watchlist_symbol(
        symbol: str = Form(...),
        note: str = Form(""),
        redirect_to: str = Form("/"),
    ):
        try:
            workspace_store = _create_workspace_store()
            entry = workspace_store.add_watchlist(symbol=symbol, note=note)
        except ValueError as exc:
            return _redirect_with_message(redirect_to, "workspace_error", str(exc))
        except Exception:
            return _redirect_with_message(redirect_to, "workspace_error", "Workspace storage is unavailable.")

        return _redirect_with_message(redirect_to, "workspace_notice", f"Saved {entry['symbol']} to the watchlist.")

    @app.post("/watchlist/remove")
    def remove_watchlist_symbol(
        symbol: str = Form(...),
        redirect_to: str = Form("/"),
    ):
        try:
            workspace_store = _create_workspace_store()
            workspace_store.remove_watchlist(symbol=symbol)
        except ValueError as exc:
            return _redirect_with_message(redirect_to, "workspace_error", str(exc))
        except Exception:
            return _redirect_with_message(redirect_to, "workspace_error", "Workspace storage is unavailable.")

        return _redirect_with_message(redirect_to, "workspace_notice", f"Removed {symbol.strip().upper()} from the watchlist.")

    @app.post("/presets")
    def save_preset(
        preset_name: str = Form(...),
        symbol: str = Form(...),
        history_percent: float = Form(...),
        history_frequency: str = Form(...),
        history_period: int = Form(...),
        history_start_to_end: bool = Form(False),
        options_target: float = Form(...),
        options_expiration: str = Form(...),
        options_use_percent: bool = Form(False),
        redirect_to: str = Form("/"),
    ):
        try:
            workspace_store = _create_workspace_store()
            preset = workspace_store.save_preset(
                name=preset_name,
                symbol=symbol,
                history_percent=history_percent,
                history_frequency=history_frequency,
                history_period=history_period,
                history_start_to_end=history_start_to_end,
                options_target=options_target,
                options_expiration=options_expiration,
                options_use_percent=options_use_percent,
            )
        except ValueError as exc:
            return _redirect_with_message(redirect_to, "workspace_error", str(exc))
        except Exception:
            return _redirect_with_message(redirect_to, "workspace_error", "Workspace storage is unavailable.")

        return _redirect_with_message(redirect_to, "workspace_notice", f"Saved preset {preset['name']}.")

    @app.get("/api/quote")
    def quote(symbol: str = Query(..., min_length=1)):
        try:
            service = _create_market_service()
            data = service.get_quote(symbol)
        except ValueError as exc:
            return _api_error(500, "missing_credentials", str(exc))
        except Exception:
            return _api_error(500, "internal_error", "Unexpected server error.")

        if not data:
            return _api_error(404, "not_found", f"Quote for {symbol.upper()} was not found.")
        return _api_success(data)

    @app.get("/api/history")
    def history(
        symbol: str = Query(..., min_length=1),
        percent: float = Query(...),
        frequency: str = Query("weekly"),
        period: int = Query(1),
        start_to_end: bool = Query(False),
    ):
        try:
            service = _create_market_service()
            data = service.get_price_history(
                symbol=symbol,
                percent=percent,
                frequency=frequency,
                period=period,
                start_to_end=start_to_end,
            )
        except ValueError as exc:
            message = str(exc)
            code = "missing_credentials" if "credentials" in message.lower() else "invalid_request"
            status_code = 500 if code == "missing_credentials" else 422
            return _api_error(status_code, code, message)
        except Exception:
            return _api_error(500, "internal_error", "Unexpected server error.")

        if not data:
            return _api_error(404, "not_found", f"Price history for {symbol.upper()} was not found.")
        return _api_success(data)

    @app.get("/api/options")
    def options(
        symbol: str = Query(..., min_length=1),
        target: float = Query(...),
        expiration: str = Query("week"),
        use_percent: bool = Query(False),
    ):
        try:
            service = _create_market_service()
            data = service.get_options_setup(
                symbol=symbol,
                target=target,
                expiration=expiration,
                use_percent=use_percent,
            )
        except ValueError as exc:
            message = str(exc)
            code = "missing_credentials" if "credentials" in message.lower() else "invalid_request"
            status_code = 500 if code == "missing_credentials" else 422
            return _api_error(status_code, code, message)
        except Exception:
            return _api_error(500, "internal_error", "Unexpected server error.")

        if not data:
            return _api_error(404, "not_found", f"Options setup for {symbol.upper()} was not found.")
        return _api_success(data)

    return app


app = create_app()


def start():
    uvicorn.run(
        "pystonk.web_app:app",
        host=configuration["web"]["host"],
        port=int(configuration["web"]["port"]),
        reload=False,
    )
