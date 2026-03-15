# Sales Agent — Master Plan

**Created:** 2026-03-15 | **Status:** Planning → Ready to Build

## TL;DR

Autonomous AI sales agent ("a named persona") that receives enriched leads via CSV, runs configurable multi-channel outreach sequences (email-first), handles all conversations via Claude, and closes deals at ~$1,000 setup + $100-500/mo. Escalates to human when uncertain. English only for now.

**Scope boundary:** Agent does NOT own lead pipeline, proposals, or website creation. Fed ready-made data. Owns outreach → conversation → close.

---

## Decisions Locked

| Decision | Answer |
|----------|--------|
| Pricing | ~$1,000 setup + $100-500/mo (finalize later) |
| Agent persona | Named person (name TBD) |
| Language | English only |
| Data input | CSV (format: s4-4b-top100-with-email.csv) |
| First channel | Always email. Escalation order configurable per flow |
| Verticals (launch) | Auto repair, landscaping, dentists |
| CRM integration | Later — CSV for now |

---

## Lead Data Format (from CSV)

Agent receives per lead:
```
name, address, city, state, phone, email,
rating, review_count, categories, hours,
google_maps_url, has_website,
vertical, facebook_url, instagram_url,
review1-5 (name, stars, text)
```

This gives the agent: business context, contact info, social proof (reviews), social links, and vertical classification. Rich enough for highly personalized outreach.

---

## Architecture

```
CSV Import ──→ Lead Store (SQLite/Supabase)
                    │
                    ▼
┌──────────────────────────────────────────────┐
│              SALES AGENT                      │
│      (Python + Claude + LangGraph)            │
│                                               │
│  ┌───────────┐  ┌────────────┐  ┌──────────┐ │
│  │ Outreach  │→ │ Convo      │→ │ Closing  │ │
│  │ Engine    │  │ Agent      │  │ Engine   │ │
│  │           │  │            │  │          │ │
│  │ Instantly │  │ Claude API │  │ Stripe   │ │
│  │ Twilio    │  │ Tool use   │  │ Onboard  │ │
│  │ Retell.ai │  │ Objections │  │ Upsell   │ │
│  └───────────┘  └────────────┘  └──────────┘ │
│                                               │
│  ┌──────────────────────────────────────────┐ │
│  │         FLOW ENGINE (configurable)        │ │
│  │  email→sms→whatsapp→phone (default)       │ │
│  │  email→phone→sms (aggressive)             │ │
│  │  email only (conservative)                │ │
│  └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
         │
         ▼ writes back
   Lead Store (stage, logs, recordings)
```

---

## Component 1: Outreach Engine

### Configurable Flow System

Flows define the outreach sequence. Each vertical or campaign can have its own flow.

```yaml
# Example: default flow
flow: default
steps:
  - day: 0, channel: email, template: intro
  - day: 2, channel: email, template: follow_up
  - day: 4, channel: sms, template: short_intro
  - day: 6, channel: whatsapp, template: casual
  - day: 8, channel: phone, template: warm_call
  - day: 10, channel: email, template: breakup
  - day: 14, channel: sms, template: final
on_reply: pause_sequence, route_to_convo_agent

# Example: email-only flow
flow: conservative
steps:
  - day: 0, channel: email, template: intro
  - day: 3, channel: email, template: follow_up
  - day: 7, channel: email, template: value_add
  - day: 14, channel: email, template: breakup
```

### Personalization Data (from CSV)

The agent uses lead data to personalize every message:
- **Business name** — "Hi, I noticed [Wheel Master] doesn't have a website yet"
- **Reviews** — "Your 4.7 stars from 993 reviews are incredible — imagine if new customers could find you online"
- **Location** — "Shops in Phoenix are going digital fast"
- **Category** — vertical-specific language
- **Hours** — "I see you're open 7 days a week — a website works for you 24/7"

### Tool Stack

| Channel | Tool | Cost | Notes |
|---------|------|------|-------|
| Cold email | Instantly.ai | $37-97/mo | Warm-up, deliverability, sequence built-in |
| Transactional email | AWS SES | $0.10/1K | Payment confirmations, onboarding only |
| SMS | Twilio | $0.008/msg | A2P 10DLC registration required |
| WhatsApp | Twilio or YCloud | $0.005-0.08/msg | Business verification needed |
| Phone | Retell.ai | $0.13-0.31/min | Best voice quality, native Claude support |

