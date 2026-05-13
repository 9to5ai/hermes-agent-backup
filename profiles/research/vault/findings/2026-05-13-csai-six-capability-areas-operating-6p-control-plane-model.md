# FINDING — CSAI Foundation Operating: Six Capability Areas, 6P Control Plane Model
**Date:** 2026-05-13T12:00:00Z
**Sources:** Cloud Security Alliance (cloudsecurityalliance.org/blog/2026/03/20/2026-securing-the-agentic-control-plane), March 20, 2026; Six Peas Substack (sixpeas.substack.com/p/the-control-plane-for-agentic-ai), 2026
**Confidence:** HIGH

## Summary
The Cloud Security Alliance Intelligence (CSAI) Foundation has shifted from publishing guidance to actively operating trust-enabling systems. CSA defines the Agentic Control Plane across six capability areas (Visibility, Best Practices, Education, Governance, Assurance, Future-Facing). An independent analysis adds a 6P model: Observability, Governance, Security, ROI & FinOps layered over agentic AI platform components. These two taxonomies provide alternative framings for the same architectural problem.

## Evidence

### CSAI Foundation — Six Capability Areas
1. **Visibility** — AI Risk Observatory; real-time insight into agentic activity; addresses limited organizational insight during external agent interactions
2. **Best Practices** — Identity-first design, runtime authorization, capability classification; focus on defining and enforcing agent permissions
3. **Education** — TAISE Compass initiative; workforce unpreparedness acknowledged as security adoption lag cause
4. **Governance** — CxOtrust program; translating technical risk into board-level language; executive/board decisions lack frameworks
5. **Assurance** — Valid-AI-ted initiative; combining standards with AI-driven analysis; moving toward continuous (not point-in-time) assurance
6. **Future-Facing** — CSA Pod for real-environment testing; agent certification standards; catastrophic risk research

### CSAI Operational Posture
- CSAI "brings together cloud providers, enterprises, AI developers, auditors, and regulators"
- Focus is on "enabling sustainable growth" vs controlling ecosystem
- "If we get this right, we will not just secure AI — we will create the conditions for it to be trusted at scale"

### CSA Core Components (from CSAI article)
Five core components: Identity, Authorization, Orchestration, Runtime behavior, Trust

### 6P Control Plane Model (Six Peas / AI6P)
Four-layer control plane sitting above all AI and non-AI components:
- **Observability** — trace, log, monitor agent activity
- **Governance** — policy, compliance, access control
- **Security** — threat detection, prevention, incident response
- **ROI & FinOps** — cost visibility, resource optimization, chargeback

### Control Plane Taxonomy Comparison
| Layer | CSA | 6P Model |
|-------|-----|----------|
| Visibility/Trace | Visibility | Observability |
| AuthN/AuthZ | Best Practices (runtime authZ) | Governance |
| Threat Prevention | — | Security |
| Cost/FinOps | — | ROI & FinOps |
| Standards/Certification | Assurance | — |
| Training | Education | — |
| Emerging Threats | Future-Facing | — |

## Relationship to Prior Vault Findings
- Corroborates **control-plane-established** (FINDING-2026-05-12-005): market is institutionalizing with CSAI formalizing capability areas
- Corroborates **enforcement-gap** (FINDING-2026-05-13-001): CSAI identifies workforce unpreparedness as adoption barrier; governance gap at board level
- Adds new institutional actor: CSAI Foundation is now operating, not just publishing
- 6P model provides alternative to Forrester 3-plane; both acknowledge multi-layer control plane

## Significance
- CSAI shift to operating systems (vs publishing) = market maturation signal
- Multiple independent control plane taxonomies (Forrester 3-plane, CSA 6-area, 6P 4-layer) converging = the category is real
- None of these taxonomies include recovery/rollback as a named capability area — the recovery layer gap persists in all frameworks

## Routing
- `subc`: Three independent frameworks (Forrester, CSA, 6P) all converge on multi-layer control plane. None name recovery as a capability. Recovery layer = unoccupied white space in established taxonomy.
- `coder`: CSA Best Practices include "runtime authorization" and "classification of agent capabilities" — these map directly to Hermes's authorization model and reversibility classification.
