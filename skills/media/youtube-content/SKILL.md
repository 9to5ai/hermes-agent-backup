---
name: youtube-content
description: >
  Summarize YouTube videos into structured content using Gemini browser session.
  Use when the user shares a YouTube URL or video link, asks to summarize a video,
  or wants to extract and reformat content from any YouTube video.
  ALL operations go through the browser — NO API keys, NO transcript downloads, NO rate limits.
---

# YouTube Content Tool

Summarize YouTube videos using Gemini in the browser. No API, no rate limits.

## Core Principle

**Use the browser for YouTube access — no API keys, no rate limits.** The browser is Jun's logged-in Chrome session.

## When to Use This Skill vs. playlist-watcher

- **For automated playlist monitoring (cron jobs):** → Load `playlist-watcher` skill instead. It handles playlist change detection, per-video Gemini requests, Telegram delivery, and tracker updates automatically.
- **For ad-hoc single-video research:** → Use this skill. One-off summarization of a specific video URL the user shares.

## Step 1 — Summarize via Gemini (One Video)

1. Navigate Gemini to: `https://gemini.google.com/app`
2. Type the prompt:
   ```
   Write the most detailed notes about this video: https://www.youtube.com/watch?v=VIDEO_ID
   ```
   **IMPORTANT: Always use "Write the most detailed notes" — NOT "Summarize in 3-5 bullet points". The user wants full Gemini output verbatim, not condensed bullet points.**
3. Wait for Gemini to finish generating (check browser_snapshot until response appears)
4. ⚠️ **IMPORTANT: Gemini may show a "Show thinking" button.** If the response appears truncated or only shows "Assessing the Task" / thinking-phase text, click the "Show thinking" button to reveal the full notes. After clicking, wait 5 seconds and take another snapshot.
5. Extract the full response text from the snapshot — headings, bullets, and paragraphs are all preserved in the snapshot output.
   - **Bold title** + hyperlink: `**Video Title** ([YouTube](https://www.youtube.com/watch?v=VIDEO_ID))`
   - Body: Gemini's full output verbatim — do NOT truncate, do NOT summarize
   - Preserve headings (`##`), bullet structure, and paragraph breaks exactly as Gemini returns them
6. Return the formatted output directly to the user.

## Output Format

**Full detailed notes** — Gemini's complete output verbatim. No truncation, no condensing, no bullet-point summaries. Preserve all headings (`##`), bullet structure, and paragraph breaks exactly as returned.

## Tracker Update — Use fcntl (Avoid Deadlock)

If updating the playlist tracker from an ad-hoc session (not the cron pipeline), use the direct fcntl approach — `playlist_watcher_check.py` deadlocks because it re-acquires its own lock:

```python
python3 -c "
import fcntl, json
lf = open('/Users/momo/.hermes/cron/output/playlist_watcher.lock', 'w')
fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
with open('/Users/momo/.hermes/cron/output/playlist_watcher_log.json') as f: d = json.load(f)
if 'VIDEO_ID' not in d.get('processed_videos',[]):
    d['processed_videos'].append('VIDEO_ID')
    with open('/Users/momo/.hermes/cron/output/playlist_watcher_log.json','w') as f: json.dump(d,f,indent=2)
    print('ADDED')
else: print('EXISTS')
fcntl.flock(lf.fileno(), fcntl.LOCK_UN); lf.close()
"
```

## Fallback: VTT Transcript Download + Local Parse

If browser/Gemini is unavailable (CDP connection fails, Gemini session dies post-submission, or no Chrome debugging port is open), fall back to `yt-dlp` to download auto-generated subtitles and parse them locally. This path has never failed and produces full transcript coverage.

**Step 1 — Download VTT subtitles:**
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download -o "%(id)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```
Output file: `{VIDEO_ID}.en.vtt`

**Step 2 — Parse to clean text:**
```python
import re

with open('/tmp/{VIDEO_ID}.en.vtt', 'r') as f:
    content = f.read()

entries = re.split(r'\n(?=\d{2}:\d{2}:\d{2}\.\d{3})', content)

clean_entries = []
seen_lines = set()
for entry in entries:
    lines = entry.strip().split('\n')
    text_parts = []
    for line in lines:
        if re.match(r'\d{2}:\d{2}:\d{2}', line):
            continue
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        text = re.sub(r'<[^>]+>', '', line).strip()
        text = re.sub(r'&gt;&gt;', '', text).strip()
        text = re.sub(r'\[.*?\]', '', text).strip()
        if text and len(text) > 2:
            text_parts.append(text)
    if text_parts:
        full_text = ' '.join(text_parts)
        if full_text not in seen_lines:
            seen_lines.add(full_text)
            clean_entries.append(full_text)

# Deduplicate near-duplicate consecutive lines
final_lines = []
for line in clean_entries:
    is_dup = False
    for e in final_lines:
        if line in e or e in line:
            is_dup = True
            break
    if not is_dup:
        final_lines.append(line)

full_transcript = ' '.join(final_lines)
# 59k chars for a ~47min video → manageable for note extraction
```

**Step 3 — Write notes from parsed transcript.** The VTT timestamps map to real video time; parse in chunks and extract key themes, quotes, and arguments. For ~47min videos, aim for 600-1200 word structured notes covering: main topics discussed, notable quotes, speaker's key arguments, and any concrete examples or frameworks mentioned.

> **Variable state across `execute_code` calls:** `execute_code` runs in an ephemeral sandbox — each invocation starts fresh with no access to variables or imports from prior calls. To pass data between calls, write to a temp file (`/tmp/`) and read it back in the next `execute_code` call. `terminal()` sessions (bash/python3) ARE persistent — variables survive within the same session but not across separate `terminal()` calls.

If browser tools fail with a stale CDP endpoint (`localhost:9222`), check for an existing Chrome remote debugging port:
```bash
lsof -nP -iTCP -sTCP:LISTEN | grep -E 'Chrome|18800|9222'
```
The usable Chrome session is often `http://127.0.0.1:18800` rather than `9222`. In cron runs, prefer direct-CDP Python scripts via `terminal()` rather than `execute_code()` if `import websocket` fails — `websocket-client` may be installed in the user's site-packages and visible to `/usr/bin/python3` in `terminal`, while the `execute_code` sandbox may not see it.
