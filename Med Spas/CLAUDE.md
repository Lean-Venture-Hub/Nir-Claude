# Med Spas Pipeline — Project Instructions

## What This Is

A multi-city pipeline that scrapes, enriches, and segments every med spa in a US metro area. Output: `labeled-medspas.csv` per city — a sales-ready database for med spa marketing outreach.

---

## Pipeline (5 steps per city)

```
01_scrape_google_maps.py  → google-maps-raw.csv     (Playwright headed, free, ~4-6 hrs)
02_enrich_websites.py     → enriched-clinics.csv     (Playwright headless, free, ~2-3 hrs)
03_label_segments.py      → labeled-medspas.csv      (instant)
04_add_practice_type.py   → labeled-medspas.csv      (instant, name + doctor_count only)
05_add_review_recency.py  → labeled-medspas.csv      (Playwright, free, ~3-5 hrs)
```

No NPI step — med spas don't have an NPI registry like dentists.
Each script reads from the previous step's output. Steps 3-5 modify `labeled-medspas.csv` in place.

---

## City Status

| City | Google Maps | Enrich | Labels | Practice Type | Review Recency | Final CSV |
|------|-------------|--------|--------|---------------|----------------|-----------|
| **DFW** | Pending | — | — | — | — | — |
| **Atlanta** | Running (started 2026-03-04) | — | — | — | — | — |

---

## Segmentation Logic

Same as dentist pipeline. Three inputs: rating (threshold: 4.0), website (yes/no), review count (thresholds: 3, 10, 20).

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

## Practice Type Classification (Simplified vs Dentists)

No NPI clustering. Uses only:
1. `doctor_count >= 2` → Group
2. `doctor_count == 1` → Solo
3. Name patterns: group signals (center, clinic, studio, spa, etc.) vs solo signals (dr., md, do)
4. Default: Unknown

---

## Final CSV Columns

```
name, address, area, city, phone, website, rating, review_count,
categories, hours, google_maps_url, search_term, scraped_at,
facebook_url, instagram_url, tiktok_url, google_review_count,
doctor_count, staff_count, site_score, has_online_booking, comments,
segment, segment_name, practice_type, review_recency, latest_review_age
```

---

## Search Terms Strategy

Per area: "med spa {area} TX", "medical spa {area} TX", "medspa {area} TX", "botox {area} TX"
Key areas also get: "aesthetics {area} TX", "laser hair removal {area} TX", "coolsculpting {area} TX"
~70 total searches across 8 DFW area groups. Expected yield: 300-800 unique med spas.

---

## Booking Platforms (Med Spa Specific)

Vagaro, GlossGenius, Boulevard, Aesthetic Record, PatientNow, Nextech, Symplast, Mangomint, Zenoti

---

## Provider Titles

MD, DO, NP, PA, RN, BSN, APRN, FNP, DNP, CRNA, Dr., Doctor

---

## Key Differences from Dentist Pipeline

1. No NPI step (no NPI registry for med spas)
2. Search terms: med spa/botox/aesthetics instead of dentist/dental
3. Booking platforms: Vagaro/Boulevard/Zenoti instead of Zocdoc/Dentrix
4. Provider titles: NP/PA/RN instead of DDS/DMD
5. Practice type: simplified (no NPI address clustering)
6. 5 steps instead of 7

---

## Key Lessons (inherited from dentist pipeline)

- Never run expensive/irreversible ops without safety net. Run 1 search at a time, save locally after each.
- Google Maps locale: Force English with `extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}` and `?hl=en` in URL.
- Test mode must not overwrite full CSV. Use separate `rows_to_process` variable; always write full `rows` list back.
- Google Maps caps at ~120 results per search. Use 30-50 neighborhood-level searches per city.
