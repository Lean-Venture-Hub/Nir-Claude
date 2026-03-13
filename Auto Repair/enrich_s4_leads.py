"""
Enrich S4 leads with reviews, social links, and email.
Uses Playwright for browser automation.

Usage:
  python3 enrich_s4_leads.py [--batch-size 10] [--offset 0] [--headed]
"""

import asyncio
import csv
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

ENRICHMENT_COLS = [
    "review1_name", "review1_stars", "review1_text",
    "review2_name", "review2_stars", "review2_text",
    "review3_name", "review3_stars", "review3_text",
    "review4_name", "review4_stars", "review4_text",
    "review5_name", "review5_stars", "review5_text",
    "facebook_url", "instagram_url", "email",
]


async def wait_and_dismiss_consent(page):
    """Dismiss Google consent banners if they appear."""
    try:
        for text in ['Accept all', 'I agree', 'Reject all', 'Accept All']:
            btn = page.locator(f'button:has-text("{text}")').first
            if await btn.is_visible(timeout=2000):
                await btn.click()
                await asyncio.sleep(1)
                return
    except Exception:
        pass


async def scrape_reviews(page, maps_url, max_reviews=5):
    """Extract reviews from a Google Maps listing."""
    reviews = []
    try:
        # Add hl=en to get English reviews
        separator = "&" if "?" in maps_url else "?"
        await page.goto(f"{maps_url}{separator}hl=en", wait_until="load", timeout=30000)
        # Wait for the page to render the place panel
        try:
            await page.wait_for_selector('h1', timeout=10000)
        except Exception:
            pass
        await asyncio.sleep(3)
        await wait_and_dismiss_consent(page)

        # Click Reviews tab to load all reviews
        try:
            reviews_tab = page.locator('button[role="tab"]').filter(
                has_text=re.compile(r"Reviews|ביקורות", re.I)
            )
            if await reviews_tab.count() > 0:
                await reviews_tab.first.click()
                await asyncio.sleep(3)
        except Exception:
            pass

        # Get full page HTML and extract reviews via regex
        html = await page.content()

        # Google Maps review text lives in spans with class "wiI7pd"
        review_texts = re.findall(r'class="wiI7pd"[^>]*>([^<]+)</span>', html)

        # Star ratings: each review has an img/span with aria-label like "5 stars" or "4 כוכבים"
        star_ratings = re.findall(r'aria-label="(\d)\s*(?:stars?|כוכב)', html)

        # Reviewer names: in elements with class "d4r55" or buttons with reviewer info
        reviewer_names = re.findall(r'class="d4r55[^"]*"[^>]*>([^<]+)<', html)
        if not reviewer_names:
            # Alternative: look for aria-label="Photo of X" pattern
            reviewer_names = re.findall(r'aria-label="(?:Photo of |תמונה של )([^"]+)"', html)

        # Filter out star ratings that belong to the overall rating (not individual reviews)
        # The first star rating is usually the overall rating, individual ones come after
        # We'll try to align by taking from the review section onwards
        # Look for review section marker
        review_section_idx = html.find('wiI7pd')
        if review_section_idx > 0:
            review_html = html[max(0, review_section_idx - 2000):]
            star_ratings_section = re.findall(r'aria-label="(\d)\s*(?:stars?|כוכב)', review_html)
        else:
            star_ratings_section = star_ratings

        for j in range(min(len(review_texts), max_reviews)):
            reviews.append({
                "name": reviewer_names[j][:100] if j < len(reviewer_names) else "",
                "stars": int(star_ratings_section[j]) if j < len(star_ratings_section) else 0,
                "text": review_texts[j][:500],
            })

        # If regex approach got nothing, try DOM selectors
        if not reviews:
            # Try .jftiEf containers (each wraps a single review)
            containers = page.locator('.jftiEf')
            count = await containers.count()
            for j in range(min(count, max_reviews)):
                el = containers.nth(j)
                try:
                    text = await el.inner_text()
                    # Parse: first line = name, then star info, then review text
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    name = lines[0] if lines else ""
                    review_text = max(lines[1:], key=len, default="") if len(lines) > 1 else ""
                    reviews.append({"name": name[:100], "stars": 0, "text": review_text[:500]})
                except Exception:
                    continue

    except Exception as e:
        print(f"    Reviews error: {e}")

    return reviews


def _is_relevant_social(url, business_name):
    """Check if a social URL likely belongs to the business (not a random result)."""
    # Normalize business name to keywords
    name_lower = business_name.lower()
    # Remove common words
    stop_words = {'auto', 'repair', 'shop', 'service', 'the', 'and', '&', 'car', 'mechanic', 'inc', 'llc', 'of'}
    keywords = [w for w in re.split(r'[\s&\'-]+', name_lower) if w and w not in stop_words and len(w) > 2]
    url_lower = url.lower()
    # At least one meaningful keyword from name should appear in URL
    return any(kw in url_lower for kw in keywords) if keywords else True


