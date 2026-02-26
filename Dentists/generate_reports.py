#!/usr/bin/env python3
"""Generate personalized HTML outreach reports for dental clinics (S1, S2, S3)."""

import csv
import os
import sys
import re
from statistics import median

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FULL_CSV = os.path.join(SCRIPT_DIR, "gush-dan-dental-clinics.csv")
LEADS_CSV = os.path.join(SCRIPT_DIR, "outreach-leads.csv")
REPORTS_DIR = os.path.join(SCRIPT_DIR, "reports")

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


def safe_float(val, default=0.0):
    try:
        return float(val) if val else default
    except (ValueError, TypeError):
        return default


def safe_int(val, default=0):
    try:
        return int(float(val)) if val else default
    except (ValueError, TypeError):
        return default


def is_chain(row):
    name = row.get("name", "").lower()
    return any(kw in name for kw in CHAIN_KEYWORDS)


def is_non_dental(row):
    combined = (row.get("name", "") + " " + row.get("categories", "")).lower()
    return any(kw in combined for kw in NON_DENTAL_KEYWORDS)


def has_booking(row):
    return "booking" in row.get("comments", "").lower()


def load_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_city_index(all_clinics):
    """Group clinics by city, sorted by review_count desc, excluding chains."""
    index = {}
    for c in all_clinics:
        if is_chain(c) or is_non_dental(c):
            continue
        city = c.get("city", "").strip()
        if not city:
            continue
        index.setdefault(city, []).append(c)
    for city in index:
        index[city].sort(key=lambda r: safe_int(r.get("review_count")), reverse=True)
    return index


def get_city_stats(city_clinics):
    reviews = [safe_int(c.get("review_count")) for c in city_clinics]
    ratings = [safe_float(c.get("rating")) for c in city_clinics if safe_float(c.get("rating")) > 0]
    docs = [(safe_int(c.get("review_count")), safe_int(c.get("doctor_count")))
            for c in city_clinics if safe_int(c.get("doctor_count")) > 0]
    return {
        "count": len(city_clinics),
        "avg_reviews": round(sum(reviews) / max(len(reviews), 1), 1),
        "median_reviews": round(median(reviews), 0) if reviews else 0,
        "avg_rating": round(sum(ratings) / max(len(ratings), 1), 2) if ratings else 0,
        "avg_reviews_per_doc": round(
            sum(r for r, d in docs) / max(sum(d for r, d in docs), 1), 1
        ) if docs else 0,
    }


def find_top_competitors(target_name, city, city_index, n=3):
    pool = city_index.get(city, [])
    return [c for c in pool if c.get("name") != target_name][:n]


def find_high_rated(city, city_index, target_name, min_rating=4.5, n=3):
    pool = city_index.get(city, [])
    return [c for c in pool
            if safe_float(c.get("rating")) >= min_rating and c.get("name") != target_name][:n]


def calculate_new_rating(current_rating, current_reviews, new_5star):
    total = current_rating * current_reviews + 5.0 * new_5star
    return round(total / (current_reviews + new_5star), 2)


def sanitize_filename(name, idx):
    clean = re.sub(r'[^\w\s\u0590-\u05FF-]', '', name)
    clean = clean.strip().replace(' ', '-')[:40]
    return f"{idx:03d}-{clean}"


# ── Shared HTML ──────────────────────────────────────────────

BASE_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; direction: rtl;
       background: #f5f5f5; color: #333; line-height: 1.6; }
.page { max-width: 680px; margin: 20px auto; background: #fff;
        border-radius: 12px; overflow: hidden; box-shadow: 0 2px 20px rgba(0,0,0,.08); }
