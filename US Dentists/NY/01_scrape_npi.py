#!/usr/bin/env python3
"""
Step 1: NPI Registry Scraper for NYC Dentists
Queries the free federal NPI API for every licensed dentist in NYC.
No auth required. No cost.

Usage:
  python3 01_scrape_npi.py          # Full run
  python3 01_scrape_npi.py --test   # First borough only, limit 50
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "npi-master-list.csv")
API_URL = "https://npiregistry.cms.hhs.gov/api/"

CSV_FIELDS = [
    "npi", "first_name", "last_name", "credential", "organization_name",
    "dba_name", "is_organization", "address", "city", "state", "zip", "phone",
    "taxonomy_code", "specialty", "enumeration_date", "last_updated",
]

# NYC boroughs + Queens neighborhoods (Queens uses neighborhood names in postal addresses)
QUERIES = [
    # Manhattan
    {"city": "New York", "state": "NY", "label": "Manhattan"},
    # Brooklyn
    {"city": "Brooklyn", "state": "NY", "label": "Brooklyn"},
    # Bronx
    {"city": "Bronx", "state": "NY", "label": "Bronx"},
    # Staten Island
    {"city": "Staten Island", "state": "NY", "label": "Staten Island"},
    # Queens — uses neighborhood names in addresses
    {"city": "Queens", "state": "NY", "label": "Queens (general)"},
    {"city": "Flushing", "state": "NY", "label": "Queens - Flushing"},
    {"city": "Jamaica", "state": "NY", "label": "Queens - Jamaica"},
    {"city": "Astoria", "state": "NY", "label": "Queens - Astoria"},
    {"city": "Long Island City", "state": "NY", "label": "Queens - LIC"},
    {"city": "Bayside", "state": "NY", "label": "Queens - Bayside"},
    {"city": "Forest Hills", "state": "NY", "label": "Queens - Forest Hills"},
    {"city": "Rego Park", "state": "NY", "label": "Queens - Rego Park"},
    {"city": "Elmhurst", "state": "NY", "label": "Queens - Elmhurst"},
    {"city": "Corona", "state": "NY", "label": "Queens - Corona"},
    {"city": "Woodside", "state": "NY", "label": "Queens - Woodside"},
    {"city": "Jackson Heights", "state": "NY", "label": "Queens - Jackson Heights"},
    {"city": "Ridgewood", "state": "NY", "label": "Queens - Ridgewood"},
    {"city": "Ozone Park", "state": "NY", "label": "Queens - Ozone Park"},
    {"city": "Howard Beach", "state": "NY", "label": "Queens - Howard Beach"},
    {"city": "Fresh Meadows", "state": "NY", "label": "Queens - Fresh Meadows"},
    {"city": "Kew Gardens", "state": "NY", "label": "Queens - Kew Gardens"},
    {"city": "Whitestone", "state": "NY", "label": "Queens - Whitestone"},
    {"city": "College Point", "state": "NY", "label": "Queens - College Point"},
    {"city": "Woodhaven", "state": "NY", "label": "Queens - Woodhaven"},
    {"city": "Sunnyside", "state": "NY", "label": "Queens - Sunnyside"},
    {"city": "Maspeth", "state": "NY", "label": "Queens - Maspeth"},
    {"city": "Middle Village", "state": "NY", "label": "Queens - Middle Village"},
    {"city": "Glen Oaks", "state": "NY", "label": "Queens - Glen Oaks"},
    {"city": "Little Neck", "state": "NY", "label": "Queens - Little Neck"},
    {"city": "Far Rockaway", "state": "NY", "label": "Queens - Far Rockaway"},
    {"city": "Rockaway Park", "state": "NY", "label": "Queens - Rockaway Park"},
    {"city": "South Richmond Hill", "state": "NY", "label": "Queens - S. Richmond Hill"},
    {"city": "Richmond Hill", "state": "NY", "label": "Queens - Richmond Hill"},
    {"city": "Springfield Gardens", "state": "NY", "label": "Queens - Springfield Gardens"},
    {"city": "Cambria Heights", "state": "NY", "label": "Queens - Cambria Heights"},
    {"city": "Saint Albans", "state": "NY", "label": "Queens - St. Albans"},
    {"city": "Hollis", "state": "NY", "label": "Queens - Hollis"},
    {"city": "Bellerose", "state": "NY", "label": "Queens - Bellerose"},
    {"city": "Floral Park", "state": "NY", "label": "Queens - Floral Park"},
]

# Dental taxonomy codes (all start with 122)
DENTAL_TAXONOMY_PREFIX = "122"


def query_npi(city, state, taxonomy_desc="Dentist", limit=200, skip=0):
    """Query NPI Registry API. Returns (results_list, result_count)."""
    params = {
        "version": "2.1",
        "city": city,
        "state": state,
        "taxonomy_description": taxonomy_desc,
        "limit": str(limit),
        "skip": str(skip),
    }
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return data.get("results", []), data.get("result_count", 0)


def parse_npi_record(record):
    """Parse a single NPI API result into a flat dict."""
    basic = record.get("basic", {})
    addresses = record.get("addresses", [])
    taxonomies = record.get("taxonomies", [])
    other_names = record.get("other_names", [])

    # Determine if individual or organization (top-level field)
    enum_type = record.get("enumeration_type", "")
    is_org = enum_type == "NPI-2"

    # Get practice location address (LOCATION preferred over MAILING)
    practice_addr = {}
    for addr in addresses:
        if addr.get("address_purpose") == "LOCATION":
            practice_addr = addr
            break
    if not practice_addr and addresses:
        practice_addr = addresses[0]

    # Get primary taxonomy
    primary_tax = {}
    for tax in taxonomies:
        if tax.get("primary"):
            primary_tax = tax
            break
    if not primary_tax and taxonomies:
        primary_tax = taxonomies[0]

    # Get DBA (Doing Business As) name
    dba_name = ""
    for on in other_names:
        if on.get("code") == "3":  # code 3 = Doing Business As
            dba_name = on.get("organization_name", "")
            break

    # Handle names differently for individuals vs organizations
    if is_org:
        first_name = basic.get("authorized_official_first_name", "")
        last_name = basic.get("authorized_official_last_name", "")
        credential = basic.get("authorized_official_credential", "")
        org_name = basic.get("organization_name", "")
    else:
        first_name = basic.get("first_name", "")
        last_name = basic.get("last_name", "")
        credential = basic.get("credential", "")
        org_name = ""

    return {
        "npi": str(record.get("number", "")),
        "first_name": first_name,
        "last_name": last_name,
        "credential": credential,
        "organization_name": org_name,
        "dba_name": dba_name,
        "is_organization": "yes" if is_org else "no",
        "address": practice_addr.get("address_1", ""),
        "city": practice_addr.get("city", ""),
        "state": practice_addr.get("state", ""),
        "zip": practice_addr.get("postal_code", "")[:5],
        "phone": practice_addr.get("telephone_number", ""),
        "taxonomy_code": primary_tax.get("code", ""),
        "specialty": primary_tax.get("desc", ""),
        "enumeration_date": basic.get("enumeration_date", ""),
        "last_updated": basic.get("last_updated", ""),
    }


def main():
    test_mode = "--test" in sys.argv

    print("=" * 60)
    print("NPI Registry Scraper — NYC Dentists")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if test_mode:
        print("TEST MODE: first query only, limit 50")
    print("=" * 60)

    # Track seen NPIs for dedup
    seen_npis = set()

    # Load existing if resuming
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                seen_npis.add(row.get("npi", ""))
        print(f"Loaded {len(seen_npis)} existing NPIs from CSV")

    # Open CSV for appending
    file_exists = os.path.exists(OUTPUT_CSV) and os.path.getsize(OUTPUT_CSV) > 0
    csv_file = open(OUTPUT_CSV, "a", encoding="utf-8", newline="")
    writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
    if not file_exists:
        writer.writeheader()

    queries = QUERIES[:1] if test_mode else QUERIES
    total_new = 0
    total_dupes = 0

    for qi, q in enumerate(queries):
        city = q["city"]
        state = q["state"]
        label = q["label"]
        print(f"\n[{qi+1}/{len(queries)}] {label} ({city}, {state})")

        skip = 0
        limit = 50 if test_mode else 200
        query_new = 0
        query_total = 0

        max_per_query = 5000  # Safety cap to avoid infinite loops

        while True:
            try:
                results, result_count = query_npi(city, state, limit=limit, skip=skip)
            except Exception as e:
                print(f"  ERROR at skip={skip}: {e}")
                break

            if not results:
                break

            for record in results:
                parsed = parse_npi_record(record)

                # Skip non-dental taxonomies (filters out students, etc.)
                if parsed["taxonomy_code"] and not parsed["taxonomy_code"].startswith(DENTAL_TAXONOMY_PREFIX):
                    continue

                # Dedup by NPI
                if parsed["npi"] in seen_npis:
                    total_dupes += 1
                    continue

                seen_npis.add(parsed["npi"])
                writer.writerow(parsed)
                query_new += 1
                total_new += 1

            query_total += len(results)
            print(f"  Fetched {query_total} — {query_new} new dentists so far", end="\r")

            # Exit when fewer results than requested (end of data)
            if len(results) < limit:
                break

            # Safety cap
            if query_total >= max_per_query:
                print(f"\n  Safety cap reached ({max_per_query})")
                break

            skip += limit
            time.sleep(0.3)  # Polite delay

            if test_mode:
                break

        print(f"  {label}: {query_new} new dentists (total queried: {query_total})")
        csv_file.flush()  # Save after each borough

    csv_file.close()

    print(f"\n{'=' * 60}")
    print(f"DONE!")
    print(f"New dentists added: {total_new}")
    print(f"Duplicates skipped: {total_dupes}")
    print(f"Total unique NPIs: {len(seen_npis)}")
    print(f"Output: {OUTPUT_CSV}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
