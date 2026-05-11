# Control Room — Main Operator View

This is the operator's view of the multi-agent system. It tracks signals, builds, QA status, and trust across all agent profiles.

## Active Signals

Signals from Dreamer (subc) waiting for review:

```
signal-log/   ← [BUILD: slug] markers left by Dreamer
```

## Current Builds

Builds in progress (from Coder):

```
projects/   ← active build projects
```

## Approval Ledger

Decisions made by Main:

```
approval-ledger/   ← idea contracts + product plans + decisions
```

## Trust Reporting

Current room status across all profiles:
- `research` — vault health, source coverage
- `subc` — room state, signal activity
- `main` — approval queue depth
- `coder` — build queue, current task
- `qa` — verification pass/fail rate

## Dashboard

Access the Hermes dashboard at `http://localhost:9119` once started.

## Profiles

| Profile | Path | Status |
|---------|------|--------|
| default | ~/.hermes | Production owner |
| research | ~/.hermes/profiles/research | Evidence collector |
| subc | ~/.hermes/profiles/subc | Dreamer/Subconscious |
| main | ~/.hermes/profiles/main | Conscious operator |
| coder | ~/.hermes/profiles/coder | Builder |
| qa | ~/.hermes/profiles/qa | Auditor |

## Cron Jobs

| Job | Schedule | Function |
|-----|----------|----------|
| Research Loop | 0 */6 * * * | 6-hourly evidence gathering |
| Dreamer Morning Walk | 0 8 * * * | 8am drift-from-research |
| Dreamer Evening Tending | 0 20 * * * | 8pm tend-the-room |

## Handoff Flow

```
Research → (vault) → Dreamer → (signal-log/) → Main → (approval-ledger/) → Coder → QA → Retention
```