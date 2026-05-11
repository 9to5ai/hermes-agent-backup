#!/usr/bin/env python3
"""
Hourly playlist watcher for Momo's YouTube playlist.
Checks for new videos, fetches transcripts, generates summaries, and posts to Telegram.
"""
import subprocess
import json
import sys
import os
from datetime import datetime

SKILL_DIR = "/Users/momo/.hermes/skills/media/youtube-content"
SCRIPT_PATH = os.path.join(SKILL_DIR, "scripts", "fetch_transcript.py")
LOG_FILE = os.path.expanduser("~/.hermes/cron/output/playlist_watcher_log.json")
OUTPUT_DIR = os.path.expanduser("~/.hermes/cron/output/")
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL7p-a4kuEU_tpR4DxY02x3KqIotrXqucg"
CHAT_ID = "925542650"  # Momo's Home
TELEGRAM_URL = f"https://api.telegram.org/bot missing/sendMessage"  # placeholder - will use send_message tool

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def get_playlist_videos():
    """Get current playlist videos as list of (title, video_id)."""
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "%(title)s | %(id)s", PLAYLIST_URL],
        capture_output=True, text=True
    )
    videos = []
    for line in result.stdout.strip().split("\n"):
        if " | " in line:
            parts = line.split(" | ", 1)
            videos.append({"title": parts[0].strip(), "id": parts[1].strip()})
    return videos

def read_log():
    """Read the log file of already-processed video IDs."""
    if not os.path.exists(LOG_FILE):
        return {}
    try:
        with open(LOG_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def write_log(log_data):
    """Write updated log file."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)

def fetch_transcript(video_id):
    """Fetch transcript for a video using the skill script."""
    result = subprocess.run(
        ["python3", SCRIPT_PATH, f"https://youtube.com/watch?v={video_id}", "--text-only"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, f"Error: {result.stderr}"
    return result.stdout, None

def generate_summary(transcript_text, video_title, video_id):
    """Generate summary using the model via the hermes execute_code context."""
    # We'll pass the transcript to the agent for summarization
    # The agent will handle this as part of the cron run
    return transcript_text  # Return raw for now, agent summarizes

def post_to_telegram(message):
    """Post message via send_message tool - this is called by the agent directly."""
    pass

def main():
    log("Starting playlist check...")
    
    videos = get_playlist_videos()
    log(f"Found {len(videos)} videos in playlist")
    
    log_data = read_log()
    
    new_videos = []
    for video in videos:
        vid_id = video["id"]
        if vid_id not in log_data:
            new_videos.append(video)
    
    if not new_videos:
        log("No new videos found.")
        print("NO_NEW_VIDEOS")
        return
    
    log(f"Found {len(new_videos)} new video(s): {[v['id'] for v in new_videos]}")
    
    # Process each new video (max 5 per run to avoid IP rate limiting)
    # Remaining videos will be picked up on the next hourly run
    import time
    new_videos = new_videos[:5]
    for i, video in enumerate(new_videos):
        if i > 0:
            time.sleep(2)  # Delay between transcript fetches to avoid IP rate limit
        vid_id = video["id"]
        title = video["title"]
        log(f"Processing: {title} ({vid_id})")
        
        transcript, err = fetch_transcript(vid_id)
        if err or not transcript:
            log(f"Failed to fetch transcript for {vid_id}: {err}")
            log_data[vid_id] = {"title": title, "status": "transcript_failed", "checked": datetime.now().isoformat()}
            write_log(log_data)
            continue
        
        # Store raw transcript for agent to summarize
        # The agent will generate the summary and post to Telegram
        log_data[vid_id] = {
            "title": title,
            "status": "transcript_ready",
            "checked": datetime.now().isoformat(),
            "transcript": transcript[:5000]  # Store preview for context
        }
        write_log(log_data)
        
        # Print structured output for the agent to process
        print(f"NEW_VIDEO|{vid_id}|{title}|{transcript[:2000]}")
    
    log(f"Processed {len(new_videos)} new video(s).")

if __name__ == "__main__":
    main()
