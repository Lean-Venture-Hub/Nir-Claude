# Dental Clinic Instagram Content Strategy
## For AI-Powered SaaS: Auto-Generate + Publish Stories

**TL;DR:** 7 content categories, 3 stories/day, ~80% fully automated. The key to authenticity is a strong onboarding data model (colors, photos, tone, specialties) plus compliance-safe prompt guardrails. Local + seasonal hooks make it feel human.

---

## 1. Content Categories

| # | Category | Automation Level | Dentist Input Needed? | Why It Works |
|---|----------|-----------------|----------------------|--------------|
| 1 | Oral Health Tips | 100% Automated | No | Educational, shareable, evergreen |
| 2 | Smile Transformations / Before-After | 50% Automated | Yes – patient photos + consent | High engagement, trust-builder |
| 3 | Meet the Team | 30% Automated | Yes – staff photos/bios | Humanizes the clinic |
| 4 | Promotions & Offers | 80% Automated | Dentist confirms offers | Drives bookings |
| 5 | Seasonal / Holiday Content | 100% Automated | No | Timely, local feel |
| 6 | Fun Dental Facts | 100% Automated | No | Shareable, low-friction |
| 7 | Patient Milestones / Reviews | 70% Automated | Review text + name approval | Social proof |

---

### Category Examples (3 per category)

**1. Oral Health Tips**
- "Did you know you should replace your toothbrush every 3 months? Here's why..." [swipe-up to blog]
- "The right way to floss (most people skip this step)" [step-by-step template]
- "5 foods that secretly stain your teeth — and what to eat instead"

**2. Smile Transformations**
- Split-screen before/after with subtle branded frame + "Ask us about veneers"
- "6-month Invisalign journey at [Clinic Name]" – progress carousel
- Close-up post-whitening shot with text: "Same-day results at [location]"

**3. Meet the Team**
- Staff headshot with: Name, Role, Fun Fact ("Dr. Sarah loves hiking with her golden retriever")
- "A day in the life at [Clinic Name]" – candid BTS shot with text overlay
- Birthday shoutout: "Happy birthday to our amazing hygienist, Mike!"

**4. Promotions & Offers**
- "New patient special: Exam + X-rays for $99. Book this week only."
- "Refer a friend, get $50 off your next visit. Tag someone who needs a checkup!"
- "Back to school season — kids' cleanings now through September."

**5. Seasonal / Holiday**
- Halloween: "Trick or treat? Skip the candy, keep the smile."
- New Year: "New year, new smile goals. Book your January appointment."
- Valentine's Day: "Give the gift of a confident smile — ask about whitening."

**6. Fun Dental Facts**
- "Your tooth enamel is the hardest substance in your body — stronger than bone."
- "The average person spends 38 days brushing teeth over their lifetime."
- "Dentists were the first medical professionals to use anesthesia — in 1844!"

**7. Patient Milestones / Reviews**
- Star-rating graphic with pull quote from Google review + "Thank you, [First Name]!"
- "Another cavity-free checkup! Congrats to [first name only]" – polaroid template
- Screenshot-style review card: "5 stars — best dentist I've ever had. Painless and professional."

---

## 2. Image Strategy

### Source Hierarchy (in order of authenticity)

| Source | Use Case | Authenticity Score | Effort |
|--------|----------|-------------------|--------|
| Dentist-provided photos | Team, office, before/after | Very High | High (one-time onboarding) |
| AI-generated images | Tips, facts, seasonal | Medium | Low (fully automated) |
| Licensed stock (Unsplash/Pexels) | Lifestyle, smiles, props | Medium | Low |
| Branded text-only templates | Promotions, facts, reviews | High (if branded) | Very Low |

### What Works Specifically for Stories

- **Text-heavy slides** with brand colors perform as well as photos — less pressure to have original images
- **Bold sans-serif headline** + supporting text + logo in corner = professional and scannable
- **Gradient or solid color backgrounds** with the clinic's brand palette feel more "theirs" than stock
- Swipe-up / poll / quiz stickers dramatically increase engagement — build these into templates
- 9:16 ratio templates only — pre-sized for Stories, no cropping

### Making It Look Like THEIR Clinic

The personalization layer should include:
- Clinic's HEX brand colors (applied to all template backgrounds/accents)
- Logo (watermarked bottom-right on every slide)
- Clinic name auto-inserted into copy where relevant
- City/neighborhood name used in local hooks ("Smile bright in [Scottsdale]!")
- Photo of the actual waiting room or team on file → auto-pulled into "team" category posts

### Practical Tech Stack for Images

| Tool | Role |
|------|------|
| Canva API or HTML/CSS templates | Branded story generation at scale |
| OpenAI DALL-E 3 or Stability AI | AI-generated lifestyle/illustrative images |
| Unsplash API | Free stock fallback for props/backgrounds |
| Cloudinary | Asset management + per-clinic media library |
| Clinic's onboarding photo upload | Team photos, office, before/after vault |

**Recommendation:** Start with Canva-style HTML/CSS templates rendered server-side. Fast, cheap, fully brand-consistent. Add AI image generation in v2.

---

## 3. Personalization Model

### Onboarding Data to Collect (One-Time Setup)

