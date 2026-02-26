#!/usr/bin/env python3
"""Generate personalized landing-page websites for S4 (Invisible Good Clinics)."""

import csv
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_CSV = os.path.join(SCRIPT_DIR, "outreach-leads.csv")
REPORTS_DIR = os.path.join(SCRIPT_DIR, "reports", "s4")

# ── Helpers ──────────────────────────────────────────────────


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


def sanitize_filename(name, idx):
    clean = re.sub(r'[^\w\s\u0590-\u05FF-]', '', name)
    clean = clean.strip().replace(' ', '-')[:40]
    return f"{idx:03d}-{clean}"


def load_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ── Color Themes (5 rotations) ──────────────────────────────

THEMES = [
    {  # Navy / Gold
        "primary": "#1a2e4a", "primary_dark": "#0f1c2e",
        "accent": "#c9a84c", "accent_soft": "rgba(201,168,76,0.12)",
        "hero_grad": "linear-gradient(135deg, #1a2e4a 0%, #2d4a6e 60%, #1a2e4a 100%)",
        "cta_bg": "#c9a84c", "cta_text": "#1a2e4a",
    },
    {  # Teal / White
        "primary": "#1a7a6e", "primary_dark": "#115a50",
        "accent": "#2ba899", "accent_soft": "rgba(43,168,153,0.12)",
        "hero_grad": "linear-gradient(135deg, #1a7a6e 0%, #2ba899 50%, #1a7a6e 100%)",
        "cta_bg": "#fff", "cta_text": "#1a7a6e",
    },
    {  # Slate Blue / Sky
        "primary": "#2c3e6b", "primary_dark": "#1a2547",
        "accent": "#5b8def", "accent_soft": "rgba(91,141,239,0.12)",
        "hero_grad": "linear-gradient(135deg, #2c3e6b 0%, #3d5a9e 60%, #2c3e6b 100%)",
        "cta_bg": "#5b8def", "cta_text": "#fff",
    },
    {  # Charcoal / Coral
        "primary": "#2d2d2d", "primary_dark": "#1a1a1a",
        "accent": "#e07055", "accent_soft": "rgba(224,112,85,0.12)",
        "hero_grad": "linear-gradient(135deg, #2d2d2d 0%, #444 60%, #2d2d2d 100%)",
        "cta_bg": "#e07055", "cta_text": "#fff",
    },
    {  # Forest / Mint
        "primary": "#2e5d4b", "primary_dark": "#1c3d31",
        "accent": "#4caf82", "accent_soft": "rgba(76,175,130,0.12)",
        "hero_grad": "linear-gradient(135deg, #2e5d4b 0%, #3d7a62 60%, #2e5d4b 100%)",
        "cta_bg": "#4caf82", "cta_text": "#fff",
    },
]

# ── SVG Icons (inline, minimal) ──────────────────────────────

SVG_TOOTH = '''<svg viewBox="0 0 64 64" width="40" height="40" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M32 6C22 6 14 13 14 22c0 8 2 14 6 22 2 6 6 14 10 14 1.5 0 2.5-3 3.5-7
  .5 2 1.5 4 2.5 7 4 0 8-6 10-14 4-8 6-14 6-22C52 13 44 6 32 6Z"
  fill="ACCENT" opacity=".15" stroke="ACCENT" stroke-width="2.5" stroke-linejoin="round"/></svg>'''

SVG_IMPLANT = '''<svg viewBox="0 0 64 64" width="40" height="40" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="24" y="6" width="16" height="14" rx="4" fill="ACCENT" opacity=".15" stroke="ACCENT" stroke-width="2.5"/>
<path d="M26 24h12l-1 10h-10l-1-10Zm1 14h10l-1 10h-8l-1-10Zm1 14h8l-1 6h-6l-1-6Z"
  stroke="ACCENT" stroke-width="2.5" stroke-linejoin="round" fill="ACCENT" opacity=".1"/></svg>'''

SVG_SMILE = '''<svg viewBox="0 0 64 64" width="40" height="40" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="26" fill="ACCENT" opacity=".12" stroke="ACCENT" stroke-width="2.5"/>
<circle cx="23" cy="27" r="3" fill="ACCENT"/><circle cx="41" cy="27" r="3" fill="ACCENT"/>
<path d="M22 38c3 6 8 9 10 9s7-3 10-9" stroke="ACCENT" stroke-width="2.5" stroke-linecap="round"/></svg>'''

