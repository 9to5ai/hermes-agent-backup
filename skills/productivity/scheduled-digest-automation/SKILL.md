---
name: scheduled-digest-automation
description: Use when building, running, or troubleshooting recurring Hermes digest/monitoring jobs that gather web signals, filter for relevance, and deliver concise summaries to Telegram or cron output. Covers deal monitors, morning digests, playlist watchers, and supervisory signal briefings.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cron, digest, monitoring, telegram, browser, web-search, automation]
    related_skills: [browser-tools, hermes-agent, youtube-content]
---

# Scheduled Digest Automation

## Overview

Use this as the umbrella workflow for recurring information-monitoring jobs: daily briefs, deal radars, playlist watchers, regulatory/cyber signal monitors, and other cron-driven digests. The class pattern is:

1. Define sources and freshness window.
2. Gather evidence with browser/search/terminal fallbacks.
3. Filter aggressively for user-relevant signal.
4. Render in a stable mobile-friendly format.
5. Deliver once, or return final output for cron auto-delivery.
6. Persist a small tracker only when needed to avoid repeats.

Session-specific monitors formerly stored as separate skills have been demoted to references:

- `references/daily-morning-digest.md` — Sydney morning digest: news, deals, events, venues.
- `references/coles-woolworths-daily-deals.md` — Coles/Woolworths 30%+ essentials filter and Chinese output format.
- `references/cyber-prudential-signal-briefing.md` — APRA/NFR AI-cyber supervisory signal brief format and source map.
- `references/playlist-watcher.md` — YouTube playlist → Gemini notes → Telegram workflow, including CDP/Gemini quirks.

## When to Use

- User asks for a daily/weekly digest, watchlist, monitor, morning brief, or scheduled research/reporting job.
- A cron job should scrape/search multiple sources and produce a structured summary.
- A task involves Telegram delivery of curated external information.
- A browser/search-based cron job is returning empty content, duplicate content, or too much noise.

Do not use this for one-off deep research unless the user also wants an ongoing monitor.

## Build Pattern

### 1. Define the job contract

Record these before scheduling:

- Schedule and timezone.
- Delivery target or whether cron final-response delivery handles it.
- Audience and tone.
- Freshness window.
- Must-include and must-exclude sources.
- Deduplication key: URL, video ID, product SKU, CVE, or headline hash.
- Output format with exact headings.

### 2. Source acquisition strategy

Prefer direct primary sources when possible, then web search, then browser navigation:

- Official feeds and JSON/RSS endpoints via `terminal(curl ...)` for reliability.
- `web_search` for broad discovery, but expect quota/rate-limit failures.
- `browser_navigate` or direct CDP for dynamic pages.
- Existing site-specific CLIs such as `yt-dlp` for YouTube playlist enumeration.

### 3. Filtering rules

Every digest needs explicit inclusion rules. Examples:

- Deals: minimum discount, unit-price check, availability, practical usefulness.
- News/events: recency, local relevance, avoid duplicate syndication.
- Cyber/regulatory: evidence strength, FI relevance, exploitation status, source credibility.
- Video monitors: unseen IDs only, full-notes requirement, no truncation unless requested.

If a source is noisy, report fewer high-confidence items rather than padding.

### 4. Output contract

Use stable headings and keep the final result directly deliverable. For Telegram, keep it mobile-friendly and avoid giant tables unless the user asked for them. For supervisory/professional briefs, include evidence links and confidence/gaps.

When the cron job auto-delivers the final response, do **not** call `send_message`; put the digest in the final response. Only use `send_message` when the job prompt explicitly requires an external platform target.

> **Clarification for multi-step job prompts that mix Telegram steps with auto-delivery:** Some session-specific prompts (e.g. playlist-watcher) include `send_message → target "telegram:..."` as a step even though the job itself is delivered via cron final-response. When BOTH are present in the same prompt, ignore the `send_message` call and instead output the Telegram-formatted content directly in your final response — the cron system delivers it automatically. This resolves the apparent contradiction: the per-step instruction reflects the desired Telegram *format*, not a separate delivery mechanism.

