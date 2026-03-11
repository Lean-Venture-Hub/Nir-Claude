"""
SMB Mass Scanner — Google Places API (New)
Scans US cities for SMBs, exports to CSV with all fields.
Uses ~$200/mo free tier.

Usage:
  python scripts/scan_smb.py --vertical auto_repair --city houston
  python scripts/scan_smb.py --vertical landscaping --city atlanta
  python scripts/scan_smb.py --all   # runs all verticals + cities
"""

import argparse
import csv
import json
import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "")
BASE_URL = "https://places.googleapis.com/v1/places:searchText"

# --- CONFIG ---

VERTICALS = {
    "auto_repair": {
        "folder": "Auto Repair",
        "search_terms": [
            "auto repair shop {area}",
            "car mechanic {area}",
            "auto body shop {area}",
            "car repair {area}",
            "auto service center {area}",
        ],
    },
    "landscaping": {
        "folder": "Landscaping",
        "search_terms": [
            "landscaping company {area}",
            "lawn care service {area}",
            "landscape maintenance {area}",
            "lawn mowing service {area}",
            "landscaper {area}",
        ],
    },
}

# Neighborhoods/areas to expand coverage (each query returns max 20)
# ~5 terms × ~5 areas = ~25 queries × 20 = ~500 max unique results per city
CITIES = {
    "auto_repair": [
        {
            "name": "Houston", "state": "TX",
            "areas": [
                "Houston, TX",
                "Houston Heights, Houston, TX",
                "Katy, TX",
                "Pasadena, TX",
                "Sugar Land, TX",
            ],
        },
        {
            "name": "Phoenix", "state": "AZ",
            "areas": [
                "Phoenix, AZ",
                "Scottsdale, AZ",
                "Tempe, AZ",
                "Mesa, AZ",
                "Glendale, AZ",
            ],
        },
    ],
    "landscaping": [
        {
            "name": "Atlanta", "state": "GA",
            "areas": [
                "Atlanta, GA",
                "Decatur, GA",
                "Marietta, GA",
                "Roswell, GA",
                "Alpharetta, GA",
            ],
        },
        {
            "name": "Dallas", "state": "TX",
            "areas": [
                "Dallas, TX",
                "Plano, TX",
                "Frisco, TX",
                "Arlington, TX",
                "Irving, TX",
            ],
        },
    ],
}

TARGET_PER_CITY = 400
MAX_PER_QUERY = 20  # Places API returns max 20 per page

FIELDS = [
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.nationalPhoneNumber",
    "places.internationalPhoneNumber",
    "places.websiteUri",
    "places.googleMapsUri",
    "places.rating",
    "places.userRatingCount",
    "places.types",
    "places.currentOpeningHours",
    "places.businessStatus",
]

CSV_COLUMNS = [
    "name",
    "address",
    "city",
    "state",
    "phone",
    "website",
    "rating",
    "review_count",
    "categories",
    "hours",
    "google_maps_url",
    "business_status",
    "has_website",
    "search_term",
    "vertical",
    "scraped_at",
    "place_id",
]


def search_places(query: str, page_token: str = None) -> dict:
    """Call Google Places API (New) Text Search."""
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": ",".join(FIELDS),
    }
    body = {
        "textQuery": query,
        "pageSize": MAX_PER_QUERY,
        "languageCode": "en",
    }
    if page_token:
        body["pageToken"] = page_token

    resp = requests.post(BASE_URL, headers=headers, json=body)
    resp.raise_for_status()
    return resp.json()


def parse_hours(opening_hours: dict) -> str:
    """Extract readable hours string."""
    if not opening_hours:
        return ""
    descriptions = opening_hours.get("weekdayDescriptions", [])
    return " | ".join(descriptions) if descriptions else ""


def parse_place(place: dict, search_term: str, city: str, state: str, vertical: str) -> dict:
    """Convert API place object to flat CSV row."""
    display_name = place.get("displayName", {})
    name = display_name.get("text", "") if isinstance(display_name, dict) else str(display_name)
    website = place.get("websiteUri", "")

    return {
        "name": name,
        "address": place.get("formattedAddress", ""),
        "city": city,
        "state": state,
        "phone": place.get("nationalPhoneNumber", "") or place.get("internationalPhoneNumber", ""),
        "website": website,
        "rating": place.get("rating", ""),
        "review_count": place.get("userRatingCount", 0),
        "categories": ", ".join(place.get("types", [])),
        "hours": parse_hours(place.get("currentOpeningHours")),
        "google_maps_url": place.get("googleMapsUri", ""),
        "business_status": place.get("businessStatus", ""),
        "has_website": "yes" if website and "facebook" not in website.lower() else "no",
        "search_term": search_term,
        "vertical": vertical,
        "scraped_at": datetime.now().isoformat(),
        "place_id": place.get("id", ""),
    }


