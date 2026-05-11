# Agent Control Plane Market Research — 2026-05-11

## Research Sweep Results

Two consecutive research sweeps on 2026-05-11 found the agent control plane space exploding:

### Projects Found

**Armorer** (just launched on HN when found ~2hrs old)
- URL: news.ycombinator.com/item?id=48056990
- "A secure local control plane that manages the lifecycle of your agents"
- Pain point: "tired of reading error logs, restarting failed jobs, debugging bad outputs"
- Open source, local/self-hosted

**Harbour** — github.com/geekforbrains/harbour
- "A control plane for AI agents doing ongoing work"

**Agent Control** (Galileo)
- Open source control plane, partnered with Cisco for AI Defense guardrails
- Announcement: galileo.ai/blog/announcing-agent-control

**AgentArmor** — github.com/Zen-Open-Source/AgentArmor
- Security scanner for AI agents

**GitHub Enterprise AI Controls**
- Agent control plane now GA as of Feb 2026

**AgentField** — github.com/Agent-Field/agentfield
- "Build, run and scale AI agents like API and microservices — observable, auditable, identity-aware from day one"

**Spring AI Playground** (from April 2026 local AI sweep)
- "Secures local AI agent workflows" — github.com/spring-ai-community/spring-ai-playground

**Bitterbot** (from April 2026 local AI sweep)
- "Brings persistent memory to local agents" — Bitterbot-AI/bitterbot-desktop

## Key Insight

**Control planes are commoditizing. Smart recovery is not.**

Every builder in this space is solving the same problem: agents need lifecycle management, supervision, log inspection. But none of them are building the recovery + compounding layer — the thing that makes the control plane get smarter over time.

This is exactly what Graeme's system built as build #1 after 37 days. The market validated the architecture independently and simultaneously.

## Implication for Recover

The Recovery Layer built here is differentiated because:
1. It compounds — each failure makes future repairs faster
2. It uses canaries — verifies repair before continuing
3. It escalates properly — doesn't loop forever
4. It learns recipes — pattern-matching on failure types

Generic control planes will copy the orchestration. They won't copy the compounding recovery intelligence.

## Timing

Armorer launched ~2hrs before our research sweep found it. Market is moving fast. The window for building differentiated recovery intelligence is now — before the control plane space fully matures.