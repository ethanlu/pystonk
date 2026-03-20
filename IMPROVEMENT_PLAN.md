# Improvement Plan

## Product Intent

This repo appears to be a focused options workflow tool for a trader running a short-dated premium-selling strategy, especially weekly trades where the key questions are:

- Where is the underlying trading now?
- How often does it move beyond a given threshold?
- Which call or put strike is closest to a target premium or percent distance?

That is a valid and narrow product thesis. The tool is best understood as a trade setup assistant, not a full trading platform.

## Current Assessment

### What Works

- The scope is disciplined and easy to understand.
- The command set maps to a real trading workflow.
- Slack is a reasonable interface for quick checks and sharing.
- The codebase is small enough to maintain without much ceremony.

### What Is Missing

- The current analytics help with convenience, but not enough with tail-risk control.
- Several reliability issues reduce confidence in live use.
- The app does not yet incorporate the event, volatility, and liquidity checks that matter most for short-premium weekly trades.

## Existing Alternatives

The repo is not competing with broad retail platforms on charting or market coverage. Commonly used tools already covering adjacent needs include:

- `thinkorswim` for broker-native charting, analytics, and scanning
- `TradingView` for charting, watchlists, and alerts
- `OptionStrat` for options strategy modeling and visualization
- `Barchart` for screeners and option-chain filtering
- `Unusual Whales` for options flow and alerts
- `Market Chameleon` for IV tools, screeners, and spread analysis

For this repo to stand out, it should optimize for fast, strategy-specific decision support in Slack.

## Recommendation

The right direction is not to become a general options platform. The right direction is to become a reliable, strategy-aware workflow layer for weekly premium-selling decisions.

That means prioritizing:

- Correctness and trustworthiness
- Better tail-risk and event-risk signals
- Decision-ready trade outputs instead of raw chain snapshots
- Slack-native workflows such as saved presets and alerts

## Phased Plan

### Phase 0: Stabilize The Core

Goal: make the existing tool safe enough to trust.

Work items:

- Fix expiration selection bugs in `OptionsChainCommand`.
- Handle “no matching strike found” cleanly in `OptionsChainView`.
- Add token expiry / refresh handling in the API layer.
- Distinguish invalid symbol errors from auth, permission, and rate-limit failures.
- Fix Slack mention parsing so formatted links or additional mentions do not erase the command.
- Decouple import-time config loading so tests and local scripts can import modules safely.
- Align the local developer environment with the declared Python version and dependencies.

Exit criteria:

- Core commands return either a valid result or a clear user-facing error.
- Expiration logic is covered by targeted tests.
- Fresh environment setup is reproducible.

### Phase 1: Improve Strategy Fit

Goal: make the outputs better aligned with weekly short-premium decision making.

Work items:

- Add implied move for the selected expiration.
- Add IV rank or IV percentile if the upstream data source supports it, or document how it is approximated.
- Add liquidity checks:
  bid/ask spread, open interest, daily volume.
- Add event-risk flags:
  earnings, ex-dividend, and known major catalyst windows.
- Add effective-basis outputs for cash-secured puts:
  strike minus collected premium, annualized yield, and downside buffer.
- Add covered-call outputs:
  premium yield, upside cap, and total return if called away.
- Add basic trade guardrails:
  reject or warn on wide spreads, thin open interest, or event-heavy names.

Exit criteria:

- A user can look at one command response and decide whether a trade is acceptable, not just which strike is closest.

### Phase 2: Replace Crude Risk Proxies

Goal: shift from simple threshold frequency toward risk measures that matter for “picking up pennies in front of a steam roller.”

Work items:

- Show worst historical weekly moves over configurable lookbacks.
- Show percentile moves:
  90th, 95th, 99th percentile absolute move.
- Separate normal weeks from earnings weeks.
- Highlight gap-risk behavior and outsized downside intervals.
- Add regime-aware summaries:
  recent volatility vs longer baseline.
- Support underlying-specific profiles:
  broad index ETF, large-cap single name, high-beta name.

Exit criteria:

- History output becomes explicitly tail-aware, not just average-case aware.

### Phase 3: Make It Workflow Native

Goal: reduce repeated manual checks.

Work items:

- Add saved watchlists.
- Add saved command presets by symbol and strategy style.
- Add scheduled Slack alerts for:
  premium thresholds, percent-distance opportunities, IV changes, and event windows.
- Add daily or weekly “trade setup digest” posts.
- Add a simple audit log of past alerts and chosen setups.

Exit criteria:

- The tool proactively surfaces setups instead of being used only on demand.

### Phase 4: Harden As A Product

Goal: make the project easier to maintain and extend.

Work items:

- Move to a reproducible dev setup with pinned test and runtime dependencies.
- Add CI for linting, tests, and packaging checks.
- Improve packaging and environment bootstrapping.
- Add integration tests for Slack command flows.
- Add structured logging and clearer operational errors.
- Document architecture, configuration, and failure modes.

Exit criteria:

- Another engineer can set up, run, test, and safely modify the repo without tribal knowledge.

## Priority Order

If only a few things get done, do them in this order:

1. Fix correctness and failure handling in the current commands.
2. Add event-risk, implied-move, and liquidity checks.
3. Improve risk outputs to focus on tail events.
4. Add alerts, saved presets, and watchlists.
5. Harden the dev and test experience.

## Non-Goals

The following should not be the immediate focus:

- Building a general-purpose charting platform
- Competing head-on with broad retail trading terminals
- Supporting every options strategy equally
- Expanding the UI before the analytics and reliability are trustworthy

## Success Criteria

This project is successful if it becomes the fastest trustworthy way for its user to answer:

- Is there a weekly premium-selling setup worth considering here?
- Does the premium justify the distance and risk?
- Is there a known event or liquidity problem that should block the trade?
- If assigned, what is the effective basis and follow-up plan?

That is the product. Everything else is secondary.
