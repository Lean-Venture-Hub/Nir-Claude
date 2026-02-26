#!/usr/bin/env python3
"""
Generate deterministic S4 websites from content.md files.

Reads each reports/S4/{name}/content.md, extracts REAL data only,
and renders a full landing page. Zero hallucination — every piece of
text comes from the parsed content.md or from a fixed generic fallback.

Usage:
    python generate_s4_from_content.py              # generate all
    python generate_s4_from_content.py --test 3     # first 3 only
    python generate_s4_from_content.py --dry-run    # parse only, print summary
"""

import os
import re
import sys
import html as html_mod
from pathlib import Path
from typing import Optional, List, Dict

SCRIPT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = SCRIPT_DIR / "reports" / "S4"

# ── Content Parser ──────────────────────────────────────────────

def parse_content_md(text: str) -> dict:
    """Parse a content.md file into a structured dict with all real data."""
    data = {
        "raw_name": "",
        "doctor_name": "",
        "city": "",
        "address": "",
        "phone": "",
        "rating": 0.0,
        "review_count": 0,
        "google_maps_url": "",
        "category": "",
        "hours": [],          # list of (day, hours_str)
        "reviews": [],        # list of {author, stars, text}
        "services": [],       # list of service names
        "subtitle": "",
        "description": "",
        "cta_text": "",
        "cta_phone": "",
        "website_title": "",
        "segment": "",
    }

    # ── פרטי המרפאה section ──
    name_m = re.search(r'\*\*שם:\*\*\s*(.+)', text)
    if name_m:
        data["raw_name"] = name_m.group(1).strip()

    doctor_m = re.search(r'\*\*רופא:\*\*\s*(.+)', text)
    if doctor_m:
        data["doctor_name"] = doctor_m.group(1).strip()

    city_m = re.search(r'\*\*עיר:\*\*\s*(.+)', text)
    if city_m:
        city_val = city_m.group(1).strip()
        # Validate: don't accept if it starts with '- **' (grabbed next field)
        if city_val and not city_val.startswith('- **') and not city_val.startswith('**'):
            data["city"] = city_val
        else:
            # Try to extract city from business name (e.g., "רופא שיניים בתל אביב")
            city_from_name = re.search(r'ב(תל אביב|בת ים|חולון|רמת גן|פתח תקווה|בני ברק|גבעתיים|הרצליה|קרית אונו)', data.get("raw_name", ""))
            if city_from_name:
                data["city"] = city_from_name.group(1)

    # Address: line after **כתובת:**
    addr_m = re.search(r'\*\*כתובת:\*\*\s*\n(.+)', text)
    if addr_m:
        data["address"] = addr_m.group(1).strip()

    # Phone: line after **טלפון:** — must look like a phone number
    phone_m = re.search(r'\*\*טלפון:\*\*\s*\n(.+)', text)
    if phone_m:
        phone_val = phone_m.group(1).strip()
        # Validate: must contain digits and dashes, look like a phone number
        if phone_val and re.match(r'^[\d\-\s+()]{7,}$', phone_val):
            data["phone"] = phone_val

    # Rating
    rating_m = re.search(r'\*\*דירוג Google:\*\*\s*([\d.]+)\s*⭐?\s*\((\d+)\s*ביקורות\)', text)
    if rating_m:
        data["rating"] = float(rating_m.group(1))
        data["review_count"] = int(rating_m.group(2))

    # Google Maps URL
    maps_m = re.search(r'\*\*Google Maps:\*\*\s*(https://[^\s]+)', text)
    if maps_m:
        data["google_maps_url"] = maps_m.group(1).strip()

    # Category
    cat_m = re.search(r'\*\*קטגוריה:\*\*\s*(.+)', text)
    if cat_m:
        data["category"] = cat_m.group(1).strip()

    # ── Hours section ──
    hours_section = re.search(r'## שעות פעילות\n(.*?)(?=\n## )', text, re.DOTALL)
    if hours_section:
        hours_text = hours_section.group(1)
        day_pattern = re.findall(
            r'(יום (?:ראשון|שני|שלישי|רביעי|חמישי|שישי|שבת))\s*\n\s*\t?\s*\n?([\d:–\-סגור]+)',
            hours_text
        )
        for day, hrs in day_pattern:
            data["hours"].append((day.strip(), hrs.strip()))

    # ── Reviews section (raw, with star count) ──
    # Hebrew star words: כוכב אחד (1), שני כוכבים (2), 3 כוכבים, 4 כוכבים, 5 כוכבים
    STAR_MAP = {"כוכב אחד": 1, "שני כוכבים": 2, "שלושה כוכבים": 3}

    reviews_section = re.search(r'## ביקורות Google[^\n]*\n(.*?)(?=\n## )', text, re.DOTALL)
    if reviews_section:
        # Split into individual review headers
        review_headers = re.finditer(
            r'### (.+?) — (.+?)\s*\(([^)]+)\)\n((?:> .+\n?)*)',
            reviews_section.group(1)
        )
        for m in review_headers:
            author = m.group(1).strip().strip('\u200e\u200f\u202a\u202b\u202c')
            stars_raw = m.group(2).strip()
            date = m.group(3).strip()
            review_text = m.group(4).strip()

            # Parse star count
            if stars_raw in STAR_MAP:
                stars = STAR_MAP[stars_raw]
            else:
                # Try "N כוכבים" pattern
                stars_num = re.match(r'(\d+)\s*כוכב', stars_raw)
                if stars_num:
                    stars = int(stars_num.group(1))
                else:
                    stars = 5  # default if unparseable

            # Clean review text (remove > prefixes and join lines)
            clean_text = re.sub(r'^>\s*', '', review_text, flags=re.MULTILINE)
            clean_text = clean_text.replace('\n', ' ').strip()

            data["reviews"].append({
                "author": author,
                "stars": stars,
                "date": date,
                "text": clean_text,
            })

    # ── Website content section ──
    title_m = re.search(r'### כותרת\n(.+)', text)
    if title_m:
        data["website_title"] = title_m.group(1).strip()

    sub_m = re.search(r'### תת-כותרת\n(.+)', text)
    if sub_m:
        data["subtitle"] = sub_m.group(1).strip()

    desc_m = re.search(r'### תיאור קצר\n(.+?)(?=\n###)', text, re.DOTALL)
    if desc_m:
        data["description"] = desc_m.group(1).strip().replace('\n', ' ')

    # Services
    svc_section = re.search(r'### שירותים\n((?:- .+\n?)+)', text)
    if svc_section:
        data["services"] = [
            line.lstrip('- ').strip()
            for line in svc_section.group(1).strip().split('\n')
            if line.strip().startswith('-')
        ]

    # CTA
    cta_m = re.search(r'### CTA\n(.+?)(?=\n###|\n## |\Z)', text, re.DOTALL)
    if cta_m:
        cta_raw = cta_m.group(1).strip()
        # Extract phone from CTA line
        cta_phone_m = re.search(r'([\d-]{9,})', cta_raw)
        if cta_phone_m:
            data["cta_phone"] = cta_phone_m.group(1)

    # Segment
    seg_m = re.search(r'## סגמנט\n(.+)', text)
    if seg_m:
        data["segment"] = seg_m.group(1).strip()

    # Fall back: use CTA phone if main phone is missing
    if not data["phone"] and data["cta_phone"]:
        data["phone"] = data["cta_phone"]

    return data


