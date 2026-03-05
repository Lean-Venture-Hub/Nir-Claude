# Plan: Content Strategy → Real Instagram Visuals
**Status:** PLAN (not started) | **Date:** 2026-03-02

## TL;DR

Turn the 7 content clusters + 90-day calendar into production-ready Instagram Stories and Reels for 439 dental clinics. The system uses a 3-layer pipeline: (1) Claude generates structured content briefs per clinic, (2) AI tools generate visuals, (3) a branding layer adds Hebrew text + logo + colors. Estimated cost: ~$4-8/clinic/month for 90 stories + 4-8 Reels.

---

## The Problem

We have strategy docs (clusters, calendar, hooks) but zero visual assets. Each clinic needs **~90 stories/month + 4-8 Reels**, personalized with their name, city, colors, and logo. Content is in Hebrew. No tool generates Hebrew text in images reliably.

---

## Recommended Tool Stack

| Layer | Tool | Why This One | Cost |
|-------|------|-------------|------|
| **Content brief generation** | Claude API (Haiku) | Cheapest/fastest for structured JSON briefs | ~$0.50/clinic/mo |
| **Images — template-based** (70%) | HTML/CSS → Puppeteer screenshot | Free, full Hebrew control, brand-locked | Free (server cost only) |
| **Images — AI-generated** (30%) | Imagen 4 Fast (Gemini API) | $0.02/image, API-ready, photorealistic | ~$0.60/clinic/mo |
| **Video — Reels** | Veo 3 Fast (Gemini API) | Best price/quality, $0.15/sec | ~$3-6/clinic/mo |
| **Hebrew text overlay** | Python (Pillow) + ffmpeg | Programmatic, RTL-correct, uses brand fonts | Free |
| **Logo/color injection** | Same Pillow/ffmpeg pipeline | Per-clinic brand assets from onboarding | Free |
| **Orchestration** | n8n or Python script | Triggers daily, pulls from calendar | Free/self-hosted |
| **Publishing** | Instagram Graph API or Later | Auto-schedule stories | ~$15/mo (Later) |

**Why NOT Canva API?** No public image generation API. Their template API works but locks you into their ecosystem + pricing. HTML/CSS templates give same result with full control.

**Why NOT Seedance/Kling for video?** API access is messy (3rd-party wrappers). Veo 3 Fast has a clean first-party API via Gemini.

---

## Content Type → Visual Production Map

| Content Type | % of Posts | Visual Approach | Tool | Dentist Input? |
|---|---|---|---|---|
| Oral Health Tips | 24% | Branded text slide (bold headline + tip) | HTML template → screenshot | No |
| Fun Dental Facts | 24% | Branded text slide + icon/illustration | HTML template → screenshot | No |
| Promotions | 14% | Offer card (price, urgency, CTA) | HTML template → screenshot | Offer details only |
| Patient Reviews | 14% | Star-rating card + pull quote | HTML template → screenshot | Review text auto-pulled from Google |
| Seasonal/Holiday | 10% | AI lifestyle image + Hebrew overlay | Imagen 4 Fast + Pillow overlay | No |
| Meet the Team | 5% | Staff photo (from vault) + name/role overlay | Pillow overlay on uploaded photo | One-time photo upload |
| Smile Transformations | 5% | Before/after split frame | HTML template + uploaded photos | Photos + consent |
| **Reels** (monthly) | 4-8/mo | 5-sec cinematic clips with text | Veo 3 Fast + ffmpeg text overlay | No |

**Key insight:** ~70% of all content is text-heavy template slides. These don't need AI image generation at all — just well-designed HTML templates rendered as images.

---

