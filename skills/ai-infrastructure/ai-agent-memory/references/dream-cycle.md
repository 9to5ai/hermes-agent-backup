# Dream Cycle — Phase-by-Phase Breakdown

## Phase Order (semantically driven: fix files first, then index)

```
1. lint         — filesystem writes, no DB
2. backlinks    — filesystem writes, no DB
3. sync         — DB picks up phases 1+2
4. synthesize   — transcripts → brain pages (v0.23)
5. extract      — DB picks up links from sync + synthesize
6. patterns     — cross-session themes (MUST be after extract)
7. recompute_emotional_weight — DB writes (v0.29)
8. consolidate — facts → Takes (v0.31, after patterns, before embed)
9. embed        — DB writes
10. orphans     — DB read, report only
11. purge       — hard-delete soft-deleted pages + expired sources (v0.26.5)
```

## Lock Coordination

- Postgres: row in `gbrain_cycle_locks` with 30-min TTL. Refreshed between phases.
- PGLite: file lock at `~/.gbrain/cycle.lock` with PID + mtime. Same 30-min TTL.
- Lock-skip: `orphans` is read-only and skips the lock. All other phases need it.
- Crashed holders auto-release when TTL expires — no manual cleanup needed.

## Phase Details

### Phase 1: lint
Fixes frontmatter issues, validates slug format, checks YAML frontmatter validity.
```bash
gbrain lint --fix
```
Filesystem-only. No DB involvement.

### Phase 2: backlinks
Parses markdown for `[[wikilinks]` and `[Name](path)` references. Reconciles
link graph. Writes to `links` table via sync.
```bash
gbrain backlinks --fix
```
Filesystem-only. No DB involvement.

### Phase 3: sync
Imports changed files from brain repo into DB. Detects changes via git diff.
Small changesets (<=100 files): embeddings generated inline.
Large syncs: use `--no-embed` and follow with `gbrain embed --stale`.
```bash
gbrain sync --repo /path/to/brain
gbrain sync --watch --repo /path/to/brain  # foreground polling, 60s interval
```
Writes to DB. Acquires cycle lock.

### Phase 4: synthesize (v0.23)
Reads transcript files (conversation logs, meeting recordings). Extracts ideas
and entities, creates/updates brain pages. Fan-out to subagents for parallel
transcript processing.
```bash
gbrain dream --phase synthesize
gbrain dream --input /path/to/transcript.txt  # ad-hoc single file
gbrain dream --from 2026-01-01 --to 2026-03-31  # date range
```
Writes to DB. Acquires cycle lock.

**Self-consumption guard**: synthesize reads its own output pages. The guard
prevents infinite loops. Bypass with `--unsafe-bypass-dream-guard` (never
auto-applied for `--input`).

### Phase 5: extract
Processes fresh graph state (links from sync + synthesize) and extracts facts
into Hot Memory. Cosine dedup: ≥0.95 skip LLM, ≥0.92 fallback, else INSERT.
Bounded queue (cap 100, drop-oldest on overflow).
```bash
gbrain dream --phase extract
```
Writes to DB. Acquires cycle lock.

### Phase 6: patterns (v0.23)
Cross-session theme detection. Scans recent pages for recurring topics.
Must run AFTER extract so graph state is fresh.
```bash
gbrain dream --phase patterns
```
Writes to DB. Acquires cycle lock.

### Phase 7: recompute_emotional_weight (v0.29)
Recomputes `emotional_weight` column on all pages using the formula from
`recompute_emotional_weight` phase output. Batched for performance.
```bash
gbrain dream --phase recompute_emotional_weight
```
Writes to DB. Acquires cycle lock.

### Phase 8: consolidate (v0.31)
Cluster unconsolidated facts per (source_id, entity_slug). Sonnet-synthesize
one take per cluster. INSERT into takes(kind='fact'). Mark facts
`consolidated_at` + `consolidated_into`. Never DELETE facts — they remain
as audit trail. Placed AFTER patterns (graph-fresh) and BEFORE embed (so new
takes get embedded same cycle).
```bash
gbrain dream --phase consolidate
```
Writes to DB. Acquires cycle lock.

### Phase 9: embed
Generate vector embeddings for chunks without them. Safety net for large syncs
or prior `--no-embed` runs.
```bash
gbrain embed --stale
```
Writes to DB. Acquires cycle lock.

### Phase 10: orphans
Read-only report of pages referenced but never indexed (or deleted but still
linked). Does NOT delete — only reports.
```bash
gbrain orphans
```
No lock acquired (read-only).

### Phase 11: purge (v0.26.5)
Hard-deletes soft-deleted pages and expired archived sources past the 72h
recovery window. Runs last so the rest of the cycle sees the recoverable set.
```bash
gbrain dream --phase purge
```
Writes to DB. Acquires cycle lock.

## Running the Cycle

### One-shot (cron)
```bash
# Daily at 2 AM
0 2 * * * gbrain dream --json >> /var/log/gbrain-dream.log
```

### Daemonized (autopilot)
```bash
gbrain autopilot --install --repo /path/to/brain
```

### Dry-run (preview, no writes)
```bash
gbrain dream --dry-run
```

### Single phase
```bash
gbrain dream --phase lint
```

### With git pull
```bash
gbrain dream --pull
```

## Output Format

`--json` returns CycleReport:
```json
{
  "schema_version": "1",
  "timestamp": "2026-05-10T12:00:00Z",
  "status": "ok",
  "phases": [
    {
      "phase": "sync",
      "status": "ok",
      "duration_ms": 2341,
      "summary": "47 pages synced",
      "details": { "pages_synced": 47 }
    }
  ],
  "totals": {
    "pages_synced": 47,
    "pages_extracted": 12,
    "pages_embedded": 3
  }
}
```

Status values:
- `clean`: ran successfully, zero work done
- `ok`: ran successfully, work was done
- `partial`: at least one phase warned or failed
- `skipped`: cycle did not run (lock held)
- `failed`: lock acquired but all phases failed

## CycleReport totals fields

| Field | Description |
|-------|-------------|
| lint_fixes | Filesystem fixes applied |
| backlinks_added | Links added to graph |
| pages_synced | Pages imported to DB |
| pages_extracted | Facts extracted |
| pages_embedded | Embeddings generated |
| orphans_found | Orphan pages detected |
| transcripts_processed | Transcripts synthesized |
| synth_pages_written | Pages created by synthesize |
| patterns_written | Pattern pages written |
| pages_emotional_weight_recomputed | Pages reweighted |
| facts_consolidated | Facts promoted to Takes |
| consolidate_takes_written | New Takes created |
| purged_sources_count | Sources hard-deleted |
| purged_pages_count | Pages hard-deleted |