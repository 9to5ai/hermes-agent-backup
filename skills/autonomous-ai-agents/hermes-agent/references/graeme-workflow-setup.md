# Graeme Workflow — Current Setup State (May 2026)

## Source Posts
- Main guide: https://x.com/gkisokay/status/2053449921554960545
- Dreamer/Subconscious: https://x.com/gkisokay/status/2040044476060864598
- Research agent: https://x.com/gkisokay/status/2051275483996909982

## What's Implemented

### Profiles (5 created)

| Profile | Path | SOUL.md | Directories |
|---------|------|---------|-------------|
| `research` | `~/.hermes/profiles/research/` | ✓ | `vault/{raw,claims,findings,sources,dossiers,decisions,runs,health}` |
| `subc` | `~/.hermes/profiles/subc/` | ✓ | `room/{walks,projects,notes,feedback,inbox-from-researchd,signal-log,signal-state}` + `fascinations.md`, `lessons.md` |
| `main` | `~/.hermes/profiles/main/` | ✓ | `control-room/`, `approval-ledger/`, `projects/` |
| `coder` | `~/.hermes/profiles/coder/` | ✓ | (uses default workspace) |
| `qa` | `~/.hermes/profiles/qa/` | ✓ | (uses default workspace) |

### Cron Jobs (3 active)

| Job ID | Name | Schedule | Next Run |
|--------|------|----------|----------|
| `3aec8f4d9290` | Research Loop - 6hr refresh | `0 */6 * * *` | 2026-05-11 12:00 +10:00 |
| `e64ad6e9e46b` | Dreamer Morning Walk | `0 8 * * *` | 2026-05-12 08:00 +10:00 |
| `1387efc92c72` | Dreamer Evening Tending | `0 20 * * *` | 2026-05-11 20:00 +10:00 |

### Dashboard

- Hermes dashboard built from source (`cd ~/.hermes/hermes-agent/web && npm run build`)
- Running at `http://127.0.0.1:9119` (background process `proc_2a7c29b5a1dd`)
- All 6 profiles visible at `/profiles`
- Gateway status: Running, 1 active session

### Hermes Version
- v0.12.0 (2026.4.30)
- Located at `~/.hermes/hermes-agent/`
- venv: `~/.hermes/hermes-agent/venv/bin/hermes`

## Key Concepts Captured

### Dreamer Build Signal Format
```
[BUILD: project-slug]
one sentence about what you want to exist
```
Signal goes in `~/.hermes/profiles/subc/room/signal-log/`

### Idea Contract Fields
What should exist · Who benefits · Why now · Evidence · Out of scope · Location · Verification method

### Product Plan Fields (Main → Coder)
Allowed paths · Planned files · Non-goals · Verification commands · Acceptance checks · Risk · Protected surfaces

### Walk Modes (Dreamer)
- `drift-from-research`: start from research snapshot, move sideways
- `continue-project`: check existing projects for life
- `pure-tangent`: ignore research, follow curiosity
- `tend-the-room`: maintenance — prune stale items

### Research Loop Discipline
Observe → Infer priorities → Gather evidence → Deepen one question → Update vault → Route implications
NOT: summarize news (that creates prose, not judgment)

### Evidence Stage Enforcement
finding ≠ claim ≠ verified knowledge ≠ conclusion ≠ daily summary ≠ task

## Manual X Browsing (No Auth Required)

User preference: browse X manually rather than set up xurl auth. When researching @gkisokay's posts:
- Use `browser_navigate(url="https://x.com/gkisokay")` directly
- X blocks `web_extract` — must use `browser_navigate` + `browser_snapshot` + `browser_scroll`
- X sometimes shows "Something went wrong. Try reloading" for certain tab views — use direct article URLs instead (e.g. `https://x.com/gkisokay/article/2040044476060864598`)
- Substack is accessible via `web_extract` — good for longer-form content

## Missing Pieces

1. **Graeme's public buildroom** — not publicly available. His GitHub (github.com/gkisokay) has 0 public repos. The `/buildroom` template with schemas/docs is referenced in the post but not published. Check for updates or ask him directly.

2. **Control Room UI** — the React Control Room from his `agent-runtime` is not publicly available.

## How to Start Individual Agents

```bash
# Via wrapper scripts (in ~/.local/bin — need PATH update):
research chat
subc chat
main chat
coder chat
qa chat

# Or via direct venv call:
~/.hermes/hermes-agent/venv/bin/research chat
~/.hermes/hermes-agent/venv/bin/subc chat

# Via hermes with profile flag:
~/.hermes/hermes-agent/venv/bin/hermes --profile research chat
```

## Hermes Dashboard Navigation

- Sessions: http://127.0.0.1:9119/sessions
- Profiles: http://127.0.0.1:9119/profiles
- Cron: http://127.0.0.1:9119/cron
- Logs: http://127.0.0.1:9119/logs
- Config: http://127.0.0.1:9119/config
- Keys: http://127.0.0.1:9119/env
- Plugins: http://127.0.0.1:9119/plugins
- Kanban: http://127.0.0.1:9119/kanban

## Related Skill

- `hermes-multi-agent-workflow` — class-level skill covering the same architecture