#!/usr/bin/env python3
"""Scrape 3-5 good Google reviews for segment 4/4a/4b dentists and add columns to labeled-dentals.csv.

Usage: python 08_scrape_reviews_for_csv.py <CityFolder>
Example: python 08_scrape_reviews_for_csv.py NY
"""

import csv, json, os, re, sys, time
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_REVIEWS = 5
TARGET_SEGMENTS = {"4", "4a", "4b"}
REVIEW_COLUMNS = []
for i in range(1, MAX_REVIEWS + 1):
    REVIEW_COLUMNS.extend([f"review{i}_name", f"review{i}_rating", f"review{i}_text"])


def extract_reviews(page, url, max_reviews=MAX_REVIEWS):
    """Visit a Google Maps URL and extract good (4-5 star) reviews."""
    reviews = []
    try:
        page.goto(url + "&hl=en", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # Click the Reviews tab
        try:
            tabs = page.locator('button[role="tab"]').all()
            for tab in tabs:
                label = (tab.get_attribute('aria-label') or '').lower()
                if 'review' in label:
                    tab.click()
                    time.sleep(3)
                    break
        except:
            pass

        # Sort by highest rating
        try:
            sort_btn = page.locator('button[aria-label="Sort reviews"], button[data-value="Sort"]').first
            if sort_btn.count() > 0:
                sort_btn.click()
                time.sleep(1)
                # Click "Highest rating"
                menu_items = page.locator('div[role="menuitemradio"], li[role="menuitemradio"]').all()
                for item in menu_items:
                    text = item.inner_text().lower()
                    if 'highest' in text:
                        item.click()
                        time.sleep(2)
                        break
        except:
            pass

        # Scroll down in the reviews panel to load more
        try:
            scrollable = page.locator('div.m6QErb.DxyBCb.kA9KIf.dS8AEf').first
            if scrollable.count() > 0:
                for _ in range(3):
                    scrollable.evaluate('el => el.scrollTop = el.scrollHeight')
                    time.sleep(1)
        except:
            pass

        # Find review elements
        review_elements = page.locator('div[data-review-id]').all()
        if not review_elements:
            review_elements = page.locator('.jftiEf').all()

        for elem in review_elements:
            if len(reviews) >= max_reviews:
                break
            try:
                # Star rating
                rating = 0
                try:
                    stars_el = elem.locator('.kvMYJc').first
                    if stars_el.count() > 0:
                        aria = stars_el.get_attribute('aria-label') or ""
                        match = re.search(r'(\d)', aria)
                        if match:
                            rating = int(match.group(1))
                except:
                    pass

                # Only keep 4-5 star reviews
                if rating < 4:
                    continue

                # Reviewer name
                name = ""
                name_el = elem.locator('.d4r55').first
                if name_el.count() > 0:
                    name = name_el.inner_text()
                if not name:
                    name_el = elem.locator('[class*="name"], .WNxzHc').first
                    if name_el.count() > 0:
                        name = name_el.inner_text()

                # Expand "More" button
                try:
                    more_btn = elem.locator('button.w8nwRe').first
                    if more_btn.count() > 0 and more_btn.is_visible():
                        more_btn.click()
                        time.sleep(0.3)
                except:
                    pass

                # Review text
                text = ""
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

                if name and name.strip() != "Anonymous" and text.strip():
                    reviews.append({
                        "name": name.strip(),
                        "rating": rating,
                        "text": text.strip()[:300]
                    })
            except:
                continue

    except Exception as e:
        print(f"    Error: {e}")

    return reviews


def main():
    if len(sys.argv) < 2:
        print("Usage: python 08_scrape_reviews_for_csv.py <CityFolder>")
        sys.exit(1)

    city = sys.argv[1]
    city_dir = os.path.join(SCRIPT_DIR, city)
    csv_path = os.path.join(city_dir, "labeled-dentals.csv")
    progress_path = os.path.join(city_dir, "reviews-progress.json")

    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        sys.exit(1)

    # Load existing progress
    progress = {}
    if os.path.exists(progress_path):
        with open(progress_path, 'r', encoding='utf-8') as f:
            progress = json.load(f)

    # Read CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        original_fields = reader.fieldnames
        rows = list(reader)

    # Filter to target segments
    target_rows = [(i, r) for i, r in enumerate(rows) if r.get('segment', '').strip() in TARGET_SEGMENTS]
    print(f"[{city}] {len(target_rows)} dentists in segments 4/4a/4b (out of {len(rows)} total)")

    already = sum(1 for _, r in target_rows if r['name'].strip() in progress)
    print(f"[{city}] {already} already scraped, {len(target_rows) - already} remaining\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            locale="en-US",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )
        page = context.new_page()

        for idx, (row_idx, row) in enumerate(target_rows):
            name = row['name'].strip()
            url = row.get('google_maps_url', '').strip()

            if name in progress:
                continue

            if not url:
                print(f"  [{idx+1}/{len(target_rows)}] {name} — NO URL, skipping")
                progress[name] = []
                continue

            print(f"  [{idx+1}/{len(target_rows)}] {name}...", end=" ", flush=True)
            reviews = extract_reviews(page, url)
            progress[name] = reviews
            print(f"got {len(reviews)} reviews")

            # Save progress after each
            with open(progress_path, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)

        browser.close()

    # Now update the CSV with review columns
    output_fields = list(original_fields)
    for col in REVIEW_COLUMNS:
        if col not in output_fields:
            output_fields.append(col)

    for row in rows:
        name = row['name'].strip()
        reviews = progress.get(name, [])
        for i in range(MAX_REVIEWS):
            if i < len(reviews):
                row[f"review{i+1}_name"] = reviews[i]["name"]
                row[f"review{i+1}_rating"] = str(reviews[i]["rating"])
                row[f"review{i+1}_text"] = reviews[i]["text"]
            else:
                row[f"review{i+1}_name"] = ""
                row[f"review{i+1}_rating"] = ""
                row[f"review{i+1}_text"] = ""

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows)

    # Summary
    total = sum(len(v) for v in progress.values())
    with_reviews = sum(1 for v in progress.values() if v)
    print(f"\n[{city}] Done! {total} reviews from {with_reviews}/{len(target_rows)} dentists")
    print(f"[{city}] CSV updated: {csv_path}")


if __name__ == '__main__':
    main()
