#!/usr/bin/env python3
"""
Dental Clinics Enrichment Script
Enriches gush-dan-dental-clinics.csv with:
  - easy.co.il data (score, reviews, social links)
  - Website analysis (social links, staff counts, site quality score)

Usage:
  python3 enrich_dental_clinics.py          # Full run (both passes)
  python3 enrich_dental_clinics.py --test   # First 5 clinics only
  python3 enrich_dental_clinics.py --easy-only   # Only easy.co.il pass
  python3 enrich_dental_clinics.py --web-only    # Only website pass
"""

import csv
import os
import re
import sys
import time
import random
from datetime import datetime
from urllib.parse import quote, urlparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# --- Config ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "gush-dan-dental-clinics.csv")
BROWSER_PROFILE = os.path.join(SCRIPT_DIR, ".browser-profile")

ORIGINAL_FIELDS = [
    "name", "address", "city", "phone", "website", "rating",
    "review_count", "categories", "hours", "google_maps_url",
    "search_term", "scraped_at",
]

NEW_FIELDS = [
    "facebook_url", "instagram_url", "tiktok_url",
    "easy_url", "easy_score", "easy_review_count",
    "google_review_count", "facebook_review_count", "madreviews_count",
    "doctor_count", "staff_count", "site_score", "comments",
]

ALL_FIELDS = ORIGINAL_FIELDS + NEW_FIELDS


# --- Utility ---

def random_delay(min_s=2.0, max_s=4.0):
    time.sleep(random.uniform(min_s, max_s))


def short_delay(min_s=0.5, max_s=1.5):
    time.sleep(random.uniform(min_s, max_s))


def log(msg):
    print(f"  {msg}")


def normalize_name(name):
    """Normalize clinic name for fuzzy matching."""
    if not name:
        return ""
    # Remove quotes, extra spaces, common prefixes
    n = name.replace('"', '').replace("'", "").replace("'", "").strip()
    n = re.sub(r'\s+', ' ', n)
    return n.lower()


def names_match(name1, name2):
    """Fuzzy check if two clinic names likely refer to the same place."""
    n1 = normalize_name(name1)
    n2 = normalize_name(name2)
    if not n1 or not n2:
        return False
    # Exact match
    if n1 == n2:
        return True
    # One contains the other
    if n1 in n2 or n2 in n1:
        return True
    # Check word overlap (at least 2 shared meaningful words)
    words1 = set(w for w in n1.split() if len(w) > 2)
    words2 = set(w for w in n2.split() if len(w) > 2)
    overlap = words1 & words2
    if len(overlap) >= 2:
        return True
    return False


def city_matches(csv_city, easy_text):
    """Check if the city from CSV appears in easy.co.il text."""
    if not csv_city or not easy_text:
        return True  # Can't verify, assume match
    city_lower = csv_city.strip().lower()
    text_lower = easy_text.strip().lower()
    # Direct match
    if city_lower in text_lower:
        return True
    # Common city name variants
    variants = {
        "תל אביב": ["תל-אביב", "תל אביב-יפו", "תל אביב יפו"],
        "פתח תקווה": ["פתח-תקווה", "פ\"ת"],
        "ראשון לציון": ["ראשון-לציון", "ראשל\"צ"],
        "בני ברק": ["בני-ברק"],
        "בת ים": ["בת-ים"],
        "רמת גן": ["רמת-גן"],
        "כפר סבא": ["כפר-סבא"],
        "הוד השרון": ["הוד-השרון"],
        "רמת השרון": ["רמת-השרון"],
        "קרית אונו": ["קריית אונו"],
    }
    for base, alts in variants.items():
        if city_lower in [base] + alts:
            for check in [base] + alts:
                if check in text_lower:
                    return True
    return False


# --- CSV I/O ---

def load_csv():
    """Load CSV into list of dicts, adding new columns if missing."""
    rows = []
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV not found at {CSV_PATH}")
        sys.exit(1)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Ensure all new columns exist
            for field in NEW_FIELDS:
                if field not in row:
                    row[field] = ""
            rows.append(row)
    print(f"Loaded {len(rows)} clinics from CSV")
    return rows


