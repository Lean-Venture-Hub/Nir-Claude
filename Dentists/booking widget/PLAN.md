# Booking Assistant Widget — Plan v2

_Created: 2026-03-05 | Updated: 2026-03-05_

## TL;DR

An embeddable AI chat widget ($99-149/mo) that sits on a dentist's website and books appointments conversationally. Not an AI phone receptionist (Arini, HeyGent = $300-500/mo, phone-based) — we eliminate the need for the phone call entirely. The $50-150/mo dental booking widget space is empty. 69% of patients prefer online booking, but <20% of practices offer it. We're the entry point for the 80%+ of practices that won't pay $300+/mo for phone AI. SMS only at launch (no WhatsApp — Meta won't sign a BAA). HIPAA-compliant from day one.

---

## Competitive Position

| Dimension | AI Phone Receptionists (Arini, HeyGent) | Our Widget |
|-----------|----------------------------------------|------------|
| **Channel** | Phone calls | Website chat |
| **Patient behavior** | Catches patients who call | Catches patients browsing at 9pm |
| **Price** | $200-500/mo | $99-149/mo |
| **Setup** | PMS integration, 2-4 weeks | Paste one `<script>` tag, 15 min |
| **PMS required?** | Yes | No (widget IS the calendar) |
| **Relationship** | Replaces receptionist on calls | Eliminates the need for the call |
| **Competitive?** | No — complementary | A clinic can use both |

**Pricing gap we exploit:** Nothing dental-specific exists at $50-150/mo. Below is generic (Calendly, no HIPAA). Above is full suites ($250-500/mo) or AI phone ($300-800/mo).

**Closest competitors:**
- **NexHealth** ($350/mo) — closest feature set but 2-3x our price, full suite
- **LocalMed** — scheduling widget but opaque pricing, limited features
- **Flossy/HeyGent** — have web chat but bundled into $300+/mo phone AI package
- **My AI Front Desk** ($45/mo) — budget phone AI, no web widget

---

## Part 1: How It Works

### Patient Experience

1. **Bubble** — Floating button, bottom-right. "Book an appointment" or clinic-branded CTA.
2. **Opens chat** — First message includes AI disclosure (required by CA SB 243, FTC, Colorado AI Act):
   > *"Hi! I'm an AI booking assistant for [Clinic Name]. I can help you schedule an appointment. What brings you in today?"*
3. **Conversational flow** — The AI:
   - Maps natural language to services ("my tooth hurts" → emergency consultation)
   - Asks preferred date/time range
   - Shows 2-3 available slots
   - Collects: name, phone, email (optional)
   - Shows consent checkbox: *"I agree to receive appointment reminders and follow-up messages from [Practice Name]. Msg & data rates may apply. Reply STOP to opt out."*
   - Confirms the appointment with summary
4. **Confirmation** — In-chat summary + SMS confirmation (Twilio, HIPAA-compliant)
5. **Done** — 60-90 seconds, 5-8 messages

### Key Differentiator: "What do you need?" not "Pick a service"

Patients don't know dental terminology:
- "My tooth hurts" → Emergency/consultation
- "I want whiter teeth" → Whitening
- "Just a regular checkup" → Cleaning + exam
- "My kid needs braces" → Orthodontic consultation

No competitor does this at our price point. Traditional booking forms have 40-60% abandonment. Conversational: 80%+ estimated completion.

### Dentist Experience

1. **Dashboard** — Simple mobile-friendly web panel:
   - Today's bookings / upcoming appointments
   - New widget bookings (highlighted)
   - Patient details (name, phone, service, time)
   - Activity log (audit trail — HIPAA requirement)
2. **Availability setup:**
   - Working hours per day
   - Slot duration per service type (cleaning = 30min, root canal = 60min)
   - Blocked dates (holidays, vacations)
   - Max appointments per day (optional cap)
3. **Notifications** — New booking → email + SMS to clinic
4. **No PMS integration needed** — Widget IS the calendar in Phase 1. Phase 2 adds Google Calendar. Phase 3 adds native PMS APIs (Open Dental, Dentrix).

---

## Part 2: Architecture

