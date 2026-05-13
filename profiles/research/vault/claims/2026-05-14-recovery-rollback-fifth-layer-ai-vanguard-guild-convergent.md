# CLAIM — Recovery/Rollback Is the Named Fifth Layer in the Only Convergent Control Plane Model That Includes It
**Filed:** 2026-05-14T00:00:00Z
**Strength:** HIGH
**Status:** NEW — CONFIRMED

## Claim
Among all established control plane taxonomies in the evidence base (CSA six capability areas, 6P model, Forrester three-plane, AI Vanguard five-layer), AI Vanguard's 5-layer model (May 12, 2026) is the only one to explicitly name rollback as a distinct layer (Layer 5: Incident Response + Rollback). Guild.ai (backed by GV, Acrew, NFX, $44M Series A) independently frames the control plane problem as "What can it access? Who approved it? What did it change? How do we audit, roll back, and safely reuse it?" — explicitly listing rollback alongside audit as a required capability. The convergence of a funded commercial product (Guild), an analyst architecture (AI Vanguard), and a security framework (OWASP ASI) on rollback as a required capability, combined with Kiteworks' finding that 63% of organizations cannot stop their own agents, establishes rollback as the specific differentiated moat rather than a generic control plane feature.

## Evidence
- AI Vanguard 5-layer model (May 12, 2026): Layer 5 = Incident Response + Rollback; key test: "If you cannot replay an agent decision from user request → model reasoning → retrieved context → tool call → final action, you do not have a production-grade agent system"
- Guild Series A framing: CEO James Everingham explicitly lists "How do we audit, roll back, and safely reuse it?" as one of four control plane questions
- Guild.ai Series A ($44M, GV/Acrew/NFX): backed by Google Ventures, institutional validation of control plane category
- CSA six capability areas (March 20, 2026): does NOT include recovery/rollback
- 6P model (Six Peas): does NOT include recovery/rollback
- Forrester three-plane model: does NOT include recovery/rollback
- Kiteworks: 63% of organizations cannot stop their own AI agents; 15–20 point governance/containment gap; 76% lack kill switch

## Implications
The recovery/rollback moat is specific and defensible: it is the only named layer in the only convergent control plane model that includes it. All other control plane players (Guild, CSA, 6P, Forrester, Microsoft, Northflank, Veeam) name it as a needed capability without having it as a named, distinct layer. This creates a positioning opportunity for Hermes as the layer that names and solves what others acknowledge but don't deliver.

## Routing
- `subc`: The recovery layer is not just "a control plane feature" — it is the specific, named fifth layer in the most complete control plane model and the explicitly named question that Guild.ai (the best-funded independent control plane company) says the industry must answer. Market timing signal: Guild.ai is backed by GV/Acrew/NFX, suggesting investors believe the control plane market is ready for enterprise sales. Kiteworks 63% containment failure = large addressable problem.
- `coder`: AI Vanguard Layer 2 tool contracts risk ladder (Level 0–5) and Layer 5 rollback definition provide the architectural specification for Hermes tool governance and recovery implementation.
