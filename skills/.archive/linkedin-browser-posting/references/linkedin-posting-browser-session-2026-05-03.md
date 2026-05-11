# LinkedIn browser posting trace — 2026-05-03

## Scenario

User asked to post a long research commentary on LinkedIn. Earlier assistant mistakenly treated an ambiguous “Post this” as Telegram and later claimed no LinkedIn integration existed. Actual successful route was through the logged-in LinkedIn browser session.

## Successful steps

1. Navigated to `https://www.linkedin.com/feed/`.
2. Confirmed logged-in account: Momo Fan.
3. Clicked **Start a post**.
4. `browser_snapshot` initially did not clearly show the modal, but `browser_vision(annotate=true)` confirmed composer UI:
   - textbox: “Text editor for creating content”
   - audience: “Post to Anyone”
   - Post button initially disabled until text entered
5. Typed the full post into the composer textbox.
6. After typing, `browser_click` on an older Post ref failed as blocked/stale.
7. Used `browser_vision` and then `browser_snapshot(full=true)` to identify the enabled blue Post button.
8. Clicked the current Post ref successfully.
9. Verified toast: “Post successful. View post”.
10. Returned URL: `https://www.linkedin.com/feed/update/urn:li:share:7456687142652772352/`.

## UI quirks observed

- Snapshot refs can lag behind modal state. Vision annotations were more accurate for the composer.
- Long content made the editor area extend upward/offscreen, but the Post button stayed at the lower-right of the modal.
- LinkedIn rewrote the arXiv URL into a `lnkd.in` short link and attached an arxiv.org preview.

## Behavioral lesson

For Jun, if a message says “post this” and the context is public/social content, avoid defaulting to Telegram unless the target is explicit. If corrected to LinkedIn, use the browser session rather than claiming no integration exists.
