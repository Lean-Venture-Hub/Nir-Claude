#!/usr/bin/env python3
"""
Step 4: Website Enrichment for NYC Dentists
Visits each clinic's website to extract:
  - Social media URLs (Facebook, Instagram, TikTok)
  - Doctor/staff count (from About/Team pages)
  - Site quality score (0-10)
  - Online booking detection

Usage:
  python3 04_enrich_websites.py                # Full run
  python3 04_enrich_websites.py --test         # First 5 clinics
  python3 04_enrich_websites.py --start=100    # Resume from row 100
"""

import csv
import os
import re
import sys
import time
import random
from datetime import datetime
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(SCRIPT_DIR, "google-maps-raw.csv")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "enriched-clinics.csv")

ORIGINAL_FIELDS = [
    "name", "address", "borough", "city", "phone", "website", "rating",
    "review_count", "categories", "hours", "google_maps_url",
    "search_term", "scraped_at",
]

ENRICHMENT_FIELDS = [
    "facebook_url", "instagram_url", "tiktok_url",
    "google_review_count", "doctor_count", "staff_count",
    "site_score", "has_online_booking", "comments",
]

ALL_FIELDS = ORIGINAL_FIELDS + ENRICHMENT_FIELDS

# Booking platform signatures
BOOKING_SIGNATURES = [
    "zocdoc.com", "zocdoc", "book online", "book now", "schedule appointment",
    "schedule online", "request appointment", "book appointment",
    "localmed.com", "localmed", "dentrix", "solutionreach",
    "patientpop", "weave", "nexphealth", "opencare",
    "calendly.com", "acuityscheduling.com", "setmore.com",
    "getweave.com", "lighthouse360", "demandforce",
]

# Social media URL patterns
SOCIAL_PATTERNS = {
    "facebook": re.compile(r'https?://(?:www\.)?facebook\.com/[^\s"\'<>]+', re.I),
    "instagram": re.compile(r'https?://(?:www\.)?instagram\.com/[^\s"\'<>]+', re.I),
    "tiktok": re.compile(r'https?://(?:www\.)?tiktok\.com/@[^\s"\'<>]+', re.I),
}

# Doctor/staff indicators
DOCTOR_TITLES = [
    r'\bDDS\b', r'\bDMD\b', r'\bD\.D\.S\.', r'\bD\.M\.D\.',
    r'\bDr\.\s', r'\bDoctor\b',
]
TEAM_LINK_PATTERNS = [
    "about", "team", "staff", "doctors", "dentists", "our-team",
    "meet-the-team", "meet-our-team", "providers", "our-doctors",
    "our-dentists", "about-us",
]


def random_delay(min_s=1.5, max_s=3.5):
    time.sleep(random.uniform(min_s, max_s))


