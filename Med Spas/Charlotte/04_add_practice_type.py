#!/usr/bin/env python3
"""
Add practice_type column (Solo / Group) to labeled-medspas.csv.
Uses: doctor_count from enrichment + name patterns.
No NPI dependency (med spas don't have NPI registry).
"""

import csv
import os
import re
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LABELED_CSV = os.path.join(SCRIPT_DIR, "labeled-medspas.csv")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "labeled-medspas.csv")  # overwrite in place


def classify_practice(row):
    # 1. Check doctor_count from enrichment
    dc = row.get("doctor_count", "").strip()
    if dc and dc != "0":
        try:
            count = int(dc)
            if count >= 2:
                return "Group", f"group ({count} providers from website)"
            elif count == 1:
                return "Solo", "solo (1 provider from website)"
        except ValueError:
            pass

    # 2. Name pattern matching
    name = row.get("name", "").lower()

    group_signals = [
        "center", "clinic", "studio", "aesthetics", "wellness",
        "beauty", "spa", "& spa", "med spa", "laser", "medspa",
        "medical spa", "rejuvenation", "skin care", "skincare",
    ]
    solo_signals = ["dr.", "dr ", "md", "do", "m.d.", "d.o."]

    is_group_name = any(sig in name for sig in group_signals)
    is_solo_name = any(sig in name for sig in solo_signals) and not is_group_name

    if is_group_name:
        return "Group", "group (name pattern)"
    elif is_solo_name:
        return "Solo", "solo (name pattern)"

    return "Unknown", ""


def main():
    print("Classifying med spa practice types...")

    rows = []
    with open(LABELED_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames)
        for row in reader:
            rows.append(row)

    print(f"Loaded {len(rows)} med spas")

    if "practice_type" not in fields:
        fields.append("practice_type")

    results = Counter()
    for row in rows:
        ptype, detail = classify_practice(row)
        row["practice_type"] = ptype
        results[ptype] += 1

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"\nPractice Type Distribution:")
    for ptype, count in results.most_common():
        print(f"  {ptype}: {count} ({count*100//len(rows)}%)")
    print(f"  Total: {len(rows)}")
    print(f"\nOutput: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
