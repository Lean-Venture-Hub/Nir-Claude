# Dental Clinic: Susceptibility Scoring + Outreach Playbook

## TL;DR

Score each clinic 0-100 using 8 auto-collectable signals. Target 55-85 scorers — too low means they don't care, too high means they're already covered. Lead with a pre-built demo website as the hook. WhatsApp is primary channel. The pitch is not "buy our service" — it's "we already built this for you, want to see it?"

---

## PART 1: Susceptibility Scoring Model

### Signal Weights (total = 100 pts)

| Signal | Data Source | Max Pts | High Score Condition |
|---|---|---|---|
| Website quality | Manual/auto audit | 25 | No site, broken, or mobile-unfriendly |
| Google review count | GBP scrape | 20 | 5-80 reviews (has some, needs more) |
| No online booking | Site check / GBP | 15 | No booking link anywhere |
| GBP photo count | GBP scrape | 10 | Under 15 photos |
| Review response rate | GBP scrape | 10 | Responds to under 20% of reviews |
| Competitive density | Google Maps radius | 10 | 3+ clinics within 1km |
| Business age | GBP / web WHOIS | 5 | 3-10 years old |
| Practice size signal | GBP / site | 5 | 1-3 dentists (not solo, not chain) |

### Scoring Logic Per Signal

**Website (25 pts)**
- No website at all: 25
- Exists but not mobile-friendly or broken: 20
- Mobile-friendly but no CTA / old design (pre-2020 look): 12
- Modern, fast, has booking: 0

**Review count (20 pts)**
- 0 reviews: 5 (low interest, not zero — penalize but don't skip)
- 1-10 reviews: 15
- 11-80 reviews: 20 (sweet spot — active but underdeveloped)
- 81-300 reviews: 10
- 300+ reviews: 3

**No online booking (15 pts)**
- No booking system detected: 15
- Has phone number only: 10
- Has Doctoralia/ZocDoc/similar: 0 (also flag as LOW susceptibility)

**GBP photos (10 pts)**
- 0-5 photos: 10
- 6-15 photos: 7
- 16-40 photos: 3
- 40+ photos: 0

**Review response rate (10 pts)**
- Responds to 0% of reviews: 10
- Responds to under 20%: 8
- Responds to 20-60%: 4
- Responds to 60%+: 0

**Competitive density (10 pts)**
- 5+ clinics within 1km: 10
- 3-4 clinics within 1km: 7
- 1-2 clinics within 1km: 3
- Isolated area: 0

**Business age (5 pts)**
- 3-10 years: 5
- 11-20 years: 2
- Under 2 years: 0
- Unknown: 2

**Practice size (5 pts)**
- Signs of 1-3 chair practice (not branded chain): 5
- Solo operator (one dentist, home clinic feel): 2
- Chain / franchise signals: 0

### Target Band + Filters

| Score | Action |
|---|---|
| 70-100 | Priority A — build demo site, reach out this week |
| 55-69 | Priority B — reach out without pre-built site |
| 35-54 | Hold — monitor, re-score in 90 days |
| Under 35 | Skip |

**Hard disqualifiers (skip regardless of score):**
- Part of a named chain (e.g., "Smile Bar", "Maccabi dental network")
- Already on Doctoralia with active profile
- Rating under 3.0 with under 10 reviews (likely dying)
- Website launched after 2023 with booking system

---

## PART 2: Outreach Playbook

### Core Hook

"We already built you a new website. Want to see it?"

Pre-build a 1-page demo site per Priority A clinic using: their clinic name, logo (scraped from GBP), photos (from GBP), specialty tags, and neighborhood. Costs ~15 min with a template. The psychological effect is enormous — it's no longer a sales call, it's a delivery.

### Channel Strategy

| Channel | Use Case | Why |
|---|---|---|
| WhatsApp | First touch for Priority A | Highest open rate in Israel, personal |
| Walk-in | Backup if no WhatsApp response in 5 days | Creates urgency, face-to-face trust |
| Email | Follow-up with audit PDF | Paper trail, good for formal decision-makers |
| Phone | Never cold call | Intrusive, skipped |

### Pitch Sequence

**Touch 1 — WhatsApp (Day 1)**

Personalized to their specific gap. Keep under 4 lines.

Template:
> "Hi [Name], I'm Nir. I ran a digital audit on dental clinics in [neighborhood] and noticed [Clinic Name] doesn't have an online booking system. I actually already built a demo website for you — takes 20 seconds to look at. Want me to send the link?"

- Do NOT say "I'm selling" or "we offer"
- Do NOT list features
- One CTA only: see the demo

**Touch 2 — Follow-up if no reply (Day 4)**

> "Sending you the link anyway — [demo URL]. Built it based on your GBP. If you hate it, no worries. If you like it, we can talk."

This removes friction. They can look without committing.

**Touch 3 — Audit Report (Day 8)**

Send a 1-page PDF audit showing:
- Their current GBP score vs. competitors in their area
- What they're losing monthly (estimated new patients) vs. top local competitor
- 3 specific fixes with before/after visuals

Close line: "Happy to walk you through this in 15 minutes. No pitch — just show you the numbers."

**Touch 4 — Walk-in (Day 12, Priority A only)**

Show up with printed audit + tablet showing demo site. Ask for the clinic owner/manager, not the receptionist. Ideal time: Tuesday-Thursday, 10am-12pm (before lunch, after rush).

### Personalization Checklist Per Outreach

Each message must include at least 3 of these:
- [ ] Clinic name (not "your clinic")
- [ ] Specific neighborhood reference
- [ ] One specific gap found in audit (e.g., "you have 18 reviews, your neighbor has 140")
- [ ] Demo site URL (Priority A only)
- [ ] One local competitor named (as a benchmark, not an insult)

### Lead Magnet Options (rank order)

1. Pre-built demo site — strongest, use for Priority A
2. 1-page PDF audit with local competitor benchmarks
3. "Free GBP optimization" — low-friction entry, upsell later

### Objection Responses

| Objection | Response |
|---|---|
| "We already have a website" | "I saw it — here's what's costing you bookings specifically" (show audit) |
| "We're with Doctoralia" | Qualify out or pivot to AI assistant only |
| "Not the right time" | "Fair. Can I leave the demo site up for you to share with your partner?" |
| "How much does it cost?" | "Depends on what you keep from the demo. Can I show you first?" |

---

## Data Collection Automation

Signals that can be scraped automatically per clinic:
- GBP review count + rating + response rate: Google Maps scraper
- Photo count: GBP API or scraper
- Website URL + mobile check: Lighthouse API (free)
- Booking system detection: check for Doctoralia/Setmore/Calendly links on site
- Competitor density: Maps search radius query
- Business age: GBP "opened" field or WHOIS

Estimated time to score 100 clinics: ~2-3 hours with semi-automated tooling.
