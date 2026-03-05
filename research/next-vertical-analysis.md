# Next SMB Vertical After Dentists: Analysis & Recommendations

## TL;DR

After scoring 10 candidate verticals against our dentist-baseline criteria (high revenue per location, fragmented ownership, digital gap, scannable public data, willingness to pay), **the top 3 are: (1) Med Spas, (2) Veterinary Clinics, and (3) Dermatology Practices**. Med spas win on revenue growth (15.8% CAGR), marketing spend (7% of revenue avg), and digital gap among single-owner operators. Veterinary clinics offer the largest fragmented base (~28K independent practices) with extremely low online booking adoption. Dermatology combines high revenue per provider ($1.3-1.8M) with a heavily fragmented market (40% solo practices). All three share the "dentist-like" traits: public GBP/reviews, clear website audit value prop, and owner-operators who make buying decisions fast.

---

## Part 1: Vertical Selection Frameworks

| # | Method | Data Sources | What It Measures |
|---|--------|-------------|------------------|
| 1 | **Revenue-per-Location Screen** | BLS, Census SUSB, IBISWorld, ProjectionHub | Filters out verticals where avg location revenue is too low to justify $500-2K/mo services |
| 2 | **Fragmentation Index** | IBISWorld (market share of top 4), Census, industry associations | % independent vs chain/PE-owned. Higher = easier sell to decision-makers |
| 3 | **Digital Maturity Audit** | Manual sampling: pull 50 GBPs per vertical, score website quality, booking, mobile, SSL | Quantifies the "gap" we exploit. Lower maturity = bigger pitch |
| 4 | **Public Data Scannability Test** | Google Maps API, Yelp API, industry directories | Can we programmatically pull profiles, reviews, website URLs at scale? |
| 5 | **Marketing Spend Benchmark** | Industry surveys (ADA, AVMA, AmSpa, ABA), Borrell Associates | What % of revenue they already spend on marketing = willingness to pay |
| 6 | **Competitive Landscape Map** | G2, Capterra, Google Ads auction insights, agency directories | Who already targets this vertical? Crowded = harder; empty = maybe no demand |
| 7 | **Regulatory Friction Check** | Industry-specific compliance (HIPAA, state licensing, advertising rules) | Does regulation limit what we can say/do in outreach or on their website? |

**Validation before committing:** Run a 50-business pilot scan in 2 metros. If >60% have identifiable gaps (bad website, <20 reviews, no online booking), the vertical passes.

---

## Part 2: Top 10 Candidate Verticals (Scored)

**Dentist baseline for comparison:** ~$800K avg revenue/location, ~130K practices (50% solo), 4-7% marketing spend, strong GBP/review ecosystem, moderate digital maturity.

**Scoring: 1-5 scale (5 = best fit for our model)**

