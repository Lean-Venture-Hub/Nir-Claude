# OpenClaw Research Brief

**Date**: 2026-02-16 | **Purpose**: Understand OpenClaw architecture to build a better, secured alternative

## TL;DR

OpenClaw is an open-source WhatsApp AI assistant built in TypeScript/Node.js. It uses **Baileys** (unofficial WhatsApp Web library) for messaging, Google OAuth for Calendar/Gmail, and a hybrid SQLite memory system. While feature-rich, it has **critical security flaws**: plaintext credentials, prompt injection vectors, and unstable WhatsApp sessions. Our opportunity is to build a hardened version using the official WhatsApp Business API with proper security from day one.

---

## Architecture

| Component | OpenClaw Approach | Risk Level |
|---|---|---|
| Runtime | Single Node.js process, TypeScript | Low |
| WhatsApp | Baileys (unofficial WA Web client, QR-code auth) | HIGH - unstable, single-session, can get banned |
| LLM | Pluggable (GPT-4, Claude, local models) | Low |
| Memory | SQLite + FTS5 full-text + vector embeddings | Medium |
| Calendar | Google Calendar API via OAuth device-code flow | Medium |
| Email | Gmail API via OAuth device-code flow | Medium |
| Hosting | Self-hosted (VPS, Raspberry Pi, etc.) | Low |
| Credential Storage | Plaintext in config files | CRITICAL |

## Key Features

- **Conversational AI** via WhatsApp (text + voice messages)
- **Google Calendar**: View events, create meetings, get daily briefs
- **Gmail**: Read, summarize, draft, send emails
- **Memory**: Persistent memory across conversations (daily logs + MEMORY.md file)
- **Reminders**: Time-based reminders delivered via WhatsApp
- **Tasks/Todo**: Create and manage task lists
- **Web browsing**: Can search and browse web pages
- **Skills/Plugins**: Extensible skill system (but 7.1% of community skills leaked credentials)

## WhatsApp Integration Details

- Uses **Baileys** library - reverse-engineered WhatsApp Web protocol
- Authenticates via QR code scan (like WhatsApp Web)
- **Problems**: Single session only, frequent disconnects, Meta can ban the number, no official support
- **Alternative (our approach)**: WhatsApp Business API (official, stable, scalable, costs ~$0.005-0.08/message)

## Memory System

- **Daily conversation logs**: Stored as markdown files per day
- **MEMORY.md**: Durable long-term memory file (manually + auto-updated)
- **Hybrid search**: SQLite FTS5 (keyword) + vector embeddings for retrieval
- **Problem**: Context window burns as memory grows, responses slow from 3s to 119s over time
- **Our opportunity**: Use proper vector DB (Pinecone/Weaviate) with smart retrieval + summarization

## Calendar & Email Integration

- Google Workspace APIs via OAuth 2.0 device-code flow
- User must set up their own GCP project + OAuth credentials
- Tokens stored in plaintext config files
- Scopes: calendar.events, gmail.readonly, gmail.send, gmail.modify

## Security Vulnerabilities (Critical for Our Design)

| Vulnerability | Details |
|---|---|
| Plaintext credentials | OAuth tokens, API keys stored unencrypted |
| Prompt injection | Emails/calendar events can contain malicious prompts |
| Skill system | Community skills can exfiltrate data (7.1% did) |
| No auth layer | Anyone with the WhatsApp number can interact |
| Browser control | Full web access = potential for abuse |
| No rate limiting | No protection against abuse or cost spiraling |

## Cost Structure

| Item | Monthly Cost |
|---|---|
| LLM API (GPT-4/Claude) | $50-200 |
| Hosting (VPS) | $5-25 |
| WhatsApp Business API | $10-50 (volume dependent) |
| Vector DB (managed) | $0-25 |
| **Total estimate** | **$65-300/mo** |

## Lessons for Our Build

### Keep from OpenClaw
- Hub-and-spoke architecture (simple, effective)
- Hybrid memory (keyword + vector search)
- Daily briefs concept
- Pluggable LLM support

### Fix / Improve
- **WhatsApp**: Use official Business API (not Baileys)
- **Security**: Encrypted credential storage (use OS keychain or encrypted vault)
- **Auth**: PIN/passphrase verification before sensitive actions
- **Memory**: Proper vector DB with automatic summarization + decay
- **Prompt injection**: Input sanitization layer before LLM processing
- **Rate limiting**: Per-user, per-action limits
- **Skill system**: Sandboxed execution, no arbitrary code
- **Monitoring**: Logging, alerts, cost tracking dashboard

---

## Next Step

Define our own bot's architecture, feature set, and security model in `architecture.md`.
