---
name: research-agent-loop
category: research
description: Recurring research agent loop for the research profile — vault health, research sweep, findings/claims processing, dossier maintenance, decision ledger, subc routing, run receipts.
---

# Research Agent Loop — SKILL.md
## Profile: research | Recurring cron job

---

## Trigger Conditions

- Scheduled cron execution (e.g., every 6 hours: 00:00, 06:00, 12:00, 18:00)
- Manual invocation: `run research agent loop for profile 'research'`
- Any task instruction containing "research sweep", "vault health", "research profile"

---

## Pre-Run Checklist (Always Read Prior Run First)

Before starting, read:
1. `vault/health/<prior-timestamp>.md` — prior health status
2. `vault/runs/<prior-timestamp>.md` — prior run receipt (what was produced, what surfaces were active)
3. `vault/sources/registry.md` — registered surfaces and cadence
4. `vault/decisions/STALE_CHECK-<prior-timestamp>.md` — prior decision ledger state

This prevents duplicating work and tells you what surfaces are pending vs triggered.

---

## Workflow Summary

```
1. Check vault health          → health/<run-timestamp>.md
2. Run research sweep          → raw/<run-timestamp>.md
3. Process findings            → findings/ (conditional on novelty)
4. File claims                 → claims/ (conditional on novelty)
5. Update dossier             → dossiers/<dossier>.md (every run)
6. Check decision ledger       → decisions/STALE_CHECK-<run-timestamp>.md
7. Route to subc              → subc/room/inbox-from-researchd/<run-timestamp>.md (conditional)
8. Write run receipt          → runs/<run-timestamp>.md
```

---

## Vault Structure

All paths under `~/.hermes/profiles/research/vault/`:

| Directory | Purpose | File Naming |
|-----------|---------|-------------|
| `health/` | Vault integrity check per run | `YYYY-MM-DDTHH-MM-SSZ.md` |
| `raw/` | Raw sweep capture (queries + sources + notes) | `YYYY-MM-DDTHH-MM-SSZ.md` |
| `findings/` | Processed primary evidence with citations | `YYYY-MM-DD-<slug>.md` |
| `claims/` | Strategic claims derived from findings | `YYYY-MM-DD-<slug>.md` |
| `dossiers/` | Living documents tracking a topic across sweeps | `<topic>.md` |
| `sources/` | Source registry (surfaces, cadence, activity) | `registry.md` |
| `decisions/` | Decision ledger (stale checks + manual decisions) | `STALE_CHECK-YYYY-MM-DDTHH-MM-SSZ.md` or `DECISION-YYYY-MM-DDTHH-MM-SSZ.md` |
| `runs/` | Run receipts (checklist + evidence yield + handoff summary) | `YYYY-MM-DDTHH-MM-SSZ.md` |

---

## Step Details

### 1. Vault Health Check

**Input:** `vault/health/` directory
**Output:** `vault/health/<run-timestamp>.md`

Check:
- All required directories exist and are writable
- Prior vault state is intact (findings count, claims count from prior run)
- Source registry is present at `vault/sources/registry.md`
- Note what surfaces are registered and their cadence (reddit, x, web, github)
- Assess novelty of this run vs prior runs

**Format template:**
```markdown
# Vault Health Check
**Run:** <run-timestamp>
**Status:** OPERATIONAL — <nth> sweep

## Directory Integrity
| Path | Exists | Writable | Content This Run |
|------|--------|----------|-----------------|
| vault/health/ | YES | YES | health check written |
...

## Novelty Assessment
- **<finding slug>**: <1-line description> — NEW or UPDATE or CONFIRM

## Alerts
- <any issues>

## Health Assessment
**OPERATIONAL** or **DEGRADED** — one line summary
```

---

### 2. Research Sweep

**Input:** Registered source surfaces from `vault/sources/registry.md`
**Output:** `vault/raw/<run-timestamp>.md`

For each active surface:
- **web**: Run 3 targeted queries (~8 results each). Rotate query domains based on open questions in dossier.
- **reddit**: Check registered subreddits for relevant posts
- **x**: Check registered accounts for relevant posts
- **github**: Check weekly cadence — skip if not due

