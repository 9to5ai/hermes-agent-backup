#!/usr/bin/env python3
"""
repair.py — Auto-repair strategies for the Autonomous Recovery Layer.
Takes detection output and applies the right repair recipe.
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

HERMES_HOME = Path.home() / ".hermes"
PROFILES = ["research", "subc", "main", "coder", "qa"]
STATE_DIR = HERMES_HOME / "profiles" / "recover" / "state"
RECIPES_FILE = STATE_DIR / "recipes.log"
REPAIR_LOG = STATE_DIR / "repairs.log"


def load_recipes() -> List[dict]:
    """Load repair recipes from log."""
    if not RECIPES_FILE.exists():
        return []
    recipes = []
    for line in RECIPES_FILE.open().read().splitlines():
        if line.startswith("RECIPE:"):
            try:
                recipes.append(json.loads(line.split("RECIPE:", 1)[1]))
            except Exception:
                pass
    return recipes


def find_recipe(failure_type: str, profile: str, recipes: List[dict]) -> Optional[dict]:
    """Find matching repair recipe for failure type + profile."""
    candidates = [r for r in recipes if r.get("type") == failure_type and r.get("profile") == profile]
    if not candidates:
        candidates = [r for r in recipes if r.get("type") == failure_type]
    if not candidates:
        return None
    return max(candidates, key=lambda r: r.get("confidence", 0.5))


def write_recipe(failure: dict, fix_applied: str, success: bool):
    """Write a learned recipe after repair attempt."""
    # Build recipe from failure + outcome
    recipe = {
        "type": failure.get("type"),
        "profile": failure.get("profile"),
        "cause": failure.get("cause", "unknown"),
        "fix": fix_applied,
        "success": success,
        "confidence": 0.5,  # increases with repetition
        "timestamp": datetime.now().isoformat(),
    }
    with open(RECIPES_FILE, "a") as f:
        f.write(f"RECIPE:{json.dumps(recipe)}\n")


def log_repair(failure: dict, action: str, outcome: str, recipe_used: str = None):
    """Log repair attempt to repair log."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "failure": failure,
        "action": action,
        "outcome": outcome,
        "recipe": recipe_used,
    }
    with open(REPAIR_LOG, "a") as f:
        f.write(f"{json.dumps(entry)}\n")


def repair_stall(failure: dict, recipe: dict = None) -> dict:
    """Re-trigger a stalled phase."""
    profile = failure["profile"]
    action = ""

    if profile == "research":
        # Re-trigger research loop via cron
        action = "hermes cron run research-loop"
    elif profile == "subc":
        # Re-trigger Dreamer walk
        action = "hermes -p subc chat -q 'Continue your walk from where you left off'"
    elif profile == "main":
        # Re-ping main with health check
        action = "hermes -p main chat -q 'Health check: are you waiting on anything?'"
    elif profile == "coder":
        # Re-trigger coder
        action = "hermes -p coder chat -q 'Check your build queue and resume if blocked'"
    elif profile == "qa":
        # Re-trigger QA
        action = "hermes -p qa chat -q 'Check your verification queue'"

    if action:
        # Execute repair action
        result = subprocess.run(action, shell=True, capture_output=True, text=True, timeout=60)
        outcome = "success" if result.returncode == 0 else "failed"

    # Also create a checkpoint marker
    checkpoint = {
        "profile": profile,
        "failure": failure,
        "repair_action": action,
        "timestamp": datetime.now().isoformat(),
    }
    checkpoint_file = STATE_DIR / f"checkpoint_{profile}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    checkpoint_file.write_text(json.dumps(checkpoint))

    return {"outcome": outcome, "action": action}


def repair_stale(failure: dict, recipe: dict = None) -> dict:
    """Mark stale output and request fresh work."""
    profile = failure["profile"]

    # Mark the stale output
    if profile == "research":
        findings_dir = HERMES_HOME / "profiles" / profile / "vault" / "findings"
        if findings_dir.exists():
            stale_marker = findings_dir / f".stale_{datetime.now().strftime('%Y%m%d%H%M%S')}.mark"
            stale_marker.write_text(f"Marked stale at {datetime.now().isoformat()}\nFailure: {json.dumps(failure)}")

    # Request fresh work by injecting a wake-up signal to subc inbox
    inbox = HERMES_HOME / "profiles" / "subc" / "room" / "inbox-from-researchd"
    wake_up = inbox / f"wake-up_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
    wake_up.write_text(f"# Wake-Up Signal\n\nOutput from {profile} went stale. Request fresh work.\n\n**Failure:** {json.dumps(failure)}\n")

    return {"outcome": "success", "action": "marked_stale_injected_wakeup"}


