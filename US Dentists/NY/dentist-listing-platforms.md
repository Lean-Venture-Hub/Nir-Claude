# NYC Dentist Listing Platforms: Full Inventory

NYC has ~2,541 licensed dentists in Manhattan alone, competing across 20+ platforms. Patient acquisition is won or lost digitally: 73% of patients use online reviews to choose a provider, 77% search online before booking, and 91% place moderate-to-high trust in reviews. Google dominates (66% of patients check it first), but Zocdoc is the highest-intent booking platform in dense urban markets like NYC.

Top 4 platforms drive ~80% of new patient acquisition: Google Business Profile, Zocdoc, Healthgrades, and Yelp — in that order. Insurance directories (Delta Dental, Cigna, Aetna, Guardian) are critical secondary touchpoints for in-network verification. Social (Facebook, Instagram) supports retention and brand, not primary discovery.

---

## Master Comparison Table

| Platform | Type | Reviews | NYC Listings (est.) | Cost | API/Scrape | Importance |
|---|---|---|---|---|---|---|
| Google Business Profile | Search + Map | Patient, 1-5 star, text | 2,300+ | Free | GBP API (enterprise); Places API | CRITICAL |
| Zocdoc | Booking + Review | Verified (post-visit only), 1-5 star | 315+ (Manhattan); 1,000+ citywide | Free basic; pay-per-booking | API (scheduling); Apify scraper $29.99/mo | VERY HIGH |
| Healthgrades | Healthcare directory | Multi-factor (wait, staff, etc.), 1-5 | 8,517+ (10mi radius) | Free basic; paid Featured | Apify scrapers $19/mo; reviewapi.com $79/mo | HIGH |
| Yelp | General review | 1-5 star, unverified text | 4,000+ | Free basic; paid ads | Places API ($5.91–$14.13/1K calls) | HIGH |
| WebMD / Vitals | Healthcare info + dir | 4-star multi-factor; no reviews on WebMD | Thousands | Free basic; paid Featured | WebMD Care API (auth required) | MODERATE |
| RateMDs | Healthcare review | 1-5 star (staff, helpfulness, punctuality) | 2,000+ | Free | Web scraping (public) | MODERATE |
| CareDash | Healthcare search | Verified, algo-filtered, 1-5 star | 1,000+ | Free | Enterprise API | EMERGING |
| 1-800-Dentist | Lead gen / referral | Patient ratings + text | National (pay to join) | ~$40-50/call | None public | MODERATE-HIGH |
| ADA Find-a-Dentist | Professional directory | None | ADA members only | Free w/ ADA membership | None public | MODERATE |
| OpenCare | Matching platform | Post-visit, curated | Growing | Free | None public | EMERGING |
| Doctor.com | General health dir | Patient reviews | 200K dentists nationally | Free claim | None public | LOW-MOD |
| Castle Connolly | Peer-nominated dir | No patient reviews; peer-vetted | 500+ NYC dentists | Paid listing | None public | LOW (gen); HIGH (specialist) |
| US News Health | Healthcare rankings | Aggregated data | N/A | N/A | None public | LOW |
| Sharecare | Health engagement | Patient reviews | Limited | Free claim | None public | LOW |
| **INSURANCE DIRECTORIES** | | | | | | |
| Delta Dental | Insurance network dir | None | In-network only | Free (via acceptance) | None public | MODERATE-HIGH |
| Cigna | Insurance network dir | None | In-network only | Free (via acceptance) | None public | MODERATE |
| Aetna | Insurance network dir | None (Smart Compare feature) | In-network only | Free (via acceptance) | None public | MODERATE |
| United Healthcare | Insurance network dir | None | In-network only | Free (via acceptance) | None public | MODERATE |
| Guardian | Insurance network dir | None | 138K+ nationally | Free (via acceptance) | None public | MODERATE-HIGH |
| MetLife | Insurance network dir | None | 138K+ nationally | Free (via acceptance) | None public | MODERATE |
| **SOCIAL / LOCAL** | | | | | | |
| Facebook Business | Social + review | 1-5 star + text, unverified | All NYC practices | Free; paid ads | Meta Graph API | MODERATE |
| Instagram Business | Visual social | Comments only, no formal review | All NYC practices | Free; paid ads | Meta Graph API | MODERATE-HIGH (under 40) |
| Nextdoor | Neighborhood social | Verified-resident recommendations | Outer boroughs focus | Free; paid deals | None public | MODERATE (outer) / LOW (Manhattan) |
| LinkedIn | Professional network | Endorsements only | All practices | Free; paid | LinkedIn API (limited) | LOW (gen) / MOD (specialist) |
| TikTok Business | Video social | Comments only | Growing | Free; paid ads | None public | LOW-MOD (emerging) |
| **LOCAL/MAP DIRECTORIES** | | | | | | |
| Apple Maps / Business Connect | Map + local search | Aggregated ratings | All NYC practices | Free | None public | LOW-MOD |
| Bing Places | Search + Map | Bing reviews + aggregated | All NYC practices | Free | None public | LOW |
| Foursquare | Local discovery | Tips + ratings | All NYC practices | Free; $20/mo enhanced | Places API | VERY LOW |
| **NYC-SPECIFIC** | | | | | | |
| DentistDirectory.com | Dental directory | None | Limited | Free | None public | VERY LOW |
| NY State Dept of Health (license lookup) | License verification | None | All licensed dentists | N/A (public record) | Public data | LOW (trust signal only) |

