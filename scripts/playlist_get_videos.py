#!/usr/bin/env python3
import json, time, sys
from websocket import create_connection

# Connect to Chrome
ws = create_connection("http://127.0.0.1:18800/json/new", timeout=10, suppress_origin=True)
print("Connected to Chrome")
sys.stdout.flush()

# Get the new target
data = ws.recv()
target = json.loads(data)
print(f"Target: {target.get('title', 'unknown')}")
ws.close()

# Connect to that target's WebSocket
ws_url = target['webSocketDebuggerUrl']
ws = create_connection(ws_url, timeout=10, suppress_origin=True)

# Enable DOM
ws.send(json.dumps({"id": 1, "method": "DOM.enable"}))
ws.recv()

# Navigate to playlist
ws.send(json.dumps({"id": 2, "method": "Page.navigate", "params": {"url": "https://youtube.com/playlist?list=PL7p-a4kuEU_tpR4DxY02x3KqIotrXqucg"}}))
ws.recv()
time.sleep(5)

# Execute script to get videos
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
  return JSON.stringify(videos);
})()
"""

ws.send(json.dumps({"id": 3, "method": "Runtime.evaluate", "params": {"expression": script, "returnByValue": True}}))
response = ws.recv()
result = json.loads(response)
videos = json.loads(result['result']['result']['value'])
print(f"Found {len(videos)} videos")
for v in videos:
    print(f"{v['id']} | {v['title']}")
ws.close()