def load_csv_rows(path):
    """Load all rows from input CSV."""
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def write_enriched_csv(path, rows):
    """Write all enriched rows to CSV."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ALL_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def clean_social_url(url, platform):
    """Clean and normalize a social media URL."""
    if not url:
        return ""
    url = url.strip().rstrip('/')
    # Remove tracking params
    url = re.sub(r'[?#].*$', '', url)
    # Remove trailing slashes and common junk
    url = url.rstrip('/')
    # Skip if it's just the base domain
    parsed = urlparse(url)
    if platform == "facebook" and parsed.path in ('/', ''):
        return ""
    return url


def extract_social_urls(page_content, page_url=""):
    """Extract social media URLs from page HTML content."""
    social = {"facebook_url": "", "instagram_url": "", "tiktok_url": ""}

    for platform, pattern in SOCIAL_PATTERNS.items():
        matches = pattern.findall(page_content)
        for match in matches:
            cleaned = clean_social_url(match, platform)
            if cleaned:
                # Skip self-referencing (e.g., their own domain appearing in OG tags)
                if page_url and urlparse(page_url).netloc in cleaned:
                    continue
                social[f"{platform}_url"] = cleaned
                break

    return social


def detect_booking(page_content):
    """Detect if the page has online booking."""
    content_lower = page_content.lower()
    for sig in BOOKING_SIGNATURES:
        if sig.lower() in content_lower:
            return True
    return False


def count_doctors(text):
    """Estimate doctor count from page text."""
    count = 0
    for pattern in DOCTOR_TITLES:
        matches = re.findall(pattern, text)
        count += len(matches)
    # Deduplicate rough estimate — titles often appear near each other
    return min(count, 50)  # Cap at 50 as sanity check


def compute_site_score(page, url):
    """Compute a 0-10 site quality score."""
    score = 0
    comments = []

    # 1. SSL (HTTPS)
    if url.startswith("https"):
        score += 1
    else:
        comments.append("No SSL")

    # 2. Mobile viewport meta tag
    viewport = page.query_selector('meta[name="viewport"]')
    if viewport:
        score += 1
    else:
        comments.append("No mobile viewport")

    # 3. Has title tag
    title = page.query_selector('title')
    if title and title.inner_text().strip():
        score += 1

    # 4. Has meta description
    desc = page.query_selector('meta[name="description"]')
    if desc and desc.get_attribute("content"):
        score += 1

    # 5. Has images (basic design quality)
    images = page.query_selector_all('img')
    if len(images) >= 3:
        score += 1

    # 6. Has phone number visible
    body_text = ""
    try:
        body_text = page.inner_text('body', timeout=5000)
    except Exception:
        pass
    if re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', body_text):
        score += 1

    # 7. Has booking/CTA
    if detect_booking(body_text):
        score += 1
        comments.append("Has online booking")

    # 8. Page loads without error
    score += 1  # Already loaded if we got here

    # 9. Has social links
    social = extract_social_urls(body_text + str(page.content()))
    if any(social.values()):
        score += 1

    # 10. Not a template/placeholder page
    if len(body_text) > 500:
        score += 1
    else:
        comments.append("Thin content")

    return min(score, 10), "; ".join(comments)


def enrich_clinic(page, row):
    """Visit clinic website and extract enrichment data."""
    website = row.get("website", "").strip()
    enrichment = {
        "facebook_url": "", "instagram_url": "", "tiktok_url": "",
        "google_review_count": row.get("review_count", ""),
        "doctor_count": "", "staff_count": "",
        "site_score": "0", "has_online_booking": "no", "comments": "",
    }

    if not website:
        enrichment["comments"] = "No website"
        enrichment["site_score"] = "0"
        return enrichment

    # Normalize URL
    if not website.startswith("http"):
        website = f"https://{website}"

    try:
        page.goto(website, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2)
    except PlaywrightTimeout:
        enrichment["comments"] = "Website timeout"
        return enrichment
    except Exception as e:
        enrichment["comments"] = f"Website error: {str(e)[:50]}"
        return enrichment

    # Get page content
    try:
        page_content = page.content()
        body_text = page.inner_text('body', timeout=5000)
    except Exception:
        enrichment["comments"] = "Could not read website content"
        return enrichment

    # Extract social URLs
    social = extract_social_urls(page_content, website)
    enrichment.update(social)

    # Detect booking
    has_booking = detect_booking(page_content + body_text)
    enrichment["has_online_booking"] = "yes" if has_booking else "no"

    # Site score
    score, score_comments = compute_site_score(page, website)
    enrichment["site_score"] = str(score)

    # Try to find team/about page for doctor count
    doctor_count = count_doctors(body_text)
    team_url = None

    # Look for team page link
    links = page.query_selector_all('a[href]')
    for link in links[:50]:  # Check first 50 links
        try:
            href = (link.get_attribute("href") or "").lower()
            text = (link.inner_text() or "").lower()
            combined = href + " " + text
            for pattern in TEAM_LINK_PATTERNS:
                if pattern in combined:
                    team_url = link.get_attribute("href")
                    break
            if team_url:
                break
        except Exception:
            continue

    # Visit team page if found
    if team_url:
        try:
            if not team_url.startswith("http"):
                base = urlparse(website)
                team_url = f"{base.scheme}://{base.netloc}/{team_url.lstrip('/')}"
            page.goto(team_url, wait_until="domcontentloaded", timeout=10000)
            time.sleep(1.5)
            team_text = page.inner_text('body', timeout=5000)
            team_count = count_doctors(team_text)
            if team_count > doctor_count:
                doctor_count = team_count

            # Also check for social URLs on team page
            team_content = page.content()
            team_social = extract_social_urls(team_content, website)
            for k, v in team_social.items():
                if v and not enrichment[k]:
                    enrichment[k] = v
        except Exception:
            pass

    if doctor_count > 0:
        enrichment["doctor_count"] = str(doctor_count)

    # Build comments
    comment_parts = []
    if has_booking:
        comment_parts.append("Has online booking")
    if doctor_count > 5:
        comment_parts.append(f"Large team ({doctor_count} doctors)")
    elif doctor_count == 1:
        comment_parts.append("Single practitioner")
    if not any([enrichment["facebook_url"], enrichment["instagram_url"], enrichment["tiktok_url"]]):
        comment_parts.append("No social media")
    elif enrichment["facebook_url"] and not enrichment["instagram_url"]:
        comment_parts.append("Facebook only")
    if score_comments:
        comment_parts.append(score_comments)

    enrichment["comments"] = "; ".join(comment_parts)

    return enrichment


def main():
    test_mode = "--test" in sys.argv
    start_idx = 0
    for arg in sys.argv:
        if arg.startswith("--start="):
            start_idx = int(arg.split("=")[1])

    print("=" * 60)
    print("NYC Dental Clinics — Website Enrichment")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if test_mode:
        print("TEST MODE: first 5 clinics only")
    print("=" * 60)

    # Load input data
    if not os.path.exists(INPUT_CSV):
        print(f"ERROR: Input file not found: {INPUT_CSV}")
        print("Run 02_scrape_google_maps.py first.")
        sys.exit(1)

    rows = load_csv_rows(INPUT_CSV)
    print(f"Loaded {len(rows)} clinics from {INPUT_CSV}")

    # Load existing enrichment if resuming
    enriched_npis = set()
    if os.path.exists(OUTPUT_CSV) and start_idx > 0:
        existing = load_csv_rows(OUTPUT_CSV)
        enriched_npis = {(r["name"], r["address"]) for r in existing}
        print(f"Loaded {len(enriched_npis)} already-enriched clinics")

    if test_mode:
        rows = rows[:5]

    # Filter to only clinics with websites (skip the rest, just copy them)
    with_website = sum(1 for r in rows if r.get("website", "").strip())
    print(f"Clinics with websites: {with_website}/{len(rows)}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # Headless is fine for website visits
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        enriched_rows = []
        for i, row in enumerate(rows):
            if i < start_idx:
                # Copy without enrichment for rows before start
                for field in ENRICHMENT_FIELDS:
                    row.setdefault(field, "")
                enriched_rows.append(row)
                continue

            name = row.get("name", "Unknown")
            website = row.get("website", "").strip()

            if not website:
                # No website — just set defaults
                for field in ENRICHMENT_FIELDS:
                    row[field] = ""
                row["comments"] = "No website"
                row["site_score"] = "0"
                row["google_review_count"] = row.get("review_count", "")
                enriched_rows.append(row)
                continue

            print(f"[{i+1}/{len(rows)}] {name} — {website[:50]}", end="")

            try:
                enrichment = enrich_clinic(page, row)
                row.update(enrichment)
                score = enrichment.get("site_score", "0")
                booking = "📅" if enrichment.get("has_online_booking") == "yes" else ""
                social = "📱" if any([enrichment["facebook_url"], enrichment["instagram_url"]]) else ""
                print(f" → score:{score} {booking}{social}")
            except Exception as e:
                print(f" → ERROR: {e}")
                for field in ENRICHMENT_FIELDS:
                    row.setdefault(field, "")
                row["comments"] = f"Enrichment error: {str(e)[:50]}"

            enriched_rows.append(row)

            # Save checkpoint every 50 clinics
            if (i + 1) % 50 == 0:
                write_enriched_csv(OUTPUT_CSV, enriched_rows)
                print(f"  --- Checkpoint saved: {i+1}/{len(rows)} ---")

            random_delay(1.0, 2.5)

        browser.close()

    # Final save
    write_enriched_csv(OUTPUT_CSV, enriched_rows)

    # Stats
    scores = [int(r.get("site_score", 0)) for r in enriched_rows if r.get("site_score")]
    with_booking = sum(1 for r in enriched_rows if r.get("has_online_booking") == "yes")
    with_social = sum(1 for r in enriched_rows if r.get("facebook_url") or r.get("instagram_url"))

    print(f"\n{'='*60}")
    print(f"DONE!")
    print(f"Total clinics enriched: {len(enriched_rows)}")
    print(f"Avg site score: {sum(scores)/len(scores):.1f}/10" if scores else "No scores")
    print(f"With online booking: {with_booking}")
    print(f"With social media: {with_social}")
    print(f"Output: {OUTPUT_CSV}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
