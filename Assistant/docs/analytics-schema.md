# Dana Analytics Schema

_Created: 2026-03-05_

## TL;DR

A lightweight event tracking schema to measure Dana's performance across 3 dimensions: **Is she useful?** (task completion), **Is she fast?** (latency), **Is she used?** (engagement). 18 core events, stored in the same PostgreSQL database. No external analytics tool needed — query directly or build a simple dashboard later.

---

## Design Principles

1. **Every event has a session** — a session = one continuous conversation thread (messages within 30 min of each other)
2. **Events are cheap** — one INSERT per event, no joins at write time
3. **Properties over events** — fewer event types with rich properties, not 50 granular events
4. **Measure what you'd act on** — if a metric wouldn't change your behavior, don't track it

---

## Core Events

### 1. Engagement Events

| Event | Fires When | Key Properties |
|-------|-----------|----------------|
| `message_received` | User sends any message | `session_id`, `message_type` (text/voice/image), `char_count`, `language` (he/en), `is_first_today` (bool) |
| `message_sent` | Dana replies | `session_id`, `char_count`, `latency_ms` (time from received to sent), `tool_used` (null if pure chat), `is_proactive` (bool — daily brief, reminder, nudge) |
| `session_started` | First message after 30min+ gap | `session_id`, `hour_of_day`, `day_of_week`, `trigger` (user/proactive) |
| `session_ended` | 30 min inactivity after last message | `session_id`, `duration_sec`, `message_count`, `tools_used[]` |

### 2. Tool Use Events

| Event | Fires When | Key Properties |
|-------|-----------|----------------|
| `tool_called` | Dana invokes any tool | `session_id`, `tool_name` (gmail_read/gmail_send/calendar_view/calendar_create/memory_store/memory_retrieve/reminder_set/task_create), `success` (bool), `latency_ms`, `error_type` (null if success) |
| `email_action` | Email read, drafted, or sent | `session_id`, `action` (read/summarize/draft/send), `email_count` (for batch reads), `confirmed` (bool — did user approve send?) |
| `calendar_action` | Calendar viewed or modified | `session_id`, `action` (view/create/update/delete), `event_date`, `confirmed` (bool) |
| `memory_action` | Memory stored or retrieved | `session_id`, `action` (store/retrieve/search), `memory_type` (explicit/implicit), `result_count` (for retrieval) |
| `reminder_action` | Reminder set or delivered | `session_id`, `action` (set/delivered/snoozed/completed), `delay_minutes` (for set), `is_recurring` (bool) |
| `task_action` | Task created, updated, completed | `session_id`, `action` (create/update/complete/delete), `priority` (urgent/important/normal/low) |

### 3. Quality Events

| Event | Fires When | Key Properties |
|-------|-----------|----------------|
| `intent_classified` | Intent classifier runs | `session_id`, `intent` (email/calendar/memory/reminder/task/chat/unclear), `confidence` (0-1), `fallback_used` (bool) |
| `confirmation_requested` | Dana asks "should I do X?" | `session_id`, `action_type` (send_email/create_event/delete), `user_response` (confirmed/rejected/modified), `response_time_sec` |
| `error_occurred` | Any system error | `session_id`, `error_type` (api_timeout/auth_expired/rate_limit/tool_failure/llm_error), `tool_name`, `recovered` (bool), `user_visible` (bool — did the user see an error message?) |
| `clarification_needed` | Dana asks for more info | `session_id`, `original_intent`, `question_asked`, `resolved` (bool) |
| `daily_brief_sent` | Morning brief delivered | `brief_date`, `sections_included[]` (calendar/email/tasks/reminders), `item_count`, `user_replied` (bool), `reply_latency_min` |
| `proactive_message_sent` | Any unprompted message | `message_type` (daily_brief/reminder/meeting_prep/overdue_nudge/conflict_warning), `user_replied` (bool), `dismissed` (bool) |

### 4. Feedback Events (Implicit)

