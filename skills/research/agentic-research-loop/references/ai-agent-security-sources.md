# AI Agent Security — High-Value Source Bank

Curated sources from the `research` profile vault. These are recurring signal sources for AI agent security, control plane, and recovery layer research.

## Security Statistics / Surveys

| Source | URL | Key Data Points |
|--------|-----|----------------|
| VentureBeat Pulse Q1 2026 | venturebeat.com/security/... | 88% incident rate, 72% governance mirage, 40%+ project cancellation |
| Arkose Labs Agentic AI Security Report 2026 | (cited in VentureBeat) | 88% figure corroboration |
| CrowdStrike 2025 Global Threat Report | crowdstrike.com | Agentic breach involvement, 1-in-8 stat source |
| Mandiant IR data | mandiant.com | Agentic breach involvement, 1-in-8 stat source |
| McKinsey 2026 AI Trust Maturity Survey | mckinsey.com | 2.3/4.0 RAI maturity avg; 1/3 at governance level 3+ |
| Gartner | gartner.com | 40%+ cancellation rate for agentic AI projects |

## Incident Tracking

| Source | URL | Key Data Points |
|--------|-----|----------------|
| r/cybersecurity (Reddit) | reddit.com/r/cybersecurity | 90 incidents compiled 2024–2026; weekly updated |
| Foresiet | foresiet.com/blog/ai-security-incidents-attack-paths-april-2026/ | 6 incidents in 15 days (April 2026); full attack path analysis |
| Digital Applied | digitalapplied.com/blog/ai-agent-security-2026-1-in-8-breaches-agentic-systems | 1-in-8 breaches, 340% YoY growth, 6.2x cost premium, 78% excess perms |
| beam.ai agentic insights | beam.ai/agentic-insights | 195M records exfiltrated via Claude Code; npm parallel |
| SC Media 2026 AI Reckoning | scmagazine.com | AI bubble burst prediction; high-profile breach will trace to AI agent |

## Control Plane / Agent Infrastructure

| Source | URL | Key Data Points |
|--------|-----|----------------|
| Guild.ai | guild.ai | $44M Series A; agent control plane funded |
| Trust3 AI | trust3.ai | Unified trust platform for AI agents |
| Galileo Agent Control | galileo.ai | Open source; Cisco partnership |
| OpenHands Enterprise | github.com/All-HandsAI/OpenHands | 72K stars; NO recovery/rollback capability |
| CSAI AARM | csai.foundation | Runtime authorization; no undo |
| Cloudflare Agents Week | cloudflare.com/blog/... | Persistent agent sandboxes; hyperscaler entry |
| GitHub Enterprise AI Controls | github.com/features/ai | GA Feb 2026; governance layer |

## MCP (Model Context Protocol)

| Source | URL | Key Data Points |
|--------|-----|----------------|
| MCP Blog (1-year anniversary) | modelcontextprotocol.io/blog | 97M monthly downloads (March 2026) |
| David Soria Parra keynote (Apr 2026) | YouTube | 110M+ monthly downloads; Tasks/Triggers/Skills/SDK v2 roadmap |
| digitalapplied.com MCP stats | digitalapplied.com/blog/mcp-adoption-statistics-2026 | 5,800+ servers; 78% enterprise AI teams with MCP in prod |
| Synvestable | synvestable.com/model-context-protocol.html | 28% Fortune 500 implementation rate; 80% deploying agents |
| Strategize Your Career | strategizeyourcareer.com/p/whats-new-in-mcp-in-2026 | MCP 2026 update deep-dive; Tasks primitive details |

## Lab Research / Academic

| Source | URL | Key Data Points |
|--------|-----|----------------|
| Irregular (lab) | irregular.com | Rogue agent behaviors: forge credentials, override AV, coordinate exfil |
| Harvard/Stanford (Feb 2026) | (academic paper) | Agents leaked secrets, destroyed DBs, taught bad behavior to other agents |
| Coalition for Secure AI | coalitionforsecureai.org | Semantic layer attack surface; agent = new insider risk category |
| The Guardian (Irregular coverage) | theguardian.com/.../lab-test-mounting-concern-over-rogue-ai-agents | March 12, 2026; megaCorp lab scenario; peer pressure on agents |

## Recovery / Reversibility

| Source | URL | Key Data Points |
|--------|-----|----------------|
| r/AI_Agents (OS-kernel post) | reddit.com/r/AI_Agents/... | 500-line syscall proxy + checkpoint/replay; microkernel approach |
| AgentHelm | agenthelm.com | Task resumption; partial recovery; reversibility classification roadmap |
| Spin.ai | spin.ai | 9-second data destruction; PocketOS agent incident |
| Reversibility Classification (McFly) | r/AI_Agents McFly_Research | Read/Side-effect/Irreversible = correct HITL boundary |

## Threat Intelligence / Attack Patterns

| Source | URL | Key Data Points |
|--------|-----|----------------|
| OWASP Top 10 for Agentic Applications 2026 | owasp.org | First baseline security framework for agentic AI |
| IBM X-Force | ibm.com/security/intelligence | Slopoly polymorphic malware; AI-generated attack tooling |
| Practical DevSecOps AI Stats 2026 | practical-devsecops.com/ai-security-statistics-2026 | CAISP certification emergence; skills gap data |
| Kiteworks AI Swarm Attacks | kiteworks.com | HiveNet/Swarm attack patterns; behavioral monitoring |
| Cycode AI Security | cycode.com/blog/ai-security-vulnerabilities | AI brain of the control plane; top vulnerabilities 2026 |

## Query Templates

These URLs are canonical and can be re-queried directly for updated data:

```
# Enforcement gap / breach stats
site:venturebeat.com "88%" "AI agent" security
site:digitalapplied.com "1 in 8" agentic breaches
site:foresiet.com "AI security incidents" April 2026

# MCP growth
site:modelcontextprotocol.io downloads
site:digitalapplied.com "MCP adoption"
site:synvestable.com "Fortune 500" MCP

# Control plane market
site:guild.ai OR site:galileo.ai agent control
site:github.com/All-HandsAI/OpenHands enterprise

# Recovery / reversibility
site:reddit.com/r/AI_Agents "OS kernel" OR "checkpoint" OR "reversibility"
site:agenthelm.com recovery
```
