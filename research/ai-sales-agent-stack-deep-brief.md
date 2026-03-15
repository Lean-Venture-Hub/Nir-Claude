# AI Sales Agent Stack — Tool & API Research (2025-2026)

**TL;DR:** For a lean autonomous AI sales agent targeting SMBs, the recommended stack is: **Retell.ai** (voice) + **Instantly.ai** (email) + **Twilio** (SMS) + **Supabase** (CRM/backend) + **LangGraph + Claude** (agent brain) + **Apollo.io** (lead data). Total operating cost for a moderate-volume operation: ~$300-800/month before LLM usage. Avoid custom voice stack (too much engineering) and paid AI SDR platforms like 11x.ai (too expensive for a 1-person operation).

---

## 1. Voice AI for Phone Calls

### Pricing Comparison (per-minute, fully loaded)

| Platform | Base Rate | Realistic Total | Latency | Turn-Taking Quality |
|---|---|---|---|---|
| **Bland.ai** | $0.09-0.14/min | ~$0.09-0.14 (all-in) | ~800ms | Poor — continues 1-2s after interruption |
| **Vapi** | $0.05/min (platform only) | ~$0.13-0.33/min | ~700ms | Sensitive — cuts off on background noise |
| **Retell.ai** | $0.07-0.08/min (voice) | ~$0.13-0.31/min | ~600-800ms | Best — proprietary turn-taking model |
| **Custom Build** | No platform fee | ~$0.09-0.20/min | 440-1600ms | Must build from scratch (very hard) |

### Custom Build Component Costs
- Twilio telephony: ~$0.008-0.014/min
- Deepgram STT: ~$0.004-0.007/min
- Claude LLM: ~$0.02-0.06/min
- ElevenLabs TTS: ~$0.06-0.30/min

### Hidden Fees to Watch
- **Bland.ai**: $0.015/call for failed dials; $0.025/min transfer fee; +$0.02/min for custom voices
- **Vapi**: +$0.01/min telephony; +$0.04-0.07/min premium TTS; $10/line/month concurrency
- **Retell.ai**: +$0.01-0.015/min telephony; $0.005/dial outbound batch; +$0.005/min knowledge base
- **ElevenLabs HIPAA**: +$1,000/month flat add-on

### Compliance
| Platform | HIPAA | SOC2 |
|---|---|---|
| Bland.ai | Yes (enterprise) | - |
| Vapi | +$1,000/mo add-on | Yes |
| Retell.ai | Included | Yes (+ GDPR) |
| Custom | Component-level | Depends |

### Verdict
**Use Retell.ai.** Best turn-taking, Claude 3.5 native support (+$0.02-0.06/min), SOC2/HIPAA included, 99.99% uptime. Avoid custom stack — WebSocket audio stream management (resampling, channel layout, frame alignment) is a significant engineering tax. Vapi is best if you need max control over every component.

---

## 2. Email at Scale

| Provider | Pricing | Cold Outreach OK? | Warm-up | Best For |
|---|---|---|---|---|
| **Instantly.ai** | $37-97/mo flat (100k emails) | Yes — built for it | Automated, unlimited accounts | AI SDR outbound cold email |
| **AWS SES** | $0.10/1,000 emails | No — banned | None native (+$0.07/1k for manager) | Transactional/app emails only |
| **Resend** | $20/mo 50k; $90/mo 100k | No — not designed for it | Ticket support only | SaaS app triggers, dev-friendly API |
| **Postmark** | $15/mo 10k; $695/mo 1M | No — banned | Excellent shared IPs | Mission-critical transactional, <1s delivery |

### Architecture Recommendation
Run **two separate email infrastructures**:
1. **Instantly.ai** — all outbound cold sales sequences
2. **AWS SES or Postmark** — transactional notifications (never mix with cold outreach to protect domain reputation)

---

## 3. SMS & WhatsApp

### SMS Pricing (US)

| Provider | Per SMS | A2P 10DLC Setup | Notes |
|---|---|---|---|
| **Twilio** | ~$0.0079-0.0083 | Manual, 2-8 weeks | Best docs, most complex pricing |
| **Telnyx** | ~$0.004 + carrier fees | Developer-managed | Cheapest wholesale pricing |
| **Pingram** | $0.0105 flat | Automated, immediate | Fastest time-to-market for US compliance |

### WhatsApp Business API

| Provider | Pricing | Notes |
|---|---|---|
| **Twilio** | $0.005/msg + Meta template fee | Official BSP, enterprise-grade |
| **YCloud / Wati** | Meta fees + platform subscription | No-code friendly, good for SMB |
| **WasenderAPI** | $6/mo unlimited (unofficial) | NOT official Meta API — unstable for production |

### Verdict
**Twilio for SMS** (best Claude/webhook integration, battle-tested). **YCloud or Wati for WhatsApp** if you want no-code setup; Twilio if you want API control. Avoid unofficial WhatsApp APIs for anything production.

---

## 4. AI Sales Agent Platforms

### Open-Source Frameworks (Build On)

