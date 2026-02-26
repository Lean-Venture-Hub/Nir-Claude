# Assistant Prompts Summary

**Date**: 2026-02-17 | **Status**: First Draft

## TL;DR

9 prompts power the assistant. They follow a pipeline: sanitize input → classify intent → execute tool → generate response → extract memory. The main system prompt sets persona + security + format. Sub-prompts handle specific tasks (email, calendar, memory, etc). All external content (emails, calendar events) is wrapped in `[UNTRUSTED CONTENT]` tags to prevent prompt injection.

---

## Prompt Inventory

| # | Prompt File | Purpose | When Used |
|---|---|---|---|
| 1 | `01_system_prompt.md` | Core persona, security rules, tool definitions, WhatsApp format | Every message (always loaded) |
| 2 | `02_intent_classifier.md` | Classify user message into actionable intent | Every incoming message (first step) |
| 3 | `03_input_sanitizer.md` | Clean/normalize user input, detect injection | Every incoming message (before classifier) |
| 4 | `04_email_reader.md` | Summarize emails, detect priority/action needed | When reading/checking email |
| 5 | `05_email_composer.md` | Draft and format outgoing emails | When user wants to send email |
| 6 | `06_calendar_manager.md` | Parse calendar queries, format event creation | When interacting with calendar |
| 7 | `07_memory_extractor.md` | Extract facts worth remembering from conversations | After every conversation (background) |
| 8 | `08_daily_brief.md` | Generate morning summary from calendar + email + tasks | Scheduled (e.g., 7:30 AM daily) |
| 9 | `09_task_reminder.md` | Manage tasks and reminders, parse natural language time | When creating/checking tasks or reminders |

## Key Design Choices

| Decision | Choice | Why |
|---|---|---|
| **Pipeline vs single prompt** | Pipeline (sanitize → classify → tool → respond) | Separation of concerns, each prompt is focused and testable |
| **Intent classification** | Dedicated classifier with confidence scores | At < 0.7 confidence, ask clarifying question instead of guessing wrong |
| **WhatsApp formatting** | Plain text only, no markdown | Markdown renders as literal asterisks/underscores in WhatsApp |
| **Response length** | 2-3 sentences default, offer detail on request | WhatsApp users expect texting, not essays |
| **Injection defense** | Multi-layer: untrusted tags + keyword detection + output validation | No single defense is enough; emails are the #1 injection vector |
| **Confirmation gates** | Send email, invite others, delete = require confirmation | Balance security vs. friction. Read-only actions run silently |
| **Memory extraction** | Background after each conversation, not inline | Doesn't slow down response time, runs async |
| **Tone** | Friendly but efficient, matches user energy | Not robotic, not overly casual. Adapts to how user writes |
| **Emoji usage** | Mirror user — only use if they use first | Some people hate emojis in productivity tools |
| **Error handling** | Honest + actionable ("Can't access your calendar right now. Want me to try again in a minute?") | Never pretend something worked when it didn't |

## Processing Pipeline

```
User sends WhatsApp message
    ↓
[03 Input Sanitizer] → cleaned text + injection flag
    ↓
[02 Intent Classifier] → intent + params + confidence
    ↓ (if confidence < 0.7 → ask clarifying question)
    ↓
[Tool execution] → call Gmail/Calendar/Memory/Task API
    ↓ (uses prompt 04-09 depending on intent)
    ↓
[01 System Prompt + tool results] → final response
    ↓
[07 Memory Extractor] → background: extract & store facts
    ↓
WhatsApp reply sent
```

## Actions Requiring Confirmation

- Sending any email
- Creating calendar events that invite other people
- Deleting tasks, reminders, or memories
- Any action that costs money or is irreversible

## Actions That Run Silently

- Reading email / calendar
- Setting personal reminders
- Storing memory facts
- Generating summaries / briefs
- Updating task status
