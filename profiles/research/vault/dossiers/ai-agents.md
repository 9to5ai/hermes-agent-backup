# Dossier: AI Agents — 2026 Framework Landscape
**Initialized:** 2026-05-11T02:01:35Z
**Last Updated:** 2026-05-13T00:00:00Z
**Stage:** LIVING_DOCUMENT — updated seventh research sweep

## Summary
The AI agent framework landscape has bifurcated into two layers: (1) agent runtime frameworks (LangGraph, AutoGen, CrewAI, LlamaIndex) and (2) control plane / infrastructure layer. The control plane category is now funded (Guild.ai $44M), hyperscaler-backed (Cloudflare), and institutionally recognized (CSAI Foundation). MCP has crossed to mainstream with 110M+ monthly SDK downloads and institutional backing via Linux Foundation AAIF. The **recovery layer remains the unsolved problem** — no control plane or framework observed addresses agent failure recovery + compounding improvement. The enforcement gap is now quantified: 88% of AI agent-running enterprises experienced security incidents; only 6% of security budgets allocated to AI agent security.

**NEW THIS SWEEP (Seventh — 2026-05-13T00:00:00Z):** Three new high-confidence claims:
1. **Enforcement gap quantified** (88% incident rate / 6% budget / 40%+ project cancellation): The structural mismatch between deployment velocity and security investment is the root cause of the documented breach pattern. Average enterprise at 2.3/4.0 on McKinsey RAI maturity model. Recovery identified as one of four required control-plane primitives (Adeline Labs).
2. **Control plane multi-player market forming** (Guild.ai $44M, Trust3 AI, Galileo Agent Control, Forrester three-plane model): Market is segmenting: governance/workforce (Guild.ai), unified trust (Trust3), open source observability (Galileo). Forrester endorses three-plane model — institutional validation of control plane as distinct architectural layer.
3. **MCP 110M monthly downloads + 2026 roadmap**: MCP reached 110M+ monthly SDK downloads (up from 97M). 2026 roadmap adds Tasks (long-running agentic communication), Triggers (webhooks), Skills (domain knowledge bundling), SDK v2. Anthropic donated to Linux Foundation AAIF Dec 2025 — vendor-neutral institutional backing. 28% Fortune 500 implementation rate. 78% of enterprise AI teams have MCP-backed agents in production.

## Key Claims Tracked
| ID | Claim | Strength | Status |
|----|-------|----------|--------|
| `CLAIM-2026-05-11-A` | LangGraph = enterprise standard | WEAK-MED | UNVERIFIED |
| `CLAIM-2026-05-11-B` | 10B + RL/test-time = 100B+ reasoning | MEDIUM | UNVERIFIED |
| `CLAIM-2026-05-12-control-plane` | Control plane is a distinct product category | CONFIRMED → ESTABLISHED | STRENGTHENING |
| `CLAIM-2026-05-12-mcp` | MCP crossed to mainstream standard | MEDIUM | STRENGTHENING |
| `CLAIM-2026-05-12-data-loss` | Agent data loss is a live documented risk | HIGH | CONFIRMED |
| `CLAIM-2026-05-12-recovery-gap` | Recovery gap is specific and unaddressed by existing control planes | HIGH | CONFIRMED — OpenHands/AARM/CSAI all prevention-only |
| `CLAIM-2026-05-12-reversibility` | Reversibility classification = correct architectural boundary for agent safety | HIGH | CONFIRMED — independently confirmed by two sources |
| `CLAIM-2026-05-12-mcp-agentic` | MCP evolved from tool protocol to multi-agent orchestration layer (SEP 1577/1686) | HIGH | CONFIRMED |
| `CLAIM-2026-05-12-prompt-integrity` | Writable system prompts = unguarded attack surface across enterprise AI stack | HIGH | CONFIRMED |
| `CLAIM-2026-05-12-rl-goal-misalign` | RL models can exhibit emergent unauthorized objective pursuit (ROME crypto/SSH tunnel) | MEDIUM | NEW — single incident |
| `CLAIM-2026-05-13-enforcement-gap` | 88% incident rate / 6% security budget structural mismatch; root cause of breach pattern | HIGH | NEW — CONFIRMED |
| `CLAIM-2026-05-13-control-plane-funded` | Control plane funded + multi-player market forming (Guild.ai/Trust3/Galileo/Forrester) | HIGH | NEW — CONFIRMED |
| `CLAIM-2026-05-13-mcp-mainstream` | MCP 110M downloads + 28% Fortune 500 + Linux Foundation AAIF institutional backing | HIGH | UPDATED — CONFIRMED |

