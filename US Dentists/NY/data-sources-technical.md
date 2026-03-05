# NYC Dentist Data Sources — Technical Reference

**TL;DR:** Best free source is NPI Registry API (federal, structured, ~1,200 records/query max — need to paginate by zip code for full NYC). Yelp gives ratings/reviews via Apify at ~$0.60/1k. Healthgrades has a solid actor at $4/1k. Google Maps Apify actor is $4/1k (no add-ons) but we already burned credits there — use carefully. NY State license DB is web-only, no API, and gives no address or specialty detail — skip it.

---

## 1. NPI Registry API (Free, Federal)

**Endpoint:** `https://npiregistry.cms.hhs.gov/api/?version=2.1`

**Query for NYC dentists:**
```
GET https://npiregistry.cms.hhs.gov/api/?version=2.1
  &city=New+York
  &state=NY
  &taxonomy_description=Dentist
  &limit=200
  &skip=0
```

**Key parameters:**

| Parameter | Values | Notes |
|---|---|---|
| `city` | `New York` | Also try Brooklyn, Bronx, Queens, Staten Island |
| `state` | `NY` | Required |
| `taxonomy_description` | `Dentist`, `Orthodontics`, `Oral Surgery` | Text match, not code |
| `limit` | 1–200 | Default 10, max 200 |
| `skip` | 0–1000 | Hard limit |

**Hard limit:** Max 1,200 records per search criteria (skip=1000 + limit=200). To get all NYC dentists, must loop by borough or zip code.

**Fields returned:**
```json
{
  "result_count": 200,
  "results": [{
    "basic": {
      "first_name": "Jane",
      "last_name": "Smith",
      "credential": "DDS"
    },
    "addresses": [{
      "address_1": "123 Main St",
      "city": "New York",
      "state": "NY",
      "postal_code": "10001",
      "telephone_number": "212-555-0100"
    }],
    "taxonomies": [{
      "code": "1223G0001X",
      "desc": "General Practice",
      "primary": true
    }]
  }]
}
```

**Dental taxonomy codes:**

| Code | Specialty |
|---|---|
| `122300000X` | Dentist (General) |
| `1223G0001X` | General Practice |
| `1223X0400X` | Orthodontics & Dentofacial Orthopedics |
| `1223S0112X` | Oral and Maxillofacial Surgery |
| `1223P0221X` | Pediatric Dentistry |
| `1223E0200X` | Endodontics |
| `1223P0300X` | Periodontics |

**Rate limits:** No documented rate limit. Reasonable use assumed. No auth required.

**Strategy for full NYC:** Query each of the 5 boroughs by name + filter by zip ranges. Estimate: ~3,000–5,000 total dentist NPIs in NYC across all queries.

**Bulk download alternative:** CMS NPPES full data dissemination file available free at `https://download.cms.gov/nppes/NPI_Files.html` — monthly CSV export of all US providers.

---

## 2. NY State License Lookup

**URL:** `https://eservices.nysed.gov/professions/verification-search`

**Verdict: Web-form only. No API. No bulk download. Minimal data. Skip as primary source.**

| Field | Available? | Notes |
|---|---|---|
| License number | Yes | 7-digit |
| Name | Yes | First + last |
| Profession | Yes | "Dentist" (broad, no specialty) |
| License status | Yes | "Registered through [date]" or "Not Registered" |
| Address | Partial | City + State only. No street address |
| Phone | No | Not shown |
| Specialty | No | No sub-specialty data |

**Bulk data:** Must file a FOIL (Freedom of Information Law) request or pay for a roster from the Office of Professions. Not self-service.

**Use case:** Cross-reference license status by name if needed. Not worth scraping at scale. NPI Registry is superior for all data fields.

---

## 3. Apify — Yelp Scraper

**Best actor for business listings (not just reviews):** `spiders/yelp-search-scraper`
- Store URL: `https://apify.com/spiders/yelp-search-scraper`
- 98.6% success rate, lead-generation focused

**Pricing (FREE tier):** $0.0006/business (~$0.60/1k)

