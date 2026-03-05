#!/usr/bin/env python3
"""
Add review_recency column to labeled-dentals.csv.
Visits each clinic's Google Maps page, scrapes the most recent review date.
Labels: "Fresh" (<6mo), "Recent" (6-12mo), "Aging" (1-2yr), "Stale" (2yr+), "No reviews"

Usage:
  python3 07_add_review_recency.py                # Full run
  python3 07_add_review_recency.py --test         # First 10 clinics
  python3 07_add_review_recency.py --start=500    # Resume from row 500
"""

import csv
import os
import re
import sys
import time
import random
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(SCRIPT_DIR, "labeled-dentals.csv")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "labeled-dentals.csv")  # overwrite in place
CHECKPOINT_CSV = os.path.join(SCRIPT_DIR, "_review_recency_checkpoint.csv")

# Time-ago patterns from Google Maps (English)
TIME_PATTERNS = [
    (r'(\d+)\s*day', 'days'),
    (r'(\d+)\s*week', 'weeks'),
    (r'(\d+)\s*month', 'months'),
    (r'(\d+)\s*year', 'years'),
    (r'a\s+day', 'days_1'),
    (r'a\s+week', 'weeks_1'),
    (r'a\s+month', 'months_1'),
    (r'a\s+year', 'years_1'),
]


def parse_time_ago(text):
    """Parse '3 months ago', 'a year ago' etc into approximate days."""
    if not text:
        return None
    text = text.lower().strip()

    for pattern, unit in TIME_PATTERNS:
        match = re.search(pattern, text)
        if match:
            if unit.endswith('_1'):
                num = 1
                unit = unit.replace('_1', '')
            else:
                num = int(match.group(1))

            if unit == 'days':
                return num
            elif unit == 'weeks':
                return num * 7
            elif unit == 'months':
                return num * 30
            elif unit == 'years':
                return num * 365
    return None


def classify_recency(days_ago):
    """Classify review recency into buckets."""
    if days_ago is None:
        return "No reviews", ""
    if days_ago <= 180:
        return "Fresh", f"{days_ago}d ago"
    elif days_ago <= 365:
        return "Recent", f"{days_ago//30}mo ago"
    elif days_ago <= 730:
        return "Aging", f"{days_ago//365}yr {(days_ago%365)//30}mo ago"
    else:
        return "Stale", f"{days_ago//365}yr ago"


def scrape_latest_review_date(page, maps_url):
    """Visit Google Maps page and get the most recent review timestamp."""
    if not maps_url:
        return None

    try:
        page.goto(maps_url, wait_until="domcontentloaded", timeout=12000)
        time.sleep(2)
    except Exception:
        return None

    # Try to find review timestamps on the main page
    # Google Maps shows a few review snippets with timestamps
    timestamps = []

    # Method 1: Look for review time elements directly on the place page
    try:
        time_els = page.query_selector_all('.rsqaWe')
        for el in time_els[:5]:
            txt = el.inner_text().strip()
            days = parse_time_ago(txt)
            if days is not None:
                timestamps.append(days)
    except Exception:
        pass

    # Method 2: Try clicking "Reviews" sort to see timestamps
    if not timestamps:
        try:
            # Click on reviews tab/button
            for sel in [
                'button[aria-label*="review"]',
                'button[aria-label*="Review"]',
                '[role="tab"]:has-text("Reviews")',
                'button[jsaction*="reviewChart"]',
            ]:
                btn = page.query_selector(sel)
                if btn:
                    btn.click()
                    time.sleep(2)
                    break

            # Now look for timestamps in the reviews panel
            time_els = page.query_selector_all('.rsqaWe')
            for el in time_els[:5]:
                txt = el.inner_text().strip()
                days = parse_time_ago(txt)
                if days is not None:
                    timestamps.append(days)
        except Exception:
            pass

    # Method 3: Look for any "ago" text patterns in the visible page
    if not timestamps:
        try:
            body = page.inner_text('body', timeout=3000)
            ago_matches = re.findall(r'(\d+\s+(?:day|week|month|year)s?\s+ago|a\s+(?:day|week|month|year)\s+ago)', body.lower())
            for match in ago_matches[:5]:
                days = parse_time_ago(match)
                if days is not None:
                    timestamps.append(days)
        except Exception:
            pass

    if timestamps:
        return min(timestamps)  # Most recent review
    return None


