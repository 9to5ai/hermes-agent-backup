#!/usr/bin/env python3
"""
One-time initialization: seed the log with ALL existing videos except the top N.
The top N will be treated as "new" so the cron job processes them on first run.
"""
import subprocess
import json
import os
from datetime import datetime

LOG_FILE = os.path.expanduser("~/.hermes/cron/output/playlist_watcher_log.json")
OUTPUT_DIR = os.path.expanduser("~/.hermes/cron/output/")
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL7p-a4kuEU_tpR4DxY02x3KqIotrXqucg"
SKIP_TOP_N = 5  # Treat top N as "new" for first-run test

os.makedirs(OUTPUT_DIR, exist_ok=True)

result = subprocess.run(
    ["yt-dlp", "--flat-playlist", "--print", "%(title)s | %(id)s", PLAYLIST_URL],
    capture_output=True, text=True
)

videos = []
for line in result.stdout.strip().split("\n"):
    if " | " in line:
        parts = line.split(" | ", 1)
        videos.append({"title": parts[0].strip(), "id": parts[1].strip()})

print(f"Total videos in playlist: {len(videos)}")

log_data = {}
for i, video in enumerate(videos):
    status = "new" if i < SKIP_TOP_N else "seeded"
    log_data[video["id"]] = {
        "title": video["title"],
        "status": status,
        "checked": datetime.now().isoformat()
    }

with open(LOG_FILE, "w") as f:
    json.dump(log_data, f, indent=2)

print(f"Log seeded: {len(videos)} videos. Top {SKIP_TOP_N} marked as 'new' for first-run processing.")
print(f"New videos on first run:")
for v in videos[:SKIP_TOP_N]:
    print(f"  - {v['title']} ({v['id']})")
