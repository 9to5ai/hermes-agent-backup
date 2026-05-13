---
name: linkedin-posting
description: Use when Jun asks to post text on LinkedIn. Opens LinkedIn in the browser, drafts the post in the composer, publishes it, and returns the post URL after verifying success.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [linkedin, social-media, browser, posting]
    related_skills: [browser-tools]
---

# LinkedIn Posting

## Overview

Use this skill when Jun asks to post text on LinkedIn. The working setup is a logged-in Chrome/LinkedIn browser session, so use browser automation rather than claiming no integration is available.

The goal is to publish exactly the requested text, verify LinkedIn reports success, and return the resulting post link.

## When to Use

- Jun says “post this on LinkedIn,” “help me post this on LinkedIn,” or similar.
- Jun provides LinkedIn post copy in the chat.
- Jun corrects a mistaken Telegram/X posting attempt and clarifies LinkedIn.

Do not use this for:

- Posting to X/Twitter (`xurl` skill/tooling may be more relevant).
- Posting to Telegram (use `send_message`).
- Draft editing only, unless Jun explicitly asks for a rewrite before posting.

## Workflow

1. **Resolve the draft text** — If Jun says "post draft 3" without pasting text, recover it:
   - Cron job output lives at `~/.hermes/cron/output/{job_id}/`.
   - Jobs are named after their job ID; the active morning-arXiv job is `3230060441fd`.
   - Output files are named `YYYY-MM-DD_HH-MM-SS.md` — use the latest.
   - Use `read_file` with a large `offset` (e.g. 900+) or `search_files` with patterns like `Draft 3`, `[DRAFT 3/3`, or key topic words to locate the post text inside the file.
   - Fallback: search past sessions with `session_search` using topic keywords from the draft.

2. **Open LinkedIn feed**
   - Navigate to `https://www.linkedin.com/feed/` with `browser_navigate`.
   - Confirm the page is logged in and shows the feed/profile. If it asks for login, tell Jun login is required.

3. **Open the composer**
   - Click the `Start a post` button from the snapshot.
   - The composer modal elements (textbox, Post button) typically appear directly in the next `browser_snapshot` without needing vision analysis — refs like `Text editor for creating content` and `Post` show up in the accessibility tree. Do NOT rely on `browser_vision(annotate=true)` to locate modal elements in this setup; it returns generic text rather than page-specific annotations. Use `browser_snapshot` to find the composer refs and proceed.

3. **Enter the post text**
   - Type the exact user-supplied copy into the composer text editor.
   - The editor is often exposed as a textbox named `Text editor for creating content`.
   - Use `browser_type` on that textbox if available.

4. **Publish**
   - After typing, take a `browser_snapshot` to confirm the Post button ref is visible.
   - Click the enabled blue `Post` button in the composer.

5. **Verify and return URL**
   - Wait for/inspect the success alert.
   - Success state usually says `Post successful.` and includes a `View post` link.
   - Return the LinkedIn URL, e.g. `https://www.linkedin.com/feed/update/urn:li:share:<id>/`.
   - If the feed shows the newly created post but the success alert is gone, extract the post URL from the visible post/update link.

## Practical Notes from the Proven Run

- The browser was already logged in as `Momo Fan`.
- Composer fields seen in `browser_vision`:
  - Dismiss/X button
  - Account selector: `Momo Fan ... Post to Anyone`
  - Textbox: `Text editor for creating content`
  - Bottom-right `Post` button
- After publishing, LinkedIn showed:
  - `Post successful.`
  - `View post`
- Example returned URL:
  - `https://www.linkedin.com/feed/update/urn:li:share:7456687142652772352/`

## Common Pitfalls

1. **Assuming there is no LinkedIn integration.** There may not be a dedicated API/tool, but browser automation works when LinkedIn is logged in.

2. **Posting to Telegram by mistake.** If Jun says “post this” in reply to a draft and the destination is ambiguous, ask or infer from context. If he explicitly says LinkedIn, do not use `send_message`.

3. **Stale or blocked refs.** LinkedIn modals may not appear fully in compact snapshots. After clicking "Start a post", use `browser_snapshot` (not `browser_vision`) to find the composer textbox and Post button refs. `browser_vision` returns generic explanations rather than page-specific annotations in this setup — do not use it to locate modal elements.

4. **Clicking Post too early.** Ensure the post body is present and the Post button is enabled (blue) before clicking.

5. **Not verifying success.** Do not report completion until LinkedIn shows `Post successful`, `View post`, or the new post appears in the feed with a usable URL.

## Reference Notes

- `references/linkedin-browser-posting-skill.md` preserves the archived narrower browser-posting sibling, including concise verification-output wording and modal/vision quirks.
- `references/linkedin-posting-browser-session-2026-05-03.md` preserves a concrete successful browser-posting trace if present.
- `references/cron-draft-recovery.md` — how to recover draft text when Jun says "post draft 3" without pasting text: locate the cron output file for job `3230060441fd`, find the relevant draft section via large-offset reads or search, extract the text, then proceed to composer.

## Verification Checklist

- [ ] LinkedIn feed loaded and user is logged in.
- [ ] Composer opened.
- [ ] Exact requested text entered.
- [ ] Enabled `Post` button clicked.
- [ ] `Post successful` or equivalent visible.
- [ ] Final response includes the LinkedIn post URL.
