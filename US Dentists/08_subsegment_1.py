#!/usr/bin/env python3
"""
Step 8: Sub-segment Segment 1 (Leaky Funnel) into 1a, 1b, 1.
Modifies labeled-dentals.csv in place.

Sub-segments:
  1a — No online booking + site score < 6 + Group practice (hottest leads)
  1b — Aging/Stale reviews + no social media
  1  — All remaining Segment 1 (good digital presence, lower urgency)

Usage:
  python3 08_subsegment_1.py                          # Run on current folder
  python3 08_subsegment_1.py --city=Phoenix            # Run on specific city
  python3 08_subsegment_1.py --all                     # Run on all city folders
"""

import csv
import os
import sys
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def subsegment_city(city_dir):
    csv_path = os.path.join(city_dir, "labeled-dentals.csv")
    if not os.path.exists(csv_path):
        print(f"  SKIP: {csv_path} not found")
        return

    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames)
        for row in reader:
            rows.append(row)

    counts = Counter()
    for row in rows:
        if row.get("segment") != "1":
            counts[row.get("segment", "")] += 1
            continue

        # Parse fields
        has_booking = row.get("has_online_booking", "").strip().lower() == "yes"
        try:
            site_score = int(row.get("site_score", "0"))
        except ValueError:
            site_score = 0
        practice_type = row.get("practice_type", "").strip()
        review_recency = row.get("review_recency", "").strip()
        has_social = bool(
            row.get("facebook_url", "").strip() or
            row.get("instagram_url", "").strip() or
            row.get("tiktok_url", "").strip()
        )

        # 1a: No booking + low site score + Group (highest priority)
        if not has_booking and site_score < 6 and practice_type == "Group":
            row["segment"] = "1a"
            row["segment_name"] = "Leaky Funnel - No Booking"
            counts["1a"] += 1

        # 1b: Aging/Stale reviews + no social
        elif review_recency in ("Aging", "Stale") and not has_social:
            row["segment"] = "1b"
            row["segment_name"] = "Leaky Funnel - Aging Reviews"
            counts["1b"] += 1

        # 1: Everything else stays as Leaky Funnel
        else:
            counts["1"] += 1

    # Write back
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    # Print summary
    total = len(rows)
    for seg in sorted(counts.keys()):
        c = counts[seg]
        print(f"  {seg:>5}: {c:>5} ({c*100//total}%)")
    print(f"  Total: {total}")


def main():
    run_all = "--all" in sys.argv
    target_city = None
    for arg in sys.argv:
        if arg.startswith("--city="):
            target_city = arg.split("=")[1]

    if run_all:
        # Find all city folders with labeled-dentals.csv
        base = SCRIPT_DIR
        cities = []
        for name in sorted(os.listdir(base)):
            city_dir = os.path.join(base, name)
            if os.path.isdir(city_dir) and os.path.exists(os.path.join(city_dir, "labeled-dentals.csv")):
                cities.append((name, city_dir))

        print(f"Sub-segmenting Segment 1 across {len(cities)} cities\n")
        for name, city_dir in cities:
            print(f"=== {name} ===")
            subsegment_city(city_dir)
            print()

    elif target_city:
        city_dir = os.path.join(SCRIPT_DIR, target_city)
        print(f"=== {target_city} ===")
        subsegment_city(city_dir)

    else:
        # Run on current directory
        print(f"=== {os.path.basename(SCRIPT_DIR)} ===")
        subsegment_city(SCRIPT_DIR)


if __name__ == "__main__":
    main()
