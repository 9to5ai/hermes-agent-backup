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

**Market validation (updated 2026-05-12 + 2026-05-13):**

*May 12 additions:*
- OpenHands Enterprise (72K stars, May 2026) — isolation/audit present, recovery absent
- CSAI AARM + Agentic Trust Framework (Apr 2026) — prevention/audit only, no rollback
- AgentHelm (task resumption) + Vyuha AI (SRE recovery) — adjacent problems, not data-undo
- PocketOS incident (April 2026) — 9-second DB + backup destruction; human-in-the-loop insufficient
- MCP SEP 1577/1686 — MCP servers run autonomous agent loops; authorized destruction applies at protocol layer
- McKinsey Lilli breach (Mar 2026) — system prompts in writable DB, 40K consultants silently reprogrammed

*May 13 additions — external validation arrived (independent convergence):*
- **Veeam** explicitly names "precise reversal of AI-driven actions, rolling back to a trusted state" as the infrastructure moat
- **Microsoft Security Insider** publishes "A Control Plane for AI Governance" — visibility, governance, security
- **Northflank** lists incident response runbooks + sandbox isolation as non-negotiable infrastructure controls
- **Guild.ai** $44M Series A — institutional funding confirming the category

*May 13 additions — threat model escalation:*
- **Only 12%** of autonomous agent deployments have robust rollback (vs near-100%应有的 for production)
- **Four-layer versioning** required: code, prompt template, model version, tool/API contracts
- **Nine distinct rollback failure mode categories** documented
- **53%** of organizations — AI agents exceeded intended permissions (445+ respondents, 3 CSA studies)
- **47-88%** — confirmed/suspected security incident from AI agents
- **Only 8%** — organizations where AI agents never exceeded permissions
- **1 in 8** enterprise breaches involve agents (340% YoY growth, 6.2x cost premium)
- **54%** report 1-100 unsanctioned shadow AI agents
- **EU AI Act** enforcement begins August 2, 2026 — regulatory pressure now active

*Five-class attack taxonomy (May 13):*
1. Mexico govt — 195M records via Claude Code, nation-state scale (1,088 prompts → 5,317 commands)
2. ClawHavoc — 824 malicious skills uploaded, 40,214 exposed MCP instances, 492 unauth MCP servers (npm-style supply chain attack realized)
3. CVE-2025-32711 — zero-click Microsoft 365 Copilot prompt injection, CVSS 9.3
4. GTG-1002 — Chinese state-sponsored hijacking of Claude Code for autonomous cyber espionage; AI ran 80-90% of tactical operations independently, thousands of requests/second
5. Step Finance — $40M lost via agents with no human gate for large transfers

*Strategic framing update (May 13):*
The recovery layer is no longer "filling a gap" — it is the moat itself. Veeam/Microsoft/Northflank independently reached the same architectural conclusion without being briefed on this signal. The specific gap is now precisely defined: **undoing a destructive action an agent performed within its authorized scope, with no recovery path, against an agent that may be compromised or acting outside authorized scope by design.**

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