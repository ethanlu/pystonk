# Repo Overview

## What This Is

`pystonk` is a Python Slack bot for stock and options workflows. It pulls market data from the Schwab Market Data API, runs a small amount of analysis, and formats the result for Slack.

The repo supports two main runtime shapes:

- A long-running Slack app started from `pystonk/slack_app.py`
- A two-Lambda flow using `pystonk/lambda_receiver.py` and `pystonk/lambda_responder.py`

Infrastructure for the older Lambda deployment lives in `aws-cdk/`, local container setup lives in `docker/`, and the preferred VM deployment assets now live in `deploy/lightsail/`.

## Request Flow

1. Slack sends either an app mention or `/pystonk` slash command.
2. The app acknowledges quickly so Slack does not time out.
3. The command text is routed through `execute_command(...)` in `pystonk/slack_app.py`.
4. A command object parses arguments and calls one or more API clients in `pystonk/api/`.
5. Raw responses are normalized into models in `pystonk/models/`.
6. A view in `pystonk/views/` turns the result into Slack Block Kit output, text fallbacks, tables, and charts.

In Lambda mode, the receiver Lambda only handles the Slack handshake and then invokes the responder Lambda asynchronously to do the heavier work.

## Main Code Areas

- `pystonk/api/`: Schwab API wrappers for quotes, price history, and option chains.
- `pystonk/commands/`: argument parsing and command dispatch.
- `pystonk/models/`: normalized market data types plus small calculation helpers.
- `pystonk/services/`: reusable backend logic for quote, history, and options setup workflows.
- `pystonk/views/`: Slack responses, PrettyTable output, and chart generation.
- `pystonk/web_app.py`: FastAPI entrypoint for the new web interface.
- `pystonk/utils/`: date helpers, parser wrapper, shared utilities.
- `scripts/lightsail/`: reusable host bootstrap, install, deploy, and backup automation for Ubuntu Lightsail.
- `tests/`: mostly unit tests around parsing, helpers, models, and API wrappers.

## Supported Commands

- `pc`: current quote / price check
- `ph`: price history with threshold-based interval analysis
- `oc`: options chain lookup with target premium or percent-distance selection

These are wired in `pystonk/slack_app.py` and implemented in `pystonk/commands/PriceCheckCommand.py`, `pystonk/commands/PriceHistoryCommand.py`, and `pystonk/commands/OptionsChainCommand.py`.

## Configuration And Packaging Notes

- Package metadata and runtime dependencies are now declared in `pyproject.toml`, with `setup.py` retained as a thin setuptools shim.
- The preferred runtime is Python `3.12`, tracked in `.python-version`.
- App config is loaded eagerly from `pystonk/__init__.py`, using `conf/app.conf` if present and otherwise falling back to `conf/default.conf`.
- Because config is loaded at import time, even lower-level modules and tests depend on config parsing dependencies being installed.

## Review Notes

The codebase is small and readable, but a few areas deserve attention:

- Option expiration selection in `pystonk/commands/OptionsChainCommand.py` can resolve to the wrong quarter/half/year expiry.
- `pystonk/views/OptionsChainView.py` assumes an option match always exists and can fail when the requested target is outside the chain.
- API auth in `pystonk/api/__init__.py` caches a bearer token with no refresh path, and quote handling in `pystonk/api/QuoteApi.py` treats every `4xx` as “symbol not found.”
- Mention parsing in `pystonk/slack_app.py` uses a greedy regex and can erase valid commands when Slack-formatted links or extra mentions are present.

## Working On This Repo

If you need to re-orient quickly, start in this order:

1. `README.md`
2. `pystonk/slack_app.py`
3. `pystonk/commands/`
4. `pystonk/api/`
5. `pystonk/views/`
6. `tests/`

Related docs:

- `REPO_OVERVIEW.md`: high-level architecture and code layout
- `IMPROVEMENT_PLAN.md`: product direction and prioritized roadmap
- `WEB_APP_PLAN.md`: web-first migration plan and near-term implementation order
- `docs/LIGHTSAIL_DEPLOY.md`: recommended persistent VM deployment runbook
