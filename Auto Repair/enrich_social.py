"""
Step 2: Enrich S4 leads with Facebook, Instagram, and email via Google Search.
Runs headed (required to avoid CAPTCHA) with delays between searches.

Usage:
  python3 enrich_social.py [--batch-size 444] [--offset 0] [--delay 8]
"""

import asyncio
import csv
import random
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Install: pip3 install playwright && python3 -m playwright install chromium")
    sys.exit(1)

BASE_DIR = Path(__file__).parent
INPUT_CSV = BASE_DIR / "s4-leads.csv"
OUTPUT_CSV = BASE_DIR / "s4-leads-enriched.csv"

REVIEW_COLS = [
    "review1_name", "review1_stars", "review1_text",
    "review2_name", "review2_stars", "review2_text",
    "review3_name", "review3_stars", "review3_text",
    "review4_name", "review4_stars", "review4_text",
    "review5_name", "review5_stars", "review5_text",
]
SOCIAL_COLS = ["facebook_url", "instagram_url", "email"]
ALL_ENRICHMENT_COLS = REVIEW_COLS + SOCIAL_COLS


async def wait_and_dismiss_consent(page):
    try:
        for text in ['Accept all', 'I agree', 'Reject all', 'Accept All']:
            btn = page.locator(f'button:has-text("{text}")').first
            if await btn.is_visible(timeout=2000):
                await btn.click()
                await asyncio.sleep(1)
                return
    except Exception:
        pass


def _is_relevant_social(url, business_name):
    name_lower = business_name.lower()
    stop_words = {'auto', 'repair', 'shop', 'service', 'the', 'and', '&', 'car', 'mechanic', 'inc', 'llc', 'of'}
    keywords = [w for w in re.split(r'[\s&\'-]+', name_lower) if w and w not in stop_words and len(w) > 2]
    url_lower = url.lower()
    return any(kw in url_lower for kw in keywords) if keywords else True


async def search_social_and_email(page, business_name, city, state, delay=8):
    result = {"facebook_url": "", "instagram_url": "", "email": ""}
    query = quote_plus(f"{business_name} {city} {state}")
    fb_exclude = r'(?!sharer|share|dialog|login|help|policies|privacy|terms|groups/|events/|marketplace|watch|photo|story|settings|hashtag)'

    # Facebook
    try:
        await page.goto(
            f"https://www.google.com/search?q={query}+facebook&hl=en&gl=us",
            wait_until="load", timeout=25000
        )
        await asyncio.sleep(2)
        await wait_and_dismiss_consent(page)
        content = await page.content()

        # Check for CAPTCHA
        if "unusual traffic" in content.lower():
            print("    ⚠ CAPTCHA detected, pausing 60s...")
            await asyncio.sleep(60)
            await page.goto(
                f"https://www.google.com/search?q={query}+facebook&hl=en&gl=us",
                wait_until="load", timeout=25000
            )
            await asyncio.sleep(3)
            content = await page.content()

        fb_matches = re.findall(
            rf'https?://(?:www\.)?facebook\.com/{fb_exclude}[a-zA-Z0-9._/%-]+[a-zA-Z0-9]',
            content
        )
        for fb_url in fb_matches:
            fb_url = re.sub(r'[?&](?:utm_|fbclid|ref=|__cft__|locale=).*', '', fb_url).rstrip('/')
            if fb_url.endswith('/p') or fb_url.endswith('facebook.com'):
                continue
            if _is_relevant_social(fb_url, business_name) or 'facebook.com/p/' in fb_url:
                result["facebook_url"] = fb_url
                break
    except Exception as e:
        print(f"    FB error: {e}")

    await asyncio.sleep(delay + random.uniform(0, 3))

    # Instagram
    try:
        await page.goto(
            f"https://www.google.com/search?q={query}+instagram&hl=en&gl=us",
            wait_until="load", timeout=25000
        )
        await asyncio.sleep(2)
        content = await page.content()

        if "unusual traffic" in content.lower():
            print("    ⚠ CAPTCHA detected, pausing 60s...")
            await asyncio.sleep(60)
            await page.goto(
                f"https://www.google.com/search?q={query}+instagram&hl=en&gl=us",
                wait_until="load", timeout=25000
            )
            await asyncio.sleep(3)
            content = await page.content()

        ig_exclude = r'(?!explore|accounts|about|legal|reel/|p/|stories|directory|developer|static)'
        ig_matches = re.findall(
            rf'https?://(?:www\.)?instagram\.com/{ig_exclude}[a-zA-Z0-9_.]+',
            content
        )
        for ig_url in ig_matches:
            if _is_relevant_social(ig_url, business_name):
                result["instagram_url"] = ig_url
                break
    except Exception as e:
        print(f"    IG error: {e}")

    await asyncio.sleep(delay + random.uniform(0, 3))

    # Email
    try:
        await page.goto(
            f"https://www.google.com/search?q={query}+email+contact&hl=en&gl=us",
            wait_until="load", timeout=25000
        )
        await asyncio.sleep(2)
        content = await page.content()

        if "unusual traffic" in content.lower():
            print("    ⚠ CAPTCHA detected, pausing 60s...")
            await asyncio.sleep(60)
            await page.goto(
                f"https://www.google.com/search?q={query}+email+contact&hl=en&gl=us",
                wait_until="load", timeout=25000
            )
            await asyncio.sleep(3)
            content = await page.content()

        email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
        skip = ['google.com', 'gstatic', 'example.com', 'schema.org', 'w3.org',
                'googleapis', 'sentry', 'noreply', 'yelp.com', 'yahoo.com']
        for email in email_matches:
            if not any(x in email.lower() for x in skip):
                result["email"] = email
                break
    except Exception as e:
        print(f"    Email error: {e}")

    return result


