# Content Pipeline: "The PM-AI Thought Leader Stack"

## Overview

```
LAYER 1: TREND RADAR (daily/weekly, automated)
  Sources -> Filter -> Score -> Surface top signals
        |
LAYER 2: TOPIC GENERATOR (weekly, semi-automated)
  Trends + Your POV angles -> Ranked topic suggestions
        |
LAYER 3: SUCCESSFUL POST ANALYZER (on-demand)
  What's working in your niche -> Patterns to apply
        |
LAYER 4: CONTENT GENERATOR (per topic)
  Topic -> 3-5 variations (thread, post, article, contrarian)
```

---

## LAYER 1: Trend Radar

**Purpose:** Automatically surface relevant AI/product/design news before it's everywhere

### Sources to Monitor

| Category | Sources | Why |
|----------|---------|-----|
| AI News | @OpenAI, @AnthropicAI, @GoogleAI, Hacker News "AI" | Tool launches, model updates |
| PM Twitter | @lennysan, @shreyas, @joulee, @gibsonbiddle | What senior PMs discuss |
| Product Hunt | AI & Design categories | New tools to review |
| Substacks | Lenny's Newsletter, Stratechery, One Useful Thing (Ethan Mollick) | Deep takes |
| Reddit | r/ProductManagement, r/UXDesign, r/artificial | Community pulse |
| LinkedIn | Your feed + "AI product management" search | B2B angle |

### Automation Setup (n8n or Make.com)

```
Trigger: Daily at 7am
    |
Fetch: RSS feeds + Twitter lists + Reddit API
    |
Filter: Keywords match your pillars:
  - "product manager" + "AI"
  - "AI tools" + "workflow"
  - "UX" + "AI" + "design"
  - "founder" + "AI"
  - "Claude" OR "ChatGPT" OR "GPT" + "productivity"
    |
Score: Engagement (likes, comments, upvotes)
    |
Dedupe & Rank: Top 10-15 signals
    |
Output: Daily digest to Notion/Slack/Email
```

### Quick-Start (No-Code)

- **Feedly + AI Feed** - $12/mo, monitors RSS + prioritizes by engagement
- **Perplexity Pro** - $20/mo, daily "what's new in AI for product managers" query
- **SparkToro** - Shows what your audience follows/reads

---

## LAYER 2: Topic Generator

**Purpose:** Turn raw trends into your unique angle topics weekly

### Your 6 Content Pillars

1. **PMs Using AI** - Tactical, how-to, workflows
2. **Becoming an AI Expert** - Learning paths, skill-building
3. **Philosophy of AI** - Big questions, ethics, future of work
4. **Design + Product** - UX/AI intersection, craft
5. **Entrepreneurship** - Building with AI, founder lessons
6. **Tools & News** - Reviews, comparisons, what's new

### The Topic Generation Prompt

```
You are a content strategist for a senior product/UX leader with 20 years of experience who writes about AI for product managers, designers, and founders.

CONTEXT:
- Voice: Experienced, slightly contrarian, practical over hype
- Audience: PMs, designers, founders who are AI-curious but overwhelmed
- Goal: Thought leadership that's useful, not performative

THIS WEEK'S TRENDS:
[Paste your top 10-15 signals from Layer 1]

CONTENT PILLARS:
1. PMs Using AI (tactical)
2. Becoming an AI Expert (learning)
3. Philosophy of AI (big ideas)
4. Design + Product (craft)
5. Entrepreneurship (building)
6. Tools & News (what's new)

TASK:
Generate 15 topic ideas across these pillars. For each:
- Topic title (punchy, specific)
- Pillar it maps to
- The "hot take" angle that makes it yours (not generic advice)
- Why now (connection to this week's trends)

Format as a table. Prioritize topics where your 20 years of experience gives you a unique POV that AI-native creators can't fake.
```

---

## LAYER 3: Successful Post Analyzer

**Purpose:** Before writing, analyze what's working in your niche right now

### The Analysis Prompt

```
Research the top 10 most engaging posts from the last 30 days about: [YOUR TOPIC]

Focus on:
- LinkedIn posts from PMs/designers with 500+ reactions
- Twitter/X threads with 1000+ likes
- Substack posts with high comment counts

For each, extract:
1. Hook (first line that grabbed attention)
2. Structure (how they organized it)
3. Length (word count, thread length)
4. What made it shareable (insight, controversy, utility)
5. Comment sentiment (what resonated most)

Then identify:
- 3 patterns to replicate
- 2 gaps/angles no one covered
- 1 contrarian take I could own
```