SVG_SHIELD = '''<svg viewBox="0 0 64 64" width="40" height="40" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M32 4L10 16v16c0 14 10 24 22 28 12-4 22-14 22-28V16L32 4Z"
  fill="ACCENT" opacity=".12" stroke="ACCENT" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M24 32l6 6 12-14" stroke="ACCENT" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

SVG_CHILD = '''<svg viewBox="0 0 64 64" width="40" height="40" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="22" r="14" fill="ACCENT" opacity=".12" stroke="ACCENT" stroke-width="2.5"/>
<circle cx="27" cy="20" r="2" fill="ACCENT"/><circle cx="37" cy="20" r="2" fill="ACCENT"/>
<path d="M28 27c1.5 2 3 3 4 3s2.5-1 4-3" stroke="ACCENT" stroke-width="2" stroke-linecap="round"/>
<path d="M22 38v10a6 6 0 006 6h8a6 6 0 006-6V38" stroke="ACCENT" stroke-width="2.5"/></svg>'''

SVG_BRACES = '''<svg viewBox="0 0 64 64" width="40" height="40" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="22" width="48" height="20" rx="10" fill="ACCENT" opacity=".12" stroke="ACCENT" stroke-width="2.5"/>
<line x1="20" y1="26" x2="20" y2="38" stroke="ACCENT" stroke-width="2"/>
<line x1="32" y1="26" x2="32" y2="38" stroke="ACCENT" stroke-width="2"/>
<line x1="44" y1="26" x2="44" y2="38" stroke="ACCENT" stroke-width="2"/>
<line x1="14" y1="32" x2="50" y2="32" stroke="ACCENT" stroke-width="2.5"/></svg>'''

SVGS = [SVG_TOOTH, SVG_IMPLANT, SVG_SMILE, SVG_SHIELD, SVG_CHILD, SVG_BRACES]

SERVICES = [
    ("טיפולי שיניים כלליים", "בדיקות תקופתיות, סתימות וטיפולים מונעים"),
    ("השתלות שיניים", "פתרון קבע לשיניים חסרות בטכנולוגיה מתקדמת"),
    ("הלבנת שיניים", "חיוך בהיר ולבן בטיפול מהיר ובטוח"),
    ("שיקום הפה", "כתרים, גשרים ותותבות לשיקום מלא"),
    ("רפואת שיניים לילדים", "סביבה נעימה וטיפול עדין לכל הגילאים"),
    ("אורתודונטיה", "יישור שיניים, ברייסס ואינויזליין"),
]

TRUST_POINTS = [
    ("טיפול אישי ומותאם", "כל מטופל מקבל תשומת לב מלאה ותוכנית טיפול ייחודית"),
    ("ציוד וטכנולוגיה מתקדמים", "המרפאה מצוידת בטכנולוגיה חדישה לטיפול מדויק ונוח"),
    ("ניסיון מקצועי", "רופאים מומחים עם שנות ניסיון בטיפולי שיניים מגוונים"),
    ("אווירה מרגיעה", "סביבה נעימה שנועדה להפוך את חוויית הטיפול לנוחה ורגועה"),
]


# ── Name Extraction ──────────────────────────────────────────

def extract_doctor_name(raw):
    name = raw.replace('""', '"').replace('\u05F4', '"')
    patterns = [
        r'["\u05D3][\"\u05F4\']?\u05E8\s+([^\-,(\n]+)',
        r'\u05D3\u05E8[\'\u05F3]?\s+([^\-,(\n]+)',
        r'Dr\.?\s+([A-Za-z][^\-,(\n]+)',
    ]
    stop_words = ['מרפאת', 'רופא', 'מומחה', 'מומחית', 'כירורג', 'מרכז',
                  'השתלות', 'שיניים', 'בתל', 'בבת', 'בבני', 'בפתח',
                  'בחולון', 'ברמת', 'בגבעתיים', 'בהרצליה', 'בקרית']
    for pat in patterns:
        m = re.search(pat, name)
        if m:
            candidate = m.group(1).strip()
            for sw in stop_words:
                if sw in candidate:
                    candidate = candidate[:candidate.index(sw)].strip()
            words = candidate.split()[:3]
            result = ' '.join(words).strip(' -,')
            if len(result) > 2:
                return result
    return None


def clean_display_name(raw, city=""):
    name = raw.replace('""', '"').replace('\u05F4', '"')
    original = name
    for prefix in ['מרפאת שיניים, ', 'מרפאת שיניים- ', 'מרפאת שיניים ',
                    'רופא שיניים ב', 'רופאת שיניים ב']:
        if name.startswith(prefix):
            name = name[len(prefix):]
    # If stripping left us with just the city name or too short, keep original
    stripped = name.strip()
    if stripped == city or len(stripped) < 4:
        return original.strip()
    if ' - ' in name and len(name) > 35:
        name = name.split(' - ')[0]
    return name.strip()


def get_initials(doctor_name, display_name):
    src = doctor_name or display_name
    if not src:
        return "D"
    first = src.strip()[0]
    if first.isalpha() or '\u0590' <= first <= '\u05FF':
        return first
    return "D"


# ── CSS Builder ──────────────────────────────────────────────

def build_css(t):
    return f"""
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Segoe UI',Arial,'Helvetica Neue',sans-serif;direction:rtl;
  color:#1a1a1a;line-height:1.6;background:#f8f9fb}}

/* NAV */
nav{{background:{t['primary']};padding:0 40px;height:64px;display:flex;align-items:center;
  justify-content:space-between;position:sticky;top:0;z-index:100;
  box-shadow:0 2px 12px rgba(0,0,0,.15)}}
.nav-logo{{color:#fff;font-size:18px;font-weight:700;letter-spacing:-.3px;
  display:flex;align-items:center;gap:10px}}
.nav-logo svg{{opacity:.85}}
.nav-cta{{background:{t['cta_bg']};color:{t['cta_text']};border:none;padding:10px 22px;
  border-radius:100px;font-size:14px;font-weight:600;cursor:pointer;
  text-decoration:none;transition:opacity .2s}}
.nav-cta:hover{{opacity:.85}}

/* HERO */
.hero{{background:{t['hero_grad']};min-height:520px;display:flex;align-items:center;
  padding:60px 40px;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;left:-120px;top:-80px;width:500px;height:500px;
  border-radius:50%;background:rgba(255,255,255,.04)}}
.hero::after{{content:'';position:absolute;right:-60px;bottom:-100px;width:350px;height:350px;
  border-radius:50%;background:rgba(255,255,255,.03)}}
.hero-content{{position:relative;max-width:600px}}
.hero-badge{{display:inline-flex;align-items:center;gap:8px;
  background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);color:#fff;
  padding:6px 16px;border-radius:100px;font-size:13px;margin-bottom:24px;
  backdrop-filter:blur(4px)}}
.hero-badge .dot{{width:7px;height:7px;border-radius:50%;background:#4ade80}}
.hero h1{{font-size:clamp(28px,5vw,44px);font-weight:800;color:#fff;line-height:1.15;
  margin-bottom:16px;letter-spacing:-.5px}}
.hero h1 em{{font-style:normal;color:{t['accent']}}}
.hero .sub{{font-size:17px;color:rgba(255,255,255,.8);margin-bottom:32px;max-width:460px}}
.hero-cta{{display:inline-flex;align-items:center;gap:10px;background:#fff;
  color:{t['primary']};padding:14px 28px;border-radius:100px;font-size:16px;
  font-weight:700;text-decoration:none;box-shadow:0 4px 20px rgba(0,0,0,.2);
  transition:transform .2s,box-shadow .2s}}
.hero-cta:hover{{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,.25)}}

/* HERO RATING */
.hero-rating{{display:inline-flex;align-items:center;gap:14px;
  background:rgba(255,255,255,.1);border:1.5px solid {t['accent']};
  border-radius:16px;padding:14px 22px;margin-top:28px}}
.hero-rating .score{{font-size:38px;font-weight:800;color:#fff;line-height:1}}
.stars{{color:#fbbf24;font-size:18px;letter-spacing:2px}}
.hero-rating .rev-label{{color:rgba(255,255,255,.7);font-size:13px}}

/* SECTIONS */
.section{{padding:64px 40px;max-width:1100px;margin:0 auto}}
.section-white{{background:#fff}}.section-gray{{background:#f4f6f8}}
.stw{{text-align:center;margin-bottom:40px}}
.tag{{display:inline-block;background:{t['accent_soft']};color:{t['primary']};
  padding:4px 14px;border-radius:100px;font-size:12px;font-weight:600;
  letter-spacing:1px;margin-bottom:12px}}
.section h2{{font-size:clamp(22px,4vw,32px);font-weight:800;color:#1a1a2e;line-height:1.3}}
.section h2 em{{font-style:normal;color:{t['primary']}}}

/* SERVICES GRID */
.sg{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;max-width:900px;margin:0 auto}}
.sc{{background:#fff;border:1px solid #e8eaed;border-radius:16px;padding:28px 22px;
  text-align:center;transition:transform .2s,box-shadow .2s,border-color .2s}}
.sc:hover{{transform:translateY(-4px);box-shadow:0 12px 32px rgba(0,0,0,.08);
  border-color:{t['accent']}}}
.sc h3{{font-size:15px;font-weight:700;color:#1a1a2e;margin:14px 0 6px}}
.sc p{{font-size:13px;color:#666;line-height:1.5}}

/* ABOUT */
.about-grid{{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;
  max-width:900px;margin:0 auto}}
.doc-card{{background:{t['accent_soft']};border:1px solid {t['primary']}20;border-radius:20px;
  padding:36px;text-align:center}}
.doc-avatar{{width:100px;height:100px;border-radius:50%;background:{t['hero_grad']};
  display:flex;align-items:center;justify-content:center;font-size:42px;color:#fff;
  font-weight:800;margin:0 auto 16px;box-shadow:0 4px 20px rgba(0,0,0,.15)}}
.doc-card .name{{font-size:22px;font-weight:800;color:#1a1a2e}}
.doc-card .title{{font-size:14px;color:#666;margin-top:4px}}
.trust-list{{list-style:none;display:flex;flex-direction:column;gap:18px}}
.trust-item{{display:flex;align-items:flex-start;gap:14px}}
.trust-check{{flex-shrink:0;width:28px;height:28px;border-radius:50%;
  background:{t['primary']};color:#fff;display:flex;align-items:center;
  justify-content:center;font-size:13px;font-weight:700}}
.trust-text h4{{font-size:15px;font-weight:700;color:#1a1a2e}}
.trust-text p{{font-size:13px;color:#666;margin-top:2px}}

/* RATING SECTION */
.rating-sec{{background:{t['hero_grad']};padding:64px 40px;text-align:center;color:#fff}}
.big-score{{font-size:80px;font-weight:900;line-height:1;color:#fff}}
.rating-src{{font-size:14px;opacity:.7;margin-top:8px}}
.rating-cta{{display:inline-block;margin-top:28px;background:#fff;color:{t['primary']};
  padding:14px 32px;border-radius:100px;font-size:16px;font-weight:700;
  text-decoration:none;box-shadow:0 4px 20px rgba(0,0,0,.2);
  transition:transform .2s}}
.rating-cta:hover{{transform:translateY(-2px)}}

/* CONTACT */
.cg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:20px;margin-top:32px;max-width:900px;margin-left:auto;margin-right:auto}}
.cc{{background:#fff;border:1px solid #e8eaed;border-radius:16px;padding:24px;
  display:flex;align-items:center;gap:16px;text-decoration:none;color:inherit;
  transition:box-shadow .2s,border-color .2s}}
.cc:hover{{box-shadow:0 8px 24px rgba(0,0,0,.08);border-color:{t['accent']}}}
.ci{{width:48px;height:48px;border-radius:12px;background:{t['accent_soft']};
  display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.cc .label{{font-size:12px;color:#999;font-weight:500}}
.cc .value{{font-size:16px;font-weight:700;color:#1a1a2e}}

/* FOOTER */
footer{{background:{t['primary_dark']};color:rgba(255,255,255,.6);text-align:center;
  padding:24px 40px;font-size:13px}}
footer strong{{color:rgba(255,255,255,.9)}}

/* MOBILE */
@media(max-width:768px){{
  nav{{padding:0 20px}}
  .hero{{padding:40px 20px;min-height:auto}}
  .section{{padding:48px 20px}}
  .sg{{grid-template-columns:1fr 1fr}}
  .about-grid{{grid-template-columns:1fr;gap:32px}}
  .big-score{{font-size:64px}}
}}
@media(max-width:420px){{
  .sg{{grid-template-columns:1fr}}
  .hero h1{{font-size:28px}}
}}
@media print{{
  nav{{position:static;box-shadow:none}}
  .hero{{min-height:auto;padding:40px 32px}}
  .sc:hover{{transform:none;box-shadow:none}}
}}
"""


# ── Inline SVG helpers ───────────────────────────────────────

SVG_PHONE_ICON = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>'''

