#!/usr/bin/env python3
"""Generate personalized HTML proposal reports for dental clinics.

Reads templates from reports/proposals/templates/, replaces hardcoded sample data
with real clinic data from labeled-dentals.csv, outputs to reports/proposals/output/{segment}/.
"""
import argparse, csv, os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "labeled-dentals.csv")
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "reports", "proposals", "templates")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "reports", "proposals", "output")

SAMPLE_NAME = "ד״ר מיטל שגב נויהוף"
SAMPLE_CITIES = ["תל אביב", "רמת גן"]

SEGMENT_TEMPLATES = {
    "4b": ["template-4-atelier.html", "template-5-rosewater.html", "template-6-ivory.html"],
    "4a": ["template-5-rosewater.html", "template-4-atelier.html", "template-10-prism.html"],
    "1":  ["template-1-clarity.html", "template-2-prestige.html", "template-10-prism.html"],
    "2":  ["template-3-warmth.html", "template-5-rosewater.html", "template-6-ivory.html"],
    "3b": ["template-7-electric.html", "template-8-aurora.html", "template-9-collage.html"],
    "4":  ["template-6-ivory.html", "template-3-warmth.html", "template-4-atelier.html"],
    "3a": ["template-2-prestige.html", "template-7-electric.html"],
    "3":  ["template-1-clarity.html"],
    "5":  [],
}

CHAIN_KEYWORDS = [
    "מכבידנט", "כללית סמייל", "הכתר", "אלפא דנט", "דנטל פלוס",
    "קופת חולים", "מאוחדת", "לאומית", "רשת שיניים", "dental network",
    "סמייל", "smile center",
]
NON_DENTAL_KEYWORDS = [
    "וטרינר", "מעבדת שיניים", "מעבדה", "הדמיה", "רנטגן", "צילום",
    "עורך דין", "עורכי דין", "רואה חשבון", "יועץ", "עיניי", "עיניים",
    "נפש", "פסיכו", "אורתופד", "קרדיו", "אונקולוג", "נוירולוג",
    "vet", "lab", "imaging", "x-ray", "ophtalm", "psychiatr",
]

# ── Helpers ──────────────────────────────────────────────────

def safe_float(v, d=0.0):
    try: return float(v) if v else d
    except (ValueError, TypeError): return d

def safe_int(v, d=0):
    try: return int(float(v)) if v else d
    except (ValueError, TypeError): return d

def is_chain(r):
    return any(kw in r.get("name", "").lower() for kw in CHAIN_KEYWORDS)

def is_non_dental(r):
    t = (r.get("name", "") + " " + r.get("categories", "")).lower()
    return any(kw in t for kw in NON_DENTAL_KEYWORDS)

def has_booking(r):
    return "booking" in r.get("comments", "").lower()

def sanitize_filename(name, idx):
    clean = re.sub(r'[^\w\s\u0590-\u05FF-]', '', name).strip().replace(' ', '-')[:40]
    return f"{idx:03d}-{clean}"

def build_city_index(clinics):
    idx = {}
    for c in clinics:
        if is_chain(c) or is_non_dental(c): continue
        city = c.get("city", "").strip()
        if city: idx.setdefault(city, []).append(c)
    for city in idx:
        idx[city].sort(key=lambda r: safe_int(r.get("review_count")), reverse=True)
    return idx

def find_top_competitors(name, city, city_index, n=3):
    return [c for c in city_index.get(city, []) if c.get("name") != name][:n]

# ── Comp table builder ──────────────────────────────────────

def _cls(you, comp, higher=True):
    if higher: return " win" if comp > you else (" lose" if comp < you else "")
    return " win" if comp < you else (" lose" if comp > you else "")

def _boolcls(you, comp):
    if comp and not you: return " win"
    if you and not comp: return " lose"
    return ""

def _chk(v): return "&#10003;" if v else "&#10007;"

def _row(label, you_val, comp_vals, extra_cls="", is_bool=False):
    """Build one comp-row. comp_vals = list of (value, css_class_suffix)."""
    rc = f'    <div class="comp-row{extra_cls}">\n'
    rc += f'      <div class="comp-cell cell-label">{label}</div>\n'
    rc += f'      <div class="comp-cell cell-you">{you_val}</div>\n'
    for val, c in comp_vals:
        rc += f'      <div class="comp-cell cell-comp{c}">{val}</div>\n'
    rc += '    </div>'
    return rc

