# FINDING — IETF Agent Audit Trail Standard (AAT) and Agent Identity Standards Emerging
**Date:** 2026-05-14T00:00:00Z
**Sources:** https://datatracker.ietf.org/doc/draft-sharif-agent-audit-trail/ (Individual Internet-Draft, expires Sep 29, 2026; last updated Mar 29, 2026); https://datatracker.ietf.org/doc/draft-sharif-aeba/ (last updated Apr 15, 2026); https://datatracker.ietf.org/doc/draft-nyantakyi-vaip-agent-identity/ (expires Oct 12, 2026); https://github.com/AiAgentKarl/agent-audit-trail-mcp; https://www.rockcybermusings.com/p/i-agent-authentication-authorization-gap
**Confidence:** HIGH

## Summary
The IETF has three active individual drafts establishing infrastructure standards for AI agent governance: (1) Agent Audit Trail (AAT, draft-sharif-agent-audit-trail) — a hash-chained JSON logging format for autonomous AI systems with EU AI Act Art. 12, SOC 2, ISO 42001, and PCI DSS compliance framing; (2) Agent Event Behaviour Analysis (AEBA, draft-sharif-aeba) — behavioral security monitoring framework; (3) Vorim Agent Identity Protocol (VAIP, draft-nyantakyi-vaip-agent-identity) — agent identity across systems. AAT defines L0–L4 trust levels, a URN-format agent_id scheme, and SHA-256 hash chaining per RFC 8785. An open-source MCP server implementation (AiAgentKarl/agent-audit-trail-mcp) already exists on GitHub.

## Evidence

### AAT Core Format
- **Mandatory fields:** record_id (UUIDv4), timestamp (RFC 3339), agent_id (URN format, e.g., `urn:agent:payment-bot.acme.example`), agent_version (SEMVER), session_id (UUIDv4), action_type, action_detail (object), outcome (success/failure/timeout/denied/escalated), trust_level (L0–L4), parent_record_id, prev_hash (SHA-256)
- **Hash chaining:** each record links to previous via SHA-256 per RFC 8785; tampering breaks chain for all subsequent records; ~0.01 ms per record hash
- **Action types defined:** tool_call, tool_response, decision (with reasoning_hash), delegation (with delegate_agent_id, constraints, timeout_ms), escalation (with urgency), error (with error_category, recoverable flag)
- **Trust levels:** L0 = no verification; L1 = self-signed key pair; L2 = Trust Authority issued passport; L3 = mutual authentication; L4 = L3 + revocation checking + continuous monitoring

### AAT Compliance Framing
- EU AI Act Article 12: high-risk AI systems must maintain automatic recording of events for entire lifecycle (effective August 2026)
- SOC 2 Trust Services Criteria
- ISO/IEC 42001 (AI management system standard)
- PCI DSS v4.0.1
- GDPR Article 17 compliance via tombstone-based deletion

### AEBA (Agent Event Behaviour Analysis)
- Behavioral security monitoring framework for autonomous AI
- Last updated April 15, 2026

### VAIP (Vorim Agent Identity Protocol)
- Agent identity across systems
- Expires October 12, 2026

### MCP Implementation
- AiAgentKarl/agent-audit-trail-mcp: open-source MIT-licensed MCP server implementing AAT-style hash-chained audit logging
- Tools: log_event, get_trail, verify_integrity, export_report, search_events, get_statistics
- EU AI Act Art. 12 compliance reporting built in
- Storage: append-only JSONL files in ~/.agent-audit-trail/

## Relationship to Prior Vault Findings
- **Corroborates** `FINDING-2026-05-13-009` (MCP roadmap four enterprise gaps): AAT directly fills the "structured audit trails and observability" gap named on the MCP 2026 roadmap — AAT's tool_call and tool_response action types map directly to MCP server interactions
- **Corroborates** `FINDING-2026-05-13-012` (Veeam/Microsoft/Northflank recovery moat): AAT provides the replay/recovery architectural substrate — without audit trail, replay is impossible
- **Extends** `FINDING-2026-05-13-007` (CSA six capability areas): AAT operationalizes CSA's Visibility and Assurance capability areas with a concrete standard
- **Direct input to** open question: "Is anyone building MCP-native structured replay/audit trail for agent sessions?" — Yes: AiAgentKarl/agent-audit-trail-mcp provides one implementation

## Routing
- `subc`: AAT + VAIP + AEBA = three converging IETF standards establishing audit trail and identity infrastructure. EU AI Act Art. 12 effective August 2026 creates regulatory deadline. AAT trust levels (L0–L4) provide vocabulary for recovery layer privilege classification.
- `coder`: AAT's URN-format agent_id, session_id (UUIDv4), and action type taxonomy (tool_call, decision, delegation, escalation) provide a production schema for Hermes agent event logging.
