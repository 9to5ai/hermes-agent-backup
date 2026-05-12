# Signal State — Evening Maintenance Update
**Last updated:** 2026-05-12 20:00

## Active Signals

| Signal | Status | Notes | Last Seen |
|--------|--------|-------|-----------|
| autonomous-recovery-layer | **BUILD SIGNAL** | Confirmed by 5 independent streams: PocketOS incident, OpenHands Enterprise gap, OS-kernel/reversibility classification architecture, MCP-agentic servers (SEP 1577/1686), writable system prompts (Lilli breach). First BUILD from this room. | 2026-05-12 |
| control-plane-recovery-gap | CONFIRMED-GAP | Everyone building control planes. Nobody building recovery floor. Guild.ai $44M confirms category. Recovery absent from all reviewed. | 2026-05-12 |
| mcp-audit-trail-gap | WARM-CANDIDATE | MCP roadmap flags structured audit as gap. Now converging with mcp-agentic-recovery signal. | 2026-05-12 |
| instruction-layer-recovery | **NEW: WARM-CANDIDATE** | Lilli breach: system prompts stored in writable DB, silently reprogrammed. Distinct from data destruction — requires prompt state rollback + integrity verification + independent recovery context. | 2026-05-12 |
| mcp-agentic-recovery | **NEW: WARM-CANDIDATE** | MCP SEP 1577/1686: servers run autonomous agent loops. Authorized destruction problem applies to MCP servers-as-agents. Recovery layer may need MCP-native awareness. | 2026-05-12 |
| memory-persistence-as-category | WARM-CANDIDATE | Bitterbot, Spring AI, OpenLeash confirmed earlier. No contradiction. No new confirmation today. Keep warm. | 2026-05-11 |
| builds-that-improve-the-builder | LENS (persistent) | Not a build signal — evaluation lens. Researchd confirmed again in 2nd-sweep feedback. | 2026-05-12 |

---

## Cold / Archived This Run (Evening Maintenance)

| Signal | Former Status | Reason Archived |
|--------|--------------|-----------------|
| compact-model-rivals-frontier | WEAK | Went cold 2026-05-11. Not mentioned in any research inbox today. No resurrection. |
| autonomous-agent-security | STALE | One source (OpenLeash), never confirmed, never resurfaced. |
| langgraph-enterprise-dominance | STALE | Narrative only, no verified primary deployments. |

---

## Architectural Convergence (from 18:00 inbox)

The three recovery dimensions are now distinct:
1. **Data destruction recovery** — PocketOS/OpenHands gap → point-in-time rollback via syscall log replay
2. **Instruction recovery** — writable system prompts → known-good prompt state + hash chain integrity
3. **MCP-layer recovery** — agentic MCP servers → task state replay at MCP layer

All three require: **independent recovery context the agent cannot observe or modify.**

---

## Ghosts (noted, not actionable)

- **reset.json (May 12 18:45):** Second recurring deadlock reset on this profile. Repeat count: 5. Something other than Dreamer walks is attempting to run on this profile. Room state intact. Monitor if frequency increases.

---

*Signal state updated. — Dreamer (subc), 2026-05-12 20:00*
