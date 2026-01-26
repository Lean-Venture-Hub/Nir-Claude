# Content Creation System - Suggestion

## Overview

A social content layer for LinkedIn/X posts, ghostwriting for employees, built on trend discovery and personalized writing style.

---

## 1. Discovery Engine

**Purpose:** Surface what's trending around user's ICP and industry.

### Scan Frequency
- **Daily batch scan** - Automated, runs overnight
- **Manual "Scan Now" button** - User-triggered real-time scan when needed

### Data Sources
| Source | What to Scan | Output |
|--------|--------------|--------|
| X/Twitter | Hashtags, viral posts in niche | Trending topics, hook styles |
| LinkedIn | Top posts from ICP job titles | Engagement patterns, formats |
| Google Trends | Rising searches in industry | Timely angles |
| Competitors | Their social content | Gaps and opportunities |

### Discovery Output
```
Topic: [Trending subject]
Why Now: [Timeliness signal]
ICP Interest: [Why audience cares]
Suggested Angle: [User's unique take based on brand/expertise]
Source Posts: [2-3 reference links]
Source: [linkedin | x | google_trends | competitor]
```

---

### Source Monitoring Algorithms

#### LinkedIn Monitoring

**What to track:**
- Posts from accounts matching user's ICP job titles (VP Marketing, CMO, Founder, etc.)
- Posts in user's industry hashtags
- Posts from competitors' company pages
- Comments/engagement on industry thought leaders

**Signals for trending:**
```
linkedin_score = (
  likes_velocity * 0.3 +           # likes per hour since posted
  comments_velocity * 0.4 +        # comments = higher signal
  reposts * 0.2 +
  icp_author_match * 0.1           # bonus if author matches ICP
)
```

**Topic extraction:**
- Cluster posts by semantic similarity
- Extract common themes/keywords
- Identify hook patterns that drive engagement

**Refresh:** Daily scan of last 48 hours of posts

---

#### X/Twitter Monitoring

**What to track:**
- Trending hashtags in user's industry
- Viral tweets (>500 likes) from accounts user's ICP follows
- Quote tweets and ratio patterns (controversy = engagement)
- Threads getting high bookmark rates

**Signals for trending:**
```
x_score = (
  retweet_velocity * 0.25 +        # spread speed
  quote_tweet_ratio * 0.25 +       # discussion indicator
  bookmark_rate * 0.3 +            # save = high intent
  reply_sentiment * 0.2            # positive replies = resonance
)
```

**Topic extraction:**
- Track hashtag co-occurrence
- Identify conversation clusters
- Extract hot takes vs evergreen insights

**Refresh:** Every 6 hours (X moves faster)

---

#### Google Trends Monitoring

**What to track:**
- Rising searches in user's industry category
- Breakout keywords (>5000% increase)
- Related queries to user's core topics
- Regional trends for user's target market

**Signals for trending:**
```
trends_score = (
  search_volume_change * 0.4 +     # velocity of increase
  is_breakout * 0.3 +              # breakout = urgent
  related_to_icp_topics * 0.2 +    # relevance filter
  geographic_match * 0.1           # user's target regions
)
```

**Topic extraction:**
- Map rising queries to content angles
- Identify "why now" timing hooks
- Connect to news events when applicable

**Refresh:** Daily (Trends data updates less frequently)

---

#### Cross-Source Aggregation

**When same topic appears across sources:**
```
combined_score = (
  max(linkedin_score, x_score, trends_score) * 0.6 +
  source_count_bonus * 0.4         # +20% per additional source
)
```

**Priority boost:**
- Topic on 2 sources = 1.2x multiplier
- Topic on all 3 sources = 1.5x multiplier (hot topic, act fast)

**Deduplication:**
- Semantic matching to merge similar topics
- Keep highest-scoring source as primary
- Show all sources in idea card

---

## 2. Writing Style Profile

**Purpose:** Capture user's authentic writing style and tone for consistent content generation.