def save_csv(rows):
    """Write all rows back to CSV."""
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ALL_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


# --- Pass 1: easy.co.il ---

def dismiss_easy_cookies(page):
    """Handle easy.co.il cookie consent."""
    try:
        for selector in [
            'button:has-text("אישור")',
            'button:has-text("הסכמה")',
            'button:has-text("אני מסכים")',
            'button:has-text("קבל")',
            'button:has-text("Accept")',
            '.cookie-consent button',
            '[class*="cookie"] button',
            '[class*="consent"] button',
            '[id*="cookie"] button',
        ]:
            btn = page.query_selector(selector)
            if btn and btn.is_visible():
                btn.click()
                log("Dismissed cookie dialog")
                short_delay()
                return True
    except Exception:
        pass
    return False


def handle_captcha(page):
    """Detect and handle easy.co.il captcha. Returns True if captcha was resolved."""
    if "captcha" in page.url.lower():
        print("\n  *** CAPTCHA DETECTED! ***")
        print("  Please solve the captcha in the browser window.")
        print("  Waiting for you to solve it...\n")
        # Wait up to 2 minutes for the user to solve
        for _ in range(120):
            time.sleep(1)
            if "captcha" not in page.url.lower():
                print("  Captcha resolved! Continuing...")
                time.sleep(2)
                return True
        print("  Captcha timeout. Skipping...")
        return False
    return True  # No captcha


def search_easy(page, clinic_name):
    """Search easy.co.il for a clinic. Returns list of result elements info with pre-parsed data."""
    encoded = quote(clinic_name)
    url = f"https://easy.co.il/search/{encoded}"

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        random_delay(3, 5)
    except PlaywrightTimeout:
        log("easy.co.il search timed out")
        return []

    # Check for captcha
    if not handle_captcha(page):
        return []

    # If captcha redirected us away from search, re-navigate
    if "/search/" not in page.url:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            random_delay(3, 5)
            if not handle_captcha(page):
                return []
        except PlaywrightTimeout:
            return []

    # Dismiss cookies on first visit
    dismiss_easy_cookies(page)
    short_delay(0.5, 1.0)

    # Wait for results
    try:
        page.wait_for_selector('[class*="biz_title"], [class*="bizTitle"], .biz-title, a[href*="/page/"]', timeout=10000)
    except PlaywrightTimeout:
        # Try scrolling down to trigger lazy loading
        try:
            page.evaluate("window.scrollBy(0, 300)")
            short_delay(1.5, 2.5)
            page.wait_for_selector('a[href*="/page/"]', timeout=5000)
        except Exception:
            log("No results loaded on easy.co.il")
            return []

    # Collect results - look for links to business pages
    results = []
    links = page.query_selector_all('a[href*="/page/"]')
    for link in links[:5]:  # Check top 5 results
        try:
            href = link.get_attribute("href") or ""
            text = link.inner_text().strip()
            if "/page/" in href and text:
                full_url = href if href.startswith("http") else f"https://easy.co.il{href}"
                # Pre-parse score and review count from search result text
                score = ""
                review_count = ""
                score_match = re.search(r'ציון העסק\s*(\d+\.?\d*)', text)
                if not score_match:
                    score_match = re.search(r'(\d+\.\d)\n', text)
                if score_match and 0 < float(score_match.group(1)) <= 10:
                    score = score_match.group(1)
                review_match = re.search(r'(\d+)\s*ביקורות', text)
                if review_match:
                    review_count = review_match.group(1)
                results.append({
                    "url": full_url,
                    "text": text,
                    "score": score,
                    "review_count": review_count,
                })
        except Exception:
            continue

    return results


