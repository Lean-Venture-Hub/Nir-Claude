# Instagram Content Management for Dentists — Product Roadmap

**TL;DR:** Add Instagram auto-posting as a third pillar alongside the WhatsApp assistant and website builder. MVP is a WhatsApp-gated weekly approval flow with AI-generated dental content, publishing via Instagram Graph API. Ship in 3 weeks.

---

## Pricing Table

| Tier | Price | What's Included |
|------|-------|-----------------|
| Starter | $49/mo | 3 story posts/day, AI-generated, auto-publish, no approval |
| Pro | $99/mo | 3 stories + 4 feed posts/week, weekly WhatsApp review session, basic analytics |
| Clinic | $179/mo | Everything in Pro + web dashboard, multi-account (up to 3 locations), content calendar, priority support |

**Bundling lever:** Dentists already on WhatsApp assistant get 30% off any Instagram tier. Website clients get Starter free for 60 days.

---

## Validation Experiment

**Goal:** Confirm dentists will pay and approve content before building the full system.

**Experiment (run in 2 weeks with 5 existing WhatsApp clients):**

1. Manually generate 3 story posts/day using ChatGPT + Canva templates
2. Send them via WhatsApp for approval each Sunday ("Here are your 7 posts for the week — reply YES to publish all, or EDIT [day] to change one")
3. Publish manually via Meta Business Suite
4. Measure: approval rate, time-to-reply, any edit requests, willingness to pay

**Success signal:** 4 of 5 approve within 24h, at least 3 say they'd pay $49+/mo.

**Kill signal:** Dentists ignore or complain the content doesn't feel personal enough.

---

## MVP Definition (Week 1-3)

**Build only this:**

- Content generation engine (GPT-4 with dental prompt library, 5 content types)
- WhatsApp approval flow (Sunday batch send, YES/EDIT/SKIP reply parsing)
- Auto-publish via Instagram Graph API on approved content
- Admin panel (internal only) to monitor batches, override, retry failed posts

**What MVP intentionally skips:**
- Web interface for dentists (Phase 2)
- Analytics (Phase 2)
- Feed posts / Reels (Phase 2)
- Multi-location (Phase 3)

---

## Day-0 to Day-30 Launch Sequence

| Day | Action |
|-----|--------|
| D-0 | Lock MVP scope, assign dev + content roles |
| D-2 | Build dental content prompt library (5 types x 10 prompts each) |
| D-4 | Stand up Instagram Graph API auth flow + test publishing |
| D-6 | Build WhatsApp approval parser (YES/EDIT/SKIP handling) |
| D-8 | Connect generation -> approval -> publish pipeline end-to-end |
| D-10 | Internal dogfood: run pipeline for 1 fake clinic account |
| D-12 | Onboard 3 real beta dentists (existing WhatsApp clients, free) |
| D-14 | Fix top 3 issues from beta feedback |
| D-17 | Add basic retry logic, error alerts to admin |
| D-20 | Soft-launch to full existing client list (offer at $49 intro price) |
| D-25 | First paid conversions, collect testimonials |
| D-28 | Begin Phase 2 scoping (web dashboard) based on what dentists ask for |
| D-30 | Review metrics: approval rate, churn signal, support tickets |

---

## Offer Stack

**Core offer:** "We run your dental Instagram for you. You approve in 60 seconds on WhatsApp, we handle everything else."

| Layer | What It Is |
|-------|------------|
| Core product | 3 AI-generated dental story posts per day, auto-published |
| Approval hook | Sunday WhatsApp batch — approve the week in under 2 minutes |
| Trust anchor | 30-day free trial, no contract |
| Upsell path | Web dashboard + feed posts at Pro tier |
| Bundle lock-in | Discounted when paired with WhatsApp assistant or website |
| Referral | 1 free month for every referred dentist who activates |

---

## Feature Phases

### Phase 1 — MVP (Weeks 1-3)
- GPT-4 content generation with dental prompt library
- 5 content types: oral health tip, promotion, before/after tease, FAQ, seasonal post
- WhatsApp Sunday batch approval (YES / EDIT [day] / SKIP [day])
- Auto-publish Stories via Instagram Graph API
- Internal admin panel (ops team only)

