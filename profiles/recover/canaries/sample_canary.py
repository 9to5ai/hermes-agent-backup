#!/usr/bin/env python3
"""
sample_canary.py — Sample regression canary.
Tests that the research vault is accessible and has recent receipts.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

HERMES_HOME = Path.home() / ".hermes"


def check_vault_accessible():
    vault = HERMES_HOME / "profiles" / "research" / "vault"
    if not vault.exists():
        return False, f"Vault not found: {vault}"
    return True, "Vault accessible"


def check_recent_receipt():
    runs = HERMES_HOME / "profiles" / "research" / "vault" / "runs"
    if not runs.exists():
        return False, "Runs dir not found"
    receipts = sorted(runs.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not receipts:
        return False, "No receipts found"
    last = datetime.fromtimestamp(receipts[0].stat().st_mtime)
    age = (datetime.now() - last).total_seconds() / 60
    if age > 120:
        return False, f"Last receipt too old: {age:.0f}min"
    return True, f"Last receipt: {age:.0f}min ago"


def check_subc_room():
    room = HERMES_HOME / "profiles" / "subc" / "room"
    if not room.exists():
        return False, f"Subc room not found: {room}"
    return True, "Subc room accessible"


if __name__ == "__main__":
    checks = [check_vault_accessible, check_recent_receipt, check_subc_room]
    failures = []
    for check in checks:
        passed, msg = check()
        if not passed:
            failures.append(msg)
            print(f"FAIL: {msg}")
        else:
            print(f"PASS: {msg}")

    sys.exit(0 if not failures else 1)