def extract_easy_detail(page, easy_url, pre_score="", pre_review_count=""):
    """Extract data from an easy.co.il business detail page.
    pre_score and pre_review_count come from search results parsing."""
    data = {
        "easy_url": easy_url,
        "easy_score": pre_score,
        "easy_review_count": pre_review_count,
        "google_review_count": "",
        "facebook_review_count": "",
        "madreviews_count": "",
        "facebook_url": "",
    }

    try:
        page.goto(easy_url, wait_until="domcontentloaded", timeout=15000)
        random_delay(2, 4)
    except PlaywrightTimeout:
        log("easy.co.il detail page timed out")
        return data

    # Try to extract score from detail page if not already parsed
    if not data["easy_score"]:
        try:
            body_text = page.inner_text("body")
            score_match = re.search(r'ציון העסק\s*(\d+\.?\d*)', body_text)
            if not score_match:
                score_match = re.search(r'ציון[:\s]*(\d+\.\d)', body_text)
            if score_match and 0 < float(score_match.group(1)) <= 10:
                data["easy_score"] = score_match.group(1)
        except Exception:
            pass

    # Try to extract review count from detail page if not already parsed
    if not data["easy_review_count"]:
        try:
            body_text = page.inner_text("body")
            for pattern in [r'(\d+)\s*ביקורות', r'(\d+)\s*חוות דעת']:
                match = re.search(pattern, body_text)
                if match:
                    data["easy_review_count"] = match.group(1)
                    break
        except Exception:
            pass

    # Extract Facebook URL from links section — filter out easy.co.il's own links
    try:
        all_links = page.query_selector_all('a[href*="facebook.com"]')
        for link in all_links:
            href = link.get_attribute("href") or ""
            href_lower = href.lower()
            # Skip share links, easy.co.il's own page, and generic links
            if ("facebook.com" in href_lower
                    and "/sharer" not in href_lower
                    and "share.php" not in href_lower
                    and "easy.co.il" not in href_lower
                    and "easyil" not in href_lower):
                data["facebook_url"] = href
                break
    except Exception:
        pass

    # Click "מהרשת" (from the web) tab to get review breakdowns
    try:
        network_tab = None
        for sel in [
            'button:has-text("מהרשת")',
            'a:has-text("מהרשת")',
            '[role="tab"]:has-text("מהרשת")',
        ]:
            el = page.query_selector(sel)
            if el and el.is_visible():
                network_tab = el
                break

        if network_tab:
            network_tab.click()
            short_delay(2.0, 4.0)

            # Get all text from the page after tab click
            tab_text = page.inner_text("body")

            # Google Maps reviews - try multiple patterns
            for pattern in [
                r'(?:google\s*maps?)\D*?(\d+)\s*(?:ביקורות|חוות)',
                r'(?:google\s*maps?)\D*?(\d+)',
                r'גוגל\D*?(\d+)\s*(?:ביקורות|חוות)',
            ]:
                google_match = re.search(pattern, tab_text, re.IGNORECASE)
                if google_match:
                    data["google_review_count"] = google_match.group(1)
                    break

            # Facebook reviews
            for pattern in [
                r'(?:facebook|פייסבוק)\D*?(\d+)\s*(?:ביקורות|חוות|המלצות)',
                r'(?:facebook|פייסבוק)\D*?(\d+)',
            ]:
                fb_match = re.search(pattern, tab_text, re.IGNORECASE)
                if fb_match:
                    data["facebook_review_count"] = fb_match.group(1)
                    break

            # Madreviews
            for pattern in [
                r'(?:madreview|מדרביו)\D*?(\d+)',
            ]:
                mad_match = re.search(pattern, tab_text, re.IGNORECASE)
                if mad_match:
                    data["madreviews_count"] = mad_match.group(1)
                    break

            # Alternative: look for structured review source elements
            if not data["google_review_count"] and not data["facebook_review_count"]:
                # Try finding link elements that point to review sources
                review_links = page.query_selector_all('a[href*="google"], a[href*="facebook"]')
                for rlink in review_links:
                    try:
                        rtext = rlink.inner_text().strip()
                        rhref = (rlink.get_attribute("href") or "").lower()
                        count_match = re.search(r'(\d+)', rtext)
                        if not count_match:
                            continue
                        count = count_match.group(1)
                        if 'google' in rhref and not data["google_review_count"]:
                            data["google_review_count"] = count
                        elif 'facebook' in rhref and not data["facebook_review_count"]:
                            data["facebook_review_count"] = count
                    except Exception:
                        continue
        else:
            log("Could not find מהרשת tab")
    except Exception as e:
        log(f"Network tab error: {e}")

    return data


