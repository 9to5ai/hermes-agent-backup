# Moondev-Style Algorithmic Trading System
## Plan: Research → Backtest → Paper Trade Pipeline

---

## 🎯 Goal

Build an autonomous system that:
1. **Researches** new trading strategy ideas (AI-generated + research sources)
2. **Backtests** them rigorously with `backtesting.py`
3. **Deploys** profitable strategies to Hyperliquid **paper trading**
4. **Iterates** indefinitely — the "infinite algos" loop from Moondev's AI Masterclass 5

---

## 📚 Moondev's 6-Step System (Reference Framework)

| Step | Action | Our Implementation |
|------|--------|-------------------|
| 1 | Generate strategies via AI prompts + research | Strategy generator agent |
| 2 | Backtest with `backtesting.py` + ChatGPT debug | Backtester module |
| 3 | Build algo → deploy small real money ($10-50) | Hyperliquid paper trading |
| 4 | Forward test must match backtest | Performance validator |
| 5 | Scale across timeframes / tickers / capital | Position scaler |
| 6 | Repeat indefinitely | Cron-driven loop |

---

## 🏗️ Architecture

```
~/.hermes/
├── moondev/                        # Root trading system directory
│   ├── config.py                    # API keys, paper trading settings
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── exchange.py              # Hyperliquid adapter (from nice_funcs.py)
│   │   ├── risk.py                  # Kill switch, PnL monitor, position sizing
│   │   ├── indicators.py             # TA library (Bollinger, RSI, SMA, ATR, SDZ)
│   │   └── data_fetcher.py          # Fetch historical + live OHLCV
│   ├── strategies/
│   │   ├── base.py                  # BaseStrategy abstract class
│   │   ├── bollinger_squeeze.py      # Implemented: BBands squeeze HL
│   │   ├── mac_cross.py             # Implemented: MA crossover
│   │   ├── funding_arb.py           # Implemented: Funding rate arb
│   │   └── sd_zone.py               # Implemented: Supply/demand zones
│   ├── research/
│   │   ├── strategy_generator.py    # AI prompt → strategy ideas
│   │   ├── idea_bank.py             # Persisted list of generated ideas
│   │   └── prompts.py               # Strategy generation prompts
│   ├── backtester/
│   │   ├── engine.py                # backtesting.py runner + reporting
│   │   ├── optimizer.py              # Parameter optimization grid
│   │   └── walkforward.py           # Walk-forward analysis
│   ├── trader/
│   │   ├── paper_trader.py          # Live paper trading on Hyperliquid
│   │   ├── scheduler.py             # Schedule loop (like Moondev's schedule.every)
│   │   └── performance_tracker.py   # Track live vs backtest performance
│   └── results/
│       ├── backtest_results/       # Saved equity curves, stats JSONs
│       ├── live_results/            # Paper trading PnL logs
│       └── idea_bank.json           # All generated strategy ideas + status
```

---

## 📋 Phase-by-Phase Implementation Plan

### PHASE 1 — Foundation (Exchange Adapter + Risk Layer)
**Goal:** Get a working Hyperliquid connection + basic risk management

1. **Install dependencies**
   ```bash
   pip install hyperliquid-python-sdk ccxt pandas pandas_ta backtesting
   pip install talib  # if on mac: conda install ta-lib first
   ```

2. **Build `utils/exchange.py`** — adapt from `nice_funcs.py` (Hyperliquid)
   - `ask_bid(symbol)` → L2 orderbook via Hyperliquid REST API
   - `get_position(symbol)` → returns (in_pos, size, entry_px, pnl_perc, long)
   - `limit_order(coin, is_buy, sz, px, reduce_only=False)`
   - `cancel_all_orders()`
   - `set_leverage(symbol, leverage)`
   - `get_account_value()` → total equity in USD

