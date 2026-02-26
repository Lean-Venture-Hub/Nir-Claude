# Assistant Architecture

**Date**: 2026-02-16 | **Status**: Draft | **Codename**: Nir's Assistant (TBD)

## TL;DR

A secure, always-on WhatsApp AI assistant powered by Claude, running on a cloud VPS. Connects to Gmail and Google Calendar via official APIs. Features persistent memory (vector DB), reminders, task management, daily briefs, and email summaries. Built in TypeScript/Node.js with encrypted credential storage and input sanitization.

---

## System Architecture

```
[WhatsApp User]
    ↓ (message)
[WhatsApp Business API (Meta Cloud API)]
    ↓ (webhook)
[Node.js Server on VPS]
    ├── Message Router
    │   ├── Intent Classifier (Claude)
    │   └── Input Sanitizer (anti prompt-injection)
    ├── Tool Executors
    │   ├── Gmail Module (read, summarize, draft, send)
    │   ├── Calendar Module (view, create, update events)
    │   ├── Memory Module (store, retrieve, search)
    │   ├── Reminder Module (schedule, deliver)
    │   └── Task Module (CRUD todo lists)
    ├── Context Builder
    │   ├── Memory Retrieval (relevant context)
    │   ├── Calendar Context (today's schedule)
    │   └── Email Context (recent important emails)
    └── Storage
        ├── PostgreSQL (tasks, reminders, conversation logs)
        ├── Vector DB - pgvector (memory embeddings)
        └── Encrypted Vault (OAuth tokens, API keys)
```

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Language | TypeScript + Node.js | Fast dev, great async, rich ecosystem |
| WhatsApp | Meta Cloud API (direct) | Official, stable, free tier: 1000 msgs/mo |
| LLM | Claude API (Anthropic) | Best instruction following, tool use |
| Database | PostgreSQL + pgvector | Single DB for structured data + vectors |
| Credential Storage | node-keytar / encrypted env | No plaintext secrets |
| Hosting | DigitalOcean Droplet ($6/mo) | Reliable, simple, good value |
| Process Manager | PM2 | Auto-restart, logs, monitoring |
| Scheduler | node-cron | Reminders, daily briefs, scheduled tasks |

## Core Features (v1)

### 1. Conversational AI
- Natural language via WhatsApp
- Claude handles intent detection + response generation
- Tool-use for structured actions (calendar, email, etc.)

### 2. Gmail Integration
- **Read**: Fetch recent emails, search by sender/subject
- **Summarize**: Daily digest of important emails
- **Draft & Send**: Compose and send emails via voice/text
- **Priority Detection**: Flag urgent emails
- OAuth 2.0 with encrypted token storage

### 3. Google Calendar
- **View**: Today's schedule, upcoming events, free slots
- **Create**: Schedule meetings with natural language
- **Daily Brief**: Morning summary of today's agenda
- **Conflicts**: Detect and warn about double-bookings

### 4. Memory System
- **Explicit Memory**: "Remember that X" → stored with tag
- **Implicit Memory**: Key facts auto-extracted from conversations
- **Retrieval**: pgvector similarity search + keyword matching
- **Decay**: Auto-summarize old memories, archive after 90 days
- **Categories**: People, preferences, facts, decisions, todos

### 5. Reminders
- "Remind me to X at Y" → scheduled cron job
- Delivered as WhatsApp message at specified time
- Supports recurring reminders (daily, weekly, custom)
- Stored in PostgreSQL with timezone awareness

### 6. Task Management
- Create, update, complete, delete tasks
- Group tasks by project/category
- Daily todo list generation
- Priority levels (urgent, important, normal, low)

### 7. Daily Briefs
- **Morning Brief** (configurable time, e.g., 7:30 AM):
  - Today's calendar events
  - Important unread emails
  - Pending tasks/reminders
  - Weather (optional, v2)
- Sent proactively via WhatsApp

## Security Model

| Threat | Mitigation |
|---|---|
| Unauthorized access | WhatsApp number verification (phone-locked) |
| Credential theft | Encrypted storage (no plaintext tokens) |
| Prompt injection via email | Input sanitization layer before LLM |
| API key exposure | Environment variables + encrypted vault |
| Cost spiraling | Daily spend limits + alerts |
| Data at rest | Encrypted PostgreSQL (full disk encryption on VPS) |
| Data in transit | TLS everywhere (HTTPS webhooks, API calls) |

## Data Flow: Message Processing

```
1. User sends WhatsApp message
2. Meta Cloud API → webhook → our server
3. Input sanitizer strips potential injection
4. Context builder assembles:
   - Recent conversation history (last 10 messages)
   - Relevant memories (vector search)
   - Today's calendar (if time-related)
   - Recent emails (if email-related)
5. Claude processes with tools available
6. Tool calls executed (if any)
7. Response sent back via WhatsApp API
8. Conversation + key facts stored in DB
```

## Project Structure (planned)

```
assistant/
├── src/
│   ├── index.ts              # Entry point
│   ├── server.ts             # Express webhook server
│   ├── whatsapp/             # WhatsApp API client
│   ├── llm/                  # Claude API integration
│   ├── tools/                # Tool implementations
│   │   ├── gmail.ts
│   │   ├── calendar.ts
│   │   ├── memory.ts
│   │   ├── reminders.ts
│   │   └── tasks.ts
│   ├── context/              # Context building
│   ├── security/             # Sanitization, encryption
│   └── scheduler/            # Cron jobs (briefs, reminders)
├── prisma/                   # Database schema
├── .env.encrypted            # Encrypted secrets
├── docker-compose.yml        # PostgreSQL + app
└── package.json
```

## Estimated Monthly Cost

| Item | Cost |
|---|---|
| DigitalOcean Droplet (2GB) | $6 |
| Claude API (moderate use) | $50-100 |
| WhatsApp Business API | $0-15 (1000 free msgs/mo) |
| Domain + SSL | $1 |
| **Total** | **~$57-122/mo** |

## Build Phases

| Phase | Scope | Est. Effort |
|---|---|---|
| **Phase 1** | WhatsApp ↔ Claude basic chat | Core foundation |
| **Phase 2** | Memory system (remember + retrieve) | Memory layer |
| **Phase 3** | Gmail integration (read + summarize) | Email module |
| **Phase 4** | Calendar integration (view + create) | Calendar module |
| **Phase 5** | Reminders + Tasks | Scheduling |
| **Phase 6** | Daily briefs (morning summary) | Automation |
| **Phase 7** | Polish, monitoring, cost alerts | Production-ready |

---

## Next Step

Review this architecture → then start Phase 1 (WhatsApp + Claude basic chat).
