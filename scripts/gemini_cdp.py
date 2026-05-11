#!/usr/bin/env python3
import json, time, subprocess, sys

# Connect to Chrome via CDP
import urllib.request
import websocket

# Get the WebSocket URL for the first tab
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:18800/json/new').read())
ws_url = tabs['webSocketDebuggerUrl']
print(f"Connected to tab: {tabs.get('title', 'unknown')}")

ws = websocket.create_connection(ws_url, timeout=30, suppress_origin=True)

def send_cmd(cmd, params=None):
    id_ = int(time.time() * 1000)
    msg = json.dumps({'id': id_, 'method': cmd, 'params': params or {}})
    ws.send(msg)
    resp = ws.recv()
    return json.loads(resp)

# Navigate to Gemini
send_cmd('Page.navigate', {'url': 'https://gemini.google.com/app'})
time.sleep(4)

# Check if we're on the right page
send_cmd('Runtime.evaluate', {'expression': 'document.title'})
time.sleep(1)

# Find the textarea and type
send_cmd('Runtime.evaluate', {'expression': '''
(function() {
  var textarea = document.querySelector('textarea');
  if (!textarea) return 'NO TEXTAREA';
  return 'TEXTAREA FOUND';
})()
'''})
time.sleep(0.5)

# Type into textarea
prompt = "Write the most detailed notes about this video: https://www.youtube.com/watch?v=4Lk_mkAkmdc"
send_cmd('Runtime.evaluate', {'expression': f'''
(function() {{
  var textarea = document.querySelector('textarea');
  if (!textarea) return 'NO TEXTAREA';
  textarea.focus();
  textarea.value = {json.dumps(prompt)};
  textarea.dispatchEvent(new Event('input', {{bubbles: true}}));
  textarea.dispatchEvent(new Event('change', {{bubbles: true}}));
  return 'TYPED';
}})()
'''})
time.sleep(1)

# Click send button
send_cmd('Runtime.evaluate', {'expression': '''
(function() {
  var btns = document.querySelectorAll('button');
  for (var b of btns) {
    if (b.textContent.trim() === 'Send message' || b.getAttribute('aria-label') === 'Send message') {
      b.click();
      return 'SENT';
    }
  }
  // Try finding send button by looking for buttons with send-related classes
  for (var b of btns) {
    var cls = b.className || '';
    if (cls.toLowerCase().includes('send')) {
      b.click();
      return 'SENT by class: ' + cls;
    }
  }
  return 'NO SEND BUTTON';
})()
'''})
print("Clicked send, waiting for response...")
time.sleep(30)

# Extract response text
result = send_cmd('Runtime.evaluate', {'expression': '''
(function() {
  var seen = {}, results = [];
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  while(walker.nextNode()) {
    var t = walker.currentNode.textContent.trim();
    if(t.length > 5 && t.length < 2000) {
      if (!seen[t]) {
        seen[t] = true;
        results.push(t);
      }
    }
  }
  return JSON.stringify(results.slice(0, 200));
})()
'''})
print(f"Extracted text length: {len(result.get('result', {}).get('result', {}).get('value', ''))}")

ws.close()
print("Done")
