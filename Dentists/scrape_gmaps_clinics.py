#!/usr/bin/env python3
"""Scrape Google Maps pages for S4 clinics and write content.md files."""

import json, os, time, re, sys
from playwright.sync_api import sync_playwright

BASE_DIR = '/Users/nirkosover/Library/Mobile Documents/com~apple~CloudDocs/Mine/Development/Claude code/Dentists/reports/S4'
INDEX_PATH = os.path.join(BASE_DIR, '_clinics_index.json')

def scrape_clinic(page, clinic):
    """Navigate to Google Maps URL and scrape all available content."""
    url = clinic['gmap_url']
    if not url:
        return None

    print(f"  Navigating to Google Maps...")
    try:
        page.goto(url, wait_until='domcontentloaded', timeout=15000)
        time.sleep(3)
    except Exception as e:
        print(f"  ERROR loading page: {e}")
        return None

    # Accept cookies if prompted
    try:
        accept_btn = page.locator('button:has-text("Accept all"), button:has-text("קבל הכל"), form[action*="consent"] button')
        if accept_btn.count() > 0:
            accept_btn.first.click()
            time.sleep(1)
    except:
        pass

    data = {}

    # 1. Business name
    try:
        name_el = page.locator('h1').first
        data['name'] = name_el.inner_text(timeout=5000)
    except:
        data['name'] = clinic['name']

    # 2. Rating and review count
    try:
        rating_el = page.locator('[role="img"][aria-label*="stars"], [role="img"][aria-label*="כוכבים"]').first
        label = rating_el.get_attribute('aria-label', timeout=3000)
        data['rating_label'] = label
    except:
        pass

    # 3. Category / type
    try:
        cat_el = page.locator('button[jsaction*="category"]').first
        data['category'] = cat_el.inner_text(timeout=3000)
    except:
        pass

    # 4. Address
    try:
        addr_el = page.locator('[data-item-id="address"] .fontBodyMedium, button[data-item-id="address"]').first
        data['address'] = addr_el.inner_text(timeout=3000)
    except:
        pass

    # 5. Phone
    try:
        phone_el = page.locator('[data-item-id*="phone"] .fontBodyMedium, button[data-item-id*="phone"]').first
        data['phone'] = phone_el.inner_text(timeout=3000)
    except:
        pass

    # 6. Website
    try:
        web_el = page.locator('[data-item-id="authority"] .fontBodyMedium, a[data-item-id="authority"]').first
        data['website'] = web_el.inner_text(timeout=3000)
    except:
        pass

    # 7. Hours
    try:
        hours_el = page.locator('[aria-label*="hours"], [aria-label*="שעות"]').first
        hours_label = hours_el.get_attribute('aria-label', timeout=3000)
        data['hours_label'] = hours_label
        # Try to expand hours
        try:
            hours_el.click()
            time.sleep(1)
            hours_table = page.locator('table.eK4R0e, table[class*="hour"]').first
            data['hours_full'] = hours_table.inner_text(timeout=3000)
        except:
            pass
    except:
        pass

    # 8. All info items (catch-all for any business details)
    try:
        info_items = page.locator('[data-item-id] .fontBodyMedium')
        count = info_items.count()
        extras = []
        for i in range(min(count, 20)):
            try:
                txt = info_items.nth(i).inner_text(timeout=2000)
                if txt.strip() and len(txt.strip()) > 1:
                    extras.append(txt.strip())
            except:
                pass
        if extras:
            data['info_items'] = extras
    except:
        pass

    # 9. Description / About
    try:
        about_el = page.locator('[class*="description"], [class*="about"] .fontBodyMedium')
        if about_el.count() > 0:
            data['about'] = about_el.first.inner_text(timeout=3000)
    except:
        pass

    # 10. Photos count
    try:
        photos_btn = page.locator('button[aria-label*="photo"], button[aria-label*="תמונ"]').first
        photos_label = photos_btn.get_attribute('aria-label', timeout=3000)
        data['photos_label'] = photos_label
    except:
        pass

    # 11. Scrape reviews
    print(f"  Scraping reviews...")
    reviews = scrape_reviews(page)
    if reviews:
        data['reviews'] = reviews

    return data