Query strategy:
- One query for the primary threat/risk domain
- One query for the technology/framework domain (e.g., MCP adoption)
- One query for recovery/control plane domain
- Rotate to fill gaps identified in dossier's "Open Questions" section

**Raw capture format:**
```markdown
# RAW SWEEP CAPTURE — <run-timestamp>
**Run:** <n>th sweep | **Profile:** research

## Query Set
1. "<query>" — <N> results
2. "<query>" — <N> results
3. "<query>" — <N> results

## Sources Accessed
- <source domain>: <finding summary> (<publication date>)
- ...

## Raw Signal Notes
- <individual observations, not processed>
- ...

## Novelty Assessment
- <new signal>: NEW or UPDATE to prior
- <known signal from prior>: CONFIRM
```

---

### 3. Process Findings

**Input:** Raw capture
**Output:** `vault/findings/<slug>.md` (one file per distinct finding)

**Trigger:** Only write a finding if there is genuinely new evidence — not just re-statement of prior findings. A finding is new if:
- New quantification (new number from a new source)
- New incident/event documented
- New framework/category identified
- New relationship established between prior findings
- Update to a prior finding's numbers requires a new finding file

**Finding format:**
```markdown
# FINDING — <title>
**Date:** <run-timestamp>
**Sources:** <source URLs> | <publication dates>
**Confidence:** HIGH / MEDIUM / LOW

## Summary
<2-3 sentence summary>

## Evidence
### <Source Name>
- <bullet points>

## Relationship to Prior Vault Findings
- Corroborates **<prior finding ID>**: <1-line connection>
- Updates **<prior finding ID>**: <what changed>

## Routing
- `subc`: <1-line implication>
- `coder`: <1-line implication>
```

---

### 4. File Claims

**Input:** New findings
**Output:** `vault/claims/<slug>.md` (one file per claim)

**Trigger:** File a claim when findings collectively support a strategic statement. A finding can support multiple claims. Claims accumulate across runs.

**Claim format:**
```markdown
# CLAIM — <title>
**Filed:** <run-timestamp>
**Strength:** HIGH / MEDIUM / LOW
**Status:** NEW — CONFIRMED / UPDATED / UNVERIFIED

## Claim
<strategic statement>

## Evidence
- <finding ID>: <1-line evidence summary>

## Implications
<what this means for strategy/product>

## Routing
- `subc`: <implication>
- `coder`: <implication>
```

---

### 5. Update Dossier

**Input:** All vault directories
**Output:** `vault/dossiers/ai-agents.md` (or relevant dossier)

Every run: update the dossier's header (timestamp, sweep count), append new findings to the findings table, update claims table with new claims, note any changes to open questions.

**Dossier update sections:**
```markdown
**Last Updated:** <run-timestamp>
**Stage:** LIVING_DOCUMENT — updated <nth> research sweep

**NEW THIS SWEEP (<nth> — <run-timestamp>):** <bulleted list of new findings/claims>
```

---

### 6. Decision Ledger

**Input:** All active claims
**Output:** `vault/decisions/STALE_CHECK-<run-timestamp>.md`

Check each active claim against open strategic questions. If a claim maps to a previously unanswered question, mark it as a decision trigger candidate.

**Stale check format:**
```markdown
# Decision Ledger — Stale Check
**Run:** <run-timestamp>
**Status:** NO NEW DECISIONS — or: NEW DECISION RECORDED

## Decision Trigger Candidates
| Claim | Strategic Question | Status |
|-------|-------------------|--------|
| <claim ID> | <question> | UNRESOLVED |

## Why No Decisions Triggered
<explanation>

## Recommendation
<action or "no action needed">

## Last Recorded Decision
<timestamp or "none">
```

**Note:** If explicit decision criteria are defined (trigger thresholds), evaluate them here. Otherwise, log as stale check only.

---

### 7. Route to subc (Conditional)

**Input:** New findings + claims
**Output:** `~/.hermes/profiles/subc/room/inbox-from-researchd/<run-timestamp>.md`

