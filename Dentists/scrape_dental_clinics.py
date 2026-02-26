#!/usr/bin/env python3
"""
Gush Dan Dental Clinics Scraper
Scrapes Google Maps for dental clinics using Playwright.
Saves results incrementally to CSV.
Run: python3 scrape_dental_clinics.py [--test]
"""

import csv
import os
import re
import sys
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# --- Config ---
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "gush-dan-dental-clinics.csv")
SEARCHES = [
    "מרפאת שיניים תל אביב יפו",
    "מרפאת שיניים רמת גן גבעתיים",
    "מרפאת שיניים חולון בת ים",
    "מרפאת שיניים הרצליה רעננה",
    "מרפאת שיניים פתח תקווה בני ברק",
    "רופא שיניים תל אביב",
]
CSV_FIELDS = [
    "name", "address", "city", "phone", "website", "rating",
    "review_count", "categories", "hours", "google_maps_url",
    "search_term", "scraped_at",
]
GOOGLE_MAPS_URL = "https://www.google.com/maps"


def random_delay(min_s=2.0, max_s=5.0):
    """Human-like random delay."""
    time.sleep(random.uniform(min_s, max_s))


def short_delay(min_s=0.5, max_s=1.5):
    """Short delay for quick actions."""
    time.sleep(random.uniform(min_s, max_s))


def load_existing_entries(csv_path):
    """Load existing CSV entries to avoid duplicates. Returns set of (name, address) tuples."""
    seen = set()
    if not os.path.exists(csv_path):
        return seen
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row.get("name", "").strip(), row.get("address", "").strip())
            if key != ("", ""):
                seen.add(key)
    print(f"  Loaded {len(seen)} existing entries from CSV")
    return seen


def append_to_csv(csv_path, row_dict):
    """Append a single row to CSV. Creates file with header if needed."""
    file_exists = os.path.exists(csv_path) and os.path.getsize(csv_path) > 0
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)


def parse_city_from_address(address):
    """Try to extract city name from Hebrew address string."""
    if not address:
        return ""
    # Common Gush Dan cities
    cities = [
        "תל אביב", "תל-אביב", "רמת גן", "גבעתיים", "חולון", "בת ים",
        "הרצליה", "רעננה", "פתח תקווה", "פתח-תקווה", "בני ברק",
        "ראשון לציון", "ראשון-לציון", "נתניה", "כפר סבא", "הוד השרון",
        "רמת השרון", "גבעת שמואל", "קרית אונו", "יהוד", "אור יהודה",
        "אזור", "ירושלים", "רחובות", "נס ציונה", "לוד", "רמלה",
    ]
    for city in cities:
        if city in address:
            return city
    return ""


def dismiss_consent(page):
    """Handle Google consent/cookie dialogs."""
    try:
        # Google consent form - click "Accept all" or similar
        for selector in [
            'button:has-text("Accept all")',
            'button:has-text("קבל הכל")',
            'button:has-text("I agree")',
            'button:has-text("אני מסכים")',
            '[aria-label="Accept all"]',
            'form[action*="consent"] button',
        ]:
            btn = page.query_selector(selector)
            if btn and btn.is_visible():
                btn.click()
                print("  Dismissed consent dialog")
                short_delay()
                return True
    except Exception:
        pass
    return False


def scroll_results_panel(page, max_scrolls=40):
    """
    Scroll the results panel to load all results.
    Returns when "end of list" is detected or max scrolls reached.
    """
    # The results feed container
    feed_selector = 'div[role="feed"]'
    try:
        page.wait_for_selector(feed_selector, timeout=10000)
    except PlaywrightTimeout:
        print("  Could not find results feed, trying alternative selectors...")
        # Try alternative: the scrollable results div
        feed_selector = 'div[role="main"] div[tabindex="-1"]'
        try:
            page.wait_for_selector(feed_selector, timeout=5000)
        except PlaywrightTimeout:
            print("  No results panel found")
            return

    prev_count = 0
    stale_rounds = 0

    for i in range(max_scrolls):
        # Count current results
        results = page.query_selector_all(f'{feed_selector} > div > div > a[href*="/maps/place/"]')
        if not results:
            # Alternative: try direct links
            results = page.query_selector_all('a[href*="/maps/place/"]')

        current_count = len(results)

        # Check for "end of results" indicator
        end_text = page.query_selector('p.fontBodyMedium span:has-text("end of")')
        if not end_text:
            end_text = page.query_selector('span:has-text("הגעת לסוף")')
        if not end_text:
            end_text = page.query_selector('span:has-text("You\'ve reached the end")')

        if end_text:
            print(f"  Reached end of results after {i+1} scrolls ({current_count} results)")
            return

        if current_count == prev_count:
            stale_rounds += 1
            if stale_rounds >= 5:
                print(f"  No new results after {stale_rounds} scrolls ({current_count} results)")
                return
        else:
            stale_rounds = 0

        prev_count = current_count

        # Scroll the feed container
        try:
            feed = page.query_selector(feed_selector)
            if feed:
                feed.evaluate('el => el.scrollTop = el.scrollHeight')
            else:
                page.keyboard.press("End")
        except Exception:
            page.keyboard.press("End")

        # Wait for new results to load
        time.sleep(random.uniform(1.5, 3.0))

        if (i + 1) % 10 == 0:
            print(f"  Scrolled {i+1} times, {current_count} results so far...")

    print(f"  Max scrolls reached ({max_scrolls}), {prev_count} results")


