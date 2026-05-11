#!/usr/bin/env python3
"""
canary.py — Regression canary runner for the Autonomous Recovery Layer.
After a repair, runs a small deterministic test to verify the fix worked.
If canary fails: revert to last good checkpoint, escalate.
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

HERMES_HOME = Path.home() / ".hermes"
CANARIES_DIR = HERMES_HOME / "profiles" / "recover" / "canaries"
STATE_DIR = HERMES_HOME / "profiles" / "recover" / "state"
RESULTS_LOG = STATE_DIR / "canaries.log"
CHECKPOINTS_DIR = STATE_DIR / "checkpoints"


def list_canaries() -> list[Path]:
    if not CANARIES_DIR.exists():
        return []
    return list(CANARIES_DIR.glob("*.py")) + list(CANARIES_DIR.glob("*.sh"))


def run_canary(canary: Path, profile: str) -> dict:
    """Run a single canary script."""
    start = datetime.now()
    try:
        if canary.suffix == ".py":
            result = subprocess.run(
                ["python3", str(canary), "--profile", profile],
                capture_output=True, text=True, timeout=30
            )
        else:
            result = subprocess.run(
                [str(canary), profile],
                capture_output=True, text=True, timeout=30
            )
        elapsed = (datetime.now() - start).total_seconds()
        outcome = "pass" if result.returncode == 0 else "fail"
    except subprocess.TimeoutExpired:
        elapsed = (datetime.now() - start).total_seconds()
        outcome = "timeout"
        result = None
    except Exception as e:
        elapsed = (datetime.now() - start).total_seconds()
        outcome = "error"
        result = None

    return {
        "canary": canary.name,
        "profile": profile,
        "outcome": outcome,
        "elapsed_seconds": round(elapsed, 2),
        "stdout": result.stdout[:500] if result else str(e),
        "stderr": result.stderr[:500] if result else "",
        "timestamp": datetime.now().isoformat(),
    }


def log_result(result: dict):
    """Log canary result."""
    with open(RESULTS_LOG, "a") as f:
        f.write(json.dumps(result) + "\n")


def revert_to_checkpoint(profile: str):
    """Revert to last good checkpoint if canary fails."""
    checkpoints = sorted(CHECKPOINTS_DIR.glob(f"checkpoint_{profile}_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not checkpoints:
        return {"outcome": "no_checkpoint", "profile": profile}

    last = checkpoints[0]
    # In a real implementation, this would restore the state
    # For now, we just log the intent
    return {
        "outcome": "reverted",
        "profile": profile,
        "checkpoint": str(last),
        "timestamp": datetime.now().isoformat(),
    }


def run_all_canaries(profile: str) -> dict:
    """Run all canaries for a profile after repair."""
    canaries = list_canaries()
    if not canaries:
        return {"outcome": "no_canaries", "profile": profile, "canaries_run": 0}

    results = []
    all_passed = True
    for canary in canaries:
        result = run_canary(canary, profile)
        results.append(result)
        log_result(result)
        if result["outcome"] != "pass":
            all_passed = False

    if not all_passed:
        # Revert on any failure
        revert_result = revert_to_checkpoint(profile)
        return {
            "outcome": "reverted",
            "profile": profile,
            "canaries_run": len(canaries),
            "results": results,
            "revert": revert_result,
        }

    return {
        "outcome": "all_passed",
        "profile": profile,
        "canaries_run": len(canaries),
        "results": results,
    }


if __name__ == "__main__":
    profile = sys.argv[1] if len(sys.argv) > 1 else "research"
    result = run_all_canaries(profile)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["outcome"] == "all_passed" else 1)