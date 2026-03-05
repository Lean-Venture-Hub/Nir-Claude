#!/usr/bin/env python3
"""
Step 5: Segment Labeling for Charlotte Metro Dentists
Reads enriched CSV, applies segmentation logic, outputs labeled-dentals.csv.

Usage:
  python3 05_label_segments.py
"""

import csv
import os
import sys
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(SCRIPT_DIR, "enriched-clinics.csv")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "labeled-dentals.csv")


def assign_segment(row):
    rating_str = row.get("rating", "").strip()
    review_str = row.get("review_count", "").strip()
    website = row.get("website", "").strip()

    try:
        rating = float(rating_str)
    except (ValueError, TypeError):
        rating = None

    try:
        reviews = int(review_str.replace(",", ""))
    except (ValueError, TypeError):
        reviews = 0

    has_website = bool(website)

    if rating is None:
        return "5", "Digitally Absent"

    if rating >= 4.0:
        if has_website:
            if reviews >= 20:
                return "1", "Leaky Funnel"
            else:
                return "2", "Warm Digital, No Proof"
        else:
            if reviews < 3:
                return "4", "Invisible Good"
            elif reviews <= 10:
                return "4a", "Invisible Good - Some Reviews"
            else:
                return "4b", "Invisible Good - High Reviews"
    else:
        if reviews < 3:
            return "3", "Reputation Rescue"
        elif reviews <= 10:
            return "3a", "Reputation Rescue - Some Reviews"
        else:
            return "3b", "Reputation Rescue - High Reviews"


def main():
    if not os.path.exists(INPUT_CSV):
        print(f"ERROR: Input file not found: {INPUT_CSV}")
        print("Run 04_enrich_websites.py first.")
        sys.exit(1)

    rows = []
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        input_fields = reader.fieldnames
        for row in reader:
            rows.append(row)

    print(f"Loaded {len(rows)} clinics from {INPUT_CSV}")

    segment_counts = Counter()
    for row in rows:
        segment, segment_name = assign_segment(row)
        row["segment"] = segment
        row["segment_name"] = segment_name
        segment_counts[f"{segment} - {segment_name}"] += 1

    output_fields = list(input_fields) + ["segment", "segment_name"]
    seen = set()
    output_fields = [f for f in output_fields if f not in seen and not seen.add(f)]

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=output_fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"\nSegment Distribution:")
    print(f"{'Segment':<40} {'Count':>6} {'%':>6}")
    print("-" * 54)
    for seg, count in sorted(segment_counts.items()):
        pct = count / len(rows) * 100
        print(f"{seg:<40} {count:>6} {pct:>5.1f}%")
    print("-" * 54)
    print(f"{'TOTAL':<40} {len(rows):>6}")
    print(f"\nOutput: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
