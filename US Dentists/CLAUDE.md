# US Dentists Pipeline — Project Instructions

## What This Is

A multi-city pipeline that scrapes, enriches, and segments every dental clinic in a US metro area. Output: `labeled-dentals.csv` per city — a sales-ready database for dental marketing outreach.

---

## Pipeline (6 steps per city)

```
01_scrape_npi.py       → npi-master-list.csv        (NPI Registry API, free, ~5 min)
02_scrape_google_maps.py → google-maps-raw.csv      (Playwright headed, free, ~4-6 hrs)
[03 — Apify: Yelp + Healthgrades]                   (not yet built, ~$23/city)
04_enrich_websites.py  → enriched-clinics.csv        (Playwright headless, free, ~2-3 hrs)
05_label_segments.py   → labeled-dentals.csv         (instant)
06_add_practice_type.py → labeled-dentals.csv        (instant, uses NPI address clustering)
07_add_review_recency.py → labeled-dentals.csv       (Playwright, free, ~3-5 hrs)
```

Each script reads from the previous step's output. Steps 5-7 modify `labeled-dentals.csv` in place.

---

## City Status

| City | NPI | Google Maps | Enrich | Labels | Practice Type | Review Recency | Final CSV |
|------|-----|-------------|--------|--------|---------------|----------------|-----------|
| **NYC** | 6,407 | 1,936 | Done | Done | Done | Done | 1,936 rows, 27 cols |
| **Houston** | 5,223 | 4,777 | Done | Done | Done | Done | 2,389 rows, 27 cols |
| **DFW** | 8,702 | 7,849 | Done | Done | Done | Done | 3,928 rows, 27 cols |
| **Atlanta** | 5,301 | 1,077 | Done | Done | Done | Done | 1,077 rows, 27 cols |
| **Phoenix** | 5,287 | 1,092 | Done | Done | Done | Done | 1,092 rows, 27 cols |
| **Charlotte** | 2,802 | 1,425 | Done | Done | Done | Done | 1,425 rows, 27 cols |

---

## Segmentation Logic

Based on `labeled-outreach-guide.md`. Three inputs: rating (threshold: 4.0), website (yes/no), review count (thresholds: 3, 10, 20).

| Seg | Name | Criteria |
|-----|------|----------|
| 1 | Leaky Funnel | rating >= 4.0, has website, reviews >= 20 |
| 2 | Warm Digital, No Proof | rating >= 4.0, has website, reviews < 20 |
| 3 | Reputation Rescue | rating < 4.0, reviews < 3 |
| 3a | Rep Rescue - Some | rating < 4.0, reviews 3-10 |
| 3b | Rep Rescue - High | rating < 4.0, reviews 10+ |
| 4 | Invisible Good | rating >= 4.0, no website, reviews < 3 |
| 4a | Invisible Good - Some | rating >= 4.0, no website, reviews 3-10 |
| 4b | Invisible Good - High | rating >= 4.0, no website, reviews 10+ |
| 5 | Digitally Absent | no rating data |

---

## Final CSV Columns

```
name, address, area, city, phone, website, rating, review_count,
categories, hours, google_maps_url, search_term, scraped_at,
facebook_url, instagram_url, tiktok_url, google_review_count,
doctor_count, staff_count, site_score, has_online_booking, comments,
segment, segment_name, practice_type, review_recency, latest_review_age
```

- `area` = borough (NYC) or metro area (Houston: Core, North, West, South, East, etc.)
- `practice_type` = Solo / Group / Unknown (from doctor_count + NPI clustering + name patterns)
- `review_recency` = Fresh (<6mo) / Recent (6-12mo) / Aging (1-2yr) / Stale (2yr+) / No reviews

---

## Adding a New City

1. Create folder: `US Dentists/{CityName}/`
2. Copy scripts 01, 02, 04-07 from an existing city
3. Adapt `01_scrape_npi.py`: update `QUERIES` with city/suburb names and zip codes
4. Adapt `02_scrape_google_maps.py`: update `SEARCHES` (neighborhood-level queries to beat Google's ~120 result cap), `AREA_PATTERNS` for area detection, and city name references
5. Scripts 04-07 are portable (use `SCRIPT_DIR` for paths) — just copy, no edits needed
6. Run in order: 01 → 02 → 04 → 05 → 06 → 07

---

## Key Lessons Learned

- **Never run expensive/irreversible ops without safety net.** Run 1 search at a time, save locally after each.
- **NPI pagination:** Exit on `len(results) < limit`, not on `result_count`. No hard 1,200 cap exists.
- **Google Maps locale:** Force English with `extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}` and `?hl=en` in URL.
- **Test mode must not overwrite full CSV.** Use separate `rows_to_process` variable; always write full `rows` list back.
- **Google Maps caps at ~120 results per search.** Use 30-50 neighborhood-level searches per city.
- **NPI-1 vs NPI-2:** Organizations use `authorized_official_first_name` not `first_name`.
- **Step 3 (Apify) not yet built.** Yelp (~$3/city) and Healthgrades (~$20/city) scrapers identified but not executed.

---

## Data Sources

| Source | Cost | What It Gives |
|--------|------|---------------|
| NPI Registry API | Free | Every licensed dentist: name, credential, address, phone, specialty |
| Google Maps (Playwright) | Free | Rating, reviews, website, hours, categories, maps URL |
| Yelp (Apify, pending) | ~$3/city | Yelp URL, rating, review count, price range |
| Healthgrades (Apify, pending) | ~$20/city | HG URL, rating, reviews, accepting new patients |
| Website visits (Playwright) | Free | Social URLs, site score (0-10), doctor count, booking detection |
| Google Maps reviews (Playwright) | Free | Review recency (most recent review timestamp) |

---

## Market Priority (from next-markets.md)

1. **Houston** — 2,200 est. practices, very high growth (+198K/yr), low agency competition
2. **DFW** — 2,500 est., very high growth, medium competition
3. **Atlanta** — 1,600 est., high growth, low-medium competition
4. **Phoenix** — 1,200 est., high growth, very low competition
5. **Charlotte** — 800 est., very high growth, very low competition