---

## Platform Detail: Tier 1 (Must-Have)

### 1. Google Business Profile
- URL: https://business.google.com
- 81% of new dental patients rely on Google; Google hosts 73% of all online reviews
- Reviews: unverified patient, 1-5 star + text, owner can respond
- NYC listings: ~2,300+; essentially every active practice
- Cost: Free (paid Local Service Ads available separately)
- API: Google Business Profile API (enterprise only); Google Places API (public, metered)
- Importance: Dominates "dentist near me" searches; affects local pack rankings; source for AI-generated answers (ChatGPT, Google AI Overview)

### 2. Zocdoc
- URL: https://www.zocdoc.com
- Reviews: verified post-appointment only — highest trust signal in category
- NYC listings: 315+ Manhattan; estimated 1,000+ citywide
- Cost: Free (Practice Solutions tier); Marketplace = pay-per-new-patient-booking (no monthly fee)
- API: Official scheduling API at api-docs.zocdoc.com; Apify community scrapers available ($29.99/mo + usage)
- Importance: Highest booking-intent platform in NYC; shows live availability + insurance; converts browsers to booked patients faster than any other platform

### 3. Healthgrades
- URL: https://www.healthgrades.com
- Reviews: multi-factor surveys (wait time, staff, communication), 1-5 star; 200M+ national reviews; 30M monthly visits
- NYC listings: 8,517+ within 10 miles of NYC
- Cost: Free basic; paid Featured (top placement, website link, click-to-call, booking widget)
- API: Apify scrapers (community, $19/mo); reviewapi.com ($0–$399/mo tiered); official API via WebMD Care Directories partnership
- Importance: Ranks on page 1 of Google for branded doctor searches; high domain authority; "Patient Favorite" badge boosts credibility

### 4. Yelp
- URL: https://www.yelp.com
- Reviews: unverified, 1-5 star + long-form text; algorithm filters reviews from new/inactive accounts (risk: valid reviews hidden)
- NYC listings: 4,000+; 308M reviews total on platform as of 2025
- Cost: Free basic; paid Sponsored Results
- API: Yelp Places API — $5.91–$14.13 per 1,000 calls; requires API key
- Importance: 44% of patients check Yelp; strong for detailed narrative reviews; Yelp listings appear in Google organic results; cited by AI search tools

---

## Platform Detail: Tier 2 (Important)