def build_comp_table(clinic, competitors):
    """Build fresh comp-table inner HTML with real data."""
    cr = safe_float(clinic.get("rating"))
    cv = safe_int(clinic.get("review_count"))
    cs = safe_int(clinic.get("site_score"))
    cb = has_booking(clinic)
    cfb = bool(clinic.get("facebook_url", "").strip())
    cig = bool(clinic.get("instagram_url", "").strip())

    comps = list(competitors[:3])
    while len(comps) < 3: comps.append({})

    # Header
    hdr = '    <div class="comp-row comp-header-row">\n'
    hdr += '      <div class="comp-cell cell-label"></div>\n'
    hdr += '      <div class="comp-cell cell-you">אתם</div>\n'
    for c in comps:
        hdr += f'      <div class="comp-cell cell-comp">{c.get("name","—")[:25]}</div>\n'
    hdr += '    </div>'

    rows = [hdr]
    # Numeric rows
    for label, you, key, extra in [
        ("ציון Google", cr, "rating", ""),
        ("ביקורות", cv, "review_count", " reviews-row"),
        ("ציון אתר", cs, "site_score", ""),
    ]:
        is_rating = key == "rating"
        vals = []
        for c in comps:
            v = safe_float(c.get(key)) if is_rating else safe_int(c.get(key))
            vals.append((v, _cls(you, v)))
        rows.append(_row(label, you, vals, extra))

    # Boolean rows
    for label, you_has, fn in [
        ("הזמנה אונליין", cb, lambda c: has_booking(c)),
        ("פייסבוק", cfb, lambda c: bool(c.get("facebook_url", "").strip())),
        ("אינסטגרם", cig, lambda c: bool(c.get("instagram_url", "").strip())),
    ]:
        vals = [(_chk(fn(c)), _boolcls(you_has, fn(c))) for c in comps]
        rows.append(_row(label, _chk(you_has), vals))

    # GBP photos (no data available)
    vals = [("—", "") for _ in comps]
    rows.append(_row("תמונות GBP", "—", vals))

    return "\n".join(rows)

# ── Replace comp-table in HTML ───────────────────────────────

def _replace_comp_table(html, new_inner):
    """Find the comp-table div in the body and replace its content."""
    start = html.find('</style>')
    if start < 0: start = 0
    marker_pos = html.find('class="comp-table', start)
    if marker_pos < 0: return html
    div_start = html.rfind('<div', start, marker_pos + 1)
    if div_start < 0: return html
    tag_end = html.index('>', div_start) + 1
    opening_tag = html[div_start:tag_end]

    depth, pos = 1, tag_end
    while pos < len(html) and depth > 0:
        nxt_open = html.find('<div', pos)
        nxt_close = html.find('</div>', pos)
        if nxt_close < 0: break
        if nxt_open >= 0 and nxt_open < nxt_close:
            depth += 1; pos = nxt_open + 4
        else:
            depth -= 1
            if depth == 0:
                return html[:div_start] + f'{opening_tag}\n{new_inner}\n  </div>' + html[nxt_close + 6:]
            pos = nxt_close + 6
    return html

# ── Personalization engine ───────────────────────────────────

