# Instagram API Publishing - Deep Brief
**Research date:** 2026-02-28 | **Target use case:** Automated publishing for dental small businesses

## TL;DR

The Instagram Graph API (now also called Meta Graph API) supports automated publishing of feed posts, carousels, Reels, and Stories TODAY - no scheduling required. You need an Instagram Business account linked to a Facebook Page (or use the newer Instagram Business Login from July 2024 which removes Facebook dependency). The daily cap is 25 posts per account. Stories publishing via API IS supported as of 2023. For a dental SaaS product, the best path is using a third-party social API like Ayrshare rather than building directly on Meta's API.

---

## Key Findings

### 1. Stories - Can You Publish Programmatically?

**YES - as of 2023, Stories ARE supported via the Content Publishing API.**

- Endpoint: `POST /{ig-user-id}/media` with `media_type=STORIES`
- Supported: image stories, video stories
- NOT supported: filters, stickers, GIF overlays, mentions/tags via Stories, shopping tags in Stories, branded content tags
- Stories cannot be scheduled (publish immediately only, unlike feed posts which support `scheduled_publish_time`)
- Stories are ephemeral - they disappear after 24h as normal

Conflicting older docs still circulate saying Stories are not supported - these are outdated. Meta added Stories support in 2023.

### 2. Feed Posts, Carousels, Reels

All supported via the 2-step "container + publish" flow:

| Content Type | Supported | Notes |
|---|---|---|
| Single image feed | Yes | JPEG only |
| Single video feed | Yes | MP4, up to 100MB |
| Carousel (images) | Yes | 2-10 items |
| Carousel (video) | Yes | Max 60 sec per video clip |
| Reels | Yes | Since mid-2022, up to 90 sec (some accounts 60 sec cap) |
| Stories (image/video) | Yes | Since 2023 |
| Live | No | Not API-supported |
| Multi-image (blend) | No | Not supported |

**Publishing flow:**
1. `POST /{ig-user-id}/media` - create container (returns container ID)
2. Poll `GET /{container-id}?fields=status_code` until `FINISHED`
3. `POST /{ig-user-id}/media_publish` - publish the container

### 3. Authentication & Permissions

**Account requirements:**
- Instagram Business or Creator account (NOT personal)
- Must be connected to a Facebook Page (old flow) OR use new Instagram Business Login (new flow, July 2024)

**Two auth paths available:**

