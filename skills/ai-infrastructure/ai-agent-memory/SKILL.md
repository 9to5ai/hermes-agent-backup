---
name: ai-agent-memory
version: 0.1.0
description: |
  GBrain personal knowledge brain for AI agents — the memory layer that sits between
  you and your AI agents. Combines hybrid search (vector + keyword + RRF), graph
  relationships, hot memory with decay halflife, a Dream Cycle for autonomous synthesis,
  a Takes system for calibrated predictions, and 34+ composable skills. Install,
  configure, and extract maximal leverage from gbrain beyond your current workflows.
triggers:
  - "set up gbrain"
  - "install gbrain"
  - "gbrain setup"
  - "brain memory for AI"
  - "personal AI memory"
  - "how does gbrain work"
  - "gbrain features"
  - "use gbrain"
  - "gbrain book-mirror"
  - "gbrain dream cycle"
  - "gbrain takes"
  - "what can gbrain do"
mutating: true
writes_pages: true
writes_to:
  - people/
  - companies/
  - concepts/
  - originals/
  - ideas/
---

# AI Agent Memory — GBrain System

GBrain is a personal knowledge brain (~14k stars, TypeScript, MIT) that gives AI
agents persistent memory. Every conversation, file, and idea flows through an
11-phase maintenance cycle. The system builds on itself — after months of running,
the agent knows your style, history, relationships, and intellectual map.

## Core Architecture

### Two Orthogonal Axes

- **Brain** = WHICH DATABASE (PGLite embedded, Postgres, or Supabase hosted)
- **Source** = WHICH REPO inside the database (wiki, gstack, openclaw, essays, etc.)
- Routing: `--brain <id>` / `--source <id>` or dotfiles (`.gbrain-mount`, `.gbrain-source`)

### The 11-Phase Dream Cycle

Runs periodically (cron or autopilot daemon). Phases:

```
lint → backlinks → sync → synthesize → extract → patterns →
recompute_emotional_weight → consolidate → embed → orphans → purge
```

Key phases:
- **synthesize**: reads conversation history, creates/updates brain pages
- **extract**: pulls facts into Hot Memory with decay halflife
- **consolidate** (v0.31+): converts 3+ fact clusters into persistent Takes
- **patterns**: surfaces cross-session themes
- **drift**: surfaces soft-band takes (weight 0.3–0.85) for review

Run manually: `gbrain dream --json`
Run daemonized: `gbrain autopilot --install`

### Hot Memory / Facts System

Short-term memory extracted from conversations. Decay halflives:

| Kind | Halflife |
|------|----------|
| event | 7 days |
| commitment | 90 days |
| preference | 90 days |
| belief | 365 days |
| fact | 365 days |

Commands: `gbrain recall <entity>` | `gbrain forget <fact-id>`
Kill switch: `gbrain config set facts.extraction_enabled false`

### Takes System — Calibrated Predictions

Typed, weighted, attributed claims stored in `takes` table. The system tracks
Brier scores and calibration curves — a real prediction market for your thinking.

```bash
# Add a bet
gbrain takes add concepts/founder-mode --claim "founder-mode teams ship 2x faster" \
  --kind bet --who jun --weight 0.65 --source "observation"

# Resolve it
gbrain takes resolve concepts/founder-mode --row 3 --quality correct \
  --evidence "measured: 1.9x over 6 months"

# Check calibration
gbrain takes scorecard jun
gbrain takes calibration jun
```

Brier score: lower is better (0.25 = always guessing 50%). Calibration curve
bins resolved bets by stated probability vs observed hit rate.

## Skills System

Skills are fat markdown files (34+) that define how the agent behaves. They chain:

- `signal-detector` → fires on every message, captures ideas + entities
- `book-mirror` → personalized chapter-by-chapter book analysis (two-column: content | your life)
- `concept-synthesis` → dedup + tier raw concept stubs → T1 Canon to T4 Riff intellectual map
- `archive-crawler` → mine old files (Dropbox, B2, mbox, PST) with gold filter
- `strategic-reading` → apply book/text to ONE specific problem → playbook
- `perplexity-research` → brain-augmented web research (sends context, surfaces delta)
- `academic-verify` → trace claims through publication → methodology → raw data → replication
- `enrich` → tiered entity enrichment (person/company pages with compiled truth)
- `cross-modal-review` → quality gate via second model; refusal routing chain
- `soul-audit` → 6-phase identity interview → SOUL.md, USER.md, ACCESS_POLICY.md, HEARTBEAT.md
- `brain-pdf` → render brain page to publication-quality PDF via gstack make-pdf
- `minion-orchestrator` → parallel subagent jobs (shell + LLM), fan-out manifests
- `data-research` → structured email-to-tracker pipelines via YAML recipes
- `voice-note-ingest` → audio → brain pages with exact-phrasing capture

