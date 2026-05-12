# FINDING — Recovery-Layer Products Emerging: AgentHelm, Vyuha AI, OS-Kernel Pattern

**Date:** 2026-05-12
**Source:** web search, Reddit (r/AI_Agents, r/artificial)
**Type:** finding
**Confidence:** medium (Reddit sources, secondary corroboration)

## Signal

### AgentHelm — Resumes Failed Agent Tasks from Last Successful Step
- Source: Reddit r/AI_Agents post by creator
- Mechanism: `/resume` command finds failed task, "hydrates" memory/variables back to last successful step, restarts
- Problem solved: agent loops burning API credits (2 AM incidents), process death losing all progress
- **Note:** This is task-level resumption (checkpoint/restart), not state-level recovery. It saves progress at the step level, not the execution-environment level.

### Vyuha AI — Triple-Cloud Autonomous Recovery Orchestrator
- Source: Reddit r/ArtificialInteligence post by creator
- Scope: AWS + Azure + GCP multi-cloud autonomous recovery
- Architecture: GLM-5.1 AI SRE agent that autonomously triages cloud outages
- Built because: "tired of 3 AM PagerDuty alerts" from cloud incidents
- **Note:** Vyuha is cloud-infra-level recovery (SRE agent), not agent-workload-level recovery. Recovers cloud infrastructure from outages; does not recover agent execution state.

### OS-Kernel for LLM Agents (500 Lines of Python)
- Source: Reddit r/AI_Agents
- Problem identified: no budget limits, no recovery (process dies = start over), no isolation
- Solution: 500-line Python framework providing process supervision, resource limits, and basic recovery primitives
- **Signals:** Community recognizes "no recovery" as a fundamental gap in agent runtimes

## What These Products Confirm and Don't Cover

| Product | Scope | Recovers Agent Execution State? | Recovers Infrastructure? | Undoes Destructive Actions? |
|---------|-------|--------------------------------|--------------------------|----------------------------|
| AgentHelm | Task-level checkpoint/restart | Partial (step-level) | No | No |
| Vyuha AI | Cloud infrastructure | No | Yes (SRE) | No |
| OS-Kernel (community) | Agent runtime supervision | No | No | No |
| PocketOS incident | Agent → DB + backups | N/A | N/A | **NO — 9 seconds, all gone** |

## Key Observation

**Two distinct recovery problems are being addressed separately:**
1. **Infrastructure recovery** (Vyuha AI, cloud SRE) — recovers from outages, not from agent actions
2. **Task-level resumption** (AgentHelm) — recovers from loops/crashes, not from destructive actions

**The recovery problem for agent-caused data loss (PocketOS scenario) remains unaddressed by any known product.** The gap is specifically: how to undo or revert a destructive action an agent performed within its authorized scope. This is a different problem than infrastructure recovery or task resumption.

## Source URLs
- https://www.reddit.com/r/AI_Agents/comments/1s5wvhc/i_was_tired_of_2_am_agent_loops_burning_my_api/ (AgentHelm)
- https://www.reddit.com/r/ArtificialInteligence/comments/1selkyi/i_got_tired_of_3_am_pagerduty_alerts_so_i_built/ (Vyuha AI)
- https://www.reddit.com/r/AI_Agents/comments/1rr5xx9/i_built_an_os_kernel_for_llm_agents_in_500_lines/ (OS kernel pattern)
- https://nerranetwork.com/blog/models_agents/ep027.html (Vyuha GLM-5.1 reference)
