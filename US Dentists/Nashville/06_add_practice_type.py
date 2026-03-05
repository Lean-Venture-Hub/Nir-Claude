#!/usr/bin/env python3
"""
Add practice_type column (Solo / Group) to labeled-dentals.csv.
Uses: doctor_count from enrichment + NPI address clustering.
Nashville Metro version.
"""

import csv
import os
import re
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LABELED_CSV = os.path.join(SCRIPT_DIR, "labeled-dentals.csv")
NPI_CSV = os.path.join(SCRIPT_DIR, "npi-master-list.csv")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "labeled-dentals.csv")  # overwrite in place


def normalize_address(addr):
    """Normalize address for fuzzy matching."""
    if not addr:
        return ""
    a = addr.upper().strip()
    # Remove unit/suite/floor info for grouping
    a = re.sub(r'\b(STE|SUITE|UNIT|APT|FLOOR|FL|RM|ROOM|#)\s*\S+', '', a)
    # Remove zip+4
    a = re.sub(r'\b\d{5}-\d{4}\b', lambda m: m.group()[:5], a)
    # Remove country
    a = re.sub(r',?\s*(UNITED STATES|USA|US)\s*$', '', a)
    # Normalize common abbreviations
    a = a.replace(' STREET', ' ST').replace(' AVENUE', ' AVE').replace(' BOULEVARD', ' BLVD')
    a = a.replace(' DRIVE', ' DR').replace(' ROAD', ' RD').replace(' PLACE', ' PL')
    a = a.replace(' EAST ', ' E ').replace(' WEST ', ' W ')
    a = a.replace(' NORTH ', ' N ').replace(' SOUTH ', ' S ')
    # Remove extra whitespace
    a = re.sub(r'\s+', ' ', a).strip()
    # Remove trailing comma and city/state for matching on street only
    parts = a.split(',')
    if parts:
        return parts[0].strip()
    return a


def build_npi_address_index(npi_csv):
    """
    Build index: normalized_street_address -> count of unique NPI dentists.
    Multiple dentists at same address = group practice.
    """
    addr_dentists = defaultdict(set)  # address -> set of NPI numbers

    with open(npi_csv, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            addr = row.get("address", "")
            npi = row.get("npi", "")
            if not addr or not npi:
                continue
            norm = normalize_address(addr)
            if norm:
                addr_dentists[norm].add(npi)

    # Convert to counts
    return {addr: len(npis) for addr, npis in addr_dentists.items()}


def classify_practice(row, npi_counts):
    """Determine Solo or Group based on available data."""
    # 1. Use doctor_count from enrichment if available
    dc = row.get("doctor_count", "").strip()
    if dc and dc != "0":
        try:
            count = int(dc)
            if count >= 2:
                return "Group", f"group ({count} doctors from website)"
            else:
                # 1 doctor found on site, but check NPI too
                pass
        except ValueError:
            pass

    # 2. Check NPI address clustering
    addr = row.get("address", "")
    norm_addr = normalize_address(addr)
    npi_count = npi_counts.get(norm_addr, 0)

    # Try partial match if exact fails
    if npi_count == 0 and norm_addr:
        # Extract just the street number + street name
        street_match = re.match(r'^(\d+\s+\S+(?:\s+\S+)?)', norm_addr)
        if street_match:
            street_prefix = street_match.group(1)
            for npi_addr, count in npi_counts.items():
                if npi_addr.startswith(street_prefix):
                    npi_count = max(npi_count, count)

    if npi_count >= 3:
        return "Group", f"group ({npi_count} NPIs at address)"
    elif npi_count == 2:
        return "Group", f"group (2 NPIs at address)"

    # 3. Use doctor_count = 1 from enrichment
    if dc == "1":
        return "Solo", "solo (1 doctor from website)"

    # 4. Check name patterns
    name = row.get("name", "").lower()
    group_signals = ["group", "center", "associates", "partners", "clinic", "family",
                     "dental care", "dental center", "dental arts", "dental studio",
                     "dental office", "dental practice", "dental health", "smiles",
                     "oral surgery", "orthodontics"]
    solo_signals = ["dr.", "dr ", "d.d.s", "dds", "dmd", "d.m.d"]

    is_group_name = any(sig in name for sig in group_signals)
    is_solo_name = any(sig in name for sig in solo_signals) and not is_group_name

    if is_group_name:
        return "Group", "group (name pattern)"
    elif is_solo_name:
        return "Solo", "solo (name pattern)"

    # 5. Default: unknown — classify by NPI count
    if npi_count == 1:
        return "Solo", "solo (1 NPI at address)"

    return "Unknown", ""


def main():
    print("Building NPI address index...")
    npi_counts = build_npi_address_index(NPI_CSV)
    print(f"  {len(npi_counts)} unique addresses in NPI data")

    # Distribution of dentists per address
    dist = Counter(npi_counts.values())
    print(f"  NPIs per address distribution: {dict(sorted(dist.items())[:10])}")

    print(f"\nClassifying practices...")
    rows = []
    with open(LABELED_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames)
        for row in reader:
            rows.append(row)

    # Add new column
    if "practice_type" not in fields:
        fields.append("practice_type")

    results = Counter()
    for row in rows:
        ptype, detail = classify_practice(row, npi_counts)
        row["practice_type"] = ptype
        results[ptype] += 1

    # Write output
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
