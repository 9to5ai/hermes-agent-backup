---
name: book-to-notebooklm
description: "Complete pipeline: download any book (Anna's Archive) → upload to NotebookLM → generate ALL Studio outputs (Slide Deck + Audio Overview + Video Overview + Infographic). Also covers triggering outputs on existing notebooks. Fully self-contained."
category: productivity
tags: [Anna's Archive, NotebookLM, EPUB, PDF, download, slides, audio overview, video overview, infographic, podcast, book summary, study materials]
triggers:
  - "download a book"
  - "turn a book into slides"
  - "book to notebooklm"
  - "generate audio overview"
  - "generate video overview"
  - "generate infographic"
  - "notebooklm slide deck"
  - "notebooklm podcast"
  - "study materials from book"
  - "book summary notebooklm"
---

# Book to NotebookLM — End-to-End Workflow

Receive a book name, screenshot, or description → download from Anna's Archive → upload to NotebookLM → generate all Studio outputs. This is the umbrella workflow for book acquisition plus NotebookLM transformation. The former standalone `anna-archive-book-download` skill is preserved in `references/anna-archive-book-download.md` for detailed mirror/countdown/curl troubleshooting. The legacy Playwright-only upload approach (from the archived `notebooklm-automation.md`) is preserved in `references/archived-notebooklm-automation.md` — not needed for current sessions but available if debugging older session artifacts.

## Workflow Overview

```
User says: "download [Book] by [Author] and make me slides"
    │
    ▼
1. Anna's Archive download
    └── Saves EPUB/PDF to ~/Downloads/
    │
    ▼
2. NotebookLM upload + all 4 Studio outputs
    ├── 🎠 Slide Deck
    ├── 🎧 Audio Overview
    ├── 🎬 Video Overview
    └── 🗺️ Infographic
    │
    ▼
3. Return notebook URL to user (to the current thread, NOT DMs)
```

## Step 1: Download from Anna's Archive

**Anna's Archive domains (in order):** annas-archive.gd → annas-archive.pk → annas-archive.gl

**Anna's Archive DDoS-Guard (critical):** Anna's Archive uses DDoS-Guard which actively blocks automated downloads. Workarounds in order of preference:

1. **CDN direct curl (fastest):** Search results sometimes expose a CDN URL like `https://momot.rs/d3/<ID>`. If available, use it directly: `curl -L -o ~/Downloads/book.epub "https://momot.rs/d3/<ID>"`. This bypasses the entire slow-download flow.
2. **Browser slow download (reliable):** Navigate to the MD5 page → click Slow Partner #N → wait 15s → extract download URL from DOM before redirect → `curl -L -o` the file.
3. **Manual fallback:** Ask user to open `https://annas-archive.gd/md5/<MD5>` manually and download to `~/Downloads/`

If all Anna's Archive domains fail, try:
- **Library Genesis mirrors:** `libgen.is`, `libgen.li`, `libgen.rocks` — search by exact MD5 or filename from the search results (e.g. `lgli/Superagency_-_Reid_Hoffman.epub`)
- **Dokumen.pub:** Often has recent books but requires JS — try Playwright navigation
- **oceanofpdf.com:** Search by book title; usually has direct download links accessible via curl

**Key rules:**
- Slow download is preferred — Fast downloads are blocked by Google's popup blocker
- URLs expire quickly — use immediately after fetching
- If domain is blocked, try the next one (.pk, then .gl)

**Save the file path** for Step 2 (e.g. `/Users/momo/Downloads/Meltdown_Novak.epub`)

## Step 2: Upload to NotebookLM + Generate All 4 Outputs

Use Playwright connected to Chrome's existing profile via CDP.

**Prerequisites:**
- Chrome running with remote debugging: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --remote-debugging-port=9222`
- Chrome must be logged into NotebookLM (Playwright inherits existing cookies/auth)
- Playwright Python installed: `pip install playwright && playwright install chromium`

**Connection:**
```python
from playwright.sync_api import sync_playwright

# NOTE: CDP port is NOT 9222 — it's dynamically assigned per Chrome session.
# Find it with: socket.create_connection(('localhost', port), timeout=2) for port in range(9000, 9500)
# Common ports seen: 18800. Check with `lsof -i tcp:-1 | grep Chrome` or `for port in 9222 18800 3456; do curl -s --connect-timeout 1 localhost:$port > /dev/null && echo "OPEN: $port"; done`
CDP_URL = "http://localhost:18800"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0]
    page = context.pages[0]
    # ... automation code ...
    browser.close()
