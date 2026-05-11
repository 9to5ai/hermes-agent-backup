---
name: hermes-multi-agent-workflow
description: "Graeme (@gkisokay) inspired multi-agent Hermes workflow: Research → Dreamer → Main → Coder → QA. 5 profiles, room/vault architecture, 3 cron jobs."
version: 1.0.0
author: graeme-gkisokay + hermes-agent
platforms: [macos, linux]
prerequisites:
  commands: [hermes]
metadata:
  hermes:
    tags: [hermes-agent, multi-agent, auto-think, auto-build, profiles]
    source: https://x.com/gkisokay/status/2053449921554960545
---

# Hermes Multi-Agent Workflow (Graeme-Inspired)

Based on Graeme's Auto-think + Auto-build system from [gkisokay's guide](https://x.com/gkisokay/status/2053449921554960545).

## Architecture

8 roles in the full system — only the core pipeline set up here:

```
Research → Dreamer/Subconscious → Main → Coder → QA
                                    ↑
                              Trust Reporting + Retention
```

### Profile Roles

| Profile | Role | Job |
|---------|------|-----|
| `research` | Evidence collector | Observe, gather, weigh, route — not summarize |
| `subc` | Dreamer / Subconscious | Pattern-noticer, leaves [BUILD: slug] signals |
| `main` | Conscious operator | Gate between thinking and building, approves work |
| `coder` | Builder | Implements only approved bounded plans |
| `qa` | Auditor | Verifies independently, reports pass/fail |

## Setup (Already Done)

5 profiles created with `hermes profile create <name>`:
- `~/.hermes/profiles/research/` — vault structure at `vault/{raw,claims,findings,sources,dossiers,decisions,runs,health}`
- `~/.hermes/profiles/subc/` — room structure at `room/{walks,projects,notes,feedback,inbox-from-researchd,signal-log,signal-state}`
- `~/.hermes/profiles/main/` — control-room, approval-ledger, projects
- `~/.hermes/profiles/coder/` — workspace for build artifacts
- `~/.hermes/profiles/qa/` — verification workspace

Each profile has its own SOUL.md defining identity and boundaries.

## Cron Jobs

3 active cron jobs:
- **Research Loop** (`3aec8f4d9290`) — every 6 hours (0 */6 * * *) — research agent refresh
- **Dreamer Morning Walk** (`e64ad6e9e46b`) — 8am daily — drift-from-research walk
- **Dreamer Evening Tending** (`1387efc92c72`) — 8pm daily — tend-the-room maintenance

## Key Concepts

### Dreamer Build Signals
```
[BUILD: project-slug]
one sentence about what you want to exist
```
A Dreamer signal is NOT a task — it's a flag that something has heat. Main decides.

### Idea Contract (from Dreamer to Main)
- What should exist + who benefits + why now
- What evidence supports it
- What is out of scope
- How it can be verified

### Product Plan (from Main to Coder)
Bounded work order — allowed paths, planned files, non-goals, verification commands, acceptance checks, risk, protected surfaces.

### Trust States
- Clean: builds passing
- Watch: issues detected, monitor
- Investigate: significant problems

### Recover Profile (added 2026-05-11)
- `~/.hermes/profiles/recover/` — survivability layer
- `monitor/` — detect.py, repair.py, canary.py, compound.py, recover_monitor.py
- `canaries/` — sample_canary.py
- `state/` — failures.log, recipes.log, canaries.log, compound.log, detector_state.json
- Cron: "Recover Monitor — 15min" (7cd072a2564d) every 15min

## Reference Materials

- `references/graeme-workflow-setup.md` — full setup state (profiles, crons, dashboard URLs, manual X browsing)
- `references/agentic-commerce-stack.md` — build candidate research from Graeme's Jan 12 Substack (x402, ERC-8004, composability)

## Starting Individual Agents

```bash
~/.hermes/hermes-agent/venv/bin/research chat
~/.hermes/hermes-agent/venv/bin/subc chat
~/.hermes/hermes-agent/venv/bin/main chat
~/.hermes/hermes-agent/venv/bin/coder chat
~/.hermes/hermes-agent/venv/bin/qa chat
```

## Running from Default

From the default profile, delegate to a specific agent:
- `delegate_task` with `profile_name` set to target profile
- Or use `hermes --profile <name> chat`

## Key Insights from Graeme's 37-Day Live Run

Graeme ran his full multi-agent system for 37 days and published the results:
**URL:** https://x.com/gkisokay/status/2053613051182772461

**Top 10 builds produced autonomously:**
1. Autonomous Recovery Layer — detect stalled phases, route repairs, dedupe stale outputs, enforce semantic acceptance, regression canaries
2. Contract Verification Hardening — stricter handoffs, clearer contracts, acceptable end states, verification paths
3. Research Agent Full Completion Plan — browser enrichment, GitHub/package signals, community inputs, source balance, evals, ops surfaces
4. Main Signal Review + Dreamer Advisory — feedback layer so Main can inspect Dreamer's output and nudge future walks
5. QA Audit Cockpit — operator-facing cockpit for system quality visibility
6. Operational Leak Content Sublane — classifier + canary to keep internal ops from leaking into content lanes
7. Foundation Hardening — runtime paths, shared state, migrations, test isolation, portability
8. Compounding Autonomy — receipts for learning over time: predictive signals, outcome health, proposal queues, level receipts, early eval harnesses
9. Local Model Load Reduction — move suitable wrapper work to local models, keep validation/reporting intact
10. QA Audit Report — proved single-shot path: Dreamer→Main→Coder→Mercy/QA

**Core lesson:** The best auto-build outputs are NOT just features — they are builds that improve the builder (recovery, verification, memory, signal quality, trust, routing, taste). That is where compounding starts.

**Implication for this system:** When the Dreamer signals a build, the most valuable ones to pursue are improvements to the system itself — not new features, but things that make Research, Dreamer, Main, Coder, and QA work better across iterations.

## Recover — The Survivability Layer (Added 2026-05-11)

A 6th profile `recover` was added as build #1 from Graeme's 37-day results. It monitors all other profiles for stalls, stale outputs, and deadlocks — then auto-repairs.

**Profile:** `~/.hermes/profiles/recover/`
- `SOUL.md` — identity as "the layer that makes everything else survive"
- `monitor/detect.py` — stall/silence/loop detection across all 5 profiles
- `monitor/repair.py` — recipe-matching auto-repair + escalation
- `monitor/canary.py` — regression canary runner (revert if fails)
- `monitor/compound.py` — pattern learning from failure/repair logs
- `monitor/recover_monitor.py` — main entry point (detect → repair → canary → compound)
- `canaries/sample_canary.py` — sample regression canary
- `state/failures.log`, `recipes.log`, `canaries.log`, `compound.log` — learning logs

**Active cron:** "Recover Monitor — 15min" (job_id `7cd072a2564d`) — every 15min, runs `recover_monitor.py` across all profiles.

**Recovery signals monitored:**
- `stall` — phase didn't complete in expected time
- `stale` — output unchanged in 3+ consecutive runs
- `deadlock` — same state repeated 5+ cycles

**Repair strategy:** Recipe first → generic repair → escalate to main if failed twice. Canary must pass after any critical repair or system reverts.

**Key insight from build:** Market timing confirmed — Armorer launched on HN 2hrs before research sweep, solving the same control-plane pain point. The gap everyone has is recovery + compounding. Control planes are commoditizing; smart recovery is not.

## Missing Pieces

- Graeme's public buildroom at `/buildroom` — not publicly available yet (github.com/gkisokay has 0 public repos)
- The Control Room React UI (agent-runtime not publicly available)
- X credential setup for auto-monitoring — browse X manually with browser_navigate; x402/ERC-8004 research done via web_extract on Substack

## Detailed Setup Reference

For the full current state of this implementation (what's created, running, and missing), see `references/graeme-workflow-setup.md` in the `hermes-agent` skill. That file includes dashboard URLs, cron job IDs, profile paths, and manual X browsing instructions.

**Overlapping skill:** `hermes-agent` has the same Graeme architecture section plus detailed multi-agent spawning patterns (tmux, delegate_task, profiles). Load both for full coverage — `hermes-agent` is the authoritative CLI reference, `hermes-multi-agent-workflow` is the quick-orientation summary.