**Trigger:** Only route if there is a significant implication for the subc (Dreamer) profile's decisions. A handoff is significant if:
- New convergent evidence changes a strategic position
- A new finding resolves an open question subc was tracking
- Market timing signal has shifted
- A new architectural alignment (e.g., MCP roadmap) bears on product decisions

**Do NOT route** if the run produced only incremental updates to existing evidence.

**Handoff format:**
```markdown
# Research → subc Handoff
**From:** research profile (<n>th sweep)
**To:** subc (Dreamer) inbox
**Run:** <run-timestamp>
**Routing:** PRIORITY / STANDARD

## Headline: <1-sentence summary>

## <Finding 1>
**Source:** <citation>
**Evidence:** <key data points>
**Strategic signal:** <what this means>
**Routing implication:** <for subc>

## <Finding 2>
...

## Cumulative Signal
<how findings connect>

## Files Produced This Run
| File | Evidence Type | Key Data |

## Prior Evidence Still Active
<what remains uncontested>

## For subc's Attention
<explicit question or decision prompt>
```

---

### 8. Run Receipt

**Input:** All steps completed
**Output:** `vault/runs/<run-timestamp>.md`

**Format:**
```markdown
# RUN RECEIPT — research profile
**Run:** <run-timestamp> (<n>th sweep)
**Duration:** <estimate>
**Status:** COMPLETE / PARTIAL / FAILED

## Run Checklist
- [x] <step 1>
- [x] <step 2>
- [ ] <step N if any failed>

## Evidence Yield
| Category | Count | Notes |
|----------|-------|-------|
| New findings | N | <slugs> |
| New claims | N | <slugs> |
| New source citations | N | <source names> |
| Total findings | N | +N from prior |
| Total claims | N | +N from prior |

## Source Surfaces This Run
| Surface | Status | Signals |
|---------|--------|---------|
| web | active | <N> results |
| reddit | not triggered | — |
| github | pending | weekly cadence |

## Decision Ledger Status
<N> consecutive runs, no decisions. <list new candidates>. Research continues evidence-accumulation.

## Handoff Summary
<N> handoffs to subc. <1-line summary of key content>.

## Next Run
Next scheduled: <timestamp>
Pending: <surfaces not triggered>
```

---

## Vault Naming Conventions

- **Run timestamps:** ISO 8601 with T and Z: `YYYY-MM-DDTHH-MM-SSZ`
- **Finding/claim slugs:** Lowercase, hyphenated, date-prefixed: `2026-05-13-mcp-9400-servers-78pct-enterprise.md`
- **Dossier:** Undated slug: `ai-agents.md`
- **Decision entries:** `STALE_CHECK-<timestamp>.md` or `DECISION-<timestamp>.md`

---

## Source Surface Registry

Maintained at `vault/sources/registry.md`. Format:

```markdown
## Registered Sources

### Reddit
- **surface_id**: reddit
- **subreddits**: <list>
- **focus**: <topic>
- **cadence**: per research loop run
- **status**: active / pending / inactive

### X/Twitter
- **surface_id**: x
- **accounts**: <list>
- **focus**: <topic>
- **cadence**: per research loop run
- **status**: active / pending / inactive

### Web Search
- **surface_id**: web
- **focus**: <topic>
- **cadence**: per research loop run
- **status**: active

### GitHub
- **surface_id**: github
- **focus**: <topic>
- **cadence**: weekly
- **status**: pending / active
```

---

## Open Questions Tracking

The dossier maintains an "Open Questions" section. After each sweep:
- Mark questions resolved by new findings
- Add new questions that emerged from findings
- Questions feed query strategy for the next sweep

---

## Support Files

- `references/domain-knowledge-bank.md` — Condensed knowledge bank of all accumulated findings (34 findings, 27 claims across 11 sweeps). Covers: enforcement gap quantification (88%/63%/12%), agent threat landscape (OWASP ASI01–ASI10, 5 real breaches), MCP adoption metrics (9,400+ servers, 78% enterprise), control plane taxonomy convergence (CSA/Forrester/6P/AI Vanguard), IETF AAT standard, recovery layer gap, routing guidance. **Read this first before running the sweep** to understand the current evidence state without re-reading all vault files.

