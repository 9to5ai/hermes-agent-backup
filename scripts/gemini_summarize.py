#!/usr/bin/env python3
"""CDP-based Gemini - navigate and type prompt."""
import json, time, urllib.request
from websocket import create_connection

HOST = "http://127.0.0.1:18800"
VIDEO_ID = "ena1W3_lWpc"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
PROMPT = f"Write the most detailed notes about this video: {VIDEO_URL}"

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
    
    print("Navigating...")
    send_ws(ws, msg_id, "Page.navigate", {"url": "https://gemini.google.com/app"}, timeout=30)
    time.sleep(6)
    
    print("Typing prompt...")
    send_ws(ws, msg_id, "Runtime.evaluate", {
        "expression": "(function() { var el = document.querySelector('div.ql-editor[contenteditable=\"true\"]') || document.querySelector('[contenteditable=\"true\"]') || document.querySelector('textarea'); if (el) { el.focus(); return 'OK'; } return 'NOT FOUND'; })()"
    })
    send_ws(ws, msg_id, "Input.insertText", {"text": PROMPT}, timeout=10)
    time.sleep(1)
    
    print("Clicking send...")
    result = send_ws(ws, msg_id, "Runtime.evaluate", {
        "expression": "(function() { var btn = document.querySelector('[aria-label*=\"Send\"]') || document.querySelector('button[aria-label*=\"Send\"]'); if (btn) { btn.click(); return 'CLICKED'; } return 'NOT FOUND'; })()"
    })
    print("Send result:", result.get('result', {}).get('result', {}).get('value'))
    
    print("Waiting 25s...")
    time.sleep(25)
    
    # Save state for next script
    state = {"done": True, "video_id": VIDEO_ID}
    with open('/Users/momo/.hermes/cron/output/gemini_state.json', 'w') as f:
        json.dump(state, f)
    print("Done waiting, state saved")
    
    ws.close()

if __name__ == "__main__":
    main()