# Web App Plan

## Why Shift To Web

The repo is currently built around Slack commands and Lambda responders. That works for quick checks, but it limits the product to a chat interface and mixes trading logic with presentation concerns.

The web direction should keep the existing Python market logic and replace Slack as the primary UI. Slack can stay later as a notification channel.

## Target Architecture

### Current

- `pystonk/slack_app.py` handles the main local Slack app flow
- `pystonk/lambda_receiver.py` and `pystonk/lambda_responder.py` handle the AWS Lambda flow
- `pystonk/commands/` combines parsing and trading workflow orchestration
- `pystonk/views/` is Slack-specific rendering

### Target

- `pystonk/services/` holds reusable quote, history, and options setup logic
- `pystonk/web_app.py` exposes the web interface and JSON API
- Slack becomes a secondary client that can call the same services later
- The web app becomes the main product surface
- Lightsail is the preferred first production target for the web app

## What Has Been Started

This branch now includes the first real web slice:

- `pystonk/services/market.py`
- `pystonk/storage/workspace.py`
- `pystonk/web_app.py`
- `pystonk/web/templates/index.html`
- `pystonk/web/templates/symbol.html`
- `docs/LIGHTSAIL_DEPLOY.md`
- `deploy/lightsail/`

This gives the project:

- a reusable service layer
- `/health`
- `/api/quote`
- `/api/history`
- `/api/options`
- normalized JSON success/error envelopes for the API
- a launcher page at `/`
- a server-rendered symbol dashboard at `/symbol/{ticker}`
- SQLite-backed watchlists
- saved presets for recurring symbol setups
- market-quality warnings for selected option candidates
- an explicit event-risk placeholder in the dashboard
- a concrete Lightsail deployment path for a persistent prototype host

## Phase 1: Stabilize The Web Foundation

Goal: make the new web surface reliable enough to build on.

Work items:

- move more shared logic out of `commands/`
- add explicit upstream error handling for auth, rate limits, and missing symbols
- fix current expiration-selection edge cases and test them
- add local run instructions for the web app
- add automated tests around the new service layer

Exit criteria:

- the JSON API returns predictable success and error shapes
- the service layer can be tested without Slack

## Phase 2: Build A Real Dashboard

Goal: replace the debug-style JSON console with a useful trade setup UI.

Work items:

- add a symbol dashboard page
- add formatted quote cards and history summaries
- add a readable options table with highlighted candidates
- add guardrail banners for no-match, low-liquidity, or event-risk states
- add a layout that works well on desktop and mobile

Exit criteria:

- the web app can be used directly for daily setup work without reading raw JSON

Status:

- largely in progress
- the current branch already has the launcher, symbol dashboard, watchlists, presets, and first-pass guardrails

## Phase 3: Add Strategy-Aware Decision Support

Goal: make the app better aligned with weekly premium-selling decisions.

Work items:

- show effective basis for cash-secured puts
- show covered-call payoff summaries
- add implied move, liquidity checks, and event-risk flags
- show tail-risk-oriented history metrics instead of only threshold frequency

Exit criteria:

- the UI helps reject bad trades, not just find candidate strikes

## Phase 4: Add Persistence And Workflow

Goal: turn the app from a lookup tool into a workflow system.

Work items:

- add watchlists
- add saved setup presets
- add alert rules
- add a lightweight trade journal
- add a backing database, starting with SQLite if the app remains single-user

Exit criteria:

- the user can save, revisit, and automate recurring setups

## Phase 5: Reposition Slack

Goal: keep Slack where it adds leverage without forcing it to remain the main UI.

Work items:

- keep Slack for alerts and daily digests
- have Slack commands call the shared service layer
- stop duplicating business logic across Slack and web

Exit criteria:

- web is primary
- Slack is additive

## Near-Term Backlog

Recommended next implementation order:

1. add tests for `pystonk/services/market.py`
2. improve error handling in `pystonk/web_app.py`
3. build a proper symbol page instead of raw JSON output
4. add effective basis and assignment-aware summaries
5. replace the event-risk placeholder with actual earnings and dividend checks