### Build vs Buy: Instantly.ai

Instantly handles cold email sequences natively (warm-up, scheduling, tracking). Two options:
1. **Use Instantly's built-in sequences** — faster to launch, less control
2. **Use Instantly as send engine only** — our agent controls timing/content via API

Recommend: Start with option 1 for email, build custom for SMS/WhatsApp/phone. Migrate email to custom later if needed.

---

## Component 2: Conversation Agent

### Claude-Powered Brain

```python
# Pseudo-architecture
class SalesAgent:
    model = "claude-sonnet-4-20250514"  # Volume. Opus for escalated/complex.

    tools = [
        lookup_lead,           # Full lead context
        get_conversation,      # All messages history
        get_vertical_playbook, # Selling points, objections, lingo
        send_message,          # Reply on any channel
        schedule_call,         # Book AI or human call
        update_stage,          # Move pipeline: new→contacted→engaged→qualified→closing→won/lost
        add_note,              # Log insight
        escalate,              # Flag for human
        send_payment_link,     # Stripe
        trigger_onboarding,    # Post-sale
    ]

    system_prompt = """
    You are {AGENT_NAME}, a sales rep at Scalefox.
    You help small businesses get online with a professional website
    and digital presence.

    Current lead: {lead_context}
    Vertical playbook: {vertical_playbook}
    Conversation so far: {history}

    Rules:
    - Always reference their specific business by name
    - Use their reviews as social proof ("your customers love you")
    - Be helpful, not pushy
    - Fixed pricing: $1,000 setup + $X/mo (no negotiation on base)
    - If unsure, escalate — better to lose a beat than lose the deal
    """
```

### Pipeline Stages

```
NEW → CONTACTED → ENGAGED → QUALIFIED → PROPOSAL_SENT → CLOSING → WON / LOST
                                                                    ↓
                                                               ONBOARDING → ACTIVE → UPSELL
```

### Objection Playbook (to create)

| Objection | Response Strategy |
|-----------|------------------|
| "Too expensive" | ROI math: 1 new customer/mo from Google pays for it |
| "I get business from word of mouth" | "Imagine if those referrals could check you out online first" |
| "I'm not tech savvy" | "We handle everything — you just approve" |
| "I already have a Facebook page" | "Great! A website makes your Facebook work harder" |
| "Not interested" | Graceful exit, note reason, try again in 90 days |
| "I need to think about it" | "Totally fair — I'll send you the proposal page to review" |

### Escalation Rules

Escalate immediately:
- Lead asks to speak to human
- Angry / profanity
- Legal questions
- Custom requirements outside standard offering
- >3 exchanges without progress
- Lead claims to be on do-not-contact list

---

## Component 3: Closing Engine

### Payment Flow
```
Agent: "Ready to get started? Here's your payment link: [Stripe]"
  → Lead pays → Webhook triggers:
    1. Update CRM: stage = WON
    2. Send welcome email (SES, transactional)
    3. Notify human: "New customer! Deploy their site"
    4. Schedule onboarding (Day 1, Day 3, Day 7 check-ins)
    5. Queue upsell sequence (Day 30+)
```

### Upsell Sequences (post-sale, same agent persona)
- Day 30: "How's the website working? Here's what we could add..."
- Day 60: Social media posting offer
- Day 90: Review management offer
- Ongoing: Contextual upsells based on their engagement

---

## Build Phases

### Phase 1: Email Outreach MVP (Week 1)
> Goal: CSV → personalized email sequence → track responses

| # | Task | Est. |
|---|------|------|
| 1.1 | Set up project structure (Python, FastAPI, deps) | 1h |
| 1.2 | CSV importer → SQLite lead store | 2h |
| 1.3 | Set up Instantly.ai account + domain warm-up | 1h |
| 1.4 | Build flow engine (YAML config → scheduled sends) | 4h |
| 1.5 | Personalization engine (lead data → message templates) | 3h |
| 1.6 | Write email templates for 3 verticals | 3h |
| 1.7 | Instantly.ai integration (API or built-in sequences) | 3h |
| 1.8 | Reply detection → webhook → log | 2h |
| 1.9 | Test with 10 real leads | 1h |