| Field | Used For | Required? |
|-------|----------|-----------|
| Brand colors (primary + accent) | All templates | Yes |
| Logo file | Watermark on all posts | Yes |
| Clinic name + city | Copy injection | Yes |
| Services offered (checkboxes) | Content filtering | Yes |
| Tone (Warm/Friendly, Professional, Fun) | Prompt style | Yes |
| Dentist name(s) + headshots | Team posts | Yes |
| Staff names + roles + fun facts | Meet the team | Recommended |
| Before/after photos (with consent) | Transformation posts | Optional |
| Promotions / seasonal offers | Promo posts | Optional (recurring) |
| Google Business URL | Review pulls (API) | Recommended |
| Holidays to skip (e.g., religious) | Calendar filtering | Optional |

### Local + Seasonal Automation

- **City injection:** "The top 3 smile tips for [City] families this summer"
- **Seasonal calendar:** Pre-built content for 52 weeks — Halloween, back-to-school, summer, NYE — triggered by date
- **Local events hook:** If dentist provides a city, pull local school calendar or holiday dates for relevant posts
- **Weather-adjacent:** "Cold weather can increase tooth sensitivity — here's what to do" in winter months

### Tone Personalization via Prompts

Three prompt presets based on selected tone:
- **Warm/Friendly:** "Write like a trusted neighbor, not a corporation. Use 'we' and 'your family.'"
- **Professional:** "Clinical but approachable. Short sentences. No exclamation points in excess."
- **Fun/Playful:** "Light humor, emojis allowed, dentist puns OK. Aim for a smile, not just a click."

---

## 4. Content Calendar — Sample Week (21 Stories)

| Day | Story 1 (9am) | Story 2 (12pm) | Story 3 (6pm) | Photos Needed? |
|-----|--------------|----------------|---------------|----------------|
| Mon | Oral Health Tip | Fun Dental Fact | Promotion/Offer | No |
| Tue | Meet the Team | Seasonal Hook | Patient Review | Yes (staff headshot) |
| Wed | Oral Health Tip | Fun Dental Fact | Smile Transformation | Yes (before/after) |
| Thu | Promotion/Offer | Oral Health Tip | Meet the Team | Yes (staff headshot) |
| Fri | Fun Dental Fact | Seasonal Hook | Patient Review | No |
| Sat | Smile Transformation | Oral Health Tip | Fun Dental Fact | Yes (before/after) |
| Sun | Seasonal/Weekend Vibe | Patient Review | Promo Reminder | No |

**Breakdown of 21 stories:**
- Oral Health Tips: 5 (24%) — 100% automated
- Fun Dental Facts: 5 (24%) — 100% automated
- Promotions: 3 (14%) — 80% automated
- Patient Reviews: 3 (14%) — 70% automated
- Seasonal/Holiday: 2 (10%) — 100% automated
- Meet the Team: 2 (10%) — needs staff photos (one-time)
- Smile Transformations: 2 (10%) — needs patient photos + consent

**Fully automated (no dentist needed): ~14 of 21 stories (67%)**
**Needs pre-loaded assets (photos uploaded at onboarding): ~7 of 21 (33%)**

---

## 5. Quality Control + Compliance Guardrails

### Dental Compliance Rules (Baked Into Prompts)

| Rule | What to Block | Safe Alternative |
|------|--------------|-----------------|
| No diagnosis language | "You might have gum disease" | "Regular checkups catch issues early" |
| No treatment guarantees | "Whitening WILL remove stains" | "Many patients see results after one session" |
| No before/after exaggeration | "Dramatic results guaranteed" | "Results vary — see our patient gallery" |
| No pricing claims without caveat | "Cheapest dentist in [City]" | "Competitive pricing + flexible payment plans" |
| No claims about pain | "Completely painless, always" | "We prioritize your comfort" |
| HIPAA: no patient ID without consent | Never use full name in reviews | First name only, or "a patient shared..." |
| FTC: testimonial disclosure | Don't imply typical results | "Individual results may vary" in fine print |

### Prompt-Level Guardrails (System Prompt Additions)

```
NEVER make specific medical claims or diagnoses.
NEVER guarantee treatment outcomes.
ALWAYS use hedging language: "may," "can," "many patients," "in some cases."
NEVER use a patient's full name without explicit written consent on file.
ALWAYS include "Results may vary" near any before/after reference.
If unsure whether a claim is compliant, rewrite it as a general tip instead.
Keep all copy at a 6th-8th grade reading level.
```

### Content Review Flow

| Risk Level | Content Type | Review Required? |
|-----------|--------------|-----------------|
| Low | Tips, facts, seasonal | Auto-publish (no review) |
| Medium | Promotions, reviews | 24hr dentist preview window (approve/reject via SMS) |
| High | Before/after, medical claims | Manual approval required before publish |

**Recommended UX:** Dentist gets a daily SMS/email digest with next day's content. One-tap approve or edit. Default is auto-publish if no response in 12 hours (configurable).

### Anti-Generic-AI Signals to Avoid in Copy

- No "In today's fast-paced world..."
- No "As a dental professional, we understand..."
- No lists of 10 tips (max 3-5)
- No "It's important to note that..."
- No passive voice overuse
- Short sentences. Active voice. Contractions allowed ("you'll", "we're", "don't")
- Each post reads like a human wrote it at 7am, not a machine at midnight