SVG_MAP_ICON = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="ACCENT" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>'''

SVG_GOOGLE_ICON = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="ACCENT"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" opacity=".7"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" opacity=".5"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18A10.96 10.96 0 001 12c0 1.77.42 3.45 1.18 4.93l3.66-2.84z" opacity=".6"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" opacity=".8"/></svg>'''

SVG_NAV_TOOTH = '''<svg width="24" height="24" viewBox="0 0 64 64" fill="none"><path d="M32 6C22 6 14 13 14 22c0 8 2 14 6 22 2 6 6 14 10 14 1.5 0 2.5-3 3.5-7 .5 2 1.5 4 2.5 7 4 0 8-6 10-14 4-8 6-14 6-22C52 13 44 6 32 6Z" fill="rgba(255,255,255,.9)" stroke="rgba(255,255,255,.5)" stroke-width="2"/></svg>'''


# ── HTML Builders ────────────────────────────────────────────

def build_nav(display_name, phone, t):
    cta = ""
    if phone:
        cta = f'<a class="nav-cta" href="tel:{phone}">{SVG_PHONE_ICON} {phone}</a>'
    else:
        cta = f'<span class="nav-cta" style="opacity:.5">רפואת שיניים</span>'
    return f'''<nav>
  <span class="nav-logo">{SVG_NAV_TOOTH} {display_name}</span>
  {cta}
</nav>'''


