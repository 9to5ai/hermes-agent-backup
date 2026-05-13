# Source Surface Reference

## Overview

A "source surface" is a registered information source that the research loop queries on a defined cadence. Surfaces are registered in `vault/sources/registry.md`.

## Surface Types

### Web Search

**Tool:** `hermes_tools.web_search` + `hermes_tools.web_extract`
**Cadence:** Per run (every sweep)
**Pattern:** 3–5 targeted queries per sweep, focused on filling specific dossier gaps

Query strategy:
- Start from the dossier's "Open Questions" section — each open question should drive a query
- Don't query generically — query to confirm or refute a specific claim
- Limit: 5 results per query

Extraction:
- Use `web_extract` for blog posts, news articles, documentation
- `web_extract` often fails on Reddit — use browser navigation instead

### Reddit

**Tool:** `web_search` with `site:reddit.com` (preferred) OR `browser_navigate` + `browser_snapshot`
**Cadence:** Per run
**Subreddits to monitor:** r/SideProject, r/LocalAI, r/LocalLLaMA, r/LocalLLM, r/automation, r/IndiaAgents, r/AI_Agents, r/cybersecurity
**Focus:** AI agents, autonomous building, local AI, multi-agent systems, security incidents

**Critical finding:** `web_extract` does NOT render Reddit pages — do not rely on it for Reddit content. The reliable patterns are:

1. **`web_search` with `site:reddit.com`** (preferred) — search result snippets carry post titles and descriptions even when direct extraction fails. This is how Reddit signals were captured this session.
2. **`browser_navigate` + `browser_snapshot`** (fallback) — for direct post URLs (`reddit.com/r/subreddit/comments/postid`). Slower but renders content.
3. **`web_extract`** on Reddit — only works for direct post URLs, fails on subreddit listing pages. Do not use for listings.

What to look for:
- Novel agent patterns (OS-kernel, reversibility classification)
- Incident reports (agent loops, cost burns, data destruction)
- Security incidents involving AI agents (r/cybersecurity is a key signal source)
- Product launches and roadmaps
- Framework comparisons from real users

### X/Twitter

**Tool:** `xurl` CLI or browser navigation
**Cadence:** Per run or daily (depends on profile configuration)
**Accounts to monitor:** @gkisokay, @NousResearch, @amplifi_now
**Focus:** agent architecture, multi-agent systems, Hermes ecosystem

X can be noisy. Target specific accounts rather than running generic searches.

### GitHub

**Cadence:** Weekly (do NOT trigger on per-run cadences)
**Focus:** agent frameworks, AI agent platforms
**What to check:**
- New repos in AI agent space
- Stars/forks growth on known projects
- Issue activity on control plane projects

Before triggering GitHub, check the last GitHub sweep timestamp in the source registry.

## Cadence Rules

| Surface | Default Cadence | Override Condition |
|---------|----------------|-------------------|
| Web search | per run | always |
| Reddit | per run | always |
| X/Twitter | per run | depends on profile config |
| GitHub | weekly | only if last sweep > 7 days ago |

## Source Registry Entry Format

```markdown
### <surface_id>
- **surface_id**: <id>
- **<relevant fields>**: <value>
- **focus**: <what this surface covers>
- **cadence**: per run / daily / weekly
- **status**: active / pending / inactive
```

## Surface Activity This Run Table Format

```markdown
| Surface | Signals Captured | Status |
|---------|-----------------|--------|
| web | N results across M queries | processed |
| reddit | N posts captured | processed |
| x | brief description | not triggered / partial / processed |
| github | pending / N repos checked | weekly cadence not triggered / processed |
```