### Tools for This Layer

- **Perplexity** - Quick research on what's been written
- **Kleo** (Chrome extension) - Shows LinkedIn post analytics on others' posts
- **Tweetdeck/Typefully** - Sort by engagement in your niche
- **SparkToro Audience Research** - What your audience engages with

---

## LAYER 4: Content Generator

**Purpose:** Turn one topic into multiple format variations

### The Master Generation Prompt

```
You are writing as a senior product/UX leader with 20 years of experience.

VOICE GUIDELINES:
- Confident but not arrogant ("In my experience..." not "Everyone knows...")
- Specific examples over generic advice
- Contrarian where earned (you've seen cycles repeat)
- Practical > theoretical
- Occasional dry humor
- Never use: "game-changer", "unlock", "leverage", "dive deep"

TOPIC: [Your chosen topic]
KEY INSIGHT: [The core idea/hot take]
SUPPORTING POINTS: [2-3 things that back it up]

Generate 4 variations:

---
VERSION 1: LinkedIn Post (under 1300 characters)
- Hook in first line (pattern interrupt or bold claim)
- 3-5 short paragraphs
- End with question or CTA
- No hashtags in body, 3-5 at very end

---
VERSION 2: Twitter/X Thread (5-8 tweets)
- Tweet 1: Hook + promise
- Tweets 2-6: One idea per tweet, can stand alone
- Tweet 7: Summary or bold conclusion
- Tweet 8: CTA (follow, reply, share)

---
VERSION 3: Contrarian Hot Take (single punchy post)
- The spicy version that might get pushback
- Under 280 characters
- Designed for engagement/debate

---
VERSION 4: Long-form Intro (first 200 words of article)
- For Substack/Medium
- Story-led opening OR bold claim opening
- Sets up the rest of the piece
```

### Quick Variation Matrix

| Format | Length | Platform | Tone |
|--------|--------|----------|------|
| Thread | 5-8 tweets | X/Twitter | Tactical |
| Post | 1000-1300 chars | LinkedIn | Professional |
| Hot take | <280 chars | Both | Spicy |
| Article intro | 200 words | Substack | Thoughtful |
| Carousel script | 8-10 slides | LinkedIn | Visual |

---

## Weekly Workflow

### Time Investment: ~3-4 hours/week

| Day | Task | Time | Tools |
|-----|------|------|-------|
| **Monday AM** | Review Trend Radar digest | 15 min | Notion/Email |
| **Monday AM** | Run Topic Generator prompt | 20 min | Claude |
| **Monday AM** | Pick 2-3 topics for the week | 10 min | You |
| **Tuesday** | Run Successful Post Analyzer on Topic 1 | 20 min | Perplexity + Claude |
| **Tuesday** | Generate 4 variations of Topic 1 | 30 min | Claude |
| **Tuesday** | Edit/personalize best variation | 30 min | You |
| **Wednesday** | Post Topic 1 content | 5 min | Native or scheduler |
| **Thursday** | Repeat for Topic 2 | 1 hr | Same flow |
| **Friday** | Repeat for Topic 3 (optional) | 1 hr | Same flow |

---

## Tech Stack

### Minimum Viable Stack (start here)

| Layer | Tool | Cost |
|-------|------|------|
| Trend Radar | Perplexity Pro + manual Twitter/LinkedIn | $20/mo |
| Topic Generator | Claude Pro | $20/mo |
| Post Analyzer | Perplexity + Kleo | Free |
| Content Generator | Claude Pro | (included) |
| **Total** | | **$40/mo** |

### Scaled Stack (when ready)

| Layer | Tool | Cost |
|-------|------|------|
| Trend Radar | n8n + Tavily API + RSS | ~$30/mo |
| Topic Generator | Claude API (batch) | ~$10/mo |
| Post Analyzer | Perplexity API | ~$20/mo |
| Content Generator | Claude API | ~$20/mo |
| Scheduling | Typefully or Buffer | $15/mo |
| **Total** | | **~$95/mo** |

---

## Quick Start: This Week

1. Set up Perplexity Pro - Ask daily: "What's new in AI for product managers this week?"
2. Save these prompts somewhere accessible (Notion, text file)
3. Run the Topic Generator with this week's trends
4. Pick ONE topic and run it through all 4 layers
5. Post it and see what resonates