def build_hero(display_name, doctor_name, city, phone, rating, reviews, t):
    # Headline varies based on whether we have a doctor name
    if doctor_name:
        h1 = f'ד"ר {doctor_name}<br><em>חיוך שמתחיל בידיים טובות</em>'
    else:
        h1 = f'טיפול שיניים<br><em>מקצועי ואישי</em>'

    subtitle = f'מרפאת שיניים ב{city} — טיפול מקצועי, אישי ועדין לכל המשפחה.'

    cta_href = f"tel:{phone}" if phone else "#contact"
    cta_text = "קבעו תור עכשיו" if phone else "צרו קשר"
    cta_arrow = "&#8592;" if phone else "&#8595;"

    rev_line = ""
    if reviews > 0:
        rev_line = f'<div class="rev-label">{reviews} ביקורות מטופלים</div>'

    rating_str = f"{rating:.1f}" if rating == int(rating) else str(rating)

    return f'''<section class="hero">
  <div class="hero-content">
    <div class="hero-badge"><span class="dot"></span> מרפאה פעילה | {city}</div>
    <h1>{h1}</h1>
    <p class="sub">{subtitle}</p>
    <a class="hero-cta" href="{cta_href}">{cta_text} {cta_arrow}</a>
    <div class="hero-rating">
      <div>
        <div class="score">{rating_str}</div>
        <div class="stars">\u2605\u2605\u2605\u2605\u2605</div>
      </div>
      <div>
        <div style="color:#fff;font-weight:700;font-size:15px">Google \u05D3\u05D9\u05E8\u05D5\u05D2</div>
        {rev_line}
      </div>
    </div>
  </div>
</section>'''


