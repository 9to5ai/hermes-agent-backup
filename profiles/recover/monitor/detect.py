#!/usr/bin/env python3
"""
detect.py — Stall/silence/loop detection for the Autonomous Recovery Layer.
Watches run receipts and signal logs across all agent profiles.
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, List, Dict

HERMES_HOME = Path.home() / ".hermes"
PROFILES = ["research", "subc", "main", "coder", "qa"]
STATE_DIR = HERMES_HOME / "profiles" / "recover" / "state"

# Thresholds (configurable)
STALL_THRESHOLD_MINUTES = {
    "research": 60,
    "subc": 45,
    "main": 30,
    "coder": 90,
    "qa": 45,
}
STALE_CONSECUTIVE = 3
LOOP_MAX = 5


def get_last_receipt_time(profile: str) -> Optional[datetime]:
    runs_dir = HERMES_HOME / "profiles" / profile / "vault" / "runs"
    if not runs_dir.exists():
        return None
    receipts = sorted(runs_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not receipts:
        return None
    return datetime.fromtimestamp(receipts[0].stat().st_mtime)


def get_signal_state(profile: str) -> Dict:
    signal_log = HERMES_HOME / "profiles" / profile / "room" / "signal-log" / "current.json"
    if signal_log.exists():
        return json.loads(signal_log.read_text())
    return {}


def get_output_hash(profile: str) -> Optional[str]:
    # For research: check latest finding
    if profile == "research":
        findings_dir = HERMES_HOME / "profiles" / profile / "vault" / "findings"
        if findings_dir.exists():
            files = sorted(findings_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
            if files:
                return files[0].read_text()[:500]
    return None


def detect_stalls() -> list[dict]:
    """Find phases that should have completed but haven't."""
    now = datetime.now()
    stalled = []
    for profile in PROFILES:
        last = get_last_receipt_time(profile)
        if last is None:
            continue
        threshold = STALL_THRESHOLD_MINUTES.get(profile, 60)
        elapsed = (now - last).total_seconds() / 60
        if elapsed > threshold:
            stalled.append({
                "type": "stall",
                "profile": profile,
                "last_receipt": last.isoformat(),
                "elapsed_minutes": round(elapsed, 1),
                "threshold_minutes": threshold,
                "severity": "critical" if elapsed > threshold * 2 else "warning",
            })
    return stalled


def detect_stale_outputs() -> list[dict]:
    """Find outputs that haven't changed in consecutive runs."""
    # Track last 3 hashes per profile
    hash_history: dict[str, list[str]] = defaultdict(list)
    stale = []
    for profile in PROFILES:
        h = get_output_hash(profile)
        if h:
            hash_history[profile].append(h)
    for profile, hashes in hash_history.items():
        if len(hashes) >= STALE_CONSECUTIVE:
            if all(h == hashes[0] for h in hashes):
                stale.append({
                    "type": "stale",
                    "profile": profile,
                    "consecutive_same": len(hashes),
                    "severity": "warning",
                })
    return stale


def load_state() -> dict:
    state_file = STATE_DIR / "detector_state.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {"last_states": defaultdict(dict), "loop_count": defaultdict(int)}


def save_state(state: dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "detector_state.json").write_text(json.dumps(state, indent=2))


def detect_loops() -> list[dict]:
    """Detect same state repeated across cycles."""
    state = load_state()
    current_states = {}
    for profile in PROFILES:
        sig = get_signal_state(profile)
        current_states[profile] = json.dumps(sig.get("current_walk", {}), sort_keys=True)

    loops = []
    for profile, current in current_states.items():
        last = state["last_states"].get(profile)
        if last == current:
            state["loop_count"][profile] += 1
        else:
            state["loop_count"][profile] = 0
        if state["loop_count"][profile] >= LOOP_MAX:
            loops.append({
                "type": "deadlock",
                "profile": profile,
                "repeat_count": state["loop_count"][profile],
                "severity": "critical",
            })
        state["last_states"][profile] = current
    save_state(state)
    return loops


def run_detection() -> dict:
    """Run all detectors, return findings."""
    failures = []
    failures.extend(detect_stalls())
    failures.extend(detect_stale_outputs())
    failures.extend(detect_loops())

    log_failures(failures)

    return {
        "timestamp": datetime.now().isoformat(),
        "failures": failures,
        "total": len(failures),
        "critical": sum(1 for f in failures if f.get("severity") == "critical"),
    }


def log_failures(failures: list):
    """Append failures to failure log."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    log = STATE_DIR / "failures.log"
    lines = []
    for f in failures:
        lines.append(f"[{datetime.now().isoformat()}] {json.dumps(f)}")
    if lines:
        log.open("a").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    result = run_detection()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["total"] == 0 else 1)