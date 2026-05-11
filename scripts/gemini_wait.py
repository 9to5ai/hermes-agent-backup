#!/usr/bin/env python3
import json, time
from websocket import create_connection

WS_URL = "ws://127.0.0.1:18800/devtools/page/5A2A3EB5992BACA9F861B289A408E82F"

def send_cmd(ws, method, params=None, _id=1):
    payload = {"id": _id, "method": method, "params": params or {}}
    ws.send(json.dumps(payload))
    resp = ws.recv()
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

ws = create_connection(WS_URL, timeout=60, suppress_origin=True)
print("Connected")

# Check for stop button presence
for i in range(30):  # Wait up to 30 seconds
    result = send_cmd(ws, "Runtime.evaluate", {
        "expression": """
(function() {
  var stopBtn = document.querySelector('button[aria-label*="Stop"]') || document.querySelector('button[aria-label*="Stop generating"]');
  var containers = document.querySelectorAll('.message-content, .model-response, .response-container, .response-content, .markdown');
  var text = '';
  containers.forEach(c => { text += c.innerText + '\\n'; });
  return {hasStop: !!stopBtn, containerText: text.substring(0, 2000), containers: containers.length};
})()
""",
        "returnByValue": True
    })
    val = result.get('result', {}).get('result', {}).get('value', {})
    print(f"Check {i+1}: hasStop={val.get('hasStop')}, containers={val.get('containers')}, text_len={len(val.get('containerText',''))}")
    if not val.get('hasStop') and val.get('containerText', '').strip():
        print("Response complete!")
        print("TEXT:", val.get('containerText', ''))
        break
    time.sleep(2)

ws.close()
