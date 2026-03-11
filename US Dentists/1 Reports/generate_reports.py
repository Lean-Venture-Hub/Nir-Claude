#!/usr/bin/env python3
"""Generate complete report folders for each US dentist in the CSV.

For each dentist creates:
  - content.md    (website copy, 3 article outlines, proposal data)
  - index.html    (website from real template, personalized)
  - blog.html     (blog listing page, personalized)
  - blog/         (3 blog post HTML files)
  - proposal.html (template-6 Frost style, English)
  - images/       (all needed images copied locally)
"""

import csv, os, re, math, random, hashlib, shutil, json, glob as globmod

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "first_batch.csv")
REVIEWS_PATH = os.path.join(SCRIPT_DIR, "Inbox_list", "reviews.json")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# Source template base
TMPL_BASE = os.path.join(SCRIPT_DIR, "..", "..", "Dentists", "templates", "website")
IMAGES_BASE = os.path.join(SCRIPT_DIR, "..", "..", "Dentists", "templates", "images")

# Templates to rotate through
TEMPLATE_IDS = [3, 2, 6, 11, 20, 8]

# ─── Helpers ───────────────────────────────────────────────────────────

def slugify(name):
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def extract_doctor_name(raw_name):
    name = raw_name.strip()
    for suffix in [' LLC', ' PC', ' Inc', ' PLLC']:
        name = name.replace(suffix, '')
    return name.strip()

def extract_short_name(raw_name):
    name = extract_doctor_name(raw_name)
    name = re.sub(r',?\s*DDS$', '', name)
    name = re.sub(r',?\s*DMD$', '', name)
    if len(name) > 30:
        parts = name.split(':')
        if len(parts) > 1:
            name = parts[0].strip()
    return name

def get_doctor_last_name(raw_name):
    """Get a plausible last name for testimonial references like 'Dr. Levy'."""
    name = extract_doctor_name(raw_name)
    name = re.sub(r',?\s*DDS$', '', name)
    name = re.sub(r',?\s*DMD$', '', name)
    # Remove "Dr. " prefix
    name = re.sub(r'^Dr\.\s*', '', name)
    # Remove practice suffixes
    for w in ['Dental', 'Associates', 'Group', 'General', 'Medical', 'PC', 'LLC']:
        name = name.replace(w, '')
    name = name.strip().rstrip(':').strip()
    parts = name.split()
    if parts:
        return parts[-1]
    return name

def extract_city_state(address):
    match = re.search(r',\s*([A-Za-z\s]+),\s*([A-Z]{2})\s+\d', address)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return "", ""

def get_street(address):
    addr = address.replace('\n', ' ').replace('îƒˆ', '').strip()
    parts = addr.split(',')
    return parts[0].strip() if parts else addr

def seed_from_name(name):
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)


# ─── Competitor generation ─────────────────────────────────────────────

CITY_COMPETITORS = {
    "New York": [
        ("Park Avenue Dental", 4.8, 342), ("Manhattan Smiles", 4.7, 218),
        ("NYC Dental Group", 4.6, 567), ("Bright Dental NYC", 4.9, 189),
        ("Metro Dental Care", 4.5, 423), ("Upper East Dental", 4.8, 301),
    ],
    "Houston": [
        ("Houston Premier Dental", 4.7, 389), ("Bayou City Smiles", 4.8, 256),
        ("Texas Dental Experts", 4.6, 445), ("Gulf Coast Dental", 4.9, 178),
        ("Lone Star Dentistry", 4.5, 512), ("Space City Dental", 4.7, 234),
    ],
    "DFW": [
        ("DFW Dental Excellence", 4.8, 367), ("North Texas Smiles", 4.7, 289),
        ("Metroplex Dental Care", 4.6, 478), ("Prairie Dental Group", 4.9, 156),
        ("Lone Star Family Dental", 4.5, 534), ("Fort Worth Dental", 4.7, 312),
    ],
    "Atlanta": [
        ("Peachtree Dental", 4.8, 298), ("Atlanta Premier Smiles", 4.7, 187),
        ("Georgia Dental Group", 4.6, 423), ("Buckhead Dental Care", 4.9, 165),
        ("Southern Smiles ATL", 4.5, 356), ("Midtown Dental Atlanta", 4.7, 234),
    ],
    "Phoenix": [
        ("Desert Smiles Dental", 4.8, 312), ("Phoenix Dental Excellence", 4.7, 245),
        ("Valley Dental Care", 4.6, 389), ("Sonoran Dental Group", 4.9, 167),
        ("AZ Premier Dental", 4.5, 456), ("Scottsdale Smiles", 4.7, 278),
    ],
    "Tampa": [
        ("Tampa Bay Dental", 4.8, 278), ("Gulf Breeze Smiles", 4.7, 198),
        ("Sunshine Dental Care", 4.6, 345), ("Bay Area Dental Group", 4.9, 156),
        ("Florida Premier Dental", 4.5, 423), ("Clearwater Smiles", 4.7, 234),
    ],
}