def run_easy_pass(page, rows, test_mode=False):
    """Pass 1: Enrich from easy.co.il."""
    print("\n" + "=" * 60)
    print("PASS 1: easy.co.il enrichment")
    print("=" * 60)

    to_process = []
    for i, row in enumerate(rows):
        # Skip if already has easy data
        if row.get("easy_url"):
            continue
        to_process.append(i)

    if test_mode:
        to_process = to_process[:5]

    print(f"Processing {len(to_process)} clinics on easy.co.il")
    if not to_process:
        print("All clinics already have easy.co.il data. Skipping.")
        return

    found_count = 0
    consecutive_failures = 0
    MAX_CONSECUTIVE_FAILURES = 4  # After this many, do a long cooldown
    COOLDOWN_SECONDS = 90  # Pause when rate-limited

    for progress, idx in enumerate(to_process):
        row = rows[idx]
        name = row.get("name", "").strip()
        city = row.get("city", "").strip()

        if not name:
            continue

        print(f"\n[{progress+1}/{len(to_process)}] Searching: {name}")

        try:
            results = search_easy(page, name)

            if not results:
                consecutive_failures += 1
                log(f"No results found ({consecutive_failures} consecutive failures)")

                if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                    log(f"Possible rate limit! Pausing {COOLDOWN_SECONDS}s...")
                    # Navigate to homepage to check for captcha
                    try:
                        page.goto("https://easy.co.il", wait_until="domcontentloaded", timeout=10000)
                        handle_captcha(page)
                        dismiss_easy_cookies(page)
                    except Exception:
                        pass
                    time.sleep(COOLDOWN_SECONDS)
                    consecutive_failures = 0

                    # Retry this clinic after cooldown
                    log("Retrying after cooldown...")
                    results = search_easy(page, name)
                    if not results:
                        log("Still no results after retry")
                        random_delay(4, 8)
                        continue
                else:
                    random_delay(4, 8)
                    continue

            # Reset failure counter on any results
            consecutive_failures = 0

            # Find best match
            matched = None
            for r in results:
                if names_match(name, r["text"]) and city_matches(city, r["text"]):
                    matched = r
                    break

            # If no match by name+city, try just name with first result
            if not matched and results:
                if names_match(name, results[0]["text"]):
                    matched = results[0]

            if not matched:
                log(f"No matching result (top: '{results[0]['text'][:60]}')")
                random_delay(3, 6)
                continue

            log(f"Matched: {matched['text'][:60]}")

            # Visit detail page (pass pre-parsed score/count from search results)
            easy_data = extract_easy_detail(
                page, matched["url"],
                pre_score=matched.get("score", ""),
                pre_review_count=matched.get("review_count", ""),
            )

            # Merge data into row
            for key, val in easy_data.items():
                if val:  # Only overwrite if we have data
                    if key == "facebook_url" and row.get("facebook_url"):
                        continue  # Don't overwrite existing
                    rows[idx][key] = val

            found_count += 1
            score_str = f" | Score: {easy_data['easy_score']}" if easy_data['easy_score'] else ""
            reviews_str = f" | Reviews: {easy_data['easy_review_count']}" if easy_data['easy_review_count'] else ""
            log(f"OK{score_str}{reviews_str}")

        except Exception as e:
            log(f"Error: {e}")
            consecutive_failures += 1
            continue

        # Save after each clinic
        save_csv(rows)
        random_delay(3, 6)

    print(f"\nPass 1 complete: {found_count}/{len(to_process)} clinics enriched from easy.co.il")


# --- Pass 2: Website analysis ---

def extract_social_links(page):
    """Extract social media links from current page."""
    social = {"facebook_url": "", "instagram_url": "", "tiktok_url": ""}

    try:
        all_links = page.query_selector_all("a[href]")
        for link in all_links:
            try:
                href = (link.get_attribute("href") or "").strip()
                if not href:
                    continue

                href_lower = href.lower()

                # Facebook (skip share/sharer links)
                if "facebook.com" in href_lower and not social["facebook_url"]:
                    if "/sharer" not in href_lower and "share.php" not in href_lower:
                        social["facebook_url"] = href

                # Instagram
                if "instagram.com" in href_lower and not social["instagram_url"]:
                    if "/p/" not in href_lower:  # Skip individual post links
                        social["instagram_url"] = href

                # TikTok
                if "tiktok.com" in href_lower and not social["tiktok_url"]:
                    social["tiktok_url"] = href

            except Exception:
                continue
    except Exception:
        pass

    return social


