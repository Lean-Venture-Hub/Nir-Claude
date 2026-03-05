# Google Maps Platform API - Research Brief

**Date:** 2026-02-27

Google Maps Platform uses a pay-as-you-go model with free monthly usage caps per API. As of March 1, 2025, Google replaced the old flat $200/month credit with per-API free tiers that, combined, are worth up to $3,250/month in free usage. This is a net improvement for most developers who use multiple APIs. After free caps are exhausted, volume-based pricing kicks in automatically.

The main risk: if you exceed daily/monthly limits, APIs fail hard (no graceful degradation). A billing account and credit card are required even for free-tier usage. Legacy APIs (old Directions, Distance Matrix, Places v1) were frozen on March 1, 2025 - new projects must use the new versions.

---

## Available APIs (as of 2025-2026)

| Category | API | Notes |
|---|---|---|
| Maps | Maps JavaScript API | Web map embeds |
| Maps | Maps Embed API | Free, unlimited |
| Maps | Maps SDK (iOS/Android) | Free, unlimited |
| Maps | Map Tiles API | 2D + Street View tiles |
| Routes | Routes API | Replaces legacy Directions + Distance Matrix |
| Routes | Directions API (Legacy) | Frozen Mar 2025, no new enables |
| Routes | Distance Matrix API (Legacy) | Frozen Mar 2025, no new enables |
| Places | Places API (New) | Replaces legacy Places API |
| Places | Address Validation API | New, Pro tier |
| Places | Autocomplete | Part of Places (New) |
| Geocoding | Geocoding API | Address <-> lat/lng |
| Geocoding | Geolocation API | IP/cell-based location |
| Geocoding | Time Zone API | |
| Environment | Air Quality API | |
| Environment | Solar API | |
| Environment | Pollen API | |

---

## Pricing Table (March 2025 onwards)

| API / SKU | Free Cap | Price after cap (per 1,000) | Tier |
|---|---|---|---|
| Maps JavaScript (Dynamic Maps) | 10,000/mo | $7.00 → $0.53 (at 5M+) | Essentials |
| Maps Embed API | Unlimited | Free | - |
| Maps SDK (iOS/Android) | Unlimited | Free | - |
| Geocoding API | 10,000/mo | $5.00 → $0.38 (at 5M+) | Essentials |
| Routes - Compute Routes Essentials | 10,000/mo | $5.00 → $0.38 (at 5M+) | Essentials |
| Places - Place Details Essentials | 10,000/mo | $5.00 → $0.38 (at 5M+) | Essentials |
| Places - Autocomplete | 10,000/mo | $2.83 → $0.21 (at 5M+) | Essentials |
| Places - Text Search Pro | 5,000/mo | $32.00 → $2.40 (at 5M+) | Pro |
| Address Validation | 5,000/mo | ~$2.50/1,000 | Pro |
| Routes - Advanced (traffic-aware) | 5,000/mo | Higher enterprise rates | Pro |
| Route Optimization API | 1,000/mo | Enterprise pricing | Enterprise |
| Photorealistic 3D Tiles | 1,000/mo | Enterprise pricing | Enterprise |
| Map Tiles (2D + Street View) | 100,000/mo | Tiered | Essentials |

---

## Free Tier Structure (Post-March 2025)

- **Essentials SKUs:** 10,000 free calls/month per SKU
- **Pro SKUs:** 5,000 free calls/month per SKU
- **Enterprise SKUs:** 1,000 free calls/month per SKU
- **Maps Embed + SDK:** Unlimited free
- **Total free value:** Up to $3,250/month across all APIs combined
- Free usage resets on the 1st of each month at midnight Pacific time

**Comparison to old model:**
- Old: Flat $200/month credit applied across all APIs
- New: Per-API caps worth significantly more in aggregate

---

## Key Limits & Gotchas

- Billing account + credit card required even for free usage
- No daily quota by default - monthly caps apply; can set budget alerts
- If monthly cap exceeded: service stops, does not degrade gracefully
- Rate limits: 3,000 requests per minute per project (varies by API)
- 1 API key per project; can restrict by HTTP referrer, IP, or mobile app
- Legacy APIs (Directions v1, Distance Matrix, Places v1) frozen as of March 1, 2025 - existing users can continue, new projects cannot enable them

---

## 2025-2026 Changes Summary

| Date | Change |
|---|---|
| March 1, 2025 | $200/mo flat credit replaced by per-API free caps |
| March 1, 2025 | Legacy Directions, Distance Matrix, Places APIs frozen (no new enables) |
| March 1, 2025 | Automatic volume discounts now scale to 5M+ events (was 100K+) |
| 2025 | New Environment APIs added (Air Quality, Solar, Pollen) |
| 2025 | Route Optimization and Photorealistic 3D Tiles added as Enterprise tier |

---

## Sources

- [Google Maps Platform Pricing Overview](https://developers.google.com/maps/billing-and-pricing/overview)
- [March 2025 Changes](https://developers.google.com/maps/billing-and-pricing/march-2025)
- [Core Services Pricing List](https://developers.google.com/maps/billing-and-pricing/pricing)
- [Google Maps Platform Pricing Page](https://mapsplatform.google.com/pricing/)
- [9to5Google: Expanding Free Usage Limits](https://9to5google.com/2024/12/09/google-maps-platform-usage-limits/)
- [Radar: True Cost of Google Maps API 2026](https://radar.com/blog/google-maps-api-cost)
- [Places API Usage and Billing](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing)
