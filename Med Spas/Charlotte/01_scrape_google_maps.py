#!/usr/bin/env python3
"""
Step 1: Google Maps Scraper for Charlotte Metro Med Spas
Scrapes Google Maps for med spas using Playwright.

Usage:
  python3 01_scrape_google_maps.py                    # Full run
  python3 01_scrape_google_maps.py --test              # First search only, 5 results
  python3 01_scrape_google_maps.py --area=central      # Single area
  python3 01_scrape_google_maps.py --start=3           # Resume from search #3
"""

import csv
import os
import re
import sys
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "google-maps-raw.csv")

CSV_FIELDS = [
    "name", "address", "area", "city", "phone", "website", "rating",
    "review_count", "categories", "hours", "google_maps_url",
    "search_term", "scraped_at",
]

GOOGLE_MAPS_URL = "https://www.google.com/maps?hl=en"

SEARCHES = {
    "central": [
        "med spa Uptown Charlotte NC",
        "med spa South End Charlotte NC",
        "med spa NoDa Charlotte NC",
        "med spa Plaza Midwood Charlotte NC",
        "med spa Dilworth Charlotte NC",
        "med spa Myers Park Charlotte NC",
        "med spa Elizabeth Charlotte NC",
        "med spa Downtown Charlotte NC",
        "medical spa Charlotte NC",
        "medspa Charlotte NC",
        "botox Charlotte NC",
        "aesthetics clinic Charlotte NC",
        "laser hair removal Charlotte NC",
        "coolsculpting Charlotte NC",
    ],
    "south": [
        "med spa Pineville NC",
        "med spa Ballantyne Charlotte NC",
        "med spa Steele Creek Charlotte NC",
        "med spa Fort Mill SC",
        "medical spa Indian Land SC",
        "med spa Tega Cay SC",
        "medspa Lake Wylie SC",
        "med spa Rock Hill SC",
        "botox Ballantyne Charlotte NC",
        "botox Fort Mill SC",
    ],
    "north": [
        "med spa Huntersville NC",
        "med spa Cornelius NC",
        "med spa Davidson NC",
        "med spa Mooresville NC",
        "medical spa Statesville NC",
        "med spa University City Charlotte NC",
        "botox Huntersville NC",
        "medspa Mooresville NC",
        "laser hair removal Huntersville NC",
    ],
    "east": [
        "med spa Matthews NC",
        "med spa Mint Hill NC",
        "med spa Indian Trail NC",
        "medical spa Monroe NC",
        "medspa Stallings NC",
        "med spa Waxhaw NC",
        "med spa Weddington NC",
        "med spa Harrisburg NC",
        "med spa Concord NC",
        "medical spa Kannapolis NC",
        "botox Concord NC",
        "botox Matthews NC",
        "aesthetics Concord NC",
    ],
    "west": [
        "med spa Gastonia NC",
        "med spa Belmont NC",
        "medical spa Mount Holly NC",
        "medspa Lincolnton NC",
        "med spa Shelby NC",
        "botox Gastonia NC",
    ],
    "northwest": [
        "med spa Salisbury NC",
        "medical spa China Grove NC",
        "medspa Albemarle NC",
        "botox Salisbury NC",
    ],
}

AREA_ORDER = ["central", "south", "north", "east", "west", "northwest"]

# Area detection from address — matches Charlotte dentist scraper geography
AREA_PATTERNS = {
    "Central Charlotte": ["charlotte, nc 282", "uptown", "south end", "noda",
                          "plaza midwood", "dilworth", "myers park", "elizabeth"],
    "South": ["pineville", "ballantyne", "steele creek", "fort mill", "indian land",
              "tega cay", "lake wylie", "rock hill", "clover"],
    "North": ["huntersville", "cornelius", "davidson", "mooresville", "statesville",
              "university city"],
    "East": ["matthews", "mint hill", "indian trail", "monroe", "stallings",
             "waxhaw", "weddington", "wesley chapel", "harrisburg", "concord",
             "kannapolis"],
    "West": ["gastonia", "belmont", "mount holly", "dallas, nc", "cramerton",
             "lincolnton", "denver, nc", "shelby"],
    "Northwest": ["salisbury", "china grove", "albemarle"],
}


