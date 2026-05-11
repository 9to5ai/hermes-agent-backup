# GBrain Commands Reference

## Core Commands

### `gbrain init [--mcp-only]`
Initialize brain. Defaults to PGLite (embedded, zero-config). `--mcp-only` connects to a remote brain over OAuth-protected MCP.

### `gbrain doctor [--fix]`
Verify installation. With `--fix`, auto-fix what it can.

### `gbrain sync [--repo <path>] [--no-pull] [--no-embed]`
Sync brain repo to DB. Detects changes via git diff, imports only changed files. For small changesets (<=100 files), embeddings generated inline. Use `--watch` for foreground polling loop.

### `gbrain embed [--stale]`
Backfill embeddings for chunks without them. Run after sync if sync used `--no-embed`.

### `gbrain query "<natural question>" [--brain <id>] [--source <id>]`
Hybrid search (vector + keyword + RRF). 97.6% R@5 on LongMemEval.

### `gbrain search "<exact phrase>"` [--limit N]
Keyword-only search (pg_trgm trigram matching).

---

## Dream Cycle

### `gbrain dream [--json] [--dry-run] [--phase <phase>] [--pull] [--dir <path>]`
Run one maintenance cycle. `--phase` to run single phase. `--json` for machine-readable output.

### `gbrain autopilot --install --repo <path>`
Install daemonized maintenance. Runs `gbrain dream` on a schedule.

### `gbrain dream --input <transcript-file>`
Run synthesize phase on a specific transcript file.

---

## Memory / Facts

### `gbrain recall <entity>`
Show facts extracted about an entity.

### `gbrain forget <fact-id>`
Remove a specific fact from hot memory.

### `gbrain config set facts.extraction_enabled false`
Kill switch to disable fact extraction.

---

## Salience / Anomalies

### `gbrain salience [--days N] [--limit N] [--kind prefix] [--json]`
Pages recently touched, ranked by emotional + activity salience. Zero LLM calls. Deterministic.

### `gbrain anomalies [--days N]`
Statistical oddities — pages with unusual activity patterns vs historical norms.

---

## Takes System

### `gbrain takes <slug> [--json] [--who <holder>] [--kind <kind>] [--expired]`
List takes for a page.

### `gbrain takes search "<query>" [--limit N] [--json]`
Keyword search across all takes.

### `gbrain takes add <slug> --claim "..." --kind <fact|take|bet|hunch> --who <holder> [--weight 0.5] [--source "..."]`
Append a take (markdown fence + DB).

### `gbrain takes update <slug> --row N [--weight 0.7] [--source "..."]`
Update mutable fields on a take.

### `gbrain takes supersede <slug> --row N --claim "..." [--kind k] [--who h] [--weight 0.5]`
Strikethrough old take, append new one.

### `gbrain takes resolve <slug> --row N --quality correct|incorrect|partial [--evidence "..."] [--value N --unit usd|pct|count] [--by <slug>]`
Record bet resolution. `--outcome true|false` is deprecated alias.

### `gbrain takes scorecard [<holder>] [--domain <prefix>] [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--json]`
Aggregate calibration scorecard. Brier score (lower=better, 0.25=always-50% baseline).

### `gbrain takes calibration [<holder>] [--bucket-size 0.1] [--json]`
Calibration curve: observed vs predicted frequency per probability bucket.

---

## Skills

### `gbrain book-mirror --chapters-dir <dir> --context-file <file> --slug <slug> --title "<title>" --author "<author>" [--model claude-opus-4-7]`
Personalized chapter-by-chapter book analysis. Fans out N read-only subagents, assembles two-column output.

### `gbrain agent run "<prompt>" [--tools query,search,get_page] [--model <id>] [--timeout-ms N]`
Spawn LLM subagent job. `--fanout-manifest <file>` for parallel work.

### `gbrain agent run --fanout-manifest <file>`
N children + 1 aggregator. Children are read-only subagents. Aggregator runs after all children terminate.

---

## Brain / Source Management

### `gbrain mounts add <id> <url>`
Mount an additional brain (team-published, separate DB).

### `gbrain sources add <name> [--local-path <path>]`
Add a new source repo inside the current brain.

### `gbrain features [--json]`
Show configured features and brain health.

---

## Integrations

### `gbrain jobs submit shell --params '{"cmd":"...","cwd":"/path"}'`
Submit deterministic shell job (requires `GBRAIN_ALLOW_SHELL_JOBS=1`).

### `gbrain jobs submit shell --params '...' --follow`
Inline execution on PGLite or one-shot deployments.

### `gbrain jobs stats`
Worker/queue health dashboard.

### `gbrain auth register-client <name> --grant-types client_credentials --scopes "read write"`
Register OAuth client for remote MCP access.

---

## MCP Server

### `gbrain serve`
Start stdio MCP server (local agents, zero config).

### `gbrain serve --http --port 3131 [--public-url https://...]`
Start HTTP MCP server with OAuth 2.1. `--public-url` required when behind a tunnel.

### `gbrain auth create <name>`
Create legacy bearer token (Postgres only).

---

## Storage

### `gbrain storage status [--repo <path>] [--json]`
Show tier breakdown (db_tracked vs db_only).

### `gbrain export --restore-only [--repo <path>] [--type <type>] [--slug-prefix <prefix>]`
Restore missing db_only files from the database.

---

## Eval

### `gbrain eval --qrels <file> --run <run-file> [--metrics p@5,r@5,mrr,ndcg@5]`
Run retrieval eval against qrels.

### `gbrain eval cross-modal [--budget-usd N]`
Three frontier models score outputs on 5 dimensions. Verdict pass/fail/inconclusive.

### `gbrain eval export --since 7d > base.ndjson`
Export captured queries for replay benchmarking.

### `gbrain eval replay --against base.ndjson`
Replay queries against modified retrieval.

### `gbrain eval longmemeval <dataset.jsonl>`
Run against isolated in-memory PGLite per question. `~/.gbrain` never opened.

---

## Config

### `gbrain config get <key>`
Read config value.

### `gbrain config set <key> <value>`
Write config value.

### `gbrain config get sync.repo_path`
Get brain repo path.

---

## Import / Export

### `gbrain import <path> [--no-embed]`
Import markdown files from path into brain.

### `gbrain lint [--fix]`
Lint brain pages (frontmatter, broken links, etc.).

### `gbrain backlinks [--fix]`
Populate link graph from markdown.

### `gbrain extract timeline --source db`
Extract timeline entries from existing brain pages into the graph.

### `gbrain extract takes --slugs <slug>`
Reconcile takes markdown fence with DB state.

---

## Migration

### `gbrain apply-migrations [--yes]`
Run pending schema migrations.

### `gbrain migrate-engine --to supabase|pglite`
Bidirectional engine migration.

### `gbrain upgrade`
Upgrade brain to new version. Runs `gbrain post-upgrade` which runs `gbrain apply-migrations`.

---

## Utilities

### `gbrain pages [--source <id>] [--limit N] [--json]`
List brain pages.

### `gbrain graph-query [--brain <id>] [--source <id>] [--depth N] <slug>`
Graph traversal from a slug.

### `gbrain report [--period day|week|month] [--format markdown|json]`
Generate activity report.

### `gbrain check-update [--install]`
Check for updates. With `--install`, apply upgrade.

### `gbrain integrity [--fix]`
Check brain integrity, fix issues.

### `gbrain repair-jsonb [--dry-run]`
Repair malformed JSONB in pages table.