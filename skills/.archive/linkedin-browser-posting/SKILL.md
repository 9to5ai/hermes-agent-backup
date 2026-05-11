---
name: linkedin-browser-posting
description: Post, verify, and troubleshoot LinkedIn feed posts using the logged-in browser session
---

# LinkedIn Browser Posting

Use this skill when the user asks to post something on LinkedIn, publish a LinkedIn update, or corrects an ambiguous “post this” request to mean LinkedIn.

## Core workflow

1. Open LinkedIn feed in the active browser session:
   - `browser_navigate(url='https://www.linkedin.com/feed/')`
2. Confirm the user is logged in and identify the active profile/account from the feed header or composer.
3. Click **Start a post**.
4. Fill the composer textbox with the user-provided content exactly unless the user asks for editing.
5. Check audience if visible; default is usually **Post to Anyone**.
6. Click the enabled **Post** button.
7. Verify success before responding:
   - Look for a toast/alert such as **Post successful** and/or **View post**.
   - Capture and return the LinkedIn post URL if available.

## Important pitfalls

- Do **not** conclude that “no LinkedIn integration is available” just because there is no dedicated LinkedIn API tool. The logged-in browser session can post manually through LinkedIn Web.
- If the user says only “Post this” in a social-posting context, do not assume Telegram. If the target is ambiguous, use the prior context if it indicates a platform; if the user corrects “LinkedIn,” switch to LinkedIn immediately.
- LinkedIn modals may be invisible or stale in `browser_snapshot` after a click. Use `browser_vision(annotate=true, ...)` to confirm the composer, textbox, and Post button coordinates/refs.
- `browser_click` can fail with “blocked by another element” when refs are stale. Refresh with `browser_snapshot(full=true)` or `browser_vision`, then click the currently annotated Post button.
- Long pasted posts may shift the composer vertically; the Post button can remain visible near the bottom even when the textbox extends upward/offscreen.
- LinkedIn may rewrite external URLs into `lnkd.in` links and attach a link preview; this is expected. Verify the visible post includes the link or preview.
- If CAPTCHA, login, or account-selection prompts appear, stop and ask the user to complete them unless the action is clearly safe and already authenticated.

## Verification output

Final response should be short:

```text
Posted on LinkedIn ✓

<post URL>
```

If posted but URL is unavailable, say it was posted and mention that no View post URL was exposed.

## Reference notes

- See `references/linkedin-posting-browser-session-2026-05-03.md` for a concrete successful browser-posting trace and quirks observed in the composer UI.
