---
name: agentic-research-loop
title: Agentic Research Loop
description: Run an autonomous research agent loop for a named profile. Execute periodic sweeps of registered source surfaces, process findings, maintain vault evidence chains, route implications to downstream profiles, and log receipts. Used when the user asks to "run research", "run the research loop", "execute a research sweep", or similar for a cron or scheduled job.
version: 1.0.0
author: Hermes Research Stack
license: MIT
dependencies: []
platforms: [linux, macos]
metadata:
  hermes:
    tags: [research, autonomous, agent, vault, evidence-chain, cron, monitoring]
    category: research
    requires_toolsets: [terminal, files, web_search, web_extract, browser]

---

# Agentic Research Loop

End-to-end loop for running an autonomous research agent on a named profile. This skill executes a single research sweep — not a continuous stream, but one discrete run that produces tracked evidence, updates the vault, and routes relevant findings to downstream inboxes.

This skill is loaded when running research as a scheduled cron job or when manually triggering a research sweep for a profile.

## Prerequisites

- Profile must exist at `~/.hermes/profiles/<profile_name>/`
- Profile must have a `vault/` directory with subdirectories already initialized
- Required vault subdirectories: `health/`, `sources/`, `raw/`, `findings/`, `claims/`, `dossiers/`, `decisions/`, `runs/`
- Source registry must exist at `vault/sources/registry.md`

## Step-by-Step Execution

### Step 0 — Pre-flight: Verify Vault Health

Before any sweep, confirm the vault is operational:

```bash
# Check vault health directory exists and last health check
ls -la ~/.hermes/profiles/<profile>/vault/health/
cat ~/.hermes/profiles/<profile>/vault/health/<latest>.md

# Verify all required subdirectories exist
ls ~/.hermes/profiles/<profile>/vault/
```

If health check is stale (>12h), note it but proceed — the sweep itself will refresh it.

### Step 1 — Read Prior State (CRITICAL — do this before sweeping)

Read these files BEFORE executing any surface queries:
- `vault/runs/<last_run>.md` — what was done last run (avoids duplicating work)
- `vault/sources/registry.md` — registered surfaces and their cadence
- `vault/decisions/STALE_CHECK-<latest>.md` — decision ledger status
- `vault/dossiers/<latest_dossier>.md` — current dossier state (living document)
- `vault/findings/` and `vault/claims/` — review recent files to identify novelty

**Why this matters:** Reading prior state before sweeping lets you detect novelty efficiently. In this session, reading the last run receipt revealed that MCP was at 97M downloads, 3 new claims were pending, and the enforcement gap was untracked — directly shaping the 3 queries run this sweep. Sweeping blind means re-processing known signals.

### Step 2 — Execute Research Sweep

### Step 2 — Execute Research Sweep

Sweep each registered surface according to its cadence. Use targeted queries, not generic ones.

**Web Search:**
- Run 3–5 targeted queries focused on filling specific knowledge gaps from the dossier's "Open Questions" section
- Use `web_search` tool with `limit=5` per query
- Extract top results with `web_extract` for detailed content

**Reddit:**
- `web_extract` does NOT reliably render Reddit pages — do not rely on it for Reddit content
- Instead, use `web_search` with `site:reddit.com` queries to capture Reddit-hosted signals
- Reddit post titles and descriptions surface through search results even when direct extraction fails
- `browser_navigate` + `browser_snapshot` works as a fallback for direct post URLs but is slower
- Prior run receipts often capture Reddit signals via web extraction of Reddit-hosted content (this is acceptable when search snippet coverage is sufficient)

**X/Twitter:**
- Check if triggered this run (some loops use per-run cadence, others daily)
- Use `xurl` CLI or browser navigation for specific accounts

**GitHub:**
- Typically weekly cadence — check last sweep date before triggering

### Step 3 — Process Findings

For each new signal captured:

1. **New finding** → write to `vault/findings/<date>-<slug>.md`
   - Include: source URL, confidence level, key claim, connection to prior findings
   - Format as evidence, not summary

2. **Confirmed claim** → write to `vault/claims/<date>-<slug>.md`
   - Only write if the claim is new or materially strengthened
   - Include evidence chain citations

3. **Dossier update** → update the living document in `vault/dossiers/`
   - Add new finding IDs to the table
   - Update claim statuses
   - Update "Open Questions" based on what was answered this sweep

### Step 4 — Route to Downstream Inboxes