```

**Step 2a: Create or find notebook**
```python
# Create new notebook
page.goto("https://notebooklm.google.com")
page.wait_for_timeout(2000)
page.get_by_text("Create new notebook").click()
page.wait_for_timeout(3000)
notebook_id = page.url.split("/notebook/")[1].split("?")[0]
```

**Step 2b: Upload file**
```python
# Note: NotebookLM's file picker is a native OS dialog — NOT controllable via CDP.
# Playwright's set_input_files() bypasses it by setting the file directly on the DOM input.
page.goto(f"https://notebooklm.google.com/notebook/{notebook_id}?addSource=true")
page.wait_for_timeout(2000)
page.get_by_text("Upload files").click()
page.wait_for_timeout(1000)
page.locator('input[type="file"]').first.set_input_files("/path/to/book.epub")
page.wait_for_timeout(6000)  # server-side processing
assert 'source' in page.inner_text('body'), "Upload may have failed"
```

**Upload approach — CRITICAL UPDATE (2026-05):** The skill's previous `set_input_files()` approach on `input[type="file"]` does NOT work. NotebookLM uses a custom Angular uploader (`xapscottyuploadertrigger`) that completely bypasses the standard browser file input mechanism. The `filechooser` event never fires. `set_input_files()` on any `<input type="file">` element silently fails — the upload never starts. **No programmatic workaround exists** as of this session. The user must drag-and-drop or use the OS file picker manually.

**Workaround — connect Playwright to Chrome and navigate, but leave upload to the user:**
```python
# Create notebook via CDP JS injection
script = """
(() => {
    const btn = document.querySelector('.create-new-button');
    if(btn) { btn.click(); return 'Clicked'; }
    return 'Not found';
})()
"""
result = page.evaluate(script)
# Read the new URL from browser
notebook_url = page.url  # contains the new notebook ID
```

Then tell the user to drag the EPUB onto the notebook page. This is the ONLY reliable path as of 2026-05.
**Step 2c: Generate all 4 Studio outputs** (always do all 4, never skip any)

⚠️ **Critical timing rule:** Studio buttons are disabled while the source is "indexing." This can take 3–8 minutes after upload. You MUST poll and wait. Checking via CDP is more reliable than browser_snapshot:

```python
# Check button state via CDP (target_id = NotebookLM page target)
script = """
(() => {
    const containers = Array.from(document.querySelectorAll('.create-artifact-button-container'));
    return containers.map(c => {
        const label = c.getAttribute('aria-label') || '';
        return label + ' | disabled=' + c.classList.contains('disabled-tile');
    }).join('\\n');
})()
"""
result = page.target_id  # use the CDP target for the NotebookLM page
# Then use browser_cdp tool with Runtime.evaluate on that target
```

If all buttons show `disabled=true`, keep polling every 15s. When `disabled=false`, all outputs are ready to trigger simultaneously.

```python
import time

def wait_for_indexing(page, notebook_id, timeout=480, interval=15):
    """Wait until Studio buttons are enabled (source has finished indexing)."""
    page.goto(f"https://notebooklm.google.com/notebook/{notebook_id}")
    page.wait_for_timeout(3000)
    start = time.time()
    while time.time() - start < timeout:
        # Expand studio panel first if needed
        expand_btn = page.get_by_text("Expand studio panel")
        if expand_btn.count() > 0:
            expand_btn.click()
            page.wait_for_timeout(1000)
        # Check if Slide Deck button is enabled (not disabled-tile)
        slide_btn = page.locator('.create-artifact-button-container', has_text='Slide Deck')
        if slide_btn.count() > 0 and 'disabled-tile' not in (slide_btn.first.get_attribute('class') or ''):
            return True
        print(f"  Still indexing... ({int(time.time()-start)}s elapsed)")
        time.sleep(interval)
    raise TimeoutError(f"Source never finished indexing after {timeout}s")
```

```python
# 1. Wait for indexing (buttons must be enabled first)
wait_for_indexing(page, notebook_id)

# 2. 🎠 Slide Deck — triggers immediately
page.get_by_role("button", name="Slide Deck", exact=True).click()
page.wait_for_timeout(1000)

# 3. 🎧 Audio Overview — triggers immediately (Escape if customize dialog opens)
page.get_by_role("button", name="Audio Overview", exact=True).click()
page.wait_for_timeout(500)
if page.locator('[role="dialog"]').count() > 0:
    page.keyboard.press("Escape")
page.wait_for_timeout(500)

# 4. 🎬 Video Overview — opens customize dialog → click Generate
page.get_by_role("button", name="Video Overview", exact=True).click()
page.wait_for_timeout(500)
page.get_by_role("button", name="Generate", exact=True).click()
page.wait_for_timeout(1000)

# 5. 🗺️ Infographic — triggers immediately
page.get_by_role("button", name="Infographic", exact=True).click()
page.wait_for_timeout(1000)

