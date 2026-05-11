# PolyAgent Live Paper Testing Notes

Session-derived implementation notes for testing an autoresearched Polymarket strategy against live markets without placing real orders.

## Safe Paper Loop Pattern

- Run the live adapter in paper mode by default and write append-only JSONL signals/positions.
- Map directions explicitly:
  - `long` => BUY YES token
  - `short` => BUY NO token
- Fetch active CLOB price history with the YES token ID; using `conditionId` returned empty histories for some active markets.
- Use a project venv with Python 3.11 for `py-clob-client`; macOS system Python 3.9.6 cannot install current versions.

## PnL Tracking Requirements

A paper bot that only logs signals is insufficient. Add/verify:

1. One paper position per market by default; repeated loop signals should be skipped unless explicitly testing repeat entries.
2. Each paper entry records: market id, question, direction, outcome YES/NO, token id, size USDC, entry/limit price, confidence, spread, timestamp.
3. Mark-to-market PnL values the bought YES/NO token at the current CLOB bid:
   - `shares = size_usdc / entry_price`
   - `current_value = shares * current_bid`
   - `paper_pnl = current_value - size_usdc`
4. Report wins/losses, win rate, staked amount, current value, PnL, and largest movers.
5. Label this as mark-to-market paper PnL, not final settlement PnL.

## Chat Update Pattern for Jun

Jun asked to receive updates in the same Telegram chat. Scheduled updates should be concise and include:

- Whether the paper loop appears running.
- Number of paper positions/signals.
- Mark-to-market PnL, wins/losses, win rate, staked amount.
- Newest or largest 3-5 positions with LONG=BUY YES / SHORT=BUY NO, market question, entry/current bid, size, confidence/spread, and PnL.
- Any obvious issues: wide spreads, duplicate skipped markets, no new activity, unpriced positions.
- Reminder that it is paper-only and no real orders are being placed.

## Useful Commands From Session

```bash
cd /Users/momo/polyagent
uv venv --python /Users/momo/.local/share/uv/python/cpython-3.11-macos-aarch64-none/bin/python3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt

.venv/bin/python live_autoresearch_bot.py --paper --loop --interval 300 \
  --markets 50 --max-intents 5 --history-interval 1d --fidelity 60 \
  --min-history 10 --max-position-usdc 25 --min-liquidity 1000 --max-spread-pct 10.0

.venv/bin/python paper_pnl_report.py --top 5
```
