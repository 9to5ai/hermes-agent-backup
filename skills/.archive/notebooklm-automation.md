# NotebookLM Automation

Upload files to NotebookLM and generate slide decks using Playwright connected to Chrome's existing profile via CDP.

## Key Discovery

NotebookLM's file upload button triggers a **native OS file picker** (`<input type="file">`) inside a `<dialog>` element. This is NOT controllable via Chrome DevTools Protocol (CDP) alone — `Page.setFileInputFiles` requires a DOM node ID that can't be obtained cross-frame, and native dialogs are outside CDP's reach.

**Solution:** Use Playwright Python with `set_input_files()` — this directly sets the file on the input DOM element, bypassing the OS file picker entirely.

## Prerequisites

1. Chrome must be running with remote debugging enabled:
   ```
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   ```
   Or simply navigate to `chrome://inspect` and enable port forwarding.

2. Playwright Python library installed:
   ```
   pip install playwright && playwright install chromium
   ```

## Connection Setup

```python
from playwright.sync_api import sync_playwright

CDP_URL = "http://localhost:9222"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0]  # Main browser context (preserves cookies/auth)
    page = context.pages[0]       # Active tab
    # ... automation code ...
    browser.close()
```

## Workflow

### Step 1: Find or Create Target Notebook

List notebooks at `https://notebooklm.google.com` — the snapshot contains notebook links with IDs in their URLs (`/notebook/{UUID}`).

For a **new** notebook:
1. Click `Create new notebook` button
2. Wait for redirect to new notebook URL
3. Extract the notebook ID from `page.url`

For an **existing** notebook, use its UUID directly.

### Step 2: Upload File

```python
# Navigate to notebook with addSource=true dialog open
page.goto(f"https://notebooklm.google.com/notebook/{NOTEBOOK_ID}?addSource=true")
page.wait_for_timeout(2000)

# Click "Upload files" button
page.get_by_text("Upload files").click()
page.wait_for_timeout(1000)

# Find the file input and set the file (bypasses native OS file picker)
file_input = page.locator('input[type="file"]').first
file_input.set_input_files("/path/to/file.epub")

# Wait for upload + processing
page.wait_for_timeout(5000)

# Verify upload by checking "1 source" appears
body = page.inner_text('body')
assert '1 source' in body, "Upload may have failed"
```

**Supported file types:** PDF, EPUB, DOCX, TXT, MP3, WAV, MP4, YouTube URLs, websites.

### Step 3: Generate Slide Deck

```python
# Navigate to notebook (without ?addSource)
page.goto(f"https://notebooklm.google.com/notebook/{NOTEBOOK_ID}")
page.wait_for_timeout(3000)

# Expand Studio panel if not already open
expand_btn = page.get_by_text("Expand studio panel")
if expand_btn.count() > 0:
    expand_btn.click()
    page.wait_for_timeout(1000)

# Click "Slide Deck"
page.get_by_text("Slide Deck").click()
page.wait_for_timeout(1000)

# Confirm generation started
body = page.inner_text('body')
assert 'Generating' in body, "Slide deck generation did not start"
print("Slide deck generation started — check Studio panel for completion")
```

### Step 4: Download/Access Generated Slides

The generated slide deck appears in the Studio panel. NotebookLM provides:
- In-browser slide viewer
- Export options (may vary by content type)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Page.setFileInputFiles` not found in CDP | Normal — CDP's file input method requires node IDs not accessible cross-frame. Use Playwright instead. |
| Native file picker appears despite `set_input_files` | Use `page.locator('input[type="file"]').first.set_input_files()` — this targets the DOM element directly, not CDP. |
| File upload silently fails | Check `page.inner_text('body')` for '1 source'. If missing, the file may be unsupported or too large. |
| Playwright connects but page shows "Loading" | Add `page.wait_for_timeout(3000)` after navigation. NotebookLM is a heavy SPA. |
| Auth required / redirected to login | Playwright inherits Chrome's cookies from the existing profile — ensure Chrome was logged into NotebookLM. |
| `context.pages[0]` is wrong tab | Iterate `context.pages` to find the correct URL, or call `context.new_page()` for a fresh tab. |
| `osascript` commands hang / timeout | AppleScript for native dialog control is NOT needed — use Playwright `set_input_files()` instead. |

## Key Implementation Notes

- **Never try to control the native OS file picker via AppleScript or CDP.** The native dialog is spawned by the browser's renderer process and is outside CDP's reach.
- **Playwright + Chrome CDP = full automation** — Playwright's `set_input_files()` works because it manipulates the DOM directly, not the OS dialog.
- **The `?addSource=true` URL param** opens the "Add source" dialog on page load — useful for ensuring the dialog is present.
- **Wait after file set** — NotebookLM uploads to Google's servers and then processes/embeds. Wait 5+ seconds before checking for source count.
- **Studio generation is async** — Once "Generating Slide Deck..." appears, the task runs server-side. Check Studio panel manually or poll every 30s.