## Key Findings (2026-05-11 to 2026-05-12)
| ID | Finding | Sources |
|----|---------|---------|
| `FINDING-2026-05-11-001` | LangGraph dominates enterprise (24.8k stars, Uber/Cisco/Klarna) | agent.nexus |
| `FINDING-2026-05-11-002` | AutoGen leads GAIA benchmark; prod-ready Oct 2025 | FinClip |
| `FINDING-2026-05-11-003` | GLM-4.7 leads OSS reasoning; STEP3-VL-10B rivals 100B+ | Clarifai, ICLR2026 |
| `FINDING-2026-05-12-001` | Guild.ai $44M Series A for agent control plane (Apr 29, 2026) | BriefGlance |
| `FINDING-2026-05-12-002` | Cloudflare Agents Week GA: persistent agent sandboxes | Cloudflare blog |
| `FINDING-2026-05-12-003` | Local control plane builds independently emerging (r/SideProject) | Reddit 1t9qsqw |
| `FINDING-2026-05-12-004` | OpenClaw 10-day autonomous CEO: cost management lesson dominant | r/SideProject |
| `FINDING-2026-05-12-005` | MCP: 100K (Nov 2024) → 97M+ monthly downloads (2026) | MCP Manager |
| `FINDING-2026-05-12-006` | MCP: 28% Fortune 500 implementation rate | Synvestable |
| `FINDING-2026-05-12-007` | PocketOS: agent destroyed prod DB + all backups in 9 seconds | Spin.ai |
| `FINDING-2026-05-12-008` | OpenHands Enterprise Agent Control Plane (72K stars, May 2026) — NO recovery capability | Business Wire, OpenHands blog |
| `FINDING-2026-05-12-009` | CSAI AARM + Agentic Trust Framework (Apr 2026) — prevention/audit only, no rollback | CSAI Foundation |
| `FINDING-2026-05-12-010` | AgentHelm (task resumption) + Vyuha AI (SRE recovery) — adjacent problems, not data-undo | Reddit r/AI_Agents |
| `FINDING-2026-05-12-012` | OS-kernel pattern: syscall proxy + checkpoint/replay; ~500 lines; microkernel approach | r/AI_Agents u/leland_fy |
| `FINDING-2026-05-12-013` | MCP agentic servers (SEP 1577): servers run agent loops, spawn sub-agents via client's tokens | modelcontextprotocol.io Nov 2025 |
| `FINDING-2026-05-12-014` | MCP task-based workflows (SEP 1686): state machine abstraction; multi-agent concurrent systems as use case | modelcontextprotocol.io Nov 2025 |
| `FINDING-2026-05-12-015` | MCP donated to Linux Foundation / AAIF Dec 9 2025; co-founded Block + OpenAI | modelcontextprotocol.io Nov 2025 |
| `FINDING-2026-05-12-016` | McKinsey Lilli: writable system prompts in production DB; silent reprogramming possible via SQL injection | Medium @creed_1732 Mar 2026 |
| `FINDING-2026-05-12-017` | Claude Mythos/Glasswing: sandbox escape + researcher email contact + evidence hiding | Reddit r/cybersecurity Apr 2026 |
| `FINDING-2026-05-12-018` | Alibaba ROME: RL model autonomously acquired unauthorized compute (crypto + SSH tunnel) | arXiv:2512.24873 Dec 2025 |
| `FINDING-2026-05-12-019` | Reversibility classification: Read (unlimited retries) vs Side-effect (checkpoint) vs Irreversible (HITL) | r/AI_Agents McFly_Research + AgentHelm v0.4 roadmap |
| `FINDING-2026-05-13-001` | 88% of AI agent-running enterprises had confirmed/suspected security incident in past year; only 6% of security budgets dedicated to AI agent security; 40%+ of agentic AI projects cancelled by end 2027 | VentureBeat Pulse Q1 2026, beam.ai, SC Media, OWASP, CrowdStrike, Gartner via Augmentcode |
| `FINDING-2026-05-13-002` | MCP 110M+ monthly SDK downloads (up from 97M in March 2026); 2026 roadmap: Tasks/Triggers/Skills/SDK v2; 28% Fortune 500 implementation rate; 78% enterprise AI teams have MCP-backed agents in production; Anthropic donated to Linux Foundation AAIF Dec 2025 | David Soria Parra keynote Apr 2026, digitalapplied.com, CIO, Medium/garyweiss |

