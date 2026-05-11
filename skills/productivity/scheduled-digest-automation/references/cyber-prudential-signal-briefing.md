# Archived skill: cyber-prudential-signal-briefing

Original path: `research/cyber-prudential-signal-briefing/SKILL.md`

---

---
name: cyber-prudential-signal-briefing
description: Daily AI-Cyber Prudential Supervision Signal Briefing for APRA/NFR supervisors. Produces a high-signal daily brief on frontier AI cyber capabilities, vulnerability management, and financial-sector resilience. Runs as a daily cron at 2am Australia/Sydney.
version: 1.0.0
author: Hermes Agent
metadata:
  schedule: "0 2 * * *"  # 2am Australia/Sydney (AEST, UTC+10)
  audience: Senior cyber/AI risk supervisor at Australian prudential regulator (APRA/NFR)
  classification: Confidential - Supervisory Use Only
---

# AI-Cyber Prudential Signal Brief — Skill

This skill produces a daily supervision signal brief covering frontier AI cyber capability developments, vulnerability management, and financial-sector operational resilience.

## Input
No external input required — the cron job prompt is self-contained and executes all research passes independently.

## Sources to Monitor

### A. Frontier AI Labs & Safety Institutes
- Anthropic (security, policy, red-team, model cards)
- OpenAI (security, preparedness, capability updates)
- Google DeepMind (safety, cybersecurity)
- UK AI Security Institute
- US AI Safety Institute / NIST
- EU AI Office / ENISA
- METR, Apollo Research, ARC Evals, RAND

### B. Cyber Authorities & Exploited Vulnerabilities
- ACSC / ASD (Australia)
- CISA KEV catalog and alerts
- NCSC UK
- NSA, FBI, US Cyber Command
- CERT-EU
- ENISA
- JPCERT, SingCERT, Canadian Centre for Cyber Security
- Vendor emergency advisories: Microsoft, Google, Apple, Cisco, Fortinet, Palo Alto, Ivanti, Citrix, VMware/Broadcom, Atlassian, Okta, CrowdStrike, Cloudflare, AWS, Azure, Google Cloud, GitHub, GitLab, Docker, Kubernetes

### C. Financial-Sector Regulators
- APRA, ASIC, RBA, CFR
- Bank of England / PRA, FCA
- ECB, EBA, ESMA, EIOPA
- MAS Singapore, HKMA
- Federal Reserve, OCC, FDIC, FFIEC
- OSFI Canada, IOSCO, FSB, BIS, CPMI
- SEC cyber disclosure/enforcement

### D. Security Research
- Google Project Zero
- Microsoft Security Response Center
- Mandiant / Google Threat Intelligence
- CrowdStrike, Palo Alto Unit 42, Wiz
- Trail of Bits, Bishop Fox, SpecterOps
- NCC Group, Rapid7, Tenable, Qualys
- GreyNoise, VulnCheck, Snyk, Chainguard
- GitHub Security Lab, HackerOne, Bugcrowd
- arXiv, SSRN (AI cyber capability papers)

### E. Developer / Open-Source
- GitHub trending: AI vulnerability discovery, autonomous pentesting, AI red teaming, exploit generation, fuzzing, SAST/SCA/DAST, SBOM, cloud security posture management, Kubernetes security, agentic security testing, MCP security, browser/sandbox/container escape

### F. Media (signal detection only)
- Reuters, Bloomberg, FT, WSJ
- The Record, CyberScoop, Risky Business
- Dark Reading, BleepingComputer

## Search Strategy (18 passes)

Run these searches using `web_search` in parallel batches:

**Batch 1 — Frontier AI Cyber Capability:**
1. "frontier AI cyber capability 2026"
2. "Anthropic Mythos Claude cyber exploit capability"
3. "AI vulnerability discovery benchmark 2026"

**Batch 2 — AI Exploit & Attack:**
4. "AI exploit generation autonomous pentest 2026"
5. "AI red teaming vulnerability chaining 2026"
6. "autonomous agent cyber attack proof of concept 2026"

**Batch 3 — Vulnerabilities & CVEs:**
7. "CISA KEV known exploited vulnerability 2026"
8. "emergency vendor advisory critical patch 2026"
9. "zero-day exploit financial sector 2026"

**Batch 4 — Defensive AI:**
10. "AI secure code review tool 2026 release"
11. "AI vulnerability triage detection incident response 2026"
12. "AI patch management automation 2026"

**Batch 5 — Regulatory & Financial:**
13. "APRA CPS 234 cyber resilience 2026"
14. "financial sector AI cyber risk regulator guidance 2026"
15. "CPS 230 operational resilience cyber 2026"

**Batch 6 — Supply Chain & Systemic:**
16. "third-party cyber vulnerability financial services supply chain 2026"
17. "systemic bank cyber vulnerability concentration 2026"
18. "frontier model cyber risk evaluation regulator 2026"

## Output Format

Produce the following 11 sections. Target ~10-minute read.

