#!/usr/bin/env python3
"""Generate a single outreach CSV with segment assignments from the enriched dental clinics data."""

import csv
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(SCRIPT_DIR, "gush-dan-dental-clinics.csv")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "outreach-leads.csv")

# Chain keywords to exclude
CHAIN_KEYWORDS = [
    "מכבידנט", "כללית סמייל", "הכתר", "אלפא דנט", "דנטל פלוס",
    "קופת חולים", "מאוחדת", "לאומית", "רשת שיניים", "dental network",
    "סמייל", "smile center", "אורתודנטיה בע\"מ"
]

# Non-dental keywords to exclude
NON_DENTAL_KEYWORDS = [
    "וטרינר", "מעבדת שיניים", "מעבדה", "הדמיה", "רנטגן", "צילום",
    "עורך דין", "רואה חשבון", "יועץ", "vet", "lab", "imaging", "x-ray"
]


def safe_float(val, default=0.0):
    try:
        return float(val) if val else default
    except (ValueError, TypeError):
        return default


def safe_int(val, default=0):
    try:
        return int(val) if val else default
    except (ValueError, TypeError):
        return default


def is_chain(row):
    name_lower = row.get("name", "").lower()
    for kw in CHAIN_KEYWORDS:
        if kw in name_lower:
            return True
    return False


def is_non_dental(row):
    name_lower = row.get("name", "").lower()
    cats = row.get("categories", "").lower()
    combined = name_lower + " " + cats
    for kw in NON_DENTAL_KEYWORDS:
        if kw in combined:
            return True
    return False


def has_website(row):
    w = row.get("website", "").strip()
    return w.startswith("http")


def has_social(row):
    return bool(row.get("facebook_url", "").strip() or
                row.get("instagram_url", "").strip() or
                row.get("tiktok_url", "").strip())


def has_booking(row):
    comments = row.get("comments", "").lower()
    return "booking" in comments


def is_digitally_mature(row):
    """Already invested heavily in digital — low need for our services."""
    site_score = safe_int(row.get("site_score"))
    review_count = safe_int(row.get("review_count"))
    return site_score >= 7 and has_social(row) and has_booking(row) and review_count >= 30


def assign_segment(row):
    """Assign a clinic to a single segment (mutually exclusive). Returns (num, name) or None."""
    rating = safe_float(row.get("rating"))
    review_count = safe_int(row.get("review_count"))
    site_score = safe_int(row.get("site_score"))

    # --- Exclusions ---
    if is_chain(row):
        return None
    if is_non_dental(row):
        return None
    if rating < 3.5 and review_count > 30:
        return None  # truly bad — marketing won't help
    if is_digitally_mature(row):
        return None  # already invested, low need

    # --- Assignment (checked in warmth order, first match wins) ---

    # Segment 2 first (warmest): website + good rating + very few reviews
    # These already believe in digital but have the clearest gap
    if has_website(row) and site_score > 0 and review_count < 20 and rating >= 4.0:
        return (2, "Warm Digital, No Proof")

    # Segment 1: good site + good rating + few reviews (20-29 range after S2 takes <20)
    if site_score >= 5 and review_count < 30 and rating >= 4.0:
        return (1, "Leaky Funnel")

    # Segment 3: low rating but fixable (few reviews means we can dilute)
    if rating < 4.0 and review_count < 15:
        return (3, "Reputation Rescue")

    # Segment 4: great rating, no/bad digital presence
    if rating >= 4.5 and site_score <= 3:
        return (4, "Invisible Good Clinics")

    # Segment 5: no website, no social — coldest
    if not has_website(row) and not has_social(row):
        return (5, "Digitally Absent")

    return None


def main():
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    # Outreach columns: segment first, then useful outreach data
    outreach_fields = [
        "segment", "segment_name",
        "name", "city", "phone", "website",
        "rating", "review_count", "site_score",
        "facebook_url", "instagram_url",
        "easy_url", "easy_score",
        "doctor_count", "google_maps_url", "comments"
    ]

    leads = []
    for row in all_rows:
        result = assign_segment(row)
        if result is None:
            continue
        seg_num, seg_name = result
        lead = {"segment": seg_num, "segment_name": seg_name}
        for col in outreach_fields:
            if col not in ("segment", "segment_name"):
                lead[col] = row.get(col, "")
        leads.append(lead)

    # Sort by segment number, then by rating descending within each segment
    leads.sort(key=lambda r: (r["segment"], -safe_float(r.get("rating"))))

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=outreach_fields)
        writer.writeheader()
        writer.writerows(leads)

    # Print summary
    from collections import Counter
    seg_counts = Counter(r["segment_name"] for r in leads)
    print(f"Total leads: {len(leads)}")
    for seg_num in range(1, 6):
        for name, count in seg_counts.items():
            matching = [r for r in leads if r["segment_name"] == name and r["segment"] == seg_num]
            if matching:
                print(f"  Segment {seg_num} ({name}): {len(matching)}")
    print(f"\nSaved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