Check `vault/dossiers/<dossier>.md` "Routing Relevance" section.
Route to `~/.hermes/profiles/<target_profile>/room/inbox-from-researchd/<timestamp>.md`

**Routing criteria — when to route to a profile:**
- Route when findings have **architectural implications** for the recipient's work, not just when they're "interesting"
- Route when a finding **directly answers an open question** the recipient's dossier has
- Route when a finding **changes a prior claim status** (e.g., weak → confirmed → established)
- Route when findings **converge** on the same architecture from independent sources (stronger signal than any single source)
- Do NOT route generic summaries or weakly evidenced signals

**Inbox format:**
- Header: routing signal name, urgency level
- Body: what was found, why it matters to this recipient, specific questions if any
- Footer: evidence chain (paths to findings/claims in vault)

**Do not combine multiple unrelated signals in one inbox** — one finding cluster per inbox. If two findings are independent, write two inbox files.

### Step 5 — Decision Ledger Check

Check `vault/decisions/STALE_CHECK-<timestamp>.md`:
- If no new decisions triggered → write a stale check entry (confirms the ledger is being monitored)
- If a decision trigger threshold was crossed → write a full decision record with rationale

### Step 6 — Write Run Receipt

Write `vault/runs/<timestamp>.md`:
- Surfaces swept and their status
- New findings (table with file, topic, confidence)
- New claims (table with claim, status)
- Vault metrics after run
- Handoff summary
- Decision ledger status

### Step 7 — Write Health Check

Write `vault/health/<timestamp>.md`:
- Directory integrity table
- Source surface status
- Vault contents summary
- Alerts if any
- Health assessment: OPERATIONAL / DEGRADED / FAIL

## Vault Directory Structure

```
vault/
  health/       — one health check file per run
  sources/      — registry.md + per-source subdirs
  raw/          — raw sweep captures (one file per run)
  findings/      — one finding per file, date-slug naming
  claims/        — one claim per file, date-slug naming
  dossiers/     — living documents, fully rewritten each sweep
  decisions/    — stale checks + explicit decision records
  runs/         — run receipts
```

## Source Registry Format

`vault/sources/registry.md` should contain:
```markdown
## Registered Sources

### <surface_id>
- **surface_id**: <id>
- **focus**: <what this surface covers>
- **cadence**: per run / daily / weekly
- **status**: active / pending / inactive
```

## Finding Template

```markdown
# Finding: <Topic>
**Date:** <YYYY-MM-DD>
**Confidence:** HIGH / MEDIUM / LOW
**Source:** <URL or surface>

## Evidence
<what was found>

## Key Claim
<the specific claim this finding supports or contradicts>

## Connection to Prior Findings
<link to related findings>

## Citation
<full URL>
```

## Claim Template

```markdown
# Claim: <Claim Statement>
**Date:** <YYYY-MM-DD>
**Status:** NEW / CONFIRMED / STRENGTHENED / REVISED
**Confidence:** HIGH / MEDIUM / LOW

## Claim Statement
<precise claim>

## Evidence
<evidence chain>

## Status
<explanation of status change>

## Routing
<which profile this claim is relevant to and why>
```

## Pitfalls

- **Do not produce summaries** — produce tracked evidence with source citations. The vault is an evidence chain, not a report.
- **Sweep before reading prior state = blind duplication** — always read the last run receipt and recent findings/claims BEFORE running new surface queries. This is the primary mechanism for novelty detection. Skipping it means re-processing known signals and missing what is actually new.
- **Reddit via web_extract fails for listings, works for direct posts** — `web_extract` does not render subreddit listing pages; use `web_search` with `site:reddit.com` queries instead. Direct post URLs (`reddit.com/r/subreddit/comments/postid`) may work with `web_extract` — test first, fall back to browser if content is garbled.
- **Empty decision ledger is normal** — the ledger tracks explicit decisions, not evidence. If no decision trigger threshold was crossed, write a stale check, not a decision. The research profile's primary routing is to subc's inbox — the decision ledger is for manually recorded strategic decisions by other profiles.
- **Don't skip the dossier update** — the dossier is the living synthesis. If you update findings/claims but not the dossier, the evidence chain is incomplete.
- **Route before writing health check** — inbox routing is the delivery step; write it before the health check that confirms the run completed.
- **GitHub cadence is weekly** — don't trigger GitHub on per-run cadences; check last sweep timestamp first.

## Support Files

- `references/vault-structure.md` — detailed vault schema and directory conventions
- `references/source-surfaces.md` — how to query each surface type (web, reddit, github, x)
