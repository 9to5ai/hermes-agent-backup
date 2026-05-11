# Graeme Workflow Setup Reference — Updated 2026-05-11

## Full Profile List (6 profiles)

| Profile | Path | Purpose |
|---------|------|---------|
| `default` | `~/.hermes/` | Main operating profile |
| `research` | `~/.hermes/profiles/research/` | Evidence collector, vault structure |
| `subc` | `~/.hermes/profiles/subc/` | Dreamer/Subconscious, room structure |
| `main` | `~/.hermes/profiles/main/` | Conscious operator, approval gate |
| `coder` | `~/.hermes/profiles/coder/` | Builder, bounded implementation |
| `qa` | `~/.hermes/profiles/qa/` | Auditor, independent verification |
| `recover` | `~/.hermes/profiles/recover/` | Survivability layer (added 2026-05-11) |

## Cron Jobs (4 active)

| Name | Schedule | Job ID | Skill |
|------|----------|--------|-------|
| Research Loop - 6hr refresh | `0 */6 * * *` | 3aec8f4d9290 | research |
| Dreamer Morning Walk | `0 8 * * *` | e64ad6e9e46b | autonomous-ai-agents |
| Dreamer Evening Tending | `0 20 * * *` | 1387efc92c72 | autonomous-ai-agents |
| **Recover Monitor — 15min** | `*/15 * * * *` | 7cd072a2564d | autonomous-recovery-layer |

## Recover Profile — What Was Built

**Python 3.9 compatibility note:** All scripts use `Optional[]` from typing, not `type | None`.

**Monitor scripts** (`profiles/recover/monitor/`):
- `detect.py` — stall/silence/loop detection, writes to `state/failures.log`
- `repair.py` — recipe-matched repairs, writes to `state/repairs.log` + `state/recipes.log`
- `canary.py` — regression runner, writes to `state/canaries.log`
- `compound.py` — pattern learning, reads failures+repairs → updates recipe confidences
- `recover_monitor.py` — main entry point, runs detect → repair → canary → compound

**State files:**
- `state/detector_state.json` — persists loop counter + last states across runs
- `state/failures.log` — all detected failures
- `state/recipes.log` — repair recipes as `RECIPE:{json}` lines
- `state/repairs.log` — repair attempt outcomes
- `state/canaries.log` — canary results
- `state/compound.log` — pattern analysis reports

**Canaries:**
- `canaries/sample_canary.py` — checks vault accessibility + recent receipts

**How to test:**
```bash
python3 ~/.hermes/profiles/recover/monitor/recover_monitor.py
```

## Market Research — What We Found

**Agent Control Plane space confirmed as real category (2026-05-11):**
- Armorer — local control plane, just launched on HN (2hrs old when found)
- Harbour — github.com/geekforbrains/harbour — control plane for ongoing work
- Agent Control (Galileo + Cisco partnership) — open source
- AgentArmor — security scanner for agents
- GitHub Enterprise AI Controls — now GA (Feb 2026)

**Gap:** Recovery + compounding. Everyone's building control planes; nobody's building the layer that makes it get smarter over time.

**Armorer specifically solves:** "reading error logs, restarting failed jobs, debugging bad outputs" — exact same pain point Graeme describes for OpenClaw.

## X/Twitter Browsing (Manual)

No X auth configured — browse manually via browser_navigate:
- Main post: https://x.com/gkisokay/status/2053449921554960545
- Dreamer guide: https://x.com/gkisokay/article/2040044476060864598
- Research guide: https://x.com/gkisokay/article/2051275483996909982
- 37-day results: https://x.com/gkisokay/status/2053613051182772461

Substack (no paywall): https://gkisokay.substack.com/
Personal site: https://gkisokay.com/