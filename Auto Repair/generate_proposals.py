#!/usr/bin/env python3
"""Generate personalized HTML proposal reports for auto repair shops.

Adapted from Dentists/generate_proposals.py for US auto repair vertical.
Reads enriched S4 leads, finds competitors in same city, builds comparison
table with review quotes, outputs personalized proposals.

Usage:
  python3 generate_proposals.py                      # all leads
  python3 generate_proposals.py --segment 4b         # only S4b
  python3 generate_proposals.py --test 5             # first 5 per segment
  python3 generate_proposals.py --name "Space city"  # single business (partial match)
  python3 generate_proposals.py --template template-1-gazette-en.html
"""
import argparse, csv, os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "s4-leads-enriched.csv")
ALL_CSV_PATH = os.path.join(SCRIPT_DIR, "apify-all-auto-repair.csv")
TEMPLATES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "templates", "proposals")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "proposals", "output")

# Sample data in English templates (to be replaced)
SAMPLE_NAME = "Dr. Meital Segev Neuhoff"
SAMPLE_CITY = "Tel Aviv"

# Which English templates to use (1=Gazette, 4=Dusk, 6=Frost, 10=Amethyst)
SEGMENT_TEMPLATES = {
    "4b": "template-1-gazette-en.html",
    "4a": "template-4-dusk-en.html",
}
ALLOWED_TEMPLATES = [
    "template-1-gazette-en.html",
    "template-4-dusk-en.html",
    "template-6-frost-en.html",
    "template-10-amethyst-en.html",
    "template-11-ironworks-en.html",
    "template-12-asphalt-en.html",
    "template-13-chrome-en.html",
    "template-14-torque-en.html",
    "template-15-garage-en.html",
    "template-16-piston-en.html",
    "template-17-carbon-en.html",
    "template-18-grease-en.html",
    "template-19-horsepower-en.html",
    "template-20-junction-en.html",
]

CHAIN_KEYWORDS = [
    "firestone", "jiffy lube", "midas", "pep boys", "pepboys",
    "valvoline", "goodyear", "discount tire", "maaco", "meineke",
    "aamco", "safelite", "caliber collision", "service king",
    "take 5", "ntb ", "national tire", "brake masters", "sun devil",
    "big o tires", "les schwab", "christian brothers",
]

# ── Helpers ──────────────────────────────────────────────────

def safe_float(v, d=0.0):
    try: return float(v) if v else d
    except (ValueError, TypeError): return d

def safe_int(v, d=0):
    try: return int(float(v)) if v else d
    except (ValueError, TypeError): return d

def is_chain(name):
    return any(kw in name.lower() for kw in CHAIN_KEYWORDS)

def sanitize_filename(name, idx):
    clean = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '-').lower()[:50]
    return f"{idx:03d}-{clean}"

def build_city_index(shops):
    """Build index of all shops by city for competitor lookup."""
    idx = {}
    for s in shops:
        if is_chain(s.get("name", "")): continue
        city = s.get("city", "").strip()
        if city: idx.setdefault(city, []).append(s)
    for city in idx:
        idx[city].sort(key=lambda r: safe_int(r.get("review_count")), reverse=True)
    return idx

def find_top_competitors(name, city, city_index, n=3):
    """Find top N competitors in same city (by review count), excluding self."""
    return [c for c in city_index.get(city, []) if c.get("name") != name][:n]

# ── Review quotes builder ────────────────────────────────────

def build_reviews_section(shop):
    """Build HTML for customer review quotes section."""
    reviews = []
    for j in range(1, 6):
        name = shop.get(f"review{j}_name", "").strip()
        stars = safe_int(shop.get(f"review{j}_stars"))
        text = shop.get(f"review{j}_text", "").strip()
        if text:
            reviews.append({"name": name, "stars": stars, "text": text})

    if not reviews:
        return ""

    html = '<div class="reviews-quotes" style="margin:32px 0;padding:24px;background:rgba(155,142,194,0.06);border:1px solid rgba(155,142,194,0.15);border-radius:8px;">\n'
    html += '  <h3 style="font-family:var(--playfair);font-size:22px;margin-bottom:16px;color:var(--accent);">What Your Customers Say</h3>\n'

    for r in reviews[:3]:
        star_str = "★" * r["stars"] + "☆" * (5 - r["stars"]) if r["stars"] else ""
        html += f'  <div style="margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid rgba(155,142,194,0.1);">\n'
        html += f'    <div style="font-size:13px;color:var(--accent);margin-bottom:4px;">{star_str}</div>\n'
        html += f'    <div style="font-style:italic;color:var(--text);line-height:1.6;">"{r["text"][:200]}"</div>\n'
        html += f'    <div style="font-size:12px;color:var(--text-dim);margin-top:4px;">— {r["name"]}</div>\n'
        html += f'  </div>\n'

    html += '</div>'
    return html

