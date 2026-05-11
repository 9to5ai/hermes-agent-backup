#!/usr/bin/env python3
import json, time

# Use Chrome CDP at port 18800
import urllib.request
import websocket

# Create a new tab
new_tab_data = urllib.request.urlopen('http://127.0.0.1:18800/json/new').read()
new_tab = json.loads(new_tab_data)
ws_url = new_tab['webSocketDebuggerUrl']
tab_id = new_tab['id']
print(f"Created new tab: {tab_id}, URL: {new_tab.get('url', 'empty')}")

ws = websocket.create_connection(ws_url, timeout=30, suppress_origin=True)

def send_cmd(cmd, params=None):
    id_ = int(time.time() * 1000)
    msg = json.dumps({'id': id_, 'method': cmd, 'params': params or {}})
    ws.send(msg)
    resp = ws.recv()
    return json.loads(resp)

# Navigate to Gemini
result = send_cmd('Page.navigate', {'url': 'https://gemini.google.com/app'})
print(f"Navigate result: {result}")
time.sleep(5)

# Check page title
result = send_cmd('Runtime.evaluate', {'expression': 'document.title'})
print(f"Title: {result}")

# Find the textarea
result = send_cmd('Runtime.evaluate', {'expression': '''
(function() {
  var ta = document.querySelector('textarea');
  var div = document.querySelector('div.ql-editor[contenteditable="true"]');
  if (ta) return 'TEXTAREA: ' + ta.className;
  if (div) return 'DIV_EDITOR: ' + div.className;
  return 'NOT FOUND. Looking for inputs... buttons: ' + document.querySelectorAll('button').length + ' textareas: ' + document.querySelectorAll('textarea').length;
})()
'''})
print(f"Input check: {result}")

# Type the prompt
prompt = "Write the most detailed notes about this video: https://www.youtube.com/watch?v=4Lk_mkAkmdc"
result = send_cmd('Runtime.evaluate', {'expression': f'''
(function() {{
  var ta = document.querySelector('textarea');
  if (ta) {{
    ta.focus();
    return 'focused textarea';
  }}
  var div = document.querySelector('div.ql-editor[contenteditable="true"]');
  if (div) {{
    div.focus();
    return 'focused div';
  }}
  return 'no input found';
}})()
'''})
print(f"Focus: {result}")

# Actually insert text using Input.insertText
result = send_cmd('Input.insertText', {'text': prompt})
print(f"InsertText: {result}")
time.sleep(2)

# Find and click send button
result = send_cmd('Runtime.evaluate', {'expression': '''
(function() {
  var btns = Array.from(document.querySelectorAll('button'));
  for (var b of btns) {
    if (b.textContent.trim() === 'Send message' || b.getAttribute('aria-label') === 'Send message') {
      b.click();
      return 'CLICKED Send message';
    }
  }
  // Try by class
  for (var b of btns) {
    var cls = (b.className || '').toLowerCase();
    if (cls.includes('send')) {
      b.click();
      return 'CLICKED by class: ' + b.className;
    }
  }
  return 'NO SEND. Buttons: ' + btns.map(function(b){ return b.textContent.trim().substring(0,30) + '|' + b.className.substring(0,30); }).join('; ');
})()
'''})
print(f"Send button: {result}")

print("Waiting 35 seconds for response...")
time.sleep(35)

# Extract response using TreeWalker
result = send_cmd('Runtime.evaluate', {'expression': '''
(function() {
  var seen = {}, texts = [];
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  while(walker.nextNode()) {
    var node = walker.currentNode;
    var t = node.textContent.trim();
    if (t.length > 10 && t.length < 3000 && !seen[t]) {
      // Skip obvious noise
      if (t.indexOf('style') !== -1 || t.indexOf('display') !== -1) continue;
      seen[t] = true;
      texts.push(t);
    }
  }
  return JSON.stringify(texts.slice(0, 300));
})()
'''})
print(f"Response length: {len(result.get('result', {}).get('result', {}).get('value', ''))}")
print(f"Response preview: {str(result.get('result', {}).get('result', {}).get('value', ''))[:500]}")

ws.close()
print("Done")
