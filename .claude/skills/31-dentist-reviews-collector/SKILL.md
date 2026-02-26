---
name: dentist-reviews-collector
description: Collect all reviews for an Israeli dentist from Google, Medreviews.co.il, and Facebook into a single CSV. Use when collecting dentist reviews, scraping dental clinic feedback, or building a review database for a dental practice.
---

# Dentist Reviews Collector

Collect all public reviews for a dental clinic from 3 sources into one unified CSV.

## Trigger

User provides a dentist website URL (e.g., `drandy.co.il`) and wants all their reviews collected.

## Output

Single CSV file: `dr-{name}-reviews.csv`
Columns: `Reviewer Name,Stars,Review Text,Source,Review Link`

---

## Step 1: Discover the Dentist's Online Presence

Use `mcp__apify__apify-slash-rag-web-browser` to find the dentist's listings.

**Search queries to run (as separate calls):**

1. `"{business name from website}" Google Maps` — find the Google Maps listing URL
2. `site:medreviews.co.il "{business name}"` — find the Medreviews provider page
3. `"{business name}" Facebook page` — find the Facebook page and extract the page ID

**From results, extract:**
- Google Maps place URL (must contain `/maps/place/` or `/maps/search/`)
- Medreviews.co.il provider page URL
- Facebook page ID (numeric ID from the page URL or page info)

**If any source isn't found:** Skip it, note it in the final summary, and continue with the others.

---

## Step 2: Google Reviews

Use the Apify actor `compass/Google-Maps-Reviews-Scraper`.

**Call with `mcp__apify__call-actor`:**
```json
{
  "actor": "compass/Google-Maps-Reviews-Scraper",
  "input": {
    "startUrls": [{"url": "<GOOGLE_MAPS_URL>"}],
    "maxReviews": 99999,
    "language": "iw",
    "personalData": true,
    "reviewsSort": "newest"
  }
}
```

**Wait for completion**, then use `mcp__apify__get-actor-output` with the returned `datasetId`.

**Map output fields to CSV:**
| Actor field | CSV column |
|---|---|
| `name` | Reviewer Name |
| `stars` | Stars |
| `text` | Review Text |
| (hardcoded) | Source = "Google" |
| `reviewUrl` | Review Link |

---

## Step 3: Medreviews.co.il

Use Playwright MCP to browse the Medreviews provider page.

**Workflow:**

1. Navigate to the provider's Medreviews URL with `mcp__playwright__browser_navigate`
2. Take a snapshot with `mcp__playwright__browser_snapshot`
3. Extract all reviews visible on the page. Each review typically contains:
   - Reviewer name
   - Star rating (numeric or visual)
   - Review text
   - Date
4. **Paginate:** Look for pagination buttons (next page / numbered pages) in the snapshot. Click the next page button with `mcp__playwright__browser_click`, then snapshot again. Repeat until no more pages.
5. Collect ALL reviews across all pages.

**Map to CSV:**
| Medreviews field | CSV column |
|---|---|
| Reviewer name | Reviewer Name |
| Rating (numeric) | Stars |
| Review text | Review Text |
| (hardcoded) | Source = "Medreviews" |
| Page URL | Review Link |

---

## Step 4: Facebook Reviews

Use the Apify actor `powerai/facebook-page-review-scraper`.

**Call with `mcp__apify__call-actor`:**
```json
{
  "actor": "powerai/facebook-page-review-scraper",
  "input": {
    "page_id": "<FACEBOOK_PAGE_ID>",
    "maxResults": 9999
  }
}
```

**Wait for completion**, then use `mcp__apify__get-actor-output` with the returned `datasetId`.

**Map output fields to CSV:**
| Actor field | CSV column |
|---|---|
| Author name | Reviewer Name |
| `recommend` true/false | Stars = "Recommend" / "Not Recommend" |
| `message` | Review Text |
| (hardcoded) | Source = "Facebook" |
| Post URL | Review Link |

---

## Step 5: Combine & Save

1. Ask user for the output folder path (suggest `Dentists/{ClinicName}/`)
2. Merge all reviews from Steps 2-4 into one array
3. Sort by Source (Google first, then Medreviews, then Facebook)
4. Write CSV with header: `Reviewer Name,Stars,Review Text,Source,Review Link`
   - Properly escape commas and quotes in review text (wrap in double quotes, escape internal quotes)
5. Save as `dr-{name}-reviews.csv` in the chosen folder

**Print summary:**
```
| Source      | Reviews |
|-------------|---------|
| Google      | XX      |
| Medreviews  | XX      |
| Facebook    | XX      |
| **Total**   | **XXX** |
```

---

## Error Handling

- **Google Maps URL not found:** Try searching with Hebrew business name + city
- **Medreviews has no pagination:** Collect whatever is on the single page
- **Facebook page ID not found:** Try using the RAG browser to visit the Facebook page directly and extract the ID from page source
- **Actor timeout:** Retry once. If still failing, skip and note in summary.
- **Empty results from a source:** Include source in summary with 0 count, don't error

## CSV Formatting Rules

- Always use UTF-8 encoding (Hebrew text)
- Wrap any field containing commas, quotes, or newlines in double quotes
- Escape double quotes inside fields by doubling them (`""`)
- First row is always the header: `Reviewer Name,Stars,Review Text,Source,Review Link`