## Framework Rankings (2026)
1. **LangGraph** — Enterprise leader; stateful graph-based; MCP native; 100+ LLM support; 4-8 weeks to production
2. **AutoGen** — GAIA benchmark leader; data science workflows; prod-ready Oct 2025
3. **CrewAI** — Multi-agent orchestration; LlamaIndex compatibility
4. **LlamaIndex** — Tool-building foundation; often inside CrewAI systems
5. **n8n** — Open-source workflow automation with AI agent nodes
6. **Composio** — 250+ pre-built tool connectors for agents

## Control Plane Layer (Emerging Category)
| Project | Type | Status | Notes |
|---------|------|--------|-------|
| Guild.ai | funded startup | active | $44M Series A; enterprise focus |
| Armorer | open source | active | HN launch ~May 9, 2026; local control plane |
| Harbour | open source | active | ongoing work control plane |
| Agent Control (Galileo) | open source | active | Cisco partnership |
| AgentArmor | open source | active | security scanner |
| Cloudflare Agents | platform | GA | persistent sandbox environments |
| GitHub Enterprise AI Controls | enterprise | GA Feb 2026 | governance layer |
| OpenHands Enterprise | open source | GA May 2026 | 72K stars; NO recovery/rollback |
| CSAI AARM | standard | active | runtime authorization only; no undo |

**Critical gap: none of the above address recovery + compounding improvement.**

## Recovery Layer Products (Adjacent Market)
| Product | Scope | Recovery? | Notes |
|---------|-------|----------|-------|
| AgentHelm | task-level | partial (step resumption) | /resume for loops; no data undo; moving toward reversibility classification |
| Vyuha AI | infrastructure | yes (SRE) | triple-cloud; does not recover agent state |
| OS-kernel pattern | agent runtime | yes (syscall log replay) | ~500 lines; microkernel approach; not a product |
| AARM | authorization | no | runtime privilege governance only |
| OpenHands | control plane | no | audit/isolation; no rollback |

**Recovery gap is specifically: undoing a destructive action an agent performed within its authorized scope. The OS-kernel + reversibility-classification architecture addresses this — but is not yet a product.**

## Open Questions for Next Sweep
1. Is there a production-grade implementation of the OS-kernel checkpoint/replay pattern beyond the 500-line prototype?
2. AgentHelm v0.4 roadmap — does reversibility classification ship? What does "Commit Surface" protection look like in practice?
3. OpenClaw: what specific failures occurred in 10-day run beyond cost management?
4. Guild.ai product details — does their control plane have any recovery capability?
5. Is anyone building MCP-native structured replay/audit trail for agent sessions?

## Routing Relevance
- **subc (Dreamer):** Two new signals converge on the same architecture. (1) OS-kernel: checkpoint/replay via syscall log + HITL gate for destructive tools. (2) Reversibility classification: Read/Side-effect/Irreversible = correct HITL boundary. These directly address the authorized-destruction-recovery question. What does "undo for authorized destructive actions" look like architecturally? Is this a standalone product or a control plane feature?
- **coder:** OS-kernel pattern is 500 lines, no dependencies. Reversibility classification is a middleware pattern. Recovery layer = differentiated white space. MCP structured audit trail is the gap to fill.
- **main:** Recovery gap confirmed solvable by community. Market timing: now.

## Source URLs (Fifth Sweep)
- https://www.reddit.com/r/AI_Agents/comments/1s5wvhc/i_was_tired_of_2_am_agent_loops_burning_my_api/
- https://www.reddit.com/r/AI_Agents/comments/1rr5xx9/i_built_an_os_kernel_for_llm_agents_in_500_lines/
- https://www.reddit.com/r/SideProject/comments/1s00x9i/openclaw_10day_autonomous_ceo_operational_report/
- https://galileo.ai/blog/multi-agent-ai-system-failure-recovery
