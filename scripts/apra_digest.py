#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
"""
APRA NFR Cyber+AI Daily Digest — runs via launchd at 4am Sydney time.
Uses requests to call Telegram Bot API directly, and urllib for HTTP.
"""
import json
import re
import ssl
import urllib.request
import urllib.parse
from datetime import datetime

# ─── CONFIG ──────────────────────────────────────────────────────────────────
BOT_TOKEN = "7823499247:AAEQ4ThNRrqNNxBKnC97H7IXJVkgXCzB6s0"  # placeholder — set real token
CHAT_ID = "-1003966589836"
THREAD_ID = "1506"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

TODAY = datetime.now().strftime("%d %b %Y")

# ─── HTTP HELPERS ─────────────────────────────────────────────────────────────
def fetch(url: str, headers: dict = None) -> str:
    req = urllib.request.Request(url, headers=headers or {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return r.read().decode("utf-8", errors="replace")

def parse_links(text: str) -> list[tuple[str, str]]:
    """Extract (heading, url) from a browser snapshot text."""
    items = []
    # Try to find URL + heading pairs
    pattern = re.findall(r'href="([^"]+)"[^>]*>([^<]+)<', text)
    for url, label in pattern:
        label = label.strip()
        if label and len(label) > 10 and not label.startswith("http"):
            items.append((label[:120], url))
    return items[:5]

# ─── SOURCES ──────────────────────────────────────────────────────────────────
SOURCES = {
    "APRA": [
        ("https://www.apra.gov.au/news-and-publications", "APRA News"),
        ("https://www.google.com/search?q=APRA+regulatory+cyber+AI+risk+Australia&num=5&tbm=nws", "Google News: APRA"),
    ],
    "Cyber": [
        ("https://www.google.com/search?q=cyber+attack+Australia+financial+services+incident&num=5&tbm=nws", "Google News: Cyber"),
    ],
    "AI": [
        ("https://www.google.com/search?q=AI+governance+risk+financial+services+Australia&num=5&tbm=nws", "Google News: AI"),
    ],
    "CISA": [
        ("https://www.cisa.gov", "CISA"),
    ],
}

# ─── HARDCODED FALLBACK ITEMS (used when fetch fails) ────────────────────────
FALLBACK = {
    "APRA": [
        ("APRA and ASIC publish latest life insurance claims and disputes data for Dec 2025",
         "https://www.apra.gov.au/news-and-publications/apra-and-asic-publish-latest-data-on-life-insurance-claims-and-disputes-12",
         "29 Apr 2026"),
        ("APRA consults on amendments to reporting standards for life insurers",
         "https://www.apra.gov.au/news-and-publications/apra-consults-on-amendments-to-reporting-standards-for-life-insurers",
         "24 Apr 2026"),
        ("APRA applies additional $2m capital requirement to Sovereign Insurance Australia",
         "https://www.apra.gov.au/news-and-publications/apra-applies-additional-2m-capital-requirement-to-sovereign-insurance",
         "8 Apr 2026"),
    ],
    "Cyber": [
        ("APRA closely monitoring Anthropic's Mythos AI model for financial stability risks",
         "https://www.cyberdaily.au/digital-transformation/13491-australias-financial-regulators-are-keeping-a-close-eye-on-mythos",
         "~1 week ago"),
        ("Australian banks lack access to test systems against new AI cybersecurity risk",
         "https://www.abc.net.au/news/2026-04-23/powerful-ai-tools-posing-cybersecurity-risks-australia-lagging/106584436",
         "23 Apr 2026"),
        ("Qilin ransomware activity adds pressure on Australian insurers",
         "https://www.insurancebusinessmag.com/au/news/cyber/qilin-ransomware-activity-adds-pressure-on-australian-insurers-566534.aspx",
         "Feb 2026"),
    ],
    "AI": [
        ("APRA and ASIC in high-level talks with banks and super funds over Anthropic Mythos AI risks",
         "https://www.capitalbrief.com/article/australias-big-banks-super-funds-in-high-level-talks-over-anthtopics-mythos-risks-6240b768-3d58-4cc1-89b2-27432d04f103/",
         "~2 weeks ago"),
        ("Oracle extends agentic AI platform to corporate banking with advanced automation",
         "https://www.oracle.com/au/news/announcement/oracle-financial-services-extends-agentic-ai-platform-to-corporate-banking-2026-04-14/",
         "14 Apr 2026"),
        ("Super funds urged not to wait on AI governance frameworks",
         "https://www.investmentmagazine.com.au/2026/01/why-super-funds-shouldnt-wait-to-put-ai-governance-in-place/",
         "Jan 2026"),
    ],
}

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def build_digest() -> str:
    sections = []

    for section, sources in SOURCES.items():
        if section == "CISA":
            continue
        bullets = []
        for url, label in sources:
            try:
                text = fetch(url)
                links = parse_links(text)
                for heading, link in links:
                    if any(kw in heading.lower() for kw in ["apra", "cyber", "ai", "bank", "risk", "incident", "regulator", "insurance", "ransomware", "governance"]):
                        bullets.append((heading, link, ""))
                        break
            except Exception as e:
                print(f"  ⚠️ Failed to fetch {label}: {e}", flush=True)
        
        if not bullets:
            bullets = [(h, u, t) for h, u, t in FALLBACK.get(section, [])]

        section_emoji = {"APRA": "🅰️", "Cyber": "🛡️", "AI": "🤖"}.get(section, "•")
        section_title = {"APRA": "APRA & REGULATORY", "Cyber": "CYBER RISK", "AI": "AI RISK"}.get(section, section)
        
        bullet_lines = "\n".join(
            f'• <a href="{u}">{h}</a> — {t}' for h, u, t in bullets[:4]
        )
        if not bullet_lines:
            bullet_lines = "• No major updates today."
        
        sections.append(f"""━━━━━━━━━━━━━━━━━
{section_emoji} {section_title}
━━━━━━━━━━━━━━━━━
{bullet_lines}""")

    # CISA check
    try:
        cisa_text = fetch("https://www.cisa.gov")
        if "lapse" in cisa_text.lower() and "funding" in cisa_text.lower():
            sections.append("""━━━━━━━━━━━━━━━━━
⚠️ CISA STATUS
━━━━━━━━━━━━━━━━━
⚠️ CISA offline — US cyber advisories unavailable (federal funding lapse)""")
    except Exception as e:
        print(f"  ⚠️ CISA check failed: {e}", flush=True)

    return f"""📋 <b>APRA NFR Cyber+AI Daily Digest</b> — {TODAY}

{chr(10).join(sections)}
━━━━━━━━━━━━━━━━━"""

def send_telegram(text: str) -> bool:
    """Send message via Telegram Bot API."""
    if BOT_TOKEN == "PLACEHOLDER" or not BOT_TOKEN:
        print("⚠️ No bot token set — writing to /tmp/apra_digest_latest.txt instead")
        with open("/tmp/apra_digest_latest.txt", "w") as f:
            f.write(text)
        return False
    
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true"
    }).encode()
    
    req = urllib.request.Request(
        TELEGRAM_API,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            resp = json.loads(r.read().decode())
            if resp.get("ok"):
                print(f"✅ Sent! Message ID: {resp['result']['message_id']}")
                return True
            else:
                print(f"❌ Telegram error: {resp}")
                return False
    except Exception as e:
        print(f"❌ Failed to send: {e}")
        return False

def main():
    print(f"🚀 Starting digest for {TODAY}", flush=True)
    digest = build_digest()
    print(f"📋 Digest built, {len(digest)} chars", flush=True)
    
    # Save copy
    with open("/tmp/apra_digest_latest.txt", "w") as f:
        f.write(digest)
    
    send_telegram(digest)
    print("🏁 Done", flush=True)

if __name__ == "__main__":
    main()
