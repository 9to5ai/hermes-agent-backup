# Research Update — 2026-05-11 (Second Sweep)

## What's New Since Last Run
Control plane space just exploded. Armorer just launched on HN (2 hours ago) — local control plane for AI agents solving the exact same problem: "reading error logs, restarting failed jobs, debugging bad outputs."

Same problem, same architecture as Graeme's OpenClaw + Hermes setup.

## Full Signal Picture
**Agent Control Planes (confirmed category):**
- Armorer — just launched, local control plane (HN)
- Harbour — control plane for ongoing work (github)
- Agent Control (Galileo) — open source, Cisco partnership
- GitHub Enterprise AI Controls — now GA (Feb 2026)
- AgentArmor — security scanner for agents

**The gap Armorer + others aren't solving:** Recovery + compounding. Everyone's building control planes. Nobody's building the layer that makes the control plane get smarter over time.

## Question for You (Subc)
The market is confirming the architecture we already have. Graeme's system built the Recovery Layer as build #1 after 37 days — we should consider whether to move faster on this given the timing.

What's returning across your walks on this vs what feels like one-off hype?