def scrape_reviews(page):
    """Click on reviews tab and scrape individual reviews."""
    reviews = []

    # Try clicking the reviews button/tab
    try:
        rev_btn = page.locator('button[aria-label*="review"], button[aria-label*="ביקור"], [role="tab"]:has-text("ביקורות"), [role="tab"]:has-text("Reviews")').first
        rev_btn.click(timeout=5000)
        time.sleep(2)
    except:
        # Try alternative: click on the rating/review count text
        try:
            rev_link = page.locator('[jsaction*="reviewChart"], .fontBodySmall:has-text("ביקורות"), .fontBodySmall:has-text("reviews")').first
            rev_link.click(timeout=5000)
            time.sleep(2)
        except:
            return reviews

    # Scroll the reviews panel to load more
    try:
        scrollable = page.locator('[class*="review"] [tabindex="-1"], div.m6QErb.DxyBCb').first
        for _ in range(3):
            scrollable.evaluate('el => el.scrollTop = el.scrollHeight')
            time.sleep(1)
    except:
        pass

    # Extract individual reviews
    try:
        review_els = page.locator('[data-review-id], div.jftiEf')
        count = review_els.count()
        print(f"  Found {count} reviews")

        for i in range(min(count, 20)):  # Cap at 20 reviews, dedup brings it down
            try:
                rev_el = review_els.nth(i)
                review = {}

                # Reviewer name
                try:
                    name_el = rev_el.locator('.d4r55, [class*="reviewer"]').first
                    review['author'] = name_el.inner_text(timeout=2000)
                except:
                    pass

                # Star rating
                try:
                    stars_el = rev_el.locator('[role="img"][aria-label*="star"], [role="img"][aria-label*="כוכב"]').first
                    review['stars'] = stars_el.get_attribute('aria-label', timeout=2000)
                except:
                    pass

                # Review text - try to expand "More" first
                try:
                    more_btn = rev_el.locator('button:has-text("More"), button:has-text("עוד"), button.w8nwRe').first
                    if more_btn.count() > 0:
                        more_btn.click(timeout=2000)
                        time.sleep(0.3)
                except:
                    pass

                try:
                    text_el = rev_el.locator('.wiI7pd, [class*="review-text"], .MyEned span').first
                    review['text'] = text_el.inner_text(timeout=2000)
                except:
                    pass

                # Time ago
                try:
                    time_el = rev_el.locator('.rsqaWe, [class*="publish"]').first
                    review['time'] = time_el.inner_text(timeout=2000)
                except:
                    pass

                if review.get('text') or review.get('stars'):
                    # Deduplicate by text
                    if not any(existing.get('text') == review.get('text') for existing in reviews if review.get('text')):
                        reviews.append(review)
            except:
                continue
    except Exception as e:
        print(f"  Error extracting reviews: {e}")

    return reviews


