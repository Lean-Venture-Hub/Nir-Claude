#!/usr/bin/env python3
"""
seed-data.py
Reads labeled-dentals.csv and generates JSON data files for the dashboard.
Outputs:
  - data/clinics/index.json          (list of all clinics)
  - data/clinics/clinic-NNN.json     (detailed file per clinic, NNN = 001..439)
"""

import csv
import json
import os
import random
import math
from datetime import datetime, timedelta, timezone

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH    = "/Users/nirkosover/Library/Mobile Documents/com~apple~CloudDocs/Mine/Development/Claude code/Dentists/labeled-dentals.csv"
OUTPUT_DIR  = os.path.join(BASE_DIR, "data", "clinics")

# ── Constants ─────────────────────────────────────────────────────────────────
THEMES_13_WEEK = [
    "Foundation", "Oral Hygiene", "Meet the Team", "Smile Goals",
    "Kids Dentistry", "Promos & Offers", "Fun Facts", "Reviews Showcase",
    "Seasonal Care", "Culture & Community", "Education", "Summer Smiles",
    "Grand Recap"
]

CONTENT_TYPES   = ["A", "A", "A", "A", "A", "A", "A",   # ~67% A
                   "P", "P",                              # ~19% P (rounded from 2/10.7)
                   "R"]                                   # ~14% R

STATUS_WEIGHTS  = [                                       # (status, weight)
    ("published", 70),
    ("generated", 15),
    ("pending",   10),
    ("failed",     5),
]
STATUS_POOL = []
for s, w in STATUS_WEIGHTS:
    STATUS_POOL.extend([s] * w)

REEL_TOPICS = [
    "Before & After Transformation", "Meet Dr. {name}", "3 Signs You Need a Check-up",
    "Behind the Scenes at Our Clinic", "Patient Smile Story", "Top 5 Teeth-Whitening Tips",
    "Kids First Dentist Visit", "Emergency Dental FAQ", "How We Clean Your Teeth",
    "Why Flossing Actually Matters", "Invisalign vs. Braces", "Our Team in Action"
]

SEO_STATUSES = ["active", "paused", "planned"]

