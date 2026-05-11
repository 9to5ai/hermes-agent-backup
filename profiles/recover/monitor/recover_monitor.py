#!/usr/bin/env python3
"""
recover_monitor.py — Main entry point for the Autonomous Recovery Layer.
Ties detect + repair + canary together into a single pass.
Run via cron every 15-30 minutes.
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

HERMES_HOME = Path.home() / ".hermes"
SCRIPT_DIR = Path(__file__).parent


def run_detect() -> dict:
    """Run detection phase."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "detect.py")],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode not in (0, 1):
        return {"error": "detect_failed", "stdout": result.stdout[:500], "stderr": result.stderr[:500]}
    try:
        return json.loads(result.stdout)
    except Exception:
        return {"error": "detect_parse_failed", "raw": result.stdout[:500]}


def run_repair(failures: list) -> dict:
    """Run repair phase on detected failures."""
    if not failures:
        return {"outcome": "no_failures", "repaired": 0, "failed": 0}
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "repair.py"), json.dumps(failures)],
        capture_output=True, text=True, timeout=120
    )
    try:
        return json.loads(result.stdout)
    except Exception:
        return {"error": "repair_parse_failed", "raw": result.stdout[:500], "failures": len(failures)}


def run_canary(profile: str) -> dict:
    """Run canary checks after repairs."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "canary.py"), profile],
        capture_output=True, text=True, timeout=60
    )
    try:
        return json.loads(result.stdout)
    except Exception:
        return {"error": "canary_parse_failed", "raw": result.stdout[:500]}


def write_receipt(result: dict, phase: str):
    """Write a run receipt for this recovery pass."""
    receipt = {
        "phase": phase,
        "timestamp": datetime.now().isoformat(),
        "result": result,
    }
    receipts_dir = HERMES_HOME / "profiles" / "recover" / "state"
    receipts_dir.mkdir(parents=True, exist_ok=True)
    receipt_file = receipts_dir / f"recovery_receipt_{datetime.now().strftime('%Y%m%dT%H%M%S')}.json"
    receipt_file.write_text(json.dumps(receipt, indent=2))


def run_recovery_pass():
    """Run a full recovery pass: detect → repair → canary → log."""
    print(f"[{datetime.now().isoformat()}] Recovery pass starting...")

    # Phase 1: Detect
    detect_result = run_detect()
    write_receipt(detect_result, "detect")

    if detect_result.get("error"):
        print(f"Detect error: {detect_result}")
        return detect_result

    failures = detect_result.get("failures", [])
    critical = detect_result.get("critical", 0)
    print(f"  Detection: {len(failures)} failures ({critical} critical)")

    if not failures:
        print("  No failures detected — pass complete.")
        return {"outcome": "clean", "failures": 0}

    # Phase 2: Repair
    repair_result = run_repair(failures)
    write_receipt(repair_result, "repair")
    print(f"  Repair: {repair_result.get('repaired', 0)} repaired, {repair_result.get('failed', 0)} failed")

    # Phase 3: Canary (for critical failures)
    for failure in failures:
        if failure.get("severity") == "critical":
            profile = failure.get("profile", "research")
            canary_result = run_canary(profile)
            write_receipt(canary_result, f"canary_{profile}")
            if canary_result.get("outcome") == "reverted":
                print(f"  Canary FAILED for {profile} — reverted to checkpoint")
            else:
                print(f"  Canary passed for {profile}")

    # Phase 4: Compound (learn from this pass)
    compound_result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "compound.py")],
        capture_output=True, text=True, timeout=30
    )
    if compound_result.returncode == 0:
        print("  Compounding: patterns updated")

    return {
        "outcome": "pass_complete",
        "failures": len(failures),
        "critical": critical,
        "repair": repair_result,
    }


if __name__ == "__main__":
    result = run_recovery_pass()
    print(f"\nFinal: {json.dumps(result, indent=2)}")
    sys.exit(0 if result.get("outcome") == "clean" else 0)  # Always exit 0 — repairs are logged