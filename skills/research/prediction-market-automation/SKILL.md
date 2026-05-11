---
name: prediction-market-automation
description: Use when researching, building, operating, or troubleshooting prediction-market automation such as Polymarket data adapters, trading bots, paper/live execution, market APIs, orderbooks, whale tracking, and strategy evaluation.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [prediction-markets, polymarket, trading-bot, api, automation, research]
    related_skills: [polymarket]
---

# Prediction Market Automation

## Overview

Use this umbrella for automated prediction-market workflows: querying markets, building adapters, tracking positions, testing strategies, paper/live order execution, and debugging API quirks. It generalizes the PolyAgent project notes, preserved in `references/polyagent-prediction-market-bot.md`.

## When to Use

- User asks about Polymarket automation, market data collection, trading bots, or strategy backtests.
- A project needs Gamma/CLOB/Data API access, orderbook/midprice/spread data, or trade history.
- You are debugging an automated prediction-market codebase with paper/live modes.

Do not use for generic finance questions with no prediction-market data or automation component.

## Standard Architecture

- **Adapter layer** — API clients for markets, events, orderbooks, prices, trades.
- **Models** — Market, Position, Signal, Order, Trade, Wallet/Whale dataclasses.
- **Data store** — local SQLite or equivalent for market snapshots, trades, positions, signals.
- **Research/signal generation** — momentum, convergence, mispricing, event/news evidence, whale following.
- **Execution** — paper mode first, live mode behind credentials and explicit user approval.
- **Risk controls** — bankroll, max position, liquidity/spread limits, no-trade conditions.

## Autoresearch / Strategy Search

When improving a prediction-market strategy harness, treat weak initial gains as insufficient if the user asks to keep going. Run a phased search: baseline → candidate family exploration → broad randomized/grid search → exact-runner verification. Keep `runner.py` immutable, edit only the safe strategy surface, and verify the final selected strategy with the documented runner command. See `references/autoresearch-strategy-search.md` for detailed workflow, pitfalls, and reporting style.

## Polymarket API Notes

Common endpoint classes:

- Gamma API for events, markets, search, profiles.
- CLOB API for orderbooks, midprices, spreads, and price history.
- Data API for trades and open interest.

Validate response shapes from live calls before coding assumptions; endpoints often return flat lists where wrappers/nesting might be expected.

## Live Trading Safety

- Default to paper/simulated mode unless credentials and live-trading approval are explicit.
- Never place orders without confirming market, side, size, limit price, slippage, and maximum loss.
- Keep private keys out of logs and summaries.
- Verify chain/network, allowance, and signing setup before live execution.
- For autoresearched strategies, do **not** deploy the backtest surface directly. Add a live adapter with signal-only → paper → approval-only → tiny-cap-live stages.
- Map strategy direction carefully: in these harnesses `short` means **buy NO**, not sell YES. Resolve the market's `clobTokenIds` and send BUY orders to the correct YES/NO token ID.
- Live-market paper tests must track positions and mark-to-market PnL, not just signal counts. Skip repeat paper entries on the same market by default to avoid fake exposure. See `references/polyagent-live-paper-testing.md` for the paper-loop/PnL reporting pattern.
- See `references/live-deployment-safety.md` for the live deployment checklist and PolyAgent-specific pitfalls.

## Verification Checklist

- [ ] API response shape verified against current endpoint output.
- [ ] Paper mode works before live mode.
- [ ] Orders/positions serialize to the exact database schema.
- [ ] Risk limits are enforced before execution.
- [ ] Credentials are present only when live trading is explicitly intended.
