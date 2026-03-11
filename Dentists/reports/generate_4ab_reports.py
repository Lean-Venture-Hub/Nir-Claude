#!/usr/bin/env python3
"""Generate complete report folders for 4a/4b Tel Aviv dental clinics.

For each clinic creates:
  - content.md    (all real data: info, reviews, proposal data)
  - index.html    (website from Hebrew template, personalized)
  - blog.html     (blog listing page)
  - blog/         (3 Hebrew blog post HTML files)
  - proposal.html (template-6 Frost style, Hebrew)
  - images/       (all needed images copied locally)
  - screenshots   (home, blog, article — via Playwright)
  - site-walkthrough.mp4 (scrolling video — via Playwright)
"""

import csv, os, re, random, hashlib, shutil, json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # Dentists/
CSV_PATH = os.path.join(BASE_DIR, "labeled-dentals.csv")
REVIEWS_PATH = os.path.join(BASE_DIR, "reviews.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# Source template base
TMPL_BASE = os.path.join(BASE_DIR, "templates", "website")
IMAGES_BASE = os.path.join(BASE_DIR, "templates", "images")
PROPOSAL_BASE = os.path.join(BASE_DIR, "templates", "proposals")

GUSH_DAN_CITIES = {"תל אביב", "בת ים", "בני ברק", "פתח תקווה", "רמת גן", "חולון", "גבעתיים", "קרית אונו", ""}
SEGMENTS = ("4a", "4b")
# Skip non-dental categories
SKIP_CATEGORIES = {"לינה וארוחת בוקר", "מלון", "מסעדה", "קפה"}

# Templates to rotate through for websites (picked for visual variety)
WEBSITE_TEMPLATES = [4, 5, 3, 10, 11, 8, 12, 15, 20]

# ─── Hebrew fake placeholders in all templates ─────────────────────────
FAKE_CLINIC_NAMES = ['מרפאת חיוך פלוס', 'חיוך פלוס']
FAKE_DOCTOR_NAMES = ['ד״ר מיכל לוי', 'ד"ר מיכל לוי', 'ד״ר לוי', 'ד"ר לוי', 'מיכל לוי']
FAKE_PHONE = '03-555-1234'
FAKE_REVIEWER_NAMES = ['נועה כהן', 'יוסי אברהם', 'שירה דויד']
FAKE_REVIEW_TEXTS = [
    'ד״ר לוי שינתה לי את החיים. אחרי שנים שנמנעתי מלחייך, עברתי טיפול הלבנה וציפויים — התוצאה מדהימה. הצוות מקצועי, חם ומפנק. ממליצה בחום!',
    'עברתי השתלת שיניים במרפאה — מהייעוץ הראשוני ועד לתוצאה הסופית, הכל היה ברמה הגבוהה ביותר. ד״ר לוי מסבירה כל שלב ועושה הכל בסבלנות.',
    'מקום מדהים! הגעתי בפעם הראשונה לטיפול שורש ומאז אני מטופלת קבועה. האווירה נעימה, הצוות מדהים, והטיפול ברמה אחרת לגמרי. תודה רבה!',
]

# ─── Helpers ───────────────────────────────────────────────────────────

def slugify(name):
    """Create a filesystem-safe slug from Hebrew/English name."""
    s = name.strip()
    # Replace Hebrew chars with transliteration is hard; just use hash + cleaned name
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = s.strip('-')
    if not s or not re.search(r'[a-zA-Z]', s):
        # Pure Hebrew — create a readable slug
        s = name.strip()
        s = re.sub(r'[,\.\(\)"\'\|]', '', s)
        s = re.sub(r'\s+', '-', s)
        s = s.strip('-')
    return s[:80]


def seed_from_name(name):
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)