| Event | Fires When | Key Properties |
|-------|-----------|----------------|
| `correction_detected` | User corrects Dana's action or understanding | `session_id`, `original_action`, `correction_type` (wrong_time/wrong_person/wrong_intent/rephrase), `tool_name` |
| `conversation_abandoned` | User stops mid-task (didn't confirm/complete) | `session_id`, `last_intent`, `messages_in_session`, `last_tool_used` |

---

## Event Schema (PostgreSQL)

```sql
CREATE TABLE analytics_events (
  id            BIGSERIAL PRIMARY KEY,
  event_name    TEXT NOT NULL,          -- e.g. 'message_received'
  session_id    UUID NOT NULL,
  timestamp     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  properties    JSONB NOT NULL DEFAULT '{}',

  -- Denormalized for fast queries (avoid JSONB lookups on hot paths)
  tool_name     TEXT,                   -- NULL if not tool-related
  latency_ms    INTEGER,               -- NULL if not applicable
  success       BOOLEAN                -- NULL if not applicable
);

CREATE INDEX idx_events_name ON analytics_events(event_name);
CREATE INDEX idx_events_session ON analytics_events(session_id);
CREATE INDEX idx_events_timestamp ON analytics_events(timestamp);
CREATE INDEX idx_events_tool ON analytics_events(tool_name) WHERE tool_name IS NOT NULL;
```

Single table, JSONB properties for flexibility, denormalized columns for the 3 fields you'll query most.

---

## Key Metrics (What to Dashboard)

### Daily Health (check every morning)

| Metric | Query Logic | Target |
|--------|------------|--------|
| **Messages/day** | COUNT `message_received` today | Baseline first, then track trend |
| **Avg response latency** | AVG `latency_ms` from `message_sent` | < 3 seconds |
| **Error rate** | `error_occurred` / `message_received` | < 2% |
| **Tool success rate** | `tool_called` WHERE success=true / total | > 95% |

### Weekly Engagement (review Sundays)

| Metric | Query Logic | Target |
|--------|------------|--------|
| **Active days/week** | DISTINCT days with `message_received` | 7/7 (daily use) |
| **Sessions/day** | COUNT `session_started` / active days | Growing |
| **Most-used tools** | `tool_called` GROUP BY tool_name, ORDER BY count | Understand usage patterns |
| **Proactive engagement rate** | `proactive_message_sent` WHERE user_replied / total | > 50% |
| **Brief read rate** | `daily_brief_sent` WHERE user_replied / total | > 70% |

### Monthly Quality (review monthly)

| Metric | Query Logic | Target |
|--------|------------|--------|
| **Correction rate** | `correction_detected` / `tool_called` | < 5% |
| **Abandonment rate** | `conversation_abandoned` / `session_started` | < 10% |
| **Confirmation accept rate** | `confirmation_requested` WHERE confirmed / total | > 90% |
| **Clarification rate** | `clarification_needed` / `intent_classified` | < 15% (she should understand first try) |
| **Fallback rate** | `intent_classified` WHERE fallback_used / total | < 10% |

---

## Session Definition

```
Session starts: first message after 30+ min gap from last message
Session ends:   30 min after last message (retroactive — set on next session start)
Session ID:     UUID generated on session_started
```

All events within a session share the same `session_id`. This lets you reconstruct full conversation flows for debugging.

---

## Implementation Notes

1. **Track in the message pipeline** — add event emitting to the existing message processing flow (step 8 in architecture.md data flow). No separate analytics service needed.
2. **Async writes** — fire-and-forget INSERTs, don't block the response pipeline. Use a simple queue (array buffer, flush every 5 sec or 10 events).
3. **Latency measurement** — capture `Date.now()` at webhook receipt, compute delta at response send. Store as integer ms.
4. **Session management** — store `last_message_at` in a simple key-value (Redis or even in-memory). On each message, check if gap > 30 min → new session.
5. **No PII in properties** — don't store message content in analytics events. Session + timestamp is enough to cross-reference with conversation logs if needed.
6. **Retention** — keep raw events for 90 days, then aggregate to daily summaries. Raw events at ~20 events/session × ~10 sessions/day = ~200 rows/day = trivial for PostgreSQL.

---

## What NOT to Track (Yet)

- **Message content** — already in conversation logs, no need to duplicate
- **Sentiment analysis** — overkill for a single user, just watch correction rate
- **A/B tests** — one user, no variants to test
- **Funnel analysis** — not a product with conversion goals
- **Cost per message** — track at the billing level (Claude API dashboard), not per event