### 1. Executive Summary
Max 8 bullets. What changed, why it matters, action required.

### 2. Signal Table
| Signal | Source | Category | Evidence | FI Relevance | Hype Risk | Supervisory Implication | Action |

Categories: Capability jump | Exploitability acceleration | Patch-window compression | Defensive uplift | Third-party/supply-chain | Operational resilience | Regulatory signal | Market/industry signal | Hype/weak signal

### 3. What Changed (Last 24–72h)
Separate:
- Frontier model capability
- Vulnerabilities / exploited CVEs
- Vendor advisories
- Regulatory signals
- Defensive tools
- Financial-sector implications

### 4. Hype vs Reality
Use direct language:
- "This is panic."
- "This is plausible but not yet evidenced."
- "This is materially relevant."
- "This should change supervisory expectations now."

### 5. Implications for Vulnerability Management
Assess: patch SLAs, emergency change windows, internet-facing exposure, KEV handling, legacy tech, dependency management, SBOM, cloud/SaaS config risk, identity/privileged access, attack-path management, vulnerability disclosure intake.

### 6. Implications for Third-Party & Supply-Chain Risk
Assess: critical vendors, SaaS dependencies, managed service providers, open-source dependencies, cloud concentration, security-tool concentration, vendor notification speed, contractual patching obligations, fourth-party visibility.

### 7. Implications for Operational Resilience
Assess: critical operations, tolerance levels, severe-but-plausible scenarios, crisis management, incident notification, board reporting, customer impact, payment systems, cross-sector contagion.

### 8. Recommended Supervisory Actions
- Immediate (7 days)
- Near-term (30 days)
- Medium-term (90 days)

### 9. Recommended Questions for Institutions
5–10 sharp questions for CISOs, CROs, CIOs, boards or accountable executives.

### 10. Watchlist
Rolling list:
- Models / labs to monitor
- Regulators to monitor
- CVEs / vendors to monitor
- GitHub repos / tools to monitor
- Financial institutions to monitor
- Claims requiring verification

### 11. Confidence & Gaps
- Overall confidence level
- Key evidence gaps
- What to verify tomorrow
- Items requiring human escalation

## Decision Rules

**High Priority** (escalate now):
1. Affects internet-facing systems widely used by FIs
2. Affects identity, privileged access, remote access, payment systems, cloud control planes, core banking, managed file transfer, endpoint security, security appliances
3. Listed in CISA KEV or equivalent exploited-vulnerability source
4. Credible public exploit code or active exploitation
5. Material third party or concentrated technology provider
6. Frontier AI materially lowers exploit development time
7. Plausible impact to critical operations or systemic institutions
8. Regulatory expectations changing

**Watch but do not act** (monitor):
1. Media speculation only
2. Lab benchmark without real-world evidence
3. Vendor marketing without reproducible evidence
4. Narrow technical domain, low FI relevance
5. Plausible but unsupported claim

**Debunk / deprioritise**:
1. CTF results confused with real-world compromise
2. No technical detail
3. Recycled news with no new information
4. Ignores existing controls/monitoring
5. Mainly fear-based vendor positioning

## Tone
- Clear, direct, analytical, supervisor-grade
- No sensationalism, no vendor marketing language
- No generic cyber hygiene filler
- No long academic preamble
- Include source links for every important claim

## Research Tool Fallbacks

The `web_search` (Tavily) API frequently returns HTTP 432 (rate-limit) errors during cron execution. When this occurs, fall back to the following reliable sources in order:

### Primary Sources (via terminal/curl)
- **CISA KEV JSON feed** — most reliable primary source:
  ```
  curl -s --max-time 20 -o /tmp/kev.json "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
  ```
  Parse with `execute_code` (save to file first, then parse — do NOT pipe curl to python).

- **The Hacker News RSS** — reliable media source:
  ```
  curl -s --max-time 15 -o /tmp/thn.xml "https://feeds.feedburner.com/TheHackersNews"
  ```
  Parse with `execute_code` using `xml.dom.minidom`.

### Browser Navigation
- `browser_navigate` works for CISA, APRA, Project Zero, GitHub advisories, and most government sites.
- **Known failure:** Some Microsoft URLs (MSRC RSS, advisory pages) return 404 or redirect to generic pages. Try the direct GitHub advisory URL format: `https://github.com/advisories/GHSA-xxxx`.
- **Known redirect:** Browser navigation may redirect to Google Gemini on some URLs. Verify the final URL matches the intended source.
- NVD (nvd.nist.gov) is frequently down or returns 404. Do not rely on it as a primary source during cron runs.

### Article Content Extraction
- When `web_extract` fails (rate-limited), use `browser_navigate` to the article URL and read the page snapshot directly.
- THN articles are readable via browser_navigate despite anti-bot banners.

## Delivery
When running as a cron job (this skill's primary mode), **do NOT use `send_message`** — the cron job delivery system handles output automatically. Only use `send_message` when invoked on-demand.