def extract_doctor_name(clinic_name):
    """Extract just the doctor's name from clinic name. Returns (doctor, clinic_brand)."""
    name = clinic_name.strip()

    # All Hebrew doctor prefixes: ד"ר, ד״ר, ד''ר, דר, דר', דוקטור
    dr_prefix = r"""(?:ד"ר|ד״ר|ד''ר|דר'|דר|דוקטור|Dr\.?\s*)"""

    # Pattern 1: "NAME, ד"ר" or "NAME ד"ר" (reversed, name before title)
    m = re.search(rf'^(.+?),?\s+{dr_prefix}$', name)
    if m:
        person = m.group(1).strip(' ,')
        return f'ד"ר {person}'

    # Pattern 2: "מרפאת שיניים ד"ר NAME" or "... | ד"ר NAME"
    m = re.search(rf'{dr_prefix}\s+(.+)', name)
    if m:
        person = m.group(1).strip(' -–,|')
        # Remove trailing clinic descriptors
        for suffix in ['מרפאת שיניים', 'רופא שיניים בתל אביב', 'רופא שיניים',
                       'מומחה לשיקום הפה', '- טיפולי שורש - אנדודונטיה',
                       'מרפאת שיניים בע"מ', 'בע"מ']:
            person = person.replace(suffix, '').strip(' -–,|')
        # Remove "- מרכז רפואי מתקדם..." and similar long suffixes
        person = re.sub(r'\s*[-–]\s*מרכז רפואי.*$', '', person).strip()
        if person:
            return f'ד"ר {person}'

    # Pattern 3: English "Dr. Name"
    m = re.search(r'Dr\.?\s*(\w[\w\s]+?)(?:\s*[-–]|$)', name)
    if m:
        return f'Dr. {m.group(1).strip()}'

    # No doctor found — return empty string (NOT the full name!)
    return ''


def extract_short_name(clinic_name):
    """Get a short display name for the clinic (the brand/clinic portion, not the doctor)."""
    name = clinic_name.strip()
    # Remove long suffixes
    for suffix in ['- מרכז רפואי מתקדם להשתלות שיניים ושיקום הפה',
                   'מומחה לשיקום הפה', '- טיפולי שורש - אנדודונטיה',
                   'רופא שיניים בתל אביב', 'רופא שיניים',
                   'בע"מ', 'Dental Center', 'AYAN']:
        name = name.replace(suffix, '').strip(' -–,|')
    # Remove "מרפאת שיניים" prefix/suffix
    name = re.sub(r'מרפאת שיניים\s*', '', name).strip(' -–,|')
    if len(name) > 40:
        name = name[:40].rsplit(' ', 1)[0]
    return name.strip() or clinic_name.strip()


# ─── Load data ─────────────────────────────────────────────────────────

def load_clinics():
    """Load 4a/4b Tel Aviv clinics from labeled CSV."""
    clinics = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get('city', '').strip() in GUSH_DAN_CITIES and
                row.get('segment', '').strip() in SEGMENTS and
                row.get('categories', '').strip() not in SKIP_CATEGORIES):
                clinics.append(row)
    return clinics