def find_team_page(page, base_url):
    """Try to find and navigate to team/about page. Returns True if found."""
    team_patterns = ['צוות', 'הצוות', 'team', 'about', 'רופאים', 'הרופאים', 'staff', 'doctors']

    try:
        all_links = page.query_selector_all("a[href]")
        for link in all_links:
            try:
                href = (link.get_attribute("href") or "").strip()
                text = (link.inner_text() or "").strip().lower()
                href_lower = href.lower()

                for pattern in team_patterns:
                    if pattern in text or pattern in href_lower:
                        # Build full URL if relative
                        if href.startswith("/"):
                            parsed = urlparse(base_url)
                            href = f"{parsed.scheme}://{parsed.netloc}{href}"
                        elif not href.startswith("http"):
                            href = f"{base_url.rstrip('/')}/{href}"

                        page.goto(href, wait_until="domcontentloaded", timeout=8000)
                        short_delay(1, 2)
                        return True
            except Exception:
                continue
    except Exception:
        pass

    return False


def count_staff(page):
    """Count doctors and other staff from current page text."""
    doctor_count = 0
    staff_count = 0

    try:
        body_text = page.inner_text("body")

        # Count doctor patterns
        doctor_patterns = [r'ד"ר', r"דר'", r'Dr\.', r"פרופ'", r'Prof\.', r'פרופסור']
        for pattern in doctor_patterns:
            matches = re.findall(pattern, body_text)
            doctor_count += len(matches)

        # Count other staff patterns
        staff_patterns = [r'שיננית', r'סייעת', r'טכנאי', r'מנהלת', r'היגיניסטית', r'רופא שיניים']
        for pattern in staff_patterns:
            matches = re.findall(pattern, body_text)
            staff_count += len(matches)

    except Exception:
        pass

    return doctor_count, staff_count


def calculate_site_score(page, url, social_links, has_team_page):
    """Calculate 1-10 website quality score."""
    score = 0
    comments = []

    try:
        # 1. Site loads (we're here, so yes)
        score += 1

        # 2. HTTPS
        if url.startswith("https"):
            score += 1

        # 3. Has team/staff page
        if has_team_page:
            score += 1

        # 4. Has online booking
        body_html = page.content()
        body_lower = body_html.lower()
        booking_indicators = [
            'calendly.com', 'acuity', 'fresha.com', 'booking', 'הזמן תור',
            'קבע תור', 'schedule', 'appointment', 'זמן תור', 'setmore',
            'clinicminds', 'תור', 'book-now', 'book_now',
        ]
        has_booking = any(ind in body_lower for ind in booking_indicators)
        if has_booking:
            score += 1
            comments.append("Has online booking")

        # 5. Has social media
        has_social = any(social_links.values())
        if has_social:
            score += 1

        # 6. Has treatments/services page
        service_patterns = ['טיפולים', 'שירותים', 'services', 'treatments', 'procedures']
        has_services = any(p in body_lower for p in service_patterns)
        if has_services:
            score += 1

        # 7. Has multiple pages (3+ internal nav links)
        parsed = urlparse(url)
        base_domain = parsed.netloc
        internal_links = page.query_selector_all(f'a[href*="{base_domain}"], a[href^="/"]')
        nav_links = set()
        for link in internal_links:
            try:
                href = link.get_attribute("href") or ""
                if href and href != "/" and href != url and "#" not in href:
                    nav_links.add(href)
            except Exception:
                continue
        if len(nav_links) >= 3:
            score += 1

        # 8. Has contact form/email
        has_contact = (
            '<form' in body_lower
            or 'mailto:' in body_lower
            or 'contact' in body_lower
            or 'צור קשר' in body_lower
        )
        if has_contact:
            score += 1

        # 9. Mobile responsive (viewport meta)
        has_viewport = 'viewport' in body_lower
        if has_viewport:
            score += 1

        # 10. Content richness (500+ words)
        try:
            visible_text = page.inner_text("body")
            word_count = len(visible_text.split())
            if word_count >= 500:
                score += 1
        except Exception:
            pass

    except Exception as e:
        log(f"Score calculation error: {e}")

    return score, comments


