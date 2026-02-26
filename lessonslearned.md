# Lessons Learned

## 1. Never Run Expensive/Irreversible Operations Without a Safety Net (2026-02-22)

**General rule:** Before running anything that costs money, uses external APIs, or can't be undone — STOP and do three things:
1. **Estimate the cost/impact** and tell the user explicitly before running
2. **Run in small batches**, save results locally after each batch — so if something fails mid-way, you keep what you already got
3. **Ask the user** to confirm they want to proceed, including: what it will cost, what the risks are, and what the fallback plan is if it fails

**Why:** A single large operation that fails mid-way loses everything. Small batches with local saves mean worst case you lose one batch, not the whole thing.

**Specific example — Apify Google Maps Scraper:**
Ran 5 search terms x 500 results + enrichment on free tier (~$5 credits). Actor charged per-place as it scraped, credits ran out mid-run, only 5 of ~200+ scraped results were saved. ~$5 wasted.

What should have happened:
- Run 1 search term at a time, `async: false`, save to local CSV after each
- Check credit balance before launching
- Estimate: "This will cost ~$4-6, you have ~$5 — tight. Want to run a smaller test first?"

**Cost reference (Google Maps Scraper, free tier):**
- ~$1 per 100 basic places, ~$2 per 100 with enrichment