# ── Display Name Helpers ─────────────────────────────────────────

def extract_display_name(raw_name: str, city: str) -> str:
    """Clean the raw business name for display."""
    name = raw_name
    for prefix in ['מרפאת שיניים, ', 'מרפאת שיניים- ', 'מרפאת שיניים ',
                    'רופא שיניים ב', 'רופאת שיניים ב']:
        if name.startswith(prefix):
            stripped = name[len(prefix):].strip()
            if stripped != city and len(stripped) >= 4:
                name = stripped
                break
    # Truncate long names with ' - ' separator
    if ' - ' in name and len(name) > 40:
        name = name.split(' - ')[0].strip()
    return name


def extract_doctor_short(doctor_field: str) -> Optional[str]:
    """Extract just the doctor's personal name (e.g., 'גיא פרידמן' from 'ד"ר גיא פרידמן מומחה לשיקום הפה')."""
    stop_words = ['מומחה', 'מומחית', 'מרפאת', 'רופא', 'שיניים', 'מרכז',
                  'כירורג', 'השתלות', 'בתל', 'בבת', 'בבני', 'בפתח',
                  'בחולון', 'ברמת', 'בגבעתיים', 'בהרצליה', 'בקרית',
                  'לשיקום', 'טיפולי', 'אנדודונטיה', 'אסתטיקה']

    def clean_candidate(candidate):
        candidate = candidate.strip()
        for sw in stop_words:
            if sw in candidate:
                candidate = candidate[:candidate.index(sw)].strip()
        words = candidate.split()[:3]
        result = ' '.join(words).strip(' -,')
        return result if len(result) > 2 else None

    # Pattern 1: "Name, ד"ר" (reversed format like "אלי פרידוולד, דר")
    rev_m = re.match(r'^(.+?),\s*[דd][\"\u05F4\']?\u05E8\s*$', doctor_field)
    if rev_m:
        result = clean_candidate(rev_m.group(1))
        if result:
            return result

    # Pattern 2: Standard "ד"ר Name" / "דר Name"
    patterns = [
        r'[דd][\"\u05F4\']?\u05E8\s+([^\-,(]+)',   # ד"ר / דר / ד״ר
        r'Dr\.?\s*([A-Za-z][^\-,(]+)',               # English Dr. (with or without space)
    ]
    for pat in patterns:
        m = re.search(pat, doctor_field)
        if m:
            result = clean_candidate(m.group(1))
            if result:
                return result

    return None


