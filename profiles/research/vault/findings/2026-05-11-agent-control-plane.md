# FINDING — Agent Control Plane Space Is Exploding

**Date:** 2026-05-11 (second sweep)
**Source:** Reddit/HN + GitHub
**Type:** finding
**Confidence:** high

## New Signals

### Armorer (NEW — just launched)
- HN link: news.ycombinator.com/item?id=48056990 (2 hours ago as of search)
- "A secure local control plane that manages the lifecycle of your agents"
- Problem being solved: tired of reading error logs, restarting failed jobs, debugging bad outputs
- Open source, local/self-hosted
- Reddit: r/coolgithubprojects

### GitHub Enterprise AI Controls
- Agent control plane now generally available (Feb 2026)
- Enterprise-grade governance for AI agents

### Related Projects
- **Harbour** (github.com/geekforbrains/harbour) — control plane for AI agents doing ongoing work
- **Agent Control** (Galileo) — open source control plane, partnering with Cisco
- **AgentArmor** (Zen-Open-Source) — security scanner for AI agents
- **AgentField** — build/run/scale AI agents like API/microservices

## Pattern: "Control Plane" Is the New Bottleneck
Multiple independent builders hitting the same wall: agents need supervision, lifecycle management, log inspection, and recovery. This mirrors Graeme's OpenClaw + Hermes setup exactly — the market is validating the architecture.

## Convergence with Our Build
This confirms the **Autonomous Recovery Layer** build is well-timed. The market is building control planes without recovery. That's the gap.

## Source URLs
- https://news.ycombinator.com/item?id=48056990
- https://github.com/geekforbrains/harbour
- https://github.com/Zen-Open-Source/AgentArmor