**Milestone:** 10 auto-repair leads get personalized 4-email sequence. Replies tracked.

### Phase 2: Conversation Agent (Week 2)
> Goal: AI handles email replies autonomously

| # | Task | Est. |
|---|------|------|
| 2.1 | Inbound email routing (Instantly reply → webhook → agent) | 3h |
| 2.2 | Build Claude conversation agent (LangGraph + tool use) | 5h |
| 2.3 | Create objection playbook + vertical knowledge bases | 3h |
| 2.4 | Pipeline stage management | 2h |
| 2.5 | Escalation system (notify human via SMS/email) | 2h |
| 2.6 | Conversation logging to lead store | 1h |
| 2.7 | Test with simulated reply scenarios | 2h |

**Milestone:** Agent handles replies, qualifies leads, escalates when needed.

### Phase 3: Multi-Channel + Closing (Week 3)
> Goal: Add SMS, WhatsApp, phone. Close deals.

| # | Task | Est. |
|---|------|------|
| 3.1 | Twilio setup (SMS + WhatsApp) | 2h |
| 3.2 | SMS/WhatsApp send + receive integration | 3h |
| 3.3 | Retell.ai setup + phone call integration | 3h |
| 3.4 | Phone call scripts per vertical | 2h |
| 3.5 | Stripe payment link generation | 2h |
| 3.6 | Close flow: payment → onboarding trigger | 2h |
| 3.7 | Multi-channel flow engine (email→SMS→WhatsApp→phone) | 3h |
| 3.8 | End-to-end test: full lead lifecycle | 2h |

**Milestone:** Full pipeline. Lead gets email → SMS → phone. Can close and pay.

### Phase 4: Production Hardening (Week 4)
> Goal: Reliable, monitored, scalable

| # | Task | Est. |
|---|------|------|
| 4.1 | Error handling + retry logic | 2h |
| 4.2 | Monitoring + alerting (failed sends, stuck leads) | 2h |
| 4.3 | Simple dashboard (HTML, shows pipeline + conversations) | 4h |
| 4.4 | A/B test framework for templates | 3h |
| 4.5 | Add new verticals (template + playbook per vertical) | 2h each |
| 4.6 | Rate limiting + compliance (opt-out, business hours) | 2h |

---

## Monthly Cost (at 1,000 leads/mo)

| Item | Cost |
|------|------|
| Instantly.ai | $37-97 |
| Claude API (Sonnet, ~30 msgs/lead on avg) | ~$100 |
| Twilio SMS (2/lead × 1000) | ~$16 |
| Twilio WhatsApp (500 leads) | ~$25-40 |
| Retell.ai phone (200 calls × 3min) | ~$80-180 |
| AWS SES (transactional) | ~$1 |
| Supabase (when migrated from SQLite) | Free-$25 |
| **Total** | **$260-440/mo** |

**Break-even:** 1 closed deal/month at $1,000 setup covers 2-3 months of costs.

---

## Open Items

| Item | Status | Notes |
|------|--------|-------|
| Agent persona name | TBD | Need to pick a name |
| Exact pricing tiers | TBD | ~$1K setup + $100-500/mo |
| Upsell pricing | TBD | Per service add-on |
| Instantly.ai: sequences vs API | Decide in Phase 1 | Test both |
| Phone: Retell vs Bland | Decide in Phase 3 | Test both |
| Proposal page integration | When CRM ready | Agent sends proposal URL from CRM |
| CRM API migration | When CRM ready | Replace CSV import with API calls |

---

## Key Files

| File | Purpose |
|------|---------|
| `sales-agent/PLAN.md` | This file |
| `sales-agent/src/` | Agent codebase |
| `sales-agent/flows/` | YAML flow definitions |
| `sales-agent/playbooks/objections.md` | Objection handling |
| `sales-agent/playbooks/verticals/` | Per-vertical knowledge |
| `sales-agent/templates/` | Email/SMS/WhatsApp message templates |
| `research/ai-sales-agent-stack-deep-brief.md` | Tool/API research |