def repair_deadlock(failure: dict, recipe: dict = None) -> dict:
    """Inject reset signal to clear a deadlock."""
    profile = failure["profile"]

    # Write a reset signal to the profile's signal state
    room_dir = HERMES_HOME / "profiles" / profile / "room"
    signal_log_dir = room_dir / "signal-log"
    signal_log_dir.mkdir(parents=True, exist_ok=True)
    reset_signal = signal_log_dir / "reset.json"
    reset = {
        "type": "reset",
        "profile": profile,
        "reason": "deadlock_detected",
        "timestamp": datetime.now().isoformat(),
        "repeat_count": failure.get("repeat_count", 0),
    }
    reset_signal.write_text(json.dumps(reset, indent=2))

    # Also clear the detection state's loop counter
    import json as jsonmod
    state_file = STATE_DIR / "detector_state.json"
    if state_file.exists():
        state = jsonmod.loads(state_file.read_text())
        state["loop_count"][profile] = 0
        state_file.write_text(jsonmod.dumps(state, indent=2))

    return {"outcome": "success", "action": "reset_injected"}


def escalate(failure: dict, reason: str):
    """Escalate to main operator with failure context."""
    # Write to main's inbox
    inbox = HERMES_HOME / "profiles" / "main" / "inbox" / f"escalation_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text(f"# Escalation — {failure.get('type')} — {failure.get('profile')}\n\n**Reason:** {reason}\n**Failure:** {json.dumps(failure, indent=2)}\n**Time:** {datetime.now().isoformat()}\n")


def apply_repair(failure: dict) -> dict:
    """Match failure to repair strategy and apply."""
    failure_type = failure.get("type")
    profile = failure.get("profile")

    # First try recipe
    recipes = load_recipes()
    recipe = find_recipe(failure_type, profile, recipes)

    if failure_type == "stall":
        result = repair_stall(failure, recipe)
    elif failure_type == "stale":
        result = repair_stale(failure, recipe)
    elif failure_type == "deadlock":
        result = repair_deadlock(failure, recipe)
    else:
        result = {"outcome": "unknown_failure_type", "action": "none"}

    # Log the repair attempt
    log_repair(failure, result.get("action", "unknown"), result.get("outcome", "unknown"), recipe_used=json.dumps(recipe) if recipe else None)

    # Write recipe if this succeeded (for future compounding)
    if result.get("outcome") == "success":
        write_recipe(failure, result.get("action", ""), True)
    elif result.get("outcome") == "failed":
        # Failed repair — escalate
        escalate(failure, f"Repair failed twice: {result.get('action')}")
        write_recipe(failure, result.get("action", ""), False)

    return result


def run_repairs(failures: List[dict]) -> dict:
    """Process all failures and apply repairs."""
    results = []
    for failure in failures:
        if failure.get("severity") == "critical":
            # Critical failures: repair, then escalate
            result = apply_repair(failure)
            results.append({"failure": failure, "repair": result})
            if result.get("outcome") == "failed":
                escalate(failure, "Critical failure repair failed")
        elif failure.get("severity") == "warning":
            # Warnings: repair and watch
            result = apply_repair(failure)
            results.append({"failure": failure, "repair": result})
        else:
            # Info: log only
            results.append({"failure": failure, "repair": {"outcome": "no_action"}})

    return {
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "total_failures": len(failures),
        "repaired": sum(1 for r in results if r["repair"].get("outcome") == "success"),
        "failed": sum(1 for r in results if r["repair"].get("outcome") == "failed"),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: repair.py <failures_json>")
        sys.exit(1)

    failures = json.loads(sys.argv[1])
    result = run_repairs(failures)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["failed"] == 0 else 1)