**Path A - Facebook Login (traditional):**
- User must have Facebook account + Page linked to Instagram
- OAuth scopes needed: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`, `pages_show_list`
- More friction for onboarding

**Path B - Instagram Business Login (new, July 2024):**
- No Facebook account required
- Direct Instagram login for Business/Creator accounts
- Simpler onboarding - major UX improvement
- Still does NOT support personal Instagram accounts

**App review required:** Meta requires app review before going live with real user accounts. Test with sandbox accounts during development.

### 4. Rate Limits

| Limit Type | Value |
|---|---|
| Posts per 24h per account | 25 (combined: feed + Reels + Stories) |
| API calls per hour | 200 per account |
| Carousel items max | 10 |
| Video size (Reels) | 100MB max |
| Video length (Reels) | 90 sec max (60 sec on some accounts) |
| Carousel video length | 60 sec max per clip |
| Image format | JPEG only |

Note: Some sources cite 100 API-published posts per 24h - the 25 limit appears to be the standard enforced cap. Verify current limits in Meta docs as this has fluctuated.

### 5. Third-Party APIs (Recommended for SaaS Products)

Building directly on Meta's API is viable but has app review friction and ongoing maintenance overhead. For a dental SaaS serving multiple clients, a wrapper API is strongly recommended.

| Service | Dev API? | Instagram Stories? | Price | Notes |
|---|---|---|---|---|
| **Ayrshare** | Yes - full REST API | Yes | Free (20 posts/mo), $49/mo Starter, $99/mo Premium, $499+/mo Business | Best-in-class developer API, SDKs for multiple languages, handles carousels/video optimization |
| **Late (getlate.dev)** | Yes | Unknown | Competitive to Ayrshare | Dev-focused, 99.97% uptime SLA, sub-50ms |
| **Upload-Post** | Yes | Yes | Free tier available | n8n + Make.com integrations pre-built |
| **Buffer** | Limited | Unknown | $6/profile/mo | No new developer accounts since 2019 |
| **Hootsuite** | Outdated API | No (API doesn't support) | $199+/mo | API not updated in 5+ years, skip |
| **Later** | No public API | Yes (app) | $18+/mo | No developer API, not suitable |
| **Make.com / Zapier** | No-code | Via Instagram direct | Per-operation pricing | Good for MVP/prototyping, not scalable SaaS |

**Recommendation for dental SaaS:** Start with Ayrshare. It abstracts away Meta's complexity, handles app review requirements on their end, and has a free tier to prototype.

### 6. Content Type Specs

**Images:**
- Format: JPEG only (no PNG, no WebP)
- Aspect ratio: 4:5 (portrait) to 1.91:1 (landscape) for feed; 9:16 for Stories
- Min width: 320px; Max width: 1440px

**Videos (Reels):**
- Format: MP4 (H.264 codec recommended)
- Max size: 100MB
- Max length: 90 seconds (some accounts limited to 60s)
- Aspect ratio: 9:16 recommended
- Must be publicly accessible URL at time of upload (not local file)

**Carousels:**
- 2-10 items (images or video)
- Mixed media (image + video) supported
- Videos max 60 sec each
- Reels cannot be included in carousels

**Important:** Media must be hosted at a publicly accessible URL - you upload to your own CDN/storage first, then pass the URL to the API.

### 7. Recent Changes & Deprecations (2024-2025)

| Change | Date | Impact |
|---|---|---|
| Instagram Basic Display API - END OF LIFE | Dec 4, 2024 | Personal accounts no longer API-accessible at all |
| Instagram Business Login (no Facebook required) | July 23, 2024 | Simplifies onboarding significantly |
| Insights metrics deprecated (video_views, email_contacts, profile_views, etc.) | Jan 8, 2025 (v21+) | Analytics only, no publishing impact |
| Graph API v22 - Views metric replaces legacy IG Media metrics | 2025 | Analytics impact |
| Graph API v25 released | ~Feb 2025 | Current version |
| Post/Page Reach, Video Impressions, Story Impressions metrics deprecation | June 2026 (upcoming) | Analytics impact |
| Creator accounts added to publishing API | 2022-2023 | Now both Business AND Creator can publish |

**Key deprecation risk:** The Insights API (analytics) is in flux. Publishing API itself is stable.

---

## Contradictions Found

1. **Stories support**: Multiple old sources say "Stories not supported" - this is WRONG as of 2023. Stories ARE supported via `media_type=STORIES`. Verify with current Meta docs.
2. **Daily post limit**: Sources cite both 25 and 100 posts/24h. The 25 limit appears to be the more commonly enforced one for most apps - test your specific app tier.
3. **Creator accounts**: Some sources say "Business only" but Meta added Creator account support. Both now work.
4. **Facebook requirement**: Pre-July 2024 all sources required Facebook Page linkage. New Instagram Business Login flow removes this for apps using the new auth.

---

## Quotes

> "Apps can create media containers for images, videos, or carousels and then publish them to the Instagram Feed via API calls. Since mid-2022, you can publish Instagram Reels videos through the API, and as of 2023, you can schedule and post Instagram Stories via the Content Publishing API."

> "Meta launched a new Instagram API with Instagram Business Login on July 23, 2024, which simplifies onboarding by removing the need for Facebook login."

> "On December 4, 2024, the Instagram Basic Display API reached end-of-life and no longer functions. Personal Instagram accounts are no longer supported via third-party APIs."

> "Ayrshare stands out with its developer-friendly approach with multiple SDKs available for popular programming languages and detailed code examples, and the platform handles complex scenarios like Instagram carousel posts and video optimization across different platforms."

---

## Synthesis: What to Build for Dental SaaS

**Recommended architecture:**

1. **Auth:** Use Instagram Business Login (July 2024 flow) - no Facebook required, simpler for dentist clients
2. **Publishing layer:** Use Ayrshare API rather than direct Meta API - saves months of app review + maintenance
3. **Content pipeline:** Generate JPEG images (not PNG) and MP4 videos, host on S3/CDN, pass URLs to Ayrshare
4. **Post types to support:** Single image (easiest), carousel (best engagement), Stories (daily touch)
5. **Rate limit budget:** 25 posts/day per clinic account is plenty (target 1-3/day)

**What's NOT possible via API:**
- Posting to personal Instagram accounts (must be Business or Creator)
- Adding interactive Story stickers, polls, links via API
- Instagram Live
- DM outreach (separate API, different rules)

**Biggest risk:** Meta's app review process. If you're building a multi-tenant SaaS (one app, many dentist accounts), you need Meta's "Advanced Access" approval. Budget 4-8 weeks for this. Ayrshare bypasses this entirely since they already have Meta approval.

---

## Full Source List

- [getlate.dev - API to Post to Instagram 2026 (Tutorial)](https://getlate.dev/blog/api-to-post-to-instagram)
- [Elfsight - Instagram Graph API Complete Developer Guide 2026](https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2026/)
- [Elfsight - Instagram API Changes 2025](https://elfsight.com/blog/instagram-graph-api-changes/)
- [Ayrshare - Instagram Stories API: How to Post a Story](https://www.ayrshare.com/instagram-stories-api-how-to-post-a-story/)
- [Ayrshare - Best Social Media Posting and Scheduling APIs 2024](https://www.ayrshare.com/best-social-media-posting-and-scheduling-apis/)
- [Ayrshare Pricing](https://www.ayrshare.com/pricing/)
- [Phyllo - How to Use Instagram API to Post Photos](https://www.getphyllo.com/post/how-to-use-instagram-api-to-post-photos-on-instagram)
- [Phyllo - Instagram Graph API Use Cases 2025](https://www.getphyllo.com/post/instagram-graph-api-use-cases-in-2025-iv)
- [Phyllo - Complete Guide to Instagram Reels API](https://www.getphyllo.com/post/a-complete-guide-to-the-instagram-reels-api)
- [Swipe Insight - Meta Releases New Instagram API with Instagram Login](https://web.swipeinsight.app/posts/new-instagram-api-with-instagram-login-9186)
- [n8n - Schedule & publish all Instagram content types workflow](https://n8n.io/workflows/4498-schedule-and-publish-all-instagram-content-types-with-facebook-graph-api/)
- [n8n - Automate Instagram Stories from Google Sheets workflow](https://n8n.io/workflows/8785-automate-instagram-stories-publishing-from-google-sheets-with-meta-graph-api/)
- [GitHub Gist - Instagram Platform API (Direct Login) Implementation Guide July 2024](https://gist.github.com/PrenSJ2/0213e60e834e66b7e09f7f93999163fc)
- [Medium - Instagram Graph API Overview, Content Publishing, Limitations](https://datkira.medium.com/instagram-graph-api-overview-content-publishing-limitations-and-references-to-do-quickly-99004f21be02)
- [Emplifi - Instagram Media Insights Metrics Deprecation Jan 2025](https://docs.emplifi.io/platform/latest/home/instagram-media-and-profile-insights-metrics-depre)
- [SociaVault - Instagram API Deprecated? 2026](https://sociavault.com/blog/instagram-api-deprecated-alternative-2026)
- [Data365 - Ayrshare Alternatives Social Media API Reviews](https://data365.co/blog/best-ayrshare-alternative)
- [outstand.so - 10 Best Unified Social Media APIs for Developers 2026](https://www.outstand.so/blog/best-unified-social-media-apis-for-devs)
- [CreatorFlow - Instagram API Rate Limits Explained](https://creatorflow.so/blog/instagram-api-rate-limits-explained/)
- [Tagembed - Instagram API Complete Guide for Businesses 2025](https://tagembed.com/blog/instagram-api/)
- [ContentStudio Help - Requirements for Direct Publishing to Instagram](https://docs.contentstudio.io/article/830-what-are-the-requirements-to-directly-publish-images-and-videos-to-instagram)
