#!/usr/bin/env python3
"""
Batch generator for Auto Repair websites and proposals.
Phase 1: Creates folder structure, content.md, and proposal.html for 30 businesses.
"""
import csv, os, re, json, html

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
CSV_PATH = os.path.join(BASE, "s4-4b-top100-with-email.csv")
WEBSITES_DIR = os.path.join(BASE, "reports", "websites")
PROPOSALS_DIR = os.path.join(BASE, "reports", "proposals")

# Liked website templates to rotate through
LIKED_TEMPLATES = [7, 9, 11, 12, 14, 16, 21, 25]

# Auto repair services by category keywords
SERVICES_MAP = {
    "default": [
        ("Oil Change & Lube", "Full-synthetic and conventional oil changes with multi-point inspection."),
        ("Brake Repair", "Brake pad replacement, rotor resurfacing, and complete brake system service."),
        ("Engine Diagnostics", "Computer diagnostics to identify check engine lights and performance issues."),
        ("A/C Repair", "Air conditioning recharge, leak detection, and full climate system repair."),
        ("Tire Service", "Tire rotation, balancing, alignment, and new tire installation."),
        ("Transmission Service", "Fluid flush, filter replacement, and complete transmission repair."),
    ],
    "tire": [
        ("New & Used Tires", "Quality new and affordable used tires for all vehicle makes and models."),
        ("Tire Repair & Patching", "Professional flat tire repair, plug, and patch services."),
        ("Wheel Alignment", "Precision 4-wheel alignment to extend tire life and improve handling."),
        ("Tire Balancing", "Computer balancing to eliminate vibration and ensure smooth rides."),
        ("Tire Rotation", "Regular rotation service to maximize tire lifespan and performance."),
        ("Brake Service", "Complete brake inspection, pad replacement, and rotor service."),
    ],
    "body": [
        ("Collision Repair", "Expert collision repair to restore your vehicle to pre-accident condition."),
        ("Paint & Refinishing", "Professional auto painting with perfect color matching technology."),
        ("Dent Removal", "Paintless dent repair and traditional body work for all damage types."),
        ("Frame Straightening", "Precision frame alignment to ensure structural integrity after impact."),
        ("Auto Detailing", "Complete interior and exterior detailing to restore your vehicle's shine."),
        ("Insurance Claims", "We work directly with all major insurance companies for hassle-free repairs."),
    ],
    "glass": [
        ("Windshield Replacement", "OEM and aftermarket windshield replacement for all vehicle types."),
        ("Windshield Repair", "Quick chip and crack repair to prevent further damage."),
        ("Side Window Replacement", "Fast replacement of broken or damaged side windows."),
        ("Rear Window Service", "Back glass replacement including heated and defroster models."),
        ("Mobile Service", "We come to your location for convenient on-site glass service."),
        ("Insurance Processing", "We handle insurance claims directly for zero out-of-pocket repairs."),
    ],
    "mobile": [
        ("On-Site Diagnostics", "We come to you with full diagnostic equipment for accurate troubleshooting."),
        ("Mobile Oil Change", "Convenient oil change service at your home or office location."),
        ("Battery Replacement", "Same-day mobile battery testing and replacement service."),
        ("Brake Service", "Mobile brake pad replacement and rotor service at your location."),
        ("Starter & Alternator", "On-site starter and alternator diagnosis and replacement."),
        ("Emergency Repair", "Urgent mobile repair service when you're stranded or can't drive in."),
    ],
    "inspection": [
        ("State Inspection", "Quick and reliable state vehicle inspection to keep you road-legal."),
        ("Emissions Testing", "Complete emissions testing and repair to pass inspection requirements."),
        ("Oil Change & Lube", "Full-synthetic and conventional oil changes with multi-point inspection."),
        ("Brake Inspection", "Thorough brake system check with detailed report and repair options."),
        ("A/C Service", "Air conditioning diagnosis, recharge, and full system repair."),
        ("General Repair", "Complete auto repair service for all makes and models."),
    ],
}