```
┌─────────────────────────────────────────────────┐
│  Clinic Website                                  │
│  ┌───────────────────────────────────────────┐   │
│  │  <script src="booking.js?clinic=abc123">  │   │
│  │  → Loads chat widget (iframe/shadow DOM)  │   │
│  └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
          │ HTTPS (TLS 1.2+)
          ▼
┌─────────────────────────────────────────────────┐
│  Backend API (our server)                        │
│  ├── /api/chat       → AI conversation engine    │
│  ├── /api/slots      → Availability lookup       │
│  ├── /api/book       → Create appointment        │
│  ├── /api/consent    → Record SMS consent         │
│  ├── /api/notify     → SMS confirmation (Twilio)  │
│  ├── /api/audit      → HIPAA audit log            │
│  └── /api/dashboard  → Clinic admin panel         │
│                                                  │
│  Database: clinic configs, appointments, chats   │
│  AI: Claude Haiku via Anthropic API (w/ BAA)     │
│  All PHI encrypted at rest (AES-256)             │
└─────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Choice | Why | BAA? |
|-------|--------|-----|------|
| **Widget** | Vanilla JS + Shadow DOM | No framework deps, <15KB, works on any site | N/A |
| **Backend** | Next.js API routes | Fast to build, deploy on Vercel | — |
| **Database** | Supabase (Postgres) | Auth, DB, realtime, HIPAA-compliant | **Yes** |
| **AI** | Claude Haiku (Anthropic API) | Fast (~300ms), cheap, smart enough | **Yes** |
| **SMS** | Twilio Programmable SMS | HIPAA-eligible, BAA available | **Yes** |
| **Hosting** | Vercel | Auto-scaling, Pro tier BAA available | **Yes** |
| **Dashboard** | Next.js + Tailwind | Same stack, ship faster | — |

### Data Model

```sql
-- Core tables
clinics (
  id, name, slug, website, phone, timezone,
  config_json, baa_signed_at, created_at
)

services (
  id, clinic_id, name, duration_min, description, keywords[]
)

availability (
  id, clinic_id, day_of_week, start_time, end_time, is_active
)

blocked_dates (
  id, clinic_id, date, reason
)

appointments (
  id, clinic_id, service_id,
  patient_name, patient_phone, patient_email,  -- PHI: encrypted at rest
  start_time, end_time,
  status (confirmed/cancelled/no_show),
  source (widget/manual),
  conversation_id, consent_id,
  created_at
)

conversations (
  id, clinic_id, messages_json,  -- PHI: encrypted at rest
  outcome (booked/abandoned/question_only),
  created_at
)

-- Compliance tables
consent_records (
  id, clinic_id, patient_phone,
  consent_text,           -- exact language shown
  consent_type (sms_transactional/sms_marketing),
  granted_at, revoked_at,
  ip_address, user_agent  -- proof of consent
)

audit_log (
  id, clinic_id, user_id, action,
  resource_type, resource_id,
  ip_address, timestamp   -- HIPAA audit trail
)
```

### AI Conversation Design

System prompt per clinic (note: data minimization — only first name sent to Claude):

```
You are an AI booking assistant for [Clinic Name], a dental clinic in [City].

IMPORTANT: You must identify yourself as an AI assistant in your first message.
Never diagnose or give medical advice. Never claim to be human.

Available services:
- Cleaning (30 min)
- Whitening consultation (15 min)
- Emergency visit (45 min)
[dynamically injected per clinic]

Today is [date]. Available slots for next 7 days:
[dynamically injected from availability API]

Your job:
1. Understand what the patient needs (map to a service)
2. Suggest 2-3 available time slots
3. Collect: first name, phone number
4. Confirm the booking
5. NEVER collect: SSN, insurance details, medical history, date of birth