| Vertical | Rev/Location | # Independent | Digital Gap | Scannable Data | Mktg Spend | Competition | Reg. Complexity | **Total /35** |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Med Spas** | 4 ($300K-1M+) | 4 (42% single-owner, ~10K+) | 5 (50% lack digital mktg) | 5 (GBP, Yelp, RealSelf) | 5 (7% avg revenue) | 3 (crowded but growing) | 3 (medical oversight varies by state) | **29** |
| **Veterinary Clinics** | 4 ($600K-1.8M) | 5 (65% independent, ~28K) | 5 (<10% online booking) | 5 (GBP, Yelp, AVMA directory) | 4 (5-10% revenue) | 3 (PetDesk, Vetstoria exist) | 4 (minimal ad restrictions) | **30** |
| **Dermatology** | 5 ($1.3-1.8M/provider) | 4 (40% solo, ~5.3K practices) | 4 (many outdated sites) | 5 (GBP, Healthgrades, Zocdoc) | 5 (8-15% revenue) | 3 (Cardinal, PatientGain) | 3 (HIPAA, medical advertising rules) | **29** |
| **Optometry** | 4 ($973K avg) | 4 (~22.9K practices) | 4 (60% spend <$500/mo mktg) | 4 (GBP, Yelp, VSP directory) | 3 (1-2% typical) | 4 (less targeted) | 3 (HIPAA) | **26** |
| **Chiropractors** | 2 ($140-200K/provider) | 5 (>95% independent, ~70K) | 4 (many poor sites) | 5 (GBP, Yelp) | 3 (5-10% revenue, but low base) | 3 (The Smart Chiropractor, etc.) | 4 (minimal) | **26** |
| **Solo/Small Law Firms** | 3 (varies widely) | 4 (~450K solo/small firms) | 4 (30% solos lack website) | 4 (GBP, Avvo, state bar dirs) | 2 (only 14% solos have mktg budget) | 2 (very crowded: Clio, FindLaw, Scorpion) | 3 (bar advertising rules) | **22** |
| **Home Services (HVAC/Plumbing)** | 3 ($500K-2M varies) | 4 (highly fragmented) | 3 (improving fast) | 3 (GBP, Angi, HomeAdvisor) | 4 (aggressive spenders) | 2 (ServiceTitan, Housecall Pro, many agencies) | 5 (minimal) | **24** |
| **CPA/Accounting Firms** | 3 ($200K-1M) | 4 (~90K small firms) | 4 (many basic sites) | 3 (GBP, limited review culture) | 2 (low marketing culture) | 4 (less targeted) | 3 (compliance content needs) | **23** |
| **Property Management** | 2 (<$500K avg) | 4 (~330K companies) | 3 (tech adoption high at 85%) | 3 (GBP, Yelp, Zillow) | 2 (low marketing focus) | 2 (AppFolio, Buildium, many agencies) | 3 (state regulations vary) | **19** |
| **Auto Body/Repair** | 2 ($300-600K) | 4 (~32K+ body shops) | 4 (many poor sites) | 4 (GBP, Yelp, CarFax) | 3 ($500-2K/mo) | 3 (AutoShop Solutions, Kukui) | 5 (minimal) | **25** |

---

## Part 3: Top 3 Recommendations

### 1. Veterinary Clinics (Score: 30/35)

**Why:** Most "dentist-like" vertical available.

| Dimension | Dentists | Veterinary |
|-----------|----------|------------|
| Avg revenue/location | $800K | $600K-1.8M |
| Independent % | ~50% solo | ~65% independent |
| # of practices | ~130K | ~28K independent |
| Online booking adoption | Moderate | <10% (massive gap) |
| Review ecosystem | Strong (Google) | Strong (Google, Yelp) |
| Marketing spend | 4-7% revenue | 5-10% revenue |
| Decision-maker | Owner-dentist | Owner-vet |

**Key advantages:** Enormous digital gap (especially online booking), emotional category (pet owners leave reviews), growing PE consolidation creates urgency for independents to compete. GeniusVets acquisition by ProSites validates the market.

**Risks:** Smaller total addressable market (28K vs 130K). Revenue pressure in 2025 from declining visit volumes.

---

### 2. Med Spas (Score: 29/35)

**Why:** Fastest-growing vertical with highest marketing willingness.

| Dimension | Dentists | Med Spas |
|-----------|----------|----------|
| Avg revenue/location | $800K | $300K-1M+ |
| Independent % | ~50% solo | ~42% single-owner |
| Market growth | Steady | 15.8% CAGR |
| Marketing spend | 4-7% | 7% avg (up to 15%) |
| Review ecosystem | Google | Google, Yelp, RealSelf |
| Digital sophistication | Moderate | Low-moderate (50% lack digital mktg) |

**Key advantages:** Owners are marketing-hungry (aesthetic business = vanity metrics matter). High AOV per customer means ROI from our service is easy to demonstrate. Rapidly growing market = new practices opening constantly that need websites immediately. RealSelf as an additional data source for scanning.

**Risks:** More competition from specialized med spa marketing agencies (Brenton Way, Growth99, SagaPixel). Higher churn risk as med spas fail faster than medical practices.

---

### 3. Dermatology Practices (Score: 29/35)

**Why:** Highest revenue per provider with proven marketing spend.

