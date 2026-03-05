# Plan: Geo Content Skill — Local SEO Content Engine for Dental Clinics
**Status:** PLAN (not started) | **Date:** 2026-03-02

## TL;DR

A "Geo Skill" that acts as a local SEO brain for each dental clinic. It discovers what people in a specific city/neighborhood actually search for, then auto-generates and distributes content across blog, X/Twitter, Reddit, Quora, and local forums — all optimized for local search intent. The goal: make each clinic the #1 result for "[service] + [city]" queries without them lifting a finger.

---

## What This Skill Does

```
Input:  Clinic name, city, services, language
Output: Blog posts, tweets, Reddit answers, Quora answers — all geo-targeted, published automatically
```

Three core capabilities:

1. **Keyword Discovery** — Find what locals actually search for (Hebrew + English)
2. **Content Generation** — Blog posts, social posts, forum answers per keyword cluster
3. **Multi-Channel Publishing** — Push content to blog, X, Reddit, Quora, local directories

---

## Phase 1: Keyword Discovery Engine

### How It Finds Important Words & Phrases

| Source | What It Extracts | Method |
|--------|-----------------|--------|
| **Google Autocomplete** | Real search suggestions for "[service] [city]" | SerpAPI / ValueSERP autocomplete endpoint |
| **Google "People Also Ask"** | Question-format queries locals ask | SerpAPI PAA extraction |
| **Google Related Searches** | Bottom-of-SERP related terms | SerpAPI related_searches |
| **Competitor blog analysis** | Keywords competitors rank for | Scrape top 5 dental sites in city, extract H1/H2/meta |
| **Google Trends (IL)** | Seasonal spikes for dental terms in Israel | Google Trends API (pytrends) |
| **Clinic's own Google reviews** | Natural language patients use | Already scraped in `gush-dan-dental-clinics.csv` |
| **Reddit/Quora threads** | Questions people ask in forums about dental in Israel | Apify Reddit scraper |

### Keyword Clustering Logic

```
Raw keywords → Deduplicate → Cluster by intent → Score by volume + competition → Assign to content type
```

| Intent Type | Example Keywords (Hebrew + English) | Content Type |
|------------|-------------------------------------|-------------|
| **Transactional** | "רופא שיניים בבת ים", "dentist bat yam appointment" | Blog (service page), Google Business post |
| **Informational** | "כמה עולה השתלת שיניים", "how much dental implant israel" | Blog (guide), Quora answer |
| **Comparison** | "הלבנת שיניים מחיר השוואה", "best dentist petah tikva" | Blog (comparison), Reddit comment |
| **Problem-aware** | "כאב שיניים בלילה מה לעשות", "tooth pain at night" | Blog (FAQ), tweet thread |
| **Local navigation** | "מרפאת שיניים פתוחה בשבת חולון" | Blog (hours page), Google Business |

### Output: Keyword Map Per Clinic