def build_services(t):
    cards = ""
    for i, (title, desc) in enumerate(SERVICES):
        svg = SVGS[i].replace("ACCENT", t["accent"])
        cards += f'''<div class="sc">
      <div class="si">{svg}</div>
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>'''
    return f'''<div class="section-white">
  <div class="section" style="padding-top:64px;padding-bottom:64px">
    <div class="stw">
      <div class="tag">\u05D4\u05E9\u05D9\u05E8\u05D5\u05EA\u05D9\u05DD \u05E9\u05DC\u05E0\u05D5</div>
      <h2>\u05D8\u05D9\u05E4\u05D5\u05DC\u05D9\u05DD <em>\u05DE\u05E7\u05E6\u05D5\u05E2\u05D9\u05D9\u05DD</em><br>\u05DC\u05DB\u05DC \u05D4\u05E6\u05E8\u05DB\u05D9\u05DD \u05E9\u05DC\u05DA</h2>
    </div>
    <div class="sg">{cards}</div>
  </div>
</div>'''


def build_about(doctor_name, display_name, city, t):
    initials = get_initials(doctor_name, display_name)

    if doctor_name:
        card = f'''<div class="doc-card">
      <div class="doc-avatar">{initials}</div>
      <div class="name">\u05D3"\u05E8 {doctor_name}</div>
      <div class="title">\u05E8\u05D5\u05E4\u05D0/\u05EA \u05E9\u05D9\u05E0\u05D9\u05D9\u05DD | {city}</div>
    </div>'''
    else:
        card = f'''<div class="doc-card">
      <div class="doc-avatar">{initials}</div>
      <div class="name">{display_name}</div>
      <div class="title">\u05DE\u05E8\u05E4\u05D0\u05EA \u05E9\u05D9\u05E0\u05D9\u05D9\u05DD | {city}</div>
    </div>'''

    trust = ""
    for title, desc in TRUST_POINTS:
        trust += f'''<li class="trust-item">
        <div class="trust-check">\u2713</div>
        <div class="trust-text"><h4>{title}</h4><p>{desc}</p></div>
      </li>'''

    return f'''<div class="section-gray">
  <div class="section" style="padding-top:64px;padding-bottom:64px">
    <div class="stw">
      <div class="tag">\u05D0\u05D5\u05D3\u05D5\u05EA</div>
      <h2>\u05DC\u05DE\u05D4 <em>\u05DC\u05D1\u05D7\u05D5\u05E8</em> \u05D1\u05E0\u05D5</h2>
    </div>
    <div class="about-grid">
      {card}
      <ul class="trust-list">{trust}</ul>
    </div>
  </div>
</div>'''


