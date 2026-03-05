# Booking Assistant Widget — Plan

_Created: 2026-03-05_

## TL;DR

An embeddable chat widget that sits on a dentist's website (bottom-right corner, like Intercom). Instead of a traditional booking form, patients talk to an AI assistant that handles appointment scheduling conversationally — asks what they need, finds an available slot, collects their info, and confirms the booking. The dentist gets a simple dashboard to manage availability. We host everything; the clinic just adds one `<script>` tag.

---

## Part 1: How It Works

### Patient Experience (What the visitor sees)

1. **Bubble** — Small floating button on bottom-right of the clinic website. Shows "Book an appointment" or clinic-branded CTA.
2. **Opens chat** — Clean chat window. First message: *"Hi! I'm [Clinic Name]'s booking assistant. What brings you in today?"*
3. **Conversational flow** — The AI:
   - Asks what service they need (cleaning, whitening, emergency, consultation, etc.)
   - Asks if they have a preferred date/time range
   - Shows 2-3 available slots that match
   - Collects: name, phone, email (optional), insurance (optional)
   - Confirms the appointment with a summary
4. **Confirmation** — Patient gets a summary in-chat + optional SMS/email confirmation
5. **Done** — Total interaction: 60-90 seconds, 5-8 messages

### Dentist Experience (What the clinic sees)

1. **Dashboard** — Simple web panel showing:
   - Today's bookings / upcoming appointments
   - New bookings from the widget (highlighted)
   - Patient details (name, phone, service, time)
2. **Availability setup** — Clinic sets:
   - Working hours per day (e.g., Mon-Fri 9-5, Sat 9-1)
   - Slot duration per service type (cleaning = 30min, root canal = 60min, consultation = 15min)
   - Blocked dates (holidays, vacations)
   - Max appointments per day (optional cap)
3. **Notifications** — New booking → instant notification (email + optional SMS/WhatsApp to clinic)
4. **No calendar sync needed initially** — The widget IS the calendar for clinics that don't have one. For clinics with existing systems, phase 2 adds integrations.

### What Makes This Different From a Booking Form

| Traditional form | AI booking assistant |
|-----------------|---------------------|
| Patient picks from dropdown of services they don't understand | AI asks "what's bothering you?" and maps to service |
| Patient sees 30-slot calendar grid and freezes | AI suggests 2-3 best slots based on preference |
| Form abandonment: 40-60% | Conversational completion: 80%+ (estimated) |
| No personality, no trust-building | Branded, warm, answers questions mid-flow |
| Can't handle "I'm not sure what I need" | AI triages and recommends |
| Static — same for everyone | Adapts language, handles edge cases |

### Key Differentiator: "What do you need?" not "Pick a service"

Most patients don't know dental terminology. They say things like:
- "My tooth hurts" → Emergency/consultation
- "I want whiter teeth" → Whitening
- "Just a regular checkup" → Cleaning + exam
- "My kid needs braces" → Orthodontic consultation

The AI maps natural language to the clinic's service list. This alone solves a huge UX gap.

---

## Part 2: How It Can Be Done

### Architecture

```
┌─────────────────────────────────────────────────┐
│  Clinic Website                                  │
│  ┌───────────────────────────────────────────┐   │
│  │  <script src="booking.js?clinic=abc123">  │   │
│  │  → Loads chat widget (iframe or shadow DOM)│   │
│  └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
          │ WebSocket / REST API
          ▼
┌─────────────────────────────────────────────────┐
│  Backend API (our server)                        │
│  ├── /api/chat       → AI conversation engine    │
│  ├── /api/slots      → Availability lookup       │
│  ├── /api/book       → Create appointment        │
│  ├── /api/notify     → SMS/email confirmation    │
│  └── /api/dashboard  → Clinic admin panel        │
│                                                  │
│  Database: clinic configs, appointments, chats   │
│  AI: Claude API (Haiku for speed + cost)         │
└─────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| **Widget** (frontend) | Vanilla JS + Shadow DOM | No framework dependency, works on any site, <15KB |
| **Chat UI** | Custom (not a library) | Full control, brand-able, mobile-optimized |
| **Backend** | Next.js API routes or FastAPI | Fast to build, easy to deploy |
| **Database** | Supabase (Postgres) | Auth, DB, realtime — all in one. Free tier covers MVP |
| **AI** | Claude Haiku via Anthropic API | Fast (~300ms), cheap (~$0.001/conversation), smart enough for booking flow |
| **SMS** | Twilio or MessageBird | Confirmation + clinic notifications |
| **Hosting** | Vercel (frontend + API) | Free tier, auto-scaling, edge functions |
| **Dashboard** | Next.js + Tailwind | Same stack as API, ship faster |

### Data Model (Core Tables)

```
clinics
  id, name, slug, website, phone, timezone, config_json, created_at

