#!/usr/bin/env python3
"""Scrape 3-5 Google reviews per Tel Aviv dental clinic from labeled-dentals.csv.

Output: reviews.csv with columns:
  clinic_name, reviewer_name, stars, review_text, review_date, google_maps_url
"""

import csv, os, time, re, sys
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(SCRIPT_DIR, "labeled-dentals.csv")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "reviews.csv")
TARGET_REVIEWS = 5
GUSH_DAN_CITIES = {"תל אביב", "בת ים", "בני ברק", "פתח תקווה", "רמת גן", "חולון", "גבעתיים", "קרית אונו", ""}


def load_clinics():
    clinics = []
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("city", "").strip() in GUSH_DAN_CITIES and row.get("google_maps_url", "").strip():
                clinics.append({
                    "name": row["name"].strip(),
                    "url": row["google_maps_url"].strip(),
                })
    return clinics


def load_already_scraped():
    """Return set of clinic names already in output CSV."""
    done = set()
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                done.add(row.get("clinic_name", "").strip())
    return done


def scrape_reviews(page, clinic_name, url):
    """Navigate to a Google Maps place and scrape up to TARGET_REVIEWS reviews."""
    reviews = []
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(3)
    except Exception as e:
        print(f"  ERROR loading page: {e}")
        return reviews

    # Accept cookies/consent if prompted
    try:
        consent = page.locator('button:has-text("Accept all"), button:has-text("קבל הכל"), form[action*="consent"] button')
        if consent.count() > 0:
            consent.first.click()
            time.sleep(1)
    except:
        pass

    # Click on the reviews tab/button to open the reviews panel
    try:
        # Try clicking the reviews count button (e.g. "55 reviews" or "55 ביקורות")
        reviews_btn = page.locator('button[jsaction*="reviews"], button[aria-label*="review"], button[aria-label*="ביקור"]')
        if reviews_btn.count() > 0:
            reviews_btn.first.click()
            time.sleep(2)
        else:
            # Try the tab approach
            tab = page.locator('button[role="tab"]:has-text("Reviews"), button[role="tab"]:has-text("ביקורות")')
            if tab.count() > 0:
                tab.first.click()
                time.sleep(2)
    except:
        pass

    # Wait for review elements to appear
    time.sleep(2)

    # Try to expand "More" buttons on reviews so we get full text
    try:
        more_buttons = page.locator('button.w8nwRe, button:has-text("More"), button:has-text("עוד")')
        for i in range(min(more_buttons.count(), TARGET_REVIEWS)):
            try:
                more_buttons.nth(i).click()
                time.sleep(0.3)
            except:
                pass
    except:
        pass

    # Extract reviews - Google Maps uses div[data-review-id] or jxGMlf class
    review_containers = page.locator('div[data-review-id], div.jftiEf')
    count = review_containers.count()

    for i in range(min(count, TARGET_REVIEWS)):
        try:
            container = review_containers.nth(i)

            # Reviewer name
            name_el = container.locator('div.d4r55, button.WNxzHc div, a.WNxzHc div.d4r55')
            reviewer = name_el.first.inner_text().strip() if name_el.count() > 0 else ""

            # Star rating - look for aria-label with stars or count filled star icons
            stars = 0
            rating_el = container.locator('span[role="img"][aria-label]')
            if rating_el.count() > 0:
                label = rating_el.first.get_attribute("aria-label") or ""
                # Extract number from "5 stars" or "5 כוכבים"
                m = re.search(r'(\d)', label)
                if m:
                    stars = int(m.group(1))

            # Review text
            text_el = container.locator('span.wiI7pd, div.MyEned span')
            review_text = text_el.first.inner_text().strip() if text_el.count() > 0 else ""

            # Review date
            date_el = container.locator('span.rsqaWe')
            review_date = date_el.first.inner_text().strip() if date_el.count() > 0 else ""

            if reviewer or review_text:
                reviews.append({
                    "clinic_name": clinic_name,
                    "reviewer_name": reviewer,
                    "stars": stars,
                    "review_text": review_text.replace("\n", " ").strip(),
                    "review_date": review_date,
                    "google_maps_url": url,
                })
        except Exception as e:
            continue

    return reviews


def main():
    clinics = load_clinics()
    already_done = load_already_scraped()
    remaining = [c for c in clinics if c["name"] not in already_done]

    print(f"Total Tel Aviv clinics: {len(clinics)}")
    print(f"Already scraped: {len(already_done)}")
    print(f"Remaining: {len(remaining)}")

    if not remaining:
        print("All clinics already scraped!")
        return

    # Check if output file exists to determine if we need to write headers
    write_header = not os.path.exists(OUTPUT_CSV)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            locale="he-IL",
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["clinic_name", "reviewer_name", "stars", "review_text", "review_date", "google_maps_url"])
            if write_header:
                writer.writeheader()

            for idx, clinic in enumerate(remaining):
                print(f"\n[{idx + 1}/{len(remaining)}] {clinic['name']}")
                try:
                    reviews = scrape_reviews(page, clinic["name"], clinic["url"])
                    if reviews:
                        for r in reviews:
                            writer.writerow(r)
                        f.flush()
                        print(f"  -> {len(reviews)} reviews collected")
                    else:
                        print(f"  -> No reviews found")
                except Exception as e:
                    print(f"  ERROR: {e}")

                # Small delay between clinics
                time.sleep(1)

        browser.close()

    # Count results
    total = 0
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            total = sum(1 for _ in f) - 1
    print(f"\nDone! Total reviews in {OUTPUT_CSV}: {total}")


if __name__ == "__main__":
    main()