def build_rating(rating, reviews, maps_url, t):
    rating_str = f"{rating:.1f}" if rating == int(rating) else str(rating)
    rev_text = f'<div style="font-size:18px;color:rgba(255,255,255,.9);margin-top:12px">{reviews} \u05D1\u05D9\u05E7\u05D5\u05E8\u05D5\u05EA \u05DE\u05D8\u05D5\u05E4\u05DC\u05D9\u05DD \u05D1-Google</div>' if reviews else ''
    maps_btn = f'<a class="rating-cta" href="{maps_url}" target="_blank">\u05E8\u05D0\u05D5 \u05D0\u05D5\u05EA\u05E0\u05D5 \u05D1\u05D2\u05D5\u05D2\u05DC</a>' if maps_url else ''

    return f'''<section class="rating-sec">
  <div class="big-score">{rating_str}</div>
  <div class="stars" style="font-size:28px">\u2605\u2605\u2605\u2605\u2605</div>
  {rev_text}
  <div class="rating-src">\u05D3\u05D9\u05E8\u05D5\u05D2 Google Maps</div>
  {maps_btn}
</section>'''


def build_contact(phone, city, maps_url, t):
    cards = ""

    if phone:
        cards += f'''<a class="cc" href="tel:{phone}">
      <div class="ci">{SVG_PHONE_ICON.replace('white', t['accent'])}</div>
      <div><div class="label">\u05D8\u05DC\u05E4\u05D5\u05DF</div><div class="value" style="direction:ltr">{phone}</div></div>
    </a>'''

    map_svg = SVG_MAP_ICON.replace("ACCENT", t["accent"])
    if maps_url:
        cards += f'''<a class="cc" href="{maps_url}" target="_blank">
      <div class="ci">{map_svg}</div>
      <div><div class="label">\u05DE\u05D9\u05E7\u05D5\u05DD</div><div class="value">{city}</div></div>
    </a>'''
    elif city:
        cards += f'''<div class="cc">
      <div class="ci">{map_svg}</div>
      <div><div class="label">\u05DE\u05D9\u05E7\u05D5\u05DD</div><div class="value">{city}</div></div>
    </div>'''

    google_svg = SVG_GOOGLE_ICON.replace("ACCENT", t["accent"])
    if maps_url:
        cards += f'''<a class="cc" href="{maps_url}" target="_blank">
      <div class="ci">{google_svg}</div>
      <div><div class="label">Google Maps</div><div class="value">\u05E6\u05E4\u05D5 \u05D1\u05E4\u05E8\u05D5\u05E4\u05D9\u05DC \u05E9\u05DC\u05E0\u05D5</div></div>
    </a>'''

    return f'''<div class="section-white">
  <div class="section" id="contact" style="padding-top:64px;padding-bottom:64px">
    <div class="stw">
      <div class="tag">\u05E6\u05E8\u05D5 \u05E7\u05E9\u05E8</div>
      <h2>\u05E7\u05D1\u05E2\u05D5 <em>\u05EA\u05D5\u05E8</em> \u05E2\u05D5\u05D3 \u05D4\u05D9\u05D5\u05DD</h2>
    </div>
    <div class="cg">{cards}</div>
  </div>
</div>'''


