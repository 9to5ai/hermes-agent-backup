# FINDING — Guild.ai $44M Series A: Specific Backing, CEO Background, and Control Plane Definition; AI Vanguard 5-Layer Control Plane Model with Explicit Rollback Layer
**Date:** 2026-05-14T00:00:00Z
**Sources:** https://www.guild.ai/knowledge/news/guild.ai-raises-a-series-a; https://www.globenewswire.com/news-release/2026/04/29/3284142/0/en/guild-ai-introduces-the-first-control-plane-for-ai-agents.html; https://aivanguard.tech/ai-agent-control-plane-2026/ (Ehab Al Dissi, updated May 12, 2026)
**Confidence:** HIGH

## Summary
Guild.ai Series A specifics: $44M raised from GV (Google Ventures), Acrew Capital, and NFX. CEO James Everingham previously ran Meta's 1,000-person Developer Infrastructure organization. Guild explicitly frames the control plane problem as: "What can it access? Who approved it? What did it change? How do we audit, roll back, and safely reuse it?" Guild positions immutable audit logging, least-privilege access, centralized identity, typed interfaces, versioned releases, and safe execution boundaries as the core primitives. Separately, AI Vanguard's control plane architecture (May 12, 2026) defines a 5-layer model: (1) Identity/Permission Boundaries, (2) Tool Contracts, (3) Memory Governance, (4) Guardrails/Approval Gates, (5) Incident Response + Rollback — the only model in the evidence base to explicitly name rollback as Layer 5.

## Evidence

### Guild.ai Series A Specifics
- **Backers:** GV (Google Ventures), Acrew Capital, NFX
- **CEO:** James Everingham — previously VP of Meta Engineering, ran 1,000-person Developer Infrastructure organization
- **Current problem statement:** Agents are now executing across repos, CI/CD pipelines, data stores, credentials, and incident workflows — once teams cross that line, the question is: "What can it access? Who approved it? What did it change? How do we audit, roll back, and safely reuse it?"
- **Core governance primitives:**
  - Centralized identity for agents
  - Least-privilege access enforcement
  - Immutable audit logging
  - Typed interfaces and versioned releases
  - Safe execution boundaries
  - Full execution traces
- **Agent Hub:** GitHub-like public platform for agent discovery and reuse — builds agents like real software and ships as products
- **Guild positions itself as neutral:** works with Anthropic, OpenAI, Google, and open-source models; no governance lock-in to single stack
- **Agent lifecycle coverage:** build, deploy, govern, share in production; run via chat, APIs, webhooks, and schedules

### AI Vanguard 5-Layer Control Plane Model (May 12, 2026)
- **Author:** Ehab Al Dissi; updated May 12, 2026
- **Layer 1 — Identity and Permission Boundaries:** Delegated identity (agent acts on behalf of user/team/workflow role); every action carries human/business owner, agent identity, tool/system touched, permission scope, approval state
- **Layer 2 — Tool Contracts:** Purpose, inputs, validation rules, stable response shapes, risk level (Level 0 read public → Level 5 financial/legal/security), timeout behavior, audit fields
- **Layer 3 — Memory Governance:** Session memory (minutes to hours), user memory (until revoked), workflow memory (versioned), enterprise knowledge (source-controlled); rule: sales email agent should not inherit HR notes; support agent should not remember payment details beyond transaction window
- **Layer 4 — Guardrails and Approval Gates:** Input guardrails (classify risk before agent acts), tool guardrails (check proposed call), output guardrails (verify final answer)
- **Layer 5 — Incident Response + Rollback:** Explicit rollback included; key test: "If you cannot replay an agent decision from user request → model reasoning → retrieved context → tool call → final action, you do not have a production-grade agent system"

### AI Vanguard Key Framing
- "The model is the reasoning engine. The control plane is the production system around it. In enterprise AI, the second one decides whether the first one is useful."
- "AI agents fail in production for boring reasons, not capability reasons: call wrong tool, stale context, cannot distinguish reversible drafts from irreversible actions, retry failed APIs until rate limits, expose private docs, write confident answers nobody can trace"
- "The control plane turns an agent from 'LLM plus tools' into a managed operational actor"

## Relationship to Prior Vault Findings
- **Corroborates** `FINDING-2026-05-13-012` (Veeam/Microsoft/Northflank recovery moat): both Guild and AI Vanguard explicitly name rollback/replay as a required control plane capability
- **Updates** `FINDING-2026-05-13-007` (CSA six capability areas) and `FINDING-2026-05-13-012` (three convergent taxonomies): AI Vanguard 5-layer model adds the explicit rollback layer (Layer 5) that was missing from CSA's six capability areas and the three convergent taxonomies
- **Corroborates** `FINDING-2026-05-13-003` (1-in-8 breach, 78% excess perms): Guild CEO's framing of agents now executing across repos, data stores, credentials confirms the attack surface that produces the documented breach patterns
- **Direct input to** open question: "Guild.ai product details — does their control plane have any recovery capability?" — Guild positions "audit, roll back, and safely reuse" as core questions but no explicit recovery capability described in available materials

## Routing
- `subc`: Guild Series A ($44M, GV/Acrew/NFX) validates the control plane market. AI Vanguard 5-layer model explicitly includes rollback as Layer 5 — first model to name rollback as a distinct layer. The convergence of Guild (enterprise product), AI Vanguard (analyst architecture), and the OWASP ASI (security framework) on rollback/replay as a required capability is significant.
- `coder`: AI Vanguard Layer 2 tool contracts (risk ladder: Level 0 read → Level 5 financial/legal) provide the tool risk classification framework for Hermes tool exposure policy.