services
  id, clinic_id, name, duration_min, description, keywords[]

availability
  id, clinic_id, day_of_week, start_time, end_time, is_active

blocked_dates
  id, clinic_id, date, reason

appointments
  id, clinic_id, service_id, patient_name, patient_phone, patient_email,
  start_time, end_time, status (confirmed/cancelled), source (widget/manual),
  conversation_id, created_at

conversations
  id, clinic_id, messages_json, outcome (booked/abandoned/question_only),
  created_at
```

### AI Conversation Design

The AI gets a system prompt per clinic:

```
You are a friendly booking assistant for [Clinic Name], a dental clinic in [City].

Available services:
- Cleaning (30 min)
- Whitening consultation (15 min)
- Emergency visit (45 min)
...

Today is [date]. Available slots for the next 7 days:
[dynamically injected from availability API]

Your job:
1. Understand what the patient needs (map to a service)
2. Suggest 2-3 available time slots
3. Collect: name, phone number
4. Confirm the booking

Rules:
- Be warm and brief (1-2 sentences per message)
- If unsure about service, suggest a general consultation
- Never diagnose or give medical advice
- If patient asks a question unrelated to booking, answer briefly then redirect
- Speak in the same language as the patient
```

Each message round-trip:
1. Patient sends message
2. Backend appends to conversation history
3. Calls Claude Haiku with system prompt + history + current availability
4. AI responds with next step
5. If AI's response contains a booking action (structured output), backend creates the appointment

### Build Phases

#### Phase 1: MVP (2-3 weeks)
- Widget: chat bubble + chat window (vanilla JS, embeddable)
- Backend: conversation API with Claude Haiku
- Clinic config: hardcoded for 1 test clinic (services, hours)
- Availability: simple day/time rules (no real-time calendar)
- Booking: saves to DB + sends email notification to clinic
- No dashboard yet — clinic gets email per booking

#### Phase 2: Dashboard + Multi-Clinic (2 weeks)
- Clinic dashboard: see bookings, manage availability, set services
- Onboarding flow: clinic signs up, configures services/hours
- Unique embed code per clinic (`<script src="...?id=CLINIC_ID">`)
- SMS confirmation to patient (Twilio)

#### Phase 3: Polish + Scale (2 weeks)
- Widget customization (colors, logo, welcome message)
- Conversation analytics (completion rate, drop-off points)
- Calendar integrations (Google Calendar sync)
- Multi-language (auto-detect patient language)
- Appointment reminders (24hr before, via SMS)

### Cost Estimate Per Clinic

| Item | Monthly Cost |
|------|-------------|
| Claude Haiku (~200 conversations/mo, ~8 messages each) | ~$0.50 |
| Supabase (free tier up to 50K rows) | $0 |
| Vercel hosting (free tier) | $0 |
| Twilio SMS (~200 confirmations) | ~$15 |
| **Total per clinic** | **~$16/mo** |

At $99-149/mo pricing → **83-89% margin**.

### Pricing Model

| Tier | Price | Includes |
|------|-------|---------|
| Starter | $99/mo | Widget + 200 conversations/mo + email notifications |
| Pro | $149/mo | Above + SMS confirmations + dashboard + analytics |
| Premium | $249/mo | Above + Google Calendar sync + custom branding + priority support |

Setup fee: $0 (frictionless onboarding — they just paste a script tag)

---

## Open Questions

1. **Hebrew + English?** — If targeting Israeli dentists first, the AI needs to handle Hebrew natively. Claude handles Hebrew well. Widget UI needs RTL support.
2. **Existing calendar systems?** — Many clinics use Dentrix, Eaglesoft, or paper. Phase 1 ignores this (widget IS the calendar). Phase 3 adds Google Calendar. Enterprise integrations (Dentrix API) are Phase 4+.
3. **No-show handling?** — Should the widget collect a credit card or deposit? Probably Phase 3.
4. **After-hours?** — Widget should still work 24/7 but say "Next available slot is Monday 9am" — this is actually a huge selling point.
5. **US vs Israel first?** — US dentists from our pipeline are the obvious market. Israel dentists are from the existing Dentists/ project. Could do both.

---

## Why This Wins

- **For the patient**: Faster, friendlier, available 24/7, no phone tag
- **For the clinic**: Captures after-hours bookings they're currently losing, zero staff effort, measurable ROI (count bookings from widget)
- **For us**: $16/mo cost, $99-249/mo revenue, embeds on sites we already audit/build, natural upsell from our existing pipeline data
- **Moat**: Once embedded on a clinic's site and handling bookings, switching cost is high