def build_footer(display_name, city, t):
    return f'''<footer>
  <strong>{display_name}</strong> | {city} | \u05DB\u05DC \u05D4\u05D6\u05DB\u05D5\u05D9\u05D5\u05EA \u05E9\u05DE\u05D5\u05E8\u05D5\u05EA \u00A9 2026
</footer>'''


# ── Main Generator ───────────────────────────────────────────

def generate_s4(clinic, theme_idx):
    t = THEMES[theme_idx % len(THEMES)]

    raw_name = clinic.get("name", "").replace('""', '"')
    city = clinic.get("city", "").strip() or "גוש דן"
    phone = clinic.get("phone", "").strip()
    rating = safe_float(clinic.get("rating"), 5.0)
    reviews = safe_int(clinic.get("review_count"))
    maps_url = clinic.get("google_maps_url", "").strip()

    doctor_name = extract_doctor_name(raw_name)
    display_name = clean_display_name(raw_name, city)

    css = build_css(t)
    nav = build_nav(display_name, phone, t)
    hero = build_hero(display_name, doctor_name, city, phone, rating, reviews, t)
    services = build_services(t)
    about = build_about(doctor_name, display_name, city, t)
    rating_sec = build_rating(rating, reviews, maps_url, t)
    contact = build_contact(phone, city, maps_url, t)
    footer = build_footer(display_name, city, t)

    if "\u05DE\u05E8\u05E4\u05D0" in display_name or "\u05D3\"\u05E8" in display_name or "Dr" in display_name:
        title = f"{display_name} | {city}"
    else:
        title = f"\u05DE\u05E8\u05E4\u05D0\u05EA \u05E9\u05D9\u05E0\u05D9\u05D9\u05DD {display_name} | {city}"

    return f'''<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{nav}
{hero}
{services}
{about}
{rating_sec}
{contact}
{footer}
</body>
</html>'''


# ── CLI ──────────────────────────────────────────────────────

def main():
    test_n = None
    for i, arg in enumerate(sys.argv[1:], 1):
        if sys.argv[i - 1] == "--test":
            try:
                test_n = int(arg)
            except ValueError:
                pass

    leads = load_csv(LEADS_CSV)
    seg4 = [r for r in leads if r.get("segment") == "4"]

    if test_n:
        seg4 = seg4[:test_n]

    os.makedirs(REPORTS_DIR, exist_ok=True)

    for idx, clinic in enumerate(seg4, 1):
        html = generate_s4(clinic, theme_idx=idx - 1)
        fname = sanitize_filename(clinic.get("name", "clinic"), idx)
        path = os.path.join(REPORTS_DIR, f"{fname}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    print(f"S4 websites generated: {len(seg4)} files")
    print(f"Output: {REPORTS_DIR}/")


if __name__ == "__main__":
    main()
