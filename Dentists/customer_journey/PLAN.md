# Patient Journey Service — Plan

_Created: 2026-03-05_

## TL;DR

A no-integration patient engagement system for dental clinics. The front desk or operations manager enters patient name + phone into a simple web panel after each visit. Our system handles everything from there — review collection, follow-up care, rebooking, referrals — all via WhatsApp/SMS, conversationally with AI. Zero CRM connection needed. The clinic's input is literally: name, phone, service done, next recommended visit. We do the rest.

---

## The Core Problem

Clinics lose patients silently. After treatment, 70%+ of patients hear nothing until they call back (if they ever do). Clinics know they should follow up, ask for reviews, remind about next visits — but nobody on staff has time. CRM integrations are expensive, complex, and most small clinics don't even have a CRM worth connecting to.

**Our solution: The human input IS the integration.** One person spends 30 seconds per patient entering 4 fields. The system handles the next 6 months of that patient relationship.

---

## How It Works (All Options)

### Input Method (Same for All)

The clinic gets a **simple web panel** (mobile-friendly — works from reception desk phone/tablet):

```
┌─────────────────────────────────┐
│  + New Patient Visit            │
│                                 │
│  Name:     [Sarah Cohen      ]  │
│  Phone:    [054-555-1234     ]  │
│  Service:  [Cleaning ▼       ]  │
│  Next rec: [6 months ▼       ]  │
│  Notes:    [optional         ]  │
│                                 │
│  [Submit ✓]                     │
└─────────────────────────────────┘
```

Takes 15-20 seconds. That's the clinic's only job. Everything below is automated.

---

## 5 Service Modules

Each module is independent. Clinics can buy one or stack them. All triggered by the same single input.

---

### Module 1: Review Booster

**Trigger:** 2 hours after visit submission

**Flow (WhatsApp/SMS):**

```
[2 hours after visit]
"Hi Sarah, this is [Clinic Name] 😊
How are you feeling after your cleaning today?
Is everything okay?"

→ Patient replies (any response)

"Great to hear! We'd really appreciate it if you could
share your experience with a quick Google review.
It helps other patients find us.

Here's a ready-made text you can use or edit:

"I had an excellent experience at [Clinic Name].
The staff was professional and friendly, and
the cleaning was thorough and comfortable.
Highly recommend!"

👉 [Leave a review] → (direct Google review link)"
```

**Why it works:**
- Asks about wellbeing FIRST (not "leave us a review") — feels caring, not transactional
- Provides pre-written review text — removes the blank page problem (biggest barrier to reviews)
- Direct link opens Google Maps review form with one tap
- 2-hour delay = still top of mind but not annoyingly instant
- If patient reports a problem → flags the clinic instead of pushing review (reputation protection)

**Negative sentiment handling:**
```
Patient: "Actually my gum is still hurting"

"I'm sorry to hear that, Sarah. I'll let the clinic know
right away so they can help. Someone will call you shortly.
In the meantime — is the pain manageable?"

→ Clinic gets alert: "⚠️ Sarah Cohen reported post-treatment
   discomfort (cleaning, today). Needs follow-up call."
```

This saves the clinic from getting a 1-star review AND gives them a chance to recover the relationship.

---

### Module 2: Post-Treatment Care

**Trigger:** Immediately after visit submission (different content per service type)

**Flow:**

```
[Immediately]
"Hi Sarah, here are your post-cleaning care tips
from [Clinic Name]:

🦷 Post-Cleaning Care:
• Avoid eating/drinking for 30 minutes
• Some gum sensitivity is normal for 24 hours
• Brush gently tonight, resume normal brushing tomorrow
• Avoid very hot/cold drinks today

Questions? Just reply here and we'll help."

[24 hours later]
"Hi Sarah, quick check-in from [Clinic Name] —
how's everything feeling after yesterday's cleaning?"
```

