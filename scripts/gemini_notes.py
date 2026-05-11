#!/usr/bin/env python3
"""Get Gemini notes for a YouTube video using direct CDP/WebSocket."""
import json, time, sys
from websocket import create_connection

CHROME_WS = "ws://127.0.0.1:18800/devtools/page/FE7D27B6BAB1BB2BFD6145A38B2517B5"

def get_ws():
    ws = create_connection(CHROME_WS, timeout=15, suppress_origin=True)
    return ws

def send(ws, cmd):
    ws.send(json.dumps(cmd))
    resp = ws.recv()
    return json.loads(resp)

def wait_for_response(ws, timeout=60, poll=3):
    for i in range(timeout // poll):
        time.sleep(poll)
        # Check for response container or stop button
        result = send(ws, {
            "id": 100, "method": "Runtime.evaluate",
            "params": {"expression": """
(function() {
  var stop = document.querySelector('button[aria-label*="Stop"]');
  var resp = document.querySelector('.message-content,.model-response,.response-container,.response-content,.markdown');
  var genText = document.querySelector('.gen-msg');
  return {
    hasStop: !!stop,
    hasResp: !!resp,
    hasGen: !!genText,
    respText: resp ? resp.innerText.substring(0, 200) : '',
    genText: genText ? genText.innerText.substring(0, 100) : ''
  };
})()
""", "returnByValue": True}
        })
        val = result.get('result', {}).get('value', {})
        if isinstance(val, dict):
            if val.get('hasResp') or not val.get('hasStop'):
                # Response is done (no stop button) or response found
                return val
        print(f"  Poll {i+1}: {val}")
    return {}

def extract_full_text(ws):
    result = send(ws, {
        "id": 200, "method": "Runtime.evaluate",
        "params": {"expression": """
(function() {
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  var lines = [];
  while(walker.nextNode()) {
    var t = walker.currentNode.textContent.trim();
    if(t.length > 5 && t.length < 1000) lines.push(t);
  }
  return lines.join('\\n').substring(0, 15000);
})()
""", "returnByValue": True}
    })
    return result.get('result', {}).get('value', {})

def main():
    video_id = sys.argv[1] if len(sys.argv) > 1 else "JH65uE9oEqs"
    prompt = f"Write the most detailed notes about this video: https://www.youtube.com/watch?v={video_id}"
    
    ws = get_ws()
    print("Connected to Chrome")
    
    # Check current page
    result = send(ws, {"id": 1, "method": "Runtime.evaluate", "params": {"expression": "document.body.innerText.substring(0,100)", "returnByValue": True}})
    print("Current page:", result.get('result', {}).get('value', ''))
    
    # Click on the main chat area to activate input
    result = send(ws, {"id": 2, "method": "Runtime.evaluate", "params": {"expression": "(function(){var el=document.querySelector('div[contenteditable=\"true\"]');if(el){el.click();return'ok';}return'not found';})()", "returnByValue": True}})
    print("Click:", result.get('result', {}).get('value', ''))
    time.sleep(1)
    
    # Insert the prompt text
    result = send(ws, {"id": 3, "method": "Input.insertText", "params": {"text": prompt}})
    print("InsertText:", result)
    time.sleep(1)
    
    # Find and click send button
    result = send(ws, {"id": 4, "method": "Runtime.evaluate", "params": {"expression": "(function(){var b=document.querySelector('button[aria-label=\"Send message\"]')||document.querySelector('.send-button');if(b){b.click();return'clicked';}return'not found';})()", "returnByValue": True}})
    print("Send click:", result.get('result', {}).get('value', ''))
    
    print("\nWaiting for response...")
    resp_val = wait_for_response(ws)
    print("Response status:", resp_val)
    
    # Wait a bit more for text to fully populate
    time.sleep(5)
    
    full_text = extract_full_text(ws)
    print(f"\n=== EXTRACTED TEXT ({len(full_text)} chars) ===")
    print(full_text[:500])
    print("...")
    print(full_text[-200:])
    
    ws.close()

if __name__ == "__main__":
    main()
