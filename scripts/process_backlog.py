#!/usr/bin/env python3
"""
Process 14 backlog playlist videos: Gemini notes → stdout (cron auto-delivers).
Uses Chrome CDP WebSocket at port 18800.
"""
import json, subprocess, time
from websocket import create_connection

# Active Chrome debug port
WS_URL = "ws://127.0.0.1:18800"

TRACKER_PATH = "/Users/momo/.hermes/cron/output/playlist_watcher_log.json"
LOCK_PATH = "/Users/momo/.hermes/cron/output/playlist_watcher.lock"

VIDEOS = [
    ("eRS3CmvrOvA", "I Tried 100+ Claude Code Skills. These 6 Are The Best"),
    ("Bgxsx8slDEA", "Stop Using Claude Code Without an Agentic OS"),
    ("XZYqX6ZY6QY", "LIFE IS SHORT — Most People Realize It Too Late."),
    ("nccFRimntJA", "The Hidden Strategy That Makes Certain Employees Untouchable."),
    ("oH2iZ5yG9Nk", "30 分鐘重塑你的《孫子兵法》世界觀！..."),
    ("S9InNdQhFwc", "Using Your Money To Be Happier"),
    ("pNXHX7FlYR0", "iOS 27 Adds an Apple Wallet Feature We've Been Waiting For"),
    ("BLBRRNwMZNE", "Once You Learn This, Saying No to You Becomes Impossible"),
    ("RA1Ym0HHDOg", "Cam'ron BELIEVES LeBron will be 'tied up with Jordan'..."),
    ("CQIq2k-9Chs", "If You're Serious About Building Wealth in Australia, Start Here!"),
    ("r-CGDAGeXLU", "全网最全！60分钟全面掌握Claude Code~..."),
    ("Bg-IPiql7x8", "Hermes Agent might have just killed OpenClaw"),
    ("9L4XaHGaPLY", "LeBron Breaks Down Round 1 and Previews OKC Series | MIND THE GAME"),
    ("6-i9nIIi80E", "This Is How The Wealthy Invest Their Money"),
]

def get_active_tab_url(title_contains):
    """Get the websocket URL for an active tab matching title fragment."""
    import urllib.request
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:18800/json").read().decode())
    for t in tabs:
        if title_contains.lower() in t['title'].lower():
            return t["id"], t["webSocketDebuggerUrl"]
    return None, None

def cdp_ws(ws_url, method, params=None):
    """Send CDP command via existing WebSocket connection."""
    ws = create_connection(ws_url, timeout=30, suppress_origin=True)
    msg_id = int(time.time() * 1000)
    payload = json.dumps({"id": msg_id, "method": method, "params": params or {}}).encode()
    ws.send(payload)
    resp = ws.recv()
    ws.close()
    return json.loads(resp)

def navigate_to_gemini(ws_url):
    cdp_ws(ws_url, "Page.navigate", {"url": "https://gemini.google.com/app"})
    time.sleep(4)

def submit_gemini_prompt(ws_url, video_id):
    prompt = f"Write the most detailed notes about this video: https://www.youtube.com/watch?v={video_id}"
    # Insert text character by character
    for chunk in [prompt[i:i+200] for i in range(0, len(prompt), 200)]:
        cdp_ws(ws_url, "Input.insertText", {"text": chunk})
        time.sleep(0.05)
    time.sleep(1)
    # Click send
    cdp_ws(ws_url, "Runtime.evaluate", {
        "expression": """
(function() {
  var btns = document.querySelectorAll('button');
  for (var b of btns) {
    if (b.getAttribute('aria-label') && b.getAttribute('aria-label').match(/send/i)) {
      b.click(); return 'SENT';
    }
  }
  var form = document.querySelector('form');
  if (form) { form.submit(); return 'SUBMITTED'; }
  return 'NO_SEND';
})()
"""
    })

def wait_and_click_thinking(ws_url):
    """Wait for Gemini to respond, clicking Show thinking if needed."""
    for i in range(90):
        time.sleep(2)
        r = cdp_ws(ws_url, "Runtime.evaluate", {
            "expression": """
(function() {
  var btns = document.querySelectorAll('button');
  for (var b of btns) {
    if (b.innerText && b.innerText.includes('Show thinking')) {
      b.click(); return 'SHOW_THINKING_CLICKED';
    }
  }
  var modelMsg = document.querySelector('[data-message-author-role="model"]');
  if (modelMsg) {
    var text = modelMsg.innerText || modelMsg.textContent || '';
    if (text.length > 200) return 'CONTENT:' + text.substring(0, 80);
  }
  return 'WAITING';
})()
"""
        })
        val = r.get('result', {}).get('result', {}).get('value', '')
        print(f"    poll {i}: {val[:80]}")
        if 'SHOW_THINKING_CLICKED' in val:
            time.sleep(3)
            break
        if 'CONTENT:' in val:
            time.sleep(2)
            break
    return True

def extract_notes(ws_url):
    r = cdp_ws(ws_url, "Runtime.evaluate", {
        "expression": """
(function() {
  var els = document.querySelectorAll('[data-message-author-role="model"]');
  if (els.length > 0) {
    return els[els.length-1].innerText;
  }
  return '';
})()
"""
    })
    return r.get('result', {}).get('result', {}).get('value', '') or ''

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
    # Find active Gemini tab
    gemini_id, gemini_ws = get_active_tab_url("gemini")
    if not gemini_ws:
        print("ERROR: No active Gemini tab found")
        return
    print(f"Using Gemini tab: {gemini_id}")

    for i, (video_id, title) in enumerate(VIDEOS):
        print(f"\n[VIDEO {i+1}/14] {video_id}: {title[:60]}", flush=True)
        
        try:
            # Navigate to Gemini
            navigate_to_gemini(gemini_ws)
            
            # Submit prompt
            submit_gemini_prompt(gemini_ws, video_id)
            
            # Wait for response
            wait_and_click_thinking(gemini_ws)
            
            # Extract notes
            notes = extract_notes(gemini_ws)
            print(f"  Notes length: {len(notes)} chars", flush=True)
            
            if len(notes) < 100:
                print(f"  WARNING: Notes seem short. Raw: {notes[:200]}")
            
            # Output formatted for cron delivery
            print(f"\n{'='*60}")
            print(f"**{title}** ([YouTube](https://www.youtube.com/watch?v={video_id}))")
            print(f"{'='*60}")
            print(notes)
            print(f"\n[PROCESSED: {video_id}]")
            
            # Update tracker
            update_tracker(video_id)
            
        except Exception as e:
            print(f"  ERROR: {e}")
        
        time.sleep(3)
    
    print("\nALL_DONE")

if __name__ == "__main__":
    main()
