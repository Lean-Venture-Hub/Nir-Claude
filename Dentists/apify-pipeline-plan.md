# Dental Clinic Research Pipeline - Apify Actors & Technical Plan

**TL;DR:** Use a 2-step pipeline: (1) `compass/crawler-google-places` to scrape all dental clinics from Google Maps Israel with GBP data, contacts, and website URLs, then (2) `koushikbiswas/site-lens-analyzer` + `nocodeventure/seo-data-extractor` to audit each clinic's website for quality signals. Total cost estimate: ~$15-25 for 500 clinics.

---

## Recommended Actors

| # | Actor | Purpose | Pricing (Free tier) |
|---|-------|---------|---------------------|
| 1 | `compass/crawler-google-places` | Google Maps + GBP data | $0.004/place + add-ons |
| 2 | `koushikbiswas/site-lens-analyzer` | Desktop/mobile screenshots, fonts, CSS, links | ~free (pay per event) |
| 3 | `nocodeventure/seo-data-extractor` | SEO metadata, SSL, headings, OG tags, technical data | $0.005/result |
| 4 | `ittechinnovators/advanced-seo-audit-tool---ai-powered-insights` | Full SEO + UX + performance audit | $0.01/result |

**Why `compass/crawler-google-places` over alternatives:**
- 282K users, 96% success rate, 4.7 stars (887 reviews)
- Most comprehensive: GBP data + contacts + reviews + images in one run
- Supports Israel (country code `il`), Hebrew language
- Pay-per-event keeps costs predictable

---

## Pipeline Steps

### Step 1: Google Maps Scrape (compass/crawler-google-places)

**Input config:**
```json
{
  "searchStringsArray": ["מרפאת שיניים", "רופא שיניים", "dental clinic", "dentist"],
  "countryCode": "il",
  "language": "he",
  "maxCrawledPlacesPerSearch": 500,
  "website": "allPlaces",
  "skipClosedPlaces": true,
  "scrapePlaceDetailPage": true,
  "scrapeContacts": true,
  "maxReviews": 0,
  "maxImages": 0,
  "scrapeReviewsPersonalData": false
}
```

**Key params explained:**
- `searchStringsArray`: Hebrew + English search terms to maximize coverage
- `countryCode: "il"` + `language: "he"`: Targets Israel, Hebrew results
- `scrapePlaceDetailPage: true`: Gets openingHours, reviewsDistribution, popularTimes ($0.002/place extra)
- `scrapeContacts: true`: Extracts emails/social from websites ($0.002/place extra)
- `skipClosedPlaces: true`: Filters out closed clinics ($0.001/place extra)
- `maxReviews: 0` / `maxImages: 0`: We only need counts, not full reviews/images (saves cost)

**What you get back per place:**
- name, address, phone, website, googleMapsUrl, placeId
- totalScore (rating), reviewsCount, imageCount
- categories (e.g., "Dentist", "Cosmetic dentist")
- openingHours, popularTimesLiveText
- reviewsDistribution (1-5 star breakdown)
- emails, socialMedia links (from website scrape)
- isAdvertising (whether they run Google Ads)

**Cost estimate:** 500 places x ($0.004 base + $0.002 details + $0.002 contacts + $0.001 filter) = ~$4.50

### Step 2a: Website Visual Audit (koushikbiswas/site-lens-analyzer)

Run for each clinic URL from Step 1.

**Input config:**
```json
{
  "url": "<clinic_website_url>",
  "maxDepth": 1,
  "captureScreenshots": true,
  "extractCss": true,
  "extractText": true,
  "extractLinks": true,
  "extractImages": false,
  "extractVideos": false
}
```

**What you get back:**
- Desktop + mobile full-page screenshots (visual modernity check)
- Fonts and colors used (design quality signal)
- Internal/external link structure
- Text content + word count

**Cost estimate:** Minimal (pay-per-event, low cost per URL)

### Step 2b: SEO & Technical Audit (nocodeventure/seo-data-extractor)

Run in parallel with 2a for each clinic URL.

**Input config:**
```json
{
  "startUrls": [{"url": "<clinic_website_url>"}],
  "extractSslInfo": true,
  "maxRequestsPerCrawl": 5,
  "requestTimeout": 10
}
```

**What you get back:**
- Meta tags (title, description, viewport = mobile-friendly signal)
- SSL certificate validity
- Open Graph tags, Twitter Cards
- Heading structure (H1-H6)
- Image alt text coverage
- Response status codes

**Cost estimate:** 500 URLs x $0.005 = ~$2.50

### Step 2c (Optional): Full AI SEO Audit (ittechinnovators/advanced-seo-audit-tool)

Only run for high-priority targets or a sample.

**Input:** `{"startUrls": [{"url": "<url>"}]}`
**Returns:** Performance scores, UX analysis, social presence, payment gateway detection
**Cost:** $0.01/result

---

## Pipeline Orchestration

```
Step 1: compass/crawler-google-places
   ├── Output: dataset with ~500 dental clinics
   ├── Filter: extract website URLs (non-null)
   │
   ├── Step 2a: site-lens-analyzer (screenshots + CSS)  ──┐
   │                                                       ├── Merge by URL
   └── Step 2b: seo-data-extractor (SEO + technical)  ────┘
                                                           │
                                                     Final Dataset
```

**Implementation options:**
1. **Manual:** Run Step 1, download dataset, feed URLs into Steps 2a/2b
2. **Apify API:** Chain actors via webhooks or a Node.js/Python orchestrator script
3. **Apify Scheduler:** Set up recurring runs for monitoring over time

---

## Detecting Online Booking

None of the actors directly detect booking systems. Options:
- **From Step 2b output:** Search extracted links/text for booking platform domains (e.g., zocdoc, doctorlib, mydent, calendly, acuity)
- **From Step 2a output:** Search extracted text content for Hebrew booking terms (הזמנת תור, קביעת תור)
- **Custom script:** After scraping, grep the HTML/text for common booking widget patterns

---

## Total Cost Estimate

| Step | Items | Cost |
|------|-------|------|
| Google Maps scrape | 500 places | ~$4.50 |
| Site Lens screenshots | ~350 URLs (with websites) | ~$1-2 |
| SEO Data Extractor | ~350 URLs | ~$2.50 |
| **Total** | | **~$8-10** |

Add ~$5-10 if you also run the AI SEO audit on a subset.