def get_positive_reviews(reviews: list, min_stars: int = 4) -> list:
    """Filter to positive reviews with actual text content."""
    return [
        r for r in reviews
        if r["stars"] >= min_stars and len(r["text"]) > 10
    ]


def truncate_review(text: str, max_len: int = 150) -> str:
    """Truncate review text at word boundary."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len].rsplit(' ', 1)[0]
    return truncated.rstrip('.,!? ') + '...'


def stars_html(count: int) -> str:
    """Generate star characters for a given count."""
    return '&#9733;' * count + '&#9734;' * (5 - count)


def esc(text: str) -> str:
    """HTML-escape text."""
    return html_mod.escape(text, quote=True)


# ── Color Themes ─────────────────────────────────────────────────

THEMES = [
    {   # Navy / Gold
        "name": "navy",
        "primary": "#1a2e4a", "primary_dark": "#0f1c2e",
        "accent": "#c9a84c", "accent_soft": "rgba(201,168,76,0.12)",
        "hero_grad": "linear-gradient(135deg, #1a2e4a 0%, #2d4a6e 60%, #1a2e4a 100%)",
        "cta_bg": "#c9a84c", "cta_text": "#1a2e4a",
    },
    {   # Teal / White
        "name": "teal",
        "primary": "#1a7a6e", "primary_dark": "#115a50",
        "accent": "#2ba899", "accent_soft": "rgba(43,168,153,0.12)",
        "hero_grad": "linear-gradient(135deg, #1a7a6e 0%, #2ba899 50%, #1a7a6e 100%)",
        "cta_bg": "#fff", "cta_text": "#1a7a6e",
    },
    {   # Slate Blue / Sky
        "name": "slate",
        "primary": "#2c3e6b", "primary_dark": "#1a2547",
        "accent": "#5b8def", "accent_soft": "rgba(91,141,239,0.12)",
        "hero_grad": "linear-gradient(135deg, #2c3e6b 0%, #3d5a9e 60%, #2c3e6b 100%)",
        "cta_bg": "#5b8def", "cta_text": "#fff",
    },
    {   # Charcoal / Coral
        "name": "charcoal",
        "primary": "#2d2d2d", "primary_dark": "#1a1a1a",
        "accent": "#e07055", "accent_soft": "rgba(224,112,85,0.12)",
        "hero_grad": "linear-gradient(135deg, #2d2d2d 0%, #444 60%, #2d2d2d 100%)",
        "cta_bg": "#e07055", "cta_text": "#fff",
    },
    {   # Forest / Mint
        "name": "forest",
        "primary": "#2e5d4b", "primary_dark": "#1c3d31",
        "accent": "#4caf82", "accent_soft": "rgba(76,175,130,0.12)",
        "hero_grad": "linear-gradient(135deg, #2e5d4b 0%, #3d7a62 60%, #2e5d4b 100%)",
        "cta_bg": "#4caf82", "cta_text": "#fff",
    },
]

# ── Generic Service Data (fallback when content.md has generic list) ──

SERVICE_ICONS = {
    "טיפולי שיניים כלליים": "tooth",
    "טיפולי שיניים אסתטיים": "smile",
    "השתלות שיניים": "implant",
    "יישור שיניים": "braces",
    "טיפולי חניכיים": "shield",
    "רפואת שיניים לילדים": "child",
}

SERVICE_DESCRIPTIONS = {
    "טיפולי שיניים כלליים": "בדיקות תקופתיות, סתימות וטיפולים מונעים לשמירה על בריאות הפה",
    "טיפולי שיניים אסתטיים": "ציפויי חרסינה, הלבנה ושיפור מראה החיוך",
    "השתלות שיניים": "פתרון קבע לשיניים חסרות בטכנולוגיה מתקדמת",
    "יישור שיניים": "קשתיות שקופות וברייסס לחיוך ישר ומסודר",
    "טיפולי חניכיים": "טיפול ומניעה של מחלות חניכיים לבריאות ארוכת טווח",
    "רפואת שיניים לילדים": "סביבה נעימה וטיפול עדין המותאם לכל הגילאים",
}

# SVG icon paths by type
SVG_ICONS = {
    "tooth": '<svg viewBox="0 0 64 64" width="40" height="40" fill="none"><path d="M32 6C22 6 14 13 14 22c0 8 2 14 6 22 2 6 6 14 10 14 1.5 0 2.5-3 3.5-7 .5 2 1.5 4 2.5 7 4 0 8-6 10-14 4-8 6-14 6-22C52 13 44 6 32 6Z" fill="{accent}" opacity=".15" stroke="{accent}" stroke-width="2.5" stroke-linejoin="round"/></svg>',
    "implant": '<svg viewBox="0 0 64 64" width="40" height="40" fill="none"><rect x="24" y="6" width="16" height="14" rx="4" fill="{accent}" opacity=".15" stroke="{accent}" stroke-width="2.5"/><path d="M26 24h12l-1 10h-10l-1-10Zm1 14h10l-1 10h-8l-1-10Zm1 14h8l-1 6h-6l-1-6Z" stroke="{accent}" stroke-width="2.5" stroke-linejoin="round" fill="{accent}" opacity=".1"/></svg>',
    "smile": '<svg viewBox="0 0 64 64" width="40" height="40" fill="none"><circle cx="32" cy="32" r="26" fill="{accent}" opacity=".12" stroke="{accent}" stroke-width="2.5"/><circle cx="23" cy="27" r="3" fill="{accent}"/><circle cx="41" cy="27" r="3" fill="{accent}"/><path d="M22 38c3 6 8 9 10 9s7-3 10-9" stroke="{accent}" stroke-width="2.5" stroke-linecap="round"/></svg>',
    "shield": '<svg viewBox="0 0 64 64" width="40" height="40" fill="none"><path d="M32 4L10 16v16c0 14 10 24 22 28 12-4 22-14 22-28V16L32 4Z" fill="{accent}" opacity=".12" stroke="{accent}" stroke-width="2.5" stroke-linejoin="round"/><path d="M24 32l6 6 12-14" stroke="{accent}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "child": '<svg viewBox="0 0 64 64" width="40" height="40" fill="none"><circle cx="32" cy="22" r="14" fill="{accent}" opacity=".12" stroke="{accent}" stroke-width="2.5"/><circle cx="27" cy="20" r="2" fill="{accent}"/><circle cx="37" cy="20" r="2" fill="{accent}"/><path d="M28 27c1.5 2 3 3 4 3s2.5-1 4-3" stroke="{accent}" stroke-width="2" stroke-linecap="round"/><path d="M22 38v10a6 6 0 006 6h8a6 6 0 006-6V38" stroke="{accent}" stroke-width="2.5"/></svg>',
    "braces": '<svg viewBox="0 0 64 64" width="40" height="40" fill="none"><rect x="8" y="22" width="48" height="20" rx="10" fill="{accent}" opacity=".12" stroke="{accent}" stroke-width="2.5"/><line x1="20" y1="26" x2="20" y2="38" stroke="{accent}" stroke-width="2"/><line x1="32" y1="26" x2="32" y2="38" stroke="{accent}" stroke-width="2"/><line x1="44" y1="26" x2="44" y2="38" stroke="{accent}" stroke-width="2"/><line x1="14" y1="32" x2="50" y2="32" stroke="{accent}" stroke-width="2.5"/></svg>',
}

# Inline SVGs for nav/contact/footer
SVG_PHONE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>'

SVG_MAP = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>'

SVG_CLOCK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'

SVG_NAV_TOOTH = '<svg width="24" height="24" viewBox="0 0 64 64" fill="none"><path d="M32 6C22 6 14 13 14 22c0 8 2 14 6 22 2 6 6 14 10 14 1.5 0 2.5-3 3.5-7 .5 2 1.5 4 2.5 7 4 0 8-6 10-14 4-8 6-14 6-22C52 13 44 6 32 6Z" fill="rgba(255,255,255,.9)" stroke="rgba(255,255,255,.5)" stroke-width="2"/></svg>'

SVG_GOOGLE = '<svg width="18" height="18" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18A10.96 10.96 0 001 12c0 1.77.42 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>'


# ── CSS Template ─────────────────────────────────────────────────

def build_css(t: dict) -> str:
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
  display:flex;align-items:center;gap:10px;text-decoration:none}}
.nav-links{{display:flex;align-items:center;gap:24px;list-style:none}}
.nav-links a{{color:rgba(255,255,255,.75);text-decoration:none;font-size:14px;font-weight:500;
  transition:color .2s}}
.nav-links a:hover{{color:#fff}}
.nav-cta{{background:{t['cta_bg']};color:{t['cta_text']};border:none;padding:10px 22px;
  border-radius:100px;font-size:14px;font-weight:600;cursor:pointer;
  text-decoration:none;transition:opacity .2s;display:inline-flex;align-items:center;gap:8px}}
.nav-cta:hover{{opacity:.85}}

/* HERO */
.hero{{background:{t['hero_grad']};min-height:520px;display:flex;align-items:center;
  padding:60px 40px;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;left:-120px;top:-80px;width:500px;height:500px;
  border-radius:50%;background:rgba(255,255,255,.04)}}
.hero-content{{position:relative;max-width:620px}}
.hero-badge{{display:inline-flex;align-items:center;gap:8px;
  background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);color:#fff;
  padding:6px 16px;border-radius:100px;font-size:13px;margin-bottom:24px;
  backdrop-filter:blur(4px)}}
.hero-badge .dot{{width:7px;height:7px;border-radius:50%;background:#4ade80}}
.hero h1{{font-size:clamp(28px,5vw,44px);font-weight:800;color:#fff;line-height:1.15;
  margin-bottom:16px;letter-spacing:-.5px}}
.hero h1 em{{font-style:normal;color:{t['accent']}}}
.hero .sub{{font-size:17px;color:rgba(255,255,255,.8);margin-bottom:32px;max-width:480px}}
.hero-cta{{display:inline-flex;align-items:center;gap:10px;background:#fff;
  color:{t['primary']};padding:14px 28px;border-radius:100px;font-size:16px;
  font-weight:700;text-decoration:none;box-shadow:0 4px 20px rgba(0,0,0,.2);
  transition:transform .2s,box-shadow .2s}}
.hero-cta:hover{{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,.25)}}
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

/* SERVICES */
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
.info-list{{list-style:none;display:flex;flex-direction:column;gap:16px}}
.info-item{{display:flex;align-items:flex-start;gap:14px}}
.info-icon{{flex-shrink:0;width:40px;height:40px;border-radius:12px;
  background:{t['accent_soft']};display:flex;align-items:center;
  justify-content:center;color:{t['primary']}}}
.info-text h4{{font-size:15px;font-weight:700;color:#1a1a2e}}
.info-text p{{font-size:13px;color:#666;margin-top:2px}}
.info-text a{{color:{t['primary']};text-decoration:none;font-weight:600}}

/* TESTIMONIALS */
.tg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;
  max-width:900px;margin:0 auto}}
.tc{{background:#fff;border:1px solid #e8eaed;border-radius:16px;padding:24px;
  transition:box-shadow .2s}}
.tc:hover{{box-shadow:0 8px 24px rgba(0,0,0,.06)}}
.tc-stars{{color:#fbbf24;font-size:14px;letter-spacing:2px;margin-bottom:12px}}
.tc blockquote{{font-size:14px;line-height:1.7;color:#444;margin:0 0 16px;font-style:normal}}
.tc-author{{display:flex;align-items:center;gap:10px}}
.tc-avatar{{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:14px;font-weight:700;color:#fff;flex-shrink:0}}
.tc-name{{font-size:13px;font-weight:600;color:#1a1a2e}}
.tc-date{{font-size:11px;color:#999}}

/* HOURS */
.hours-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
  gap:12px;max-width:700px;margin:0 auto}}
.hour-item{{background:#fff;border:1px solid #e8eaed;border-radius:12px;padding:14px 18px;
  display:flex;justify-content:space-between;align-items:center}}
.hour-day{{font-size:13px;font-weight:600;color:#1a1a2e}}
.hour-time{{font-size:13px;color:#666;direction:ltr}}
.hour-closed{{color:#ef4444;font-weight:500}}

/* RATING SECTION */
.rating-sec{{background:{t['hero_grad']};padding:64px 40px;text-align:center;color:#fff}}
.big-score{{font-size:80px;font-weight:900;line-height:1;color:#fff}}
.rating-src{{font-size:14px;opacity:.7;margin-top:8px}}
.rating-cta{{display:inline-block;margin-top:28px;background:#fff;color:{t['primary']};
  padding:14px 32px;border-radius:100px;font-size:16px;font-weight:700;
  text-decoration:none;box-shadow:0 4px 20px rgba(0,0,0,.2);transition:transform .2s}}
.rating-cta:hover{{transform:translateY(-2px)}}

/* CONTACT */
.cg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:20px;margin-top:32px;max-width:900px;margin-left:auto;margin-right:auto}}
.cc{{background:#fff;border:1px solid #e8eaed;border-radius:16px;padding:24px;
  display:flex;align-items:center;gap:16px;text-decoration:none;color:inherit;
  transition:box-shadow .2s,border-color .2s}}
.cc:hover{{box-shadow:0 8px 24px rgba(0,0,0,.08);border-color:{t['accent']}}}
.ci{{width:48px;height:48px;border-radius:12px;background:{t['accent_soft']};
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
  color:{t['primary']}}}
.cc .label{{font-size:12px;color:#999;font-weight:500}}
.cc .value{{font-size:16px;font-weight:700;color:#1a1a2e}}

/* FOOTER */
footer{{background:{t['primary_dark']};color:rgba(255,255,255,.6);text-align:center;
  padding:24px 40px;font-size:13px}}
footer strong{{color:rgba(255,255,255,.9)}}

/* MOBILE */
@media(max-width:768px){{
  nav{{padding:0 20px}}.nav-links{{display:none}}
  .hero{{padding:40px 20px;min-height:auto}}
  .section{{padding:48px 20px}}
  .sg{{grid-template-columns:1fr 1fr}}
  .about-grid{{grid-template-columns:1fr;gap:32px}}
  .tg{{grid-template-columns:1fr}}
  .big-score{{font-size:64px}}
  .hours-grid{{grid-template-columns:1fr}}
}}
@media(max-width:420px){{
  .sg{{grid-template-columns:1fr}}
  .hero h1{{font-size:28px}}
}}
"""


