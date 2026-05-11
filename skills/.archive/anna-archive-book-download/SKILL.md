---
name: anna-archive-book-download
description: Download a book from Anna's Archive (annas-archive.gd) end-to-end — search, wait for slow download countdown, extract URL, and download via curl. Works even when browser blocks popups.
triggers:
  - download a book from anna archive
  - anna's archive slow download
  - download ebook annas archive browser
---

## Anna's Archive Book Download Workflow

### Step 1: Navigate to the correct domain
Try these domains in order — use the first one that loads successfully:
1. `https://annas-archive.gd`
2. `https://annas-archive.pk`
3. `https://annas-archive.gl`

If all are blocked/DNS-hijacked, the ISP is blocking Anna's Archive at the DNS level — change DNS to 8.8.8.8 or use a VPN.

### Step 2: Search for the book
1. Go to `https://annas-archive.gd`
2. Click **Search** in the nav
3. Type the book name + author in the search input (name="q")
4. Submit the form (press Enter or submit via JS)
5. Wait for results to load (2 results = Z-Library match found)

### Step 3: Click the correct result
- The first result with the matching book name is usually correct.
- If results are ambiguous, verify by author name (e.g., "Lauren Novak").
- Click the link to go to the book's MD5 page.

### Step 4: Find slow downloads section
On the book's page:
1. Scroll down past the "🚀 Fast downloads" section
2. Find the **"🐢 Slow downloads"** section
3. Click **"Slow Partner Server #1"** (or any slow partner)

### Step 5: Handle the countdown page
The slow download page requires a **15-second wait**. After waiting:
1. A **"📚 Download now"** link appears
2. The actual download URL is in the `href` of this link (format: `https://wbsg8v.xyz/...`)

If **Slow Partner #1** doesn't show a working download link, try **#2, #3, etc.** — each is a different mirror and one may work when others don't.

### Step 6: Download via curl (NOT browser popup)
The browser will likely block the file download as a popup. Use curl instead:
```bash
curl -L -o ~/Downloads/<BookName>.epub "<DOWNLOAD_URL>" \
  --max-time 180 \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
```

**If the download times out or is slow**, resume with:
```bash
curl -L -C - -o ~/Downloads/<BookName>.epub "<DOWNLOAD_URL>" \
  --max-time 300 \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
```
The `-C -` flag resumes from where the previous attempt left off. Slow Partner servers can be very slow (5-15 KB/s) — set `--max-time` generously (300+ seconds) and be ready to resume.

### Step 7: Verify the file
```bash
file ~/Downloads/<BookName>.epub
unzip -l ~/Downloads/<BookName>.epub | head -5
```
A real EPUB will show `EPUB document` from `file` and `mimetype` from unzip. File sizes vary widely (0.5MB–20MB+).

### Troubleshooting
- **DNS hijacking to spam/trading sites**: Use `annas-archive.gd` specifically (not `.org`). If that fails try `.pk` and `.gl`. If all fail, change DNS to 8.8.8.8 or use a VPN.
- **No slow downloads section visible**: Scroll down — it appears after the fast download options
- **"Download Now" link not appearing or URL broken**: Try Slow Partner #2, #3, etc. — different mirrors work on different days
- **curl times out or is very slow**: Use `curl -C -` to resume from where it left off. Slow Partner servers can do 5-15 KB/s — use `--max-time 300` and be patient.
- **curl returns HTML (not EPUB)**: Download URL may have expired — go back to Step 4 and get a fresh URL.
- **File is HTML (not EPUB)**: URL returned a redirect page — ensure the `Download now` link URL is used directly, not a redirect chain