### Input Methods
| Method | User Action |
|--------|-------------|
| **Paste examples** | 3-5 posts they've written or admire |
| **LinkedIn import** | Pull their existing posts via URL |
| **Style questionnaire** | 5 quick questions (tone, topics, no-gos) |

### Style Profile Output
```
Tone: [casual/professional/provocative/etc]
Sentence Style: [short punchy / long flowing]
Hooks: [question / stat / story / bold claim]
Vocabulary: [words they use, words to avoid]
POV: [first person / we / third person]
Signature Elements: [emoji use, hashtag style, CTA patterns]
```

**Storage:** 1 profile per user (ghostwriting with multiple profiles in future phase)

**Location:** Settings > Writing Style

---

## 3. Content Creation

**Purpose:** Generate publish-ready posts from brief to final.

### Creation Flow
```
Idea Selected → Brief Generated → Full Post Created → User Edits → Image Generated → Ready to Copy
```

### Post Generation Includes
| Element | How |
|---------|-----|
| **Hook** | 3 options using user's preferred hook style |
| **Body** | Voice-matched, best practices applied |
| **CTA** | Engagement-focused (question, share prompt) |
| **Hashtags** | Platform-appropriate (3-5 for LinkedIn, 1-2 for X) |
| **Image** | Auto-generated or suggested from existing assets |

### Post Formats Supported
- Text-only (LinkedIn, X)
- Text + single image
- Carousel (LinkedIn) - multi-slide
- Thread (X) - multi-tweet

### Edit Modes
| Mode | Function |
|------|----------|
| **Direct edit** | Type in textarea |
| **AI rewrite** | "Make it shorter" / "More provocative" / "Add story" |
| **Tone shift** | Slider or presets (casual ↔ professional) |
| **Hook swap** | Cycle through alternative hooks |

---

## 4. User Flow (UX)

### Navigation Structure
```
/content
├── Ideas Feed     ← Discovery, pick topics (default)
├── Saved Ideas    ← Ideas bookmarked for later
├── Drafts         ← Saved posts, not yet published
├── Published      ← Archive of posted content
├── Monitor        ← Analytics & insights
└── Personalize    ← Refine writing style
```

---

### Screen 1: Ideas Feed (`/content`)

**Layout:** Vertical feed of idea cards + top action bar

**Top Bar:**
```
[Ideas Feed] [Saved (2)] [Drafts (3)] [Published] [Monitor] [Personalize]     [🔄 Scan Now]
```

**Idea Card Contains:**
```
┌────────────────────────────────────┐
│ 🔥 Trending in [ICP segment]       │
│                                    │
│ [Topic/Theme]                      │
│ "Your angle: [suggested take]"     │
│                                    │
│ [in] [𝕏] [📈] · [Freshness]        │  ← Source badges (LinkedIn, X, Trends)
│              [Save 🔖] [Create →]  │
└────────────────────────────────────┘
```

**Source Badges:**
| Badge | Source | Meaning |
|-------|--------|---------|
| `in` | LinkedIn | Trending on LinkedIn |
| `𝕏` | X/Twitter | Trending on X |
| `📈` | Google Trends | Rising in search |

Multiple badges = cross-platform trend (higher priority)

