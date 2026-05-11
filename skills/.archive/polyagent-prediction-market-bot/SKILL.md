---
name: polyagent-prediction-market-bot
description: PolyAgent automated Polymarket trading bot at /Users/momo/polyagent
category: productivity
---

# PolyAgent — Polymarket Trading Bot

## Quick Start
```bash
cd /Users/momo/polyagent
python3 -c "from polyagent.agent import PolyAgent; PolyAgent(bankroll=10_000).run_cycle()"
```

## Architecture
- agent.py — main agent, run_cycle, portfolio management
- core/polymarket_adapter.py — Polymarket API wrapper (Gamma/CLOB/Data APIs)
- core/models.py — Market, Position, Signal, Order, WhaleWallet dataclasses
- core/data_store.py — SQLite persistence at ~/.polyagent/polyagent.db
- research/researcher.py — signal generation from market data
- whales/tracker.py — whale wallet tracking
- execution/executor.py — order execution (paper or live)
- strategies/ — momentum, convergence, whale_follow strategies

## Key Polymarket API Endpoints
- Gamma: https://gamma-api.polymarket.com — events, markets, search, profiles
- CLOB: https://clob.polymarket.com — orderbook, midprice, spread, price history
- Data: https://data-api.polymarket.com — trades, open interest

## Known API Quirks
- /markets returns a FLAT list of market dicts (NOT nested in events)
- fetch_trades() uses market param = conditionId, NOT slug or market_id
- Data API /trades returns a list directly, not a dict wrapper
- top-holders endpoint on Gamma always 404s — use Data API trades instead
- Order.to_dict() must return exactly 9 keys for the trades DB table
- Position objects use .size, .avg_price, .side.value attributes — NOT .get

## Live Trading Setup
```bash
pip install requests web3 py-clob-client
export POLY_PRIVATE_KEY=0x...   # hex WITH 0x prefix
export POLY_API_KEY=your_key
```
Without keys: paper mode (simulated fills only).

## Autoresearch Strategy Harness
- Location: `/Users/momo/polyagent/autoresearch`
- Purpose: Karpathy-style autonomous strategy research for Polymarket, read-only/paper-only.
- Editable surface for agents: `candidate_strategy.py` only.
- Instructions: `program.md`.
- Runner command:
```bash
cd /Users/momo/polyagent/autoresearch
python3 runner.py --markets 12 --interval 1m --fidelity 60 --min-confidence 0.25 --json > run.log 2>&1
```
- Results append to `results.tsv`; `run.log` and `experiments/` are ignored artifacts.
- Important API quirk discovered: CLOB `/prices-history` needs the YES/NO CLOB token ID, not `conditionId`; the harness uses YES token history and simulates NO as `1 - YES price`.
- Safety: no live trading, no wallet/private-key imports, no order placement.
