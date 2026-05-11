---
name: playlist-watcher
description: Watch a YouTube playlist for new videos, fetch Gemini summaries, and post detailed notes to Telegram. Triggered by a cron job or on-demand via "run it now".
category: productivity
tags: [youtube, gemini, telegram, playlist, automation]
tools: [browser, terminal, send_message, execute_code]
---

# Playlist Watcher

Watch a YouTube playlist for new videos, generate **full detailed notes** via Gemini, and post to Telegram — no truncation.

## Workflow

## Operational notes learned from browser-only cron runs

### ⚠️ ALWAYS use yt-dlp for playlist enumeration first

**YouTube's browser DOM only loads ~100 videos even when the playlist has hundreds.** Every browser-based enumeration technique described below (DOM queries, `ytInitialData` extraction, scroll-and-reload tricks) is fundamentally unreliable for large playlists — YouTube lazy-loads in batches and the browser will *never* see videos beyond the first ~100 items. The cron job was failing silently because it kept reporting "0 new videos" from an incomplete browser DOM.

**Primary method for getting the full playlist:**
```bash
yt-dlp --flat-playlist --print id "https://www.youtube.com/playlist?list=PL7p-a4kuEU_tpR4DxY02x3KqIotrXqucg"
```
This is the ONLY reliable way to enumerate all videos. Use it for every comparison against the tracker.

**Browser-based playlist enumeration is a last resort** — only if `yt-dlp` is unavailable. Even then, do NOT conclude "no new videos" from a partial browser DOM. Scroll tricks (100→200→etc.) are unreliable and the scroll count needed changes unpredictably.

- If the normal `browser_*` tools fail with a stale CDP endpoint such as `localhost:9222`, check for an existing Chrome remote debugging port with `lsof -nP -iTCP -sTCP:LISTEN | grep -E 'Chrome|18800|9222'`. In this environment, the usable Chrome session has often been `http://127.0.0.1:18800` rather than `9222`.
- You can drive that Chrome directly from Python via `/json/new?...` and `websocket-client`. Chrome may reject the WebSocket unless the client suppresses the Origin header:
  ```python
  from websocket import create_connection
  ws = create_connection(tab['webSocketDebuggerUrl'], timeout=10, suppress_origin=True)
  ```
- **⚠️ WebSocket URL changes after `Page.navigate`**: If using raw CDP Python scripts, the tab's `webSocketDebuggerUrl` changes after every navigation. Re-fetch the tab list via `/json` after each `Page.navigate` to get the fresh WebSocket URL — the old URL becomes stale and all subsequent CDP commands will fail silently (0-char responses, no errors).
- In cron runs, prefer running the direct-CDP Python script with `terminal()` rather than `execute_code()` if `import websocket` fails. `websocket-client` may be installed in the user's site-packages and visible to `/usr/bin/python3` in `terminal`, while the `execute_code` sandbox may not see it even after `pip install --user websocket-client`.

Load `/Users/momo/.hermes/cron/output/playlist_watcher_log.json` and find IDs not yet in `processed_videos`.

### Step 3 — Gemini summarization

Open Gemini at `https://gemini.google.com/app` and use this exact prompt:

```
Write the most detailed notes about this video: https://www.youtube.com/watch?v={video_id}
```

**IMPORTANT: Always use "Write the most detailed notes about this video:" — NOT "Summarize in 3-5 bullet points". The user wants full Gemini output, no condensing.**

#### Confirmed-working Gemini input approach (2026)

The Gemini page at `gemini.google.com/app` uses a `div.ql-editor` for focus but submission goes through the visible textbox. Use this exact sequence:

1. **Navigate** to `https://gemini.google.com/app`
2. **Type** the prompt using `browser_type` on the main textbox (`textbox "Enter a prompt for Gemini"`)
3. **Click** the Send button (ref `eN` with `button "Send message"`)
4. **Wait ~45-60 seconds** for the full response to generate

Note: CDP `Input.insertText` and `Runtime.evaluate` on this Chrome session (port 18800) do NOT work reliably — use `browser_type` + click instead.

#### ⚠️ The "Show thinking" State — Critical

After submission, Gemini may show a "Show thinking" button in the response area. **The actual response is HIDDEN behind this thinking block.** The `div.response-content` DOM query will only return the thinking-phase text (e.g. "Assessing the Task"), NOT the actual notes.

**You MUST click "Show thinking" to reveal the full response:**

```javascript
// Find and click "Show thinking" button
var buttons = document.querySelectorAll('button');
for (var i = 0; i < buttons.length; i++) {
  var b = buttons[i];
  if (b.innerText && b.innerText.includes('Show thinking')) {
    b.click();
    return 'Clicked Show thinking';
  }
}
```

After clicking, wait 5 seconds, then take a `browser_snapshot` — the full notes will now be visible with headings, bullets, and paragraphs.

#### Extracting Gemini's response

After revealing "Show thinking", use `browser_snapshot` (full=true) as the primary extraction method. The snapshot preserves all headings (`##`), bullet structure, and paragraphs.

**DOM querying is unreliable as a primary method** because:
- `div.response-content` only returns the thinking-phase text until "Show thinking" is clicked
- TreeWalker approaches return script/CSS noise mixed with actual content
- The response does not live in any stable container selector

Only fall back to DOM queries if `browser_snapshot` is unavailable, and always validate that the result contains recognizable content (timestamps like `[00:01:21]`, actual paragraphs about the video topic) rather than HTML scaffolding.

### Step 4 — Post to Telegram

Send to `telegram:-1003966589836:2` (Momo's Home thread 2). Format:
- **Bold title** + hyperlink: `**Title** ([YouTube](https://www.youtube.com/watch?v={id}))`
- Body: Gemini's full output verbatim — do NOT truncate, do NOT summarize
- Preserve headings (`##`), bullet structure, and paragraph breaks exactly as Gemini returns them

### Step 5 — Update tracker

After posting, add the video ID to the tracker:

```python
python3 -c "
import fcntl, json
lf = open('/Users/momo/.hermes/cron/output/playlist_watcher.lock', 'w')
fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
with open('/Users/momo/.hermes/cron/output/playlist_watcher_log.json') as f: d = json.load(f)
if '{video_id}' not in d.get('processed_videos',[]):
    d['processed_videos'].append('{video_id}')
    with open('/Users/momo/.hermes/cron/output/playlist_watcher_log.json','w') as f: json.dump(d,f,indent=2)
    print('ADDED')
else: print('EXISTS')
fcntl.flock(lf.fileno(), fcntl.LOCK_UN); lf.close()
"
```

### Step 6 — Wait 3 seconds between videos

Use `time.sleep(3)` between each video to avoid rate limiting.

## Gemini Prompt Template

```
Write the most detailed notes about this video: https://www.youtube.com/watch?v={video_id}
```

## Tracker file

`/Users/momo/.hermes/cron/output/playlist_watcher_log.json`

Lock file: `/Users/momo/.hermes/cron/output/playlist_watcher.lock`

## Telegram target

`telegram:-1003966589836:2`

## Playlist ID

`PL7p-a4kuEU_tpR4DxY02x3KqIotrXqucg` (Momo playlist)