## Cron + Browser Reliability

Common failure modes:

1. `web_search`/`web_extract` quota errors or empty results.
2. Browser tools unavailable in cron sandbox.
3. CDP port mismatch: active Chrome may be on `127.0.0.1:18800` rather than `9222`.
4. Dynamic pages with stale DOM selectors.
5. Trackers that deadlock on their own lock file.
6. Browser navigation tool attaches to/reports a stale tab even after `browser_navigate` succeeds.
7. YouTube playlist DOM changes: `ytd-playlist-video-renderer` can be absent while videos are rendered under newer lockup components. **Always use `playlist_watcher_check.py check` (yt-dlp) first** — it is authoritative and has never failed.
8. Gemini CDP session dies post-submission — a known YouTube/playlist watcher failure mode. When this happens, **use `yt-dlp --write-auto-sub --sub-lang en --skip-download` to pull the VTT transcript**. Parse with the recipe in `references/playlist-watcher.md`. This is a first-class note source, not a degraded fallback.

Fallbacks:

- For YouTube playlist watchers specifically: **always run `playlist_watcher_check.py check` (yt-dlp) first before any browser DOM extraction**. The browser's `ytd-playlist-video-renderer`/`a#video-title` selectors are unreliable on newer YouTube lockup DOM and can return `[]` while videos are still present. `check` uses `yt-dlp --flat-playlist` and is the authoritative detection method.
- Use direct feeds via `curl` and parse locally.
- Spawn a browser-capable `delegate_task` subagent when the cron sandbox lacks CDP.
- Use direct CDP Python with `websocket-client` from `terminal()` when browser tools are flaky but Chrome is reachable.
- If browser navigation appears to land on the wrong page, create a fresh CDP target with `Target.createTarget`, call `Page.navigate` on that `target_id`, then evaluate against the same `target_id`.
- When tracker status only prints counts (not IDs), use the provided script's `check` mode if available as the safest comparison path; only inspect helper implementation to understand supported commands, not to bypass it.
- If a helper script's `add` command hangs/timeouts after a successful digest, suspect nested `fcntl` locking (e.g. `cmd_add()` taking the same lock before calling `save_tracker()`). Patch the helper to have a single lock owner rather than writing the JSON directly; then rerun `add` and verify with `status`/`check`.
- Verify delivery or final output before marking the job fixed.

## Tracker Pattern

Use trackers only for repeat suppression or stateful watchlists. Keep them small JSON files in `~/.hermes/cron/output/` and protect writes with `fcntl` locks.

**Implemented tracker shape** (playlist-watcher; field names differ from the ideal below):

```json
{
  "processed_videos": ["VIDEO_ID", ...],
  "last_checked": "ISO_TIMESTAMP",
  "TOTAL": 637,
  "LAST_CHECKED": "ISO_TIMESTAMP"
}
```

Key operational facts about the playlist-watcher tracker:
- `processed_videos` (not `processed_items`) — array of video ID strings.
- `TOTAL` = count of all processed IDs ever seen (cumulative, not current playlist size).
- `status` command prints only `{TOTAL, LAST_CHECKED}` — it does NOT list IDs and cannot be used to check what's new.
- `check` command compares yt-dlp output against `processed_videos` and prints `NEW|id|title` for unprocessed items — silent if nothing new. Use this as the authoritative no-new signal.
- If yt-dlp returns fewer videos than `TOTAL` (e.g. 629 vs 637), the playlist has removed entries — this is normal. Only `check`-reported items are genuinely new.

Never store sensitive source data or long generated content in a tracker; store IDs and timestamps.

## Verification Checklist

- [ ] Schedule, timezone, delivery mode, and audience are explicit.
- [ ] Sources have fallbacks when search/browser tools fail.
- [ ] Filtering rules prevent noisy padding.
- [ ] Output format is copied into the job prompt or skill reference.
- [ ] Deduplication key is defined if the job repeats.
- [ ] Manual run produces non-empty, on-format output.
- [ ] Delivery target is verified, or cron final response is sufficient.
