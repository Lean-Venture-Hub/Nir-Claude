#!/usr/bin/env python3
"""Scrape 3-5 Google reviews for each dentist in the CSV using Playwright."""

import csv, json, os, re, time
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "first_batch.csv")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "reviews.json")

def extract_reviews(page, url, max_reviews=5):
    """Visit a Google Maps URL and extract reviews."""
    reviews = []
    try:
        page.goto(url + "&hl=en", wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # Click on the reviews tab/button
        # Look for the reviews count button or tab
        try:
            # Try clicking the reviews tab
            reviews_tab = page.locator('button[aria-label*="review"]').first
            if reviews_tab.is_visible(timeout=3000):
                reviews_tab.click()
                time.sleep(2)
        except:
            pass

        # Try clicking "More reviews" or the review count text
        try:
            review_link = page.locator('button:has-text("review")').first
            if review_link.is_visible(timeout=2000):
                review_link.click()
                time.sleep(2)
        except:
            pass

        # Wait for reviews to load
        time.sleep(2)

        # Try to find review elements
        # Google Maps reviews are in div elements with specific data attributes
        review_elements = page.locator('div[data-review-id]').all()

        if not review_elements:
            # Alternative selector
            review_elements = page.locator('.jftiEf').all()

        for elem in review_elements[:max_reviews]:
            try:
                # Reviewer name
                name_el = elem.locator('.d4r55').first
                name = name_el.inner_text() if name_el.count() > 0 else ""

                if not name:
                    name_el = elem.locator('[class*="name"], .WNxzHc').first
                    name = name_el.inner_text() if name_el.count() > 0 else "Anonymous"

                # Star rating
                rating = 5  # default
                try:
                    stars_el = elem.locator('.kvMYJc').first
                    if stars_el.count() > 0:
                        aria = stars_el.get_attribute('aria-label') or ""
                        match = re.search(r'(\d)', aria)
                        if match:
                            rating = int(match.group(1))
                except:
                    pass

                # Review text
                text = ""
                try:
                    # Try "More" button first to expand
                    more_btn = elem.locator('button.w8nwRe').first
                    if more_btn.count() > 0 and more_btn.is_visible():
                        more_btn.click()
                        time.sleep(0.3)
                except:
                    pass

                try:
                    text_el = elem.locator('.wiI7pd').first
                    if text_el.count() > 0:
                        text = text_el.inner_text()
                    else:
                        text_el = elem.locator('.MyEned').first
                        if text_el.count() > 0:
                            text = text_el.inner_text()
                except:
                    pass

                if name and name != "Anonymous":
                    reviews.append({
                        "name": name.strip(),
                        "rating": rating,
                        "text": text.strip()[:300] if text else ""
                    })
            except Exception as e:
                continue

    except Exception as e:
        print(f"    Error: {e}")

    return reviews


def main():
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Scraping reviews for {len(rows)} dentists...\n")

    all_reviews = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            locale="en-US",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )
        page = context.new_page()

        for i, d in enumerate(rows):
            name = d['name'].strip()
            url = d.get('google_maps_url', '').strip()

            if not url:
                print(f"  [{i+1:2d}] {name} — NO URL, skipping")
                all_reviews[name] = []
                continue

            print(f"  [{i+1:2d}] {name}...", end=" ", flush=True)
            reviews = extract_reviews(page, url, max_reviews=5)
            all_reviews[name] = reviews
            print(f"got {len(reviews)} reviews")

            # Save progress after each
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(all_reviews, f, indent=2, ensure_ascii=False)

        browser.close()

    # Summary
    total = sum(len(v) for v in all_reviews.values())
    with_reviews = sum(1 for v in all_reviews.values() if v)
    print(f"\nDone! {total} reviews from {with_reviews}/{len(rows)} dentists")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
