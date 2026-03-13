"""
Step 1: Enrich S4 leads with Google Maps reviews only.
Fast — runs headless, no Google Search needed.

Usage:
  python3 enrich_reviews.py [--batch-size 444] [--offset 0]
"""

import asyncio
import csv
import re
import sys
from pathlib import Path

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


async def scrape_reviews(page, maps_url, max_reviews=5):
    reviews = []
    try:
        separator = "&" if "?" in maps_url else "?"
        await page.goto(f"{maps_url}{separator}hl=en", wait_until="load", timeout=30000)
        try:
            await page.wait_for_selector('h1', timeout=10000)
        except Exception:
            pass
        await asyncio.sleep(3)
        await wait_and_dismiss_consent(page)

        # Click Reviews tab
        try:
            reviews_tab = page.locator('button[role="tab"]').filter(
                has_text=re.compile(r"Reviews|ביקורות", re.I)
            )
            if await reviews_tab.count() > 0:
                await reviews_tab.first.click()
                await asyncio.sleep(3)
        except Exception:
            pass

        html = await page.content()

        review_texts = re.findall(r'class="wiI7pd"[^>]*>([^<]+)</span>', html)
        star_ratings = re.findall(r'aria-label="(\d)\s*(?:stars?|כוכב)', html)
        reviewer_names = re.findall(r'class="d4r55[^"]*"[^>]*>([^<]+)<', html)
        if not reviewer_names:
            reviewer_names = re.findall(r'aria-label="(?:Photo of |תמונה של )([^"]+)"', html)

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

        if not reviews:
            containers = page.locator('.jftiEf')
            count = await containers.count()
            for j in range(min(count, max_reviews)):
                el = containers.nth(j)
                try:
                    text = await el.inner_text()
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    name = lines[0] if lines else ""
                    review_text = max(lines[1:], key=len, default="") if len(lines) > 1 else ""
                    reviews.append({"name": name[:100], "stars": 0, "text": review_text[:500]})
                except Exception:
                    continue

    except Exception as e:
        print(f"    Reviews error: {e}")

    return reviews


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


async def enrich_reviews(batch_size=444, offset=0):
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_fields = reader.fieldnames
        rows = list(reader)

    batch = rows[offset:offset + batch_size]
    print(f"Reviews enrichment: {len(batch)} leads (offset={offset})")

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
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            locale="en-US",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )
        page = await context.new_page()

        skipped = 0
        for i, row in enumerate(batch):
            name = row["name"]
            place_id = row["place_id"]
            maps_url = row["google_maps_url"]

            existing = enriched_data.get(place_id, {})
            if existing.get("review1_text"):
                skipped += 1
                continue

            print(f"  [{i+1}/{len(batch)}] {name} ({row['city']}, {row['state']})")

            reviews = await scrape_reviews(page, maps_url)
            print(f"    → {len(reviews)} reviews")

            # Merge reviews into row, preserve existing social data
            for j in range(5):
                if j < len(reviews):
                    row[f"review{j+1}_name"] = reviews[j]["name"]
                    row[f"review{j+1}_stars"] = reviews[j]["stars"]
                    row[f"review{j+1}_text"] = reviews[j]["text"]
                else:
                    row[f"review{j+1}_name"] = ""
                    row[f"review{j+1}_stars"] = ""
                    row[f"review{j+1}_text"] = ""

            # Preserve existing social data if any
            row["facebook_url"] = existing.get("facebook_url", "")
            row["instagram_url"] = existing.get("instagram_url", "")
            row["email"] = existing.get("email", "")

            enriched_data[place_id] = row
            _save_output(rows, enriched_data, original_fields)

            await asyncio.sleep(1)

        await browser.close()

    has_reviews = sum(1 for r in enriched_data.values() if r.get("review1_text"))
    print(f"\nDone. {has_reviews}/{len(rows)} have reviews (skipped {skipped} already done) → {OUTPUT_CSV}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=444)
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()
    asyncio.run(enrich_reviews(args.batch_size, args.offset))