# ── Comp table builder ───────────────────────────────────────

def _cls(you, comp, higher=True):
    if higher: return " win" if comp > you else (" lose" if comp < you else "")
    return " win" if comp < you else (" lose" if comp > you else "")

def _chk(v): return "&#10003;" if v else "&#10007;"

def build_comp_table(shop, competitors):
    """Build comparison table HTML (uses <table> to match English templates)."""
    cr = safe_float(shop.get("rating"))
    cv = safe_int(shop.get("review_count"))
    cfb = bool(shop.get("facebook_url", "").strip())
    cig = bool(shop.get("instagram_url", "").strip())
    cem = bool(shop.get("email", "").strip())
    cweb = shop.get("has_website", "no") == "yes"

    comps = list(competitors[:3])
    while len(comps) < 3: comps.append({})

    rows = []
    # Header
    rows.append('<tr class="comp-header-row">')
    rows.append('  <th class="cell-label"></th>')
    rows.append(f'  <th class="cell-you">You</th>')
    for c in comps:
        rows.append(f'  <th class="cell-comp">{c.get("name","—")[:30]}</th>')
    rows.append('</tr>')

    # Google Rating
    rows.append('<tr class="comp-row">')
    rows.append('  <td class="cell-label">Google Rating</td>')
    rows.append(f'  <td class="cell-you comp-cell">{cr}</td>')
    for c in comps:
        v = safe_float(c.get("rating"))
        rows.append(f'  <td class="cell-comp comp-cell{_cls(cr, v)}">{v}</td>')
    rows.append('</tr>')

    # Reviews
    rows.append('<tr class="comp-row reviews-row">')
    rows.append('  <td class="cell-label">Reviews</td>')
    rows.append(f'  <td class="cell-you comp-cell">{cv}</td>')
    for c in comps:
        v = safe_int(c.get("review_count"))
        rows.append(f'  <td class="cell-comp comp-cell{_cls(cv, v)}">{v}</td>')
    rows.append('</tr>')

    # Website
    rows.append('<tr class="comp-row">')
    rows.append('  <td class="cell-label">Website</td>')
    rows.append(f'  <td class="cell-you comp-cell">{_chk(cweb)}</td>')
    for c in comps:
        has = c.get("has_website", c.get("website", ""))
        has_it = has == "yes" or (has and has.startswith("http") and "facebook" not in has)
        rows.append(f'  <td class="cell-comp comp-cell{" win" if has_it and not cweb else ""}">{_chk(has_it)}</td>')
    rows.append('</tr>')

    # Facebook
    rows.append('<tr class="comp-row">')
    rows.append('  <td class="cell-label">Facebook</td>')
    rows.append(f'  <td class="cell-you comp-cell">{_chk(cfb)}</td>')
    for c in comps:
        has = bool(c.get("facebook_url", "").strip())
        rows.append(f'  <td class="cell-comp comp-cell">{_chk(has)}</td>')
    rows.append('</tr>')

    # Instagram
    rows.append('<tr class="comp-row">')
    rows.append('  <td class="cell-label">Instagram</td>')
    rows.append(f'  <td class="cell-you comp-cell">{_chk(cig)}</td>')
    for c in comps:
        has = bool(c.get("instagram_url", "").strip())
        rows.append(f'  <td class="cell-comp comp-cell">{_chk(has)}</td>')
    rows.append('</tr>')

    return "\n".join(rows)