| Dimension | Dentists | Dermatology |
|-----------|----------|-------------|
| Avg revenue/location | $800K | $1.3-1.8M/provider |
| Independent % | ~50% solo | ~40% solo, 73% have <5 physicians |
| # of practices | ~130K | ~5.3K |
| Marketing spend | 4-7% | 8-15% (cosmetic derm) |
| Review ecosystem | Google | Google, Healthgrades, Zocdoc |
| Avg mktg budget | $2-5K/mo | $5-15K/mo |

**Key advantages:** Highest revenue = highest willingness to pay. Cosmetic derm practices spend aggressively on marketing. Fewer total practices means we can achieve high market penetration faster. Strong review culture on multiple platforms = rich scanning data.

**Risks:** Smaller TAM (~5.3K practices). PE consolidation is active (top practices being acquired). HIPAA compliance adds friction to website/content work.

---

## Next Steps

1. **Pilot scan (1 week):** Pick one vertical (recommend veterinary). Scrape 100 GBPs across 3 metros. Score website quality, review count, online booking presence, mobile responsiveness.
2. **Outreach test (2 weeks):** Build 10 audit reports for worst-scoring practices. Cold email/call with personalized gap analysis. Measure response rate.
3. **Compare to dentist baseline:** If pilot response rate is within 50% of dentist outreach performance, green-light the vertical.
4. **Parallel validation:** While piloting vet, run the same 100-GBP scan for med spas to have a backup vertical ready.

---

## Sources

- [AVMA Veterinary Industry Tracker](https://www.avma.org/resources-tools/veterinary-economics/veterinary-industry-tracker)
- [PetDesk 2025 Veterinary Stats](https://petdesk.com/blog/2025-veterinary-industry-stats)
- [AmSpa Med Spa State of Industry Report](https://americanmedspa.org/resources/med-spa-statistics)
- [Grand View Research - Medical Spa Market](https://www.grandviewresearch.com/industry-analysis/medical-spa-market)
- [IBISWorld - Dermatologists in the US](https://www.ibisworld.com/united-states/industry/dermatologists/4168/)
- [FOCUS Bankers - Dermatology Practice Valuation 2025](https://focusbankers.com/dermatology-practice-valuation/)
- [ABA 2024 Solo/Small Firm TechReport](https://www.americanbar.org/groups/law_practice/resources/tech-report/2024/2024-solo-and-small-firm-techreport/)
- [Clio 2025 Legal Trends Report](https://www.clio.com/blog/solo-small-law-firms-highlights-2025-legal-trends/)
- [ProjectionHub - Veterinary Clinic Profitability](https://www.projectionhub.com/post/opening-a-profitable-vet-clinic-numbers-you-need-to-know)
- [ProjectionHub - Chiropractor Financial Statistics](https://www.projectionhub.com/post/9-chiropractor-industry-financial-statistics)
- [Overjet - Average Dental Practice Revenue 2025](https://www.overjet.com/blog/average-dental-practice-revenue-in-2025-complete-breakdown-by-specialty)
- [WebFX - Home Services Marketing Benchmarks 2026](https://www.webfx.com/blog/home-services/home-services-marketing-benchmarks/)
- [Schwab 2025 RIA Benchmarking Study](https://www.aboutschwab.com/ria-benchmarking-study-2025)
- [iPropertyManagement - PM Industry Statistics](https://ipropertymanagement.com/research/property-management-industry-statistics)
- [Salon Industry Trends 2025 - Boulevard](https://www.joinblvd.com/blog/salon-trends-industry-statistics)
- [IDOC - Optometrist Marketing Spend](https://idoc.net/blog/630/how-much-should-an-independent-optometrist-spend-on-marketing)
- [Vertical IQ - Optometry Practices](https://verticaliq.com/product/optometry-practices/)
- [Boomcloud - Optometry Benchmarks](https://boomcloudapps.com/optometry-benchmarks-where-should-your-practice-be-and-how-the-heck-do-you-get-there/)
- [Brenton Way - Med Spa Marketing Trends 2026](https://brentonway.com/med-spa-marketing-stats-trends/)
- [PMC - Resurgent US Independent Veterinary Practice SWOT](https://pmc.ncbi.nlm.nih.gov/articles/PMC12106480/)