### Insurance Directories
All function the same way: patients log into their insurance portal, search for in-network dentists by ZIP/specialty. No patient reviews. Dentists are auto-listed when they join the network.

| Insurer | URL | Notes |
|---|---|---|
| Delta Dental | deltadental.com | Largest dental insurer nationally; most important in NYC |
| Cigna | hcpdirectory.cigna.com | Large NYC employer base |
| Aetna | aetna.com/find-a-doctor | "Smart Compare" highlights top-quality providers |
| United Healthcare | uhc.com/find-a-doctor | Substantial NYC membership |
| Guardian | guardianlife.com/find-a-dentist | 138K+ provider network; popular with NYC employers |
| MetLife | providers.online.metlife.com | Large dental-only subscriber base |

### Social
- Facebook: 45% of patients check before booking; best for community/retention
- Instagram: Strongest for under-40 demographics; visual treatment results, Reels, staff personality
- Nextdoor: Best in outer boroughs (Park Slope, Forest Hills, Astoria); verified neighbor recommendations carry high credibility; less useful in transient Manhattan neighborhoods

### Other Tier 2
- WebMD/Vitals: vitals.com (owned by WebMD); Featured profiles syndicate to both; 26.79% of patients use Healthgrades vs. lower for Vitals, but WebMD brand association adds credibility
- ADA Find-a-Dentist: findadentist.ada.org — filters by specialty, language, insurance; credibility signal more than volume driver
- 1-800-Dentist: join1800dentist.com — pay ~$40-50/call for verified phone leads; 70,000+ calls/month nationally; good for capacity filling

---

## Key Stats for NYC

| Metric | Data | Source |
|---|---|---|
| Patients using online reviews to choose dentist | 73.28% | Repugen 2025 Survey |
| Patients who trust online reviews | 91.27% | Repugen 2025 Survey |
| Patients who search online before booking | 71–77% | Multiple sources |
| Patients using Google first | 66–81% | Repugen / BrightLocal 2024 |
| Patients using Yelp | 44% | Chatmeter 2025 |
| Patients using Healthgrades | 26.79% | Repugen 2025 |
| Patients preferring providers who respond to reviews | 59.48% | Repugen 2025 |
| Patients who consider reviews >2 years old as outdated | 40% | Repugen 2025 |
| Patients unlikely to choose provider under 4 stars | 72% | Chatmeter 2025 |
| NYC licensed dentists (Manhattan/NY County) | ~2,541 | NY State license data |

---

## API / Scraping Quick Reference

| Platform | Method | Cost |
|---|---|---|
| Google | Places API | Metered; GBP API = enterprise |
| Yelp | Places API | $5.91–$14.13 / 1K calls |
| Healthgrades | Apify community scrapers | $19/mo + usage |
| Zocdoc | Apify community scrapers | $29.99/mo + usage |
| Healthgrades (reviews) | reviewapi.com | Free–$399/mo tiered |
| NPI Registry (license data) | npiregistry.cms.hhs.gov/api | Free, public |
| NY State license DB | health.ny.gov | Free, public |

---

## NYC-Specific Notes

- Manhattan market is saturated; comprehensive Tier 1 presence is table stakes
- Outer boroughs (Brooklyn, Queens): Nextdoor + Yelp + Google matter more; less Zocdoc competition
- Multilingual practices: Healthgrades and Zocdoc support language filters — high value for NYC's immigrant populations
- AI search (ChatGPT, Perplexity, Google AI Mode): pulls from Google Business Profile, Healthgrades, and review content — platform coverage now affects AI discovery even without direct platform visits
- DSO competition: large chains dominate Zocdoc and Google Ads; independent practices must differentiate on reviews and niche specialization

---

*Sources: Repugen Patient Review Survey 2025, BrightLocal Local Consumer Review Survey 2024, Chatmeter 2025, SocialPilot 2025, Apify platform listings, Zocdoc API docs, Healthgrades platform data, 2740consulting.com dental marketing statistics*