# Verify all 4 started
body = page.inner_text('body')
for output in ["Slide Deck", "Audio Overview", "Video Overview", "Infographic"]:
    assert output in body, f"{output} not found — may not have triggered"
print("All 4 outputs generating!")
notebook_url = f"https://notebooklm.google.com/notebook/{notebook_id}"
```

**Re-triggering on an existing notebook:** If the source was already uploaded and indexed, go straight to the notebook URL, expand the Studio panel, and trigger all 4 outputs. If buttons are still disabled, the source may have been added but not fully processed — use `wait_for_indexing()` above.

**Triggering Video Overview with custom format:** After clicking "Video Overview" → select format (Cinematic/Explainer/Brief) → optionally type a focus prompt → then click "Generate."

## Step 3: Report to User

Send the user in the **current thread** (NOT DMs):
- The **notebook URL**
- Confirmation that all 4 outputs are generating: 🎠 Slide Deck, 🎧 Audio Overview, 🎬 Video Overview, 🗺️ Infographic
- The book name and author
- Remind them all 4 generate asynchronously — check the Studio panel in a few minutes

## Handling Ambiguous Book Names

If the user says "download The Great Gatsby" without an author:
1. Search Anna's Archive for the title
2. If multiple results appear, prefer the most well-known edition / classic literature
3. If still ambiguous, show the top 3 results and ask the user to confirm

## Handling Image Input (Book Screenshot)

If the user sends an **image** of a book cover:
1. Use `vision_analyze` to extract the book title and author
2. Proceed with Anna's Archive download using the extracted name
3. Verify with user if the extracted name looks wrong

## File Format Handling

- **EPUB**: Upload directly to NotebookLM (supported)
- **PDF**: Upload directly to NotebookLM (supported)
- **Other formats**: Convert first using Calibre CLI (`brew install calibre`) or mention the format isn't supported

## Key Implementation Notes

- **Anna's Archive domains**: If `annas-archive.gd` is blocked, try `.pk` then `.gl`
- **Slow download is required** — Fast downloads are often blocked by Google's popup blocker; slow partner always works
- **Wait 15 seconds** on the countdown page before the download URL appears
- **curl with `-L`** follows redirects — the actual file URL is behind a redirect
- **NotebookLM supports EPUB and PDF natively** — no conversion needed
- **Chrome CDP port:** Must be running — find it first: `for port in 9222 18800 3456 9223; do curl -s --connect-timeout 1 localhost:$port > /dev/null && echo "OPEN: $port"; done`. Current known port is **18800**, not 9222.

## Error Handling

| Scenario | Action |
|----------|--------|
| Anna's Archive DDoS-Guard blocks slow download | Try CDN direct URL from search results first (`curl -L -o`); else browser slow download via Playwright |
| Anna's Archive CDN URL found in page DOM (e.g. `93.123.118.12:6060/...` via slow download) | **curl to CDN direct URLs returns 403 Forbidden** — the CDN blocks non-browser requests even with correct User-Agent. Do NOT rely on curl for these. Use the browser slow-download flow instead: navigate to `slow_download` page in Playwright → wait for countdown → extract URL → verify the download starts. |
| CDN URL returns 404 or redirect to Anna's homepage | Fall back to Playwright slow-download browser flow |
| CDN URL returns 404 or redirect to Anna's homepage | Fall back to Playwright slow-download browser flow |
| CDP connection refused on port 9222 | Port is dynamically assigned — find with: `for port in 9222 18800 3456; do curl -s --connect-timeout 1 localhost:$port && echo "OPEN: $port"; done`. Current known port is **18800**, not 9222 |
| No search results found | Try alternate spellings, or year in search query |
| Download URL expired | Re-fetch from Slow Partner (URLs expire quickly) |
| curl download times out | Resume with `curl -C -`; slow partners can be very slow |
| NotebookLM upload fails | Retry once — server-side processing may have been slow |
| Studio buttons disabled after upload | Source is still indexing — use `wait_for_indexing()` (3–8 min). Re-check periodically |
| Book not in Anna's Archive | Try oceanofpdf.com (has direct download links accessible via browser navigation — curl returns static HTML only, download requires JS rendering), libgen.li, libgen.is, or dokumen.pub |
| Image of book sent | Use vision_analyze first to extract title/author |

## Complete One-Shot Prompt (for cron or delegation)

```
Download "[Book Name] by [Author]" from Anna's Archive (annas-archive.gd or annas-archive.pk),
convert to EPUB if needed, upload to NotebookLM, and generate all 4 Studio outputs:
🎠 Slide Deck, 🎧 Audio Overview, 🎬 Video Overview, 🗺️ Infographic.
File path: ~/Downloads/[BookName].epub
Return the notebook URL when done (to the current thread, NOT DMs).
```
