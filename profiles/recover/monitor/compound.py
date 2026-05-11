#!/usr/bin/env python3
"""
compound.py — Pattern learning for the Autonomous Recovery Layer.
Reads failure + repair logs and updates repair recipes.
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

HERMES_HOME = Path.home() / ".hermes"
STATE_DIR = HERMES_HOME / "profiles" / "recover" / "state"
FAILURES_LOG = STATE_DIR / "failures.log"
REPAIRS_LOG = STATE_DIR / "repairs.log"
RECIPES_FILE = STATE_DIR / "recipes.log"
COMPOUND_LOG = STATE_DIR / "compound.log"


def load_failures() -> list[dict]:
    """Load all logged failures."""
    if not FAILURES_LOG.exists():
        return []
    failures = []
    for line in FAILURES_LOG.open().read().splitlines():
        if line.startswith("[") and "{" in line:
            # Parse log line: [timestamp] {json}
            try:
                ts = line.split("]")[0][1:]
                body = line.split("]", 1)[1].strip()
                f = json.loads(body)
                f["logged_at"] = ts
                failures.append(f)
            except Exception:
                pass
    return failures


def load_repairs() -> list[dict]:
    """Load all logged repairs."""
    if not REPAIRS_LOG.exists():
        return []
    repairs = []
    for line in REPAIRS_LOG.open().read().splitlines():
        try:
            repairs.append(json.loads(line))
        except Exception:
            pass
    return repairs


def count_pattern(failures: list[dict], field: str, value: str) -> int:
    return sum(1 for f in failures if f.get(field) == value)


def build_pattern_report(failures: list[dict], repairs: list[dict]) -> dict:
    """Analyze failures and repairs to build pattern summary."""
    # Group by failure type
    by_type = defaultdict(list)
    for f in failures:
        by_type[f.get("type", "unknown")].append(f)

    # Group repairs by outcome
    by_outcome = defaultdict(list)
    for r in repairs:
        by_outcome[r.get("outcome", "unknown")].append(r)

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_failures": len(failures),
        "total_repairs": len(repairs),
        "by_type": {k: len(v) for k, v in by_type.items()},
        "repair_outcomes": {k: len(v) for k, v in by_outcome.items()},
        "most_common_failure": max(by_type, key=lambda k: len(by_type[k])) if by_type else "none",
        "repair_success_rate": round(
            len([r for r in repairs if r.get("outcome") == "success"]) / max(len(repairs), 1) * 100, 1
        ),
    }
    return report


def update_recipe_confidence():
    """Update recipe confidence scores based on repeated success."""
    if not RECIPES_FILE.exists():
        return

    recipes = []
    for line in RECIPES_FILE.open().read().splitlines():
        if line.startswith("RECIPE:"):
            try:
                recipes.append(json.loads(line.split("RECIPE:", 1)[1]))
            except Exception:
                pass

    if not recipes:
        return

    # Group by type + profile
    by_key = defaultdict(list)
    for r in recipes:
        key = (r.get("type"), r.get("profile"))
        by_key[key].append(r)

    updated = []
    for key, group in by_key.items():
        successes = sum(1 for r in group if r.get("success"))
        confidence = min(0.95, 0.5 + (successes / max(len(group), 1)) * 0.1)
        # Update most recent recipe with new confidence
        if group:
            group[-1]["confidence"] = round(confidence, 3)
            updated.append(group[-1])

    if updated:
        # Rewrite recipes file with updated confidences
        with open(RECIPES_FILE, "w") as f:
            for r in updated:
                f.write(f"RECIPE:{json.dumps(r)}\n")


def run_compounding():
    """Run a compounding pass — learn from recent failures/repairs."""
    failures = load_failures()
    repairs = load_repairs()

    if not failures and not repairs:
        return {"outcome": "no_data", "message": "No failures or repairs to analyze"}

    report = build_pattern_report(failures, repairs)

    # Update recipe confidences based on repeated repairs
    update_recipe_confidence()

    # Log the compounding report
    with open(COMPOUND_LOG, "a") as f:
        f.write(json.dumps(report) + "\n")

    return {
        "outcome": "compounded",
        "report": report,
        "recipes_updated": True,
    }


if __name__ == "__main__":
    result = run_compounding()
    print(json.dumps(result, indent=2))
    sys.exit(0)