def collect_result_links(page):
    """Collect all place links from the results panel."""
    links = page.query_selector_all('a[href*="/maps/place/"]')
    urls = []
    seen_hrefs = set()
    for link in links:
        try:
            href = link.get_attribute("href")
            if href and href not in seen_hrefs:
                seen_hrefs.add(href)
                urls.append(href)
        except Exception:
            continue
    return urls


def extract_text(page, selectors, default=""):
    """Try multiple selectors, return first match text."""
    for sel in selectors:
        try:
            el = page.query_selector(sel)
            if el:
                text = el.inner_text().strip()
                if text:
                    return text
        except Exception:
            continue
    return default


def extract_detail(page, url):
    """Extract clinic details from the currently loaded detail panel/page."""
    data = {}

    # Name - the main heading
    data["name"] = extract_text(page, [
        'h1.fontHeadlineLarge',
        'h1[class*="header"]',
        'h1',
        'div[role="main"] h1',
    ])

    # Address
    data["address"] = ""
    addr_btn = page.query_selector('button[data-item-id="address"]')
    if addr_btn:
        data["address"] = addr_btn.inner_text().strip()
    else:
        # Try aria-label approach
        addr_el = page.query_selector('[data-item-id*="address"]')
        if addr_el:
            data["address"] = addr_el.get_attribute("aria-label") or addr_el.inner_text().strip()

    data["city"] = parse_city_from_address(data["address"])

    # Phone
    data["phone"] = ""
    phone_btn = page.query_selector('button[data-item-id*="phone"]')
    if phone_btn:
        data["phone"] = phone_btn.inner_text().strip()
        # Clean phone - extract just the number
        phone_match = re.search(r'[\d\-\+\(\)\s]{7,}', data["phone"])
        if phone_match:
            data["phone"] = phone_match.group().strip()

    # Website
    data["website"] = ""
    web_link = page.query_selector('a[data-item-id="authority"]')
    if web_link:
        data["website"] = web_link.get_attribute("href") or ""
    if not data["website"]:
        web_btn = page.query_selector('button[data-item-id="authority"]')
        if web_btn:
            aria = web_btn.get_attribute("aria-label") or ""
            data["website"] = aria

    # Rating
    data["rating"] = ""
    rating_el = page.query_selector('div.fontDisplayLarge')
    if rating_el:
        text = rating_el.inner_text().strip()
        if re.match(r'^\d[\.\d]*$', text):
            data["rating"] = text
    if not data["rating"]:
        # Try from aria-label
        star_el = page.query_selector('span[role="img"][aria-label*="star"]')
        if not star_el:
            star_el = page.query_selector('span[role="img"][aria-label*="כוכב"]')
        if star_el:
            aria = star_el.get_attribute("aria-label") or ""
            num = re.search(r'([\d\.]+)', aria)
            if num:
                data["rating"] = num.group(1)

    # Review count
    data["review_count"] = ""
    review_el = page.query_selector('button[jsaction*="reviewChart"] span')
    if review_el:
        text = review_el.inner_text().strip()
        # Extract number from "(123)" or "123 reviews"
        num = re.search(r'[\d,]+', text.replace(',', ''))
        if num:
            data["review_count"] = num.group().replace(',', '')
    if not data["review_count"]:
        # Try aria-label on reviews button
        rev_btn = page.query_selector('button[aria-label*="review"]')
        if not rev_btn:
            rev_btn = page.query_selector('button[aria-label*="ביקורת"]')
        if rev_btn:
            aria = rev_btn.get_attribute("aria-label") or ""
            num = re.search(r'([\d,]+)', aria)
            if num:
                data["review_count"] = num.group(1).replace(',', '')

    # Categories
    data["categories"] = ""
    cat_btn = page.query_selector('button[jsaction*="category"]')
    if cat_btn:
        data["categories"] = cat_btn.inner_text().strip()
    else:
        # Sometimes it's a plain span near the rating
        cat_spans = page.query_selector_all('span.fontBodyMedium button')
        cats = [s.inner_text().strip() for s in cat_spans[:3] if s.inner_text().strip()]
        data["categories"] = ", ".join(cats)

    # Hours - try to get from info section
    data["hours"] = ""
    hours_el = page.query_selector('[data-item-id*="oh"] .fontBodyMedium')
    if hours_el:
        data["hours"] = hours_el.inner_text().strip().replace('\n', ' | ')
    if not data["hours"]:
        hours_aria = page.query_selector('[aria-label*="hours"]')
        if not hours_aria:
            hours_aria = page.query_selector('[aria-label*="שעות"]')
        if hours_aria:
            data["hours"] = hours_aria.get_attribute("aria-label") or ""

    # Google Maps URL
    data["google_maps_url"] = url

    return data