3. **Build `utils/risk.py`** — adapt from `nice_funcs.py` + `5_risk.py`
   - `kill_switch(symbol)` → loops until position closed
   - `pnl_close(symbol, target, max_loss)` → exits on roe% threshold
   - `position_size(usd_size, leverage, price)` → contracts calculator
   - `max_pos_guard(max_positions)` → prevent >N concurrent positions

4. **Build `utils/data_fetcher.py`**
   - `fetch_ohlcv(symbol, timeframe, limit)` → pd.DataFrame
   - `save_candle_csv(symbol, timeframe, start_date, end_date)` → for backtesting
   - Cache to `~/.hermes/moondev/data/`

5. **Test**: Run kill switch + pnl_close against Hyperliquid **paper trading** (not real funds)

---

### PHASE 2 — Backtesting Engine
**Goal:** Reproducible backtesting with `backtesting.py` + walk-forward validation

1. **Build `backtester/engine.py`**
   ```python
   def run_backtest(csv_path, StrategyClass, cash=10000, commission=0.001):
       data = pd.read_csv(csv_path, parse_dates=True, index_col='Date')
       bt = Backtest(data, StrategyClass, cash=cash, commission=commission)
       stats = bt.run()
       return stats
   ```
   - Fee: Hyperliquid paper trading = 0% fees (confirm in docs)
   - Output: Sharpe, Sortino, Calmar, max drawdown, win rate, trade count

2. **Build `backtester/optimizer.py`**
   - Grid search over StrategyClass parameters
   - `bt.optimize(param=range(...), maximize='Equity Final [$]')`
   - Save top-5 parameter sets to JSON

3. **Build `backtester/walkforward.py`**
   - Train on Jan–Jun 2024, validate on Jul–Sep 2024
   - Must pass: live performance within 20% of backtest

4. **Add strategies to `strategies/`**:
   - `bollinger_squeeze.py` — from `day10_hyperliquid/10_bollinger_bot.py`
   - `mac_cross.py` — from `mac_backtest/mac_backtest.py`
   - `funding_arb.py` — from `hyperliquid-trading-bot/arb.py`
   - `sd_zone.py` — from `hyperliquid_supply_demand_algo/bot.py`

---

### PHASE 3 — Research Agent (AI Strategy Generator)
**Goal:** Automate the "unlimited strategies" step from Moondev's AI Masterclass 5

1. **Build `research/prompts.py`**
   - Prompt 1: "Give me 10 mean reversion strategies for crypto"
   - Prompt 2: "Give me 10 breakout strategies for 15m timeframe"
   - Prompt 3: "Give me 5 volatility strategies"
   - Each strategy prompt includes: entry logic, exit logic, stop loss, timeframe, indicators needed

2. **Build `research/strategy_generator.py`**
   - Uses Claude API to generate strategy ideas
   - Parses response → saves to `idea_bank.json`
   - Each idea has: name, hypothesis, indicators, entry rules, exit rules, timeframe, status: "generated"

3. **Build `research/idea_bank.py`**
   - JSON file with all ideas
   - Status flow: `generated` → `backtesting` → `passed`/`failed` → `paper_trading` → `live`

4. **Add ideas to backtest queue automatically**
   - If idea passes filter (e.g., has complete entry/exit rules), auto-generate a StrategyClass and backtest it

---

### PHASE 4 — Paper Trading System
**Goal:** Deploy passed strategies to Hyperliquid paper trading

1. **Build `trader/paper_trader.py`**
   - Loads passed strategy
   - Runs `scheduler.every(N).seconds.do(strategy.bot)`
   - Logs every order, fill, PnL to `results/live_results/`
   - Auto-cancel all orders every 30 mins (Moondev pattern from mean reversion bot)

2. **Build `trader/performance_tracker.py`**
   - Compare live PnL vs backtested PnL
   - Alert if live < 50% of backtest (kill the bot)
   - Alert if drawdown > 2x backtest max drawdown

