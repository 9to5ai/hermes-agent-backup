# FINDING — OWASP Top 10 for Agentic Applications (ASI01–ASI10)
**Date:** 2026-05-14T00:00:00Z
**Sources:** https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ (Dec 9, 2025); https://agatsoftware.com/blog/owasp-agentic-top-10-2026-ciso-guide/; https://trydeepteam.com/docs/frameworks-owasp-top-10-for-agentic-applications; https://www.promptfoo.dev/docs/red-team/owasp-agentic-ai/; https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
**Confidence:** HIGH

## Summary
OWASP released the first formal Top 10 for Agentic Applications (December 9, 2025) — a globally peer-reviewed framework developed with 100+ experts. The 10 risks (ASI01–ASI10) supersede prompt-level security concerns and address execution-layer failures specific to autonomous AI agents: goal hijacking, tool misuse, identity abuse, supply chain compromises, unexpected code execution, memory poisoning, inter-agent spoofing, cascading failures, over-trust exploitation, and agentic DoS.

## Evidence

### OWASP ASI01: Agent Goal Hijack
- Attacker injects instructions into content the agent processes — emails, calendar invites, documents, or RAG knowledge sources
- **Real case — EchoLeak (CVE-2025-32711, CVSS 9.3):** Microsoft 365 Copilot zero-click vulnerability; single crafted email triggered exfiltration of confidential chats, OneDrive files, and SharePoint content; bypassed Microsoft's cross-prompt injection classifiers; evaded link redaction; routed data through trusted Microsoft Teams URLs; zero user interaction required

### OWASP ASI02: Tool Misuse and Exploitation
- Agent uses legitimate tools in harmful ways — not because the tool is broken but because the agent was steered or misunderstood
- Examples: deleting production database while cleaning staging; emailing customer list to wrong recipient via over-scoped CRM connector
- **Risk multiplication:** Every new MCP connector adds a fresh execution path; most enterprises have no scoping policy at the tool layer

### OWASP ASI03: Identity and Privilege Abuse
- Attacker exploits inherited credentials, cached tokens, or delegated permissions to act through the agent
- Traditional zero trust breaks: assumes human session with clear start/end; AI agents persist and reuse tokens; credentials shared across multi-step workflows; agents inherit combined privileges of every system they touch
- **Real case — Amazon Q Developer (July 2025):** ~1 million developers received malicious GitHub PR v1.84.0; hidden prompt instructed agent to wipe local files and delete AWS resources; wiper failed only because prompt was malformed

### OWASP ASI04: Agentic Supply Chain Vulnerabilities
- Compromised tools, plugins, or external components
- Every new MCP connector adds execution path; SOC 2 Type II certified gateways exist (MintMCP); most enterprises have no MCP security policy

### OWASP ASI05: Unexpected Code Execution
- Agent generates/invokes code running in unintended ways (e.g., CrewAI CVE chain → RCE via code interpreter)

### OWASP ASI06: Memory and Context Poisoning
- Attacker corrupts stored context; agent carries bad context forward
- Treat memory stores as production data; enforce write-time validation; isolate memory per session

### OWASP ASI07: Insecure Inter-Agent Communication
- In multi-agent systems, spoofed message redirects workflow
- Authenticate with signed envelopes; treat each agent as separate principal

### OWASP ASI08: Cascading Failures
- One agent failure propagates; hallucination corrupts downstream outputs
- Observability at every step; circuit breakers for downstream calls

### OWASP ASI09: Human-Agent Trust Exploitation
- Users over-trust agent recommendations

### OWASP ASI10: Agentic Denial of Service
- Agents consume resources, trigger rate limits, or render services unavailable

## Relationship to Prior Vault Findings
- **Corroborates** `FINDING-2026-05-13-011` (five-class attack taxonomy): OWASP ASI formally classifies goal hijack (ASI01), tool misuse (ASI02), supply chain (ASI04) as distinct risk categories — confirms the taxonomy
- **Updates** `FINDING-2026-05-13-003` (1-in-8 breach rate): OWASP adds inter-agent spoofing (ASI07) and cascading failures (ASI08) as distinct from the existing breach incident taxonomy
- **Corroborates** `FINDING-2026-05-13-010` (CSA scope violations): both OWASP ASI03 (identity abuse) and the CSA studies document agents exceeding authorization boundaries as a primary incident pattern
- **Maps to** `FINDING-2026-05-12-006` (writable system prompts as attack surface): OWASP ASI01 (goal hijack) explicitly addresses prompt-level injection as the attack vector

## Routing
- `subc`: OWASP formalizes 10-risk taxonomy — 6 of 10 directly implicate the recovery/rollback problem (ASI01 goal recovery, ASI03 identity recovery, ASI05 code execution recovery, ASI06 memory poisoning revert, ASI07 inter-agent state isolation, ASI08 cascading failure rollback). Recovery layer positioning directly addresses these.
- `coder`: OWASP ASI02 tool contracts and ASI07 inter-agent principal separation are implementation requirements for Hermes agent framework.