# ── HTML Section Builders ────────────────────────────────────────

def build_nav(display_name: str, phone: str, t: dict) -> str:
    if phone:
        cta = f'<a class="nav-cta" href="tel:{esc(phone)}">{SVG_PHONE} קבעו תור</a>'
    else:
        cta = '<span class="nav-cta" style="opacity:.6">רפואת שיניים מקצועית</span>'

    return f'''<nav>
  <a href="#" class="nav-logo">{SVG_NAV_TOOTH} {esc(display_name)}</a>
  <ul class="nav-links">
    <li><a href="#services">שירותים</a></li>
    <li><a href="#about">אודות</a></li>
    <li><a href="#reviews">ביקורות</a></li>
    <li><a href="#contact">צרו קשר</a></li>
  </ul>
  {cta}
</nav>'''


def build_hero(data: dict, display_name: str, doctor_short: Optional[str], t: dict) -> str:
    city = esc(data["city"]) or "גוש דן"
    rating = data["rating"]
    reviews = data["review_count"]

    if doctor_short:
        h1 = f'ד"ר {esc(doctor_short)}<br><em>חיוך שמתחיל בידיים טובות</em>'
    else:
        h1 = f'{esc(display_name)}<br><em>טיפול מקצועי ואישי</em>'

    subtitle = data["subtitle"] or f'מרפאת שיניים ב{city} — טיפול מקצועי, אישי ועדין לכל המשפחה.'

    cta_href = f'tel:{esc(data["phone"])}' if data["phone"] else '#contact'
    cta_text = "קבעו תור עכשיו" if data["phone"] else "צרו קשר"
    cta_arrow = "&#8592;" if data["phone"] else "&#8595;"

    rev_line = f'<div class="rev-label">{reviews} ביקורות מטופלים</div>' if reviews > 0 else ''
    rating_str = f"{rating:.1f}" if rating == int(rating) else f"{rating}"

    return f'''<section class="hero">
  <div class="hero-content">
    <div class="hero-badge"><span class="dot"></span> מרפאה פעילה | {city}</div>
    <h1>{h1}</h1>
    <p class="sub">{esc(subtitle)}</p>
    <a class="hero-cta" href="{cta_href}">{cta_text} {cta_arrow}</a>
    <div class="hero-rating">
      <div>
        <div class="score">{rating_str}</div>
        <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      </div>
      <div>
        <div style="color:#fff;font-weight:700;font-size:15px">Google דירוג</div>
        {rev_line}
      </div>
    </div>
  </div>
</section>'''


