# Vault Structure Reference

## Purpose

The vault is an evidence chain — a permanent, auditable record of research findings. It is not a scratchpad or a report. Every piece of information flows through the chain: raw capture → finding → claim → dossier.

## Directory Schema

```
vault/
  health/          # One health check per run (run completes → health check)
  sources/         # Source registry + per-source subdirs for raw surface data
    registry.md    # Canonical list of registered surfaces
    <surface>/     # Per-surface: raw captures, cookies, session state
  raw/             # One raw sweep capture file per run (what was searched/collected)
  findings/        # One finding file per discrete new signal
  claims/          # One claim file per assertion being tracked
  dossiers/        # Living synthesis documents (fully rewritten each sweep)
  decisions/       # Decision ledger: stale checks + explicit decisions
  runs/           # One run receipt per run
```

## File Naming Conventions

| Directory | Filename Pattern | Example |
|-----------|-----------------|---------|
| health/ | `YYYY-MM-DDTHH-MM-SSZ.md` | `2026-05-12T12-00-00Z.md` |
| runs/ | `YYYY-MM-DDTHH-MM-SSZ.md` | `2026-05-12T12-00-00Z.md` |
| raw/ | `YYYY-MM-DDTHH-MM-SSZ.md` | `2026-05-12T12-00-00Z.md` |
| decisions/ | `STALE_CHECK-YYYY-MM-DDTHH-MM-SSZ.md` OR `DECISION-YYYY-MM-DDTHH-MM-SSZ.md` | `STALE_CHECK-2026-05-12T12-00-00Z.md` |
| findings/ | `YYYY-MM-DD-<slug>.md` | `2026-05-12-os-kernel-syscall-replay-pattern.md` |
| claims/ | `YYYY-MM-DD-<slug>.md` | `2026-05-12-recovery-gap-confirmed.md` |
| dossiers/ | `<subject>.md` | `ai-agents.md` |

## Evidence Chain Flow

```
raw/          ← raw sweep output (what was queried, what came back)
    ↓
findings/     ← processed signals (source cited, confidence assessed)
    ↓
claims/       ← assertions being tracked (status: NEW/CONFIRMED/REVISED)
    ↓
dossiers/     ← living synthesis (all active findings + claims in one doc)
    ↓
inbox/        ← routing to downstream profiles (extracted from dossier routing section)
```

## Health Check Schema

Every health check file must contain:

```markdown
# Vault Health Check
**Run:** <timestamp>
**Status:** OPERATIONAL | DEGRADED | FAIL

## Directory Integrity
| Path | Exists | Writable | Content This Run |

## Source Surface Status
**Registered surfaces:** N
**Active this run:** N

## Vault Contents Summary
| Directory | Count | Notes |

## Alerts
- <any issues>

## Health Assessment
OPERATIONAL | DEGRADED | FAIL
```

## Run Receipt Schema

Every run receipt must contain:

```markdown
# RUN RECEIPT — <profile>
**Timestamp:** <timestamp>
**Status:** COMPLETED | PARTIAL | FAILED

## Surfaces Swept
## Findings Written (N new)
## Claims Updated/Added (N new)
## Vault Contents After This Run
## Handoffs
## Decision Ledger Status
```

## Decision Ledger Behavior

- **Stale check**: Written when no decision trigger threshold was crossed. Confirms the ledger is being monitored.
- **Decision record**: Written when a trigger threshold IS crossed. Contains: what was decided, rationale, alternatives considered.
- The ledger does NOT need to contain a decision every run. It must contain a stale check entry every run.
- A stale check file can be empty (0 bytes) — that's acceptable for a stale check.
- Decision records are never empty.

## Routing

The dossier's "Routing Relevance" section maps claims/findings to target profiles. Routing writes to:
`~/.hermes/profiles/<target_profile>/room/inbox-from-researchd/<timestamp>.md`

Inbox files should:
- Exist in the inbox directory
- Be named with the same timestamp as the run that produced them
- Reference specific finding/claim files in the vault evidence chain