---

## Pitfalls

1. **Don't produce summaries — produce tracked evidence with source citations.** Each finding must cite a specific source with a URL. Raw observations without sources go in the raw capture only.

2. **Only update dossier if there is genuinely new content.** Incremental runs that produce no new findings still update health, raw capture, and decision ledger — but dossier update is only warranted if the evidence base changed.

3. **Route to subc conditionally, not automatically.** The instruction says "route any significant implications." If every run routes automatically, the inbox becomes noise. Apply the significance criteria before routing.

4. **Don't conflate findings and claims.** Findings are primary evidence. Claims are strategic interpretations derived from findings. A finding can exist without a claim; a claim should not exist without a finding.

5. **Check prior run's health before starting.** The prior run's receipt tells you what was produced last, which surfaces were active, and what novelty to expect. Always read the prior health + run receipt first.

6. **Decision ledger should not accumulate stale checks forever.** After 3+ consecutive "no decisions" runs with the same unresolved questions, flag explicitly that the decision criteria need to be defined or the questions need to be closed.

7. **Skill was referenced in job but didn't exist.** If the skill for a job is listed as available but doesn't exist, the cron job will fail gracefully — but the skill should be created immediately so the next scheduled run succeeds.

8. **Duplicate findings — use concrete search patterns, not gut checks.** Before writing any new finding, search vault/findings/ for: (a) the key stat number ("88%", "12%", "53%", "65%"), (b) incident names ("mexico", "clawhavoc", "gtg-1002", "echoleak"), (c) study affiliations ("csa scope violation", "zenity", "token security", "foresiet"). Only write if the signal is genuinely absent. A new quantification of the same phenomenon (e.g., a different CSA study reporting a different percentage) still warrants a new finding file.

9. **Dossier table patch corruption.** After patching the Key Claims or Key Findings table in ai-agents.md, re-read the affected lines. Look for `|||` (should be `||`) — the patch operation can corrupt pipe-prefix alignment across multiple rows simultaneously, especially when patching near a table boundary or when the old_string matches multiple rows. Fix immediately after patching, before finishing the run. If corruption spreads across many rows, use a targeted patch with a unique surrounding context string (e.g., the row's unique claim ID slug) rather than a generic pipe pattern. Do NOT use a generic `|||` → `||` replacement as the only fix — it may corrupt rows you didn't intend to touch.

10. **`rg` (ripgrep) may not be available.** The skill uses `rg` for vault searches but it is not always installed. Always fall back to `grep -rl` or `grep -rn` if `rg` is absent. Do not assume ripgrep is present in the execution environment.

11. **Domain knowledge bank reference file.** The skill references `references/domain-knowledge-bank.md` as a pre-read to avoid re-reading all vault files. This file must be created manually and kept updated with the condensed evidence state. It is not auto-generated. If it does not exist at `~/.hermes/skills/research-agent-loop/references/domain-knowledge-bank.md`, create it from the current vault state before the next scheduled run.

12. **GitHub surface cadence is a tracking gap, not a failure.** "Pending — weekly cadence not confirmed triggered" is expected behavior. Continue without treating it as an error. If GitHub signals become critical, add explicit GitHub web search queries to the sweep rather than relying on surface-level access.

---

## Verification Steps

After completing the run:
- [ ] `vault/health/<timestamp>.md` written
- [ ] `vault/raw/<timestamp>.md` written
- [ ] `vault/findings/` has new files (if novel evidence found)
- [ ] `vault/claims/` has new files (if new strategic claims)
- [ ] `vault/dossiers/ai-agents.md` header updated
- [ ] `vault/decisions/STALE_CHECK-<timestamp>.md` written
- [ ] `vault/runs/<timestamp>.md` written
- [ ] Subc inbox updated (if significant findings)
- [ ] No broken links in finding files (sources are accessible)