def build_services(services: list, t: dict) -> str:
    icon_keys = list(SVG_ICONS.keys())
    cards = ""
    for i, svc_name in enumerate(services[:6]):
        # Match to an icon, or cycle through them
        icon_key = SERVICE_ICONS.get(svc_name, icon_keys[i % len(icon_keys)])
        svg = SVG_ICONS[icon_key].replace("{accent}", t["accent"])
        desc = SERVICE_DESCRIPTIONS.get(svc_name, "טיפול מקצועי ומותאם אישית")
        cards += f'''    <div class="sc">
      <div>{svg}</div>
      <h3>{esc(svc_name)}</h3>
      <p>{esc(desc)}</p>
    </div>\n'''

    return f'''<div class="section-white" id="services">
  <div class="section">
    <div class="stw">
      <div class="tag">השירותים שלנו</div>
      <h2>טיפולים <em>מקצועיים</em><br>לכל הצרכים שלך</h2>
    </div>
    <div class="sg">
{cards}    </div>
  </div>
</div>'''


def build_about(data: dict, display_name: str, doctor_short: Optional[str], t: dict) -> str:
    city = esc(data["city"]) or "גוש דן"
    address = data["address"]
    phone = data["phone"]

    # Doctor card
    initial = "ד"
    if doctor_short:
        initial = doctor_short[0]
        card_name = f'ד"ר {esc(doctor_short)}'
        card_title = f'{esc(data["category"] or "רופא/ת שיניים")} | {city}'
    else:
        initial = display_name[0] if display_name else "מ"
        card_name = esc(display_name)
        card_title = f'מרפאת שיניים | {city}'

    # Info items (real data only)
    info_items = ""
    if address:
        info_items += f'''<li class="info-item">
        <div class="info-icon">{SVG_MAP}</div>
        <div class="info-text"><h4>כתובת</h4><p>{esc(address)}</p></div>
      </li>'''
    if phone:
        info_items += f'''<li class="info-item">
        <div class="info-icon">{SVG_PHONE}</div>
        <div class="info-text"><h4>טלפון</h4><p style="direction:ltr;text-align:right"><a href="tel:{esc(phone)}">{esc(phone)}</a></p></div>
      </li>'''
    if data["google_maps_url"]:
        info_items += f'''<li class="info-item">
        <div class="info-icon">{SVG_GOOGLE}</div>
        <div class="info-text"><h4>Google Maps</h4><p><a href="{esc(data["google_maps_url"])}" target="_blank">צפו בפרופיל שלנו</a></p></div>
      </li>'''

    return f'''<div class="section-gray" id="about">
  <div class="section">
    <div class="stw">
      <div class="tag">אודות</div>
      <h2>למה <em>לבחור</em> בנו</h2>
    </div>
    <div class="about-grid">
      <div class="doc-card">
        <div class="doc-avatar">{initial}</div>
        <div class="name">{card_name}</div>
        <div class="title">{card_title}</div>
      </div>
      <ul class="info-list">{info_items}</ul>
    </div>
  </div>
</div>'''


