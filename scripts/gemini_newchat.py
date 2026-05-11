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

ws = create_connection(WS_URL, timeout=15, suppress_origin=True)
print("Connected")

# Navigate to a fresh Gemini app page
send_cmd(ws, "Page.navigate", {"url": "https://gemini.google.com/app"})
time.sleep(4)

# Check for "New chat" button and click it
result = send_cmd(ws, "Runtime.evaluate", {
    "expression": """
(function() {
  // Look for new chat button in various forms
  var buttons = [...document.querySelectorAll('button')];
  var newChatBtn = buttons.find(b => b.textContent.includes('New chat') || b.getAttribute('aria-label') === 'New chat');
  if (newChatBtn) { newChatBtn.click(); return 'clicked new chat'; }
  // Try keyboard shortcut
  var body = document.querySelector('body');
  body.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', code: 'Escape', bubbles: true}));
  return 'buttons found: ' + buttons.map(b => b.textContent.trim().substring(0, 30)).join(', ').substring(0, 300);
})()
""",
    "returnByValue": True
})
print("New chat result:", result.get('result', {}).get('result', {}).get('value'))
time.sleep(2)

# Now type the prompt
video_id = "YSaww_tepJ4"
prompt = f"Write the most detailed notes about this video: https://www.youtube.com/watch?v={video_id}"

result2 = send_cmd(ws, "Runtime.evaluate", {
    "expression": """
(function() {
  var div = document.querySelector('div.ql-editor[contenteditable="true"]');
  if (div) { div.focus(); return 'focused'; }
  return 'no div';
})()
""",
    "returnByValue": True
})
print("Focus:", result2.get('result', {}).get('result', {}).get('value'))

result3 = send_cmd(ws, "Input.insertText", {"text": prompt})
print("InsertText:", result3.get('result'))
time.sleep(1)

# Click send
result4 = send_cmd(ws, "Runtime.evaluate", {
    "expression": """
(function() {
  var btn = document.querySelector('button[aria-label="Send message"]');
  if (btn) { btn.click(); return 'sent'; }
  return 'no send button';
})()
""",
    "returnByValue": True
})
print("Send:", result4.get('result', {}).get('result', {}).get('value'))

ws.close()
print("Prompt sent, now waiting for response...")