**Input schema:**
```json
{
  "search_urls": [],
  "search_location": "New York, NY",
  "search_limit": 10,
  "search_sort": "recommended",
  "domain": "www.yelp.com"
}
```
To search dentists: use `search_urls` with `https://www.yelp.com/search?find_desc=dentist&find_loc=New+York%2C+NY`

**Fields returned:** Business name, URL, address (formatted), phone, operating hours, category hierarchy, price range, aggregate rating, review count, review excerpts, reviewer metadata, photos, open/closed status, verified-license indicator.

**Pagination limit:** Yelp caps search results at ~240 results per search query (24 results x 10 pages). To get all NYC dentists, must segment by neighborhood or zip code — run multiple queries.

**Secondary actor (reviews only):** `tri_angle/yelp-scraper` — $0.001/result, 5,111 users, 99.3% success rate. Better if you want deep review text per business.

---

## 4. Apify — Healthgrades Scraper

**Best actor:** `fatihtahta/healthgrades-scraper`
- Store URL: `https://apify.com/fatihtahta/healthgrades-scraper`
- 100% success rate, 10 users (newer but well-reviewed)

**Pricing:** $3.99/1k listings (~$0.004/listing)

**Input schema:**
```json
{
  "startUrls": [
    "https://www.healthgrades.com/usearch?what=Dentist&where=New+York%2C+NY&state=NY"
  ],
  "limit": 50000,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"],
    "apifyProxyCountry": "US"
  }
}
```
Note: Residential proxy is required (built into input). No extra proxy cost.

**Fields returned:** Provider name + profile link, specialty, biography, numeric rating, review count, address + distance, phone, primary practice info, accepting new patients flag, listing placement metadata.

**Search strategy:** Use Healthgrades search URL with `what=Dentist&where=New+York,+NY`. Supports location-based search. Set `limit` high (50000) and let it paginate automatically.

**Alternative actor:** `shahidirfan/Healthgrades-Scraper` — FREE, covers doctors/dentists/hospitals, but lower usage count (8 users). May require own residential proxies.

---

## 5. Google Maps — Playwright vs. API

### Apify Actor (existing pipeline)
**Actor:** `compass/crawler-google-places`
- Same actor used in Israel pipeline — works for US with no changes
- Input: `searchStringsArray: ["dentist"], locationQuery: "New York, NY", maxCrawledPlacesPerSearch: 500`

**Pricing (FREE tier):**

| Item | Price |
|---|---|
| Base (per place scraped) | $0.004 |
| Filter add-on (per place, per filter) | $0.001 |
| Contact enrichment | $0.002 |
| Reviews | $0.0005/review |

**5,000 dentists, no add-ons = ~$20. With contact enrichment = ~$30.**

**NYC-scale gotchas:**
- Google caps results at ~120 per single search query — must run multiple search terms or borough/neighborhood splits
- Actor handles this via tiled polygon search or multiple `searchStringsArray` entries
- Run borough-by-borough: Manhattan, Brooklyn, Queens, Bronx, Staten Island
- Recommended: `async: false`, one borough at a time, save to CSV after each (per lessonslearned.md)

### Google Places API (direct, no Apify)
- $32/1k requests (Nearby Search) or $17/1k (Text Search) via GCP billing
- 5,000 dentists = ~$85–$160 depending on endpoint
- Requires GCP billing account, API key, pagination code
- **Verdict: Apify actor is cheaper and requires no infrastructure.**

---

## Cost Summary for ~5,000 NYC Dentists

| Source | Actor/Method | Est. Cost | Data Quality |
|---|---|---|---|
| NPI Registry | Direct API | Free | Address, phone, taxonomy — no ratings |
| Healthgrades | fatihtahta/healthgrades-scraper | ~$20 | Ratings, specialty, accepting patients |
| Yelp | spiders/yelp-search-scraper | ~$3 | Ratings, reviews, photos |
| Google Maps | compass/crawler-google-places | ~$20 | Address, phone, hours, ratings |
| NY State License | Web-only / FOIL | Skip | License status only, no address |

**Recommended stack:** NPI (free backbone) + Healthgrades ($20) + Yelp ($3). Cross-reference by name/address. Skip Google Maps unless you need hours/photos specifically.
