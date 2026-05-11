---
name: daily-morning-digest
description: Compile and send a daily morning digest to Telegram — news headlines (SMH, AFR), deals (Ozbargain, Coles, Amazon), events (Eventbrite), and trending venues (Broadsheet/TimeOut). Triggered by a cron job at ~4-6 AM or on-demand.
category: productivity
---

# Daily Morning Digest

## Trigger
Run as a scheduled cron job (e.g. 4-6 AM Australia/Sydney) or on-demand. Compiles a single formatted Telegram message from multiple web sources.

## Sources & Search Strategy

| Section | Source | Search / Method |
|---|---|---|
| News — SMH | https://www.smh.com.au | Google: `site:smh.com.au latest news today` |
| News — AFR | https://www.afr.com | Google: `site:afr.com latest news today` |
| Deals — Ozbargain | https://www.ozbargain.com.au | Google: `site:ozbargain.com.au best deals today` |
| Deals — Coles | https://www.coles.com.au/catalogues | Browse catalogue pages (Baby category ID 529, Half Price ID 683) |
| Deals — Amazon Kids | https://www.amazon.com.au | Google: `site:amazon.com.au clearance kids gifts` |
| Events — Sydney | https://eventbrite.com.au | Google: `Sydney events this weekend May 2026 site:eventbrite.com.au` |
| Venues — Sydney | Broadsheet, TimeOut, SMH Good Food | Google: `new cafes restaurants Sydney opening 2026 trending` |

## Coles Catalogue Browsing
Navigate to `https://www.coles.com.au/catalogues/view#view=category&saleId=65351&categoryId=CATID&areaName=c-nsw-met` with these category IDs:
- Baby: `529`
- Half Price: `683`
- Fruit & Veg: `526`
- Meat/Seafood/Deli: `527,528,525`

## Web Scraping Notes
- `web_search` via Tavily API may return 432 errors — if so, use `browser_navigate` to Google search results instead
- Browse directly to Coles catalogue category pages for structured product data
- Amazon clearance deals appear on `amazon.com.au/clearance-kids/s?k=clearance+kids`

## Output Format (Telegram Markdown)

```
🌅 *Good morning, Jun — Daily Digest for [DATE]*

📰 *NEWS — Sydney Morning Herald*
• [Headline](URL) — 1 line context
• ...

📰 *NEWS — Australian Financial Review*
• [Headline](URL) — 1 line context
• ...

🏷️ *DEALS — Ozbargain Top Picks*
• [Deal title](URL) — $price or brief description
• ...

🛒 *DEALS — Coles 30%+ Off*
• [Item](URL) — was $X, now $Y (% off)
• ...

🎁 *DEALS — Amazon Kids Gifts 30%+ Off*
• [Product](URL) — was $X, now $Y ⭐rating
• ...

🎉 *EVENTS — Sydney*
• [Event name](URL) — date, location — 1 line
• ...

☕ *NEW CAFES & RESTAURANTS — Sydney*
• [Place name](URL) — neighbourhood — brief why-trending note
• ...
```

## Rules
- Send as ONE message to the home channel
- Be selective — show the best 3-5 items per section, not everything
- If a source is paywalled, still show headline + URL
- Coles deals: filter for fresh foods, life essentials, baby products at 30%+ off
- Amazon deals: filter for kids gifts at 30%+ off
- Preserve headings (`##`), bullet structure, and paragraph breaks exactly as returned
- Output only the compiled digest message — no tool results, no reasoning text

## Common Issues
- Tavily search returning 432 → switch to `browser_navigate` through Google search results
- Coles catalogue page may not load products on first visit → navigate to specific category URL
- Amazon search results may need direct URL navigation to clearance pages
