#!/usr/bin/env python3
import json, time, subprocess, sys

# Chrome CDP connection
from websocket import create_connection

WS_URL = "ws://127.0.0.1:18800/devtools/page/6DC21EF6653431D438B0D3E650B036F6"

def cdp_send(method, params=None):
    ws = create_connection(WS_URL, timeout=30, suppress_origin=True)
    msg_id = 1
    msg = {"id": msg_id, "method": method, "params": params or {}}
    ws.send(json.dumps(msg))
    result = ws.recv()
    ws.close()
    return json.loads(result)

# Step 1: Navigate to playlist
print("Navigating to playlist...")
r = cdp_send("Page.navigate", {"url": "https://www.youtube.com/playlist?list=PL7p-a4kuEU_tpR4DxY02x3KqIotrXqucg"})
print("Nav result:", r)

time.sleep(5)

# Step 2: Get page content via Evaluate
script = """
(function() {
  var items = document.querySelectorAll('ytd-playlist-video-renderer');
  var videos = [];
  items.forEach(function(item) {
    var link = item.querySelector('a#video-title');
    if (link) {
      var href = link.href || link.getAttribute('href');
      var match = href.match(/[?&]v=([^&]+)/);
      if (match) {
        videos.push({id: match[1], title: link.textContent.trim()});
      }
    }
  });
  // Fallback
  if (videos.length === 0) {
    var anchors = document.querySelectorAll('a.ytLockupMetadataViewModelTitle[href*="watch?v="]');
    anchors.forEach(function(a) {
      var match = a.href.match(/[?&]v=([^&]+)/);
      if (match) {
        videos.push({id: match[1], title: a.textContent.trim().replace(/\\s+/g, ' ')});
      }
    });
  }
  return JSON.stringify(videos);
})()
"""
r = cdp_send("Runtime.evaluate", {"expression": script, "returnByValue": True})
content = r.get("result", {}).get("result", {})
value = content.get("value", "[]")
videos = json.loads(value)
print(f"Found {len(videos)} videos:", [v['id'] for v in videos])

# Step 3: Read tracker
tracker_path = "/Users/momo/.hermes/cron/output/playlist_watcher_log.json"
try:
    with open(tracker_path) as f:
        tracker = json.load(f)
except:
    tracker = {"processed_videos": []}

processed = tracker.get("processed_videos", [])
print(f"Tracker has {len(processed)} processed videos")

new_videos = [v for v in videos if v['id'] not in processed]
print(f"New videos: {[v['id'] for v in new_videos]}")

if not new_videos:
    print("[SILENT]")
    sys.exit(0)

# Process at most 1 video
video = new_videos[0]
video_id = video['id']
title = video['title']
print(f"Processing: {title} ({video_id})")

# Step 4: Navigate to Gemini
print("Navigating to Gemini...")
r = cdp_send("Page.navigate", {"url": "https://gemini.google.com/app"})
print("Gemini nav:", r)
time.sleep(5)

# Step 5: Find and fill the input
# Check for textarea or contenteditable div
prompt_script = """
(function() {
  var textarea = document.querySelector('textarea');
  if (textarea) {
    textarea.focus();
    return 'textarea:focus';
  }
  var editor = document.querySelector('div.ql-editor[contenteditable="true"]');
  if (editor) {
    editor.focus();
    return 'editor:focus';
  }
  var genimi_input = document.querySelector('textarea[aria-label*="ask"], textarea[aria-label*="message"], textarea.gI-BJc');
  if (genimi_input) {
    genimi_input.focus();
    return 'genimi:focus';
  }
  return 'NO_INPUT';
})()
"""
r = cdp_send("Runtime.evaluate", {"expression": prompt_script, "returnByValue": True})
print("Input check:", r)

# Type the prompt
prompt_text = f"Write the most detailed notes about this video: https://www.youtube.com/watch?v={video_id}"
cdp_send("Runtime.evaluate", {
    "expression": f"""
    (function() {{
      var el = document.querySelector('textarea');
      if (el) {{
        el.value = {json.dumps(prompt_text)};
        el.dispatchEvent(new Event('input', {{bubbles: true}}));
        return 'typed_in_textarea';
      }}
      var ed = document.querySelector('div.ql-editor[contenteditable="true"]');
      if (ed) {{
        ed.textContent = {json.dumps(prompt_text)};
        ed.dispatchEvent(new Event('input', {{bubbles: true}}));
        return 'typed_in_editor';
      }}
      return 'FAILED';
    }})()
    """,
    "returnByValue": True
})
time.sleep(1)

# Click send button
send_script = """
(function() {
  var btn = document.querySelector('button[aria-label*="Send"]') || 
            document.querySelector('button[aria-label*="send"]') ||
            document.querySelector('button[aria-label*="Submit"]') ||
            document.querySelector('.send-button') ||
            document.querySelector('button.ql-action[aria-label*="Send"]') ||
            document.querySelector('button[type="submit"]');
  if (btn) { btn.click(); return 'SENT'; }
  return 'NO_SEND_BTN';
})()
"""
r = cdp_send("Runtime.evaluate", {"expression": send_script, "returnByValue": True})
print("Send click:", r)

# Wait for response
print("Waiting for Gemini response...")
time.sleep(30)

# Extract response
extract_script = """
(function() {
  var text = '';
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  while(walker.nextNode()) {
    var t = walker.currentNode.textContent.trim();
    if(t.length > 5 && t.length < 1000) text += t + '\\n';
  }
  return text.substring(0, 15000);
})()
"""
for attempt in range(3):
    r = cdp_send("Runtime.evaluate", {"expression": extract_script, "returnByValue": True})
    content = r.get("result", {}).get("result", {}).get("value", "")
    
    # Check for stop button presence
    stop_check = cdp_send("Runtime.evaluate", {
        "expression": "!!document.querySelector('button[aria-label*=\"Stop\"]') || !!document.querySelector('.stop-button')",
        "returnByValue": True
    })
    is_still_loading = stop_check.get("result", {}).get("result", {}).get("value", False)
    
    if not is_still_loading:
        break
    time.sleep(5)

print(f"Extracted {len(content)} chars of content")

# Step 6: Send to Telegram
telegram_msg = f"**{title}** ([YouTube](https://www.youtube.com/watch?v={video_id}))\n\n{content}"
print(f"Telegram message length: {len(telegram_msg)}")

# Step 7: Update tracker using fcntl
import fcntl
lf = open('/Users/momo/.hermes/cron/output/playlist_watcher.lock', 'w')
fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
with open(tracker_path) as f:
    d = json.load(f)
if video_id not in d.get('processed_videos', []):
    d['processed_videos'].append(video_id)
    with open(tracker_path, 'w') as f:
        json.dump(d, f, indent=2)
    print("TRACKER UPDATED")
else:
    print("ALREADY_IN_TRACKER")
fcntl.flock(lf.fileno(), fcntl.LOCK_UN)
lf.close()

print(f"OUTPUT_FOR_DELIVERY:{telegram_msg}")