def detect_area(address, search_term=""):
    text = f"{address} {search_term}".lower()
    for area, patterns in AREA_PATTERNS.items():
        for p in patterns:
            if p in text:
                return area
    if "charlotte" in text:
        return "Central Charlotte"
    return ""


def random_delay(min_s=2.0, max_s=5.0):
    time.sleep(random.uniform(min_s, max_s))


def short_delay(min_s=0.5, max_s=1.5):
    time.sleep(random.uniform(min_s, max_s))


def load_existing_entries(csv_path):
    seen = set()
    if not os.path.exists(csv_path):
        return seen
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row.get("name", "").strip().lower(), row.get("address", "").strip().lower())
            if key != ("", ""):
                seen.add(key)
    print(f"  Loaded {len(seen)} existing entries from CSV")
    return seen


def append_to_csv(csv_path, row_dict):
    file_exists = os.path.exists(csv_path) and os.path.getsize(csv_path) > 0
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)


def dismiss_consent(page):
    for selector in [
        'button:has-text("Accept all")', 'button:has-text("I agree")',
        '[aria-label="Accept all"]', 'form[action*="consent"] button',
    ]:
        try:
            btn = page.query_selector(selector)
            if btn and btn.is_visible():
                btn.click()
                short_delay()
                return True
        except Exception:
            pass
    return False


def scroll_results_panel(page, max_scrolls=50):
    feed_selector = 'div[role="feed"]'
    try:
        page.wait_for_selector(feed_selector, timeout=10000)
    except PlaywrightTimeout:
        feed_selector = 'div[role="main"] div[tabindex="-1"]'
        try:
            page.wait_for_selector(feed_selector, timeout=5000)
        except PlaywrightTimeout:
            print("  No results panel found")
            return

    prev_count = 0
    stale_rounds = 0

    for i in range(max_scrolls):
        results = page.query_selector_all(f'{feed_selector} > div > div > a[href*="/maps/place/"]')
        if not results:
            results = page.query_selector_all('a[href*="/maps/place/"]')
        current_count = len(results)

        for end_text_query in [
            'span:has-text("You\'ve reached the end")',
            'span:has-text("end of")',
        ]:
            end_text = page.query_selector(end_text_query)
            if end_text:
                try:
                    txt = end_text.inner_text()
                    if "end" in txt.lower() or "reached" in txt.lower():
                        print(f"  End of results after {i+1} scrolls ({current_count} results)")
                        return
                except Exception:
                    pass

        if current_count == prev_count:
            stale_rounds += 1
            if stale_rounds >= 5:
                print(f"  No new results after {stale_rounds} scrolls ({current_count} results)")
                return
        else:
            stale_rounds = 0
        prev_count = current_count

        try:
            feed = page.query_selector(feed_selector)
            if feed:
                feed.evaluate('el => el.scrollTop = el.scrollHeight')
            else:
                page.keyboard.press("End")
        except Exception:
            page.keyboard.press("End")

        time.sleep(random.uniform(1.5, 3.0))
        if (i + 1) % 10 == 0:
            print(f"  Scrolled {i+1} times, {current_count} results so far...")

    print(f"  Max scrolls reached ({max_scrolls}), {prev_count} results")


def collect_result_links(page):
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


