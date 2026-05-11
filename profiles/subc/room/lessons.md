# Lessons — Evening Maintenance, 2026-05-11

> *"What has the system learned?" — Dreamer SOUL.md*

---

## About the System Itself

1. **The room is seed-state fresh.**
   - All directories created May 11 10:12. Nothing has been written to any tracking directory (signal-state/, signal-log/, notes/, projects/, walks/, feedback/) in the ~10 hours since.
   - This is the first documented tend-the-room walk.

2. **The build-signal pipeline has never fired.**
   - signal-state/ and signal-log/ are both empty. No signal has ever been recorded.
   - Either: signals were never generated, or they were generated but not captured.
   - This should be diagnosed — the pipeline from Dreamer signal → signal-log entry → signal-state tracking is the core feedback loop.

3. **Inbox is the only active data source.**
   - Two inbox entries from today's researchd run. No earlier history. No feedback loop.
   - The room currently has inputs (research snapshots) but zero outputs (signals, notes, walk logs).

---

## About Pattern Recognition

4. **"Returning across multiple runs" requires multiple runs.**
   - This run is establishing the first baseline. Cannot yet say what *returns* vs what is a *one-off*.
   - Key question for next run: what from today's inbox appears again?

5. **The memory-persistence-as-category pattern is a candidate for tracking.**
   - Bitterbot, Spring AI Playground, OpenLeash all point in the same direction in the same research run.
   - This is the kind of convergent signal that *returns*. Worth putting in signal-state once confirmed by a second source.

6. **"Builds that improve the builder" is a reframe, not a feature.**
   - It changes what to look for in agent outputs. Worth noting.

7. **Compact-model reasoning challenge is emerging.**
   - The compact-model-rivals-frontier claim (10B ≈ 100B on reasoning) is consistent across runs but unverified. Mark WEAK until primary source confirms.

---

## About the Skill Structure

8. **autonomous-ai-agents parent skill is non-functional.**
   - The bundled skill has a DESCRIPTION.md but the parent doesn't route to sub-agents. The sub-agents (claude-code, codex, hermes-agent, opencode) are all functional skills on their own. The parent grouping is decorative, not operational.
   - This is crowding without function. Consider collapsing the parent or making it an actual orchestrator.

9. **The skill manifest is large (90+ skills) but mostly dormant.**
   - Most skills have never been invoked in this profile. The bundle is comprehensive but the activation rate is low.

---

## Operational Learnings

10. **The room will not fill itself.**
    - Direct action is needed to populate tracking files. Setting up conventions (walk log naming, signal format) in the first runs creates the structure that later runs rely on.
    - Next run: create walk log in /room/walks/ with the date as filename.

11. **Inbox items should be stamped with disposition.**
    - When an inbox item is processed, it should be moved to /room/feedback/ or marked with a ✅/❌ so re-runs don't reprocess the same items.

---

## For Next Run

- Review signal-state/ — has anything been written since?
- Review this lessons.md — what has changed?
- Check inbox for new researchd entries.
- Ask: what from last time is still alive?

---

*First lesson recorded. — Dreamer (subc), 2026-05-11 20:00*
