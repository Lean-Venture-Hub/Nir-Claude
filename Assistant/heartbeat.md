# Heartbeat — Alex's Always-On Loop

> Defines the scheduled tasks, health checks, and proactive behaviors that keep Alex alive and useful even when Nir isn't actively chatting.

---

## Scheduled Jobs

### Morning Brief — Daily, 07:30 (configurable)
**Trigger**: Cron job
**What it does**:
1. Fetch today's calendar events from Google Calendar
2. Fetch overnight emails, run through email reader prompt
3. Check tasks due today + overdue tasks
4. Check reminders scheduled for today
5. Generate brief using `08_daily_brief.md` prompt
6. Send via WhatsApp

**Skip conditions**:
- Weekend (Saturday) — unless Nir has calendar events that day
- If Nir already messaged Alex today (he's awake, don't repeat info)

### Email Check — Every 30 minutes
**Trigger**: Polling interval
**What it does**:
1. Fetch new unread emails since last check
2. Run through email reader prompt for priority classification
3. If action-required + high urgency → send WhatsApp alert
4. If normal priority → batch for next daily brief or on-demand check
5. Update email summary cache

**Alert threshold**: Only push-notify for emails classified as `urgency: high` + `type: action-required`

### Reminder Delivery — Per-reminder schedule
**Trigger**: Individual cron per reminder
**What it does**:
1. Fire at scheduled time
2. Send WhatsApp: "תזכורת: {reminder_message}"
3. If recurring: schedule next occurrence
4. If one-time: mark as delivered

**Retry**: If WhatsApp delivery fails, retry 3x at 5-min intervals, then notify Nir on next interaction.

### Memory Maintenance — Weekly, Sunday 03:00
**Trigger**: Weekly cron
**What it does**:
1. Review all Tier 3 memories
2. Archive memories with 0 access in 90+ days
3. Merge duplicate/overlapping memories
4. Summarize verbose memories into concise versions
5. Update embedding vectors for modified memories
6. Log cleanup stats

### Calendar Sync — Every 15 minutes
**Trigger**: Polling interval
**What it does**:
1. Fetch calendar changes since last sync
2. Detect new events, cancellations, time changes
3. Update local calendar cache
4. If a meeting was added/changed for today → consider notifying Nir
5. Detect upcoming conflicts

**Notification rules**:
- New meeting added for today → notify
- Meeting cancelled → notify
- Meeting moved → notify
- Meeting 15 min away → send reminder (if not already reminded)

---

## Health Checks

### Self-health — Every 5 minutes
| Check | Action on Failure |
|---|---|
| WhatsApp connection alive | Attempt reconnect, log error |
| Database connection alive | Attempt reconnect, alert if 3 fails |
| Claude API reachable | Log, switch to fallback response |
| Google OAuth tokens valid | Refresh tokens, alert if refresh fails |
| Disk space > 1GB | Alert Nir via alternative channel |
| Memory usage < 80% | Log warning, restart if > 90% |

### Fallback responses (when Claude API is down)
If the LLM is unreachable, Alex can still:
- Deliver scheduled reminders (pre-generated)
- Send raw calendar data (unformatted)
- Acknowledge messages: "I'm having trouble thinking right now. I'll get back to you shortly."
- Queue incoming messages for processing when API returns

---

## Proactive Behaviors

Things Alex does without being asked, based on patterns and context:

| Behavior | Trigger | Action |
|---|---|---|
| Meeting prep | 15 min before meeting | "You have [meeting] in 15 min with [person]. Here's context from your last interaction." |
| End-of-day recap | 18:00 (if Nir interacted today) | "Quick recap: you completed X, Y is still pending, tomorrow starts with Z." |
| Conflict alert | New event overlaps existing | "Heads up — [new event] overlaps with [existing]. Want me to move one?" |
| Overdue task nudge | Task 1+ day overdue | "Reminder: [task] was due yesterday. Still on your list or should I reschedule?" |
| Follow-up prompt | Nir said "I'll do X tomorrow" | Next day: "You mentioned you'd [X] today. Want me to add it to your list?" |
| Stale email alert | High-priority email unanswered 24h | "David's email about [topic] is still unanswered. Want to reply or snooze?" |

**Proactive rules**:
- Max 3 proactive messages per day (don't be annoying)
- Never proactive before 08:00 or after 22:00 (respect quiet hours)
- If Nir ignores a proactive message, don't repeat it
- Proactive messages use softer tone — suggest, don't push

---

## Process Management

### Startup sequence
1. Load soul.md (identity)
2. Load security.md (defense rules)
3. Load core memory (Tier 1)
4. Connect to PostgreSQL
5. Connect to WhatsApp Business API
6. Validate Google OAuth tokens (refresh if needed)
7. Initialize cron jobs (briefs, checks, reminders)
8. Run health check
9. Log: "Alex is online"

### Graceful shutdown
1. Complete any in-progress LLM calls
2. Save pending memory extractions
3. Persist conversation state
4. Close database connections
5. Close WhatsApp connection
6. Log: "Alex is offline"

### Crash recovery
1. PM2 auto-restarts the process
2. On restart: run startup sequence
3. Check for undelivered reminders → deliver immediately
4. Check for unprocessed messages → process in order
5. Log: "Alex recovered from crash at {timestamp}"

---

## Configurable Timing

All times are configurable per-user. Defaults:

| Setting | Default | Config Key |
|---|---|---|
| Morning brief time | 07:30 | `brief_time` |
| Quiet hours start | 22:00 | `quiet_start` |
| Quiet hours end | 08:00 | `quiet_end` |
| Email check interval | 30 min | `email_poll_minutes` |
| Calendar sync interval | 15 min | `calendar_poll_minutes` |
| Max proactive messages/day | 3 | `max_proactive_daily` |
| Meeting reminder lead time | 15 min | `meeting_reminder_minutes` |