def slugify(name):
    """Create a URL-safe slug from business name."""
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s[:60].rstrip('-')

def get_services(categories, name):
    """Pick service set based on business category keywords."""
    cats_lower = (categories + " " + name).lower()
    if "glass" in cats_lower:
        return SERVICES_MAP["glass"]
    if "body" in cats_lower or "paint" in cats_lower or "collision" in cats_lower:
        return SERVICES_MAP["body"]
    if "tire" in cats_lower or "wheel" in cats_lower or "llant" in cats_lower:
        return SERVICES_MAP["tire"]
    if "mobile" in cats_lower:
        return SERVICES_MAP["mobile"]
    if "inspection" in cats_lower or "emission" in cats_lower or "lube" in cats_lower:
        return SERVICES_MAP["inspection"]
    return SERVICES_MAP["default"]

def get_competitors(biz, all_rows, idx):
    """Find 3 competitors from same city (different businesses)."""
    city = biz["city"].strip()
    comps = []
    for i, r in enumerate(all_rows):
        if i == idx:
            continue
        if r["city"].strip() == city and r["name"] != biz["name"]:
            comps.append(r)
        if len(comps) >= 3:
            break
    # If not enough from same city, grab from any city
    if len(comps) < 3:
        for i, r in enumerate(all_rows):
            if i == idx and r["name"] != biz["name"] and r not in comps:
                comps.append(r)
            if len(comps) >= 3:
                break
    return comps[:3]

def star_html(rating):
    """Generate star display from numeric rating."""
    full = int(float(rating))
    half = 1 if float(rating) - full >= 0.3 else 0
    return "&#9733;" * full + ("&#189;" if half else "") + ("&#9734;" * (5 - full - half))

def win_lose(biz_val, comp_val, higher_is_better=True):
    """Return 'win' or 'lose' CSS class."""
    try:
        b, c = float(biz_val), float(comp_val)
        if higher_is_better:
            return "win" if b >= c else "lose"
        return "win" if b <= c else "lose"
    except:
        return ""

