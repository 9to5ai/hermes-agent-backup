# FINDING — CSAI Foundation: AARM + Agentic Trust Framework — Control Plane Standards Emerging

**Date:** 2026-05-12
**Source:** web search → CSAI Foundation blog (cloudsecurityalliance.org)
**Type:** finding
**Confidence:** high (official standards body)

## Signal

### CSAI Foundation Launches Agentic Control Plane Standards Work (April 29, 2026)
The CSAI Foundation (501(c)(3) arm of Cloud Security Alliance) announced its 2026 mission: **Securing the Agentic Control Plane**.

**Scale of existing foundation:**
- 1,000+ research publications
- 250,000+ individual members
- 500+ corporate members
- 12,000+ STAR certifications issued
- CSAI registered as **first CVE Numbering Authority (CNA) for AI security community**

**Key programs launched:**

### AARM — Autonomous Action Runtime Management (aarm.dev)
Open specification for securing AI-driven actions at runtime. Covers:
- Context, policy, intent, and behavior
- Runtime authorization with just-in-time access
- Agent privilege governance
- Zero-trust principles applied to autonomous agents

### Agentic Trust Framework (agentictrustframework.ai)
Applies zero-trust governance to autonomous AI agents.

**CxO engagement:**
- 160+ enterprise CISOs attended OpenClaw briefing
- 500+ participated in Mythos-readiness session

### Forbes Technology Council: Control Plane Must Be Centralized
Source: Forbes Council article (March 18, 2026) by Joan Vendrell, CEO NeuralTrust

Four disciplines of agentic governance:
1. **Discovery** — continuous detection of new AI activity, up-to-date map of capabilities/dependencies/data
2. **Control** — least privilege, explicit boundaries, consistent rules across environments
3. **Test** — probe for prompt injection, tool misuse, boundary bypass; test the control plane itself
4. **Protect** — real-time enforcement, not post-incident audit

## Relevance to Recovery Layer Thesis

**Institutional validation.** CSAI Foundation framing "Securing the Agentic Control Plane" as its 2026 mission — most ambitious expansion in 17-year history — signals that the control plane problem is now at the top of the institutional agenda. This follows Guild.ai ($44M), Cloudflare Agents, and OpenHands all independently converging on the same category.

**AARM is the closest existing spec to a recovery mechanism** — but it focuses on runtime authorization and privilege governance, not on restoring state after a destructive action. The distinction matters: AARM can prevent unauthorized destruction; it cannot undo destruction that was authorized (even if mistaken).

**Recovery is still outside the perimeter.** The Forbes article's four disciplines (Discover/Control/Test/Protect) are all preventive or detective. None address what happens after an agent successfully executes a destructive action that was within its authorized scope. This is the gap the PocketOS incident exposed.

**The CSAI CNA designation is significant** — AI-specific CVEs can now be issued directly for AI vulnerabilities. This creates a path for categorizing and tracking agent failure incidents systematically, which could eventually produce the incident data needed to drive recovery-layer requirements.

## Source URLs
- https://cloudsecurityalliance.org/blog/2026/04/29/securing-the-agentic-control-plane-key-progress-at-the-csai-foundation
- https://www.forbes.com/councils/forbestechcouncil/2026/03/18/ai-agents-wont-scale-without-a-centralized-control-plane/
- https://aarm.dev
- https://agentictrustframework.ai