def personalize_template(html, clinic, competitors):
    name = clinic.get("name", "")
    city = clinic.get("city", "").strip()
    rating = safe_float(clinic.get("rating"))
    reviews = safe_int(clinic.get("review_count"))
    site_score = safe_int(clinic.get("site_score"))
    c_booking, c_fb, c_ig = has_booking(clinic), bool(clinic.get("facebook_url","").strip()), bool(clinic.get("instagram_url","").strip())

    # 1) Title
    html = re.sub(r'(<title>).*?(</title>)', rf'\g<1>הצעה למרפאת שיניים — {name}\g<2>', html)
    # 2) Clinic name
    html = html.replace(SAMPLE_NAME, name)
    # 3) City
    for sc in SAMPLE_CITIES:
        html = html.replace(sc, city)
    # 4) Rating in bento (first occurrence of >5.0< only)
    html = html.replace('>5.0<', f'>{rating}<', 1)
    # 5) Reviews in bento — target specific CSS class containers
    for pat in [r'(class="big-num">)24(</)', r'(class="big-number">)24(</)',
                r'(class="big-number playfair">)24(</)', r'(class="rev-num neon-pink">)24(</)',
                r'(class="reviews-num">)24(</)', r'(class="review-count">)24(</)',
                r'(class="stat-value display">)24(</)',]:
        html = re.sub(pat, rf'\g<1>{reviews}\2', html, count=1)
    # 6) Site score
    html = html.replace('8/10', f'{site_score}/10')
    # Update SVG dashoffset (infer total from old 80% offset)
    html = re.sub(r'(style="stroke-dashoffset:\s*)([\d.]+)',
        lambda m: f'{m.group(1)}{round(float(m.group(2))/0.2*(1-site_score/10),1)}', html)
    html = re.sub(r'(stroke-dashoffset:\s*)(45\.2)',
        lambda m: f'{m.group(1)}{round(226*(1-site_score/10),1)}', html)
    # 7) Online presence booleans
    for label, has_it in [("ONLINE_BOOKING", c_booking), ("FACEBOOK", c_fb), ("INSTAGRAM", c_ig),
                          ("הזמנה אונליין", c_booking), ("פייסבוק", c_fb), ("אינסטגרם", c_ig)]:
        if not has_it:
            html = re.sub(rf'(&#10003;)(.*?{re.escape(label)})', r'&#10007;\2', html, count=1, flags=re.DOTALL)
            html = re.sub(rf'(&#10003;.*?{re.escape(label)}.*?)ACTIVE', r'\g<1>INACTIVE', html, count=1, flags=re.DOTALL)
    # 8) Comp table
    html = _replace_comp_table(html, build_comp_table(clinic, competitors))
    # 9) Warning box
    ranked = sorted(
        [(clinic.get("name"), reviews)] + [(c.get("name",""), safe_int(c.get("review_count"))) for c in competitors[:3]],
        key=lambda x: x[1], reverse=True)
    rank = next((i for i,(n,_) in enumerate(ranked,1) if n==clinic.get("name")), len(ranked))
    total = len(ranked)
    top_rev = ranked[0][1] if ranked else 0
    mult = round(top_rev / max(reviews, 1), 1)
    html = re.sub(r'מקום 4 מתוך 4', f'מקום {rank} מתוך {total}', html)
    html = re.sub(r'>4 מתוך 4<', f'>{rank} מתוך {total}<', html)
    html = re.sub(r'RANKING_POSITION = 4/4', f'RANKING_POSITION = {rank}/{total}', html)
    html = re.sub(r'756 ביקורות', f'{top_rev} ביקורות', html)
    html = re.sub(r'פי 31\.5', f'פי {mult}', html)
    # 10) Subtitle
    html = re.sub(r'(מול\s+)3(\s+מרפאות מובילות)', rf'\g<1>{len(competitors[:3])}\2', html)
    return html

# ── Main ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate personalized proposal reports")
    parser.add_argument("--segment", type=str, help="Only generate for this segment")
    parser.add_argument("--test", type=int, help="Limit to N clinics per segment")
    parser.add_argument("--template", type=str, help="Override template for all clinics")
    args = parser.parse_args()

    all_clinics = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    city_index = build_city_index(all_clinics)
    tpl_cache = {}

    def get_tpl(name):
        if name not in tpl_cache:
            with open(os.path.join(TEMPLATES_DIR, name), encoding="utf-8") as f:
                tpl_cache[name] = f.read()
        return tpl_cache[name]

    segments = [args.segment] if args.segment else list(SEGMENT_TEMPLATES.keys())
    counts = {}

    for seg in segments:
        templates = SEGMENT_TEMPLATES.get(seg, [])
        if not templates and not args.template: continue
        tpl_name = args.template or templates[0]

        seg_clinics = [c for c in all_clinics if c.get("segment") == seg and not is_chain(c) and not is_non_dental(c)]
        if args.test: seg_clinics = seg_clinics[:args.test]
        if not seg_clinics: continue

        out_dir = os.path.join(OUTPUT_DIR, seg)
        os.makedirs(out_dir, exist_ok=True)

        for idx, clinic in enumerate(seg_clinics, 1):
            city = clinic.get("city", "").strip()
            comps = find_top_competitors(clinic.get("name"), city, city_index, n=3)
            try: tpl_html = get_tpl(tpl_name)
            except FileNotFoundError:
                print(f"  WARN: {tpl_name} not found, skipping {clinic.get('name')}"); continue
            html = personalize_template(tpl_html, clinic, comps)
            fname = sanitize_filename(clinic.get("name", "clinic"), idx)
            with open(os.path.join(out_dir, f"{fname}.html"), "w", encoding="utf-8") as f:
                f.write(html)
        counts[seg] = len(seg_clinics)

    print("Proposals generated:")
    total = 0
    for seg, n in sorted(counts.items()):
        print(f"  Segment {seg}: {n} → {OUTPUT_DIR}/{seg}/")
        total += n
    print(f"  Total: {total}")

if __name__ == "__main__":
    main()