def generate_proposal(biz, competitors, idx):
    """Generate proposal HTML based on template #13 style (adapted to English LTR)."""
    name = html.escape(biz["name"])
    city = html.escape(biz["city"])
    state = html.escape(biz.get("state", ""))
    rating = biz.get("rating", "0")
    reviews = biz.get("review_count", "0")

    # Competitor rows
    comp_headers = ""
    comp_rating_cells = ""
    comp_review_cells = ""
    comp_website_cells = ""
    comp_refs = []

    for c in competitors:
        cname = html.escape(c["name"][:35])
        comp_headers += f'        <td class="comp-cell">{cname}</td>\n'

        cr = c.get("rating", "0")
        crv = c.get("review_count", "0")
        cw = c.get("has_website", "")

        r_class = win_lose(rating, cr)
        comp_rating_cells += f'        <td class="comp-cell cell-comp {r_class}">{cr}</td>\n'

        rv_class = win_lose(reviews, crv)
        comp_review_cells += f'        <td class="comp-cell cell-comp {rv_class}">{crv}</td>\n'

        w_mark = "&#10003;" if cw.lower() in ("true", "yes", "1") else "&#10005;"
        comp_website_cells += f'        <td class="comp-cell cell-comp">{w_mark}</td>\n'

        comp_refs.append(f'{cname} &mdash; {cr} ({crv} reviews)')

    # Find ranking among competitors
    all_reviews = [int(reviews)] + [int(c.get("review_count", "0")) for c in competitors]
    all_reviews_sorted = sorted(all_reviews, reverse=True)
    rank = all_reviews_sorted.index(int(reviews)) + 1
    total = len(all_reviews)
    top_reviews = max(all_reviews)
    if int(reviews) > 0:
        ratio = round(top_reviews / int(reviews), 1)
    else:
        ratio = "N/A"

    # Review projection
    curr_rating = float(rating) if rating else 0
    curr_reviews = int(reviews) if reviews else 0
    projection_rows = ""
    for add in [0, 10, 25, 50, 100]:
        if add == 0:
            projection_rows += f'        <tr><td>Today</td><td>{curr_rating}</td><td>&mdash;</td></tr>\n'
        else:
            # Assume new reviews are 4.8 avg
            new_total = curr_reviews + add
            new_rating = round((curr_rating * curr_reviews + 4.8 * add) / new_total, 1)
            change = round(new_rating - curr_rating, 1)
            sign = "+" if change >= 0 else ""
            projection_rows += f'        <tr><td>+{add}</td><td>{new_rating}</td><td>{sign}{change}</td></tr>\n'

    # Collect real reviews
    reviews_html = ""
    for j in range(1, 6):
        rname = biz.get(f"review{j}_name", "").strip()
        rtext = biz.get(f"review{j}_text", "").strip()
        rstars = biz.get(f"review{j}_stars", "").strip()
        if rname and rtext:
            star_count = int(float(rstars)) if rstars else 5
            stars_display = "&#9733;" * star_count + "&#9734;" * (5 - star_count)
            reviews_html += f'''    <div class="review-card">
      <div class="review-stars">{stars_display}</div>
      <p class="review-text">"{html.escape(rtext[:200])}"</p>
      <p class="review-author">&mdash; {html.escape(rname)}</p>
    </div>\n'''

    reviews_section = ""
    if reviews_html:
        reviews_section = f'''
<section class="section"><div class="container">
    <hr class="hr"><div style="height:80px"></div>
    <p class="section-label">Your Real Google Reviews</p>
    <div class="reviews-grid">
{reviews_html}    </div>
    <p class="insight-text">These are actual reviews from your Google Business Profile &mdash; powerful social proof that builds trust with new customers.</p>
</div></section>'''

    proposal_html = f'''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Digital Analysis &mdash; {name}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Instrument+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
html{{font-size:16px}}
body{{font-family:'Inter','Instrument Sans',sans-serif;background:#fafbfd;color:#1a1e2e;line-height:1.6}}
.container{{max-width:720px;margin:0 auto;padding:0 32px}}
.hero-line{{height:2px;background:#7b8cc4}}
.hero{{padding:48px 0 0}}
.hero-meta{{font-family:'Instrument Sans',sans-serif;font-size:12px;text-transform:uppercase;letter-spacing:0.3em;color:#999;margin-bottom:20px}}
.hero-name{{font-family:'Inter',sans-serif;font-size:42px;font-weight:700;line-height:1.15;color:#1a1e2e;margin-bottom:8px}}
@media(max-width:600px){{.hero-name{{font-size:28px}}}}
.hero-city{{font-family:'Inter',sans-serif;font-size:18px;color:#7b8cc4;margin-bottom:32px}}
.hr{{height:1px;background:#eee;border:none}}
.stats-strip{{display:flex;align-items:center;padding:28px 0}}
.stat-item{{flex:1;text-align:center}}
.stat-divider{{width:1px;height:48px;background:#ddd;flex-shrink:0}}
.stat-number{{font-family:'Instrument Sans',sans-serif;font-size:44px;font-weight:700;color:#1a1e2e;line-height:1}}
.stat-label{{font-size:11px;color:#999;text-transform:uppercase;letter-spacing:0.08em;margin-top:6px}}
.section{{padding:80px 0 0}}
.section-label{{font-family:'Instrument Sans',sans-serif;font-size:14px;text-transform:uppercase;letter-spacing:0.2em;color:#999;margin-bottom:32px}}
.comp-table{{width:100%;border-collapse:collapse;margin-bottom:24px}}
.comp-header-row .comp-cell{{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;color:#999;padding:0 12px 12px;text-align:center;border-bottom:1px solid #ddd}}
.comp-row{{border-bottom:1px solid #eee}}
.comp-cell{{padding:14px 12px;text-align:center;font-size:14px;vertical-align:middle;color:#1a1e2e}}
.cell-label{{text-align:left;font-weight:700;font-size:13px;color:#666}}
.cell-you{{background:rgba(123,140,196,0.04);font-weight:700}}
.cell-comp{{color:#666}}
.reviews-row{{background:rgba(123,140,196,0.03)}}
.win{{color:#4ade80;font-weight:700}}
.lose{{color:#c7a0b8;font-weight:700}}
.callout{{border-left:2px solid #7b8cc4;padding:0 20px;font-size:14px;line-height:1.7;color:#666;margin-top:28px}}
.rating-block{{text-align:center;margin-bottom:12px}}
.rating-number{{font-family:'Instrument Sans',sans-serif;font-size:72px;font-weight:700;color:#1a1e2e;line-height:1}}
.rating-label{{font-size:14px;color:#999;margin-top:4px}}
.insight-text{{font-size:14px;color:#666;text-align:center;margin:20px 0 40px;line-height:1.7}}
.calc-table{{width:100%;border-collapse:collapse;margin-bottom:40px}}
.calc-table th{{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;color:#999;padding:0 16px 12px;text-align:center;border-bottom:1px solid #ddd}}
.calc-table td{{padding:12px 16px;text-align:center;font-size:14px;border-bottom:1px solid #eee;color:#1a1e2e}}
.calc-table tbody tr:first-of-type td{{font-weight:700}}
.comp-refs{{font-size:13px;color:#999;text-align:center;padding:20px 0;border-top:1px solid #eee;margin-bottom:20px}}
.comp-refs span{{margin:0 12px}}
.urgency-text{{font-size:14px;color:#7b8cc4;text-align:center;margin-top:8px;line-height:1.7}}
.reviews-grid{{display:grid;grid-template-columns:1fr;gap:20px;margin-bottom:32px}}
.review-card{{background:#fff;border:1px solid #eee;border-radius:8px;padding:20px 24px}}
.review-stars{{color:#facc15;font-size:14px;letter-spacing:2px;margin-bottom:8px}}
.review-text{{font-size:14px;color:#444;line-height:1.7;font-style:italic;margin-bottom:8px}}
.review-author{{font-size:13px;color:#999;font-weight:500}}
.cta-section{{padding:80px 0 0}}
.cta-line{{height:2px;background:#7b8cc4;margin-bottom:40px}}
.cta-headline{{font-size:24px;font-weight:700;color:#1a1e2e;margin-bottom:6px}}
.cta-sub{{font-size:14px;color:#999;line-height:1.7}}
.cta-button{{display:inline-block;margin-top:20px;padding:14px 36px;background:#7b8cc4;color:#fff;font-weight:700;font-size:14px;border-radius:6px;text-decoration:none;letter-spacing:0.05em;transition:background 0.25s,transform 0.2s}}
.cta-button:hover{{background:#6474a8;transform:translateY(-2px)}}
.preview-section{{margin-top:32px;padding:24px;background:#f0f2f8;border-radius:8px;text-align:center}}
.preview-section p{{font-size:14px;color:#666;margin-bottom:12px}}
.preview-link{{color:#7b8cc4;font-weight:700;font-size:15px;text-decoration:none}}
.preview-link:hover{{text-decoration:underline}}
.footer{{padding:80px 0 32px;text-align:center;font-family:'Instrument Sans',sans-serif;font-size:11px;color:#ccc}}
@media(max-width:600px){{
  .stats-strip{{flex-direction:column;gap:16px}}
  .stat-divider{{width:80px;height:1px}}
  .comp-table{{font-size:12px}}
  .comp-cell{{padding:10px 6px}}
  .rating-number{{font-size:56px}}
}}
</style>
</head>
<body>
<div class="hero-line"></div>
<section class="hero"><div class="container">
    <p class="hero-meta">Digital Analysis &mdash; March 2026</p>
    <h1 class="hero-name">{name}</h1>
    <p class="hero-city">{city}, {state}</p>
    <hr class="hr">
    <div class="stats-strip">
      <div class="stat-item"><div class="stat-number">{rating}</div><div class="stat-label">Google Rating</div></div>
      <div class="stat-divider"></div>
      <div class="stat-item"><div class="stat-number">{reviews}</div><div class="stat-label">Reviews</div></div>
      <div class="stat-divider"></div>
      <div class="stat-item"><div class="stat-number">0/10</div><div class="stat-label">Website Score</div></div>
    </div>
</div></section>

<section class="section"><div class="container">
    <hr class="hr"><div style="height:80px"></div>
    <p class="section-label">Competitor Comparison</p>
    <table class="comp-table">
      <tr class="comp-header-row">
        <td class="comp-cell"></td>
        <td class="comp-cell cell-you">You</td>
{comp_headers}      </tr>
      <tr class="comp-row">
        <td class="comp-cell cell-label">Google Rating</td>
        <td class="comp-cell cell-you">{rating}</td>
{comp_rating_cells}      </tr>
      <tr class="comp-row reviews-row">
        <td class="comp-cell cell-label">Reviews</td>
        <td class="comp-cell cell-you">{reviews}</td>
{comp_review_cells}      </tr>
      <tr class="comp-row">
        <td class="comp-cell cell-label">Website</td>
        <td class="comp-cell cell-you">&#10005;</td>
{comp_website_cells}      </tr>
    </table>
    <div class="callout">Your position: #{rank} of {total} by review count. The top competitor has {top_reviews} reviews &mdash; {ratio}x more than you.</div>
</div></section>

<section class="section"><div class="container">
    <hr class="hr"><div style="height:80px"></div>
    <p class="section-label">Reputation Analysis</p>
    <div class="rating-block"><div class="rating-number">{rating}</div><div class="rating-label">{reviews} reviews</div></div>
    <p class="insight-text">{"Great rating &mdash; but without a website, potential customers searching online will find your competitors first. A professional website converts your strong reputation into new business." if float(rating) >= 4.5 else "Your reviews show room for improvement. A professional website with your best reviews featured prominently helps control the narrative and build trust."}</p>
    <table class="calc-table">
      <thead><tr><th>New Reviews</th><th>Projected Rating</th><th>Change</th></tr></thead>
      <tbody>
{projection_rows}      </tbody>
    </table>
    <div class="comp-refs">{"</span> | <span>".join(f"<span>{c}</span>" for c in comp_refs)}</div>
    <p class="urgency-text">Every month without a website, you're losing potential customers to competitors who show up in local search. Your {rating}-star rating deserves to be seen.</p>
</div></section>
{reviews_section}
<section class="cta-section"><div class="container">
    <div class="cta-line"></div>
    <h2 class="cta-headline">Want to see the full analysis?</h2>
    <p class="cta-sub">Including keyword research, full digital presence audit, and a website preview built specifically for {name}.<br>10 minutes on a call &mdash; interested?</p>
    <div class="preview-section">
      <p>We've already built a website preview for your business:</p>
      <a class="preview-link" href="../websites/{slugify(biz['name'])}/index.html">View Your Website Preview &rarr;</a>
    </div>
</div></section>

<footer class="footer"><p>Based on public Google data | March 2026</p></footer>
</body>
</html>'''

    return proposal_html

