# Finding: Reversibility Classification Pattern Proposed for Agent Tool Calls
**Date:** 2026-05-12
**Confidence:** HIGH
**Source:** Reddit r/AI_Agents — comment thread on AgentHelm v0.3.0 launch post

## Evidence
McFly_Research ( commenter, 1mo ago) proposed a reversibility-based classification for agent tool calls:

> "The agent loops because nothing told it to stop — the loop is a valid execution path from the model's perspective."

> "Classify every tool call by reversibility before execution. Read operations = unlimited retries. Side-effect operations = bounded retries with dedup. Irreversible operations = one shot, human confirm if failed."

Author (Necessary_Drag_8031, AgentHelm creator) responded:
> "I'm currently architecting exactly what you described for the next SDK update: moving from a flat decorator to a Classification-First model (Read vs. Side-Effect vs. Irreversible). Tagging tools by their 'reversibility' is the only way to solve the Human-in-the-loop noise problem while actually protecting the 'Commit Surface.'"

## Key Distinction
Token budgets (cost guardrails) catch the bill. Execution boundaries (reversibility classification) catch the damage.

## Implication
- **Reversibility classification = correct architectural boundary for agent safety controls**
- AgentHelm is moving toward this model in next SDK update (v0.4.x)
- This pattern directly addresses the "authorized destruction" problem: destructive tools are Irreversible = one shot + human confirm
- Contrast with token budget approach (AgentHelm's current v0.3.0 cost sliding window) which only catches cost, not damage

## Connection to Prior Findings
- Confirms recovery gap framing: existing solutions (cost guardrails, loop detection) treat symptoms
- Complements OS-kernel pattern finding: both point toward pre-execution validation as the correct layer
- Provides specific terminology: "Commit Surface" — the set of irreversible actions requiring HITL

## Citation
- Reddit: https://www.reddit.com/r/AI_Agents/comments/1s5wvhc/i_was_tired_of_2_am_agent_loops_burning_my_api/
- AgentHelm v0.3.0 release post by u/Necessary_Drag_8031
