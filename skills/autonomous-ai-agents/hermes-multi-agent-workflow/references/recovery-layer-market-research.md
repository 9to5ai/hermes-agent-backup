# Recovery Layer — Market Research Reference
*Fourth research sweep — 2026-05-12T06:00:00Z*

## What the Research Found

### Core Claim (ESTABLISHED)
The autonomous recovery layer gap is **specific** and **unaddressed** by any known product:
- Not infrastructure recovery (Vyuha AI — SRE tier)
- Not task resumption (AgentHelm — checkpoint/restart)
- Not runtime authorization (CSAI AARM — privilege governance)
- Not control plane per se (OpenHands — 72K stars, no recovery)

The specific gap: **undoing a destructive action an agent performed within its authorized scope.**

### Why 9 Seconds Matters
The PocketOS incident (April 2026): Cursor agent destroyed production DB + all volume-level backups in 9 seconds. Human-in-the-loop cannot react in time. The solution must be automated and baked into the execution environment.

### Products Assessed

| Product | Scope | Has Recovery? | Notes |
|---------|-------|---------------|-------|
| OpenHands Enterprise | control plane | **NO** | "Process dies? Start over" confirmed; isolation/audit only |
| CSAI AARM | runtime authorization | **NO** | Prevents unauthorized; cannot undo authorized destruction |
| AgentHelm | task resumption | partial | Step-level checkpoint/restart; cannot undo DB deletion |
| Vyuha AI | infrastructure SRE | yes | Recovers cloud outages; not agent state |
| OS-kernel pattern | agent runtime | **NO** | Community; recognizes gap exists |
| Guild.ai ($44M) | control plane | **NO** | Governance + audit; no rollback documented |
| AARM spec | standard | **NO** | Runtime privilege governance; zero restorative mechanism |

### Control Plane Category — Confirmed
- Guild.ai: $44M Series A (April 29, 2026)
- OpenHands Enterprise: 72K stars, enterprise tier (May 5-6, 2026)
- CSAI Foundation: "Securing the Agentic Control Plane" as 2026 mission (April 29, 2026)
- Forbes Tech Council: four disciplines (Discover/Control/Test/Protect) — all preventive/detective
- CSAI registered as first CVE Numbering Authority for AI security
- Cloudflare Agents Week: persistent sandbox environments

### MCP — Mainstream
- Downloads: 100K (Nov 2024) → 97M+ monthly (2026)
- Fortune 500 implementation: 28%
- Server registry: 7.8x growth in one year
- Stewardship: donated to Agentic AI Foundation (Linux Foundation)
- Security concerns active on r/cybersecurity (prompt injection, mcp-server-git chain)

## Implications for Build Decisions

1. **Recovery is the white space** — even the most mature control plane (OpenHands 72K stars) has no recovery. This is not "everyone's building it and it's commodity" — it's "nobody is building it at all."

2. **The specific problem is narrower than "recovery"** — it's not infra recovery (solved) or task resumption (solved adjacent). It's specifically: undo for authorized destructive actions within the agent's scope.

3. **MCP-native positioning** — if MCP is the USB-C of agent tool integration, the recovery layer may need to be MCP-native to be relevant at the right interception point.

4. **9-second destruction timeline** — forces fully automated recovery, not human-in-the-loop. Any solution needs to be baked into the execution environment, not applied after the fact.

## Source URLs (Fourth Sweep)
- https://cloudsecurityalliance.org/blog/2026/04/29/securing-the-agentic-control-plane-key-progress-at-the-csai-foundation
- https://www.forbes.com/councils/forbestechcouncil/2026/03/18/ai-agents-wont-scale-without-a-centralized-control-plane/
- https://www.businesswire.com/news/home/20260506314667/en/OpenHands-Launches-an-Agent-ontro
- https://www.openhands.dev/blog/openhands-enterprise-agent-control-plane
- https://openhands.dev/blog/agent-control-plane
- https://www.reddit.com/r/AI_Agents/comments/1s5wvhc/i_was_tired_of_2_am_agent_loops_burning_my_api/ (AgentHelm)
- https://www.reddit.com/r/ArtificialInteligence/comments/1selkyi/i_got_tired_of_3_am_pagerduty_alerts_so_i_built/ (Vyuha AI)
- https://www.reddit.com/r/AI_Agents/comments/1rr5xx9/i_built_an_os_kernel_for_llm_agents_in_500_lines/
- https://spin.ai/blog/ai-agents-data-loss-backup/ (PocketOS incident)
- https://galileo.ai/blog/multi-agent-ai-system-failure-recovery