def build_testimonials(reviews: list, t: dict) -> str:
    """Build testimonials section from REAL positive reviews only."""
    positive = get_positive_reviews(reviews, min_stars=4)
    if not positive:
        return ""  # No testimonials section if no good reviews

    # Use up to 3 best reviews
    selected = positive[:3]
    avatar_colors = [t["primary"], t["accent"], "#6B7280"]

    cards = ""
    for i, rev in enumerate(selected):
        color = avatar_colors[i % len(avatar_colors)]
        initial = rev["author"][0] if rev["author"] else "מ"
        # Clean the initial from unicode markers
        if not (initial.isalpha() or '\u0590' <= initial <= '\u05FF'):
            initial = "מ"

        display_text = truncate_review(rev["text"], 200)

        cards += f'''    <div class="tc">
      <div class="tc-stars">{stars_html(rev["stars"])}</div>
      <blockquote>{esc(display_text)}</blockquote>
      <div class="tc-author">
        <div class="tc-avatar" style="background:{color}">{initial}</div>
        <div>
          <div class="tc-name">{esc(rev["author"])}</div>
          <div class="tc-date">{esc(rev["date"])}</div>
        </div>
      </div>
    </div>\n'''

    return f'''<div class="section-white" id="reviews">
  <div class="section">
    <div class="stw">
      <div class="tag">ביקורות</div>
      <h2>מה <em>המטופלים</em> שלנו אומרים</h2>
    </div>
    <div class="tg">
{cards}    </div>
  </div>
</div>'''