Rules:
- Be warm and brief (1-2 sentences per message)
- If unsure about service, suggest a general consultation
- Speak in the patient's language
- If patient asks clinical questions, redirect to calling the clinic
```

---

## Pricing

| Tier | Price | Includes |
|------|-------|---------|
| **Starter** | $99/mo | Widget + 200 conversations/mo + email notifications |
| **Pro** | $149/mo | Above + SMS confirmations + dashboard + analytics |
| **Premium** | $249/mo | Above + Google Calendar sync + custom branding + priority support |

Setup fee: $0 (frictionless — paste a script tag).

### Cost Per Clinic (at 200 conversations/mo)

| Item | Monthly Cost |
|------|-------------|
| Claude Haiku (~200 convos × 8 msgs) | ~$0.50 |
| Supabase (Pro plan for HIPAA) | ~$25 |
| Vercel (Pro for BAA) | ~$20 |
| Twilio SMS (~200 confirmations) | ~$15 |
| **Total per clinic** | **~$61/mo** |

At $99/mo → 39% margin. At $149/mo → 59% margin. At $249/mo → 76% margin.

**Note:** Margins improve with scale — Supabase/Vercel costs are shared across clinics, not per-clinic. At 20+ clinics, effective cost drops to ~$20/clinic.

---

## Build Phases

### Phase 1: MVP (3-4 weeks) — includes compliance foundation

**Pre-code (Week 1):**
- [ ] Sign BAAs with Anthropic, Twilio, Supabase, Vercel
- [ ] Draft standard BAA template for clinic customers
- [ ] Write HIPAA Security Policies document
- [ ] Designate HIPAA Security Officer
- [ ] Draft Privacy Policy + Terms of Service

**Build (Weeks 2-4):**
- [ ] Widget: chat bubble + chat window (vanilla JS, embeddable)
- [ ] Backend: conversation API with Claude Haiku
- [ ] AI disclosure in first message
- [ ] Consent capture (checkbox, recorded with timestamp + language)
- [ ] STOP keyword handling
- [ ] Clinic config: hardcoded for 1 test clinic
- [ ] Availability: simple day/time rules
- [ ] Booking: saves to DB + email notification to clinic
- [ ] Audit logging on all PHI access
- [ ] Encryption at rest (Supabase AES-256)
- [ ] Role-based access controls (clinic isolation)
- No dashboard yet — clinic gets email per booking

### Phase 2: Dashboard + Multi-Clinic + SMS (2-3 weeks)

- [ ] Clinic dashboard: bookings, availability, services
- [ ] Onboarding flow: clinic signs up, configures, gets embed code
- [ ] SMS confirmations to patients (Twilio)
- [ ] SMS appointment reminders (24hr before)
- [ ] Consent management in dashboard
- [ ] BAA signing flow (click-through for clinics)

### Phase 3: PMS Integration + Polish (3-4 weeks)

- [ ] Google Calendar two-way sync
- [ ] Open Dental API integration (public API, most accessible)
- [ ] Widget customization (colors, logo, welcome message)
- [ ] Conversation analytics (completion rate, drop-off)
- [ ] Multi-language (auto-detect)
- [ ] No-show tracking

### Phase 4: Scale + Upsell (ongoing)

- [ ] Dentrix integration (harder, requires partnership)
- [ ] Eaglesoft integration
- [ ] Deposit/prepay for no-show reduction
- [ ] Customer journey modules (→ see `customer_journey/PLAN.md`):
  - Post-treatment care tips via SMS
  - Review request automation
  - Smart rebooking reminders
  - Referral engine
- [ ] SOC 2 Type II certification
- [ ] Cyber liability + E&O insurance

---

## Integration Roadmap (PMS)

Based on competitor research — Arini/HeyGent take 2-4 weeks per integration. Our phased approach:

| Phase | Calendar Source | Complexity | Covers |
|-------|---------------|------------|--------|
| **Phase 1** | Widget IS the calendar (own DB) | None | Clinics with no PMS or paper books |
| **Phase 2** | Google Calendar sync | Low | Small practices using Google |
| **Phase 3** | Open Dental API | Medium | Open API, covers ~20% of market |
| **Phase 4** | Dentrix, Eaglesoft | High | Requires partnerships, covers ~50% of market |
| **Alt path** | Zapier bridge (like Dentina) | Low-Medium | Works with anything, less real-time |

---

## Resolved Questions (from v1)

| Question | Answer |
|----------|--------|
| WhatsApp vs SMS? | **SMS only at launch.** Meta doesn't offer a BAA — cannot send PHI over WhatsApp. |
| HIPAA compliance? | **Yes, mandatory.** We're a Business Associate. BAAs needed with all vendors + clinics. See `compliance-research.md`. |
| Existing calendar systems? | **Phase 1: own calendar. Phase 3: Open Dental. Phase 4: Dentrix/Eaglesoft.** Zapier as alternative bridge. |
| US vs Israel first? | **US first.** Pipeline data is US-based. HIPAA framework is clear. Israel has different regs (Privacy Protection Authority). |
| AI disclosure? | **Required.** CA SB 243, FTC Section 5, Colorado AI Act. First message must identify as AI. |
| Review requests legal? | **Yes, with written consent.** Marketing under TCPA — need checkbox consent covering both transactional + marketing SMS. |

## Open Questions (remaining)

1. **No-show deposits** — Collect credit card in widget? Adds Stripe + PCI compliance. Probably Phase 4.
2. **Insurance verification** — Competitors like NexHealth offer this. Worth adding? Probably not MVP.
3. **Voice messages** — Should the widget accept voice input? Could help with accessibility. Phase 3+.
4. **White-label** — Should we offer white-label to dental marketing agencies? Arini does this at ~$100/mo base. Consider after 20+ clinics.

---

## Why This Wins

- **For the patient**: Book at 9pm without calling. AI understands "my tooth hurts." 60 seconds, done.
- **For the clinic**: Captures after-hours bookings they're losing. Zero staff effort. Measurable ROI ($99/mo vs $20-70K/yr in no-shows).
- **For us**: $61/mo cost → $99-249/mo revenue. Embeds on sites we already audit/build. Natural upsell to customer journey modules ($79-249/mo additional).
- **Moat**: Once embedded + handling bookings → high switching cost. Compliance (BAAs, audit logs) = barrier to entry for casual competitors.
- **Complementary, not competitive**: A clinic can use Arini for phone ($300/mo) AND our widget for web ($99/mo). We're additive, not a replacement.

---

## Reference Documents

- `competitor-research.md` — Full competitive landscape (dental PMS, med spa, general scheduling)
- `ai-receptionist-landscape.md` — 20+ AI receptionist companies, pricing, channels, gaps
- `compliance-research.md` — HIPAA, TCPA, state laws, vendor BAAs, MVP checklist
- `../customer_journey/PLAN.md` — Patient journey modules (upsell path from booking widget)