PRIMARY_COLORS = [
    "#2563eb", "#16a34a", "#dc2626", "#9333ea", "#0891b2",
    "#ea580c", "#0d9488", "#7c3aed", "#be185d", "#1d4ed8",
    "#15803d", "#b45309", "#0369a1", "#6d28d9", "#047857",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def safe_float(val, default=0.0):
    try:
        return float(val) if val and val.strip() else default
    except (ValueError, AttributeError):
        return default


def safe_int(val, default=0):
    try:
        return int(float(val)) if val and val.strip() else default
    except (ValueError, AttributeError):
        return default


def clean_address(raw):
    """Strip leading garbage characters (e.g. private-use Unicode) from address."""
    if not raw:
        return ""
    # Remove leading non-printable / private-use chars and extra whitespace
    cleaned = raw.strip()
    # Remove leading chars that are not standard printable text
    while cleaned and (ord(cleaned[0]) > 0xE000 or ord(cleaned[0]) < 0x20):
        cleaned = cleaned[1:]
    return cleaned.strip()


def random_hex_color(rng):
    r = rng.randint(30, 200)
    g = rng.randint(30, 200)
    b = rng.randint(30, 200)
    return f"#{r:02x}{g:02x}{b:02x}"


def generate_stories(rng, clinic_id):
    """Generate 90 story slots (30 weeks × 3 per week)."""
    stories = []
    # Start date: ~90 days ago
    base_date = datetime.now(timezone.utc) - timedelta(days=90)

    for day_idx in range(90):
        week_idx  = day_idx // 7
        theme     = THEMES_13_WEEK[week_idx % len(THEMES_13_WEEK)]
        slot_date = (base_date + timedelta(days=day_idx)).strftime("%Y-%m-%d")

        for slot in range(3):
            content_type = rng.choice(CONTENT_TYPES)
            # Earlier slots are more likely published; future slots pending/planned
            if day_idx < 70:
                status = rng.choice(STATUS_POOL)
            elif day_idx < 85:
                status = rng.choice(["pending", "generated", "generated"])
            else:
                status = "pending"

            story = {
                "id":          f"s{clinic_id}-{day_idx}-{slot}",
                "day":         day_idx + 1,
                "slot":        slot + 1,
                "date":        slot_date,
                "week":        week_idx + 1,
                "theme":       theme,
                "contentType": content_type,
                "status":      status,
                "caption":     f"{theme} – Day {day_idx+1} slot {slot+1}",
            }
            stories.append(story)

    return stories


def generate_reels(rng, clinic_id, clinic_name):
    """Generate 12 reel items (1 per week for 12 weeks)."""
    reels = []
    base_date = datetime.now(timezone.utc) - timedelta(weeks=12)

    for week in range(12):
        topic     = REEL_TOPICS[week % len(REEL_TOPICS)]
        topic_fmt = topic.replace("{name}", clinic_name.split()[0] if clinic_name else "Our Doctor")
        week_date = (base_date + timedelta(weeks=week)).strftime("%Y-%m-%d")

        if week < 8:
            status = rng.choice(["published", "published", "published", "generated"])
        elif week < 10:
            status = rng.choice(["generated", "pending"])
        else:
            status = "pending"

        views = rng.randint(800, 18000) if status == "published" else 0
        reel  = {
            "id":          f"r{clinic_id}-{week+1}",
            "week":        week + 1,
            "date":        week_date,
            "topic":       topic_fmt,
            "status":      status,
            "views":       views,
            "durationSec": rng.choice([15, 30, 45, 60]),
        }
        reels.append(reel)

    return reels


def generate_seo_channels(rng):
    channels = [
        {"channel": "blog",    "label": "Blog Posts",       "postsPlanned": 8},
        {"channel": "twitter", "label": "Twitter/X",        "postsPlanned": 15},
        {"channel": "reddit",  "label": "Reddit",           "postsPlanned": 4},
        {"channel": "quora",   "label": "Quora",            "postsPlanned": 4},
        {"channel": "gbp",     "label": "Google Business",  "postsPlanned": 8},
    ]
    forced_active = {"blog", "gbp"}
    result = []
    for ch in channels:
        published = rng.randint(0, ch["postsPlanned"])
        if ch["channel"] in forced_active:
            status = "active"
        else:
            status = rng.choice(SEO_STATUSES)
        result.append({
            "channel":        ch["channel"],
            "label":          ch["label"],
            "postsPlanned":   ch["postsPlanned"],
            "postsPublished": published,
            "status":         status,
        })
    return result


def generate_costs(rng):
    """3 months of cost data."""
    months = []
    base_month = datetime.now(timezone.utc).replace(day=1) - timedelta(days=60)
    for m in range(3):
        month_dt  = (base_month + timedelta(days=m * 30)).strftime("%Y-%m")
        stories   = round(rng.uniform(80, 160), 2)
        reels     = round(rng.uniform(40, 100), 2)
        seo       = round(rng.uniform(30, 80), 2)
        total     = round(stories + reels + seo, 2)
        months.append({
            "month":   month_dt,
            "stories": stories,
            "reels":   reels,
            "seo":     seo,
            "total":   total,
        })
    return months


def generate_onboarding(rng):
    items = [
        {"key": "logo",      "label": "Logo uploaded"},
        {"key": "colors",    "label": "Brand colors set"},
        {"key": "photos",    "label": "Photo vault (15+ photos)"},
        {"key": "tone",      "label": "Tone of voice defined"},
        {"key": "gbp",       "label": "Google Business connected"},
        {"key": "instagram", "label": "Instagram connected"},
        {"key": "approval",  "label": "Content approval flow set"},
    ]
    result = []
    for item in items:
        result.append({**item, "completed": rng.random() > 0.35})
    return result


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Read CSV
    print(f"Reading CSV from: {CSV_PATH}")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows   = list(reader)

    print(f"Loaded {len(rows)} rows")

    index_clinics = []
    now_iso       = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for i, row in enumerate(rows):
        clinic_id = i + 1
        rng       = random.Random(clinic_id)   # seeded by ID for reproducibility

        # ── Parse CSV fields ──────────────────────────────────────────────
        name         = (row.get("name") or "").strip()
        city         = (row.get("city") or "").strip()
        address      = clean_address(row.get("address") or "")
        phone        = (row.get("phone") or "").strip()
        website      = (row.get("website") or "").strip()
        rating       = safe_float(row.get("rating"), 0.0)
        review_count = safe_int(row.get("review_count"), 0)
        site_score   = safe_float(row.get("site_score"), 0.0)
        segment      = (row.get("segment") or "").strip()
        segment_name = (row.get("segment_name") or "").strip()

        # Try to coerce segment to int if possible, else keep as string
        try:
            segment_val = int(segment)
        except ValueError:
            segment_val = segment   # e.g. "4b", "3a"

        # ── Random but reproducible metrics ──────────────────────────────
        stories_completed = rng.randint(40, 80)
        reels_completed   = rng.randint(3, 8)
        seo_completed     = rng.randint(5, 15)
        onboarding_pct    = rng.randint(60, 100)

        # ── Index entry (lightweight) ─────────────────────────────────────
        index_entry = {
            "id":               clinic_id,
            "name":             name,
            "city":             city,
            "segment":          segment_val,
            "segmentName":      segment_name,
            "rating":           rating,
            "reviewCount":      review_count,
            "siteScore":        site_score,
            "storiesCompleted": stories_completed,
            "storiesTotal":     90,
            "reelsCompleted":   reels_completed,
            "reelsTotal":       12,
            "seoCompleted":     seo_completed,
            "seoTotal":         20,
            "onboardingPct":    onboarding_pct,
        }
        index_clinics.append(index_entry)

        # ── Detailed clinic file ──────────────────────────────────────────
        primary_color = rng.choice(PRIMARY_COLORS)
        onboarding    = generate_onboarding(rng)
        stories       = generate_stories(rng, clinic_id)
        reels         = generate_reels(rng, clinic_id, name)
        seo_channels  = generate_seo_channels(rng)
        costs         = generate_costs(rng)

        clinic_detail = {
            "id":           clinic_id,
            "name":         name,
            "city":         city,
            "address":      address,
            "phone":        phone,
            "website":      website,
            "segment":      segment_val,
            "segmentName":  segment_name,
            "rating":       rating,
            "reviewCount":  review_count,
            "siteScore":    site_score,
            "colors": {
                "primary": primary_color,
                "accent":  "#e8a849",
            },
            "onboarding":   onboarding,
            "stories":      stories,
            "reels":        reels,
            "seoChannels":  seo_channels,
            "costs":        costs,
        }

        out_path = os.path.join(OUTPUT_DIR, f"clinic-{clinic_id:03d}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(clinic_detail, f, ensure_ascii=False, indent=2)

        if clinic_id % 50 == 0 or clinic_id == len(rows):
            print(f"  Written {clinic_id}/{len(rows)}: {out_path}")

    # ── Write index ───────────────────────────────────────────────────────
    index = {
        "lastUpdated":  now_iso,
        "totalClinics": len(rows),
        "clinics":      index_clinics,
    }
    index_path = os.path.join(OUTPUT_DIR, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"\nDone.")
    print(f"  Index  → {index_path}")
    print(f"  Clinics → {OUTPUT_DIR}/clinic-001.json … clinic-{len(rows):03d}.json")
    print(f"  Total files written: {len(rows) + 1}")


if __name__ == "__main__":
    main()
