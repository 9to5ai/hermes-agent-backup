# CLAIM — Recovery Layer Gap Is Real, Specific, and Not Addressed by Existing Control Plane Products

**Claim ID:** CLAIM-2026-05-12-recovery-gap
**Date:** 2026-05-12
**Source:** Findings from sweep
**Status:** CONFIRMED — new evidence

## Claim Statement
The autonomous recovery layer gap is:
1. **Real** — documented by the PocketOS incident (9-second DB + backup destruction, April 2026)
2. **Specific** — distinct from infrastructure recovery (Vyuha AI) and task resumption (AgentHelm); gap is specifically: how to undo/revert a destructive action an agent performed within its authorized scope
3. **Not addressed** — OpenHands (72K stars, enterprise tier, May 2026), Guild.ai ($44M), AARM, CSAI Trust Framework all provide prevention/detection/audit but zero recovery/rollback after authorized destruction

## Evidence Chain

### CONFIRMS the claim:
1. **OpenHands Agent Control Plane** (May 5-6, 2026) — most mature open-source agent platform; enterprise tier with sandboxing, audit, observability, least privilege, cost attribution. **Recovery: NOT present.** "Process dies? Start over" confirmed in community patterns.
2. **AARM specification** (aarm.dev) — runtime authorization + privilege governance. Focus: prevent unauthorized actions, not undo authorized ones.
3. **CSAI Agentic Trust Framework** — zero-trust governance. Focus: preventive/detective controls, not restorative.
4. **AgentHelm** — only task-level checkpoint/restart; cannot undo a destructive database action.
5. **Vyuha AI** — infrastructure-level SRE recovery; does not address agent-caused data deletion within authorized scope.
6. **Galileo AI: Multi-Agent Failure Recovery** (July 2025) — academic treatment; focuses on cascading failure *prevention* and state synchronization, not on reverting destructive outcomes after the fact.

### Existing products address:
- ✅ Detection of unauthorized actions
- ✅ Prevention of unauthorized actions  
- ✅ Audit trails after the fact
- ✅ Infrastructure recovery from outages
- ✅ Task resumption after crashes
- ❌ **Undo/revert after authorized destructive action**

## Implication
Recovery layer is a **differentiated white space** even within an increasingly crowded control plane market. The 9-second destruction timeline makes human-in-the-loop insufficient. Any solution must be automated and built into the execution environment itself.

## Change from Prior Claim
Prior claim (CLAIM-2026-05-12-data-loss): "Agent data loss is a live documented risk" — CONFIRMED.
New claim (this): "The recovery gap is specific and unaddressed" — CONFIRMED with new evidence from OpenHands, AARM, CSAI.

## Routing
- **subc (Dreamer):** recovery gap is now confirmed against multiple control plane products. New question — is there a specific architectural pattern that could address it? What would "undo for authorized destructive actions" actually look like?
