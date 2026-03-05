# NYC Dental Clinics — Full Pipeline Plan

## TL;DR

4-source pipeline: NPI Registry (free backbone, every licensed dentist) → Google Maps via Playwright (free, ratings + reviews + website + hours) → Yelp via Apify (~$3) → Healthgrades via Apify (~$20). Then website enrichment via Playwright (free) and segmentation labeling. Total cost: **~$23 in Apify credits**. Output: `labeled-dentals.csv` matching the Israel format.

---

## Pipeline Overview

```
Step 1: NPI Registry API ──→ master-list.csv (name, address, phone, specialty)
              │                    ~3,000-5,000 dentists, FREE
              ▼
Step 2: Google Maps (Playwright) ──→ google-enriched.csv
              │                    + rating, review_count, website, hours, categories, maps_url
              │                    FREE, ~4-6 hrs runtime
              ▼
Step 3: Apify enrichment ──→ platform-enriched.csv
              │  3a: Yelp scraper ──→ yelp_url, yelp_rating, yelp_review_count     (~$3)
              │  3b: Healthgrades ──→ hg_url, hg_rating, hg_review_count, specialty (~$20)
              ▼
Step 4: Website enrichment (Playwright) ──→ full-enriched.csv
              │  Visit each website → social URLs, site_score, doctor_count
              │  FREE, ~2-3 hrs runtime
              ▼
Step 5: Segmentation ──→ labeled-dentals.csv
              Exact same 1/2/3/3a/3b/4/4a/4b/5 logic
```

| Step | Source | Cost | Runtime | Records |
|------|--------|------|---------|---------|
| 1 | NPI Registry API | $0 | ~5 min | 3,000-5,000 |
| 2 | Google Maps (Playwright) | $0 | ~4-6 hrs | match by name/addr |
| 3a | Yelp (Apify) | ~$3 | ~10 min | match by name/addr |
| 3b | Healthgrades (Apify) | ~$20 | ~15 min | match by name/addr |
| 4 | Website visits (Playwright) | $0 | ~2-3 hrs | clinics with websites |
| 5 | Label script | $0 | instant | all |
| **Total** | | **~$23** | **~7-10 hrs** | |

---

## Step 1: NPI Registry (Free Backbone)

**Why start here:** Every practicing dentist in NYC MUST have an NPI. This gives us the complete universe — no one is missed.

**Endpoint:** `https://npiregistry.cms.hhs.gov/api/?version=2.1`

**Strategy:** Loop by borough (NPI caps at 1,200 results/query):

```python
QUERIES = [
    {"city": "New York", "state": "NY"},      # Manhattan
    {"city": "Brooklyn", "state": "NY"},
    {"city": "Bronx", "state": "NY"},
    {"city": "Queens", "state": "NY"},         # may need zip splits
    {"city": "Staten Island", "state": "NY"},
    # Add zip-code queries for any borough hitting 1,200 cap
]
# taxonomy_description = "Dentist" catches all dental specialties
```

**Fields we get:** NPI number, first/last name, credential (DDS/DMD), practice address, phone, taxonomy (specialty), enumeration date.

**What we DON'T get:** Rating, reviews, website, hours, social media → that's what Steps 2-4 add.

**Script:** `01_scrape_npi.py` — pure API calls, no browser needed. Outputs `npi-master-list.csv`.

---

## Step 2: Google Maps (Playwright, Free)

**Why:** Ratings, review counts, website URLs, hours, categories, Google Maps link. The core data for segmentation.

**Adapt from:** `Dentists/scrape_dental_clinics.py` (identical approach, English locale)

**Search strategy:** 25 neighborhood-level searches to beat Google's ~120 result cap:

| Borough | Searches | Est. Results |
|---------|----------|-------------|
| Manhattan | 7 (Midtown, UES, UWS, Downtown, EV/LES, Harlem/WH, Chelsea) | 800-1,500 |
| Brooklyn | 6 (Downtown, Wburg, Park Slope, Bay Ridge, Flatbush, Bushwick) | 600-1,200 |
| Queens | 5 (Astoria/LIC, Flushing, Jamaica, Forest Hills, Bayside) | 500-1,000 |
| Bronx | 3 (Fordham, Riverdale, South Bronx) | 300-600 |
| Staten Island | 1 | 100-300 |
| Generic | 3 (citywide, emergency, cosmetic) | dedup mostly |

**Matching to NPI:** Join on (name + address) fuzzy match. NPI gives us the universe; Google gives us the digital presence.

**Script:** `02_scrape_google_maps.py` — Playwright, headed browser, incremental CSV saves.

---

## Step 3: Apify Enrichment

### What You Need from Apify

**Account:** Your existing Apify account. Check credit balance before running.

**Two actors to run:**

#### 3a. Yelp — `spiders/yelp-search-scraper`