def build_hours(hours: list, t: dict) -> str:
    if not hours:
        return ""

    items = ""
    for day, time_str in hours:
        if time_str == "סגור":
            items += f'''<div class="hour-item">
        <span class="hour-day">{esc(day)}</span>
        <span class="hour-time hour-closed">סגור</span>
      </div>'''
        else:
            items += f'''<div class="hour-item">
        <span class="hour-day">{esc(day)}</span>
        <span class="hour-time">{esc(time_str)}</span>
      </div>'''

    return f'''<div class="section-gray">
  <div class="section">
    <div class="stw">
      <div class="tag">שעות פעילות</div>
      <h2>מתי <em>אפשר</em> להגיע</h2>
    </div>
    <div class="hours-grid">
      {items}
    </div>
  </div>
</div>'''


def build_rating_section(data: dict, t: dict) -> str:
    rating = data["rating"]
    reviews = data["review_count"]
    maps_url = data["google_maps_url"]

    rating_str = f"{rating:.1f}" if rating == int(rating) else f"{rating}"
    rev_text = f'<div style="font-size:18px;color:rgba(255,255,255,.9);margin-top:12px">{reviews} ביקורות מטופלים ב-Google</div>' if reviews else ''
    maps_btn = f'<a class="rating-cta" href="{esc(maps_url)}" target="_blank">ראו אותנו בגוגל</a>' if maps_url else ''

    return f'''<section class="rating-sec">
  <div class="big-score">{rating_str}</div>
  <div class="stars" style="font-size:28px">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
  {rev_text}
  <div class="rating-src">דירוג Google Maps</div>
  {maps_btn}
</section>'''


