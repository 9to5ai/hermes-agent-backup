#!/usr/bin/env python3
"""Gemini notes using fresh WS connections per action."""
from websocket import create_connection
import json, time, sys

CHROME_WS = "ws://127.0.0.1:18800/devtools/page/FE7D27B6BAB1BB2BFD6145A38B2517B5"

def ws_connect():
    return create_connection(CHROME_WS, timeout=15, suppress_origin=True)

def send(ws, cmd):
    ws.send(json.dumps(cmd))
    resp = ws.recv()
    return json.loads(resp)

def eval_js(ws, expr):
    """Evaluate JavaScript and return result value."""
    result = send(ws, {"id": 1, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True, "awaitPromise": True}})
    return result.get('result', {}).get('result', {}).get('value', '')

def main():
    video_id = sys.argv[1] if len(sys.argv) > 1 else "JH65uE9oEqs"
    prompt = f"Write the most detailed notes about this video: https://www.youtube.com/watch?v={video_id}"

    # Fresh connection
    ws = ws_connect()

    # Navigate
    print("Navigating...")
    send(ws, {"id": 1, "method": "Page.navigate", "params": {"url": "https://gemini.google.com/app"}})
    time.sleep(8)

    # Check title
    title = eval_js(ws, "document.title")
    print(f"Page title: {title}")

    # Find and focus input
    print("Finding input...")
    result = eval_js(ws, """
(function() {
    var el = document.querySelector('div[contenteditable="true"]') || document.querySelector('textarea');
    if (el) { el.focus(); return 'found:' + el.tagName; }
    return 'not found';
})()
""")
    print(f"Input focus: {result}")
    time.sleep(0.5)

    # Insert prompt
    print("Inserting text...")
    send(ws, {"id": 2, "method": "Input.insertText", "params": {"text": prompt}})
    time.sleep(1)

    # Check text
    text = eval_js(ws, """
(function() {
    var el = document.querySelector('div[contenteditable="true"]') || document.querySelector('textarea');
    return el ? (el.innerText || el.value || '').substring(0, 100) : 'not found';
})()
""")
    print(f"Input text: {text}")

    # Find and click send
    print("Clicking send...")
    result = eval_js(ws, """
(function() {
    var btn = document.querySelector('button[aria-label="Send message"]') || document.querySelector('.send-button') || [...document.querySelectorAll('button')].find(function(b) { return b.textContent.trim() === 'Send'; });
    if (btn) { btn.click(); return 'clicked'; }
    return 'not found: ' + [...document.querySelectorAll('button')].map(function(b) { return b.ariaLabel || b.textContent.trim(); }).join(', ');
})()
""")
    print(f"Send click: {result}")

    # Wait for response
    print("Waiting for response...")
    for i in range(18):
        time.sleep(5)
        elapsed = (i + 1) * 5
        body_text = eval_js(ws, """
(function() {
    var stop = document.querySelector('button[aria-label*="Stop\"]');
    var resp = document.querySelector('.message-content,.model-response');
    var body = document.body ? document.body.innerText.substring(0, 300) : '';
    return JSON.stringify({hasStop: !!stop, hasResp: !!resp, bodyLen: body.length, body: body.substring(0, 200)});
})()
""")
        print(f"  [{elapsed}s]: {body_text[:200]}")
        try:
            data = json.loads(body_text)
            if data.get('hasResp') or (not data.get('hasStop') and data.get('bodyLen', 0) > 100):
                print("Response detected!")
                break
        except:
            pass
    else:
        print("Timeout!")

    # Extract full text
    print("Extracting...")
    full_text = eval_js(ws, """
(function() {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    var lines = [];
    while(walker.nextNode()) {
        var t = walker.currentNode.textContent.trim();
        if(t.length > 5 && t.length < 2000) lines.push(t);
    }
    return lines.join('\\n').substring(0, 15000);
})()
""")
    print(f"Extracted {len(full_text)} chars")
    for i in range(0, len(full_text), 500):
        print(full_text[i:i+500])
        print("---")

    ws.close()

if __name__ == "__main__":
    main()