def write_content_md(clinic, scraped):
    """Write enriched content.md for a clinic."""
    folder_path = os.path.join(BASE_DIR, clinic['folder'])
    content_path = os.path.join(folder_path, 'content.md')

    name = scraped.get('name', clinic['name'])
    doctor = clinic.get('doctor', name)
    city = clinic.get('city', '')
    address = scraped.get('address', clinic.get('address', ''))
    phone = scraped.get('phone', clinic.get('phone', ''))
    rating = clinic.get('rating', '')
    reviews_count = clinic.get('reviews', '0')
    segment = clinic['segment']
    gmap_url = clinic.get('gmap_url', '')
    easy_url = clinic.get('easy_url', '')

    md = f"""# {name}

## סיכום
{doctor} — מרפאת שיניים ב{city}. דירוג Google: {rating} ({reviews_count} ביקורות). סגמנט {segment}.

## פרטי המרפאה
- **שם:** {name}
- **רופא:** {doctor}
- **עיר:** {city}
- **כתובת:** {address}
- **טלפון:** {phone}
- **דירוג Google:** {rating} ⭐ ({reviews_count} ביקורות)
- **Google Maps:** {gmap_url}
"""

    if easy_url:
        md += f"- **Easy.co.il:** {easy_url}\n"

    if scraped.get('category'):
        md += f"- **קטגוריה:** {scraped['category']}\n"

    if scraped.get('website'):
        md += f"- **אתר:** {scraped['website']}\n"

    if scraped.get('photos_label'):
        md += f"- **תמונות:** {scraped['photos_label']}\n"

    # Hours
    if scraped.get('hours_full'):
        md += f"\n## שעות פעילות\n{scraped['hours_full']}\n"
    elif scraped.get('hours_label'):
        md += f"\n## שעות פעילות\n{scraped['hours_label']}\n"

    # About / Description
    if scraped.get('about'):
        md += f"\n## אודות\n{scraped['about']}\n"

    # Additional info
    if scraped.get('info_items'):
        md += f"\n## מידע נוסף\n"
        for item in scraped['info_items']:
            md += f"- {item}\n"

    # Reviews
    reviews = scraped.get('reviews', [])
    if reviews:
        md += f"\n## ביקורות Google ({len(reviews)} מתוך {reviews_count})\n"
        for r in reviews:
            author = r.get('author', 'אנונימי')
            stars = r.get('stars', '')
            text = r.get('text', '')
            when = r.get('time', '')
            md += f"\n### {author}"
            if stars:
                md += f" — {stars}"
            if when:
                md += f" ({when})"
            md += "\n"
            if text:
                md += f"> {text}\n"

    # Miscellaneous - anything we couldn't categorize
    misc = []
    if scraped.get('rating_label'):
        misc.append(f"Rating label: {scraped['rating_label']}")

    if misc:
        md += f"\n## שונות\n"
        for m in misc:
            md += f"- {m}\n"

    # Content for website
    md += f"""
## תוכן לאתר

### כותרת
מרפאת שיניים {doctor} | {city}

### תת-כותרת
טיפולי שיניים מקצועיים בסביבה חמה ואישית

### תיאור קצר
מרפאת השיניים של {doctor} ב{city} מציעה מגוון טיפולי שיניים מתקדמים.
{f'עם דירוג {rating} ו-{reviews_count} ביקורות חיוביות, ' if rating not in ('', 'N/A') else ''}המרפאה מתמחה בטיפול אישי ומקצועי.

### שירותים
- טיפולי שיניים כלליים
- טיפולי שיניים אסתטיים
- השתלות שיניים
- יישור שיניים
- טיפולי חניכיים
- רפואת שיניים לילדים

### CTA
📞 {phone} | קבעו תור עוד היום
"""

    # Top review quotes for website
    good_reviews = [r for r in reviews if r.get('text') and len(r.get('text','')) > 20]
    if good_reviews:
        md += "\n### ציטוטים מביקורות (לשימוש באתר)\n"
        for r in good_reviews[:5]:
            md += f'- "{r["text"][:150]}..." — {r.get("author", "מטופל/ת")}\n'

    md += f"\n## סגמנט\n{segment} — {'Invisible Good - High Reviews' if segment == '4b' else 'Invisible Good - Some Reviews'}\n"

    with open(content_path, 'w') as f:
        f.write(md)


def main():
    with open(INDEX_PATH) as f:
        clinics = json.load(f)

    # Check --test flag
    test_mode = '--test' in sys.argv
    if test_mode:
        clinics = clinics[:3]
        print(f"TEST MODE: processing {len(clinics)} clinics only\n")

    # Check --start flag for resuming
    start_idx = 0
    for arg in sys.argv:
        if arg.startswith('--start='):
            start_idx = int(arg.split('=')[1])

    print(f"Processing {len(clinics)} clinics (starting from #{start_idx})...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            locale='he-IL',
            viewport={'width': 1280, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        for i, clinic in enumerate(clinics):
            if i < start_idx:
                continue

            name = clinic['name']
            print(f"[{i+1}/{len(clinics)}] {name} ({clinic['segment']})")

            # Check if already scraped (content.md > 2KB means enriched)
            content_path = os.path.join(BASE_DIR, clinic['folder'], 'content.md')
            if os.path.exists(content_path) and os.path.getsize(content_path) > 4000:
                print(f"  Already scraped, skipping\n")
                continue

            scraped = scrape_clinic(page, clinic)
            if scraped:
                write_content_md(clinic, scraped)
                rev_count = len(scraped.get('reviews', []))
                print(f"  Saved: {rev_count} reviews scraped\n")
            else:
                print(f"  Failed to scrape\n")

            # Polite delay
            time.sleep(2)

        browser.close()

    print("Done!")


if __name__ == '__main__':
    main()
