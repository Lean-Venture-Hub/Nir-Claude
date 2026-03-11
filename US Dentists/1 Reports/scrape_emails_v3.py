#!/usr/bin/env python3
"""Find dentist emails via NPI API + Healthgrades + Vitals scraping. No Google search.

Strategy:
  1. NPI Registry API (free, no auth) — sometimes has email in endpoint data
  2. Healthgrades profile page — scrape for email/contact
  3. Vitals.com profile page
  4. Yellowpages listing

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
                'iana.org', 'mapbox.com', 'apple.com', 'microsoft.com',
                'healthgrades.com', 'vitals.com', 'yellowpages.com', 'zocdoc.com',
                'brimingtondentalpractice.co.uk', 'guildforddentalpractice.co.uk',
                'rahenydentalcentre'}


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
    # Filter out URL-encoded junk
    if '%' in email_lower:
        return True
    return False


def extract_emails(text):
    found = EMAIL_REGEX.findall(text)
    return list(set(e.lower() for e in found if not is_junk_email(e)))


def parse_doctor_name(raw_name):
    """Parse a raw dentist name into first/last for lookups."""
    name = raw_name.strip()
    # Remove suffixes
    for suffix in ['DDS', 'DMD', 'LLC', 'PC', 'PLLC', 'Inc']:
        name = name.replace(suffix, '')
    name = name.replace('Dr.', '').replace('&', ' ').strip()
    name = re.sub(r'[,:\s]+$', '', name).strip()

    # Handle "Practice Name: Doctor Name" format
    if ':' in name:
        parts = name.split(':')
        name = parts[-1].strip()  # take the doctor part

    parts = name.replace(',', ' ').split()
    # Filter out short initials and common words
    parts = [p for p in parts if len(p) > 1 and p not in
             ['Dental', 'Group', 'Associates', 'Medical', 'General', 'Street',
              'West', 'East', 'North', 'South', 'Pioneer', 'Reunited', 'P.E.G.']]

    if len(parts) >= 2:
        return parts[0], parts[-1]
    elif len(parts) == 1:
        return parts[0], parts[0]
    return None, None


def npi_api_lookup(page, first_name, last_name, state):
    """Query the free NPI Registry API for dentist info."""
    emails = set()
    try:
        url = (f"https://npiregistry.cms.hhs.gov/api/?version=2.1"
               f"&first_name={urllib.parse.quote(first_name)}"
               f"&last_name={urllib.parse.quote(last_name)}"
               f"&state={urllib.parse.quote(state)}"
               f"&taxonomy_description=dentist&limit=5")
        page.goto(url, wait_until="domcontentloaded", timeout=10000)
        time.sleep(1)
        content = page.inner_text('body')

        # NPI API returns JSON - parse for any email-like fields
        try:
            data = json.loads(content)
            for result in data.get('results', []):
                # Check addresses for email
                for addr in result.get('addresses', []):
                    # The API doesn't have email field, but check anyway
                    for key, val in addr.items():
                        if isinstance(val, str) and '@' in val:
                            for e in extract_emails(val):
                                emails.add(e)
                # Check other_names, basic info
                raw = json.dumps(result)
                for e in extract_emails(raw):
                    emails.add(e)
        except json.JSONDecodeError:
            pass

    except Exception as e:
        pass
    return emails


def healthgrades_lookup(page, first_name, last_name, state):
    """Search Healthgrades for the dentist and scrape their profile."""
    emails = set()
    try:
        # Search URL
        url = f"https://www.healthgrades.com/dentist/{first_name.lower()}-{last_name.lower()}"
        page.goto(url, wait_until="domcontentloaded", timeout=12000)
        time.sleep(2)
        content = page.content()
        for e in extract_emails(content):
            emails.add(e)
        # Check mailto links
        for m in re.findall(r'mailto:([^"\'&\s?]+)', content):
            m = m.strip().lower()
            if EMAIL_REGEX.match(m) and not is_junk_email(m):
                emails.add(m)

        # If that didn't work, try search
        if not emails:
            search_url = (f"https://www.healthgrades.com/find-a-doctor/search"
                          f"?what={urllib.parse.quote(first_name + ' ' + last_name)}"
                          f"&category=dentist&state={state}")
            page.goto(search_url, wait_until="domcontentloaded", timeout=12000)
            time.sleep(2)

            # Click first result
            try:
                first_result = page.locator('a[data-qa-target="ProviderDisplayName"]').first
                if first_result.count() > 0:
                    first_result.click()
                    time.sleep(2)
                    content = page.content()
                    for e in extract_emails(content):
                        emails.add(e)
                    for m in re.findall(r'mailto:([^"\'&\s?]+)', content):
                        m = m.strip().lower()
                        if EMAIL_REGEX.match(m) and not is_junk_email(m):
                            emails.add(m)
            except:
                pass

    except:
        pass
    return emails


def vitals_lookup(page, first_name, last_name):
    """Search Vitals.com for the dentist profile."""
    emails = set()
    try:
        url = (f"https://www.vitals.com/search?q="
               f"{urllib.parse.quote(first_name + ' ' + last_name)}&type=name")
        page.goto(url, wait_until="domcontentloaded", timeout=12000)
        time.sleep(2)
        content = page.content()
        for e in extract_emails(content):
            emails.add(e)

        # Try clicking first result
        try:
            first_link = page.locator('a.search-result-doctor-name').first
            if first_link.count() > 0:
                first_link.click()
                time.sleep(2)
                content = page.content()
                for e in extract_emails(content):
                    emails.add(e)
                for m in re.findall(r'mailto:([^"\'&\s?]+)', content):
                    m = m.strip().lower()
                    if EMAIL_REGEX.match(m) and not is_junk_email(m):
                        emails.add(m)
        except:
            pass
    except:
        pass
    return emails


def yellowpages_lookup(page, name, city, state):
    """Search YellowPages for the business."""
    emails = set()
    try:
        url = (f"https://www.yellowpages.com/search?search_terms="
               f"{urllib.parse.quote(name)}&geo_location_terms="
               f"{urllib.parse.quote(city + ', ' + state)}")
        page.goto(url, wait_until="domcontentloaded", timeout=12000)
        time.sleep(2)

        # Click first result
        try:
            first_link = page.locator('a.business-name').first
            if first_link.count() > 0:
                first_link.click()
                time.sleep(2)
                content = page.content()
                for e in extract_emails(content):
                    emails.add(e)
                for m in re.findall(r'mailto:([^"\'&\s?]+)', content):
                    m = m.strip().lower()
                    if EMAIL_REGEX.match(m) and not is_junk_email(m):
                        emails.add(m)
        except:
            pass
    except:
        pass
    return emails


def main():
    # Load progress
    progress = {}
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
            progress = json.load(f)

    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Searching emails for {len(rows)} dentists (directories + NPI API)...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            locale="en-US",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )
        page = context.new_page()

        for i, d in enumerate(rows):
            name = d['name'].strip()
            address = d.get('address', '').strip()

            city_match = re.search(r',\s*([A-Za-z\s]+),\s*([A-Z]{2})\s', address)
            city = city_match.group(1).strip() if city_match else ''
            state = city_match.group(2).strip() if city_match else ''

            first_name, last_name = parse_doctor_name(name)

            # Skip if already found email
            existing = progress.get(name, {})
            if existing.get('emails') and existing.get('source', '').startswith('v3'):
                print(f"  [{i+1:2d}] {name} — already found: {existing['emails']}")
                continue
            if existing.get('source') == 'v3_checked':
                print(f"  [{i+1:2d}] {name} — already checked v3, no email")
                continue

            print(f"  [{i+1:2d}] {name} ({first_name} {last_name}, {city} {state})...", end=" ", flush=True)
            all_emails = set()

            if first_name and last_name:
                # 1. NPI API
                npi_found = npi_api_lookup(page, first_name, last_name, state)
                all_emails.update(npi_found)
                if npi_found:
                    print(f"NPI: {npi_found}", end=" ")

                # 2. Healthgrades
                if not all_emails:
                    hg_found = healthgrades_lookup(page, first_name, last_name, state)
                    all_emails.update(hg_found)
                    if hg_found:
                        print(f"HG: {hg_found}", end=" ")

                # 3. Vitals
                if not all_emails:
                    vit_found = vitals_lookup(page, first_name, last_name)
                    all_emails.update(vit_found)
                    if vit_found:
                        print(f"Vitals: {vit_found}", end=" ")

            # 4. YellowPages (works for practice names too)
            if not all_emails:
                yp_found = yellowpages_lookup(page, name, city, state)
                all_emails.update(yp_found)
                if yp_found:
                    print(f"YP: {yp_found}", end=" ")

            emails_list = list(all_emails)
            if emails_list:
                print(f"FOUND: {emails_list}")
                progress[name] = {"emails": emails_list, "source": "v3_directories"}
            else:
                print("no email found")
                progress[name] = {"emails": [], "source": "v3_checked"}

            # Save after each
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)

        browser.close()

    # Summary
    found = sum(1 for v in progress.values() if v.get('emails'))
    total_emails = sum(len(v.get('emails', [])) for v in progress.values())
    print(f"\nDone! Found {total_emails} emails for {found}/{len(rows)} dentists")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