def scrape_search(page, search_term, seen_entries, test_mode=False):
    """Run one search term and scrape all results."""
    print(f"\n{'='*60}")
    print(f"Search: {search_term}")
    print(f"{'='*60}")

    # Navigate to Google Maps
    page.goto(GOOGLE_MAPS_URL, wait_until="domcontentloaded")
    random_delay(2, 4)

    # Dismiss consent if needed
    dismiss_consent(page)

    # Find search box and enter query
    search_box = page.query_selector('#searchboxinput')
    if not search_box:
        search_box = page.query_selector('input[name="q"]')
    if not search_box:
        print("  ERROR: Could not find search box!")
        return 0

    search_box.click()
    short_delay(0.3, 0.8)
    search_box.fill("")
    short_delay(0.2, 0.5)

    # Type search term character by character for more human-like behavior
    search_box.fill(search_term)
    short_delay(0.5, 1.0)
    page.keyboard.press("Enter")

    # Wait for results to load
    random_delay(3, 5)

    # Check if we got a results list (not a single place)
    if '/maps/place/' in page.url and 'search' not in page.url:
        print("  Single result page detected, extracting...")
        data = extract_detail(page, page.url)
        data["search_term"] = search_term
        data["scraped_at"] = datetime.now().isoformat()
        key = (data["name"], data["address"])
        if key not in seen_entries and data["name"]:
            append_to_csv(OUTPUT_CSV, data)
            seen_entries.add(key)
            print(f"  Saved: {data['name']}")
            return 1
        return 0

    # Scroll to load all results
    print("  Scrolling to load all results...")
    scroll_results_panel(page)

    # Collect all result URLs
    urls = collect_result_links(page)
    print(f"  Found {len(urls)} result links")

    if test_mode:
        urls = urls[:5]  # Only scrape first 5 in test mode
        print(f"  TEST MODE: limiting to {len(urls)} results")

    saved_count = 0

    for idx, url in enumerate(urls):
        try:
            # Navigate to the place page
            page.goto(url, wait_until="domcontentloaded")
            random_delay(2, 4)

            # Extract details
            data = extract_detail(page, url)
            data["search_term"] = search_term
            data["scraped_at"] = datetime.now().isoformat()

            # Dedup check
            key = (data["name"], data["address"])
            if key in seen_entries or not data["name"]:
                if data["name"]:
                    pass  # skip silently for dupes
                continue

            # Save incrementally
            append_to_csv(OUTPUT_CSV, data)
            seen_entries.add(key)
            saved_count += 1

            # Progress
            status = f"  [{idx+1}/{len(urls)}] {data['name']}"
            if data["phone"]:
                status += f" | {data['phone']}"
            if data["rating"]:
                status += f" | ★{data['rating']}"
            print(status)

        except PlaywrightTimeout:
            print(f"  [{idx+1}/{len(urls)}] Timeout - skipping")
            continue
        except Exception as e:
            print(f"  [{idx+1}/{len(urls)}] Error: {e}")
            continue

    print(f"\n  Search complete: {saved_count} new clinics saved ({len(urls)} total found)")
    return saved_count


def main():
    test_mode = "--test" in sys.argv

    if test_mode:
        print("=" * 60)
        print("TEST MODE: Running first search only, max 5 results")
        print("=" * 60)

    # Load existing entries for dedup
    seen_entries = load_existing_entries(OUTPUT_CSV)

    total_saved = 0

    with sync_playwright() as p:
        # Launch headed browser (visible) for anti-detection
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--lang=he-IL",
            ],
        )
        context = browser.new_context(
            locale="he-IL",
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        searches = SEARCHES[:1] if test_mode else SEARCHES

        for i, search_term in enumerate(searches):
            try:
                count = scrape_search(page, search_term, seen_entries, test_mode)
                total_saved += count
            except Exception as e:
                print(f"\n  SEARCH FAILED: {e}")
                print("  Continuing to next search...")
                continue

            # Longer pause between searches
            if i < len(searches) - 1:
                delay = random.uniform(5, 10)
                print(f"\n  Pausing {delay:.0f}s before next search...")
                time.sleep(delay)

        browser.close()

    print("\n" + "=" * 60)
    print(f"DONE! Total new clinics saved: {total_saved}")
    print(f"Total unique clinics in CSV: {len(seen_entries)}")
    print(f"Output: {OUTPUT_CSV}")
    print("=" * 60)


if __name__ == "__main__":
    main()
