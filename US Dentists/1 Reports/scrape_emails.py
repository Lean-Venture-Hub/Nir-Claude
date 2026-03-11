#!/usr/bin/env python3
"""Scrape email addresses from Google Maps listings for US dentists.

Checks:
  1. Google Maps "More info" section
  2. Google Maps website link → scrape contact page for email

Saves progress after each dentist.
"""

import csv, json, os, re, time
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "first_batch.csv")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "emails.json")

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
JUNK_EMAILS = {'sentry@', 'noreply@', 'example@', 'test@', 'wixpress', 'googleapis',
               'schema.org', 'cloudflare', 'w3.org', 'google.com', 'facebook.com',
               'instagram.com', 'twitter.com', 'youtube.com', 'squarespace.com',
               'godaddy.com', 'wordpress.com', 'wix.com', 'weebly.com'}


def is_junk_email(email):
    email_lower = email.lower()
    for junk in JUNK_EMAILS:
        if junk in email_lower:
            return True
    if email_lower.endswith('.png') or email_lower.endswith('.jpg'):
        return True
    return False


def extract_email_from_maps(page, url):
    """Try to get email from Google Maps listing."""
    emails = set()
    try:
        page.goto(url + "&hl=en", wait_until="domcontentloaded", timeout=20000)
        time.sleep(3)

        # Method 1: Check the info panel for email/website
        # Look for email in the page content
        content = page.content()
        found = EMAIL_REGEX.findall(content)
        for e in found:
            if not is_junk_email(e):
                emails.add(e.lower())

        # Method 2: Try clicking the website link and scraping that
        if not emails:
            try:
                # Find website link in Maps
                website_link = page.locator('a[data-item-id="authority"]').first
                if website_link.count() > 0:
                    href = website_link.get_attribute('href') or ''
                    if href and 'google' not in href:
                        website_url = href
                    else:
                        website_url = website_link.inner_text().strip()

                    if website_url and not website_url.startswith('http'):
                        website_url = 'https://' + website_url

                    if website_url:
                        emails.update(scrape_website_for_email(page, website_url))
            except:
                pass

    except Exception as e:
        print(f"Maps error: {e}")

    return list(emails)


def scrape_website_for_email(page, base_url):
    """Visit a website and its contact page to find emails."""
    emails = set()

    # Visit homepage
    try:
        page.goto(base_url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2)
        content = page.content()
        found = EMAIL_REGEX.findall(content)
        for e in found:
            if not is_junk_email(e):
                emails.add(e.lower())
    except:
        pass

    # Try common contact page paths
    if not emails:
        for path in ['/contact', '/contact-us', '/about', '/about-us']:
            try:
                url = base_url.rstrip('/') + path
                page.goto(url, wait_until="domcontentloaded", timeout=10000)
                time.sleep(1)
                content = page.content()
                found = EMAIL_REGEX.findall(content)
                for e in found:
                    if not is_junk_email(e):
                        emails.add(e.lower())
                if emails:
                    break
            except:
                continue

    # Try clicking any "Contact" link on the page
    if not emails:
        try:
            page.goto(base_url, wait_until="domcontentloaded", timeout=10000)
            time.sleep(1)
            contact_links = page.locator('a').all()
            for link in contact_links:
                try:
                    text = (link.inner_text() or '').lower().strip()
                    href = (link.get_attribute('href') or '').lower()
                    if 'contact' in text or 'contact' in href:
                        link.click()
                        time.sleep(2)
                        content = page.content()
                        found = EMAIL_REGEX.findall(content)
                        for e in found:
                            if not is_junk_email(e):
                                emails.add(e.lower())
                        if emails:
                            break
                except:
                    continue
        except:
            pass

    # Also check for mailto: links
    try:
        content = page.content()
        mailto = re.findall(r'mailto:([^"\'&\s?]+)', content)
        for e in mailto:
            e = e.strip().lower()
            if EMAIL_REGEX.match(e) and not is_junk_email(e):
                emails.add(e)
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

    print(f"Searching emails for {len(rows)} dentists...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            locale="en-US",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )
        page = context.new_page()

        for i, d in enumerate(rows):
            name = d['name'].strip()
            url = d.get('google_maps_url', '').strip()

            if name in progress:
                status = progress[name]
                if status.get('emails'):
                    print(f"  [{i+1:2d}] {name} — already found: {status['emails']}")
                else:
                    print(f"  [{i+1:2d}] {name} — already checked, no email")
                continue

            if not url:
                print(f"  [{i+1:2d}] {name} — NO URL, skipping")
                progress[name] = {"emails": [], "source": "skipped"}
                continue

            print(f"  [{i+1:2d}] {name}...", end=" ", flush=True)

            # Try Google Maps
            emails = extract_email_from_maps(page, url)

            if emails:
                print(f"FOUND: {emails}")
                progress[name] = {"emails": emails, "source": "google_maps"}
            else:
                print("no email found")
                progress[name] = {"emails": [], "source": "checked"}

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