def scrape_vertical_city(vertical: str, city_info: dict) -> list[dict]:
    """Scrape one vertical in one city, returns list of rows."""
    config = VERTICALS[vertical]
    city = city_info["name"]
    state = city_info["state"]
    results = []
    seen_ids = set()

    areas = city_info.get("areas", [f"{city}, {state}"])

    for area in areas:
        if len(results) >= TARGET_PER_CITY:
            break
        for term_template in config["search_terms"]:
            if len(results) >= TARGET_PER_CITY:
                break

            term = term_template.format(area=area)
            print(f"  Searching: {term}")

            page_token = None
            pages = 0

            while pages < 5:  # max 5 pages per query (100 results)
                if len(results) >= TARGET_PER_CITY:
                    break

                try:
                    data = search_places(term, page_token)
                except requests.HTTPError as e:
                    print(f"  Error: {e}")
                    print(f"  Response: {e.response.text}")
                    break

                places = data.get("places", [])
                if not places:
                    break

                for place in places:
                    pid = place.get("id", "")
                    if pid in seen_ids:
                        continue
                    seen_ids.add(pid)
                    results.append(parse_place(place, term, city, state, vertical))

                page_token = data.get("nextPageToken")
                pages += 1

                if not page_token:
                    break

                time.sleep(1.5)  # be nice to the API

            time.sleep(1)  # pause between search terms

    print(f"  → {len(results)} unique results for {city}, {state}")
    return results


def save_csv(rows: list[dict], filepath: Path):
    """Save results to CSV."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Saved {len(rows)} rows → {filepath}")


def run_vertical(vertical: str):
    """Run scraping for one vertical across its cities."""
    config = VERTICALS[vertical]
    folder = Path(__file__).parent.parent / config["folder"]
    all_results = []

    print(f"\n{'='*50}")
    print(f"VERTICAL: {vertical.upper()}")
    print(f"{'='*50}")

    for city_info in CITIES[vertical]:
        city = city_info["name"]
        state = city_info["state"]
        print(f"\n📍 {city}, {state}")

        results = scrape_vertical_city(vertical, city_info)
        all_results.extend(results)

        # Save per-city CSV
        city_file = folder / f"{city.lower().replace(' ', '-')}-{state.lower()}.csv"
        save_csv(results, city_file)

    # Save combined CSV
    combined_file = folder / f"all-{vertical.replace('_', '-')}.csv"
    save_csv(all_results, combined_file)

    # Print summary
    no_site = sum(1 for r in all_results if r["has_website"] == "no")
    with_reviews = sum(1 for r in all_results if int(r["review_count"] or 0) >= 5)
    hot_leads = sum(1 for r in all_results if r["has_website"] == "no" and int(r["review_count"] or 0) >= 5)

    print(f"\n--- {vertical.upper()} SUMMARY ---")
    print(f"Total scraped:    {len(all_results)}")
    print(f"No website:       {no_site} ({no_site*100//max(len(all_results),1)}%)")
    print(f"5+ reviews:       {with_reviews} ({with_reviews*100//max(len(all_results),1)}%)")
    print(f"HOT LEADS:        {hot_leads} (no site + 5+ reviews)")

    return all_results


def main():
    if not API_KEY:
        print("ERROR: Set GOOGLE_PLACES_API_KEY environment variable")
        print("  export GOOGLE_PLACES_API_KEY=your_key_here")
        return

    parser = argparse.ArgumentParser(description="SMB Mass Scanner")
    parser.add_argument("--vertical", choices=list(VERTICALS.keys()), help="Vertical to scan")
    parser.add_argument("--city", help="Single city override (e.g. 'houston')")
    parser.add_argument("--all", action="store_true", help="Run all verticals + cities")
    args = parser.parse_args()

    if args.all:
        for v in VERTICALS:
            run_vertical(v)
    elif args.vertical:
        if args.city:
            # Override cities list with single city
            for city_info in CITIES[args.vertical]:
                if city_info["name"].lower() == args.city.lower():
                    CITIES[args.vertical] = [city_info]
                    break
        run_vertical(args.vertical)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