def extract_detail(page, url, search_term):
    data = {}
    data["name"] = extract_text(page, [
        'h1.fontHeadlineLarge', 'h1[class*="header"]', 'h1', 'div[role="main"] h1',
    ])

    data["address"] = ""
    addr_btn = page.query_selector('button[data-item-id="address"]')
    if addr_btn:
        data["address"] = addr_btn.inner_text().strip()
    else:
        addr_el = page.query_selector('[data-item-id*="address"]')
        if addr_el:
            data["address"] = (addr_el.get_attribute("aria-label") or addr_el.inner_text()).strip()

    data["area"] = detect_area(data["address"], search_term)
    data["city"] = "Charlotte"

    data["phone"] = ""
    phone_btn = page.query_selector('button[data-item-id*="phone"]')
    if phone_btn:
        raw = phone_btn.inner_text().strip()
        phone_match = re.search(r'[\d\-\+\(\)\s]{7,}', raw)
        if phone_match:
            data["phone"] = phone_match.group().strip()

    data["website"] = ""
    web_link = page.query_selector('a[data-item-id="authority"]')
    if web_link:
        data["website"] = web_link.get_attribute("href") or ""
    if not data["website"]:
        web_btn = page.query_selector('button[data-item-id="authority"]')
        if web_btn:
            data["website"] = web_btn.get_attribute("aria-label") or ""

    data["rating"] = ""
    rating_el = page.query_selector('div.fontDisplayLarge')
    if rating_el:
        text = rating_el.inner_text().strip()
        if re.match(r'^\d[\.\d]*$', text):
            data["rating"] = text
    if not data["rating"]:
        star_el = page.query_selector('span[role="img"][aria-label*="star"]')
        if star_el:
            aria = star_el.get_attribute("aria-label") or ""
            num = re.search(r'([\d\.]+)', aria)
            if num:
                data["rating"] = num.group(1)

    data["review_count"] = ""
    review_el = page.query_selector('button[jsaction*="reviewChart"] span')
    if review_el:
        text = review_el.inner_text().strip()
        num = re.search(r'[\d,]+', text.replace(',', ''))
        if num:
            data["review_count"] = num.group().replace(',', '')
    if not data["review_count"]:
        for sel in ['button[aria-label*="review"]', 'button[aria-label*="Review"]']:
            rev_btn = page.query_selector(sel)
            if rev_btn:
                aria = rev_btn.get_attribute("aria-label") or ""
                num = re.search(r'([\d,]+)', aria)
                if num:
                    data["review_count"] = num.group(1).replace(',', '')
                    break

    data["categories"] = ""
    cat_btn = page.query_selector('button[jsaction*="category"]')
    if cat_btn:
        data["categories"] = cat_btn.inner_text().strip()

    data["hours"] = ""
    hours_el = page.query_selector('[data-item-id*="oh"] .fontBodyMedium')
    if hours_el:
        data["hours"] = hours_el.inner_text().strip().replace('\n', ' | ')
    if not data["hours"]:
        hours_aria = page.query_selector('[aria-label*="hours"]')
        if hours_aria:
            data["hours"] = (hours_aria.get_attribute("aria-label") or "").strip()

    data["google_maps_url"] = url
    data["search_term"] = search_term
    data["scraped_at"] = datetime.now().isoformat()
    return data