**Service-specific content library:**
| Service | Key instructions | Check-in timing |
|---------|-----------------|-----------------|
| Cleaning | Avoid eating 30min, gentle brushing | 24 hours |
| Filling | Don't chew on that side, sensitivity normal | 24 hours + 1 week |
| Extraction | Ice, soft foods, no straws, no smoking | 4 hours + 24 hours + 3 days |
| Root canal | Pain management, temporary crown care | 24 hours + 1 week |
| Whitening | Avoid staining foods 48hrs, sensitivity tips | 24 hours + 48 hours |
| Implant | Soft diet, ice, bleeding normal first 24hrs | 4 hours + 24 hours + 1 week + 1 month |
| Crown | Don't chew sticky foods, sensitivity normal | 24 hours + 1 week |
| Braces adjustment | Soft foods, wax for irritation, pain normal | 24 hours |

**Why it works:**
- Patients actually read WhatsApp messages (vs printed sheets they throw away)
- Reduces "is this normal?" panic calls to the clinic
- Shows the clinic cares about aftercare (differentiator)
- Creates a natural messaging thread for the review ask + rebooking later

---

### Module 3: Smart Rebooking

**Trigger:** Based on "next recommended visit" field from input

**Flow:**

```
[2 weeks before recommended next visit]
"Hi Sarah, it's been almost 6 months since your
last cleaning at [Clinic Name].

Dr. Cohen recommended scheduling your next
cleaning around now. Would you like to book?

Reply:
1️⃣ Yes, find me a time
2️⃣ Not now, remind me later
3️⃣ I've already booked"

→ If "1": connects to booking widget (Module from booking widget plan)
   or asks for preferred day/time and clinic calls them back

→ If "2": "No problem! When should I remind you?"
   Patient picks 2 weeks / 1 month / 3 months

→ If "3": "Great! See you soon 😊"
```

**Escalation sequence if no reply:**

```
[2 weeks before] → First message (above)
[1 week before]  → "Just a friendly reminder — your
                    6-month cleaning is coming up!"
[On the date]    → "Today's the day Dr. Cohen recommended
                    for your next visit. Shall we book?"
[2 weeks after]  → Final: "We noticed you're overdue for
                    your cleaning. Shall we help you schedule?"
[No reply]       → Mark as "lapsed" in dashboard, stop messaging
```

**Why it works:**
- Most patients WANT to come back, they just forget
- 4-touch sequence over 4 weeks — persistent but not spammy
- Easy reply options (numbered) reduce friction
- "Dr. [Name] recommended" adds authority
- Captures intent even if they can't book right now

---

### Module 4: Referral Engine

**Trigger:** 1 week after visit (only if patient left a positive review or replied positively to check-in)

**Flow:**

```
[1 week after, only for happy patients]
"Hi Sarah! Glad your visit went well 😊

Know anyone who's looking for a great dentist?
If you refer a friend to [Clinic Name], you'll both
get [10% off / free whitening consultation / $25 credit].

Just share this link with them:
🔗 [unique referral link]

Or give them your code: SARAH-2547"
```

**Tracking:**
- Unique referral link per patient → tracks who referred whom
- When a new patient books via referral link, original patient gets notified
- Clinic dashboard shows: referrals sent, referrals converted, revenue attributed

**Why it works:**
- Only sent to HAPPY patients (filtered by review/check-in response)
- Timed after they've had a week to tell friends naturally
- Simple sharing mechanism (link or code)
- Incentive for both sides (dual-sided referral)

---

### Module 5: Treatment Plan Follow-Up

**Trigger:** When clinic marks a visit as having a recommended treatment plan

The input form gets one extra field:

```
┌─────────────────────────────────────┐
│  Pending treatment: [Crown on #14 ▼]│
│  Estimated cost:    [$1,200        ]│
│  Urgency:           [Within 3mo ▼  ]│
└─────────────────────────────────────┘
```

**Flow:**

