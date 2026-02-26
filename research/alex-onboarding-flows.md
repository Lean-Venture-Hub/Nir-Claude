# Alex – WhatsApp AI Assistant: 3 Onboarding Flow Designs

**TL;DR:** Three approaches trading off between speed-to-value, trust-building, and depth of setup. Recommendation: Flow 2 (The Instant Demo) wins on time-to-wow, but Flow 3 (The Conversation) wins on memory depth and retention.

---

## Shared Constraints & Principles

**WhatsApp limits:**
- Buttons: max 3 per message
- List menus: up to 10 rows
- No custom typing indicators
- Links open natively in browser (good for OAuth)
- Images, audio, documents all work

**Design principles applied:**
- Superhuman: teach by doing, never explain
- Arc: product IS the onboarding
- Duolingo: micro-commitments, immediate reward loops
- Notion AI: show magic first, ask questions second

**The OAuth problem:** OAuth requires leaving WhatsApp → browser → back. This is the highest-friction moment. Every flow must place it strategically — never first, always after user has already experienced value.

---

## Flow 1: "The Setup Wizard"

**Concept:** Classic linear onboarding. Alex walks the user through structured steps with clear progress. Feels intentional and complete. Inspired by Superhuman's onboarding call — high-touch, thorough, builds confidence.

**Philosophy:** "You're setting up a powerful tool. Let's do it right."

---

### Step-by-Step

