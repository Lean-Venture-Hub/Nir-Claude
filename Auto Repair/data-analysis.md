# Auto Repair Leads — Data Analysis
**Date:** 2026-03-14 | **Enriched file:** s4-leads-enriched.csv | **Main file:** apify-all-auto-repair.csv

---

## Full Pipeline Overview (apify-all-auto-repair.csv)

| Segment | Name | Count | % of Total |
|---------|------|-------|-----------|
| 0 | Excluded (Chain/Bad) | 734 | 54.2% |
| 4b | No Website + Good | 382 | 28.2% |
| 4 | No Website (unscored) | 78 | 5.8% |
| 4a | No Website + Some | 62 | 4.6% |
| 2 | Warm Digital | 60 | 4.4% |
| 1 | Leaky Funnel | 29 | 2.1% |
| 3 | Reputation Rescue | 10 | 0.7% |
| **Total** | | **1,355** | |

**Target pool (S4a + S4b):** 444 leads

**Cities (main CSV):** Houston 611, Phoenix 662, suburbs ~82

---

## 1. Segment Breakdown — Enriched File (n=444)

| Segment | Name | Count | % |
|---------|------|-------|---|
| 4b | No Website + Good | 382 | 86% |
| 4a | No Website + Some | 62 | 14% |

**Key difference:** S4a = low review count (avg 7, median 6). S4b = established shops (avg 79, median 50).

---

## 2. City Distribution

| City | Count | % |
|------|-------|---|
| Houston | 256 | 57.7% |
| Phoenix | 173 | 39.0% |
| Suburbs (Sugar Land, Humble, Kingwood, etc.) | 15 | 3.3% |

---

## 3. Rating Distribution (n=444)

| Metric | Value |
|--------|-------|
| Average | 4.53 |
| Median | 4.60 |
| Min / Max | 2.8 / 5.0 |

| Rating Bucket | Count | % |
|---------------|-------|---|
| 5.0 exact | 54 | 12% |
| 4.5 – 4.9 | 243 | 55% |
| 4.0 – 4.4 | 108 | 24% |
| 3.0 – 3.9 | 38 | 9% |
| Below 3.0 | 1 | <1% |

**By segment:** S4a avg 4.46 vs S4b avg 4.54 — negligible difference. Both are high-quality shops by rating.

---

## 4. Review Count Distribution (n=444)

| Bucket | Count | % |
|--------|-------|---|
| 1–5 reviews | 26 | 6% |
| 6–15 | 81 | 18% |
| 16–30 | 88 | 20% |
| 31–50 | 59 | 13% |
| 50+ | 190 | 43% |

| Metric | S4a | S4b |
|--------|-----|-----|
| Avg reviews | 7 | 79 |
| Median reviews | 6 | 50 |

**Implication:** S4b shops are well-established local businesses with real traction. S4a is very early-stage (likely opened <1 year).

---

## 5. Social Presence

### Overall (n=444)

| Channel | Count | % |
|---------|-------|---|
| Facebook | 233 | 52.5% |
| Email | 189 | 42.6% |
| Instagram | 141 | 31.8% |
| FB + IG | 133 | 30.0% |
| All 3 (FB + IG + Email) | 98 | 22.1% |
| None of the above | 188 | 42.3% |

### By Segment

| Metric | S4a (n=62) | S4b (n=382) |
|--------|-----------|------------|
| Has Facebook | 76% | 49% |
| Has Instagram | 47% | 29% |
| Has Email | 55% | 41% |
| Has All 3 | 34% | 20% |
| Has None | 19% | 46% |

**Insight:** S4a shops are significantly more socially active despite having fewer reviews — they're newer/more digitally aware but haven't accumulated proof yet. S4b is the larger volume but nearly half have zero social presence, making them cold-contact only via phone.

---

## 6. Review Sentiment — 20 Sample Reviews

**Theme categories identified:**

| Theme | Frequency in Sample | Signal |
|-------|-------------------|--------|
| Trust / Honesty | 9/20 (45%) | "honest," "didn't upsell," "trust him more than any mechanic" |
| Quality of work | 8/20 (40%) | "great work," "excellent job," "incredible results" |
| Fair pricing | 7/20 (35%) | "good prices," "affordable," "fair price" |
| Speed / Convenience | 4/20 (20%) | "same day," "out in no time," "before 3pm" |
| Long-term relationship | 5/20 (25%) | "30 years," "over a decade," "since 1984" |
| Negative — broken trust | 2/20 (10%) | price changes, car held too long, mockery |

**Key takeaway:** The dominant buying trigger for auto repair customers is TRUST, not price. Reviews overwhelmingly mention honesty and not being ripped off over speed or cost. Marketing angle should lead with credibility, not discounts.

---

## 7. Top Service Categories

| Category | Count |
|----------|-------|
| Auto repair shop (general) | 313 |
| Auto body shop | 39 |
| Mechanic | 36 |
| Tire shop | 32 |
| Car repair and maintenance service | 23 |
| Oil change service | 23 |
| Brake shop | 21 |
| Transmission shop | 16 |
| Wheel alignment service | 12 |
| Auto air conditioning service | 10 |
| Auto tune up service | 10 |
| Muffler shop | 9 |
| Car inspection station | 9 |

**Most common profile:** General mechanic/repair shop. Specialty shops (tires, brakes, transmission, AC) represent meaningful sub-segments with distinct service needs.

---

## What's Working

- **Large target pool:** 444 qualified S4 leads across 2 cities — enough for multiple campaign waves
- **Rating quality:** 91% rate 4.0+, 67% rate 4.5+ — these are legitimately good businesses worth helping
- **Social hooks exist:** 57.7% have at least one contact channel (FB, IG, or email) beyond phone
- **S4b volume:** 382 established shops with real review volume = proof of business viability

## What's Not Working

- **42.3% have zero social presence** — no FB, IG, or email found. Phone outreach only for nearly half the list
- **S4a small pool:** Only 62 leads, and they're very early-stage (median 6 reviews). Lower conversion likelihood
- **City concentration risk:** 96.7% of leads are Houston or Phoenix. One bad campaign tanks the whole list

## Kill List

- Stop treating S4a and S4b as a single outreach cohort — their profiles are fundamentally different (7 vs 79 avg reviews, 19% vs 46% zero social)
- Stop leading outreach with pricing/features — trust/honesty is the #1 theme in reviews, messaging should match

## Double Down

- **S4b with email:** 155 leads (~35%) have verified emails + established review counts. Highest-yield segment for cold email
- **FB-only shops (no website, has FB):** Clear pain point — they know social exists but haven't built a site. Natural entry for web + local SEO pitch

## Test Next

| Experiment | Hypothesis | Method | Success Criteria |
|-----------|-----------|--------|-----------------|
| Trust-first outreach copy | Leads convert better when copy mirrors their customers' "honest mechanic" language | A/B two email variants: trust-led vs. results-led | >2x reply rate on trust variant |
| S4b email-only mini-wave | Verified email + 50+ reviews = highest intent signal | Send 30 emails to S4b leads with email, track replies | 3+ positive responses in 7 days |
| Phoenix vs Houston split | Phoenix shops may be at different adoption stage than Houston | Compare reply rates by city in first 60 outreaches | Determine which city gets second wave first |
