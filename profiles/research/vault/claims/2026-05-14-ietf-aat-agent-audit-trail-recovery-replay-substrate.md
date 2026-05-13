# CLAIM — IETF Agent Audit Trail (AAT) + Identity Standards Establish Recovery/Replay Infrastructure Substrate
**Filed:** 2026-05-14T00:00:00Z
**Strength:** HIGH
**Status:** NEW — CONFIRMED

## Claim
Three active IETF individual drafts (AAT, AEBA, VAIP) collectively establish the infrastructure substrate for AI agent recovery and replay: (1) AAT defines hash-chained, tamper-evident logging with EU AI Act Art. 12 compliance and L0–L4 trust levels; (2) AEBA defines behavioral security monitoring for autonomous AI; (3) VAIP defines agent identity across systems. An open-source MCP server implementation (AiAgentKarl/agent-audit-trail-mcp) already exists, demonstrating feasibility. AAT's explicit tool_call, decision, and delegation action types with session_id and agent_id provide the data model for session replay and selective undo.

## Evidence
- AAT action types: tool_call (with parameters_hash), tool_response (with response_hash), decision (with reasoning_hash), delegation, escalation, error — each with timestamp, session_id, agent_id, and prev_hash
- AAT session_id (UUIDv4): consistent across all records in a session — enables full session replay
- AAT reasoning_hash: SHA-256 of chain-of-thought stored in decision records — enables reconstruction of agent reasoning at any point
- AAT L0–L4 trust levels: maps to the reversibility classification from prior vault (L0 = no verification; L4 = full mutual auth with revocation)
- AiAgentKarl/agent-audit-trail-mcp: MIT-licensed MCP server implementing AAT-style logging with verify_integrity and export_report tools
- EU AI Act Art. 12: mandatory automatic recording of events for entire lifecycle of high-risk AI systems (effective August 2026) — creates regulatory pull for AAT-compliant logging

## Implications
Recovery/replay requires: (a) complete event log, (b) tamper-evident storage, (c) session-level identity, (d) reasoning reconstruction. AAT provides all four as a published standard. The recovery layer does not need to invent its own logging schema — it can adopt AAT as the canonical format. The open-source MCP implementation demonstrates that AAT is implementable today.

## Routing
- `subc`: AAT is the closest thing to a canonical standard for agent event logging. If Hermes Recovery Layer adopts AAT format, it becomes immediately interoperable with any other AAT-compliant system. EU AI Act Art. 12 creates enterprise procurement pull for AAT-compliant audit trails.
- `coder`: AAT's JSON schema (record_id, timestamp, agent_id, session_id, action_type, action_detail, outcome, trust_level, prev_hash) is a production-ready schema for Hermes agent event logging. The four-layer reversibility classification (read unlimited, side-effect checkpoint, irreversible HITL) maps directly to Hermes tool risk classification.