CITY_ALIASES = {
    "NYC": "New York", "New York": "New York",
    "Houston": "Houston",
    "DFW": "DFW", "Dallas": "DFW",
    "Atlanta": "Atlanta",
    "Phoenix": "Phoenix",
    "Tampa": "Tampa",
}

def get_competitors(city_name, dentist_name, n=3):
    resolved = CITY_ALIASES.get(city_name, city_name)
    comps = CITY_COMPETITORS.get(resolved, CITY_COMPETITORS["New York"])
    rng = random.Random(seed_from_name(dentist_name))
    return rng.sample(comps, min(n, len(comps)))


# ─── Template file reading & personalization ───────────────────────────

def read_template_file(tmpl_id, filename):
    """Read a file from a template folder."""
    path = os.path.join(TMPL_BASE, f"template-{tmpl_id}", filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_blog_post(tmpl_id, category, post_filename):
    """Read a blog post from a template folder."""
    path = os.path.join(TMPL_BASE, f"template-{tmpl_id}", "blog-en", category, post_filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_blog_posts(tmpl_id):
    """Get all blog post paths for a template."""
    blog_dir = os.path.join(TMPL_BASE, f"template-{tmpl_id}", "blog-en")
    posts = []
    for cat_dir in sorted(os.listdir(blog_dir)):
        cat_path = os.path.join(blog_dir, cat_dir)
        if os.path.isdir(cat_path):
            for html_file in sorted(os.listdir(cat_path)):
                if html_file.endswith('.html'):
                    posts.append((cat_dir, html_file))
    return posts

def personalize(html, d):
    """Replace template placeholders with real dentist data."""
    name = extract_doctor_name(d['name'])
    short = extract_short_name(d['name'])
    last_name = get_doctor_last_name(d['name'])
    city, state = extract_city_state(d['address'])
    location = f"{city}, {state}" if city and state else d.get('city', '')
    cat = d.get('categories', 'Dentist').strip() or 'Dentist'
    rating = d.get('rating', '4.0')
    reviews = d.get('review_count', '0')
    phone = d.get('phone', '').strip()
    address = get_street(d['address'])
    tel_href = phone.replace(' ', '').replace('(', '').replace(')', '')

    # Order matters: longer strings first
    replacements = [
        ('Smile Plus Dental', short),
        ('Smile Plus', short),
        ('Dr. Michelle Levy', name),
        ('Michelle Levy', name),
        ('Dr. Levy', f'Dr. {last_name}'),
        ('Noa Cohen', 'Sarah Mitchell'),
        ('03-555-1234', phone),
        ('tel:03-555-1234', f'tel:{tel_href}'),
        ('45 Rothschild Blvd', address),
        ('45 Rothschild', address),
        ('Tel Aviv', location),
        # Rating/reviews in specific contexts
        ('>4.9<', f'>{rating}<'),
        ('>187 Reviews<', f'>{reviews} Reviews<'),
        ('>187<', f'>{reviews}<'),
        # Catch remaining patterns: "· 187 Reviews", "187+ Reviews on Google", "(187 Reviews)"
        ('187 Reviews', f'{reviews} Reviews'),
        ('187+', f'{reviews}+'),
    ]

    for old, new in replacements:
        html = html.replace(old, new)

    return html

def fix_image_paths_main(html):
    """Fix image paths in main-level files (index.html, blog.html)."""
    # ../../images/ → images/
    html = html.replace('../../images/', 'images/')
    return html

def fix_image_paths_blog_post(html):
    """Fix image paths in blog posts (blog/category/post.html)."""
    # ../../../../../images/ → ../../images/
    html = html.replace('../../../../../images/', '../../images/')
    # Also handle ../../images/ (some posts may use this)
    # Don't double-replace: only fix if still has ../../../
    html = html.replace('../../../images/', '../../images/')
    return html

def fix_blog_links_main(html):
    """Fix blog link from blog-en.html to blog.html in main template."""
    html = html.replace('blog-en.html', 'blog.html')
    return html

def fix_blog_links_in_blog(html):
    """Fix links in blog listing page."""
    # blog-en/category/post.html → blog/category/post.html
    html = html.replace('blog-en/', 'blog/')
    # template_example-N-en.html → index.html
    html = re.sub(r'template_example-\d+-en\.html', 'index.html', html)
    html = re.sub(r'template_example-\d+\.html', 'index.html', html)
    html = html.replace('blog-en.html', 'blog.html')
    return html

def load_reviews():
    """Load real Google reviews from reviews.json."""
    if os.path.exists(REVIEWS_PATH):
        with open(REVIEWS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Fake reviewer names used in all templates
FAKE_NAMES = ['Noa Cohen', 'Yossi Abraham', 'Shira David']
FAKE_TEXTS = [
    'Dr. Levy changed my life',
    'I had dental implants at this clinic',
    'Amazing place! I came for the first time',
]

def inject_real_reviews(html, reviews):
    """Replace fake testimonial names/texts with real Google review data."""
    if not reviews:
        return html

    for i, fake_name in enumerate(FAKE_NAMES):
        if i < len(reviews):
            rev = reviews[i]
            real_name = rev['name']
            real_text = rev.get('text', '') or 'Great experience at this dental office.'
            real_initial = real_name[0].upper()
            fake_initial = fake_name[0].upper()

            # Replace reviewer name (appears in .name div and .testimonial-name div)
            html = html.replace(f'>{fake_name}<', f'>{real_name}<')
            # Replace avatar initial
            html = html.replace(f'>{fake_initial}<', f'>{real_initial}<', 1)

        # Replace review text (find the fake text snippet and replace the full text)
        if i < len(reviews) and i < len(FAKE_TEXTS):
            rev = reviews[i]
            real_text = rev.get('text', '') or 'Great experience at this dental office.'
            # Find the paragraph/blockquote containing the fake text and replace
            fake_snippet = FAKE_TEXTS[i]
            # Match the full text content in testimonial-text or blockquote
            pattern = re.compile(
                r'(class="testimonial-text">|<blockquote>)([^<]*' + re.escape(fake_snippet) + r'[^<]*)(</p>|</blockquote>)',
                re.DOTALL
            )
            html = pattern.sub(lambda m: m.group(1) + real_text + m.group(3), html)

    return html


def fix_blog_post_links(html):
    """Fix navigation links in blog posts back to main pages."""
    # The blog posts link back to ../blog-en.html etc
    html = html.replace('blog-en.html', 'blog.html')
    html = html.replace('blog-en/', 'blog/')
    # Fix "back to site" links - posts are in blog/cat/, so site root is ../../
    # template_example links → ../../index.html
    html = re.sub(
        r'href="(?:\.\./)*template_example-\d+-en\.html"',
        'href="../../index.html"',
        html
    )
    html = re.sub(
        r'href="(?:\.\./)*template_example-\d+\.html"',
        'href="../../index.html"',
        html
    )
    return html

def get_needed_images(tmpl_id):
    """Collect all unique image filenames needed for a template."""
    images = set()

    # From main template
    html = read_template_file(tmpl_id, f"template_example-{tmpl_id}-en.html")
    for m in re.findall(r'(?:../../images|images)/((?:template-images|blog-images)/[^"\']+)', html):
        images.add(m)

    # From blog listing
    try:
        blog_html = read_template_file(tmpl_id, "blog-en.html")
        for m in re.findall(r'(?:\.\./)*images/((?:template-images|blog-images)/[^"\']+)', blog_html):
            images.add(m)
    except FileNotFoundError:
        pass

    # From blog posts
    for cat, post in get_blog_posts(tmpl_id):
        post_html = read_blog_post(tmpl_id, cat, post)
        for m in re.findall(r'(?:\.\./)*images/((?:template-images|blog-images)/[^"\']+)', post_html):
            images.add(m)

    return images


# ─── content.md generation ─────────────────────────────────────────────

ARTICLE_TOPICS = {
    "Dentist": [
        ("5 Signs You Need to See a Dentist Right Away", "Warning signs like persistent toothache, bleeding gums, and sensitivity that shouldn't be ignored."),
        ("The Complete Guide to Dental Implants", "Everything patients need to know about implants: procedure, recovery, costs, and long-term benefits."),
        ("How to Choose the Right Dentist for Your Family", "Key factors to consider including location, insurance, specialties, and patient reviews."),
    ],
    "Orthodontist": [
        ("Braces vs. Invisalign: Which Is Right for You?", "A comparison of traditional braces and clear aligners covering cost, comfort, and effectiveness."),
        ("When Should Your Child First See an Orthodontist?", "AAO recommends age 7 — why early evaluation matters for jaw development and spacing issues."),
        ("Adult Orthodontics: It's Never Too Late for a Great Smile", "Modern options like clear aligners and lingual braces make adult treatment discreet and effective."),
    ],
    "Endodontist": [
        ("Root Canal Myths vs. Reality", "Debunking common fears about root canals — modern treatment is virtually painless."),
        ("When to See an Endodontist Instead of a General Dentist", "Complex cases, retreatments, and microsurgery that require specialist expertise."),
        ("How to Know If You Need a Root Canal", "Signs and symptoms including persistent pain, sensitivity to hot/cold, and gum swelling."),
    ],
    "Dental clinic": [
        ("The Importance of Regular Dental Checkups", "Why twice-yearly visits are crucial for preventing cavities, gum disease, and oral cancer."),
        ("A Parent's Guide to Children's Dental Health", "From first tooth to teenage years — tips for building lifelong oral hygiene habits."),
        ("Understanding Dental Insurance and Payment Options", "Navigating PPOs, HMOs, discount plans, and financing options for dental care."),
    ],
}

def generate_content_md(d, real_reviews=None):
    name = extract_doctor_name(d['name'])
    short = extract_short_name(d['name'])
    city, state = extract_city_state(d['address'])
    cat = d.get('categories', 'Dentist').strip() or 'Dentist'
    rating = d.get('rating', '4.0')
    reviews = d.get('review_count', '0')
    phone = d.get('phone', '')
    address = get_street(d['address'])
    city_name = d.get('city_name', '').strip()
    articles = ARTICLE_TOPICS.get(cat, ARTICLE_TOPICS["Dentist"])
    comps = get_competitors(city_name, name)

    content = f"""# {name} — Content Package

## Practice Info
- **Name:** {name}
- **Brand:** {short}
- **Category:** {cat}
- **Address:** {address}, {city}, {state}
- **Phone:** {phone}
- **Google Rating:** {rating} ({reviews} reviews)

---

## Website Content

### Hero
- **Headline:** Quality Dental Care You Can Trust
- **Sub:** {short} in {city}, {state} — personalized care for your comfort, health, and confidence.

### About
At {short}, we provide exceptional dental care in a comfortable, welcoming environment. Years of experience plus the latest dental technologies mean outstanding results for every patient.

### Services
- General/Cosmetic Dentistry, Implants, Emergency Care (adapted per specialty)

---

## Blog Articles

"""
    for i, (title, desc) in enumerate(articles, 1):
        content += f"### Article {i}: {title}\n{desc}\n\n"

    # Real Google Reviews section
    content += "---\n\n## Real Google Reviews\n\n"
    if real_reviews:
        for rev in real_reviews:
            stars = '★' * rev.get('rating', 5) + '☆' * (5 - rev.get('rating', 5))
            content += f"- **{rev['name']}** {stars}\n"
            if rev.get('text'):
                content += f"  > {rev['text']}\n"
            content += "\n"
    else:
        content += "_No reviews scraped yet._\n\n"

    content += f"""---

## Proposal Data

### Competitors
"""
    for cn, cr, cv in comps:
        content += f"- **{cn}:** {cr} rating, {cv} reviews\n"

    content += f"""
### Key Insight
- {rating} rating is {'excellent' if float(rating) >= 4.3 else 'good'}, but only {reviews} reviews
- No website — missed patients searching online
- Competitors have 150-500+ reviews
"""
    return content


# ─── Proposal HTML (Template 6 Frost) ─────────────────────────────────

def generate_proposal(d):
    name = extract_doctor_name(d['name'])
    city, state = extract_city_state(d['address'])
    location = f"{city}, {state}" if city and state else d.get('city', '')
    rating = float(d.get('rating', '4.0'))
    reviews = int(d.get('review_count', '0'))
    city_name = d.get('city_name', '').strip()
    comps = get_competitors(city_name, name)
    top_reviews = max(c[2] for c in comps)
    position = sum(1 for c in comps if c[2] > reviews) + 1
    total = len(comps) + 1
    multiplier = round(top_reviews / max(reviews, 1), 1)

    calc_rows = ""
    for add in [0, 5, 10, 15, 20]:
        new_total = reviews + add
        new_rating = round((rating * reviews + 5.0 * add) / max(new_total, 1), 1)
        improvement = round(new_rating - rating, 1)
        label = "Today" if add == 0 else f"+{add}"
        imp = "—" if add == 0 else f"+{improvement}"
        calc_rows += f"        <tr><td>{label}</td><td>{new_rating}</td><td>{imp}</td></tr>\n"

    comp_headers = '        <td class="comp-cell cell-you">You</td>\n'
    for c in comps:
        comp_headers += f'        <td class="comp-cell">{c[0]}</td>\n'

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

    rows_html = comp_row("Google Rating", rating, [c[1] for c in comps])
    rows_html += comp_row("Reviews", reviews, [c[2] for c in comps], " reviews-row")
    rows_html += comp_row("Website", "&#10005;", ["&#10003;"] * len(comps))

    comp_refs = " | ".join(f'<span>{c[0]} — {c[1]} ({c[2]} Reviews)</span>' for c in comps)
    pos_suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(position, 'th')

    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Digital Analysis — {name}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700&family=Instrument+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
html{{font-size:16px}}
body{{font-family:'Instrument Sans','Heebo',sans-serif;background:#fafbfd;color:#1a1e2e;line-height:1.6;direction:ltr}}
.container{{max-width:720px;margin:0 auto;padding:0 32px}}
.hero-line{{height:2px;background:#7b8cc4}}
.hero{{padding:48px 0 0}}
.hero-meta{{font-family:'Instrument Sans',sans-serif;font-size:12px;text-transform:uppercase;letter-spacing:0.3em;color:#999;margin-bottom:20px}}
.hero-name{{font-family:'Heebo',sans-serif;font-size:64px;font-weight:700;line-height:1.05;color:#1a1e2e;margin-bottom:8px}}
@media(max-width:600px){{.hero-name{{font-size:36px}}}}
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
.cell-label{{text-align:left;font-weight:700;font-size:13px;color:#666}}
.cell-you{{background:rgba(123,140,196,0.04);font-weight:700}}
.cell-comp{{color:#666}}
.reviews-row{{background:rgba(123,140,196,0.03)}}
.win{{color:#4ade80;font-weight:700}}
.lose{{color:#c7a0b8;font-weight:700}}
.callout{{border-left:2px solid #7b8cc4;padding:0 20px;font-family:'Heebo',sans-serif;font-size:14px;line-height:1.7;color:#666;margin-top:28px}}
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
    <p class="hero-meta">Digital Analysis — March 2026</p>
    <h1 class="hero-name">{name}</h1>
    <p class="hero-city">{location}</p>
    <hr class="hr">
    <div class="stats-strip">
      <div class="stat-item"><div class="stat-number">{rating}</div><div class="stat-label">Google Rating</div></div>
      <div class="stat-divider"></div>
      <div class="stat-item"><div class="stat-number">{reviews}</div><div class="stat-label">Reviews</div></div>
      <div class="stat-divider"></div>
      <div class="stat-item"><div class="stat-number">0</div><div class="stat-label">Website Score</div></div>
    </div>
</div></section>

<section class="section"><div class="container">
    <hr class="hr"><div style="height:80px"></div>
    <p class="section-label">Competitor Comparison</p>
    <table class="comp-table">
      <tr class="comp-header-row">
        <td class="comp-cell"></td>
{comp_headers}      </tr>
{rows_html}    </table>
    <div class="callout">Your Position: {position}{pos_suffix} out of {total} by reviews. The leading competitor has {top_reviews} reviews — {multiplier}x more than you.</div>
</div></section>

<section class="section"><div class="container">
    <hr class="hr"><div style="height:80px"></div>
    <p class="section-label">Reputation Analysis</p>
    <div class="rating-block"><div class="rating-number">{rating}</div><div class="rating-label">{reviews} Reviews</div></div>
    <p class="insight-text">{'Excellent' if rating >= 4.3 else 'Good'} rating — but only {reviews} reviews. Low volume hurts both credibility and rankings. New patients look for volume of proof, not just score.</p>
    <table class="calc-table">
      <thead><tr><th>New Reviews</th><th>New Rating</th><th>Improvement</th></tr></thead>
      <tbody>
{calc_rows}      </tbody>
    </table>
    <div class="comp-refs">{comp_refs}</div>
    <p class="urgency-text">Your rating is {'excellent' if rating >= 4.3 else 'good'}, but with only {reviews} reviews you appear "new" compared to competitors with hundreds. Every month without a review collection plan widens the gap.</p>
</div></section>

<section class="cta-section"><div class="container">
    <div class="cta-line"></div>
    <h2 class="cta-headline">Want to See the Full Analysis?</h2>
    <p class="cta-sub">Including review analysis, keyword research, and full digital presence audit.<br>10 minutes on Zoom — interested?</p>
</div></section>

<footer class="footer"><p>Based on public data from Google | March 2026</p></footer>
</body>
</html>"""


# ─── Image copying ─────────────────────────────────────────────────────

def copy_images(tmpl_id, dest_folder):
    """Copy all needed images for a template into dest_folder/images/."""
    needed = get_needed_images(tmpl_id)

    for rel_path in needed:
        src = os.path.join(IMAGES_BASE, rel_path)
        dst = os.path.join(dest_folder, "images", rel_path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copy2(src, dst)


# ─── Main ──────────────────────────────────────────────────────────────

def main():
    # Clean output dir
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Load real reviews
    all_reviews = load_reviews()
    print(f"Loaded reviews for {len(all_reviews)} dentists")
    print(f"Processing {len(rows)} dentists...\n")

    for i, d in enumerate(rows):
        name = extract_doctor_name(d['name'])
        slug = slugify(name)
        folder = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(folder, exist_ok=True)

        # Assign template (rotate)
        tmpl_id = TEMPLATE_IDS[i % len(TEMPLATE_IDS)]

        # Get real reviews for this dentist
        dentist_reviews = all_reviews.get(d['name'].strip(), [])

        # 1. Read & personalize website template
        website_html = read_template_file(tmpl_id, f"template_example-{tmpl_id}-en.html")
        website_html = inject_real_reviews(website_html, dentist_reviews)
        website_html = personalize(website_html, d)
        website_html = fix_image_paths_main(website_html)
        website_html = fix_blog_links_main(website_html)
        with open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(website_html)

        # 2. Read & personalize blog listing
        try:
            blog_html = read_template_file(tmpl_id, "blog-en.html")
            blog_html = personalize(blog_html, d)
            blog_html = fix_image_paths_main(blog_html)
            blog_html = fix_blog_links_in_blog(blog_html)
            with open(os.path.join(folder, 'blog.html'), 'w', encoding='utf-8') as f:
                f.write(blog_html)
        except FileNotFoundError:
            print(f"  WARNING: No blog-en.html for template {tmpl_id}")

        # 3. Read & personalize blog posts
        for cat, post_file in get_blog_posts(tmpl_id):
            post_html = read_blog_post(tmpl_id, cat, post_file)
            post_html = personalize(post_html, d)
            post_html = fix_image_paths_blog_post(post_html)
            post_html = fix_blog_post_links(post_html)

            post_dir = os.path.join(folder, "blog", cat)
            os.makedirs(post_dir, exist_ok=True)
            with open(os.path.join(post_dir, post_file), 'w', encoding='utf-8') as f:
                f.write(post_html)

        # 4. Copy images
        copy_images(tmpl_id, folder)

        # 5. content.md
        content_md = generate_content_md(d, real_reviews=dentist_reviews)
        with open(os.path.join(folder, 'content.md'), 'w', encoding='utf-8') as f:
            f.write(content_md)

        # 6. proposal.html
        proposal_html = generate_proposal(d)
        with open(os.path.join(folder, 'proposal.html'), 'w', encoding='utf-8') as f:
            f.write(proposal_html)

        img_count = sum(len(files) for _, _, files in os.walk(os.path.join(folder, "images")))
        blog_count = len(get_blog_posts(tmpl_id))
        rev_count = len(dentist_reviews)
        print(f"  [{i+1:2d}/{len(rows)}] {slug}/ (tmpl-{tmpl_id}, {img_count} imgs, {blog_count} posts, {rev_count} reviews)")

    print(f"\nDone! Created {len(rows)} folders in: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
