# CLAIM — Rollback Gap Quantified at 12%; Agent Versioning Requires Four-Layer Model
**Filed:** 2026-05-13T12:00:00Z
**Strength:** HIGH
**Status:** NEW — CONFIRMED

## Claim
Only 12% of autonomous agent deployments have robust rollback capability. Agent versioning requires four independent layers (code, prompt template, model version, tool/API contracts), any of which can break agent-to-agent dependencies. Recovery of an agent to a safe state after a destructive action requires handling nine distinct failure mode categories. The 12% stat quantifies the adoption gap; the four-layer + nine-runbook framework provides the architectural specification for addressing it.

## Evidence
- 12% rollback: LinkedIn/Vamshidhar Gudlanarva citing 2025 study
- Four-layer versioning: buildmvpfast.com/blog/agent-versioning-rollback-production-ai-update-zero-downtime-2026
- Nine runbooks: medium.com/@bhagyarana80/agent-rollback-drills-9-runbooks-for-real-chaos-8a5cf6aeba31

## Relationship to Prior Claims
- Distinct from: `recovery-gap-confirmed` (which was about OpenHands/AARM/Vyuha — absence of recovery products)
- Distinct from: `enforcement-gap` (which was about incident rate vs budget)
- This claim is specifically about the deployment architecture gap: even organizations trying to build robust agents are missing rollback

## Implications
- Recovery layer has two distinct sub-gaps: (1) data undo after authorized destruction, and (2) state rollback after any failure
- The four-layer versioning model = architectural specification for what Hermes recovery layer must track
- Nine runbook categories = nine product requirements for recovery layer testing

## Routing
- `subc`: 12% is a market readiness signal — if 12% have robust rollback already, the market knows the problem exists
- `coder`: Four-layer versioning = immediate implementation input for Hermes agent versioning system
