#!/usr/bin/env python3
"""CDP-based Gemini - extract response."""
import json, time, urllib.request
from websocket import create_connection

HOST = "http://127.0.0.1:18800"

def get_tabs():
    req = urllib.request.urlopen(f"{HOST}/json", timeout=10)
    return json.loads(req.read().decode())

def send_ws(ws, msg_id_ref, method, params, timeout=60):
    msg_id_ref[0] += 1
    ws.send(json.dumps({"id": msg_id_ref[0], "method": method, "params": params}))
    ws.settimeout(timeout)
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = ws.recv()
            obj = json.loads(resp)
            if obj.get('id') == msg_id_ref[0]:
                return obj
        except:
            time.sleep(0.05)
    return {"error": "timeout"}

def main():
    tabs = get_tabs()
    gemini_tab = None
    for t in tabs:
        url = t.get('url', '')
        if "gemini.google.com" in url and "accounts" not in url:
            gemini_tab = t
            break
    
    if not gemini_tab:
        print("No Gemini tab")
        return
    
    ws_url = gemini_tab.get('webSocketDebuggerUrl')
    ws = create_connection(ws_url, timeout=30, suppress_origin=True)
    ws.settimeout(30)
    
    msg_id = [0]
    send_ws(ws, msg_id, "Page.enable", {})
    send_ws(ws, msg_id, "Runtime.enable", {})
    
    # Extract full response - try response container then tree walker
    print("Extracting response...")
    
    result = send_ws(ws, msg_id, "Runtime.evaluate", {
        "expression": """
        (function() {
            var container = document.querySelector('.response-container') ||
                           document.querySelector('.message-content') ||
                           document.querySelector('.model-response');
            if (container) {
                return 'CONTAINER:' + container.textContent.substring(0, 15000);
            }
            
            // Tree walker approach
            var text = '';
            var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
            var lastText = '';
            while(walker.nextNode()) {
                var t = walker.currentNode.textContent.trim();
                if(t.length > 5 && t.length < 2000) {
                    text += t + '\\n';
                    lastText = t;
                }
            }
            return 'WALKER:' + text.substring(0, 15000);
        })()
        """,
        "returnByValue": True
    })
    
    response = result.get('result', {}).get('result', {}).get('value', '')
    print(f"Response length: {len(response)}")
    
    with open('/Users/momo/.hermes/cron/output/gemini_response.txt', 'w') as f:
        f.write(response)
    
    print("Saved")
    print("\n===RESPONSE===")
    print(response[:3000])
    
    ws.close()

if __name__ == "__main__":
    main()