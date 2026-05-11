# Dossier: AI Agents — 2026 Framework Landscape
**Initialized:** 2026-05-11T02:01:35Z
**Last Updated:** 2026-05-11T02:01:35Z
**Stage:** LIVING_DOCUMENT — initial version from first research sweep

## Summary
The 2026 AI agent framework landscape is maturing rapidly. Enterprise adoption is growing; LangGraph leads in enterprise production deployments while AutoGen leads on autonomous benchmark performance. The MCP (Model Context Protocol) is emerging as a standard for tool-use interoperability. Compact models with scaled RL are showing competitive reasoning capabilities against much larger models.

## Key Claims Tracked
| ID | Claim | Strength | Status |
|----|-------|----------|--------|
| `CLAIM-2026-05-11-A` | LangGraph = enterprise standard | WEAK-MED | UNVERIFIED |
| `CLAIM-2026-05-11-B` | 10B + RL/test-time = 100B+ reasoning | MEDIUM | UNVERIFIED |

## Key Findings
| ID | Finding | Sources |
|----|---------|---------|
| `FINDING-2026-05-11-001` | LangGraph dominates enterprise (24.8k stars, Uber/Cisco/Klarna) | Airbyte, AlphaCorp AI |
| `FINDING-2026-05-11-002` | AutoGen leads GAIA benchmark; prod-ready Oct 2025 | FinClip |
| `FINDING-2026-05-11-003` | GLM-4.7 leads OSS reasoning; STEP3-VL-10B rivals 100B+ | Clarifai, ICLR2026 |

## Framework Rankings (2026, from multiple analyst sources)
1. **LangGraph** — Enterprise leader; stateful graph-based; MCP native; 100+ LLM support; 4-8 weeks to production
2. **AutoGen** — GAIA benchmark leader; data science workflows; prod-ready Oct 2025
3. **CrewAI** — Multi-agent orchestration; LlamaIndex compatibility noted
4. **LlamaIndex** — Tool-building foundation; often used inside CrewAI systems
5. **n8n** — Open-source workflow automation with AI agent nodes
6. **Composio** — 250+ pre-built tool connectors for agents

## Open Questions for Next Sweep
1. Verify LangGraph deployment claims at Uber/Cisco/Klarna (primary sources)
2. Access STEP3-VL-10B technical report directly — is the 10B-to-100B claim independently replicated?
3. Check GAIA benchmark leaderboard to verify AutoGen's claimed position
4. Is MCP (Model Context Protocol) gaining actual ecosystem traction beyond LangChain/LangGraph?
5. What is Kimi K2 Thinking's actual open-source availability?

## Source URLs
- https://agent.nexus/blog/top-10-open-source-ai-agent-frameworks
- https://super-apps.ai/blogs/open-source-ai-agent-frameworks-2026-complete-developer-comparison-guide
- https://alphacorp.ai/blog/the-8-best-ai-agent-frameworks-in-2026-a-developers-guide
- https://github.com/ARUNAGIRINATHAN-K/awesome-ai-agents
- https://www.clarifai.com/blog/top-10-open-source-reasoning-models-in-2026
- https://todatabeyond.substack.com/p/important-llm-papers-for-the-week-504

## Routing Relevance
- **subc (Dreamer):** Pattern signal — "compact models rival frontier" challenges existing beliefs about scaling laws; worth surfacing as a reframe opportunity
- **coder:** LangGraph and AutoGen are both Python-based; MCP tool integration is a concrete build signal
- **main:** No decisions pending; claims too weak for action