## Production Pipeline (Per Clinic, Per Day)

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌──────────────┐
│ 90-Day       │ ──→ │ Claude Haiku     │ ──→ │ Visual Layer    │ ──→ │ Brand Layer   │ ──→ Publish
│ Calendar     │     │ Generates brief: │     │                 │     │              │
│ (day + slot) │     │ - headline (HE)  │     │ Template? →     │     │ + Logo       │
│              │     │ - body text (HE) │     │   HTML render   │     │ + HEX colors │
│              │     │ - visual desc    │     │ AI image? →     │     │ + Hebrew text│
│              │     │ - CTA            │     │   Imagen 4 Fast │     │ + Clinic name│
│              │     │ - category       │     │ Reel? →         │     │              │
│              │     │ - engagement     │     │   Veo 3 Fast    │     │              │
└─────────────┘     └──────────────────┘     └─────────────────┘     └──────────────┘
```

---

## What We Need From Each Clinic (Onboarding)

| Asset | Required? | Used For |
|-------|-----------|----------|
| Clinic name (Hebrew) | Yes | All posts |
| City (Hebrew) | Yes | Local hooks |
| Primary color HEX | Yes | Templates, backgrounds |
| Accent color HEX | Yes | Highlights, CTAs |
| Logo (PNG, transparent) | Yes | Watermark bottom-right |
| Hebrew font preference | Optional | Default: Assistant/Heebo |
| Tone (warm/professional/fun) | Yes | Claude prompt style |
| Staff photos + names | Recommended | "Meet the Team" posts |
| Google Business URL | Recommended | Auto-pull reviews |
| Active promotions | Optional | Promo posts |

**For existing 439 clinics:** We already have name, city, phone, rating, reviews, segment from `gush-dan-dental-clinics.csv`. Missing: logo, colors, photos. Options:
1. **Ask clinics** during outreach (best quality)
2. **Auto-generate** brand colors from their website/Google listing (scrape dominant colors)
3. **Assign from template palette** based on segment mapping (we already have this)

---

## Reels Strategy — What Veo 3 Generates

| Reel Type | Prompt Pattern | Frequency |
|-----------|---------------|-----------|
| "Did you know?" fact | Cinematic close-up of teeth/smile + text overlay | 2/month |
| Seasonal mood | Holiday-themed dental scene (e.g., pumpkin + toothbrush) | 1/month |
| "Visit your dentist" reminder | Happy patient in modern dental chair | 1/month |
| Service showcase | Whitening/Invisalign process (abstract, no real patient) | 1-2/month |
| Behind-the-scenes vibe | Clean, modern dental office walkthrough | 1/month |

**All Reels:** 5-8 seconds → ffmpeg adds Hebrew text overlay + logo + music (royalty-free library).

---

## Hebrew Text — The Critical Solve

No AI tool reliably generates Hebrew in images. Our approach:

1. **AI generates visual only** (no text baked in)
2. **Pillow (Python)** composites Hebrew text on top:
   - RTL text rendering with `arabic_reshaper` + `bidi.algorithm`
   - Brand font loaded per clinic (Heebo/Assistant from Google Fonts)
   - Text positioned per template layout (headline zone, body zone, CTA zone)
3. **For video:** ffmpeg `drawtext` filter with Hebrew font + RTL

This is the same approach professional Israeli agencies use. It's battle-tested.

---

## Cost Estimate Per Clinic Per Month

| Item | Quantity | Unit Cost | Monthly |
|------|----------|-----------|---------|
| Claude Haiku briefs | 90 stories + 6 Reels | ~$0.005/brief | $0.48 |
| AI images (Imagen 4 Fast) | ~27 (30% of stories) | $0.02 | $0.54 |
| Veo 3 Fast Reels | 6 Reels × 5 sec | $0.15/sec | $4.50 |
| HTML template renders | ~63 (70% of stories) | Free | $0.00 |
| Hebrew overlay processing | 96 assets | Free (compute) | ~$0.10 |
| **Total per clinic** | | | **~$5.62/mo** |

**At scale (100 clinics):** ~$562/month for 9,600 stories + 600 Reels.

---

## Build Phases

| Phase | What | Effort | Dependency |
|-------|------|--------|------------|
| **Phase 1** | Design 10 HTML/CSS story templates (9:16) matching the 7 content types | 2-3 days | None |
| **Phase 2** | Build the brief generator: Claude Haiku + calendar → structured JSON per clinic/day | 1-2 days | Phase 1 (template IDs) |
| **Phase 3** | Build render pipeline: JSON brief → HTML screenshot (Puppeteer) + Pillow overlay | 2-3 days | Phase 1 + 2 |
| **Phase 4** | Integrate AI image generation (Imagen 4 Fast API) for lifestyle/seasonal posts | 1 day | Phase 3 |
| **Phase 5** | Integrate Veo 3 Fast for Reels + ffmpeg text overlay | 2 days | Phase 3 |
| **Phase 6** | Build onboarding flow (collect logo, colors, tone per clinic) | 1-2 days | Phase 3 |
| **Phase 7** | Connect to Instagram Graph API or Later for auto-scheduling | 1-2 days | Phase 3+ |
| **Phase 8** | Scale test: run for 5 clinics for 1 week, review quality | 1 week | All above |

**Total to MVP:** ~2 weeks of dev work → ready for pilot with 5 clinics.

---

## Alternatives Considered & Rejected

| Option | Why Rejected |
|--------|-------------|
| **Canva API for everything** | No image generation API; template API is limited; $$ at scale |
| **Seedance 2.0 for Reels** | No stable direct API; 3rd-party wrappers are flaky |
| **Ideogram for Hebrew text** | Hebrew accuracy is ~40-60%; unreliable for production |
| **Nano Banana (Gemini Flash Image)** | Good but Imagen 4 Fast is cheaper ($0.02 vs $0.039) for our use case |
| **All AI-generated images** | Overkill — 70% of dental stories are text slides, not lifestyle photos |
| **Manual Canva design** | Doesn't scale past 5 clinics; defeats automation purpose |

---

## Key Risks

| Risk | Mitigation |
|------|------------|
| Hebrew text rendering bugs (RTL) | Use battle-tested `python-bidi` + `arabic_reshaper`; test with 50 sample strings |
| AI images look generic/stock | Strong prompts with dental-specific details; mix with HTML templates to avoid AI-overload |
| Instagram API rate limits | Queue + spread publishing across day; Later handles this natively |
| Clinic doesn't provide logo/colors | Fallback: auto-generate palette from Google listing; use generic dental icon as logo placeholder |
| Veo 3 generates weird dental scenes | Pre-approve 20 prompt templates; filter outputs for quality score before publishing |
