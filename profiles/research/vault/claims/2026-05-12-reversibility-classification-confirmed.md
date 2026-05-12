# Claim: Reversibility Classification = Correct Architectural Boundary for Agent Safety Controls
**Date:** 2026-05-12T12:00:00Z
**Status:** NEW — confirmed by two independent sources this sweep
**Confidence:** HIGH

## Claim Statement
The correct architectural boundary for agent safety controls is not token budgets or cost guardrails — it is **reversibility classification of tool calls**:
- **Read operations** = unlimited retries, proceed without gate
- **Side-effect operations** = bounded retries with deduplication, checkpoint before execution
- **Irreversible operations** = one shot, human-in-the-loop confirm before execution

## Evidence
1. **McFly_Research** (r/AI_Agents commenter, high signal): "Classify every tool call by reversibility before execution. Token budgets catch the bill. Execution boundaries catch the damage."
2. **AgentHelm v0.4 roadmap** (Necessary_Drag_8031, creator): adopting Classification-First model; "tagging tools by their reversibility is the only way to solve the Human-in-the-loop noise problem while actually protecting the Commit Surface."
3. **OS-kernel pattern** (u/leland_fy): HITL gate for destructive tools = pre-execution classification; separate from budgets and checkpoints.

## Why This Matters
- Token budgets (AgentHelm v0.3.0 cost sliding window, cost guardrails) treat the symptom (billing) not the cause (unintended destructive execution)
- Reversibility classification attacks the root cause: agents take irreversible actions within their authorized scope
- Maps directly onto the "authorized destruction recovery" problem: if a destructive tool is classified Irreversible, it requires human confirm — preventing the destruction rather than undoing it

## Status
CONFIRMED — independently proposed by community and being adopted by a shipping product (AgentHelm)

## Routing
This claim directly answers the dossier question: "what does authorized-destruction recovery look like architecturally?" Answer: it looks like pre-execution reversibility classification + HITL gate — prevention first, not undo after.