Resolver at `skills/RESOLVER.md` handles automatic routing. Always read the skill
file before acting.

## Key Commands

```bash
# Install
git clone https://github.com/garrytan/gbrain ~/gbrain && cd ~/gbrain && bun install
gbrain init                              # PGLite default (zero-config)
gbrain doctor                            # verify installation

# Dream cycle
gbrain dream --json                      # one-shot maintenance cycle
gbrain autopilot --install              # daemonized maintenance

# Memory / facts
gbrain salience --days 14               # what's emotionally alive (no LLM)
gbrain anomalies --days 30              # statistical oddities
gbrain recall <entity>                  # query facts about entity
gbrain takes <slug>                     # list takes for a page

# Search (hybrid: vector + keyword + RRF fusion, 97.6% R@5)
gbrain query "what do we know about X"  # hybrid search
gbrain search "exact phrase"            # keyword only

# Skills
gbrain book-mirror --chapters-dir ...  # personalized book analysis
gbrain agent run "research task"       # spawn subagent
gbrain agent run --fanout-manifest ... # parallel fan-out

# Thin-client (remote brain over MCP)
gbrain init --mcp-only                  # connect to remote brain
gbrain serve --http --port 3131         # serve with OAuth 2.1
ngrok http 3131 --url your-brain.ngrok.app

# Integrations
gbrain features --json                 # what features are configured
gbrain config get <key>                 # read config value
gbrain config set <key> <value>         # write config value
```

## Thin-Client MCP Server

`gbrain serve --http` serves OAuth 2.1 + MCP over HTTP. Works with:
- **ChatGPT** (OAuth 2.1 + PKCE — native)
- **Claude Desktop** (OAuth or bearer)
- **Perplexity** (client credentials)
- Any MCP client

Refuses over HTTP: `sync_brain`, `file_upload`, `file_list`, `file_url` (localOnly ops).

## Storage Tiering

In `gbrain.yml`:
```yaml
storage:
  db_tracked: ["media/"]    # indexed in brain DB
  db_only: ["sessions/"]    # NOT in git (private)
```

`gbrain sync` auto-manages `.gitignore` for db_only paths.

## Source-Aware Ranking

Hybrid search applies boost/dampening by slug prefix:
- `originals/` ×1.5, `concepts/` ×1.3, `writing/` ×1.4
- `people/`, `companies/`, `deals/` ×1.2
- `daily/` ×0.8, `wintermute/chat/` ×0.5
- Hard exclude: `test/`, `archive/`, `attachments/`, `.raw/`

## Cross-Modal Eval

Three frontier models score outputs on 5 dimensions. Verdict pass/fail/inconclusive.
```bash
gbrain eval cross-modal --budget-usd 5
```

Receipts at `~/.gbrain/eval-receipts/<slug>-<sha8>.json`.

## Unlock Sequence for Maximal Leverage

**Week 1**: Install → run `gbrain doctor` → drop a book through `book-mirror` end-to-end → run `soul-audit` (one phase per day)

**Week 2**: Connect Gmail recipe → run `gbrain salience` → run `concept-synthesis` on existing stubs

**Month 1**: Run `archive-crawler` on one old archive → start using `takes` for real decisions → configure `gbrain autopilot` → run `cross-modal-review` on something important

**Month 2+**: Intellect map building, drift surfacing, calibrated track record forming

## Recipes (Pre-built Integration Pipelines)

- `calendar-to-brain.md` — Google Calendar → daily brain pages, attendee enrichment
- `email-to-brain.md` — Gmail → digest → entity enrichment → brain pages
- `meeting-sync.md`, `twilio-voice-brain.md`, `x-to-brain.md`

## Key Files

- `src/core/operations.ts` — contract-first op definitions (~47 operations)
- `src/core/cycle.ts` — Dream Cycle primitive
- `src/core/engine.ts` — pluggable engine interface (PGLite + Postgres)
- `src/core/search/` — hybrid search (vector + keyword + RRF)
- `skills/RESOLVER.md` — skill dispatcher + routing table
- `docs/architecture/brains-and-sources.md` — two-axis mental model
- `llms.txt` / `llms-full.txt` — full documentation bundle

## Reference

See `references/commands.md` for detailed command reference.
See `references/dream-cycle.md` for phase-by-phase breakdown.
See `references/book-mirror-workflow.md` for the book-mirror pipeline.