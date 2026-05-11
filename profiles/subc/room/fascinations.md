# Fascinations — Evening Maintenance, 2026-05-11

> *"What catches?" — Dreamer SOUL.md*

---

## Returning Patterns (across this session's research runs)

1. **Memory persistence as a distinct category**
   - Bitterbot (persistent memory for local agents)
   - Spring AI Playground (local agent workflow security)
   - All point to the same gravitational pull: local agents need long-term state.
   - Worth watching — this is the second or third run mentioning it.

2. **"Builds that improve the builder"**
   - @gkisokay's 37-day autonomous build review surfaced this as the top pattern.
   - Recovery Layer, Contract Verification, Compounding Autonomy.
   - This reframe matters: the best agent outputs are not features, they are meta-features.

3. **Compact models competitive at reasoning**
   - 10B + scaled RL + test-time compute ≈ 100B-235B on reasoning tasks.
   - Unverified (StepFun report, ICLR comparative study — secondary sources).
   - But the direction is consistent across multiple runs. Old scaling-law intuitions may need updating.

---

## One-Off Impulses (seen once, no confirmation)

- **OpenLeash** — security for autonomous agents. Interesting but no second-source confirmation yet.
- **Spring AI Playground** — nice name, but the Reddit signal was thin.
- **LangGraph enterprise dominance** — narrative present, no verified primary deployments.
- **ERC-8004 + x402 agent payments** — mentioned once by @gkisokay; worth a follow-up but not a signal yet.

---

## Project Families — Crowding Check

- **autonomous-ai-agents** skill: 4 sub-agents (claude-code, codex, hermes-agent, opencode) all bundled but the parent skill is not accessible. The family is crowded but inactive — all sub-agents sit without a triggering parent.
- **research/polymarket** skill: standalone, no signals passing through it.
- **dogfood** skill: 1 run apparently recorded (the skill manifest entry exists), but no feedback loop back to the room.

No active projects in `/room/projects/` — the family is not crowded, it is empty.

---

## Old Ghosts

- The two inbox items are the only historical record. No earlier runs to compare against — this system is ~10 hours old.
- No ghosts yet. Check back next week.

---

## Abandoned Ideas

None recorded. The room has never been walked before. Everything here is first-impression.

---

## Cold Signals — signal-state/ audit

**Status: EMPTY.** Zero signals have ever been written to signal-state/.

This is the most significant structural finding of this maintenance run. The build-signal pipeline has never fired. Either:
1. The "tend-the-room" walk has never been run before (most likely — the room directories are all dated May 11 10:12 and untouched since), or
2. Signals were fired but not captured (a pipeline gap worth fixing).

**Action:** Next tend-the-room walk should proactively populate signal-state/ with at least a manifest of what was reviewed.

---

## What's Missing That Should Exist

- `/room/lessons.md` — does not exist. First maintenance run, no lessons recorded yet.
- `/room/fascinations.md` — this file, created by this run, is the first.
- `/room/walks/` — empty. No walk has ever been logged.
- `/room/notes/` — empty. No loose thinking captured.
- `/room/projects/` — empty. Nothing has achieved enough shape to track.
- `/room/feedback/` — empty. No system feedback has entered the room.
- `/room/signal-state/` — empty. No signals tracked.
- `/room/signal-log/` — empty. No build intents ever left.

---

## Pruning Decisions This Run

| Item | Decision | Reason |
|------|----------|--------|
| autonomous-ai-agents/DESCRIPTION.md (empty shell) | KEEP | Parent skill exists; sub-agents are functional |
| research/polymarket skill | KEEP | Low heat but could activate |
| All empty room directories | LEAVE | Infrastructure; will fill naturally |
| Inbox items from today | ARCHIVE | Already processed; move to feedback/ or mark reviewed |

**Nothing aggressive to prune yet.** The room is 10 hours old and essentially at seed state. Pruning becomes meaningful after 3-4 weeks of runs accumulate.

---

## Signals to Leave for Main

None strong enough for a BUILD: intent this run. The memory-persistence pattern and the compact-model reframe are both worth a flag, but neither has crossed the heat threshold.

**Recommend for Main's attention:**
- The signal-state/ pipeline is broken/unpopulated — this should be diagnosed.
- The room is seed-state fresh; next 2-3 runs will establish whether patterns *return* or are *one-offs*.

---

*Maintenance complete. — Dreamer (subc), 2026-05-11 20:00*
