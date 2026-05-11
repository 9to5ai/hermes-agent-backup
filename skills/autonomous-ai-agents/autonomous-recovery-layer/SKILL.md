---
name: autonomous-recovery-layer
description: Autonomous Recovery Layer for Hermes multi-agent pipeline — detects stalled phases, auto-repairs, dedupes stale outputs, runs regression canaries, compounds learning over time.
version: 1.0.0
author: MomoTrades / Graeme-inspired
tags: [recovery, autonomous, hermes, multi-agent, pipeline]
category: autonomous-ai-agents
---

# Autonomous Recovery Layer

The layer that watches all agent runs and makes the system survive its own failures.

## Core Problem

Every multi-agent pipeline has failure points:
- Phases that stall without crashing
- Outputs that go stale but don't fail
- Runs that silently produce nothing
- Deadlocks between agents
- Quality degradation over time

Without recovery: every failure needs manual intervention.
With recovery: the system detects, repairs, and learns.

## Architecture

```
[Research] → [Dreamer] → [Main] → [Coder] → [QA]
                ↑
         Recovery Layer (monitors all stages)
                ↓
         [Canary] → [Regression Check] → [Log] → [Compounds]
```

## What It Does

### 1. Phase Detection
- Monitors run receipts in vault/runs/ and room/signal-log/
- Detects stalls: no new receipt in expected window
- Detects silence: expected signal not arrived
- Detects loops: same state repeated N times

### 2. Auto-Repair
- Stalled phase: re-trigger with fresh context
- Stale output: mark as stale, request fresh run
- Deadlock: inject reset signal, clear path
- Missing output: re-run from last good checkpoint

### 3. Output Deduplication
- Compare new output vs previous run
- If semantic match (LLM check): mark stale, skip
- If different: accept, proceed

### 4. Regression Canaries
- After repair, run a canary check
- Canary: small deterministic test to verify repair worked
- If canary fails: revert, escalate to human

### 5. Compounding Learning
- Each failure and repair is logged
- Pattern detection: what breaks most often
- Build "repair recipes" over time
- Future failures resolve faster

## Signals (from Dreamer signal filter)
- `stalled` — phase didn't complete in expected time
- `stale` — output hasn't changed in N runs
- `deadlock` — no progress after N cycles
- `canary_pass` / `canary_fail` — regression check result
- `repair_success` / `repair_fail` — repair outcome
- `recovered` — system recovered from failure

## Implementation Notes (2026-05-11)

**Market validation:** `references/market-research.md` — Armorer launched on HN 2hrs before our sweep found it; confirms the control plane space is hot and the recovery gap is real.

### Python 3.9 Compatibility
Uses `Optional[]` from typing module instead of `type | None` union syntax (not supported in Python 3.9). Always import:
```python
from typing import Optional, List, Dict
```

### Stalls detected by:
- No run receipt in `vault/runs/` within `2x expected interval` per profile
- research=60min, subc=45min, main=30min, coder=90min, qa=45min

### State file for loop detection
Uses `state/detector_state.json` — persists `last_states` and `loop_count` across runs. Created automatically on first detect.

### Repair recipes
Stored in `state/recipes.log` as `RECIPE:{json}` lines. Loaded by `find_recipe()` in repair.py — matches on type+profile first, then type only.

### Canary revert
Revert looks for latest checkpoint in `state/checkpoints/checkpoint_{profile}_*.json`. Checkpoints written by repair.py on each stall repair.

### Running manually
```bash
python3 /Users/momo/.hermes/profiles/recover/monitor/recover_monitor.py
python3 /Users/momo/.hermes/profiles/recover/monitor/detect.py        # exit 1 if failures found
python3 /Users/momo/.hermes/profiles/recover/monitor/canary.py research  # exit 0 if all pass
```

### Current status (2026-05-11)
System is clean — 0 failures detected on first run. All profiles healthy. Cron job `7cd072a2564d` running every 15min.

## Detection Rules

| Signal | Threshold | Action |
|--------|-----------|--------|
| No new run receipt | 2x expected interval | Re-trigger phase |
| Output unchanged | 3 consecutive runs | Mark stale, skip |
| Same state repeated | 5 cycles | Inject reset signal |
| Canary fails | 1 | Revert + escalate |
| Repair fails twice | 2 | Escalate to main |

## Compounding

After each failure:
1. Log what broke, when, what fixed it
2. After 3+ similar failures, build a "repair recipe"
3. Recipe format: `{pattern: str, cause: str, fix: str, confidence: float}`
4. On future similar failure, try recipe first before generic repair

## Verification

After any repair:
1. Run canary (small test from canaries/ dir)
2. If pass → log repair_success, resume
3. If fail → revert to last good state, log repair_fail, escalate

## Output Boundaries

A canary result is not a QA result.
A repair log is not a findings file.
A recipe is not a claim.

Each stage has a distinct role — do not flatten.