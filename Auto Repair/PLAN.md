# Auto Repair — US Mass Scan

## Status: SETUP

## Target Columns (mirroring Dentists pipeline)

| Column | Source | Notes |
|---|---|---|
| name | Google Maps | Business name |
| address | Google Maps | Full address |
| city | Google Maps | City name |
| state | Google Maps | US state |
| phone | Google Maps | Phone number |
| website | Google Maps | Website URL (empty = lead) |
| rating | Google Maps | Google rating (0-5) |
| review_count | Google Maps | Total Google reviews |
| categories | Google Maps | Business categories |
| hours | Google Maps | Operating hours |
| google_maps_url | Google Maps | Direct link |
| search_term | Scraper | Query used |
| scraped_at | Scraper | Timestamp |
| facebook_url | Enrichment | Facebook page |
| instagram_url | Enrichment | Instagram profile |
| yelp_url | Enrichment | Yelp listing (US equivalent of Easy.co.il) |
| yelp_rating | Enrichment | Yelp rating |
| yelp_review_count | Enrichment | Yelp reviews |
| site_score | Enrichment | Website quality (0-10) |
| has_booking | Enrichment | Online booking available? |
| segment | Analysis | Lead segment |
| segment_name | Analysis | Segment label |

## Pilot Cities (5 cities, ~200-400 results each)

| City | State | Why |
|---|---|---|
| Houston | TX | Largest car culture city, huge volume |
| Phoenix | AZ | Fast-growing, car-dependent |
| San Antonio | TX | Large, underserved market |
| Jacksonville | FL | Sprawling, car-dependent |
| Memphis | TN | Mid-size, lower digital adoption |

## Search Terms
- "auto repair shop [city]"
- "car mechanic [city]"
- "auto body shop [city]"

## Next Steps
- [ ] Configure Apify Google Maps scraper
- [ ] Test with 1 city first (Houston)
- [ ] Review results, adjust filters
- [ ] Scale to remaining 4 cities
