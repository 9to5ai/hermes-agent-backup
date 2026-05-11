---
name: browser-tools
description: Use when debugging browser automation, Chrome DevTools Protocol (CDP), cron browser failures, dynamic-page DOM extraction, image/link verification, or browser-backed web app QA. Covers direct CDP, browser tool fallbacks, and session quirks.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [browser, cdp, chrome, debugging, cron, links, images, qa]
    related_skills: [hermes-agent, scheduled-digest-automation]
---

# Browser Tools

## Overview

Use this umbrella for Hermes browser automation and Chrome/CDP troubleshooting. It covers the general class of failures where normal browser tools, CDP ports, dynamic DOM selectors, popups, or deployed link/image verification are the limiting factor.

The former `hermes-cron-browser-debugging` skill has been demoted to `references/hermes-cron-browser-debugging.md`; load that reference for the full cron-specific failure taxonomy and delegate-task workaround.

## When to Use

- A browser task fails because refs are stale, clicks are blocked, or the DOM differs from the accessibility snapshot.
- CDP connection details matter: port `9222` vs `18800`, `/json` targets, raw protocol calls, or websocket behavior.
- A cron job that uses browser/search tools returns empty output or silently succeeds.
- A deployed site needs visual, link, or image verification.
- Dynamic pages require fallback extraction via direct DOM, TreeWalker, or screenshot/vision.

## CDP Connection Triage

1. Check which Chrome debugging port is live:

```bash
lsof -nP -iTCP -sTCP:LISTEN | grep -E 'Chrome|9222|18800'
curl -s http://127.0.0.1:18800/json | head
curl -s http://127.0.0.1:9222/json | head
```

2. Prefer Hermes `browser_cdp` when available for targeted protocol calls.
3. If writing direct Python CDP clients, `websocket-client` may need `suppress_origin=True` when attaching to Chrome's `webSocketDebuggerUrl`.
4. Browser-level CDP methods omit `target_id`; page-level methods need the tab target ID; OOPIFs may need `frame_id` routing.

## Browser Tool Fallback Ladder

Use the lightest working tool first, then escalate:

1. `browser_snapshot(full=false)` for interactive refs.
2. `browser_snapshot(full=true)` for page text extraction.
3. `browser_vision(annotate=true)` when modals/visual layout are missing or stale in the accessibility tree.
4. `browser_console(expression=...)` for DOM inspection or custom extraction.
5. `browser_cdp` for raw protocol navigation, input, screenshots, and dialog handling.
6. Direct CDP from `terminal()` if cron/tool wrappers are the problem.
7. Delegate to a browser-capable subagent if the cron sandbox lacks browser/CDP access.

## Cron Browser Failures

Symptoms often include `cronjob(action='run')` reporting success while output is empty, `last_run_at` not updating as expected, or browser tool calls returning no useful page state.

Known causes:

- CDP/browser unavailable in the cron sandbox.
- Search/extract provider quota failures causing empty source sets.
- The cron prompt lets the model complete without actually calling tools.
- Dynamic sites changed selectors or render response text behind UI toggles.

Reliable fixes:

- Make the cron prompt self-contained and tool-mandatory.
- Use direct feeds (`curl`, RSS/JSON) where possible.
- Spawn `delegate_task(toolsets=['browser', ...])` for browser-heavy work.
- Verify with a manual cron run and delivery/output check.

See `references/hermes-cron-browser-debugging.md` for detailed recipes and site-specific selectors.

## Dynamic DOM Extraction

Avoid assuming one stable selector on rich web apps. Prefer:

- First inspect visible text with full snapshot.
- Use `document.querySelectorAll(...)` only after confirming selectors in the live page.
- For generated responses, TreeWalker can recover text when containers are unstable, but validate that output is real content rather than CSS/script scaffolding.
- For text editors, contenteditable elements may replace `textarea`.

## Link and Image Verification

- Verify external links after deployment by navigating and checking final URL/status/visible content.
- For visual proof, capture screenshots via browser/CDP or use `browser_vision`.
- When using Unsplash images in web projects, append params such as `?w=800&q=80` for consistent loading and smaller payloads.
- Do not claim a deployment works until at least the production URL and key outbound links have been checked.

## Verification Checklist

- [ ] Confirmed the active Chrome/CDP endpoint and target tab.
- [ ] Refreshed snapshots after every modal/navigation-changing click.
- [ ] Used vision/CDP fallback when refs were stale or blocked.
- [ ] Verified extracted text is real page content, not scaffolding.
- [ ] For cron fixes, manually ran the job and checked delivered/final output.
- [ ] For deployed sites, verified production URL, major links, and key images.