def _save_output(rows, enriched_data, original_fields):
    all_fields = list(original_fields) + ALL_ENRICHMENT_COLS
    all_output = []
    for row in rows:
        pid = row["place_id"]
        if pid in enriched_data:
            merged = {**row, **enriched_data[pid]}
        else:
            merged = row
        all_output.append(merged)

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_output)


async def enrich_social(batch_size=444, offset=0, delay=8):
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_fields = reader.fieldnames
        rows = list(reader)

    batch = rows[offset:offset + batch_size]
    print(f"Social enrichment: {len(batch)} leads (offset={offset}, delay={delay}s between searches)")

    # Load existing enriched data
    enriched_data = {}
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                key = row.get("place_id", "")
                if key:
                    enriched_data[key] = row

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            locale="en-US",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )
        page = await context.new_page()
        await page.add_init_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        skipped = 0
        for i, row in enumerate(batch):
            name = row["name"]
            place_id = row["place_id"]

            existing = enriched_data.get(place_id, {})
            has_social = bool(existing.get("facebook_url") or existing.get("instagram_url") or existing.get("email"))
            if has_social:
                skipped += 1
                continue

            print(f"  [{i+1}/{len(batch)}] {name} ({row['city']}, {row['state']})")

            social = await search_social_and_email(page, name, row["city"], row["state"], delay)
            print(f"    FB: {social['facebook_url'] or '-'} | IG: {social['instagram_url'] or '-'} | Email: {social['email'] or '-'}")

            # Merge social into existing data, preserve reviews
            merged = {**row}
            # Keep existing review data
            for col in REVIEW_COLS:
                merged[col] = existing.get(col, "")
            # Update social
            merged["facebook_url"] = social["facebook_url"]
            merged["instagram_url"] = social["instagram_url"]
            merged["email"] = social["email"]

            enriched_data[place_id] = merged
            _save_output(rows, enriched_data, original_fields)

            # Delay between businesses
            await asyncio.sleep(delay + random.uniform(0, 5))

        await browser.close()

    has_social = sum(1 for r in enriched_data.values() if r.get("facebook_url") or r.get("instagram_url") or r.get("email"))
    print(f"\nDone. {has_social}/{len(rows)} have social data (skipped {skipped} already done) → {OUTPUT_CSV}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=444)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--delay", type=int, default=8, help="Seconds between Google searches (default 8)")
    args = parser.parse_args()
    asyncio.run(enrich_social(args.batch_size, args.offset, args.delay))
