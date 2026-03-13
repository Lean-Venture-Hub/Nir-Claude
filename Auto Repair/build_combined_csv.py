"""
Combines Apify + Google Places API data into a single deduped CSV
with segment classification adapted from the Dentists pipeline.

Segments for Auto Repair (adapted from Dentists):
  S1 - Leaky Funnel:       Has website, good rating, but very few reviews (<20)
  S2 - Warm Digital:        Has website, decent site, but low reviews — already believes in digital
  S3 - Reputation Rescue:   Has website, low rating (<4.0), few reviews — fixable
  S4 - No Website:          No website (base)
  S4a - No Website + Some:  No website, >3 reviews
  S4b - No Website + Good:  No website, >10 reviews — strongest no-website lead
  S5 - Digitally Absent:    No website, no reviews or very few — coldest
"""

import csv
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Chains to exclude
CHAIN_KEYWORDS = [
    "firestone", "jiffy lube", "midas", "pep boys", "pepboys",
    "valvoline", "goodyear", "discount tire", "maaco", "meineke",
    "aamco", "safelite", "caliber collision", "service king",
    "take 5", "ntb ", "national tire", "brake masters", "sun devil",
    "big o tires", "les schwab", "christian brothers", "greulich",
    "wilhelm", "honest-1", "precision tune",
]

OUTPUT_COLUMNS = [
    "segment", "segment_name",
    "name", "address", "city", "state", "phone", "website",
    "rating", "review_count", "categories",
    "hours", "google_maps_url", "neighborhood",
    "has_website", "search_term", "vertical", "scraped_at", "place_id",
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


def is_chain(name):
    name_lower = name.lower()
    return any(kw in name_lower for kw in CHAIN_KEYWORDS)


def has_website(website):
    w = (website or "").strip().lower()
    if not w or not w.startswith("http"):
        return False
    if "facebook.com" in w:
        return False
    return True


def assign_segment(row):
    """Assign segment. Returns (num, name) or None."""
    rating = safe_float(row.get("rating"))
    review_count = safe_int(row.get("review_count"))
    website = row.get("website", "")
    has_site = has_website(website)
    name = row.get("name", "")

    # Exclusions
    if is_chain(name):
        return None
    if rating < 3.0 and review_count > 20:
        return None  # truly bad

    # S1 - Leaky Funnel: has website, good rating, few reviews
    if has_site and review_count < 20 and rating >= 4.0:
        return (1, "Leaky Funnel")

    # S2 - Warm Digital: has website, moderate reviews, good rating
    if has_site and 20 <= review_count < 50 and rating >= 4.0:
        return (2, "Warm Digital")

    # S3 - Reputation Rescue: has website, low rating, few reviews (fixable)
    if has_site and rating < 4.0 and review_count < 15:
        return (3, "Reputation Rescue")

    # S4b - No Website + Good: >10 reviews (check first, most qualified)
    if not has_site and review_count > 10:
        return ("4b", "No Website + Good")

    # S4a - No Website + Some: >3 reviews
    if not has_site and review_count > 3:
        return ("4a", "No Website + Some")

    # S4 - No Website: base case
    if not has_site:
        return (4, "No Website")

    return None


def parse_apify_row(row):
    """Convert Apify CSV row to standard format."""
    # Parse opening hours from flat columns
    hours_parts = []
    for i in range(7):
        day = row.get(f"openingHours/{i}/day", "")
        hrs = row.get(f"openingHours/{i}/hours", "")
        if day and hrs:
            hours_parts.append(f"{day}: {hrs}")
    hours_str = " | ".join(hours_parts)

    # Parse categories
    cats = []
    for i in range(10):
        c = row.get(f"categories/{i}", "")
        if c:
            cats.append(c)

    website = row.get("website", "")

    return {
        "name": row.get("title", ""),
        "address": row.get("address", ""),
        "city": row.get("city", ""),
        "state": row.get("state", ""),
        "phone": row.get("phone", ""),
        "website": website,
        "rating": row.get("totalScore", ""),
        "review_count": row.get("reviewsCount", "0"),
        "categories": ", ".join(cats),
        "hours": hours_str,
        "google_maps_url": row.get("url", ""),
        "neighborhood": row.get("neighborhood", ""),
        "has_website": "yes" if has_website(website) else "no",
        "search_term": row.get("searchString", ""),
        "vertical": "auto_repair",
        "scraped_at": row.get("scrapedAt", ""),
        "place_id": row.get("placeId", ""),
    }


def parse_old_row(row):
    """Convert old Google Places API row to standard format."""
    return {
        "name": row.get("name", ""),
        "address": row.get("address", ""),
        "city": row.get("city", ""),
        "state": row.get("state", ""),
        "phone": row.get("phone", ""),
        "website": row.get("website", ""),
        "rating": row.get("rating", ""),
        "review_count": row.get("review_count", "0"),
        "categories": row.get("categories", ""),
        "hours": row.get("hours", ""),
        "google_maps_url": row.get("google_maps_url", ""),
        "neighborhood": "",
        "has_website": row.get("has_website", ""),
        "search_term": row.get("search_term", ""),
        "vertical": "auto_repair",
        "scraped_at": row.get("scraped_at", ""),
        "place_id": row.get("place_id", ""),
    }


def main():
    auto_dir = BASE_DIR / "Auto Repair"
    all_rows = []
    seen_ids = set()

    # Load Apify files first (richer data)
    for fname in ["apify-houston-tx.csv", "apify-phoenix-az.csv"]:
        fpath = auto_dir / fname
        if not fpath.exists():
            continue
        with open(fpath, "r", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                pid = row.get("placeId", "")
                if pid and pid not in seen_ids:
                    seen_ids.add(pid)
                    all_rows.append(parse_apify_row(row))

    # Load old Google Places API data (fill gaps)
    old_files = ["houston-tx.csv", "phoenix-az.csv", "all-auto-repair.csv"]
    for fname in old_files:
        fpath = auto_dir / fname
        if not fpath.exists():
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                pid = row.get("place_id", "")
                if pid and pid not in seen_ids:
                    seen_ids.add(pid)
                    all_rows.append(parse_old_row(row))

    # Assign segments
    output = []
    for row in all_rows:
        result = assign_segment(row)
        if result is None:
            row["segment"] = 0
            row["segment_name"] = "Excluded (Chain/Bad)"
        else:
            seg_num, seg_name = result
            row["segment"] = seg_num
            row["segment_name"] = seg_name
        output.append(row)

    # Sort by segment, then rating desc
    output.sort(key=lambda r: (str(r["segment"]), -safe_float(r.get("rating"))))

    # Write combined CSV
    out_path = auto_dir / "apify-all-auto-repair.csv"
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(output)

    # Summary
    from collections import Counter
    seg_counts = Counter(f"S{r['segment']} - {r['segment_name']}" for r in output)

    excluded = sum(1 for r in output if r["segment"] == 0)
    leads = len(output) - excluded
    print(f"Total unique businesses: {len(all_rows)}")
    print(f"S0 Excluded (chains/bad): {excluded}")
    print(f"Classified leads (S1-S5): {leads}")
    print(f"\nSegments:")
    for seg in sorted(seg_counts.keys()):
        print(f"  {seg}: {seg_counts[seg]}")
    print(f"\nSaved → {out_path}")


if __name__ == "__main__":
    main()