def analyze_website(page, row):
    """Analyze a clinic's website. Returns dict of new data."""
    url = row.get("website", "").strip()
    data = {
        "facebook_url": row.get("facebook_url", ""),
        "instagram_url": row.get("instagram_url", ""),
        "tiktok_url": row.get("tiktok_url", ""),
        "doctor_count": "",
        "staff_count": "",
        "site_score": "",
        "comments": row.get("comments", ""),
    }

    if not url or not url.startswith("http"):
        data["site_score"] = "0"
        data["comments"] = "No website"
        return data

    # Check if site is just a Facebook page
    if "facebook.com" in url.lower():
        data["facebook_url"] = url
        data["site_score"] = "1"
        data["comments"] = "Site is just a Facebook page"
        return data

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=10000)
        short_delay(1.5, 3.0)
    except PlaywrightTimeout:
        data["site_score"] = "0"
        data["comments"] = "Website down/timeout"
        return data
    except Exception as e:
        data["site_score"] = "0"
        data["comments"] = f"Website error"
        return data

    # Extract social links
    social = extract_social_links(page)

    # Merge social - prefer website links but don't overwrite easy.co.il data
    for key in ["facebook_url", "instagram_url", "tiktok_url"]:
        if social[key] and not data[key]:
            data[key] = social[key]

    # Find and visit team page
    has_team_page = find_team_page(page, url)
    if has_team_page:
        doctors, staff = count_staff(page)
        data["doctor_count"] = str(doctors) if doctors else ""
        data["staff_count"] = str(staff) if staff else ""

        # Also check for social links on team page
        team_social = extract_social_links(page)
        for key in ["facebook_url", "instagram_url", "tiktok_url"]:
            if team_social[key] and not data[key]:
                data[key] = team_social[key]

        # Navigate back to homepage for scoring
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=8000)
            short_delay(1, 2)
        except Exception:
            pass
    else:
        # Try counting staff from main page
        doctors, staff = count_staff(page)
        data["doctor_count"] = str(doctors) if doctors else ""
        data["staff_count"] = str(staff) if staff else ""

    # Calculate site score
    score, auto_comments = calculate_site_score(page, url, social, has_team_page)
    data["site_score"] = str(score)

    # Build comments
    all_comments = []
    if auto_comments:
        all_comments.extend(auto_comments)

    doctors = int(data["doctor_count"]) if data["doctor_count"] else 0
    if doctors == 0 and not has_team_page:
        pass  # Don't comment on missing staff if no team page
    elif doctors == 1:
        all_comments.append("Single practitioner")
    elif doctors >= 5:
        all_comments.append(f"Large team ({doctors} doctors)")

    if not any([data["facebook_url"], data["instagram_url"], data["tiktok_url"]]):
        all_comments.append("No social media")
    elif data["facebook_url"] and not data["instagram_url"]:
        all_comments.append("Facebook only")

    if all_comments:
        existing = data.get("comments", "")
        new_comments = "; ".join(all_comments)
        data["comments"] = f"{existing}; {new_comments}".strip("; ") if existing else new_comments

    return data


