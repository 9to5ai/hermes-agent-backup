# Recovery Status — 2026-05-14 02:00

## Summary
- **Failures detected:** 6 (5 critical)
- **Repaired:** 5
- **Failed to repair:** 1
- **All canaries:** PASS

## Failures

### 1. Research — Stall (WARNING, repair FAILED)
- Last receipt: `2026-05-14T00:12:45.053928`
- Elapsed: 108.2 min (threshold: 60 min)
- Repair attempt: `hermes cron run research-loop` — **FAILED**
- Action needed: Manual intervention for research phase

### 2. Research — Deadlock (CRITICAL, repaired)
- Repeat count: 5 cycles
- Repair: reset injected → SUCCESS

### 3. Subc — Deadlock (CRITICAL, repaired)
- Repeat count: 5 cycles
- Repair: reset injected → SUCCESS

### 4. Main — Deadlock (CRITICAL, repaired)
- Repeat count: 5 cycles
- Repair: reset injected → SUCCESS

### 5. Coder — Deadlock (CRITICAL, repaired)
- Repeat count: 5 cycles
- Repair: reset injected → SUCCESS

### 6. QA — Deadlock (CRITICAL, repaired)
- Repeat count: 5 cycles
- Repair: reset injected → SUCCESS

## Action Required
Research stall repair failed. Manual review of research phase needed.