A JSON/CSV file per clinic with:
- Keyword (Hebrew + English variant)
- Search intent
- Estimated monthly volume (from autocomplete frequency)
- Competition level (# of ranking pages)
- Assigned content type (blog/tweet/reddit/quora)
- Priority score (1-10)

---

## Phase 2: Content Generation

### Content Types & Templates

| Channel | Format | Length | Frequency | Language |
|---------|--------|--------|-----------|----------|
| **Blog post** | SEO article with H2s, FAQ schema | 800-1200 words | 4-8/month per clinic | Hebrew (primary) + English variant |
| **X/Twitter post** | Tip/fact + CTA + local hashtag | 280 chars | 3-5/week | Hebrew |
| **Reddit answer** | Helpful answer in r/Israel, r/TelAviv, dental subs | 100-300 words | 2-4/month | Hebrew or English (per sub) |
| **Quora answer** | Expert answer to dental questions with clinic mention | 200-400 words | 2-4/month | English (Quora IL is English-heavy) |
| **Google Business post** | Short update + photo + CTA | 100-200 words | 2/week | Hebrew |

### Blog Post Structure (Template)

```
Title: [Primary Keyword] — [Clinic Name], [City]
Meta: [155 chars with keyword + city + CTA]
H1: [Primary keyword natural phrasing]
Intro: 2 sentences answering the query directly
H2: [Sub-topic 1 from "People Also Ask"]
H2: [Sub-topic 2]
H2: [Sub-topic 3]
FAQ Section: 3-5 questions from PAA (structured data / schema.org)
CTA: "קבעו תור ב[Clinic Name] — [phone] | [city]"
Internal links: to clinic's service pages
```

### Content Generation Pipeline

```
Keyword map → Claude (Sonnet) generates draft → Compliance check → Hebrew grammar check → Publish
```

| Step | Tool | Details |
|------|------|---------|
| Draft generation | Claude API (Sonnet) | Prompt includes: keyword, intent, clinic data, tone, compliance rules |
| Compliance filter | Claude API (Haiku) | Check for medical claims, guarantees, HIPAA issues (same rules as Instagram) |
| Hebrew quality | Claude API (Haiku) | Grammar, natural phrasing, no translationese |
| SEO validation | Custom script | Title length, meta description, keyword density, FAQ schema markup |

---

## Phase 3: Multi-Channel Publishing

### Publishing Targets & Methods

| Channel | API/Method | Account Needed | Automation Level |
|---------|-----------|----------------|------------------|
| **Clinic blog** (WordPress/Wix) | WordPress REST API / Wix API | Clinic grants access | 90% auto (publish as draft, clinic approves) |
| **X/Twitter** | X API v2 (Basic = $200/mo) | Create per-clinic or agency account | 100% auto |
| **Reddit** | Reddit API (free) | Agency account, age + karma requirements | 50% auto (draft → human posts to avoid ban) |
| **Quora** | No official API — Playwright automation | Agency account | 30% auto (semi-manual to avoid detection) |
| **Google Business** | Google Business Profile API | Clinic grants access via OAuth | 90% auto |

### Reddit Strategy (Careful — Anti-Spam)

Reddit is high-value but aggressive on spam detection. The approach:

1. **Don't create clinic accounts** — use a genuine "dental advice" account
2. **Never link directly to clinic** — answer genuinely, mention clinic name naturally only when relevant
3. **Target subreddits:** r/Israel, r/TelAviv, r/askdentists (English), city-specific subs
4. **Monitor threads** asking about dentists in specific cities → reply helpfully
5. **Volume:** Max 2-3 posts/week from same account; rotate accounts if scaling

### X/Twitter Strategy

| Post Type | Example | Frequency |
|-----------|---------|-----------|
| Dental tip + city hashtag | "שלוש טעויות שכולם עושים בצחצוח 🦷 #רופאשיניים #בתים" | 3/week |
| Question-format engagement | "ידעתם שהלבנת שיניים לוקחת רק 45 דקות? ב[City] אפשר לקבוע היום" | 2/week |
| Seasonal hook | "לפני החגים — הזמן לבדיקה. [Clinic Name] פתוחה עד ה-..." | 1/week |
| Review highlight | "תודה ל[First Name] על ה-⭐⭐⭐⭐⭐! 'הרופא הכי סבלני שפגשתי'" | 1/week |

---

## What It Needs From Each Clinic

| Asset | Required? | Used For |
|-------|-----------|----------|
| Clinic name + city (already have) | Yes | All content |
| Services list (already have generic) | Yes | Keyword targeting |
| Blog CMS access (WordPress/Wix login) | For blog publishing | Blog posts |
| Google Business access (OAuth) | For GMB posts | Google Business posts |
| Specific promotions/prices | Optional | Transactional content |
| Doctor specialties/credentials | Recommended | Authority signals in content |

**For our 439 clinics:** We already have name, city, services, rating, reviews. Missing: blog access (most don't have blogs — we'd create one as part of the website we already generate for them).

---

## Integration With Existing Systems

| Existing Asset | How Geo Skill Uses It |
|----------------|----------------------|
| `gush-dan-dental-clinics.csv` (439 clinics) | Seed data: name, city, rating, reviews |
| `content.md` per clinic (S4 reports) | Doctor name, services, hours, address |
| S4 generated websites | Blog section target — add /blog route |
| Instagram content strategy (7 clusters) | Repurpose clusters as blog topic pillars |
| Topic clusters + SEO keywords | Starting keyword seeds — expand with geo modifiers |
| Existing Google reviews (scraped) | Mine for natural language keywords patients use |

---

## Cost Estimate Per Clinic Per Month

| Item | Quantity | Unit Cost | Monthly |
|------|----------|-----------|---------|
| Keyword discovery (SerpAPI) | 50 queries/month | $0.01/query | $0.50 |
| Blog post generation (Claude Sonnet) | 6 posts | ~$0.15/post | $0.90 |
| Social posts (Claude Haiku) | 20 tweets + 4 Reddit + 4 Quora | ~$0.005/post | $0.14 |
| Compliance check (Haiku) | 34 pieces | ~$0.003/check | $0.10 |
| X API (shared across clinics) | Basic tier | $200/mo ÷ clinics | $2.00 (at 100 clinics) |
| **Total per clinic** | | | **~$3.64/mo** |

**Combined with visual content plan:** ~$5.62 (visuals) + $3.64 (geo) = **~$9.26/clinic/month** for full content + SEO engine.

---

## Build Phases

| Phase | What | Effort | Dependency |
|-------|------|--------|------------|
| **Phase 1** | Keyword discovery module: SerpAPI integration, autocomplete + PAA scraping, clustering logic | 2-3 days | SerpAPI key |
| **Phase 2** | Content generation templates: blog post, tweet, Reddit answer, Quora answer prompts | 1-2 days | Phase 1 (keyword map) |
| **Phase 3** | Blog publishing pipeline: WordPress/Wix API integration, or add /blog to S4 websites | 2-3 days | Phase 2 |
| **Phase 4** | X/Twitter publishing: API setup, scheduling queue, hashtag injection | 1-2 days | X API Basic tier ($200) |
| **Phase 5** | Reddit/Quora monitoring: keyword alerts, thread detection, semi-auto reply drafts | 2-3 days | Phase 2 |
| **Phase 6** | Google Business posts: OAuth flow, post scheduling | 1-2 days | Clinic grants access |
| **Phase 7** | Reporting dashboard: keyword rankings tracked over time, content performance | 2-3 days | All above |
| **Phase 8** | Pilot: run for 5 clinics for 1 month, measure ranking changes | 1 month | All above |

**Total to MVP:** ~2 weeks dev + 1 month pilot.

---

## Key Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Reddit bans for promotional content | Never link directly; genuine helpful answers only; max 2-3/week; rotate accounts |
| Quora detection of automated posting | Semi-manual with Playwright; vary timing + phrasing; 1-2/week max |
| Duplicate content across 439 clinics | Each clinic gets unique city/neighborhood/doctor modifiers; never copy-paste between clinics |
| Hebrew SEO data is thin (low volume) | Supplement with English keywords for dental tourism angle; use autocomplete as proxy for volume |
| Google penalizes thin blog content | 800+ words minimum; real FAQ schema; internal linking; update quarterly |
| X API cost at $200/mo | Share across all clinics; start with 10-20 clinics to validate ROI before scaling |
| Clinic doesn't have a blog | We already generate S4 websites — add a `/blog` section as upsell |

---

## Success Metrics (Per Clinic, After 3 Months)

| Metric | Target |
|--------|--------|
| Blog posts indexed by Google | 15+ pages |
| Keywords ranking on page 1 (Hebrew) | 5-10 local keywords |
| Organic traffic increase | +30-50% from baseline |
| Google Business profile views | +20% |
| "Near me" / "[city] dentist" visibility | Top 5 in Google Maps pack |
| Reddit/Quora referral traffic | 50+ visits/month |