def build_contact(data: dict, t: dict) -> str:
    phone = data["phone"]
    city = data["city"]
    address = data["address"]
    maps_url = data["google_maps_url"]

    cards = ""
    if phone:
        cards += f'''<a class="cc" href="tel:{esc(phone)}">
      <div class="ci">{SVG_PHONE}</div>
      <div><div class="label">טלפון</div><div class="value" style="direction:ltr">{esc(phone)}</div></div>
    </a>'''

    if address:
        link_open = f'<a class="cc" href="{esc(maps_url)}" target="_blank">' if maps_url else '<div class="cc">'
        link_close = '</a>' if maps_url else '</div>'
        cards += f'''{link_open}
      <div class="ci">{SVG_MAP}</div>
      <div><div class="label">כתובת</div><div class="value">{esc(address)}</div></div>
    {link_close}'''

    if maps_url:
        cards += f'''<a class="cc" href="{esc(maps_url)}" target="_blank">
      <div class="ci">{SVG_GOOGLE}</div>
      <div><div class="label">Google Maps</div><div class="value">צפו בפרופיל שלנו</div></div>
    </a>'''

    return f'''<div class="section-white" id="contact">
  <div class="section">
    <div class="stw">
      <div class="tag">צרו קשר</div>
      <h2>קבעו <em>תור</em> עוד היום</h2>
    </div>
    <div class="cg">{cards}</div>
  </div>
</div>'''


def build_footer(display_name: str, city: str, t: dict) -> str:
    return f'''<footer>
  <strong>{esc(display_name)}</strong> | {esc(city or "ישראל")} | כל הזכויות שמורות &copy; 2026
</footer>'''


# ── Full Page Assembly ───────────────────────────────────────────

def generate_page(data: dict, theme_idx: int) -> str:
    t = THEMES[theme_idx % len(THEMES)]
    display_name = extract_display_name(data["raw_name"], data["city"])
    doctor_short = extract_doctor_short(data["doctor_name"])
    city = data["city"] or "גוש דן"

    # Build title
    if "מרפא" in display_name or 'ד"ר' in display_name or "דר" in display_name or "Dr" in display_name:
        title = f"{display_name} | {city}"
    else:
        title = f"מרפאת שיניים {display_name} | {city}"

    css = build_css(t)
    nav = build_nav(display_name, data["phone"], t)
    hero = build_hero(data, display_name, doctor_short, t)
    services = build_services(data["services"] or [
        "טיפולי שיניים כלליים", "השתלות שיניים", "טיפולי שיניים אסתטיים",
        "יישור שיניים", "טיפולי חניכיים", "רפואת שיניים לילדים"
    ], t)
    about = build_about(data, display_name, doctor_short, t)
    testimonials = build_testimonials(data["reviews"], t)
    hours = build_hours(data["hours"], t)
    rating_sec = build_rating_section(data, t)
    contact = build_contact(data, t)
    footer = build_footer(display_name, city, t)

    return f'''<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<style>{css}</style>
</head>
<body>
{nav}
{hero}
{services}
{about}
{testimonials}
{hours}
{rating_sec}
{contact}
{footer}
</body>
</html>'''


# ── CLI ──────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv
    test_n = None
    for i, arg in enumerate(sys.argv):
        if arg == "--test" and i + 1 < len(sys.argv):
            try:
                test_n = int(sys.argv[i + 1])
            except ValueError:
                pass

    if not REPORTS_DIR.exists():
        print(f"Error: {REPORTS_DIR} not found")
        sys.exit(1)

    # Find all content.md files
    content_files = sorted(REPORTS_DIR.glob("*/content.md"))
    if test_n:
        content_files = content_files[:test_n]

    print(f"Found {len(content_files)} content.md files")

    generated = 0
    skipped = 0
    errors = []

    for idx, content_path in enumerate(content_files):
        folder = content_path.parent
        folder_name = folder.name

        try:
            text = content_path.read_text(encoding="utf-8")
            data = parse_content_md(text)

            if dry_run:
                pos_reviews = get_positive_reviews(data["reviews"])
                print(f"\n{'─'*60}")
                print(f"  [{idx+1}] {folder_name}")
                print(f"  City: {data['city'] or '(missing)'}")
                print(f"  Phone: {data['phone'] or '(missing)'}")
                print(f"  Rating: {data['rating']} ({data['review_count']} reviews)")
                print(f"  Reviews parsed: {len(data['reviews'])} total, {len(pos_reviews)} positive")
                print(f"  Services: {len(data['services'])}")
                print(f"  Hours: {len(data['hours'])} days")
                print(f"  Doctor: {extract_doctor_short(data['doctor_name']) or '(not found)'}")
                continue

            html = generate_page(data, theme_idx=idx)
            out_path = folder / "index.html"
            out_path.write_text(html, encoding="utf-8")
            generated += 1

        except Exception as e:
            errors.append((folder_name, str(e)))
            skipped += 1

    print(f"\n{'='*60}")
    if dry_run:
        print(f"Dry run complete: {len(content_files)} files parsed")
    else:
        print(f"Generated: {generated} websites")
    if skipped:
        print(f"Skipped: {skipped} (errors)")
        for name, err in errors:
            print(f"  - {name}: {err}")
    print(f"Output: {REPORTS_DIR}/")


if __name__ == "__main__":
    main()