def generate_content_md(biz, services, idx, template_num):
    """Generate content.md for website creation."""
    name = biz["name"]
    city = biz["city"]
    state = biz.get("state", "")
    phone = biz.get("phone", "N/A")
    rating = biz.get("rating", "0")
    review_count = biz.get("review_count", "0")
    address = biz.get("address", "")
    categories = biz.get("categories", "")
    maps_url = biz.get("google_maps_url", "")
    segment = biz.get("segment", "")

    # Reviews
    reviews_md = ""
    for j in range(1, 6):
        rname = biz.get(f"review{j}_name", "").strip()
        rtext = biz.get(f"review{j}_text", "").strip()
        rstars = biz.get(f"review{j}_stars", "").strip()
        if rname and rtext:
            stars = "★" * int(float(rstars)) if rstars else "★★★★★"
            reviews_md += f'- **{rname}** {stars}\n  > {rtext}\n\n'

    # Services
    services_md = "\n".join(f"- **{s[0]}**: {s[1]}" for s in services)

    # Hero text
    cats_lower = (categories + " " + name).lower()
    if "glass" in cats_lower:
        specialty = "Auto Glass"
    elif "body" in cats_lower or "paint" in cats_lower:
        specialty = "Auto Body & Paint"
    elif "tire" in cats_lower:
        specialty = "Tires & Wheels"
    elif "mobile" in cats_lower:
        specialty = "Mobile Mechanic"
    elif "inspection" in cats_lower or "emission" in cats_lower:
        specialty = "Inspection & Service"
    else:
        specialty = "Auto Repair"

    content = f"""# {name} — Content Package

## Business Details
- **Name:** {name}
- **Category:** {categories if categories else specialty}
- **Address:** {address}
- **City:** {city}, {state}
- **Phone:** {phone}
- **Google Rating:** {rating} ({review_count} reviews)
- **Segment:** {segment}
- **Google Maps:** {maps_url}
- **Template:** template-{template_num}

---

## Website Content

### Hero
- **Headline:** {city}'s Trusted {specialty} Shop
- **Subtitle:** {name} — {rating}★ rated with {review_count}+ reviews. Honest service, fair prices.

### About
{name} has built a reputation as one of {city}'s most trusted {specialty.lower()} shops. With a {rating}-star Google rating backed by {review_count}+ customer reviews, we deliver honest diagnostics, quality repairs, and transparent pricing on every job. Located in {city}, {state}, we serve the local community with the care and expertise your vehicle deserves.

### Services
{services_md}

---

## Google Reviews

{reviews_md if reviews_md else "No reviews with text available."}
"""
    return content