| Framework | Paradigm | Claude Compatible | Production Readiness | Build On? |
|---|---|---|---|---|
| **LangGraph** | Graph-based state machines | Yes (model-agnostic) | High | Yes — best for complex conditional sales flows |
| **CrewAI** | Role-based multi-agent teams | Yes | Medium-High | Yes — fast for SDR team modeling |
| **AutoGen** | Conversation-driven multi-agent | Yes | Medium | Research/complex reasoning only |
| **SalesGPT** | Context-aware sales stages | Yes (LangChain) | Medium | Good starting template, not production-ready alone |

### Paid AI SDR Platforms (Buy Off-the-Shelf)

| Platform | Pricing | Claude Integration | Worth It? |
|---|---|---|---|
| **11x.ai** | ~$5,000-10,000/mo | Yes (under the hood) | No — enterprise only, annual contracts |
| **Artisan AI (Ava)** | ~$999-2,400+/mo | Proprietary | No — cheaper to build with Apollo + LangGraph |
| **AiSDR** | ~$750-900/mo | Proprietary | Maybe for MVP testing, not long-term |

### Build vs. Buy Economics
- **Custom open-source stack** (LangGraph + Claude API + Supabase): ~$50-100/mo infrastructure + LLM usage
- **Paid AI SDR platforms**: $750-10,000/mo with annual lock-in
- **Verdict**: Build on LangGraph + Claude. Paid platforms are overpriced wrappers. Use SalesGPT as a reference implementation only.

---

## 5. CRM Backend

| Platform | AI/Vector Support | Scale Ceiling | Dev Speed | Best For |
|---|---|---|---|---|
| **Supabase** | pgvector built-in, RAG-ready | Millions of rows, RLS | Fast (BaaS) | Production AI agent backends |
| **Airtable** | No vector support | Hits API limits fast | Fastest | Internal prototypes, non-technical teams |
| **Raw Postgres + Pinecone** | Separate vector DB (best perf) | Unlimited | Slow (DevOps needed) | Enterprise scale only |

### Verdict
**Supabase is the clear winner** for a 1-person AI sales agent operation. Single platform for structured CRM data + vector embeddings (agent memory/RAG), real-time subscriptions, auth, and serverless functions. Airtable is fine for prototyping but will break under programmatic agent load.

---

## 6. Lead Enrichment

| Platform | Pricing | Unit Cost | SMB Data Quality | Best For |
|---|---|---|---|---|
| **Apollo.io** | $49-99/user/mo | Predictable flat | High (275M+ contacts) | High-volume straightforward outbound |
| **Clay** | $149-720+/mo | ~$0.14/enrichment | Highest (waterfall, 50+ sources) | Hyper-targeted ABM, technical RevOps |
| **Clearbit/Breeze** | HubSpot $30+ + Breeze $45+ | ~$0.10/enrichment, no rollover | Medium | HubSpot-native teams only |

### Notes
- **Apollo.io**: Best value for standard SMB outreach. Includes dialer and sequencing tools so you may not need a separate email tool.
- **Clay**: Highest quality via cascading enrichment (queries 50+ providers until verified email found). Costs spiral fast at high volume — best for targeted lists, not mass campaigns.
- **Clearbit**: Now HubSpot Breeze. Credits expire monthly (no rollover). Only viable if already deep in HubSpot ecosystem.

---

## Recommended Stack (1-Person Operation, SMB Focus)

| Layer | Tool | Monthly Cost (est.) |
|---|---|---|
| Voice AI | Retell.ai (pay-as-you-go) | $0.13-0.31/min × volume |
| Email outbound | Instantly.ai Growth | $37-97 flat |
| Email transactional | AWS SES | ~$10-20 |
| SMS | Twilio | ~$0.008/msg × volume |
| WhatsApp | YCloud or Twilio | Meta fees + platform |
| Agent framework | LangGraph + Claude API | LLM usage only |
| CRM/Backend | Supabase | $0-25 (free tier generous) |
| Lead data | Apollo.io Basic | $49/mo |
| **Total baseline** | | **~$200-350/mo + usage** |

---

## So What? (For This Business)

1. **Voice is the differentiator.** Retell.ai with Claude 3.5 is production-ready today for autonomous outbound calls to auto-repair, dentists, and other SMB verticals. ~$0.15-0.25/min all-in is acceptable for qualifying leads.
2. **Email volume economics favor Instantly.ai** over transactional ESPs for cold outreach. Never send cold email from your main domain — use aged domains through Instantly.
3. **Don't buy AI SDR platforms.** 11x.ai/Artisan are reselling Claude/GPT + LangGraph at a 20-100x markup. Build it.
4. **Apollo.io is sufficient for SMB data.** Clay is overkill unless you're doing highly targeted ABM with <500 accounts.
5. **Build agent memory into Supabase from day one.** Retrofitting pgvector later is painful.

---

*Research date: 2026-03-15. Sources: Gemini Deep Research (44+ citations per topic). Verify pricing on provider websites before committing — Voice AI pricing in particular changes frequently.*