```
[3 days after visit]
"Hi Sarah, following up from your visit at [Clinic Name].

Dr. Cohen mentioned you'd benefit from a crown on
your back molar. I know it's a lot to think about —
happy to answer any questions you might have about
the procedure, timeline, or cost.

Would you like to:
1️⃣ Learn more about the procedure
2️⃣ Schedule the treatment
3️⃣ Not right now"

→ If "1": AI explains the procedure in plain language,
   answers follow-up questions, then offers to book

→ If "2": Routes to booking flow

→ If "3": "Totally understand. I'll check in again in
   a few weeks — the recommendation doesn't expire 😊"
```

**Nurture sequence for "not now":**
```
[3 weeks later]  → Educational: "Quick fact: a cracked tooth
                    without a crown can lead to..."
[6 weeks later]  → Social proof: "85% of patients who get
                    crowns say they wish they'd done it sooner"
[3 months later] → Urgency: "Hi Sarah, it's been 3 months
                    since Dr. Cohen recommended your crown.
                    Want to revisit this?"
[After 3 touches] → Stop. Mark as "declined" in dashboard.
```

**Why it works:**
- Biggest revenue leak in dentistry: patients who need treatment but don't schedule it
- AI answers questions patients are too embarrassed to ask ("will it hurt?", "can I do payments?")
- Gentle nurture over 3 months — not pushy, educational
- Clinic sees which treatment plans are converting vs dropping off

---

## How All 5 Modules Work Together

```
Patient visits clinic
        │
        ▼
Front desk enters: name, phone, service, next visit, [treatment plan]
        │
        ├── Immediately → Module 2: Post-treatment care tips
        │
        ├── 2 hours    → Module 1: Wellbeing check → Review ask
        │
        ├── 1 week     → Module 4: Referral offer (if positive)
        │
        ├── 3 days     → Module 5: Treatment plan follow-up (if applicable)
        │
        └── X months   → Module 3: Rebooking reminder sequence
```

One input. Five automated workflows. Six months of patient engagement.

---

## Clinic Dashboard