| Detail | Value |
|--------|-------|
| Actor ID | `spiders/yelp-search-scraper` |
| Store URL | apify.com/spiders/yelp-search-scraper |
| Cost | ~$0.60 per 1,000 results |
| Est. total | **~$3 for 5,000 dentists** |
| Success rate | 98.6% |

**Input:**
```json
{
  "search_urls": [
    "https://www.yelp.com/search?find_desc=dentist&find_loc=Manhattan%2C+New+York%2C+NY",
    "https://www.yelp.com/search?find_desc=dentist&find_loc=Brooklyn%2C+New+York%2C+NY",
    "https://www.yelp.com/search?find_desc=dentist&find_loc=Queens%2C+New+York%2C+NY",
    "https://www.yelp.com/search?find_desc=dentist&find_loc=Bronx%2C+New+York%2C+NY",
    "https://www.yelp.com/search?find_desc=dentist&find_loc=Staten+Island%2C+New+York%2C+NY"
  ],
  "search_limit": 240
}
```

**Gotcha:** Yelp caps at 240 results per search URL. 5 borough searches = max 1,200. May need neighborhood-level URLs for full coverage (same as Google approach).

**Fields returned:** name, url, address, phone, rating, review_count, categories, price_range, photos, hours, verified_license.

#### 3b. Healthgrades — `fatihtahta/healthgrades-scraper`

| Detail | Value |
|--------|-------|
| Actor ID | `fatihtahta/healthgrades-scraper` |
| Store URL | apify.com/fatihtahta/healthgrades-scraper |
| Cost | ~$4 per 1,000 listings |
| Est. total | **~$20 for 5,000 dentists** |
| Requires | Residential proxy (built into actor input) |

**Input:**
```json
{
  "startUrls": [
    "https://www.healthgrades.com/usearch?what=Dentist&where=New+York%2C+NY"
  ],
  "limit": 50000,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"],
    "apifyProxyCountry": "US"
  }
}
```

**Fields returned:** name, profile_url, specialty, rating, review_count, address, phone, accepting_new_patients, biography.

**Execution order (per lessons learned):**
1. Check Apify credit balance
2. Run Yelp first (cheaper, ~$3) — verify output quality
3. Then run Healthgrades (~$20) — one borough-search at a time if worried about credits
4. Save each result to local CSV immediately

---

## Step 4: Website Enrichment (Playwright, Free)

**For every clinic with a website URL** (from Google step):

| Check | How |
|-------|-----|
| Facebook URL | Scan page links for facebook.com |
| Instagram URL | Scan for instagram.com |
| TikTok URL | Scan for tiktok.com |
| Doctor/staff count | Visit /about or /team page, count names |
| Site score (0-10) | SSL + mobile viewport + load time + booking widget |
| Online booking | Check for Zocdoc/Calendly/LocalMed/Dentrix embed |

**Script:** `04_enrich_websites.py` — Playwright, same approach as Israel `enrich_dental_clinics.py`.

---

## Step 5: Segmentation

Exact same logic from `labeled-outreach-guide.md`:

| Segment | Name | Criteria |
|---------|------|----------|
| 1 | Leaky Funnel | Rating ≥4.0, has website, ≥20 reviews |
| 2 | Warm Digital, No Proof | Rating ≥4.0, has website, <20 reviews |
| 3 | Reputation Rescue | Rating <4.0, <3 reviews |
| 3a | Reputation Rescue - Some | Rating <4.0, 3-10 reviews |
| 3b | Reputation Rescue - High | Rating <4.0, 10+ reviews |
| 4 | Invisible Good | Rating ≥4.0, no website, <3 reviews |
| 4a | Invisible Good - Some | Rating ≥4.0, no website, 3-10 reviews |
| 4b | Invisible Good - High | Rating ≥4.0, no website, 10+ reviews |
| 5 | Digitally Absent | No rating data |

---

## Final CSV Columns

```
name, address, city, borough, phone, website, rating, review_count,
categories, hours, google_maps_url, search_term, scraped_at,
npi_number, credential, specialty,
facebook_url, instagram_url, tiktok_url,
yelp_url, yelp_rating, yelp_review_count,
hg_url, hg_rating, hg_review_count, accepting_new_patients,
google_review_count, doctor_count, staff_count, site_score,
has_online_booking, comments, segment, segment_name
```

---

## Execution Checklist

- [ ] Check Apify credit balance (need ~$25)
- [ ] Run Step 1: NPI scrape (free, 5 min)
- [ ] Run Step 2: Google Maps Playwright (free, 4-6 hrs) — borough by borough
- [ ] Run Step 3a: Yelp Apify (~$3) — verify output, then full run
- [ ] Run Step 3b: Healthgrades Apify (~$20) — start with 1 borough test
- [ ] Merge all sources by (name + address) fuzzy match
- [ ] Run Step 4: Website enrichment (free, 2-3 hrs)
- [ ] Run Step 5: Label segments
- [ ] Output: `labeled-dentals.csv`
