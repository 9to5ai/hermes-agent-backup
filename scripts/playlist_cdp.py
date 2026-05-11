#!/usr/bin/env python3
import json, time
from websocket import create_connection

WS_URL = "ws://127.0.0.1:18800/devtools/page/5A2A3EB5992BACA9F861B289A408E82F"

def send_cmd(ws, method, params=None, _id=1):
    payload = {"id": _id, "method": method, "params": params or {}}
    ws.send(json.dumps(payload))
    resp = ws.recv()
    # Find the response for our id
    for line in resp.split('\n'):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if obj.get('id') == _id:
                return obj
        except:
            pass
    return None

ws = create_connection(WS_URL, timeout=15, suppress_origin=True)
print("Connected")

# Navigate to playlist
send_cmd(ws, "Page.navigate", {"url": "https://youtube.com/playlist?list=PL7p-a4kuEU_tpR4DxY02x3KqIotrXqucg"})
time.sleep(5)

# Get DOM snapshot
result = send_cmd(ws, "DOM.getDocument", {"depth": -1})
send_cmd(ws, "Runtime.evaluate", {
    "expression": """
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
  return JSON.stringify(videos);
})()
""",
    "returnByValue": True
})
time.sleep(2)

# Try alternative selector from skill
result2 = send_cmd(ws, "Runtime.evaluate", {
    "expression": """
(function() {
  return [...document.querySelectorAll('a.ytLockupMetadataViewModelTitle[href*="watch?v="]')].map(a => {
    const m = a.href.match(/[?&]v=([^&]+)/);
    return m && {id: m[1], title: a.textContent.trim().replace(/\\s+/g, ' ')};
  }).filter(Boolean);
})()
""",
    "returnByValue": True
})

print("ytd-playlist-video-renderer approach:", result.get('result', {}).get('result', {}).get('value', 'NONE'))
print("ytLockupMetadataViewModelTitle approach:", result2.get('result', {}).get('result', {}).get('value', 'NONE'))

ws.close()
