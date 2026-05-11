# Archived skill: hermes-cron-browser-debugging

Original path: `software-development/hermes-cron-browser-debugging/SKILL.md`

---

---
name: hermes-cron-browser-debugging
description: "Debug Hermes Agent cron jobs that fail silently when using browser tools — CDP unavailable in cron sandbox, Tavily search API failures, and the delegate_task subagent workaround."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, cron, browser, CDP, debugging, delegation, subagent]
    related_skills: [hermes-agent, subagent-driven-development, debugging-hermes-tui-commands, browser-tools]
---

# Hermes Cron Job Browser Tool Debugging

## Overview

When a cron job uses `browser_navigate`, `browser_snapshot`, or any CDP-based browser tool, it may silently fail — reporting `ok` but producing empty output. This happens because the cron sandbox does not have CDP/browser access, while the main session and delegate_task subagents do.

**Also**: `web_search` and `web_extract` rely on the Tavily API, which may return 402/432 errors when quota is exhausted or the service is down.

## When to Use

- A cron job reports `ok` but produces no output
- Browser tool calls in cron always return empty/null
- Web search/extraction cron jobs return empty digests
- Cron job with `browser` toolset enabled doesn't actually browse

## Symptoms

1. `cronjob(action='run', job_id='...')` returns `{"success": true, "last_status": "ok"}`
2. `last_run_at` timestamp doesn't update after the run
3. The agent's text output is empty or minimal
4. `delegate_task` with browser tools works fine when run manually

## Root Causes

### 1. CDP/Browser Unavailable in Cron Sandbox (most common)

The cron agent runs in an isolated environment that cannot reach the CDP endpoint used by `browser_navigate`. The agent receives no error — it just silently produces nothing.

**Fix**: Delegate to a browser-capable subagent:

```
cron job prompt → "Spawn a leaf subagent with toolsets=['browser','send_message'] and goal: [task description]"
```

The subagent runs in the main session context with full CDP/browser access.

### 2. Tavily API Down/Exhausted

`web_search` and `web_extract` use Tavily. If it returns 402/432, these tools return empty results silently.

**Fix**: Use `browser_navigate` on Google Search URLs instead:
- APRA news: `https://www.google.com/search?q=APRA+regulatory+cyber+AI+risk+Australia&num=5&tbm=nws`
- Cyber news: `https://www.google.com/search?q=cyber+attack+Australia+financial+services+incident&num=5&tbm=nws`

### 3. Cron Agent Completes Without Calling Tools

The LLM in the cron agent sometimes produces a "looks ok" text response without actually calling any tools, then exits. This is a model-level shortcut, not a tool failure.

**Fix**: Be explicit in the prompt that tools MUST be called, or use the delegate_task pattern.

## Debugging Steps

1. Run `cronjob(action='list')` — check `last_status` and `last_run_at`
2. Run `cronjob(action='run', job_id='...')` — trigger manually and observe
3. Check `last_run_at` — if it didn't update, tools weren't called
4. Test with `delegate_task` manually using same toolsets:
   ```
   delegate_task(
     goal="[same task as cron prompt]",
     toolsets=["browser", "send_message"]
   )
   ```
5. If delegate works and cron doesn't → CDP issue confirmed

## Reliable Cron Pattern for Browser-Based Digests

When building a daily digest/content monitoring cron job:

```
1. Cron triggers at schedule
2. Cron prompt spawns a delegate_task subagent:
   - toolsets=["browser", "send_message"]
   - goal: gather data via browser_navigate, compile digest, send via send_message
3. Subagent has full CDP access → runs browser steps successfully
4. Subagent sends to Telegram via send_message
```

**Example cron prompt structure:**
```
Spawn a leaf subagent with toolsets=["browser","send_message"] and goal:
"Gather data using browser_navigate:
1. https://source1.com
2. https://source2.com
[... specific URLs ...]

Compile into this exact format:
[format spec]

Send via: send_message(action='send', target='telegram:CHAT_ID:THREAD_ID')"
```

## Direct CDP Python Access (cron-safe, when browser tools work)

When `browser_*` tools are available in cron but pages have non-standard DOM or navigation instability, use direct CDP via Python `websocket-client` from `terminal()`:

```python
from websocket import create_connection
import json, time

# Discover page IDs
# curl -s http://127.0.0.1:18800/json  → look for your page title

page_id = "TARGET_PAGE_ID"  # from /json listing
ws_url = f"ws://127.0.0.1:18800/devtools/page/{page_id}"
ws = create_connection(ws_url, timeout=15, suppress_origin=True)

def send_cmd(method, params=None, seq=1):
    msg = {"id": seq, "method": method}
    if params: msg["params"] = params
    ws.send(json.dumps(msg))
    return json.loads(ws.recv())

# Force fresh navigation (avoids redirect loops that browser_navigate can get stuck in)
send_cmd("Page.navigate", {"url": "https://target-site.com"})
time.sleep(3)

# For Gemini: div.ql-editor[contenteditable=true] is the input, NOT textarea
# Focus it first
send_cmd("Runtime.evaluate", {
    "expression": "document.querySelector('div.ql-editor[contenteditable=\"true\"]').focus()",
    "returnByValue": True
})
# Then insert text
send_cmd("Input.insertText", {"text": "your prompt here"})
time.sleep(0.5)
# Click send
send_cmd("Runtime.evaluate", {
    "expression": "document.querySelector('button[aria-label*=\"Send\"]').click()",
    "returnByValue": True
})
time.sleep(30)  # wait for response
# Extract via TreeWalker (reliable; class-based selectors often fail)
result = send_cmd("Runtime.evaluate", {
    "expression": """
    (function() {
        var text = '';
        var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        while(walker.nextNode()) {
            var t = walker.currentNode.textContent.trim();
            if(t.length > 5 && t.length < 1000) text += t + '\\n';
        }
        return text.substring(0, 15000);
    })()
    """,
    "returnByValue": True
})
ws.close()
```

**When to use this over delegate_task**: Direct CDP is faster (no agent spawning overhead) and works when browser tools are functional in cron but the page has navigation issues, non-standard DOM, or unreliable class-based element selectors. Use delegate_task when you need multi-step reasoning or when CDP itself is unavailable.

## Common DOM Selector Failures

| Site | Expected selector | Reliable fallback |
|------|------------------|-------------------|
| YouTube playlists | `ytd-playlist-video-renderer` | `a.ytLockupMetadataViewModelTitle[href*="watch?v="]` |
| Gemini | `textarea` | `div.ql-editor[contenteditable="true"]` |
| Gemini response | `.message-content`, `.model-response` | TreeWalker on `document.body` |

## Known External Service Status

- **CISA.gov**: Currently (Apr 2026) offline due to US federal funding lapse — check for "lapse in federal funding" text before including CISA links
- **Tavily search API**: Returns 402/432 when quota exhausted — use browser on Google Search URLs instead
- **ACSC/cyber.gov.au**: Advisories page URL changed — verify current URL before using

## Verification

After fixing a cron job:
1. `cronjob(action='run', job_id='...')` — trigger manually
2. Wait 60 seconds
3. Check `cronjob(action='list')` — `last_run_at` should be recent
4. Verify delivery target received the content
5. If still fails: test same task via `delegate_task` manually to isolate CDP vs prompt issue
