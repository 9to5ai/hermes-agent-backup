#!/usr/bin/env python3
"""
Playlist watcher — uses yt-dlp to detect new videos, with atomic state management.
The LLM must NEVER read/write the tracker JSON directly. All operations go through this script.

Usage:
  python3 playlist_watcher_check.py check   — fetch playlist, compare with tracker, print new IDs
  python3 playlist_watcher_check.py status   — print current tracker stats
"""

import json
import os
import sys
import subprocess
import fcntl
from datetime import datetime, timezone

TRACKER_FILE = os.path.expanduser("~/.hermes/cron/output/playlist_watcher_log.json")
PLAYLIST_URL = "https://youtube.com/playlist?list=PL7p-a4kuEU_tpR4DxY02x3KqIotrXqucg"
LOCK_FILE = TRACKER_FILE + ".lock"


def load_tracker():
    """Load tracker, dedup on read, return data dict and video set."""
    try:
        with open(TRACKER_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"processed_videos": [], "last_checked": None}

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for vid in data.get("processed_videos", []):
        if vid not in seen:
            seen.add(vid)
            deduped.append(vid)
    data["processed_videos"] = deduped
    return data, set(deduped)


def save_tracker(data):
    """Save tracker with merge-on-write protection (atomic)."""
    lock_fd = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)

        # Re-read current state and merge (union) — prevents overwriting concurrent changes
        try:
            with open(TRACKER_FILE, "r") as f:
                current = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            current = {"processed_videos": [], "last_checked": None}

        current_ids = set(current.get("processed_videos", []))
        new_ids = set(data.get("processed_videos", []))

        # Merge: keep disk order, append only truly new IDs
        merged = list(current.get("processed_videos", []))
        for vid in data.get("processed_videos", []):
            if vid not in current_ids:
                merged.append(vid)

        data["processed_videos"] = merged
        data["last_checked"] = datetime.now(timezone.utc).isoformat()

        # Write atomically via temp file
        tmp = TRACKER_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, TRACKER_FILE)
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()


def cmd_check():
    """Fetch playlist via yt-dlp, compare with tracker, print new ones."""
    # Fetch current playlist IDs
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "id", "--no-warnings", "--quiet", PLAYLIST_URL],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        # yt-dlp failed (rate-limited, network issue, etc.) — be silent, don't crash
        # The next run will retry. Do NOT print anything to stdout.
        sys.exit(0)

    playlist_ids = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    if not playlist_ids:
        sys.exit(0)

    data, tracked = load_tracker()

    new_ids = [vid for vid in playlist_ids if vid not in tracked]

    if not new_ids:
        pass  # Silent — no message sent
    else:
        for vid in new_ids:
            # Get title from yt-dlp for each new video
            title_result = subprocess.run(
                ["yt-dlp", "--print", "title", "--no-playlist", f"https://youtube.com/watch?v={vid}"],
                capture_output=True, text=True, timeout=30
            )
            title = title_result.stdout.strip() if title_result.returncode == 0 else "Unknown"
            print(f"NEW|{vid}|{title}")

    # Save deduped version if we cleaned anything
    if len(data["processed_videos"]) != len(tracked):
        save_tracker(data)


def cmd_add(video_id):
    """Atomically add a video ID to the tracker."""
    # save_tracker() owns the exclusive lock. Do not take LOCK_FILE here:
    # fcntl locks are process-associated, and nesting this with save_tracker()
    # can deadlock on some platforms during cron runs.
    data, _ = load_tracker()
    if video_id not in set(data["processed_videos"]):
        data["processed_videos"].append(video_id)
        save_tracker(data)
        print(f"ADDED:{video_id}:TOTAL:{len(data['processed_videos'])}")
    else:
        print(f"ALREADY_EXISTS:{video_id}:TOTAL:{len(data['processed_videos'])}")


def cmd_status():
    """Print tracker stats."""
    data, _ = load_tracker()
    total = len(data["processed_videos"])
    last_checked = data.get("last_checked", "never")
    print(f"TOTAL:{total}")
    print(f"LAST_CHECKED:{last_checked}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: playlist_watcher_check.py [check|add|status]", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "check":
        cmd_check()
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: playlist_watcher_check.py add <video_id>", file=sys.stderr)
            sys.exit(1)
        cmd_add(sys.argv[2])
    elif cmd == "status":
        cmd_status()
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
