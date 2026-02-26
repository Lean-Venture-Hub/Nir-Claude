#!/usr/bin/env python3
"""Generate HTML sites for S4 clinics using templates + scraped content."""

import json, os, re, random

BASE_DIR = '/Users/nirkosover/Library/Mobile Documents/com~apple~CloudDocs/Mine/Development/Claude code/Dentists/reports/S4'
TEMPLATES_DIR = '/Users/nirkosover/Library/Mobile Documents/com~apple~CloudDocs/Mine/Development/Claude code/Dentists/s4-templates'
IMAGES_DIR = os.path.join(TEMPLATES_DIR, 'images')
INDEX_PATH = os.path.join(BASE_DIR, '_clinics_index.json')

# Templates to use (varied selection)
TEMPLATE_POOL = [2, 3, 4, 5, 6, 7, 8, 16, 17, 19]
# Images to cycle through
IMAGE_POOL = ['image2.png', 'image3.png', 'image4.png', 'image7.png', 'image10.png']


def parse_content_md(md_path):
    """Parse a content.md file into structured data."""
    with open(md_path, 'r') as f:
        text = f.read()

    data = {}

    # Extract key fields
    patterns = {
        'name': r'\*\*שם:\*\*\s*(.+)',
        'doctor': r'\*\*רופא:\*\*\s*(.+)',
        'city': r'\*\*עיר:\*\*\s*(.+)',
        'phone': r'\*\*טלפון:\*\*\s*(.+)',
        'address': r'\*\*כתובת:\*\*\s*(.+)',
        'rating': r'\*\*דירוג Google:\*\*\s*([\d.]+)',
        'reviews_count': r'\((\d+)\s*ביקורות\)',
        'category': r'\*\*קטגוריה:\*\*\s*(.+)',
    }

    for key, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            data[key] = m.group(1).strip()

    # Extract review quotes
    reviews = []
    review_blocks = re.findall(r'###\s+(.+?)(?:\s*—\s*(.+?))?\s*(?:\((.+?)\))?\n>\s*(.+)', text)
    for author, stars, when, body in review_blocks:
        reviews.append({
            'author': author.strip(),
            'stars': stars.strip() if stars else '',
            'time': when.strip() if when else '',
            'text': body.strip()
        })
    data['reviews'] = reviews

    # Extract hours
    hours_match = re.search(r'## שעות פעילות\n([\s\S]+?)(?=\n##|\Z)', text)
    if hours_match:
        data['hours'] = hours_match.group(1).strip()

    return data


def get_absolute_image_path(image_name):
    """Return absolute file:// path for an image (works when opening HTML directly)."""
    abs_path = os.path.join(IMAGES_DIR, image_name)
    return abs_path


