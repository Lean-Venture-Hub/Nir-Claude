#!/usr/bin/env python3
"""Find dentist emails by scraping Google search results and dental directories.

Strategy:
  1. Google search "[dentist name] [city] email"
  2. Visit top results looking for email addresses
  3. Try Healthgrades, Vitals, Zocdoc profile pages
  4. Try NPI registry lookup

Saves progress after each dentist.
"""

import csv, json, os, re, time, urllib.parse
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "first_batch.csv")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "emails.json")

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
JUNK_DOMAINS = {'sentry.io', 'noreply', 'example.com', 'test.com', 'wixpress.com',
                'googleapis.com', 'schema.org', 'cloudflare.com', 'w3.org',
                'google.com', 'facebook.com', 'instagram.com', 'twitter.com',
                'youtube.com', 'squarespace.com', 'godaddy.com', 'wordpress.com',
                'wix.com', 'weebly.com', 'gstatic.com', 'pki.goog', 'mozilla.org',
                'iana.org', 'openstreetmap.org', 'mapbox.com', 'apple.com',
                'microsoft.com', 'outlook.com', 'hotmail.com', 'icloud.com'}


def is_junk_email(email):
    email_lower = email.lower()
    domain = email_lower.split('@')[-1] if '@' in email_lower else ''
    for junk in JUNK_DOMAINS:
        if junk in domain:
            return True
    if email_lower.endswith(('.png', '.jpg', '.gif', '.svg', '.css', '.js')):
        return True
    if len(email_lower.split('@')[0]) < 2:
        return True
    return False


def extract_emails_from_text(text):
    """Find all valid emails in text."""
    found = EMAIL_REGEX.findall(text)
    return [e.lower() for e in found if not is_junk_email(e)]


def google_search_emails(page, query):
    """Search Google and scrape emails from top results."""
    emails = set()
    urls_to_check = []

    try:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=en"
        page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2)

        # Extract emails from search results page itself (snippets)
        content = page.content()
        for e in extract_emails_from_text(content):
            emails.add(e)

        # Collect URLs from search results to visit
        links = page.locator('a[href]').all()
        for link in links[:20]:
            try:
                href = link.get_attribute('href') or ''
                if href.startswith('http') and 'google' not in href:
                    # Prioritize dental directories
                    if any(d in href for d in ['healthgrades', 'vitals', 'zocdoc',
                                                 'webmd', 'npidb', 'yellowpages',
                                                 'yelp', 'bbb.org', 'dentist']):
                        urls_to_check.insert(0, href)
                    elif len(urls_to_check) < 5:
                        urls_to_check.append(href)
            except:
                continue

    except Exception as e:
        print(f"(search err: {e})", end=" ")

    # Visit top results
    for url in urls_to_check[:5]:
        if emails:
            break
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
            time.sleep(1)
            content = page.content()
            for e in extract_emails_from_text(content):
                emails.add(e)
            # Check mailto links
            for m in re.findall(r'mailto:([^"\'&\s?]+)', content):
                m = m.strip().lower()
                if EMAIL_REGEX.match(m) and not is_junk_email(m):
                    emails.add(m)
        except:
            continue

    return list(emails)


def search_npi_for_email(page, doctor_name):
    """Search NPI registry for practice email (sometimes listed)."""
    emails = set()
    try:
        # Clean name for search
        name = doctor_name.replace('DDS', '').replace('DMD', '').replace('Dr.', '').strip()
        name = re.sub(r'\s*(LLC|PC|Inc|PLLC)\s*$', '', name).strip()
        parts = name.replace(',', ' ').split()

        if len(parts) >= 2:
            # Try NPPES NPI lookup
            url = f"https://npiregistry.cms.hhs.gov/api/?version=2.1&first_name={urllib.parse.quote(parts[0])}&last_name={urllib.parse.quote(parts[-1])}&taxonomy_description=dentist&limit=5"
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
            time.sleep(1)
            content = page.inner_text('body')
            for e in extract_emails_from_text(content):
                emails.add(e)
    except:
        pass
    return list(emails)


def main():
    # Load progress
    progress = {}
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
            progress = json.load(f)

    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Searching emails for {len(rows)} dentists...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            locale="en-US",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )
        page = context.new_page()

        # Open Google first so user can solve CAPTCHA
        print("Opening Google — please solve the CAPTCHA if it appears...")
        page.goto("https://www.google.com/search?q=dentist+email", wait_until="domcontentloaded", timeout=15000)
        print("Waiting 20 seconds for you to solve CAPTCHA...")
        time.sleep(20)
        print("Continuing!\n")

        for i, d in enumerate(rows):
            name = d['name'].strip()
            city_raw = d.get('city', '').strip()
            address = d.get('address', '').strip()

            # Extract city from address if needed
            city_match = re.search(r',\s*([A-Za-z\s]+),\s*[A-Z]{2}\s', address)
            city = city_match.group(1).strip() if city_match else city_raw

            # Skip if already found email
            existing = progress.get(name, {})
            if existing.get('emails'):
                print(f"  [{i+1:2d}] {name} — already found: {existing['emails']}")
                continue
            # Skip if already tried v2
            if existing.get('source') == 'v2_checked':
                print(f"  [{i+1:2d}] {name} — already checked v2, no email")
                continue

            print(f"  [{i+1:2d}] {name} ({city})...", end=" ", flush=True)
            all_emails = set()

            # Strategy 1: Google search for email
            query = f'"{name}" {city} dentist email'
            found = google_search_emails(page, query)
            all_emails.update(found)

            # Strategy 2: Search without quotes if nothing found
            if not all_emails:
                clean_name = name.replace(',', '').replace(':', '')
                query2 = f'{clean_name} {city} dentist contact email'
                found2 = google_search_emails(page, query2)
                all_emails.update(found2)

            # Strategy 3: NPI lookup
            if not all_emails:
                npi_emails = search_npi_for_email(page, name)
                all_emails.update(npi_emails)

            emails_list = list(all_emails)
            if emails_list:
                print(f"FOUND: {emails_list}")
                progress[name] = {"emails": emails_list, "source": "v2_google_search"}
            else:
                print("no email found")
                progress[name] = {"emails": [], "source": "v2_checked"}

            # Save after each
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)

            # Brief pause to avoid rate limiting
            time.sleep(1)

        browser.close()

    # Summary
    found = sum(1 for v in progress.values() if v.get('emails'))
    total_emails = sum(len(v.get('emails', [])) for v in progress.values())
    print(f"\nDone! Found {total_emails} emails for {found}/{len(rows)} dentists")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