async def search_social_and_email(page, business_name, city, state):
    """Search Google for Facebook, Instagram, and email (requires headed mode or stealth)."""
    result = {"facebook_url": "", "instagram_url": "", "email": ""}
    query = quote_plus(f"{business_name} {city} {state}")

    # Search for Facebook page
    try:
        await page.goto(
            f"https://www.google.com/search?q={query}+facebook&hl=en&gl=us",
            wait_until="load", timeout=20000
        )
        await asyncio.sleep(3)
        await wait_and_dismiss_consent(page)
        content = await page.content()

        # Match full FB URLs including /p/Name-123/ format (allow dashes, slashes, digits)
        fb_exclude = r'(?!sharer|share|dialog|login|help|policies|privacy|terms|groups/|events/|marketplace|watch|photo|story|settings|hashtag)'
        fb_matches = re.findall(
            rf'https?://(?:www\.)?facebook\.com/{fb_exclude}[a-zA-Z0-9._/%-]+[a-zA-Z0-9]',
            content
        )
        for fb_url in fb_matches:
            # Clean tracking params
            fb_url = re.sub(r'[?&](?:utm_|fbclid|ref=|__cft__|locale=).*', '', fb_url).rstrip('/')
            # Skip truncated /p URLs — need at least /p/Something
            if fb_url.endswith('/p') or fb_url.endswith('facebook.com'):
                continue
            if _is_relevant_social(fb_url, business_name) or 'facebook.com/p/' in fb_url:
                result["facebook_url"] = fb_url
                break
    except Exception as e:
        print(f"    FB search error: {e}")

    # Search for Instagram
    try:
        await page.goto(
            f"https://www.google.com/search?q={query}+instagram&hl=en&gl=us",
            wait_until="load", timeout=20000
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
        print(f"    IG search error: {e}")

    # Search for email
    try:
        await page.goto(
            f"https://www.google.com/search?q={query}+email+contact&hl=en&gl=us",
            wait_until="load", timeout=20000
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
        print(f"    Email search error: {e}")

    return result


async def enrich_batch(batch_size=10, offset=0, headed=False):
    """Enrich a batch of S4 leads."""
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_fields = reader.fieldnames
        rows = list(reader)

    batch = rows[offset:offset + batch_size]
    print(f"Enriching {len(batch)} leads (offset={offset}, total={len(rows)})")

    # Read existing enriched data
    enriched_data = {}
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                key = row.get("place_id", "")
                if key:
                    enriched_data[key] = row

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=not headed,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            locale="en-US",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )
        page = await context.new_page()
        await page.add_init_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        for i, row in enumerate(batch):
            name = row["name"]
            city = row["city"]
            state = row["state"]
            place_id = row["place_id"]
            maps_url = row["google_maps_url"]

            existing = enriched_data.get(place_id, {})
            has_reviews = bool(existing.get("review1_text"))
            has_social = bool(existing.get("facebook_url") or existing.get("instagram_url") or existing.get("email"))
            if has_reviews and has_social:
                print(f"  [{i+1}/{len(batch)}] {name} — fully enriched, skipping")
                continue

            print(f"  [{i+1}/{len(batch)}] {name} ({city}, {state})")

            # Scrape reviews
            reviews = await scrape_reviews(page, maps_url)
            print(f"    Reviews: {len(reviews)}")

            # Search for social/email
            social = await search_social_and_email(page, name, city, state)
            print(f"    FB: {social['facebook_url'] or '-'} | IG: {social['instagram_url'] or '-'} | Email: {social['email'] or '-'}")

            # Merge into row
            for j in range(5):
                if j < len(reviews):
                    row[f"review{j+1}_name"] = reviews[j]["name"]
                    row[f"review{j+1}_stars"] = reviews[j]["stars"]
                    row[f"review{j+1}_text"] = reviews[j]["text"]
                else:
                    row[f"review{j+1}_name"] = ""
                    row[f"review{j+1}_stars"] = ""
                    row[f"review{j+1}_text"] = ""

            row["facebook_url"] = social["facebook_url"]
            row["instagram_url"] = social["instagram_url"]
            row["email"] = social["email"]
            enriched_data[place_id] = row

            # Save after each business (incremental)
            _save_output(rows, enriched_data, original_fields)

            await asyncio.sleep(1)

        await browser.close()

    enriched_count = sum(1 for pid, r in enriched_data.items() if r.get("review1_text") or r.get("facebook_url") or r.get("email"))
    print(f"\nDone. Enriched {enriched_count} leads → {OUTPUT_CSV}")


def _save_output(rows, enriched_data, original_fields):
    """Save current state to CSV."""
    all_fields = list(original_fields) + ENRICHMENT_COLS
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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--headed", action="store_true", default=True, help="Run browser visibly (default, needed to avoid CAPTCHA)")
    parser.add_argument("--headless", action="store_true", help="Run headless (may get blocked by Google)")
    args = parser.parse_args()
    headed = not args.headless  # headed by default
    asyncio.run(enrich_batch(args.batch_size, args.offset, headed))
