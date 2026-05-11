#!/usr/bin/env python3
"""
Cron job for playlist watcher — uses playlist-watcher skill for full detailed notes.
Schedule: 1:00 AM AEST daily
"""

import subprocess
import json
import time
import fcntl
import os

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL7p-a4kuEU_tpR4DxY02x3KqIotrXqucg"
LOG_FILE = "/Users/momo/.hermes/cron/output/playlist_watcher_log.json"
LOCK_FILE = "/Users/momo/.hermes/cron/output/playlist_watcher.lock"
OUTPUT_DIR = "/Users/momo/.hermes/cron/output"

def get_playlist_ids():
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "id", "--no-warnings", "--quiet", PLAYLIST_URL],
        capture_output=True, text=True
    )
    return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            return json.load(f)
    return {"processed_videos": []}

def save_log(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_processed(video_id):
    lf = open(LOCK_FILE, "w")
    fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
    data = load_log()
    if video_id not in data["processed_videos"]:
        data["processed_videos"].append(video_id)
        save_log(data)
    fcntl.flock(lf.fileno(), fcntl.LOCK_UN)
    lf.close()

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ids = get_playlist_ids()
    log = load_log()
    new_ids = [i for i in ids if i not in log["processed_videos"]]
    print(f"[playlist-watcher] Found {len(new_ids)} new videos")
    for vid in new_ids:
        print(f"  -> {vid}")
        # NOTE: Gemini summarization is handled by the playlist-watcher skill.
        # This cron script only identifies new videos and updates the tracker.
        # Run the skill manually or via a subagent to get full detailed notes + Telegram posts.
        add_processed(vid)
        time.sleep(1)

if __name__ == "__main__":
    main()