.header { padding: 28px 32px; color: #fff; }
.header h1 { font-size: 22px; margin-bottom: 4px; }
.header p { opacity: .85; font-size: 14px; }
.body { padding: 28px 32px; }
.dashboard { display: flex; gap: 16px; margin: 20px 0; }
.stat-card { flex: 1; background: #f8f9fa; border-radius: 10px; padding: 16px;
             text-align: center; border: 1px solid #e9ecef; }
.stat-card .number { font-size: 32px; font-weight: 700; }
.stat-card .label { font-size: 12px; color: #666; margin-top: 4px; }
.gap-box { background: #fff3cd; border-right: 4px solid #f0ad4e;
           padding: 16px 20px; border-radius: 8px; margin: 20px 0; }
.danger-box { background: #f8d7da; border-right: 4px solid #dc3545;
              padding: 16px 20px; border-radius: 8px; margin: 20px 0; }
.success-box { background: #d4edda; border-right: 4px solid #28a745;
               padding: 16px 20px; border-radius: 8px; margin: 20px 0; }
.comp-table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
.comp-table th { background: #1a1a2e; color: #fff; padding: 10px 12px; text-align: center; }
.comp-table td { padding: 10px 12px; text-align: center; border-bottom: 1px solid #eee; }
.comp-table .you { background: #e8f4fd; font-weight: 600; }
.comp-table .lose { background: #ffeaea; color: #dc3545; font-weight: 600; }
.comp-table .win { background: #eafbea; color: #28a745; font-weight: 600; }
.section-title { font-size: 18px; font-weight: 700; margin: 24px 0 12px; color: #1a1a2e; }
.cta { background: #1a1a2e; color: #fff; padding: 24px 32px; margin-top: 24px;
       border-radius: 8px; text-align: center; }
.cta h3 { margin-bottom: 8px; font-size: 18px; }
.cta p { font-size: 14px; opacity: .9; }
.footer { padding: 16px 32px; font-size: 11px; color: #999; text-align: center;
          border-top: 1px solid #eee; }
.rating-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
.rating-table td, .rating-table th { padding: 10px 14px; text-align: center; }
.rating-table tr:nth-child(even) { background: #f8f9fa; }
.rating-table .highlight { background: #d4edda; font-weight: 700; font-size: 16px; }
.bold { font-weight: 700; }
.red { color: #dc3545; }
.green { color: #28a745; }
.amber { color: #e67e22; }
h2.section-title { border-bottom: 2px solid #eee; padding-bottom: 8px; }
@media print { .page { box-shadow: none; margin: 0; } .cta { break-inside: avoid; } }
"""


def html_wrap(title, header_bg, header_html, body_html):
    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{BASE_CSS}</style></head>
<body><div class="page">
<div class="header" style="background:{header_bg}">{header_html}</div>
<div class="body">{body_html}</div>
<div class="footer">מבוסס על נתונים ציבוריים מ-Google, easy.co.il ואתרי המרפאות | פברואר 2026</div>
</div></body></html>"""


# ── S2: Patient Voice Report ──────────────────────────────────

def generate_s2(clinic, city_stats):
    name = clinic["name"]
    rating = safe_float(clinic.get("rating"))
    reviews = safe_int(clinic.get("review_count"))
    easy = clinic.get("easy_score", "")
    docs = safe_int(clinic.get("doctor_count"))
    city = clinic.get("city", "")
    avg_rev = city_stats["avg_reviews"]

    header = f"<h1>דוח קול המטופל</h1><p>{name} | {city}</p>"

    # Dashboard
    cards = f"""<div class="dashboard">
    <div class="stat-card"><div class="number {'green' if rating >= 4.5 else 'amber'}">{rating}</div>
    <div class="label">ציון Google</div></div>
    <div class="stat-card"><div class="number {'red' if reviews < 10 else 'amber'}">{reviews}</div>
    <div class="label">ביקורות</div></div>"""
    if easy:
        cards += f"""<div class="stat-card"><div class="number green">{easy}</div>
        <div class="label">ציון easy.co.il</div></div>"""
    cards += "</div>"

    # Gap analysis
    gap = f"""<div class="gap-box">
    <strong>📊 הפער:</strong> מרפאות ב{city} מחזיקות בממוצע <strong>{avg_rev}</strong> ביקורות.
    למרפאה שלך יש <strong>{reviews}</strong>.
    {'זה פחות מרבע מהממוצע.' if reviews < avg_rev * 0.25 else 'זה מתחת לממוצע.' if reviews < avg_rev else 'אתם מעל הממוצע!'}
    </div>"""

    # Per-doctor math
    doc_section = ""
    if docs > 0:
        rpd = round(reviews / max(docs, 1), 1)
        doc_section = f"""<h2 class="section-title">ביקורות לרופא</h2>
        <div class="{'danger-box' if rpd < 3 else 'gap-box'}">
        <strong>{docs}</strong> רופאים × <strong>{reviews}</strong> ביקורות = <strong class="{'red' if rpd < 3 else 'amber'}">{rpd}</strong> ביקורות לרופא.
        <br>ממוצע עירוני: <strong>{city_stats['avg_reviews_per_doc']}</strong> ביקורות לרופא.
        {'<br><br>כל רופא צריך לייצר בממוצע 5-10 ביקורות כדי לבנות אמון אונליין.' if rpd < 5 else ''}
        </div>"""

    # What they're missing
    missing = """<h2 class="section-title">מה קורה כשאין מספיק ביקורות?</h2>
    <ul style="padding-right:20px; margin:12px 0;">
    <li>מטופל פוטנציאלי מחפש רופא שיניים בגוגל</li>
    <li>רואה את המרפאה שלך — ציון מעולה!</li>
    <li><strong>אבל רק """ + str(reviews) + """ ביקורות.</strong> המתחרה הבא? 80+ ביקורות.</li>
    <li>הוא בוחר במתחרה. לא בגלל שהוא טוב יותר — בגלל שיש לו יותר הוכחות.</li>
    </ul>"""

    cta = """<div class="cta">
    <h3>רוצה לראות את הדוח המלא עם כל הביקורות?</h3>
    <p>10 דקות בזום — נראה לך בדיוק מה המטופלים אומרים, מה אפשר לשפר, ואיך להגדיל ביקורות תוך 30 יום.</p>
    </div>"""

    body = cards + gap + doc_section + missing + cta
    return html_wrap(f"דוח קול המטופל — {name}", "#2c3e50", header, body)


# ── S1: Competitor Comparison Card ────────────────────────────

def generate_s1(clinic, competitors, city_stats):
    name = clinic["name"]
    city = clinic.get("city", "")
    rating = safe_float(clinic.get("rating"))
    reviews = safe_int(clinic.get("review_count"))
    site = safe_int(clinic.get("site_score"))
    booking = has_booking(clinic)

    header = f"<h1>כרטיס השוואה מול מתחרים</h1><p>{name} | {city}</p>"

    if not competitors:
        body = "<p>לא נמצאו מספיק מתחרים בעיר להשוואה.</p>"
        return html_wrap(f"השוואה — {name}", "#1a1a2e", header, body)

    intro = f"""<p style="margin:8px 0 20px; font-size:15px;">
    השווינו את המרפאה שלך מול <strong>{len(competitors)}</strong> מרפאות מובילות ב{city}
    (לפי מספר ביקורות).</p>"""

    # Build comparison table
    def cell(val_you, val_comp, higher_is_better=True):
        if higher_is_better:
            cls = "lose" if val_comp > val_you else "win" if val_you > val_comp else "you"
        else:
            cls = "win" if val_comp > val_you else "lose" if val_you > val_comp else "you"
        return cls

    rows = ""
    metrics = [
        ("ציון Google", "rating", True),
        ("ביקורות", "review_count", True),
        ("ציון אתר", "site_score", True),
    ]

    for label, key, higher_better in metrics:
        you_val = safe_float(clinic.get(key)) if key == "rating" else safe_int(clinic.get(key))
        rows += f'<tr><td class="bold">{label}</td><td class="you">{you_val}</td>'
        for comp in competitors:
            comp_val = safe_float(comp.get(key)) if key == "rating" else safe_int(comp.get(key))
            cls = cell(you_val, comp_val, higher_better)
            rows += f'<td class="{cls}">{comp_val}</td>'
        rows += "</tr>"

    # Boolean rows
    for label, check_fn in [("הזמנה אונליין", has_booking),
                             ("פייסבוק", lambda r: bool(r.get("facebook_url", "").strip())),
                             ("אינסטגרם", lambda r: bool(r.get("instagram_url", "").strip()))]:
        you_val = check_fn(clinic)
        rows += f'<tr><td class="bold">{label}</td><td class="you">{"✓" if you_val else "✗"}</td>'
        for comp in competitors:
            comp_val = check_fn(comp)
            cls = "lose" if comp_val and not you_val else "win" if you_val and not comp_val else ""
            rows += f'<td class="{cls}">{"✓" if comp_val else "✗"}</td>'
        rows += "</tr>"

    comp_headers = "".join(
        f'<th style="max-width:140px;font-size:12px">{c.get("name","")[:25]}</th>'
        for c in competitors
    )
    table = f"""<table class="comp-table">
    <tr><th></th><th style="background:#2c3e50">אתם</th>{comp_headers}</tr>
    {rows}</table>"""

    # Ranking insight
    all_in_city = [(c.get("name"), safe_int(c.get("review_count")))
                   for c in [clinic] + competitors]
    all_in_city.sort(key=lambda x: x[1], reverse=True)
    your_rank = next(i for i, (n, _) in enumerate(all_in_city, 1) if n == name)
    top_reviews = all_in_city[0][1]

    insight_cls = "danger-box" if your_rank > 1 else "success-box"
    insight = f"""<div class="{insight_cls}">
    <strong>{'⚠️' if your_rank > 1 else '✓'} מיקום שלך:</strong>
    מקום {your_rank} מתוך {len(all_in_city)} לפי ביקורות.
    {'המתחרה המוביל מחזיק ' + str(top_reviews) + ' ביקורות — פי ' + str(round(top_reviews / max(reviews, 1), 1)) + ' ממך.' if your_rank > 1 else 'מוביל!'}
    </div>"""

    cta = """<div class="cta">
    <h3>אני יכול לשלוח לך את כל הנתונים על המתחרים שלך</h3>
    <p>כולל ניתוח ביקורות, מילות חיפוש, ונוכחות דיגיטלית מלאה. 10 דקות בזום — רלוונטי?</p>
    </div>"""

    body = intro + table + insight + cta
    return html_wrap(f"השוואה — {name}", "#1a1a2e", header, body)


# ── S3: Reputation Risk Report ────────────────────────────────

def generate_s3(clinic, high_rated, city_stats):
    name = clinic["name"]
    city = clinic.get("city", "")
    rating = safe_float(clinic.get("rating"))
    reviews = safe_int(clinic.get("review_count"))

    header = f"<h1>דוח סיכון מוניטין</h1><p>{name} | {city}</p>"

    # Current state — big red rating
    state = f"""<div style="text-align:center; margin:20px 0;">
    <div style="font-size:72px; font-weight:800; color:#dc3545;">{rating}</div>
    <div style="font-size:16px; color:#666;">{reviews} ביקורות ב-Google</div>
    </div>
    <div class="danger-box">
    <strong>מה זה אומר:</strong> כשמטופל מחפש רופא שיניים ב{city} ורואה ציון {rating},
    הוא ממשיך לגלול. {'הציון הזה מבוסס על ' + str(reviews) + ' ביקורות בלבד — זה ניתן לשינוי.' if reviews < 15 else ''}
    </div>"""

    # Rating improvement calculator
    calc_rows = ""
    for n in [5, 10, 15, 20]:
        new_r = calculate_new_rating(rating, reviews, n)
        delta = round(new_r - rating, 2)
        cls = "highlight" if new_r >= 4.0 else ""
        star = " ⭐" if new_r >= 4.0 else ""
        calc_rows += f'<tr class="{cls}"><td>+{n}</td><td>{new_r}{star}</td><td class="green">+{delta}</td></tr>'

    calc_table = f"""<h2 class="section-title">מחשבון שיפור ציון</h2>
    <p style="margin-bottom:12px;">מה קורה אם מטופלים מרוצים מתחילים להשאיר ביקורות?</p>
    <table class="rating-table">
    <tr style="background:#1a1a2e; color:#fff;"><th>ביקורות חדשות (5⭐)</th><th>הציון החדש</th><th>שיפור</th></tr>
    <tr style="background:#f8d7da;"><td>היום</td><td class="red bold">{rating}</td><td>—</td></tr>
    {calc_rows}</table>"""

    # Target line
    if reviews > 0:
        needed = 0
        while calculate_new_rating(rating, reviews, needed) < 4.0 and needed < 100:
            needed += 1
        target = f"""<div class="success-box">
        <strong>🎯 היעד:</strong> עוד <strong>{needed}</strong> ביקורות של 5 כוכבים
        ואתם עוברים את ה-4.0 — הסף שמשנה הכל.
        </div>""" if needed <= 50 else ""
    else:
        target = """<div class="success-box">
        <strong>🎯 היעד:</strong> עוד אין לך ביקורות — 10 ביקורות ראשונות של 5 כוכבים
        יתנו לך ציון <strong>5.0</strong>. ההתחלה שלך מגדירה הכל.
        </div>"""

    # Competitor comparison
    comp_section = ""
    if high_rated:
        comp_section = f'<h2 class="section-title">הנה מה שנראה "טוב" ב{city}</h2>'
        comp_section += '<div class="dashboard">'
        for c in high_rated[:3]:
            cr = safe_float(c.get("rating"))
            crev = safe_int(c.get("review_count"))
            cname = c.get("name", "")[:30]
            comp_section += f"""<div class="stat-card" style="border:2px solid #28a745;">
            <div class="number green">{cr}</div>
            <div class="label">{crev} ביקורות</div>
            <div style="font-size:11px; margin-top:6px; color:#333;">{cname}</div>
            </div>"""
        comp_section += "</div>"

    # Urgency
    urgency = """<div class="danger-box" style="margin-top:20px;">
    <strong>⏰ כל יום שעובר:</strong> מטופלים חדשים מחפשים רופא שיניים, רואים את הציון,
    ובוחרים במתחרה. זה לא ישתנה מעצמו — אבל 10 ביקורות יכולות לשנות את התמונה.
    </div>"""

    cta = """<div class="cta">
    <h3>יש לנו תוכנית שהצליחה להעלות ציון מ-3.6 ל-4.3 תוך 60 יום</h3>
    <p>10 דקות בטלפון — נסביר בדיוק איך, עם תוצאות אמיתיות ממרפאות אחרות. רוצה לשמוע?</p>
    </div>"""

    body = state + calc_table + target + comp_section + urgency + cta
    return html_wrap(f"דוח סיכון — {name}", "#dc3545", header, body)


# ── Main ──────────────────────────────────────────────────────

def main():
    test_n = None
    seg_filter = None
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--test" and i < len(sys.argv):
            test_n = int(sys.argv[i + 1]) if i + 1 <= len(sys.argv) else 3
        if arg == "--segment" and i < len(sys.argv):
            seg_filter = sys.argv[i + 1] if i + 1 <= len(sys.argv) else None
        if sys.argv[i - 1] == "--test":
            try:
                test_n = int(arg)
            except ValueError:
                pass
        if sys.argv[i - 1] == "--segment":
            seg_filter = arg

    all_clinics = load_csv(FULL_CSV)
    leads = load_csv(LEADS_CSV)
    city_index = build_city_index(all_clinics)
    city_stats_cache = {city: get_city_stats(clinics) for city, clinics in city_index.items()}

    counts = {1: 0, 2: 0, 3: 0}
    generators = {
        2: ("s2", generate_s2_wrapper),
        1: ("s1", generate_s1_wrapper),
        3: ("s3", generate_s3_wrapper),
    }

    for seg_num in [2, 1, 3]:
        if seg_filter and str(seg_num) != seg_filter:
            continue
        folder, gen_fn = generators[seg_num]
        seg_leads = [l for l in leads if l.get("segment") == str(seg_num)]
        if test_n:
            seg_leads = seg_leads[:test_n]

        out_dir = os.path.join(REPORTS_DIR, folder)
        os.makedirs(out_dir, exist_ok=True)

        for idx, clinic in enumerate(seg_leads, 1):
            city = clinic.get("city", "").strip()
            stats = city_stats_cache.get(city, get_city_stats([]))
            html = gen_fn(clinic, city_index, stats)
            fname = sanitize_filename(clinic.get("name", "clinic"), idx)
            path = os.path.join(out_dir, f"{fname}.html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            counts[seg_num] += 1

    print("Reports generated:")
    for seg in [2, 1, 3]:
        if counts[seg]:
            print(f"  S{seg}: {counts[seg]} → {REPORTS_DIR}/{generators[seg][0]}/")
    print(f"  Total: {sum(counts.values())}")


def generate_s2_wrapper(clinic, city_index, city_stats):
    return generate_s2(clinic, city_stats)


def generate_s1_wrapper(clinic, city_index, city_stats):
    comps = find_top_competitors(clinic.get("name"), clinic.get("city", ""), city_index, n=3)
    return generate_s1(clinic, comps, city_stats)


def generate_s3_wrapper(clinic, city_index, city_stats):
    high = find_high_rated(clinic.get("city", ""), city_index, clinic.get("name"), n=3)
    return generate_s3(clinic, high, city_stats)


if __name__ == "__main__":
    main()