**0:00 — First message from Alex**
```
Hi, I'm Alex — your AI personal assistant.

I live here in WhatsApp. Before I can be useful,
I need to know a few things about you.

Takes about 3 minutes. Ready?
```
[Yes, let's go] [How does this work?]

**0:15 — Name**
```
What's your name?
```
User types: "Nir"

**0:30 — Timezone**
```
Got it, Nir. Where are you based?
(City or timezone works)
```
User types: "Tel Aviv"

**0:45 — Role/context**
```
What do you do? A sentence is enough —
this helps me understand what matters to you.
```
User types: "I run a B2B SaaS startup"

**1:00 — Preferences**
```
A few quick ones:

- When does your work day usually start?
- Any hard stops? (kids pickup, gym, etc.)
- Prefer updates in the morning, or when things happen?
```
User responds naturally

**1:45 — Memory confirmation**
Alex sends a summary card:
```
Here's what I know about you so far:

Name: Nir
Location: Tel Aviv (UTC+2)
Work: B2B SaaS founder
Day: ~8am–7pm, morning briefings preferred

Does this look right?
```
[Looks good] [Fix something]

**2:00 — OAuth intro**
```
Last step: connect your Gmail and Calendar.

This lets me:
✓ Read emails and flag what matters
✓ See your schedule and prep you for meetings
✓ Send reminders at the right time

Your data stays private — I only read, never store raw emails.
```
[Connect Gmail & Calendar →]

CTA opens browser OAuth flow. User authorizes both scopes.

**2:30 — OAuth success detection + first value**
Alex detects the connection and immediately runs a real action:
```
Connected! Let me check what's on your plate today...
```
[3–5 second pause, then:]
```
Here's your situation for today, Nir:

📅  3 meetings — your next one is at 2pm with Dan (Product review)
📬  47 unread emails — 3 look important:
    • Stripe: payment issue on account
    • Sarah: follow-up from yesterday's call
    • Y Combinator: application update

Anything you want to tackle first?
```

**Wow moment: ~3:00**

---

### Pros
- User feels fully set up and confident
- Memory is rich from the start
- OAuth is framed well with clear value prop
- No confusion about what Alex can do

### Cons
- 3 minutes before first value — long for WhatsApp
- Feels like a form, not a conversation
- Drop-off risk after each question
- Linear structure feels rigid

**Time to wow: ~3 minutes**
**OAuth placement: After setup, before value — necessary but slightly awkward**

---

## Flow 2: "The Instant Demo"

**Concept:** Skip setup entirely. Alex does something impressive in the first 30 seconds. Value first, information later. Inspired by Arc's first-launch experience — the product demonstrates itself.

**Philosophy:** "Don't tell me what you can do. Show me."

---

### Step-by-Step

**0:00 — First message**
```
Hey, I'm Alex.

Watch this — send me any email or calendar
screenshot and I'll show you what I can do.

Or just say "show me" if you want to see a demo.
```
[Show me a demo] [Connect my Gmail]

**0:10 — User taps "Show me a demo"**
Alex sends a realistic-feeling demo:
```
Okay, here's what a typical morning with me looks like:

---
Good morning. Here's your day:

8:30 — Sync with the team (Zoom link ready)
11:00 — Dan wants to move your call — want me to reschedule?
2pm — Board prep deck still missing 3 slides (Sarah last touched it)

2 emails need you today:
→ Stripe flagged a payment issue — want me to draft a reply?
→ VC partner asked for your deck — send the latest version?

What do you want to start with?
---

That's me, every morning. Want this for real?
```
[Hell yes] [Tell me more]

**0:30 — User says "Hell yes"**
```
Nice. Two things to get started:

First — what's your name?
```
User: "Nir"

**0:40**
```
Nir, connect Gmail and Calendar —
that's all I need to make this real for you.

Your data is private. I read it, I don't store it.
```
[Connect now →]

OAuth link opens. User authorizes.

**1:00 — OAuth complete. Alex immediately pulls real data.**
```
Done. Scanning your day...
```

```
Here's what's actually happening for you today, Nir:

📅  Next: 2pm Product review with Dan
📬  Stripe sent something about a payment 3 hours ago
    → Want me to open it?
📋  You have 3 tasks from last week still open in your email

What first?
```

**Wow moment: 0:30 (demo), then again at 1:00 with real data**

**1:15 — Timezone + preferences (passive)**
```
Quick — where are you? (I'll get your timezone right)
```
This feels natural, not like a form. Just one question, conversationally.

Memory builds organically from the conversation, not from a structured intake.

---

### Pros
- Wow moment at 30 seconds with demo, 60 seconds with real data
- No upfront commitment — show value before asking for anything
- OAuth placed right after first emotional hook
- Feels like talking to a person, not filling a form

### Cons
- Memory seeding is thinner early on
- Demo could feel deceptive if real data is very different
- User skips setup steps — Alex knows less upfront
- Requires good first-pull logic to not disappoint after OAuth

**Time to wow: 30 seconds (demo), 60 seconds (real)**
**OAuth placement: After first emotional hook — optimal**

---

## Flow 3: "The Conversation"

**Concept:** Alex opens with a single powerful question and learns everything through dialogue. No wizard, no demo — just a natural back-and-forth that happens to collect everything Alex needs. Inspired by how a smart new EA would start on day one.

**Philosophy:** "A great assistant asks smart questions and listens."

---

### Step-by-Step

**0:00 — First message**
```
Hey, I'm Alex — your AI assistant on WhatsApp.

One question to get started:

What's the one thing on your mind right now
that you wish was handled?
```
(No buttons — open text only)

**This question is a trap — in the best way.**

User answers reveal:
- What they care about (email backlog → Gmail is critical)
- Their role/context (mentions "investors" → founder)
- Their stress point (what to prioritize first)
- Their communication style (terse vs. verbose)

**0:30 — User responds, e.g.:**
"My inbox is a disaster. I have 300 unread and a board meeting tomorrow."

**Alex responds:**
```
That's fixable.

Board meeting tomorrow — what time? And who's on the call?
```

**0:45 — User answers**
```
2pm, 5 investors
```

**Alex:**
```
Got it. Let me help you prep.

I need to see your inbox and calendar —
takes 30 seconds to connect:
```
[Connect Gmail & Calendar →]

**The key insight here:** OAuth is placed at the moment of *maximum motivation*. The user just articulated their problem. Alex immediately offered to solve it. The OAuth ask isn't "setup" — it's the unlock to the specific solution they asked for.

**1:00 — OAuth complete**
```
Reading your inbox now...

Found 3 emails from your board investors in the last 7 days.
Your calendar shows a 2pm slot tomorrow — no prep materials attached.

Want me to:
→ Pull the key threads from each investor?
→ Draft a quick prep doc for tomorrow?
→ Both?
```
[Pull threads] [Draft prep] [Both]

**Wow moment: 1:00 — Alex is already solving the exact problem the user mentioned 30 seconds ago**

**Post-wow — memory seeding happens naturally:**
As Alex works, it asks only what it needs:
```
What's your name so I can format this right?
```
```
Which timezone — I want to make sure
"2pm tomorrow" means 2pm for you
```

Everything else (role, priorities, preferences) is inferred from the conversation and stored in memory automatically.

---

### Flow 3 Memory Seeding Strategy

Instead of a questionnaire, Alex infers:
- **Name**: asks once, naturally
- **Timezone**: asks when it matters (first time mention)
- **Role**: inferred from context ("board meeting", "investors")
- **Priorities**: inferred from first answer
- **Communication style**: inferred from how they write
- **Schedule**: inferred from calendar once connected
- **Preferences**: Alex asks "was this helpful the way I formatted it?" after first deliverable

By end of day 1, Alex knows more than any wizard would have extracted — because it came from real usage.

---

### Pros
- Most personalized from the first message
- OAuth placed at peak motivation — highest conversion
- No friction, no forms, feels like AI magic
- Memory is contextual, not artificial
- Users feel *heard*, not processed

### Cons
- Requires excellent NLP to parse free-form first answer
- Risk: user types something Alex can't extract signal from
- No guardrails — user could go off-track
- Harder to engineer (parsing intent vs. structured intake)
- Memory seeding is slower — Alex knows less for first few interactions

**Time to wow: 60–90 seconds**
**OAuth placement: At moment of maximum user motivation — best of all 3**

---

## Comparison Table

| Dimension | Flow 1: Wizard | Flow 2: Demo | Flow 3: Conversation |
|---|---|---|---|
| Time to wow | ~3 min | ~30–60 sec | ~60–90 sec |
| Memory depth at T+5min | High | Medium | Medium |
| Memory depth at T+1day | High | High | Very high |
| Friction | Medium | Low | Very low |
| OAuth conversion risk | Medium | Low | Very low |
| Engineering complexity | Low | Medium | High |
| Drop-off risk | High (each step) | Low | Low |
| Feels like | Tool setup | Magic trick | Real conversation |
| Best for | Trust-focused users | Impatient users | Engaged users |

---

## Recommended Approach: Hybrid of Flow 2 + Flow 3

**Open with Flow 2's demo hook** (30 seconds of "look what's possible")
**Then transition into Flow 3's conversation** ("what's the one thing you'd fix right now?")
**OAuth triggered by Flow 3's motivation peak**
**Memory seeding is passive, inferred, never a form**

The formula:
1. Show magic (30 sec)
2. Ask one great question (10 sec)
3. OAuth at motivation peak (30 sec)
4. Deliver real value on their specific problem (60 sec)
5. Memory fills in naturally from here

**Total time to genuine wow: under 90 seconds**

---

## OAuth UX Details (All Flows)

**The message that precedes the link matters most:**
- Bad: "Please connect your Google account to continue"
- Good: "I need to see your inbox to fix this — takes 30 seconds:"

**After OAuth success:**
- Detect completion via webhook
- Respond within 2–3 seconds with first real pull
- Never say "setup complete" — just start doing the work

**If OAuth fails or user doesn't click:**
- Don't nag immediately
- 30 min later: "Still there? Your link is still waiting when you're ready."
- Alex should still be partially useful without OAuth (answer questions, set reminders manually)

---

## WhatsApp-Specific UX Notes

**Button usage strategy:**
- Use buttons to reduce friction on binary choices ("Yes" / "Not now")
- Never use buttons for open-ended questions — kills conversation feel
- List menus for selection (e.g., timezone options if text fails)

**The "typing..." moment:**
- WhatsApp shows typing automatically — use this
- Add 1–2 second delays before sending key messages
- Rapid-fire responses feel like a bot; paced responses feel like a person

**Voice note opportunity:**
- Flow 3 could invite: "You can also just voice note me — easier than typing"
- Signals that Alex is a real assistant, not a chatbot form

**First message timing:**
- The first message arrives when user adds the number
- Should feel immediate and alive — not like an autoresponder