**Filters:**
- Platform: LinkedIn / X / Both
- Topic cluster: [from user's industry tags]
- Freshness: Today / This week / Evergreen

**Empty State:** "No trending topics yet. Click 'Scan Now' or check back tomorrow."

---

### Ideas Feed Algorithm

**Sorting Logic (daily scan):**
```
1. STILL TRENDING (top) - Ideas from previous days that are still trending today
   → Sorted by: trending_score DESC, then days_trending DESC

2. NEW TODAY - Fresh ideas from today's scan
   → Sorted by: trending_score DESC

3. COOLING DOWN (below fold) - Previously trending, no longer in today's scan
   → Sorted by: last_trending_date DESC, then original_score DESC
```

**Trending Score Calculation:**
```
trending_score = (source_engagement * 0.4) + (icp_relevance * 0.4) + (recency * 0.2)

Where:
- source_engagement = normalized engagement from source posts
- icp_relevance = match score to user's ICP/industry
- recency = decay factor based on hours since first seen
```

**Lifecycle:**
| Status | Condition | Display |
|--------|-----------|---------|
| 🔥 Hot | In today's scan, score > 70 | Top of feed, fire badge |
| 📈 Trending | In today's scan, score 40-70 | Upper feed |
| 📉 Cooling | Was trending, not in today's scan | Below fold |
| ❄️ Cold | Not trending for 7+ days | Bottom, grayed |
| 🗑️ Expired | 30 days old, never used/saved | Auto-deleted |

**Saved Ideas:** Exempt from 30-day auto-delete. Persist until manually removed.

---

### Screen 1b: Saved Ideas (`/content/saved`)

**Purpose:** Ideas bookmarked for later use

**Layout:** Same card format as Ideas Feed

**Saved Card:**
```
┌────────────────────────────────────┐
│ [Original trending badge]          │
│                                    │
│ [Topic/Theme]                      │
│ "Your angle: [suggested take]"     │
│                                    │
│ Saved [date] · Originally [date]   │
│            [Unsave ✕] [Create →]   │
└────────────────────────────────────┘
```

**Note:** Saved ideas don't expire - user explicitly saved them for a reason.

**Empty State:** "No saved ideas. Bookmark ideas from the feed to keep them."

---

### Screen 2: Post Creator (`/content/create/:id`)

**Layout:** Split view or single column

```
┌─────────────────────────────────────────────┐
│ ← Back to Ideas                    [Draft ▾]│
├─────────────────────────────────────────────┤
│ BRIEF                                       │
│ Topic: [X]                                  │
│ Angle: [Y]                                  │
│ Platform: [LinkedIn]        [Regenerate]    │
├─────────────────────────────────────────────┤
│ POST PREVIEW                                │
│ ┌─────────────────────────────────────────┐ │
│ │ [Hook - editable]                       │ │
│ │                                         │ │
│ │ [Body - editable]                       │ │
│ │                                         │ │
│ │ [CTA - editable]                        │ │
│ │                                         │ │
│ │ [Hashtags]                              │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ [Swap Hook ↻] [AI Rewrite ✨] [Tone ◐]      │
├─────────────────────────────────────────────┤
│ IMAGE (separate lightweight flow)           │
│ [Generated image preview]                   │
│ [Regenerate] [Upload Own] [No Image]        │
├─────────────────────────────────────────────┤
│ [Save Draft]                [Mark Published]│
└─────────────────────────────────────────────┘
```

**States:**
- Generating (spinner on post area)
- Draft (saved, editable)
- Published (moved to archive)

**Image Generation:** Separate simplified UX (not reusing Ad Creator) - quick generation optimized for social post images.

---

### Screen 3: Drafts (`/content/drafts`)

**Layout:** List/grid of saved drafts

**Draft Card:**
```
┌────────────────────────────────────┐
│ [Platform icon] [Topic snippet]    │
│                                    │
│ "[First line of post...]"          │
│                                    │
│ Saved [date]           [Edit] [⋮]  │
└────────────────────────────────────┘
```

**Actions:**
- Edit → opens Post Creator
- Delete
- Mark as Published

**Empty State:** "No drafts yet. Create a post from the Ideas Feed."

---

### Screen 4: Published (`/content/published`)

**Layout:** Timeline of published posts (read-only archive)

**Published Card:**
```
┌────────────────────────────────────┐
│ [Platform icon] Published [date]   │
│                                    │
│ "[Post content preview...]"        │
│                                    │
│ [View Full] [Copy Again] [Delete]  │
└────────────────────────────────────┘
```

**Purpose:**
- Reference for what you've posted
- Training data for writing style
- Source for Monitor analytics

**Empty State:** "No published posts yet. Mark posts as published after posting."

---

### Screen 5: Monitor (`/content/monitor`)

**Layout:** Analytics dashboard (API-ready UI, populated when publishing APIs connected)

```
┌─────────────────────────────────────────────┐
│ MONITOR                        [Date Range ▾]│
├─────────────────────────────────────────────┤
│ OVERVIEW                                    │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│ │ Posts   │ │ Total   │ │ Avg     │        │
│ │ 12      │ │ Engage  │ │ Engage  │        │
│ │ this mo │ │ 2.4K    │ │ 198     │        │
│ └─────────┘ └─────────┘ └─────────┘        │
├─────────────────────────────────────────────┤
│ TOP PERFORMING POSTS                        │
│ 1. [Post preview] - 542 likes, 38 comments  │
│ 2. [Post preview] - 312 likes, 21 comments  │
│ 3. [Post preview] - 287 likes, 19 comments  │
├─────────────────────────────────────────────┤
│ INSIGHTS                                    │
│ • Best day: Tuesday (2.3x avg engagement)   │
│ • Best time: 8-9am                          │
│ • Top theme: [topic] - 3x better than avg   │
│ • Hook style: Questions outperform stats    │
├─────────────────────────────────────────────┤
│ RECOMMENDATIONS                             │
│ → Post more about [topic] - resonates well  │
│ → Try posting on Tuesday mornings           │
│ → Your audience responds to questions       │
└─────────────────────────────────────────────┘
```

**Data Source:** Auto-pull via LinkedIn/X API (when connected)

**Empty State (No API connected):**
```
┌─────────────────────────────────────────────┐
│         📊 Analytics Coming Soon            │
│                                             │
│   Connect your LinkedIn or X account to     │
│   track post performance automatically.     │
│                                             │
│   [Connect LinkedIn]  [Connect X]           │
│                                             │
│   Until then, keep creating great content!  │
└─────────────────────────────────────────────┘
```

**Empty State (API connected, no data yet):**
"No published posts to analyze yet. Publish posts to see performance insights."

---

### Screen 6: Personalize (`/content/personalize`)

**Purpose:** Continuously refine writing style profile

**Layout:** Settings-style page with sections

```
┌─────────────────────────────────────────────┐
│ PERSONALIZE YOUR WRITING STYLE              │
├─────────────────────────────────────────────┤
│ EXAMPLE POSTS                               │
│ Train the AI with posts you've written      │
│ or posts you admire.                        │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ "My first post example that shows..."   │ │
│ │                              [Remove ✕] │ │
│ └─────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────┐ │
│ │ "Another example of my writing..."      │ │
│ │                              [Remove ✕] │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ [+ Add Example Post]  [Import from LinkedIn]│
├─────────────────────────────────────────────┤
│ STYLE PREFERENCES                           │
│                                             │
│ Tone:        [Casual ──●────── Professional]│
│ Length:      [Concise ────●─── Detailed]    │
│ Emoji use:   [None ●─────────── Frequent]   │
│ Hashtags:    [Minimal ──●───── Heavy]       │
├─────────────────────────────────────────────┤
│ CUSTOM INSTRUCTIONS                         │
│ Add specific guidance for your content      │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ Always mention my company ScaleFox      │ │
│ │ Never use the word "synergy"            │ │
│ │ End posts with a question               │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                  [+ Add]    │
├─────────────────────────────────────────────┤
│ TOPICS I COVER                              │
│ Help the AI understand your expertise       │
│                                             │
│ [AI Marketing ✕] [B2B SaaS ✕] [LinkedIn ✕]  │
│ [+ Add Topic]                               │
├─────────────────────────────────────────────┤
│ PREVIEW                                     │
│ See how your style generates                │
│                                             │
│ [Generate Sample Post]                      │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ "Sample post generated with your        │ │
│ │ current style settings..."              │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│                              [Save Changes] │
└─────────────────────────────────────────────┘
```

**Sections:**
| Section | Purpose |
|---------|---------|
| Example Posts | Training data - paste or import posts |
| Style Preferences | Quick sliders for common style attributes |
| Custom Instructions | Freeform rules (like "always/never" statements) |
| Topics I Cover | Tag-based expertise areas |
| Preview | Test current settings with sample generation |

**Empty State:** First-time setup flow prompting user to add 2-3 example posts.

---

## 5. Data Model (Simplified)

```
User
├── writing_style_profile (JSON)
│   ├── example_posts []
│   ├── style_sliders {tone, length, emoji, hashtags}
│   ├── custom_instructions []
│   └── topics []
├── industry_tags []
├── icp_id (reference)
└── content_posts []

ContentIdea
├── topic
├── angle
├── source_links []
├── trending_score (0-100, recalculated daily)
├── source_engagement (normalized)
├── icp_relevance_score
├── first_seen_at
├── last_trending_at
├── days_trending (counter)
├── is_saved (boolean)
├── saved_at
└── status (trending, cooling, cold, used, expired)

ContentPost
├── idea_id (optional - can create without idea)
├── platform (linkedin, x)
├── hook
├── body
├── cta
├── hashtags []
├── image_url
├── status (draft, published)
├── published_at
└── engagement (JSON - auto-pulled via API)
```

**Idea Lifecycle Rules:**
- `trending` → in today's scan
- `cooling` → was trending, not in today's scan
- `cold` → not trending for 7+ days
- `used` → converted to a post
- `expired` → 30 days old, auto-deleted (unless `is_saved = true`)

---

## 6. Integration with Existing ScaleFox

| Existing Feature | Integration |
|------------------|-------------|
| ICP/Personas | Drives topic relevance scoring |
| Brand Voice | Seeds initial voice profile |
| Smart Context | Available in post generation |
| Insights | Informs angle suggestions |
| Credits | Post generation consumes credits |

### Nav Placement
```
📚 AI Ad Library
✏️ Create
   ├─ Ads Studio
   ├─ Content Studio  ← NEW
   ├─ Favorites
   └─ All Media
```

---

## 7. MVP Scope

### Phase 1 (MVP)
- [ ] Ideas feed with daily batch scan + algorithm (hot/trending/cooling/cold)
- [ ] Manual "Scan Now" button
- [ ] Saved Ideas section
- [ ] 30-day auto-delete for unused ideas
- [ ] Personalize screen (example posts, sliders, custom instructions)
- [ ] Single post generation (LinkedIn only)
- [ ] Text editing + AI rewrite
- [ ] Drafts section
- [ ] Published section (manual mark as published)
- [ ] Copy to clipboard
- [ ] Monitor screen UI (empty state until APIs connected)

### Phase 2
- [ ] Auto-discovery from X, LinkedIn, Google Trends
- [ ] X/Twitter post support
- [ ] Image generation (simplified flow)
- [ ] LinkedIn/X API integration for auto-publish
- [ ] Monitor analytics (auto-pull engagement)

### Phase 3
- [ ] Carousel/thread support
- [ ] Monitor insights & recommendations engine
- [ ] Multiple writing style profiles (ghostwriting)
- [ ] Scheduling/queue system

---

## Decisions Made

| Question | Decision |
|----------|----------|
| Discovery frequency | Daily batch + manual "Scan Now" button |
| Discovery sources | UI for all 3 (LinkedIn, X, Google Trends) - backend connected later |
| Source algorithms | Per-source scoring + cross-source aggregation with multipliers |
| Ideas algorithm | Score-based sorting: Hot → Trending → Cooling → Cold |
| Ideas expiration | 30 days auto-delete if not used/saved |
| Saved Ideas | Separate section, exempt from expiration |
| Personalize onboarding | Not required, but suggested (prompt on first post creation) |
| Writing style | 1 profile per user, Personalize screen for continuous refinement |
| Image generation | Separate lightweight UX (not reusing Ad Creator) |
| Publishing flow | Manual "Mark Published" → Published archive → Monitor |
| Monitor data | No manual entry - API-ready UI, empty state until connected |
| Platform posting | Copy-only MVP, auto-publish in Phase 2 |

---

## Open Questions (Remaining)

None - all major decisions resolved. Ready for design/implementation.
