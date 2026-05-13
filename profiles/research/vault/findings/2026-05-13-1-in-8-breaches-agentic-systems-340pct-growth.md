# FINDING — 1 in 8 Enterprise Breaches Involves Agentic Systems; 340% YoY Growth, 6.2x Cost Premium
**Date:** 2026-05-13T06:00:00Z
**Sources:** Digital Applied (digitalapplied.com/blog/ai-agent-security-2026-1-in-8-breaches-agentic-systems)
**Confidence:** HIGH

## Summary
1 in 8 enterprise security breaches now involve agentic AI systems as primary target, exploitation vector, or breach amplifier. Agent-involved breaches grew 340% year-over-year (2024–2025) and the growth rate is not decelerating into 2026. In high-adoption verticals (finance, healthcare), the ratio is already 1 in 5. Agent-involved breaches carry a 6.2x cost premium over non-agent incidents. 78% of agents are deployed with excess permissions.

## Evidence

### Primary — Digital Applied (sourced from CrowdStrike 2025 Global Threat Report, Mandiant IR data)
- **1 in 8 enterprise breaches** involve agentic AI systems (aggregates 3 categories: agent as primary target, agent as exploitation vector, agent as breach amplifier)
- **340% YoY growth** in agent-involved breach incidents, 2024–2025
- **6.2x total breach cost** vs. non-agent incidents (agents access more systems per incident)
- **78% of agents** deployed with excess permissions
- **80% enterprise application penetration** predicted by end of 2026 (high-adoption trajectory)
- High-adoption verticals (finance, healthcare): **1 in 5** breach ratio

### Attack Taxonomy (three categories)
1. **Primary Target Breaches** — Stealing agent credentials, poisoning training data/prompt injection, disrupting agent availability
2. **Vector Exploitation Breaches** — Compromised agent used for lateral movement, bypassing network segmentation
3. **Breach Amplification Incidents** — Agent in compromised environment accelerates propagation, scales attacker capabilities

### Novel Attack Class: Prompt Injection
Described as "SQL injection for agentic AI" — attacks exploiting core mechanism:
- **Direct prompt injection**: adversary submits conflicting instructions via UI/API
- **Indirect prompt injection**: malicious instructions embedded in external content agent retrieves (document, web page, API response)
- Example: PDF with white-text instructions to forward financial docs to external address

## Relationship to Prior Vault Findings
- Corroborates **enforcement-gap** (88% incident rate, 6% budget): breach rate rising despite known gap
- Corroborates **control-plane-established**: multi-system agent access requires control plane visibility
- Adds cost dimension (6.2x premium) to enforcement gap evidence
- Adds trajectory data (340% YoY) — prior vault had point-in-time stats, now confirmed accelerating

## Routing
- `subc`: 6.2x cost premium + 340% YoY growth = urgency signal for recovery layer market timing
- `coder`: 78% excess permissions = direct hygiene requirement for Hermes agent deployments
