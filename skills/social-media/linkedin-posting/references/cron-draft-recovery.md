# Cron Draft Recovery — Finding Jun's LinkedIn Post Drafts

## Context

Jun has a daily 2:30am cron job (`3230060441fd`) that generates 3 LinkedIn post drafts from recent arXiv papers, humanizes them, and writes output to a Markdown file. When Jun says "post draft 3" in a new session, the draft text is NOT in the conversation — it must be recovered from the cron output.

## File Location

Cron output directory:
```
~/.hermes/cron/output/{job_id}/
```

The active job ID for Jun's morning research briefing is **`3230060441fd`**.

Each run produces a file like `2026-05-10_02-36-37.md`.

## Recovery Technique

### Step 1 — Identify the right file
Use `ls -lt` to get the latest run:
```bash
ls -lt ~/.hermes/cron/output/3230060441fd/
```

### Step 2 — Find the draft inside
The file is large (~45-50KB). Drafts appear near the END of the file (offset ~900+ lines).

Use `read_file` with large offset:
```
read_file(offset=900, limit=100)
```

Or search with `search_files` for patterns like:
- `[DRAFT 3/3 — LinkedIn Post]`
- `Draft 3`
- Key topic words (e.g., "cyber attack", "frontier AI", "identity verification")

### Step 3 — Extract the text
Drafts are formatted as:
```
[DRAFT 3/3 — LinkedIn Post]

<Post body text>

Source: <Paper Title> — https://arxiv.org/abs/XXXXX
---
```

The Note at EOF of some files warns that the draft may contain mixed English/Chinese text that was auto-corrected in a later rewrite — use the latest file.

## Session Log Reference

**Session:** 2026-05-10 08:54 AM (this session)
**Task:** "post draft 3" — recovered Draft 3 "Frontier AI labs deploying internal models for AI R&D" from `2026-05-10_02-36-37.md` (the latest run), posted to LinkedIn, confirmed `Post successful.`

**Post URL:** `https://www.linkedin.com/feed/update/urn:li:share:7459012785499312128/`

## Relevant Cron Output File Structure

```
~/.hermes/cron/output/3230060441fd/
├── 2026-05-02_23-50-43.md   # test run
├── 2026-05-03_02-36-59.md   # first full run
├── ...
├── 2026-05-09_02-41-29.md
└── 2026-05-10_02-36-37.md   # latest — used for Draft 3 today
```

The May 10 run contained drafts:
- Draft 1: Hadas Orgad / weight pruning / harmfulness mechanism
- Draft 2: Abhinav Agarwal / Refute-or-Promote / false-positive bug reports
- Draft 3: Centre for Governance of AI / frontier AI developer disclosure framework ← **posted**