def _replace_comp_table(html, new_inner):
    """Replace the comp-table contents in the HTML."""
    # Find the <table class="comp-table"> or <div class="comp-table">
    patterns = [
        (r'(<table\s+class="comp-table"[^>]*>)\s*<thead>.*?</tbody>\s*(</table>)',
         r'\1\n<thead></thead>\n<tbody>\n' + new_inner + r'\n</tbody>\n\2'),
    ]
    for pat, repl in patterns:
        new_html = re.sub(pat, repl, html, flags=re.DOTALL)
        if new_html != html:
            return new_html

    # Fallback: find comp-table and replace between opening/closing tags
    start = html.find('class="comp-table')
    if start < 0: return html
    tag_start = html.rfind('<', 0, start + 1)
    tag = 'table' if '<table' in html[tag_start:tag_start+10] else 'div'
    tag_end_pos = html.find(f'</{tag}>', start)
    if tag_end_pos < 0: return html
    opener_end = html.find('>', tag_start) + 1
    return html[:opener_end] + '\n<tbody>\n' + new_inner + '\n</tbody>\n' + html[tag_end_pos:]

# ── Personalization engine ───────────────────────────────────

def personalize_template(html, shop, competitors):
    name = shop.get("name", "")
    city = shop.get("city", "").strip()
    state = shop.get("state", "").strip()
    rating = safe_float(shop.get("rating"))
    reviews = safe_int(shop.get("review_count"))

    # 1) Title
    html = re.sub(r'(<title>).*?(</title>)',
                  rf'\g<1>Digital Analysis — {name}\g<2>', html)

    # 2) Business name (replace sample name)
    html = html.replace(SAMPLE_NAME, name)

    # 3) City
    html = html.replace(SAMPLE_CITY, f"{city}, {state}")
    html = html.replace("Ramat Gan", f"{city}, {state}")

    # 4) Replace dental/clinic references with auto repair
    html = html.replace("dental clinic", "auto repair shop")
    html = html.replace("Dental Clinic", "Auto Repair Shop")
    html = html.replace("dental", "auto repair")
    html = html.replace("clinic", "shop")
    html = html.replace("מרפאת שיניים", "auto repair shop")
    html = html.replace("מרפאה", "shop")
    html = html.replace("מרפאות מובילות", "top competitors")
    html = html.replace("ביקורות", "reviews")

    # 5) Rating
    html = html.replace('>5.0<', f'>{rating}<', 1)
    html = re.sub(r'(class="rating-huge">)5\.0(<)', rf'\g<1>{rating}\2', html)

    # 6) Review count — replace the sample "24"
    for pat in [r'(class="stat-number">)24(<)', r'(class="big-num">)24(<)',
                r'(class="big-number">)24(<)', r'(class="reviews-num">)24(<)',
                r'(class="review-count">)24(<)',]:
        html = re.sub(pat, rf'\g<1>{reviews}\2', html, count=1)
    html = re.sub(r'24 Reviews on Google', f'{reviews} Reviews on Google', html)
    html = re.sub(r'24 Reviews', f'{reviews} Reviews', html, count=3)

    # 7) Site score — these shops have no website, so score = 0
    html = html.replace('8/10', '0/10')
    # Update SVG dashoffset for 0/10
    html = re.sub(r'(stroke-dashoffset:\s*)([\d.]+)',
        lambda m: f'{m.group(1)}{m.group(2)}' if float(m.group(2)) < 1 else f'{m.group(1)}226', html)

    # 8) Comp table
    html = _replace_comp_table(html, build_comp_table(shop, competitors))

    # 9) Warning/ranking box
    ranked = sorted(
        [(name, reviews)] + [(c.get("name",""), safe_int(c.get("review_count"))) for c in competitors[:3]],
        key=lambda x: x[1], reverse=True)
    rank = next((i for i,(n,_) in enumerate(ranked,1) if n==name), len(ranked))
    total = len(ranked)
    top_rev = ranked[0][1] if ranked else 0
    mult = round(top_rev / max(reviews, 1), 1)

    html = re.sub(r'מקום \d+ מתוך \d+', f'Rank {rank} of {total}', html)
    html = re.sub(r'>\d+ מתוך \d+<', f'>Rank {rank} of {total}<', html)
    html = re.sub(r'RANKING_POSITION = \d+/\d+', f'RANKING_POSITION = {rank}/{total}', html)
    html = re.sub(r'\d+ ביקורות', f'{top_rev} reviews', html)
    html = re.sub(r'פי [\d.]+', f'{mult}x more', html)

    # 10) Subtitle
    html = re.sub(r'מול\s+\d+\s+מרפאות מובילות',
                  f'vs {len(competitors[:3])} top competitors', html)

    # 11) Insert customer review quotes before the CTA/footer
    reviews_html = build_reviews_section(shop)
    if reviews_html:
        # Insert before the last section or CTA
        cta_pos = html.rfind('class="cta')
        if cta_pos < 0:
            cta_pos = html.rfind('</main>')
        if cta_pos < 0:
            cta_pos = html.rfind('</body>')
        if cta_pos > 0:
            # Find the start of the containing div
            insert_pos = html.rfind('<', 0, cta_pos)
            html = html[:insert_pos] + '\n' + reviews_html + '\n' + html[insert_pos:]

    # 12) Replace competitor reference cards at bottom
    for i, c in enumerate(competitors[:3]):
        # Replace sample competitor names/ratings in reference sections
        html = re.sub(rf'(class="comp-ref-name">).*?(</)',
                      rf'\g<1>{c.get("name","—")[:30]}\2', html, count=1)
        html = re.sub(rf'(class="comp-ref-rating">)[\d.]+(<)',
                      rf'\g<1>{safe_float(c.get("rating"))}\2', html, count=1)

    return html