### Phase 2 — Web Interface (Weeks 4-8)
- Dentist-facing web dashboard: view weekly content calendar
- Inline edit: change caption, swap image, reschedule post
- Approve/reject individual posts from web
- Basic analytics: reach, impressions per post
- Notification: email or WhatsApp link to dashboard each Sunday

### Phase 3 — Scale (Weeks 9-16)
- Feed posts + Reels (short video templates)
- Multi-location clinic accounts
- Content personalization: pull from dentist's patient FAQs, seasonal promos
- Integration with website (pull before/after cases, promotions automatically)
- White-label option for dental marketing agencies

---

## User Flows

### Flow A — WhatsApp Approval (MVP)
```
Sunday 8am: System generates 21 posts (3/day x 7 days)
        |
Sunday 9am: WhatsApp message sent to dentist:
            "Here are your Instagram stories for next week.
             Reply YES to publish all, or EDIT [day] if you
             want to change something."
        |
Dentist replies "YES" → posts scheduled, publish at set times Mon-Sun
Dentist replies "EDIT Tue" → system asks for new caption or image preference
Dentist replies "SKIP Wed" → Wednesday posts dropped
No reply by Monday 6am → auto-publish anyway (configurable per dentist)
```

### Flow B — Web Dashboard (Phase 2)
```
Sunday: Dentist receives WhatsApp link: "Your week is ready — review here"
        |
Clicks link → Web calendar view showing Mon-Sun posts with images + captions
        |
Dentist can: Approve all (1 click) | Edit caption inline | Swap image | Delete post
        |
Hits "Publish Week" → posts scheduled and auto-published at set times
```

---

## Content Types (Dental)

| Type | Frequency | Example |
|------|-----------|---------|
| Oral health tip | 3x/week | "Brush for 2 minutes, twice a day — set a timer!" |
| Promotion / offer | 1x/week | "Whitening treatment this month — ask us about it" |
| Before/after tease | 1x/week | Blurred or illustrated case, drives DMs |
| Patient FAQ | 1x/week | "Does teeth cleaning hurt? Here's the truth." |
| Clinic/team moment | 2x/week | Staff intro, behind the scenes, clinic photo |
| Seasonal / local | As relevant | Holiday greeting, local event tie-in |

---

## Key Decisions to Make

| Decision | Options | Recommended |
|----------|---------|-------------|
| Default approval mode | Auto-publish vs require approval | Default: auto-publish, opt-in to review |
| Content images | Stock photos vs AI-generated vs Canva templates | Start with Canva templates (cheapest, fastest) |
| No-reply fallback | Auto-publish or skip | Auto-publish (dentist stays active even if lazy) |
| Story vs Feed first | Stories only vs both | Stories only in MVP (simpler API, less design) |
| Web dashboard timing | Build now vs Phase 2 | Phase 2 — WhatsApp is enough for MVP |
| Instagram account setup | Dentist connects own account vs managed by team | Dentist connects own (simpler compliance) |

---

## Technical Architecture (High Level)

```
[Content Engine]         [Approval Layer]        [Publishing Layer]
GPT-4 + dental          WhatsApp Business API   Instagram Graph API
prompt library    -->   (inbound/outbound)  -->  Scheduled queue
Canva API or            OR                       Retry + error log
image templates         Web dashboard            Admin alert on fail
                        (Phase 2)
```

**Stack decisions:**
- Content generation: OpenAI GPT-4 (already likely in use for WhatsApp assistant)
- WhatsApp: same integration as existing assistant (Twilio or WhatsApp Business API)
- Instagram: Meta Graph API (requires Facebook Business account from each dentist)
- Scheduler: simple cron or Bull queue (Node) / Celery (Python)
- Web dashboard: Next.js or simple React + Supabase for auth + data

---

*File: /products/instagram-dental/roadmap.md*
*Last updated: 2026-02-28*
