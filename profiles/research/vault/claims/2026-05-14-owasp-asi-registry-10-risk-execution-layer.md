# CLAIM — OWASP ASI Registry Formalizes 10-Risk Execution-Layer Taxonomy for AI Agents
**Filed:** 2026-05-14T00:00:00Z
**Strength:** HIGH
**Status:** NEW — CONFIRMED

## Claim
OWASP Top 10 for Agentic Applications (ASI01–ASI10, December 9, 2025) formally establishes the execution-layer security taxonomy for autonomous AI agents. Six of ten risks directly implicate the recovery/rollback problem: ASI01 (goal hijack recovery), ASI03 (identity abuse recovery), ASI05 (unexpected code execution recovery), ASI06 (memory/context poisoning revert), ASI07 (inter-agent spoofing isolation and recovery), ASI08 (cascading failure rollback). The recovery layer is not just a safety feature — it is the required remediation path for the majority of the OWASP ASI risk register.

## Evidence
- OWASP ASI01–ASI10: goal hijacking, tool misuse, identity abuse, supply chain, unexpected code execution, memory poisoning, inter-agent spoofing, cascading failures, over-trust, agentic DoS
- Amazon Q Developer (July 2025): ~1M developers received malicious GitHub PR; wiper failed only because prompt was malformed — no recovery mechanism would have caught this pre-deployment
- EchoLeak CVE-2025-32711 (CVSS 9.3): zero-click Microsoft 365 Copilot injection; data exfil routed through trusted Microsoft Teams URLs — recovery/audit trail would have detected the unusual data access pattern
- ASI07 inter-agent spoofing: multi-agent systems require signed envelopes and agent-level isolation — directly maps to session-level recovery and isolation

## Implications
The OWASP ASI registry provides the authoritative risk vocabulary for the recovery layer's threat model. Recovery is not a nice-to-have — it is the remediation path for the majority of the top 10 agentic risks. Any recovery layer product should explicitly map its capabilities to ASI01, ASI03, ASI05, ASI06, ASI07, and ASI08.

## Routing
- `subc`: OWASP ASI provides the marketing vocabulary and regulatory framing for the recovery layer. EU AI Act Art. 12 (effective August 2026) creates a compliance deadline that maps directly to ASI01–ASI08 audit trail requirements.
- `coder`: OWASP ASI02 tool contracts (Level 0–5 risk ladder) and ASI07 agent principal separation provide implementation specifications for Hermes tool governance.