# ── Main ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate auto repair proposal reports")
    parser.add_argument("--segment", type=str, help="Only generate for this segment (4a or 4b)")
    parser.add_argument("--test", type=int, help="Limit to N shops per segment")
    parser.add_argument("--name", type=str, help="Generate for a single business (partial name match)")
    parser.add_argument("--template", type=str, help="Override template for all shops")
    args = parser.parse_args()

    # Load enriched S4 leads
    s4_shops = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))

    # Load ALL shops (including those with websites) for competitor lookup
    all_shops = list(csv.DictReader(open(ALL_CSV_PATH, encoding="utf-8")))
    city_index = build_city_index(all_shops)

    tpl_cache = {}
    def get_tpl(name):
        if name not in tpl_cache:
            with open(os.path.join(TEMPLATES_DIR, name), encoding="utf-8") as f:
                tpl_cache[name] = f.read()
        return tpl_cache[name]

    # Filter shops
    if args.name:
        shops_to_process = [s for s in s4_shops if args.name.lower() in s.get("name","").lower()]
        if not shops_to_process:
            print(f"No shop found matching '{args.name}'")
            return
    else:
        segments = [args.segment] if args.segment else list(SEGMENT_TEMPLATES.keys())
        shops_to_process = [s for s in s4_shops
                           if s.get("segment_name","").replace("No Website + Good","4b").replace("No Website + Some","4a")
                           in ["4b","4a"] or s.get("segment") in segments]

    if args.test:
        shops_to_process = shops_to_process[:args.test]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    count = 0

    for idx, shop in enumerate(shops_to_process, 1):
        seg = shop.get("segment", "4b")
        tpl_name = args.template or SEGMENT_TEMPLATES.get(str(seg), SEGMENT_TEMPLATES["4b"])

        city = shop.get("city", "").strip()
        comps = find_top_competitors(shop.get("name"), city, city_index, n=3)

        try:
            tpl_html = get_tpl(tpl_name)
        except FileNotFoundError:
            print(f"  WARN: {tpl_name} not found, skipping {shop.get('name')}")
            continue

        html = personalize_template(tpl_html, shop, comps)
        fname = sanitize_filename(shop.get("name", "shop"), idx)
        shop_dir = os.path.join(OUTPUT_DIR, fname)
        os.makedirs(shop_dir, exist_ok=True)

        with open(os.path.join(shop_dir, "proposal.html"), "w", encoding="utf-8") as f:
            f.write(html)
        count += 1

    print(f"Generated {count} proposals → {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