def load_reviews():
    """Load reviews from reviews.csv, grouped by clinic_name."""
    reviews = {}
    with open(REVIEWS_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cn = row['clinic_name'].strip()
            if cn not in reviews:
                reviews[cn] = []
            reviews[cn].append({
                'name': row['reviewer_name'].strip(),
                'rating': int(row.get('stars', 5) or 5),
                'text': row.get('review_text', '').strip(),
                'date': row.get('review_date', '').strip(),
            })
    return reviews


# ─── Tel Aviv competitor data (real clinics from CSV) ──────────────────

def get_competitors(clinic_name, clinics_data):
    """Get 3 real competitors from the same CSV (other segments with websites)."""
    rng = random.Random(seed_from_name(clinic_name))
    candidates = []
    for c in clinics_data:
        if c['name'].strip() != clinic_name and c.get('website', '').strip():
            rating = float(c.get('rating', 0) or 0)
            reviews = int(c.get('review_count', 0) or 0)
            if rating >= 4.0 and reviews >= 15:
                candidates.append((c['name'].strip(), rating, reviews))
    if len(candidates) < 3:
        # Fallback: use any clinic with reviews
        for c in clinics_data:
            if c['name'].strip() != clinic_name:
                rating = float(c.get('rating', 0) or 0)
                reviews = int(c.get('review_count', 0) or 0)
                if rating > 0 and reviews >= 5:
                    candidates.append((c['name'].strip(), rating, reviews))
    candidates = list(set(candidates))
    return rng.sample(candidates, min(3, len(candidates)))


# ─── Template reading & personalization ────────────────────────────────

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_blog_posts(tmpl_id):
    """Get all Hebrew blog post paths for a template."""
    blog_dir = os.path.join(TMPL_BASE, f"template-{tmpl_id}", "blog")
    posts = []
    if not os.path.isdir(blog_dir):
        return posts
    for cat_dir in sorted(os.listdir(blog_dir)):
        cat_path = os.path.join(blog_dir, cat_dir)
        if os.path.isdir(cat_path):
            for html_file in sorted(os.listdir(cat_path)):
                if html_file.endswith('.html'):
                    posts.append((cat_dir, html_file))
    return posts


def personalize_hebrew(html, clinic):
    """Replace Hebrew template placeholders with real clinic data."""
    name = clinic['name'].strip()
    short = extract_short_name(name)
    doctor = extract_doctor_name(name)
    phone = clinic.get('phone', '').strip() or '—'
    rating = clinic.get('rating', '0')
    review_count = clinic.get('review_count', '0')
    address = clinic.get('address', '').strip().replace('\n', ' ')
    city = clinic.get('city', 'תל אביב').strip() or 'תל אביב'
    tel_href = phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')

    # ── Ensure doctor and clinic brand are DIFFERENT in the hero ──
    # Hero template: "ד״ר מיכל לוי —\n מרפאת חיוך פלוס"
    # doctor → replaces "ד״ר מיכל לוי", name → replaces "מרפאת חיוך פלוס"
    # They must be visually distinct.

    orig_name = name  # keep original clinic name

    if doctor:
        # Strip the doctor name out of the clinic brand to avoid repetition
        brand = orig_name
        # Remove doctor-like portions from brand (try all prefix variants)
        doc_plain = re.sub(r'^ד"ר\s*', '', doctor).strip()
        for pattern in [doctor, doc_plain,
                        doctor.replace('ד"ר', 'ד״ר'), doctor.replace('ד"ר', "דר'"),
                        doctor.replace('ד"ר', 'דר'), doctor.replace('ד"ר', 'דוקטור'),
                        doctor.replace('ד"ר ', 'Dr. '), doctor.replace('ד"ר ', 'Dr.')]:
            brand = brand.replace(pattern, '').strip()
        # Clean up ALL leftover doctor prefixes (including standalone דר)
        brand = re.sub(r'(?:ד"ר|ד״ר|ד\'\'ר|דר\'|דוקטור|Dr\.?\s*)\s*', '', brand).strip()
        brand = re.sub(r'\bדר\b\s*', '', brand).strip()  # standalone דר
        brand = re.sub(r'^[\s,\-–|]+|[\s,\-–|]+$', '', brand)
        brand = re.sub(r'^\s*[-–|]\s*', '', brand).strip()
        brand = re.sub(r'\s{2,}', ' ', brand)  # collapse double spaces

        if len(brand) < 3 or brand in ('מרפאת', 'מרפאת שיניים', '', 'דר', '-'):
            # Nothing meaningful left — use "מרפאת שיניים" + city as brand
            brand = f'מרפאת שיניים ב{city}'

        name = brand
        # Short = condensed brand
        short_brand = brand
        for suffix in ['בע"מ', 'Dental Center', 'AYAN']:
            short_brand = short_brand.replace(suffix, '').strip()
        if len(short_brand) > 30:
            short_brand = short_brand[:30].rsplit(' ', 1)[0]
        short = short_brand.strip() or brand
    else:
        # No doctor found — use clinic name for brand, short for doctor line
        doctor = short
        # Avoid "מרפאת מרפאת..." — only prepend if not already there
        if doctor == name:
            if not name.startswith('מרפאת'):
                name = f'מרפאת {short}'
            else:
                # Name already has מרפאת, use city variant for differentiation
                doctor = re.sub(r'^מרפאת שיניים\s*', '', name).strip() or short
                if doctor == name:
                    name = f'מרפאת שיניים ב{city}'

    # Order matters: longer strings first
    replacements = [
        ('מרפאת חיוך פלוס', name),
        ('חיוך פלוס', short),
        ('ד״ר מיכל לוי', doctor),
        ('ד"ר מיכל לוי', doctor),
        ('מיכל לוי', doctor),
        ('ד״ר לוי', doctor),
        ('ד"ר לוי', doctor),
        ('tel:03-555-1234', f'tel:{tel_href}'),
        ('03-555-1234', phone),
        # Rating/reviews — catch ALL patterns across all templates
        # Template-8: "187+ ביקורות ב-Google" and "דירוג 4.9 מתוך 5"
        ('187+ ביקורות ב-Google', f'{review_count}+ ביקורות ב-Google'),
        ('דירוג 4.9 מתוך 5', f'דירוג {rating} מתוך 5'),
        # Template-5: "4.9 &#9733; בגוגל" and "187 ביקורות מאומתות"
        ('4.9 &#9733; בגוגל', f'{rating} &#9733; בגוגל'),
        ('187 ביקורות מאומתות', f'{review_count} ביקורות מאומתות'),
        # Template-11: "4.9</span> · 187 ביקורות"
        ('4.9</span> · 187 ביקורות', f'{rating}</span> · {review_count} ביקורות'),
        # Template-12: "4.9 דירוג גוגל"
        ('4.9 דירוג גוגל', f'{rating} דירוג גוגל'),
        # Template-15: "4.9 כוכבים"
        ('4.9 כוכבים', f'{rating} כוכבים'),
        # Template-20: "4.9 דירוג מרוצים" and "187 ביקורות" in badge
        ('4.9 דירוג מרוצים', f'{rating} דירוג מרוצים'),
        # Generic patterns (order: longer first, then shorter)
        ('>187 ביקורות<', f'>{review_count} ביקורות<'),
        ('187 ביקורות', f'{review_count} ביקורות'),
        ('>4.9<', f'>{rating}<'),
        ('>187<', f'>{review_count}<'),
    ]

    # Replace city if not Tel Aviv
    if city != 'תל אביב':
        replacements.append(('תל אביב', city))

    for old, new in replacements:
        html = html.replace(old, new)

    return html


def inject_real_reviews_hebrew(html, reviews):
    """Replace fake Hebrew testimonial names/texts with real Google reviews."""
    if not reviews:
        return html

    # Generic short reviews for when real review text is empty
    EMPTY_REVIEW_FALLBACKS = [
        'שירות מעולה, ממליצים בחום!',
        'מקצועיות ויחס אישי. מומלץ!',
        'חוויה מצוינת, צוות אדיב ומקצועי.',
    ]

    for i, fake_name in enumerate(FAKE_REVIEWER_NAMES):
        if i < len(reviews):
            rev = reviews[i]
            real_name = rev['name']
            if real_name:
                html = html.replace(f'>{fake_name}<', f'>{real_name}<')

        if i < len(FAKE_REVIEW_TEXTS):
            if i < len(reviews):
                rev = reviews[i]
                real_text = rev.get('text', '').strip()
                if real_text:
                    html = html.replace(FAKE_REVIEW_TEXTS[i], real_text)
                else:
                    # Empty review — replace fake text with a short generic
                    html = html.replace(FAKE_REVIEW_TEXTS[i], EMPTY_REVIEW_FALLBACKS[i % len(EMPTY_REVIEW_FALLBACKS)])

    return html


def fix_image_paths_main(html):
    """Fix image paths in main-level files."""
    html = html.replace('../../images/', 'images/')
    html = html.replace('../images/', 'images/')
    return html


def fix_image_paths_blog_post(html):
    """Fix image paths in blog posts (blog/category/post.html)."""
    html = html.replace('../../../../../images/', '../../images/')
    html = html.replace('../../../../images/', '../../images/')
    html = html.replace('../../../images/', '../../images/')
    return html


def fix_blog_links(html, is_post=False):
    """Fix blog navigation links."""
    # In Hebrew we use blog/ not blog-en/
    html = html.replace('blog-en.html', 'blog.html')
    html = html.replace('blog-en/', 'blog/')
    if is_post:
        html = re.sub(
            r'href="(?:\.\./)*template_example-\d+\.html"',
            'href="../../index.html"',
            html
        )
        html = re.sub(
            r'href="(?:\.\./)*template_example-\d+-en\.html"',
            'href="../../index.html"',
            html
        )
    else:
        html = re.sub(
            r'href="template_example-\d+\.html"',
            'href="index.html"',
            html
        )
    return html


def get_needed_images(tmpl_id):
    """Collect all unique image filenames needed for a template."""
    images = set()
    files_to_check = []

    # Main template
    main_path = os.path.join(TMPL_BASE, f"template-{tmpl_id}", f"template_example-{tmpl_id}.html")
    if os.path.exists(main_path):
        files_to_check.append(main_path)

    # Blog listing
    blog_path = os.path.join(TMPL_BASE, f"template-{tmpl_id}", "blog.html")
    if os.path.exists(blog_path):
        files_to_check.append(blog_path)

    # Blog posts
    blog_dir = os.path.join(TMPL_BASE, f"template-{tmpl_id}", "blog")
    if os.path.isdir(blog_dir):
        for cat in os.listdir(blog_dir):
            cat_path = os.path.join(blog_dir, cat)
            if os.path.isdir(cat_path):
                for f in os.listdir(cat_path):
                    if f.endswith('.html'):
                        files_to_check.append(os.path.join(cat_path, f))

    for fpath in files_to_check:
        html = read_file(fpath)
        for m in re.findall(r'(?:\.\./)*images/((?:template-images|blog-images)/[^"\']+)', html):
            images.add(m)

    return images


def copy_images(tmpl_id, dest_folder):
    """Copy all needed images for a template into dest_folder/images/."""
    needed = get_needed_images(tmpl_id)
    for rel_path in needed:
        src = os.path.join(IMAGES_BASE, rel_path)
        dst = os.path.join(dest_folder, "images", rel_path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copy2(src, dst)


# ─── content.md generation ────────────────────────────────────────────

ARTICLE_TOPICS_HE = [
    ("5 סימנים שצריך לפנות לרופא שיניים מיד", "סימני אזהרה כמו כאב שיניים מתמשך, דימום חניכיים ורגישות שאסור להתעלם מהם."),
    ("המדריך המלא להשתלות שיניים", "כל מה שמטופלים צריכים לדעת על השתלות: הליך, החלמה, עלויות ויתרונות לטווח ארוך."),
    ("איך לבחור רופא שיניים מתאים למשפחה", "גורמים חשובים כולל מיקום, התמחויות וביקורות מטופלים."),
]


def generate_content_md(clinic, reviews, all_clinics):
    """Generate content.md with all real data."""
    name = clinic['name'].strip()
    short = extract_short_name(name)
    doctor = extract_doctor_name(name)
    rating = clinic.get('rating', '0')
    review_count = clinic.get('review_count', '0')
    phone = clinic.get('phone', '').strip()
    address = clinic.get('address', '').strip().replace('\n', ' ')
    city = clinic.get('city', 'תל אביב').strip() or 'תל אביב'
    segment = clinic.get('segment', '')
    google_url = clinic.get('google_maps_url', '')
    categories = clinic.get('categories', 'מרפאת שיניים')
    comps = get_competitors(name, all_clinics)

    content = f"""# {name} — חבילת תוכן

## פרטי המרפאה
- **שם:** {name}
- **שם מקוצר:** {short}
- **רופא/ה:** {doctor}
- **קטגוריה:** {categories}
- **כתובת:** {address}
- **טלפון:** {phone}
- **דירוג גוגל:** {rating} ({review_count} ביקורות)
- **סגמנט:** {segment}
- **Google Maps:** {google_url}

---

## תוכן לאתר

### Hero
- **כותרת:** טיפולי שיניים מקצועיים שאתם יכולים לסמוך עליהם
- **תת-כותרת:** {short} ב{city} — טיפול מותאם אישית לנוחותכם, בריאותכם וביטחונכם.

### אודות
ב-{short}, אנו מספקים טיפולי שיניים יוצאי דופן בסביבה נוחה ומזמינה. ניסיון רב שנים בשילוב טכנולוגיות דנטליות מתקדמות מבטיחים תוצאות מצוינות לכל מטופל.

### שירותים
- רפואת שיניים כללית וקוסמטית, השתלות, טיפולי חירום

---

## מאמרי בלוג

"""
    for i, (title, desc) in enumerate(ARTICLE_TOPICS_HE, 1):
        content += f"### מאמר {i}: {title}\n{desc}\n\n"

    # Real Google Reviews
    content += "---\n\n## ביקורות גוגל אמיתיות\n\n"
    if reviews:
        for rev in reviews:
            stars = '★' * rev.get('rating', 5) + '☆' * (5 - rev.get('rating', 5))
            content += f"- **{rev['name']}** {stars}\n"
            if rev.get('text'):
                content += f"  > {rev['text']}\n"
            if rev.get('date'):
                content += f"  _{rev['date']}_\n"
            content += "\n"
    else:
        content += "_אין ביקורות שנאספו._\n\n"

    # Proposal data
    content += "---\n\n## נתונים להצעה\n\n### מתחרים\n"
    for cn, cr, cv in comps:
        content += f"- **{cn}:** דירוג {cr}, {cv} ביקורות\n"

    rating_f = float(rating or 0)
    content += f"""
### תובנה מרכזית
- דירוג {rating} {'מצוין' if rating_f >= 4.3 else 'טוב'}, {'אבל רק ' + str(review_count) + ' ביקורות' if int(review_count or 0) < 50 else str(review_count) + ' ביקורות'}
- אין אתר אינטרנט — מטופלים פוטנציאליים שמחפשים אונליין לא מוצאים אתכם
- למתחרים יש אתרים עם עשרות עד מאות ביקורות
"""
    return content


# ─── Proposal HTML (Template 6 Frost, Hebrew) ─────────────────────────

def generate_proposal_hebrew(clinic, all_clinics):
    """Generate Hebrew RTL proposal based on template-6-frost."""
    name = clinic['name'].strip()
    short = extract_short_name(name)
    city = clinic.get('city', 'תל אביב').strip() or 'תל אביב'
    rating = float(clinic.get('rating', 0) or 0)
    reviews = int(clinic.get('review_count', 0) or 0)
    comps = get_competitors(name, all_clinics)

    if not comps:
        comps = [("מרפאת שיניים א'", 4.5, 120), ("מרפאת שיניים ב'", 4.7, 85), ("מרפאת שיניים ג'", 4.3, 200)]

    top_reviews = max(c[2] for c in comps)
    position = sum(1 for c in comps if c[2] > reviews) + 1
    total = len(comps) + 1
    multiplier = round(top_reviews / max(reviews, 1), 1)

    calc_rows = ""
    for add in [0, 5, 10, 15, 20]:
        new_total = reviews + add
        new_rating = round((rating * reviews + 5.0 * add) / max(new_total, 1), 1)
        improvement = round(new_rating - rating, 1)
        label = "היום" if add == 0 else f"+{add}"
        imp = "—" if add == 0 else f"+{improvement}"
        calc_rows += f"        <tr><td>{label}</td><td>{new_rating}</td><td>{imp}</td></tr>\n"

    comp_headers = '        <td class="comp-cell cell-you">אתם</td>\n'
    for c in comps:
        comp_headers += f'        <td class="comp-cell">{c[0][:25]}</td>\n'

    def comp_row(label, you_val, comp_vals, css_extra=""):
        row = f'      <tr class="comp-row{css_extra}">\n        <td class="comp-cell cell-label">{label}</td>\n'
        row += f'        <td class="comp-cell cell-you">{you_val}</td>\n'
        for cv in comp_vals:
            try:
                yf = float(str(you_val).replace(',', ''))
                cf = float(str(cv).replace(',', ''))
                cls = " win" if yf > cf else (" lose" if yf < cf else "")
            except:
                cls = ""
            row += f'        <td class="comp-cell cell-comp{cls}">{cv}</td>\n'
        row += '      </tr>\n'
        return row

    rows_html = comp_row("דירוג גוגל", rating, [c[1] for c in comps])
    rows_html += comp_row("ביקורות", reviews, [c[2] for c in comps], " reviews-row")
    rows_html += comp_row("אתר אינטרנט", "&#10005;", ["&#10003;"] * len(comps))

    comp_refs = " | ".join(f'<span>{c[0][:25]} — {c[1]} ({c[2]} ביקורות)</span>' for c in comps)

    rating_desc = 'מצוין' if rating >= 4.3 else 'טוב'

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ניתוח דיגיטלי — {name}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700&family=Instrument+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
html{{font-size:16px}}
body{{font-family:'Heebo','Instrument Sans',sans-serif;background:#fafbfd;color:#1a1e2e;line-height:1.6;direction:rtl}}
.container{{max-width:720px;margin:0 auto;padding:0 32px}}
.hero-line{{height:2px;background:#7b8cc4}}
.hero{{padding:48px 0 0}}
.hero-meta{{font-family:'Instrument Sans',sans-serif;font-size:12px;text-transform:uppercase;letter-spacing:0.3em;color:#999;margin-bottom:20px}}
.hero-name{{font-family:'Heebo',sans-serif;font-size:48px;font-weight:700;line-height:1.15;color:#1a1e2e;margin-bottom:8px}}
@media(max-width:600px){{.hero-name{{font-size:32px}}}}
.hero-city{{font-family:'Heebo',sans-serif;font-size:18px;color:#7b8cc4;margin-bottom:32px}}
.hr{{height:1px;background:#eee;border:none}}
.stats-strip{{display:flex;align-items:center;padding:28px 0}}
.stat-item{{flex:1;text-align:center}}
.stat-divider{{width:1px;height:48px;background:#ddd;flex-shrink:0}}
.stat-number{{font-family:'Instrument Sans',sans-serif;font-size:44px;font-weight:700;color:#1a1e2e;line-height:1}}
.stat-label{{font-family:'Heebo',sans-serif;font-size:11px;color:#999;text-transform:uppercase;letter-spacing:0.08em;margin-top:6px}}
.section{{padding:80px 0 0}}
.section-label{{font-family:'Instrument Sans',sans-serif;font-size:14px;text-transform:uppercase;letter-spacing:0.2em;color:#999;margin-bottom:32px}}
.comp-table{{width:100%;border-collapse:collapse;margin-bottom:24px}}
.comp-header-row .comp-cell{{font-family:'Heebo',sans-serif;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;color:#999;padding:0 12px 12px;text-align:center;border-bottom:1px solid #ddd}}
.comp-row{{border-bottom:1px solid #eee}}
.comp-cell{{padding:14px 12px;text-align:center;font-family:'Heebo',sans-serif;font-size:14px;vertical-align:middle;color:#1a1e2e}}
.cell-label{{text-align:right;font-weight:700;font-size:13px;color:#666}}
.cell-you{{background:rgba(123,140,196,0.04);font-weight:700}}
.cell-comp{{color:#666}}
.reviews-row{{background:rgba(123,140,196,0.03)}}
.win{{color:#4ade80;font-weight:700}}
.lose{{color:#c7a0b8;font-weight:700}}
.callout{{border-right:2px solid #7b8cc4;padding:0 20px;font-family:'Heebo',sans-serif;font-size:14px;line-height:1.7;color:#666;margin-top:28px}}
.rating-block{{text-align:center;margin-bottom:12px}}
.rating-number{{font-family:'Instrument Sans',sans-serif;font-size:72px;font-weight:700;color:#1a1e2e;line-height:1}}
.rating-label{{font-family:'Heebo',sans-serif;font-size:14px;color:#999;margin-top:4px}}
.insight-text{{font-family:'Heebo',sans-serif;font-size:14px;color:#666;text-align:center;margin:20px 0 40px;line-height:1.7}}
.calc-table{{width:100%;border-collapse:collapse;margin-bottom:40px}}
.calc-table th{{font-family:'Heebo',sans-serif;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;color:#999;padding:0 16px 12px;text-align:center;border-bottom:1px solid #ddd}}
.calc-table td{{padding:12px 16px;text-align:center;font-family:'Heebo',sans-serif;font-size:14px;border-bottom:1px solid #eee;color:#1a1e2e}}
.calc-table tbody tr:first-of-type td{{font-weight:700}}
.comp-refs{{font-family:'Heebo',sans-serif;font-size:13px;color:#999;text-align:center;padding:20px 0;border-top:1px solid #eee;margin-bottom:20px}}
.comp-refs span{{margin:0 12px}}
.urgency-text{{font-family:'Heebo',sans-serif;font-size:14px;color:#7b8cc4;text-align:center;margin-top:8px;line-height:1.7}}
.cta-section{{padding:80px 0 0}}
.cta-line{{height:2px;background:#7b8cc4;margin-bottom:40px}}
.cta-headline{{font-family:'Heebo',sans-serif;font-size:24px;font-weight:700;color:#1a1e2e;margin-bottom:6px}}
.cta-sub{{font-family:'Heebo',sans-serif;font-size:14px;color:#999}}
.footer{{padding:80px 0 32px;text-align:center;font-family:'Instrument Sans',sans-serif;font-size:11px;color:#ccc}}
</style>
</head>
<body>
<div class="hero-line"></div>
<section class="hero"><div class="container">
    <p class="hero-meta">ניתוח דיגיטלי — מרץ 2026</p>
    <h1 class="hero-name">{name}</h1>
    <p class="hero-city">{city}</p>
    <hr class="hr">
    <div class="stats-strip">
      <div class="stat-item"><div class="stat-number">{rating}</div><div class="stat-label">דירוג גוגל</div></div>
      <div class="stat-divider"></div>
      <div class="stat-item"><div class="stat-number">{reviews}</div><div class="stat-label">ביקורות</div></div>
      <div class="stat-divider"></div>
      <div class="stat-item"><div class="stat-number">0</div><div class="stat-label">ציון אתר</div></div>
    </div>
</div></section>

<section class="section"><div class="container">
    <hr class="hr"><div style="height:80px"></div>
    <p class="section-label">השוואת מתחרים</p>
    <table class="comp-table">
      <tr class="comp-header-row">
        <td class="comp-cell"></td>
{comp_headers}      </tr>
{rows_html}    </table>
    <div class="callout">המיקום שלכם: מקום {position} מתוך {total} לפי ביקורות. למתחרה המוביל {top_reviews} ביקורות — פי {multiplier} יותר מכם.</div>
</div></section>

<section class="section"><div class="container">
    <hr class="hr"><div style="height:80px"></div>
    <p class="section-label">ניתוח מוניטין</p>
    <div class="rating-block"><div class="rating-number">{rating}</div><div class="rating-label">{reviews} ביקורות</div></div>
    <p class="insight-text">דירוג {rating_desc} — אבל רק {reviews} ביקורות. נפח נמוך של ביקורות פוגע גם באמינות וגם בדירוגים. מטופלים חדשים מחפשים הוכחה כמותית, לא רק ציון.</p>
    <table class="calc-table">
      <thead><tr><th>ביקורות חדשות</th><th>דירוג חדש</th><th>שיפור</th></tr></thead>
      <tbody>
{calc_rows}      </tbody>
    </table>
    <div class="comp-refs">{comp_refs}</div>
    <p class="urgency-text">הדירוג שלכם {rating_desc}, אבל עם רק {reviews} ביקורות אתם נראים "חדשים" בהשוואה למתחרים עם מאות ביקורות. כל חודש ללא תוכנית איסוף ביקורות מרחיב את הפער.</p>
</div></section>

<section class="cta-section"><div class="container">
    <div class="cta-line"></div>
    <h2 class="cta-headline">רוצים לראות את הניתוח המלא?</h2>
    <p class="cta-sub">כולל ניתוח ביקורות, מחקר מילות מפתח ובדיקה מלאה של הנוכחות הדיגיטלית שלכם.<br>10 דקות בזום — מעוניינים?</p>
</div></section>

<footer class="footer"><p>מבוסס על מידע ציבורי מגוגל | מרץ 2026</p></footer>
</body>
</html>"""


# ─── Main ──────────────────────────────────────────────────────────────

def main():
    # Load all clinics for competitor lookup
    all_clinics_data = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('city', '').strip() in GUSH_DAN_CITIES:
                all_clinics_data.append(row)

    clinics = load_clinics()
    reviews_data = load_reviews()

    print(f"4a/4b Tel Aviv clinics: {len(clinics)}")
    print(f"Reviews loaded for {len(reviews_data)} clinics")

    # Create output dir
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, clinic in enumerate(clinics):
        name = clinic['name'].strip()
        slug = slugify(name)
        folder = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(folder, exist_ok=True)

        # Assign website template (rotate through picks)
        tmpl_id = WEBSITE_TEMPLATES[i % len(WEBSITE_TEMPLATES)]

        # Get real reviews
        clinic_reviews = reviews_data.get(name, [])

        # 1. Website (Hebrew template)
        try:
            website_html = read_file(os.path.join(TMPL_BASE, f"template-{tmpl_id}", f"template_example-{tmpl_id}.html"))
            website_html = inject_real_reviews_hebrew(website_html, clinic_reviews)
            website_html = personalize_hebrew(website_html, clinic)
            website_html = fix_image_paths_main(website_html)
            website_html = fix_blog_links(website_html)
            with open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(website_html)
        except Exception as e:
            print(f"  ERROR website for {name}: {e}")

        # 2. Blog listing (Hebrew)
        try:
            blog_html = read_file(os.path.join(TMPL_BASE, f"template-{tmpl_id}", "blog.html"))
            blog_html = personalize_hebrew(blog_html, clinic)
            blog_html = fix_image_paths_main(blog_html)
            blog_html = fix_blog_links(blog_html)
            with open(os.path.join(folder, 'blog.html'), 'w', encoding='utf-8') as f:
                f.write(blog_html)
        except Exception as e:
            print(f"  WARNING: No blog.html for template {tmpl_id}: {e}")

        # 3. Blog posts (Hebrew)
        for cat, post_file in get_blog_posts(tmpl_id):
            try:
                post_path = os.path.join(TMPL_BASE, f"template-{tmpl_id}", "blog", cat, post_file)
                post_html = read_file(post_path)
                post_html = personalize_hebrew(post_html, clinic)
                post_html = fix_image_paths_blog_post(post_html)
                post_html = fix_blog_links(post_html, is_post=True)

                post_dir = os.path.join(folder, "blog", cat)
                os.makedirs(post_dir, exist_ok=True)
                with open(os.path.join(post_dir, post_file), 'w', encoding='utf-8') as f:
                    f.write(post_html)
            except Exception as e:
                print(f"  WARNING: Blog post error {cat}/{post_file}: {e}")

        # 4. Copy images
        copy_images(tmpl_id, folder)

        # 5. content.md
        content_md = generate_content_md(clinic, clinic_reviews, all_clinics_data)
        with open(os.path.join(folder, 'content.md'), 'w', encoding='utf-8') as f:
            f.write(content_md)

        # 6. proposal.html (Hebrew, template-6 frost style)
        proposal_html = generate_proposal_hebrew(clinic, all_clinics_data)
        with open(os.path.join(folder, 'proposal.html'), 'w', encoding='utf-8') as f:
            f.write(proposal_html)

        img_count = sum(len(files) for _, _, files in os.walk(os.path.join(folder, "images"))) if os.path.isdir(os.path.join(folder, "images")) else 0
        blog_count = len(get_blog_posts(tmpl_id))
        rev_count = len(clinic_reviews)
        print(f"  [{i+1:2d}/{len(clinics)}] {slug}/ (tmpl-{tmpl_id}, {img_count} imgs, {blog_count} posts, {rev_count} reviews)")

    print(f"\nDone! Created {len(clinics)} folders in: {OUTPUT_DIR}")
    print("Next step: run generate_media.py to capture screenshots + video walkthroughs")


if __name__ == '__main__':
    main()