def fill_template(template_html, clinic_data, content, image_name):
    """Replace template placeholders with clinic-specific content."""
    html = template_html

    # Prefer clinic_data (JSON, clean) over parsed content.md
    doctor = clinic_data.get('doctor', '') or content.get('doctor', '')
    name = clinic_data.get('name', '') or content.get('name', '')
    city = clinic_data.get('city', '') or content.get('city', '')
    phone = clinic_data.get('phone', '') or content.get('phone', '')
    address = clinic_data.get('address', '') or content.get('address', '')
    rating = clinic_data.get('rating', '') or content.get('rating', '5.0')
    reviews_count = clinic_data.get('reviews', '') or content.get('reviews_count', '0')
    reviews = content.get('reviews', [])

    # Clean all fields (remove newlines, extra spaces)
    phone = re.sub(r'\s+', '', phone).strip()
    doctor = re.sub(r'\s+', ' ', doctor).strip()
    city = re.sub(r'\s+', ' ', city).strip()

    # Format phone for display (add dashes back)
    phone_display = phone
    if re.match(r'^\d{9,10}$', phone):
        if len(phone) == 10:
            phone_display = f'{phone[:3]}-{phone[3:6]}-{phone[6:]}'
        elif len(phone) == 9:
            phone_display = f'{phone[:2]}-{phone[2:5]}-{phone[5:]}'

    # ── Title tag ──
    html = re.sub(r'<title>.*?</title>', f'<title>{name} | {city}</title>', html)

    # ── Replace all known clinic/doctor names from templates ──
    known_names = [
        'מרפאת שיניים ד"ר פוקס', 'מרפאת שיניים ד"ר ברק',
        'מרפאת שיניים ד"ר רוזן', 'מרפאת שיניים ד"ר נחמיאס',
        'מרפאת שיניים ד"ר דנה', 'מרפאת שיניים ד"ר גולד',
        'ד"ר פוקס', 'ד"ר ברק', 'ד"ר רוזן', 'ד"ר גולד', 'ד"ר נחמיאס',
        'ד"ר דנה', 'ד"ר כהן', 'ד"ר לוי', 'ד"ר שמיר', 'ד"ר אברהם',
        'ד"ר מזרחי', 'ד"ר אבי', 'ד"ר מיכל', 'ד"ר רון', 'ד"ר שרון',
        'Dr. Fox', 'דר פוקס',
    ]
    # Sort by length (longest first) to avoid partial replacements
    known_names.sort(key=len, reverse=True)
    for kn in known_names:
        html = html.replace(kn, doctor)

    # Catch any remaining template doctor names via regex
    # Replace "ד"ר <template-name>" that isn't our doctor
    template_surnames = ['פוקס', 'ברק', 'רוזן', 'גולד', 'נחמיאס', 'דנה', 'כהן', 'לוי', 'שמיר', 'אברהם', 'מזרחי', 'אבי', 'מיכל', 'רון', 'שרון']
    for surname in template_surnames:
        html = html.replace(surname, doctor.split()[-1] if ' ' in doctor else doctor)

    # ── Replace cities ──
    known_cities = [
        'תל אביב-יפו', 'תל אביב', 'רמת גן', 'גבעתיים', 'הרצליה',
        'ראשון לציון', 'חולון', 'בת ים', 'בני ברק', 'פתח תקווה', 'קרית אונו'
    ]
    known_cities.sort(key=len, reverse=True)
    for kc in known_cities:
        html = html.replace(kc, city)

    # ── Replace phone numbers (any Israeli format) ──
    html = re.sub(r'0\d[\d-]{7,10}', phone_display, html)
    html = re.sub(r'tel:[0-9\-]+', f'tel:{phone}', html)

    # ── Replace rating and review counts ──
    html = re.sub(r'(?<=>)\s*5\.0\s*(?=<)', rating, html)
    html = re.sub(r'(?<=>)\s*4\.\d\s*(?=<)', rating, html)
    html = re.sub(r'\d+ ביקורות', f'{reviews_count} ביקורות', html)
    # Replace standalone review numbers in stats (127, etc.)
    html = re.sub(r'(?<=>)\s*127\s*(?=<)', reviews_count, html)

    # ── Replace images ──
    # Replace all image references with the assigned image
    for img_num in range(1, 12):
        html = html.replace(f'images/image{img_num}.png', f'images/{image_name}')
        html = html.replace(f'images/image{img_num}b.png', f'images/{image_name}')

    # ── Fill review quotes if template has review sections ──
    if reviews:
        for i, rev in enumerate(reviews[:3]):
            # Try to replace existing review placeholders
            old_quote = f'ביקורת-{i+1}'
            if old_quote in html:
                html = html.replace(old_quote, rev['text'][:200])

    return html


def copy_image_to_clinic(clinic_folder, image_name):
    """Create images folder in clinic dir and symlink the image."""
    img_dir = os.path.join(clinic_folder, 'images')
    os.makedirs(img_dir, exist_ok=True)

    src = os.path.join(IMAGES_DIR, image_name)
    dst = os.path.join(img_dir, image_name)

    if not os.path.exists(dst):
        # Use symlink to save space
        try:
            os.symlink(src, dst)
        except OSError:
            # If symlink fails (e.g., iCloud), copy
            import shutil
            shutil.copy2(src, dst)


def main():
    with open(INDEX_PATH) as f:
        clinics = json.load(f)

    # Load templates
    templates = {}
    for t_num in TEMPLATE_POOL:
        t_path = os.path.join(TEMPLATES_DIR, f'template-{t_num}.html')
        with open(t_path, 'r') as f:
            templates[t_num] = f.read()

    print(f"Loaded {len(templates)} templates")
    print(f"Processing {len(clinics)} clinics...\n")

    # Assign templates and images in round-robin
    for i, clinic in enumerate(clinics):
        t_num = TEMPLATE_POOL[i % len(TEMPLATE_POOL)]
        image_name = IMAGE_POOL[i % len(IMAGE_POOL)]

        folder_path = os.path.join(BASE_DIR, clinic['folder'])
        content_path = os.path.join(folder_path, 'content.md')
        html_path = os.path.join(folder_path, 'index.html')

        # Skip if HTML already exists
        if os.path.exists(html_path):
            print(f"[{i+1}/{len(clinics)}] {clinic['name']} — already has index.html, skipping")
            continue

        # Parse content
        content = parse_content_md(content_path)

        # Fill template
        html = fill_template(templates[t_num], clinic, content, image_name)

        # Copy image
        copy_image_to_clinic(folder_path, image_name)

        # Also copy a second image for templates that use multiple
        second_image = IMAGE_POOL[(i + 2) % len(IMAGE_POOL)]
        copy_image_to_clinic(folder_path, second_image)

        # Save HTML
        with open(html_path, 'w') as f:
            f.write(html)

        print(f"[{i+1}/{len(clinics)}] {clinic['name']} — template {t_num}, {image_name}")

    print(f"\nDone! Generated sites in {BASE_DIR}")


if __name__ == '__main__':
    main()
