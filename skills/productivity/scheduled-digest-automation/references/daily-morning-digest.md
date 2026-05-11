# Archived skill: daily-morning-digest

Original path: `productivity/daily-morning-digest/SKILL.md`

---

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

## Practical Extraction Techniques from Cron Runs

### Coles specials
- Prefer the catalogue PDF when product pages/specials pages omit prices. From `/catalogues`, use the current NSW Metro PDF link (for example CloudFront `COLNSWMETRO_*.pdf`), download it, then run:
  ```bash
  pdftotext -layout /tmp/coles.pdf /tmp/coles.txt
  ```
- Search the text for essentials/baby/fresh keywords (`BabyLove`, `Rascals`, `Huggies`, `Laundry`, `Dishwashing`, `Tissues`, `Chicken`, `Fruit`, `Vegetables`, `Wipes`) and use nearby `WAS`, `SAVE`, and sale-price lines to compute discounts. This is more reliable than the dynamic Coles specials page in cron/browser contexts.
- Fresh produce often appears as catalogue specials without explicit previous prices; only include it in the 30%+ section when a `WAS`/`SAVE` value supports the discount. Otherwise prioritise baby and household essentials with verifiable prices.

### Amazon kids gifts
- Amazon filtered URLs can show “No results” while still rendering sponsored/customer-viewed cards below. Use browser DOM extraction rather than relying on the visible snapshot alone:
  ```js
  Array.from(document.querySelectorAll('[data-component-type="s-search-result"], .s-result-item[data-asin]'))
    .filter(el => el.querySelector('h2 span'))
    .map(el => ({
      title: el.querySelector('h2 span')?.innerText,
      url: el.querySelector('h2 a')?.href || el.querySelector('a.a-link-normal.s-no-outline')?.href,
      price: el.querySelector('.a-price .a-offscreen')?.innerText,
      rating: el.querySelector('.a-icon-alt')?.innerText,
      text: el.innerText
    }))
  ```
- If the 30%+ discount filter is sparse, try exact searches for promising products surfaced by web search snippets, then calculate `RRP` vs current price from the Amazon result text. Avoid padding with unrelated adult books/comics unless they are genuinely suitable kids gifts.
- A reliable fallback for Amazon AU kids gifts is the Toys & Games limited-time deals page: `https://www.amazon.com.au/Toys-Games-Todays-Deals/s?rh=n%3A4852617051%2Cp_n_deal_type%3A10343589051`. Extract via DOM, parse either `RRP:` or `Was:` from each result’s `innerText`, then calculate `(was-now)/was`. This surfaces higher-confidence 30%+ items than broad `kids gifts` search. Example extraction:
  ```js
  Array.from(document.querySelectorAll('[data-component-type="s-search-result"], .s-result-item[data-asin]'))
    .filter(el => el.querySelector('h2 span'))
    .map(el => {
      const text = el.innerText;
      const was = (text.match(/RRP:\s*\n?\$([\d.]+)/) || text.match(/Was:\s*\n?\$([\d.]+)/) || [])[1];
      return {
        title: el.querySelector('h2 span')?.innerText,
        url: el.querySelector('h2 a')?.href || el.querySelector('a.a-link-normal.s-no-outline')?.href,
        price: el.querySelector('.a-price .a-offscreen')?.innerText,
        was: was && '$' + was,
        rating: el.querySelector('.a-icon-alt')?.innerText,
        text
      };
    })
  ```
- For Telegram output, only include toys/kids/baby gifts where the computed discount is at least 30%. Prefer clean `amazon.com.au/.../dp/ASIN` URLs when possible; sponsored redirect URLs work but are less readable.

### Coles specials
- If Coles `/specials` is too dynamic or sparse and a current OzBargain supermarket half-price catalogue report is available, use that report as a pragmatic fallback for verifiable `was`, `now`, and `% off` values. Then run targeted searches like `site:coles.com.au/product "Product Name"` to get product URLs for the digest. Keep the Coles section filtered to fresh food, baby, or life essentials; household cleaning and laundry products qualify as essentials.

### News URLs
- Search result snippets often provide cleaner canonical article URLs than paywalled homepages. For SMH/AFR, combine homepage/category `web_extract` for headline discovery with targeted `web_search` for exact headline URLs.
