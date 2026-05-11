#!/usr/bin/env python3
"""
Process backlog of new playlist videos: Gemini notes → Telegram → update tracker.
Uses Chrome CDP WebSocket at port 18800. Self-contained, no agent tools needed.

Usage:
    python3 process_backlog.py

Edit VIDEOS list below to set target video IDs and titles.
"""
import json, subprocess, time
from websocket import create_connection

# === CONFIG ===
GEMINI_TAB = "4A710FB52373C063500F"   # Find via: curl -s http://127.0.0.1:18800/json
TELEGRAM_TAB = "B13606CABDB8515624213BA532736035"
WS_URL = "ws://127.0.0.1:18800"
TRACKER_PATH = "/Users/momo/.hermes/cron/output/playlist_watcher_log.json"
LOCK_PATH = "/Users/momo/.hermes/cron/output/playlist_watcher.lock"

VIDEOS = [
    # (video_id, title)
    ("eRS3CmvrOvA", "I Tried 100+ Claude Code Skills. These 6 Are The Best"),
    ("Bgxsx8slDEA", "Stop Using Claude Code Without an Agentic OS"),
    # ...
]
# ==============

def cdp(method, params=None, tab_id=None):
    if tab_id is None:
        tab_id = GEMINI_TAB
    payload = json.dumps({"id": 1, "method": method, "params": params or {}}).encode()
    ws = create_connection(f"{WS_URL}/devtools/page/{tab_id}", timeout=30, suppress_origin=True)
    ws.send(payload)
    resp = ws.recv()
    ws.close()
    return json.loads(resp)

def submit_to_gemini(video_id):
    prompt = f"Write the most detailed notes about this video: https://www.youtube.com/watch?v={video_id}"
    for chunk in [prompt[i:i+200] for i in range(0, len(prompt), 200)]:
        cdp("Input.insertText", {"text": chunk})
        time.sleep(0.1)
    time.sleep(1)
    cdp("Runtime.evaluate", {"expression": """
(function() {
  var btns = document.querySelectorAll('button');
  for (var b of btns) {
    if (b.innerText && b.innerText.match(/Send|submit|run/i)) { b.click(); return 'SENT'; }
  }
  var sendBtn = document.querySelector('[aria-label*="Send" i]');
  if (sendBtn) { sendBtn.click(); return 'SENT_ARIA'; }
  return 'NO_SEND';
})()"""})
    return True

def wait_and_click_show_thinking():
    for i in range(60):
        time.sleep(2)
        r = cdp("Runtime.evaluate", {"expression": """
(function() {
  var btns = document.querySelectorAll('button');
  for (var b of btns) {
    if (b.innerText && b.innerText.includes('Show thinking')) { b.click(); return 'THINKING_CLICKED'; }
  }
  var els = document.querySelectorAll('[data-message-author-role="model"]');
  if (els.length > 0 && els[els.length-1].innerText.length > 200) return 'CONTENT_READY';
  return 'WAITING';
})()"""})
        val = r.get('result', {}).get('result', {}).get('value', '')
        print(f"    Poll {i}: {val[:60]}")
        if 'THINKING_CLICKED' in val:
            time.sleep(3)
            break
        if 'CONTENT_READY' in val:
            break

def extract_gemini_notes():
    r = cdp("Runtime.evaluate", {"expression": """
(function() {
  var els = document.querySelectorAll('[data-message-author-role="model"]');
  return els.length > 0 ? els[els.length-1].innerText.substring(0, 50000) : '';
})()"""})
    return r.get('result', {}).get('result', {}).get('value', '')

def send_telegram(text, video_id, title):
    msg = f"**{title}** ([YouTube](https://www.youtube.com/watch?v={video_id}))\n\n{text}"
    cdp("Page.navigate", {"url": f"https://web.telegram.org/k/#-1003966589836?thread=2"}, TELEGRAM_TAB)
    time.sleep(3)
    for chunk in [msg[i:i+500] for i in range(0, len(msg), 500)]:
        cdp("Input.insertText", {"text": chunk}, TELEGRAM_TAB)
        time.sleep(0.1)
    time.sleep(1)
    cdp("Runtime.evaluate", {"expression": """
document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}));
"""}, TELEGRAM_TAB)
    return True

def update_tracker(video_id):
    import fcntl
    lf = open(LOCK_PATH, 'w')
    fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
    with open(TRACKER_PATH) as f:
        d = json.load(f)
    if video_id not in d.get('processed_videos', []):
        d['processed_videos'].append(video_id)
        with open(TRACKER_PATH, 'w') as f:
            json.dump(d, f, indent=2)
    fcntl.flock(lf.fileno(), fcntl.LOCK_UN)
    lf.close()

def main():
    for i, (video_id, title) in enumerate(VIDEOS):
        print(f"[{i+1}/{len(VIDEOS)}] {video_id}: {title[:50]}")
        cdp("Page.navigate", {"url": "https://gemini.google.com/app"})
        time.sleep(3)
        submit_to_gemini(video_id)
        wait_and_click_show_thinking()
        notes = extract_gemini_notes()
        print(f"    Notes: {len(notes)} chars")
        send_telegram(notes, video_id, title)
        update_tracker(video_id)
        print(f"    ✓ Done")
        time.sleep(3)

if __name__ == "__main__":
    main()