def scrape_search(page, search_term, seen_entries, test_mode=False):
    print(f"\n{'='*60}")
    print(f"Search: {search_term}")
    print(f"{'='*60}")

    page.goto(GOOGLE_MAPS_URL, wait_until="domcontentloaded")
    random_delay(2, 4)
    dismiss_consent(page)

    search_box = page.query_selector('#searchboxinput') or page.query_selector('input[name="q"]')
    if not search_box:
        print("  ERROR: Could not find search box!")
        return 0

    search_box.click()
    short_delay(0.3, 0.8)
    search_box.fill("")
    short_delay(0.2, 0.5)
    search_box.fill(search_term)
    short_delay(0.5, 1.0)
    page.keyboard.press("Enter")
    random_delay(3, 5)

    if '/maps/place/' in page.url and 'search' not in page.url:
        print("  Single result page detected")
        data = extract_detail(page, page.url, search_term)
        key = (data["name"].lower(), data["address"].lower())
        if key not in seen_entries and data["name"]:
            append_to_csv(OUTPUT_CSV, data)
            seen_entries.add(key)
            print(f"  Saved: {data['name']}")
            return 1
        return 0

    print("  Scrolling to load all results...")
    scroll_results_panel(page)

    urls = collect_result_links(page)
    print(f"  Found {len(urls)} result links")

    if test_mode:
        urls = urls[:5]
        print(f"  TEST MODE: limiting to {len(urls)} results")

    saved_count = 0
    for idx, url in enumerate(urls):
        try:
            page.goto(url, wait_until="domcontentloaded")
            random_delay(2, 4)
            data = extract_detail(page, url, search_term)
            key = (data["name"].lower(), data["address"].lower())
            if key in seen_entries or not data["name"]:
                continue
            append_to_csv(OUTPUT_CSV, data)
            seen_entries.add(key)
            saved_count += 1
            status = f"  [{idx+1}/{len(urls)}] {data['name']}"
            if data["rating"]:
                status += f" | {data['rating']} ({data['review_count']})"
            if data["area"]:
                status += f" | {data['area']}"
            print(status)
        except PlaywrightTimeout:
            print(f"  [{idx+1}/{len(urls)}] Timeout - skipping")
        except Exception as e:
            print(f"  [{idx+1}/{len(urls)}] Error: {e}")

    print(f"\n  Search complete: {saved_count} new med spas saved ({len(urls)} total found)")
    return saved_count


def main():
    test_mode = "--test" in sys.argv
    target_area = None
    for arg in sys.argv:
        if arg.startswith("--area="):
            target_area = arg.split("=")[1].lower()
    start_idx = 0
    for arg in sys.argv:
        if arg.startswith("--start="):
            start_idx = int(arg.split("=")[1])

    if target_area:
        if target_area in SEARCHES:
            search_list = [(target_area, s) for s in SEARCHES[target_area]]
            print(f"Running area: {target_area} ({len(search_list)} searches)")
        else:
            print(f"Unknown area: {target_area}")
            print(f"Available: {', '.join(SEARCHES.keys())}")
            sys.exit(1)
    else:
        search_list = []
        for area in AREA_ORDER:
            for s in SEARCHES[area]:
                search_list.append((area, s))

    if test_mode:
        search_list = search_list[:1]
        print("TEST MODE: first search only, max 5 results")

    print(f"\n{'='*60}")
    print(f"Charlotte Metro Med Spas — Google Maps Scraper")
    print(f"Total searches: {len(search_list)}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    seen_entries = load_existing_entries(OUTPUT_CSV)
    total_saved = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--lang=en-US",
                "--accept-lang=en-US,en",
            ],
        )
        context = browser.new_context(
            locale="en-US",
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        page = context.new_page()

        current_area = None
        for i, (area, search_term) in enumerate(search_list):
            if i < start_idx:
                continue
            if area != current_area:
                if current_area:
                    print(f"\n{'*'*60}")
                    print(f"Area {current_area.upper()} complete. Total so far: {total_saved}")
                    print(f"{'*'*60}")
                current_area = area
                print(f"\n>>> Starting area: {area.upper()}")

            try:
                count = scrape_search(page, search_term, seen_entries, test_mode)
                total_saved += count
            except Exception as e:
                print(f"\n  SEARCH FAILED: {e}")
                print("  Continuing to next search...")

            if i < len(search_list) - 1:
                delay = random.uniform(5, 10)
                print(f"  Pausing {delay:.0f}s before next search...")
                time.sleep(delay)

        browser.close()

    print(f"\n{'='*60}")
    print(f"DONE!")
    print(f"Total new med spas saved: {total_saved}")
    print(f"Total unique med spas in CSV: {len(seen_entries)}")
    print(f"Output: {OUTPUT_CSV}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