def main():
    test_mode = "--test" in sys.argv
    start_idx = 0
    for arg in sys.argv:
        if arg.startswith("--start="):
            start_idx = int(arg.split("=")[1])

    print("=" * 60)
    print("Review Recency Analysis — NYC Dental Clinics")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if test_mode:
        print("TEST MODE: first 10 clinics")
    print("=" * 60)

    # Load data
    rows = []
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames)
        for row in reader:
            rows.append(row)

    print(f"Loaded {len(rows)} clinics")

    # Add new columns
    for col in ["review_recency", "latest_review_age"]:
        if col not in fields:
            fields.append(col)

    # Load checkpoint if resuming
    if os.path.exists(CHECKPOINT_CSV) and start_idx == 0:
        checkpoint = {}
        with open(CHECKPOINT_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                key = (row.get("name", ""), row.get("address", ""))
                checkpoint[key] = (row.get("review_recency", ""), row.get("latest_review_age", ""))
        print(f"Loaded {len(checkpoint)} from checkpoint")
    else:
        checkpoint = {}

    if test_mode:
        rows_to_process = rows[:10]
    else:
        rows_to_process = rows

    # Only scrape clinics that have reviews
    need_scrape = []
    for i, row in enumerate(rows_to_process):
        if i < start_idx:
            continue
        key = (row.get("name", ""), row.get("address", ""))
        if key in checkpoint:
            row["review_recency"] = checkpoint[key][0]
            row["latest_review_age"] = checkpoint[key][1]
            continue
        review_count = row.get("review_count", "0").strip()
        try:
            rc = int(review_count.replace(",", ""))
        except ValueError:
            rc = 0
        if rc > 0 and row.get("google_maps_url", "").strip():
            need_scrape.append(i)
        else:
            row["review_recency"] = "No reviews"
            row["latest_review_age"] = ""

    print(f"Need to scrape: {len(need_scrape)} clinics (skipping {len(rows_to_process) - len(need_scrape)})")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--lang=en-US",
            ],
        )
        context = browser.new_context(
            locale="en-US",
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        page = context.new_page()

        for count, i in enumerate(need_scrape):
            row = rows_to_process[i]
            name = row.get("name", "")[:40]
            maps_url = row.get("google_maps_url", "")

            # Force English on Google Maps URL
            if "hl=" in maps_url:
                maps_url = re.sub(r'hl=\w+', 'hl=en', maps_url)
            elif "?" in maps_url:
                maps_url += "&hl=en"
            else:
                maps_url += "?hl=en"

            days_ago = scrape_latest_review_date(page, maps_url)
            recency, age_str = classify_recency(days_ago)
            row["review_recency"] = recency
            row["latest_review_age"] = age_str

            status = f"[{count+1}/{len(need_scrape)}] {name:<40} → {recency}"
            if age_str:
                status += f" ({age_str})"
            print(status)

            # Save checkpoint every 100
            if (count + 1) % 100 == 0:
                with open(CHECKPOINT_CSV, "w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
                    writer.writeheader()
                    for r in rows:
                        if r.get("review_recency"):
                            writer.writerow(r)
                print(f"  --- Checkpoint saved: {count+1}/{len(need_scrape)} ---")

            time.sleep(random.uniform(1.0, 2.0))

        browser.close()

    # Write final output (always write ALL rows, not just processed subset)
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:  # full dataset, not rows_to_process
            # Ensure columns exist
            row.setdefault("review_recency", "")
            row.setdefault("latest_review_age", "")
            writer.writerow(row)

    # Clean up checkpoint
    if os.path.exists(CHECKPOINT_CSV):
        os.remove(CHECKPOINT_CSV)

    # Stats
    from collections import Counter as Ctr
    recency_dist = Ctr(r.get("review_recency", "") for r in rows if r.get("review_recency"))
    print(f"\n{'='*60}")
    print("Review Recency Distribution:")
    for label in ["Fresh", "Recent", "Aging", "Stale", "No reviews", ""]:
        if label in recency_dist:
            c = recency_dist[label]
            print(f"  {label or 'Unknown':<15} {c:>5} ({c*100//len(rows)}%)")
    print(f"{'='*60}")
    print(f"Output: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