def main():
    # Read CSV
    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    first30 = all_rows[:30]

    # Create base directories
    os.makedirs(WEBSITES_DIR, exist_ok=True)
    os.makedirs(PROPOSALS_DIR, exist_ok=True)

    results = []

    for i, biz in enumerate(first30):
        slug = slugify(biz["name"])
        folder_name = f"{i+1:03d}-{slug}"
        template_num = LIKED_TEMPLATES[i % len(LIKED_TEMPLATES)]

        # Create website folder
        web_dir = os.path.join(WEBSITES_DIR, folder_name)
        os.makedirs(web_dir, exist_ok=True)
        os.makedirs(os.path.join(web_dir, "images"), exist_ok=True)

        # Create proposal folder
        prop_dir = os.path.join(PROPOSALS_DIR, folder_name)
        os.makedirs(prop_dir, exist_ok=True)

        # Get services based on category
        services = get_services(biz.get("categories", ""), biz["name"])

        # Generate content.md
        content_md = generate_content_md(biz, services, i, template_num)
        with open(os.path.join(web_dir, "content.md"), "w") as f:
            f.write(content_md)

        # Generate proposal
        competitors = get_competitors(biz, all_rows[:100], i)
        proposal_html = generate_proposal(biz, competitors, i)
        with open(os.path.join(prop_dir, "proposal.html"), "w") as f:
            f.write(proposal_html)

        results.append({
            "idx": i + 1,
            "name": biz["name"],
            "slug": folder_name,
            "template": template_num,
            "city": biz["city"],
            "rating": biz.get("rating", ""),
            "reviews": biz.get("review_count", ""),
        })

        print(f"✓ {i+1:2d}. {biz['name'][:40]:<42} T{template_num:<3} → {folder_name}")

    # Save manifest for website generation agents
    manifest_path = os.path.join(BASE, "reports", "batch-manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ Generated {len(results)} content.md files in: Auto Repair/reports/websites/")
    print(f"✅ Generated {len(results)} proposal.html files in: Auto Repair/reports/proposals/")
    print(f"📋 Manifest saved: Auto Repair/reports/batch-manifest.json")
    print(f"\nNext: Run website HTML generation agents")

if __name__ == "__main__":
    main()
