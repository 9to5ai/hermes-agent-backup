# Live Deployment Safety for Autoresearched Polymarket Strategies

Use these notes when moving a paper/backtest-only prediction-market strategy toward live Polymarket execution.

## Do Not Deploy the Backtest Surface Directly

A `candidate_strategy.py` from an autoresearch harness is usually safe/pure and has a contract like:

```python
generate_signal(history, market, params) -> {direction, confidence, reasoning}
```

It should not import wallet/execution code. Wrap it with a separate live adapter that handles market discovery, history fetches, orderbook/risk checks, approvals, and execution.

## Critical Direction Mapping

Backtest semantics often differ from CLOB execution:

- `long` = buy YES
- `short` = buy NO, **not sell YES**
- `hold` = no trade

For Polymarket CLOB, orders should target the correct CLOB token ID:

- YES signal → YES token ID, BUY
- NO/short signal → NO token ID, BUY

Do not pass Gamma `market_id` or `conditionId` blindly to order placement. Resolve `clobTokenIds` from market metadata and verify the current orderbook for the selected token.

## Required Deployment Stages

1. **Signal-only / dry run**: fetch live markets + histories, call the strategy, print/log proposed trades.
2. **Paper trading**: simulate fills from live orderbooks; persist positions and exits.
3. **Approval-only mode**: submit proposed trades to a local dashboard/Telegram queue; no live order without explicit approval.
4. **Tiny-cap live mode**: only after paper + approval mode work; start with small caps such as `$10–$25` per position and daily loss limits.

## Recommended Guardrails

- Default mode must be paper/signal-only; require an explicit `--live` flag and credentials for live trading.
- Enforce max position size, max daily loss, max portfolio exposure, min liquidity, max spread, and one-position-per-market.
- In paper/live-market tests, avoid repeated entries on the same market by default. Otherwise a loop can re-log/re-buy the same signal every cycle and inflate fake exposure/PnL.
- Track paper results as positions, not just signals. Record entry token, side/outcome, size, and entry price, then mark to market using the current CLOB bid for the bought YES/NO token. Treat this as mark-to-market paper PnL, not final realized settlement PnL.
- Use limit orders with conservative slippage; avoid market orders unless the book is deep and the user explicitly wants them.
- Keep private keys out of logs, summaries, and persistent memory.
- Verify wallet, Polygon USDC balance, allowances/proxy wallet setup, and py-clob-client auth before enabling live.
- Keep a kill switch and produce auditable logs for every signal, approval, order, fill, exit, rejection, and periodic PnL summary.

## PolyAgent-Specific Notes From Session

In `/Users/momo/polyagent`, the existing `ExecutionEngine.execute_signal()` treated `SignalDirection.SHORT` as `Side.SELL`. That is unsafe for the autoresearch harness semantics because `short` meant buy NO. Future live adapters should either fix this mapping or bypass it with explicit YES/NO token selection.

For active CLOB market history, `/prices-history` should be called with the YES CLOB token ID. The autoresearch harness consumes YES-price history and simulates NO as `1 - YES`; using `conditionId` can return empty histories for active markets.

`py-clob-client` currently requires Python `>=3.9.10`; macOS system Python `3.9.6` will not install it. For Jun's PolyAgent project, use the project `.venv` with Python 3.11 and install via `uv pip install --python .venv/bin/python -r requirements.txt`.

A safe adapter shape is a separate `live_autoresearch_bot.py` with modes like:

```bash
python3 live_autoresearch_bot.py --paper --once
python3 live_autoresearch_bot.py --paper --loop --interval 300
python3 live_autoresearch_bot.py --approval-only --loop --interval 300
POLY_PRIVATE_KEY=... python3 live_autoresearch_bot.py --live --max-position-usdc 25
```

Do not simply set `POLY_PRIVATE_KEY` on an unreviewed execution stack and run it.
