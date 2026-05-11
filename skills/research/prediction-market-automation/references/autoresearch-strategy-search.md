# Autoresearch Strategy Search Notes

Use these notes when a user asks to keep improving a prediction-market strategy harness, especially a Karpathy-style loop where only `candidate_strategy.py` is safe to edit and `runner.py` is the evaluation authority.

## Effective Workflow

1. **Run the baseline first** with the exact command in the project docs and capture `score`, `total_pnl`, `n_trades`, `max_drawdown`, and `concentration`.
2. **Do not stop after one weak improvement.** If the user asks to continue or says the result is rubbish, run a broader search immediately.
3. **Keep the runner immutable.** Build temporary search scripts that import runner functions and evaluate many candidate `generate_signal` functions in-process, then write only the selected strategy to `candidate_strategy.py`.
4. **Search in phases:**
   - small hand-written variants to find promising families;
   - wider randomized/grid search around the best family;
   - final exact-runner optimization using the current live market set;
   - final verification through the actual documented `python3 runner.py ... --json` command.
5. **Optimize for robustness, not only PnL.** Prefer candidates with positive score, 30+ trades, low drawdown, and concentration below ~0.60 when possible. Penalize single-market hacks.
6. **Clean temporary scripts** after final verification unless the user asked to keep research tooling. Leave `run.log`, variant logs, and `results.tsv` as research artifacts if ignored by `.gitignore`.

## Useful Candidate Families

- Z-score mean reversion over recent prices, gated by price regime and volatility.
- Extreme-price mean reversion with drift filters.
- Sparse breakout/momentum only as a comparator; it often underperforms after fees/slippage in this harness.
- Hybrid strategies can be tested, but choose the simplest family that wins under the actual runner.

## Important Pitfalls

- In-process simulation can differ from a final runner call if the live Gamma market set changes between fetches; always verify with the actual runner and report the verified numbers.
- Very high score with high concentration may be overfit. Show concentration and per-market PnL in the final summary.
- The CLOB history endpoint should use the YES token id; NO is simulated as `1 - YES` in the harness.
- Never introduce wallet/private-key/order-placement imports in candidate strategy files.

## Reporting Style

For Jun, be concise but candid: state the final file, strategy hash, score/PnL/trades/win rate/drawdown/concentration, and explicitly flag if the result is still paper-only or likely overfit.