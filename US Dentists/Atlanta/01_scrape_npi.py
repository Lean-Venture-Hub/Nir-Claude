#!/usr/bin/env python3
"""
Step 1: NPI Registry Scraper for Atlanta Metro Dentists
Queries the free federal NPI API for every licensed dentist in Atlanta metro.

Usage:
  python3 01_scrape_npi.py          # Full run
  python3 01_scrape_npi.py --test   # First query only, limit 50
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

# Atlanta metro: Fulton, DeKalb, Gwinnett, Cobb, Clayton, Cherokee,
# Forsyth, Henry, Douglas, Rockdale, Fayette, Paulding, Carroll, Bartow, etc.
QUERIES = [
    # Core Atlanta / Fulton County
    {"city": "Atlanta", "state": "GA", "label": "Atlanta"},
    {"city": "Sandy Springs", "state": "GA", "label": "Sandy Springs"},
    {"city": "Roswell", "state": "GA", "label": "Roswell"},
    {"city": "Alpharetta", "state": "GA", "label": "Alpharetta"},
    {"city": "Johns Creek", "state": "GA", "label": "Johns Creek"},
    {"city": "Milton", "state": "GA", "label": "Milton"},
    {"city": "College Park", "state": "GA", "label": "College Park"},
    {"city": "East Point", "state": "GA", "label": "East Point"},
    {"city": "Union City", "state": "GA", "label": "Union City"},
    {"city": "Fairburn", "state": "GA", "label": "Fairburn"},
    {"city": "Palmetto", "state": "GA", "label": "Palmetto"},
    # DeKalb County
    {"city": "Decatur", "state": "GA", "label": "Decatur"},
    {"city": "Dunwoody", "state": "GA", "label": "Dunwoody"},
    {"city": "Brookhaven", "state": "GA", "label": "Brookhaven"},
    {"city": "Tucker", "state": "GA", "label": "Tucker"},
    {"city": "Stone Mountain", "state": "GA", "label": "Stone Mountain"},
    {"city": "Lithonia", "state": "GA", "label": "Lithonia"},
    {"city": "Clarkston", "state": "GA", "label": "Clarkston"},
    {"city": "Chamblee", "state": "GA", "label": "Chamblee"},
    {"city": "Doraville", "state": "GA", "label": "Doraville"},
    # Cobb County
    {"city": "Marietta", "state": "GA", "label": "Marietta"},
    {"city": "Smyrna", "state": "GA", "label": "Smyrna"},
    {"city": "Kennesaw", "state": "GA", "label": "Kennesaw"},
    {"city": "Acworth", "state": "GA", "label": "Acworth"},
    {"city": "Austell", "state": "GA", "label": "Austell"},
    {"city": "Powder Springs", "state": "GA", "label": "Powder Springs"},
    {"city": "Mableton", "state": "GA", "label": "Mableton"},
    # Gwinnett County
    {"city": "Lawrenceville", "state": "GA", "label": "Lawrenceville"},
    {"city": "Duluth", "state": "GA", "label": "Duluth"},
    {"city": "Suwanee", "state": "GA", "label": "Suwanee"},
    {"city": "Norcross", "state": "GA", "label": "Norcross"},
    {"city": "Lilburn", "state": "GA", "label": "Lilburn"},
    {"city": "Snellville", "state": "GA", "label": "Snellville"},
    {"city": "Buford", "state": "GA", "label": "Buford"},
    {"city": "Dacula", "state": "GA", "label": "Dacula"},
    {"city": "Grayson", "state": "GA", "label": "Grayson"},
    {"city": "Loganville", "state": "GA", "label": "Loganville"},
    # Cherokee County
    {"city": "Woodstock", "state": "GA", "label": "Woodstock"},
    {"city": "Canton", "state": "GA", "label": "Canton"},
    {"city": "Holly Springs", "state": "GA", "label": "Holly Springs"},
    {"city": "Ball Ground", "state": "GA", "label": "Ball Ground"},
    # Forsyth County
    {"city": "Cumming", "state": "GA", "label": "Cumming"},
    # Clayton County
    {"city": "Jonesboro", "state": "GA", "label": "Jonesboro"},
    {"city": "Morrow", "state": "GA", "label": "Morrow"},
    {"city": "Riverdale", "state": "GA", "label": "Riverdale"},
    {"city": "Forest Park", "state": "GA", "label": "Forest Park"},
    # Henry County
    {"city": "McDonough", "state": "GA", "label": "McDonough"},
    {"city": "Stockbridge", "state": "GA", "label": "Stockbridge"},
    {"city": "Hampton", "state": "GA", "label": "Hampton"},
    {"city": "Locust Grove", "state": "GA", "label": "Locust Grove"},
    # Douglas County
    {"city": "Douglasville", "state": "GA", "label": "Douglasville"},
    {"city": "Lithia Springs", "state": "GA", "label": "Lithia Springs"},
    {"city": "Villa Rica", "state": "GA", "label": "Villa Rica"},
    # Fayette County
    {"city": "Fayetteville", "state": "GA", "label": "Fayetteville"},
    {"city": "Peachtree City", "state": "GA", "label": "Peachtree City"},
    {"city": "Tyrone", "state": "GA", "label": "Tyrone"},
    # Rockdale County
    {"city": "Conyers", "state": "GA", "label": "Conyers"},
    # Newton County
    {"city": "Covington", "state": "GA", "label": "Covington"},
    # Paulding County
    {"city": "Dallas", "state": "GA", "label": "Dallas GA"},
    {"city": "Hiram", "state": "GA", "label": "Hiram"},
    # Bartow County
    {"city": "Cartersville", "state": "GA", "label": "Cartersville"},
    # Walton County
    {"city": "Monroe", "state": "GA", "label": "Monroe"},
]

DENTAL_TAXONOMY_PREFIX = "122"


def query_npi(city, state, taxonomy_desc="Dentist", limit=200, skip=0):
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
    basic = record.get("basic", {})
    addresses = record.get("addresses", [])
    taxonomies = record.get("taxonomies", [])
    other_names = record.get("other_names", [])

    enum_type = record.get("enumeration_type", "")
    is_org = enum_type == "NPI-2"

    practice_addr = {}
    for addr in addresses:
        if addr.get("address_purpose") == "LOCATION":
            practice_addr = addr
            break
    if not practice_addr and addresses:
        practice_addr = addresses[0]

    primary_tax = {}
    for tax in taxonomies:
        if tax.get("primary"):
            primary_tax = tax
            break
    if not primary_tax and taxonomies:
        primary_tax = taxonomies[0]

    dba_name = ""
    for on in other_names:
        if on.get("code") == "3":
            dba_name = on.get("organization_name", "")
            break

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
    print("NPI Registry Scraper — Atlanta Metro Dentists")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if test_mode:
        print("TEST MODE: first query only, limit 50")
    print("=" * 60)

    seen_npis = set()
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                seen_npis.add(row.get("npi", ""))
        print(f"Loaded {len(seen_npis)} existing NPIs from CSV")

    file_exists = os.path.exists(OUTPUT_CSV) and os.path.getsize(OUTPUT_CSV) > 0
    csv_file = open(OUTPUT_CSV, "a", encoding="utf-8", newline="")
    writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
    if not file_exists:
        writer.writeheader()

    queries = QUERIES[:1] if test_mode else QUERIES
    total_new = 0
    total_dupes = 0
    max_per_query = 5000

    for qi, q in enumerate(queries):
        city = q["city"]
        state = q["state"]
        label = q["label"]
        print(f"\n[{qi+1}/{len(queries)}] {label} ({city}, {state})")

        skip = 0
        limit = 50 if test_mode else 200
        query_new = 0
        query_total = 0

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
                if parsed["taxonomy_code"] and not parsed["taxonomy_code"].startswith(DENTAL_TAXONOMY_PREFIX):
                    continue
                if parsed["npi"] in seen_npis:
                    total_dupes += 1
                    continue
                seen_npis.add(parsed["npi"])
                writer.writerow(parsed)
                query_new += 1
                total_new += 1

            query_total += len(results)
            print(f"  Fetched {query_total} — {query_new} new dentists so far", end="\r")

            if len(results) < limit:
                break
            if query_total >= max_per_query:
                print(f"\n  Safety cap reached ({max_per_query})")
                break

            skip += limit
            time.sleep(0.3)

            if test_mode:
                break

        print(f"  {label}: {query_new} new dentists (total queried: {query_total})")
        csv_file.flush()

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