3. **Build `trader/scheduler.py`**
   - Like Moondev's `schedule.every(15).seconds.do(bot)`
   - Error wrapper: on exception, sleep 30s and retry (Moondev pattern)
   - Global kill switch on Ctrl+C

---

### PHASE 5 — Automation Loop
**Goal:** Run research → backtest → deploy on a schedule

1. **Daily cron job** (like Moondev's daily 4-hour routine):
   ```
   Every day at 9am:
   1. Run research agent → generate 5 new strategy ideas
   2. Backtest top 3 ideas
   3. Deploy profitable ones to paper trading
   4. Check paper trading performance
   5. Kill underperformers
   ```

2. **Weekly review**:
   - Check all paper trading bots
   - Scale successful ones (increase position size)
   - Archive failed ones

---

## 🔑 Key Files to Create (in order)

| File | Purpose | Source |
|------|---------|--------|
| `config.py` | API keys, paper trading mode | Template from Moondev |
| `utils/exchange.py` | Hyperliquid REST adapter | `nice_funcs.py` (Hyperliquid) |
| `utils/risk.py` | Kill switch, PnL close, sizing | `5_risk.py`, `nice_funcs.py` |
| `utils/data_fetcher.py` | OHLCV fetch + save | `get_ohlcv` from bot files |
| `strategies/base.py` | Abstract base for strategies | — |
| `strategies/bollinger_squeeze.py` | BBands squeeze strategy | `day10_hyperliquid/10_bollinger_bot.py` |
| `backtester/engine.py` | Run backtests | `mac_backtest.py` |
| `research/strategy_generator.py` | AI idea generation | AI Masterclass 5 |
| `trader/paper_trader.py` | Paper trading runner | `schedule.every()` pattern |
| `trader/performance_tracker.py` | Live vs backtest comparison | — |
| `results/idea_bank.json` | All strategies + status | — |

---

## ⚠️ Risks, Tradeoffs, Open Questions

### Risks
- **Hyperliquid API changes**: SDK may break with protocol updates → pin to known working version
- **Overfitting in backtesting**: The 20-more-bots backtests use random/short data windows → always do walk-forward
- **Paper trading ≠ live**: Slippage, fill reliability, edge都不一样 → start with $10 not $50
- **No stop loss in some Moondev bots**: Always add hard stop loss

### Tradeoffs
- **backtesting.py** vs **Backtrader**: Moondev chose backtesting.py for simplicity; Backtrader is more powerful but complex
- **Hyperliquid** vs **Binance/Bybit**: Hyperliquid has zero fees (currently), but may not have all perpetuals

### Open Questions
1. Does Hyperliquid still have zero trading fees on mainnet?
2. What's the current max drawdown tolerance before killing a bot?
3. Should we use `schedule` library or `APScheduler` for the trading loop?
4. Do we need WebSocket for real-time fills, or is REST polling sufficient?
5. Should strategies share a single account or have separate sub-accounts per strategy?

---

## ✅ Verification Steps

After each phase:
- Phase 1: Place a limit order on paper trading, verify fill, verify kill_switch closes it
- Phase 2: Run 3 strategies through backtester; confirm equity curves plot correctly
- Phase 3: Generate 5 ideas; manually verify at least 2 are coherent strategies
- Phase 4: Run a strategy in paper trading for 1 hour; compare fills vs expected
- Phase 5: Run daily cron for 1 week; check idea_bank.json grows and has valid statuses

---

## 🚦Immediate Next Step

**Start Phase 1 now** — build the Hyperliquid exchange adapter + risk layer.

```bash
mkdir -p ~/.hermes/moondev/{utils,strategies,research,backtester,trader,results/{backtest_results,live_results}}
touch ~/.hermes/moondev/utils/__init__.py
```

Then create files in order:
1. `config.py` (template)
2. `utils/exchange.py`
3. `utils/risk.py`
4. `utils/data_fetcher.py`
5. Test with a paper trade