def run_website_pass(page, rows, test_mode=False):
    """Pass 2: Analyze clinic websites."""
    print("\n" + "=" * 60)
    print("PASS 2: Website analysis")
    print("=" * 60)

    to_process = []
    for i, row in enumerate(rows):
        # Skip if already scored
        if row.get("site_score"):
            continue
        to_process.append(i)

    if test_mode:
        to_process = to_process[:5]

    print(f"Processing {len(to_process)} clinic websites")
    if not to_process:
        print("All clinics already have site scores. Skipping.")
        return

    analyzed_count = 0

    for progress, idx in enumerate(to_process):
        row = rows[idx]
        name = row.get("name", "").strip()
        website = row.get("website", "").strip()

        print(f"\n[{progress+1}/{len(to_process)}] {name}")
        if website:
            log(f"URL: {website[:60]}...")

        try:
            web_data = analyze_website(page, row)

            # Merge into row
            for key, val in web_data.items():
                if val:  # Only overwrite if we have data
                    rows[idx][key] = val
                elif key == "site_score":  # Always write score, even if 0
                    rows[idx][key] = val

            analyzed_count += 1
            score = web_data.get("site_score", "?")
            comments = web_data.get("comments", "")
            log(f"Score: {score}/10" + (f" | {comments}" if comments else ""))

        except Exception as e:
            log(f"Error: {e}")
            rows[idx]["site_score"] = "0"
            rows[idx]["comments"] = "Analysis error"

        # Save after each clinic
        save_csv(rows)
        random_delay(1.5, 3.5)

    print(f"\nPass 2 complete: {analyzed_count}/{len(to_process)} websites analyzed")


# --- Main ---

def main():
    test_mode = "--test" in sys.argv
    easy_only = "--easy-only" in sys.argv
    web_only = "--web-only" in sys.argv

    print("=" * 60)
    print("Dental Clinics Enrichment Script")
    print(f"Mode: {'TEST (5 clinics)' if test_mode else 'FULL RUN'}")
    if easy_only:
        print("Running: easy.co.il pass only")
    elif web_only:
        print("Running: Website pass only")
    else:
        print("Running: Both passes")
    print(f"CSV: {CSV_PATH}")
    print("=" * 60)

    # Load data
    rows = load_csv()

    with sync_playwright() as p:
        # Use persistent browser profile to preserve cookies/captcha state
        context = p.chromium.launch_persistent_context(
            BROWSER_PROFILE,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--lang=he-IL",
            ],
            locale="he-IL",
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        )
        page = context.pages[0] if context.pages else context.new_page()

        try:
            # Warm up: visit easy.co.il homepage first and handle captcha
            if not web_only:
                print("\nWarming up: visiting easy.co.il...")
                print("If a CAPTCHA appears, solve it in the browser window.")
                try:
                    page.goto("https://easy.co.il", wait_until="domcontentloaded", timeout=15000)
                    time.sleep(3)
                    handle_captcha(page)
                    dismiss_easy_cookies(page)
                    # Do a test search to verify we're not blocked
                    page.goto("https://easy.co.il/search/%D7%9E%D7%9B%D7%91%D7%99%D7%93%D7%A0%D7%98", wait_until="domcontentloaded", timeout=15000)
                    time.sleep(3)
                    if not handle_captcha(page):
                        print("WARNING: Could not clear captcha. easy.co.il pass may fail.")
                    else:
                        print("Warm-up complete - easy.co.il is accessible")
                except Exception as e:
                    print(f"Warm-up error: {e}")
                random_delay(2, 4)

            # Pass 1: easy.co.il
            if not web_only:
                run_easy_pass(page, rows, test_mode)
                save_csv(rows)

            # Pass 2: Websites
            if not easy_only:
                run_website_pass(page, rows, test_mode)
                save_csv(rows)

        except KeyboardInterrupt:
            print("\n\nInterrupted! Saving progress...")
            save_csv(rows)
            print("Progress saved.")
        except Exception as e:
            print(f"\nFATAL ERROR: {e}")
            save_csv(rows)
            print("Progress saved despite error.")
        finally:
            context.close()

    # Final stats
    print("\n" + "=" * 60)
    print("ENRICHMENT COMPLETE")
    easy_count = sum(1 for r in rows if r.get("easy_url"))
    scored_count = sum(1 for r in rows if r.get("site_score"))
    fb_count = sum(1 for r in rows if r.get("facebook_url"))
    ig_count = sum(1 for r in rows if r.get("instagram_url"))
    print(f"  easy.co.il matched: {easy_count}/{len(rows)}")
    print(f"  Websites scored: {scored_count}/{len(rows)}")
    print(f"  Facebook URLs: {fb_count}")
    print(f"  Instagram URLs: {ig_count}")
    print(f"  Output: {CSV_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