```
┌──────────────────────────────────────────────────────┐
│  [Clinic Name] — Patient Journey Dashboard            │
│                                                       │
│  Today's Stats                                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│
│  │ 12       │ │ 3        │ │ 2        │ │ 1        ││
│  │ Patients │ │ Reviews  │ │ Rebooked │ │ Referral ││
│  │ entered  │ │ received │ │ this wk  │ │ signup   ││
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘│
│                                                       │
│  Recent Activity                                      │
│  ✅ Sarah Cohen left a 5-star review (2hr ago)        │
│  📅 David Levi rebooked cleaning for Mar 15           │
│  ⚠️ Rachel Mor reported sensitivity — needs callback  │
│  💬 Tom Ben asked about crown procedure cost           │
│  👥 Sarah Cohen shared referral link                   │
│                                                       │
│  Pending Treatment Plans (conversion tracker)         │
│  ┌─────────────┬──────────┬────────┬─────────┐       │
│  │ Patient     │ Treat.   │ Value  │ Status  │       │
│  │ M. Avraham  │ Crown    │ $1,200 │ Nurture │       │
│  │ Y. Shapira  │ Implant  │ $3,500 │ Replied │       │
│  │ L. Katz     │ Braces   │ $5,000 │ Booked! │       │
│  └─────────────┴──────────┴────────┴─────────┘       │
│                                                       │
│  Monthly Report                                       │
│  Reviews: 47 (+12 vs last month)                      │
│  Rebookings: 34 (78% of due patients)                 │
│  Treatment plan conversion: 42%                       │
│  Referrals: 8 new patients                            │
│  Revenue influenced: ~$18,400                         │
└──────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| **Clinic panel** | Next.js + Tailwind | Mobile-first, fast to build |
| **Backend** | Next.js API routes | Same codebase |
| **Database** | Supabase (Postgres) | Auth, DB, realtime, free tier |
| **AI** | Claude Haiku | Conversational replies, $0.001/conversation |
| **Messaging** | WhatsApp Business API (primary) + SMS fallback | 98% open rate on WhatsApp vs 20% email |
| **Scheduling** | Built-in job queue (pg_cron or BullMQ) | Timed messages at 2hr, 24hr, 2 weeks, etc. |
| **Hosting** | Vercel | Free tier covers MVP |

### WhatsApp vs SMS

| | WhatsApp | SMS |
|-|----------|-----|
| Open rate | 98% | 95% |
| Reply rate | 40-50% | 10-15% |
| Cost | ~$0.05/conversation (24hr window) | ~$0.01-0.05/message |
| Rich content | Links, buttons, images | Text only |
| Israel | Everyone uses it | Works as fallback |
| US | Growing but not universal | Primary channel |

**Strategy:** WhatsApp primary for Israel, SMS primary for US, offer both.

---

## Pricing

| Tier | Price | Modules | Patients/mo |
|------|-------|---------|-------------|
| **Starter** | $79/mo | Review Booster + Post-Care only | Up to 200 |
| **Growth** | $149/mo | All 5 modules | Up to 500 |
| **Premium** | $249/mo | All 5 + white-label + priority | Unlimited |

**Cost per clinic at 200 patients/mo:**
- WhatsApp: ~$30 (200 patients × 3 avg conversations × $0.05)
- Claude Haiku: ~$1
- Infrastructure: ~$2
- **Total: ~$33/mo → 58-87% margin depending on tier**

---

## Build Phases

### Phase 1: Review Booster MVP (1-2 weeks)
- Clinic panel: enter patient name + phone + service
- 2-hour delayed WhatsApp: wellbeing check → review ask with pre-written text + Google link
- Negative sentiment detection → alert to clinic
- Basic dashboard: patients entered today, reviews received

### Phase 2: Post-Care + Rebooking (2 weeks)
- Post-treatment care messages (service-specific content library)
- Rebooking reminder sequence (4-touch over 4 weeks)
- Dashboard: rebooking rate, care message open rates

### Phase 3: Referrals + Treatment Plans (2 weeks)
- Referral link generation + tracking
- Treatment plan follow-up with AI Q&A
- Revenue attribution in dashboard
- Monthly report generation

### Phase 4: Polish + Scale (ongoing)
- Multi-language (Hebrew + English + Spanish)
- Booking widget integration (from separate plan)
- Clinic onboarding flow (self-serve signup)
- Analytics: conversion funnels, A/B test message variants

---

## Why No CRM Integration Is a Feature, Not a Bug

1. **Faster sales cycle** — "Paste a script" or "open this link" vs 2-week CRM integration project
2. **Works for any clinic** — Paper appointment books to Dentrix to Eaglesoft. Doesn't matter.
3. **Lower churn** — No integration = nothing to break when they update their CRM
4. **Human touch** — The front desk person entering data is a feature: they can add context ("nervous patient", "asked about whitening")
5. **Data moat** — WE own the patient interaction data, not their CRM vendor

The "limitation" of manual entry is actually 15-20 seconds of work that replaces hours of follow-up calls, review chasing, and rebooking reminders that nobody on staff does anyway.

---

## Open Questions

1. **WhatsApp Business API approval** — Requires business verification + message template approval. Takes 1-2 weeks. Need to start this early.
2. **Israel vs US first?** — WhatsApp dominant in Israel (instant adoption). SMS-first in US (bigger market). Could launch Israel MVP, then US.
3. **HIPAA (US) / Privacy (Israel)** — Patient phone + name + service type. Need consent checkbox at clinic level. No medical records stored. Consult on compliance.
4. **Review platform** — Google primary. Should we also support Yelp (US), Facebook, Medreviews (Israel)?
5. **Opt-out handling** — Patient must be able to reply "STOP" at any point. Required by WhatsApp + SMS regulations.
