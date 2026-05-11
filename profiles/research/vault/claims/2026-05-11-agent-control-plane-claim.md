# CLAIM — Agent Control Plane Space

**Date:** 2026-05-11
**Source:** Reddit/HN/GitHub research sweep (2 runs)
**Status:** strengthening — CONFIRMED by new evidence

## Claim
"Control plane" is becoming the defining category for AI agent infrastructure in 2026. Independent builders are converging on the same architecture problem: agents need lifecycle management, supervision, log inspection, and recovery — separate from the agent runtime itself.

## New Evidence (Second Sweep)
- **Armorer** launched on HN 2 hours ago — local control plane for AI agents, open source, same problem space as OpenClaw
- **Harbour** (github.com/geekforbrains/harbour) — control plane for agents doing ongoing work
- **Agent Control** (Galileo + Cisco partnership) — open source control plane
- **AgentArmor** — security scanner for AI agents (adjacent category)
- **GitHub Enterprise AI Controls** — agent control plane generally available (Feb 2026)
- Multiple "I built an agent platform" posts in r/SideProject

## Strength Assessment
**Confirmed** — multiple independent builders, open source projects, and enterprise solutions all converging on the same category within weeks of each other. Armorer (just launched) specifically calls out the same pain point Graeme describes: "reading error logs, restarting failed jobs."

## Convergence with Our System
This validates our planned **Autonomous Recovery Layer** build. The market is building control planes without recovery. Our differentiation: recovery + compounding (builds that improve the builder).

## Route To
- `subc` — pattern-noticing: is this a category we should stake territory in?
- `main` — judgment call: should we build the Recovery Layer now given market timing?