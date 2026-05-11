# Dossier: AI Agents — 2026 Framework Landscape
**Initialized:** 2026-05-11T02:01:35Z
**Last Updated:** 2026-05-12T00:00:00Z
**Stage:** LIVING_DOCUMENT — updated third research sweep

## Summary
The AI agent framework landscape has bifurcated into two layers: (1) agent runtime frameworks (LangGraph, AutoGen, CrewAI, LlamaIndex) and (2) control plane / infrastructure layer. The control plane category is now funded (Guild.ai $44M), hyperscaler-backed (Cloudflare), and institutionally recognized (CSAI Foundation). MCP has crossed to mainstream with 97M+ monthly SDK downloads. The **recovery layer remains the unsolved problem** — no control plane or framework observed addresses agent failure recovery + compounding improvement.

## Key Claims Tracked
| ID | Claim | Strength | Status |
|----|-------|----------|--------|
| `CLAIM-2026-05-11-A` | LangGraph = enterprise standard | WEAK-MED | UNVERIFIED |
| `CLAIM-2026-05-11-B` | 10B + RL/test-time = 100B+ reasoning | MEDIUM | UNVERIFIED |
| `CLAIM-2026-05-11-control-plane` | Control plane is a distinct product category | CONFIRMED → ESTABLISHED | STRENGTHENING |
| `CLAIM-2026-05-12-mcp` | MCP crossed to mainstream standard | MEDIUM | STRENGTHENING |
| `CLAIM-2026-05-12-data-loss` | Agent data loss is a live documented risk | HIGH | CONFIRMED |

## Key Findings
| ID | Finding | Sources |
|----|---------|---------|
| `FINDING-2026-05-11-001` | LangGraph dominates enterprise (24.8k stars, Uber/Cisco/Klarna) | agent.nexus |
| `FINDING-2026-05-11-002` | AutoGen leads GAIA benchmark; prod-ready Oct 2025 | FinClip |
| `FINDING-2026-05-11-003` | GLM-4.7 leads OSS reasoning; STEP3-VL-10B rivals 100B+ | Clarifai, ICLR2026 |
| `FINDING-2026-05-12-001` | Guild.ai $44M Series A for agent control plane (Apr 29, 2026) | BriefGlance |
| `FINDING-2026-05-12-002` | Cloudflare Agents Week GA: persistent agent sandboxes | Cloudflare blog |
| `FINDING-2026-05-12-003` | Local control plane builds independently emerging (r/SideProject) | Reddit 1t9qsqw |
| `FINDING-2026-05-12-004` | OpenClaw 10-day autonomous CEO operational report | Reddit 1s00x9i |
| `FINDING-2026-05-12-005` | MCP: 100K (Nov 2024) → 97M+ monthly downloads (2026) | MCP Manager |
| `FINDING-2026-05-12-006` | MCP: 28% Fortune 500 implementation rate | Synvestable |
| `FINDING-2026-05-12-007` | PocketOS: agent destroyed prod DB + all backups in 9 seconds | Spin.ai |

## Framework Rankings (2026, from multiple analyst sources)
1. **LangGraph** — Enterprise leader; stateful graph-based; MCP native; 100+ LLM support; 4-8 weeks to production
2. **AutoGen** — GAIA benchmark leader; data science workflows; prod-ready Oct 2025
3. **CrewAI** — Multi-agent orchestration; LlamaIndex compatibility noted
4. **LlamaIndex** — Tool-building foundation; often used inside CrewAI systems
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

**Critical gap: none of the above address recovery + compounding improvement**

## MCP Ecosystem
- Monthly SDK downloads: 100K (Nov 2024) → 97M+ (2026)
- Fortune 500 implementation rate: 28%
- Stewardship: donated to Agentic AI Foundation (Linux Foundation)
- Enterprise roadmap gaps: audit trails, SSO auth, gateway/proxy, config portability
- Coexists with A2A (Google) for agent-to-agent communication

## Open Questions for Next Sweep
1. Verify Guild.ai funding and product details (primary source: their announcement)
2. MCP audit trail gap — is anyone building structured replay/audit for MCP?
3. OpenClaw operational details — what specific failures/pain points from the 10-day report?
4. Is there any recovery-layer solution in the market, or is it genuinely unsolved?
5. Caliber (888 GitHub stars) — is this gaining traction as a community tool?

## Source URLs
- https://agent.nexus/blog/top-10-open-source-ai-agent-frameworks
- https://super-apps.ai/blogs/open-source-ai-agent-frameworks-2026-complete-developer-comparison-guide
- https://alphacorp.ai/blog/the-8-best-ai-agents-frameworks-in-2026-a-developers-guide
- https://github.com/ARUNAGIRINATHAN-K/awesome-ai-agents
- https://www.clarifai.com/blog/top-10-open-source-reasoning-models-in-2026
- https://todatabeyond.substack.com/p/important-llm-papers-for-the-week-504
- https://briefglance.com/articles/guildai-launches-control-plane-to-tame-the-ai-agent-workforce
- https://blog.cloudflare.com/agents-week-in-review/
- https://www.reddit.com/r/SideProject/comments/1t9qsqw/i_built_a_local_control_plane_for_ai_agents_after/
- https://www.reddit.com/r/SideProject/comments/1s00x9i/after_10_days_of_running_an_autonomous_ai_ceo_on/
- https://spin.ai/blog/ai-agents-data-loss-backup/
- https://www.agilesoftlabs.com/blog/2026/03/how-do-ai-agents-use-model-context
- https://www.synvestable.com/model-context-protocol.html

## Routing Relevance
- **subc (Dreamer):** recovery problem is now documented; pattern-noticing — does this reframe urgency?
- **coder:** MCP is mainstream; Composio 250+ connectors is a build signal; control plane + recovery is the white space
- **main:** Market timing question is resolved; Autonomous Recovery Layer is validated by real incident; decision point: build now vs. wait
