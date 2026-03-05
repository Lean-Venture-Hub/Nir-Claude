# Instagram Content System — UX Flows
TL;DR: Four designs for dentist-facing Instagram content approval. Recommended = Flow 4 (Hybrid). Daily WhatsApp for stories (15 sec), weekly web dashboard for feed posts (5 min).

---

## Shared System Logic

- AI generates content nightly based on: clinic specialty, tone profile, seasonal hooks, past performance
- Stories = 24hr ephemeral, 3/day, published at 8am / 12pm / 6pm
- Feed posts = permanent, 1/day, published at optimal time per account
- "Auto-approve" fallback: no reply within X hours = system publishes best-scored content
- First-time setup: dentist answers 5 questions to set tone (friendly/professional/educational)

---

## Flow 1: WhatsApp-Only Daily Stories

**Time commitment: ~15 seconds/morning**

### 7:45am — System sends morning bundle

```
Good morning Dr. Sarah! ☀️ Here are today's 3 Instagram stories:

Story 1 (8am) — Tip Tuesday
"Did you know? Flossing before brushing is 20% more effective 🦷"
[Preview image: clean infographic, blue/white]

Story 2 (12pm) — Behind the scenes
"Meet our hygienist Maya — 8 years keeping smiles bright ✨"
[Preview image: photo of Maya at desk, warm filter]

Story 3 (6pm) — Weekend reminder
"We're open Saturday 9am–2pm! DM us to book 📅"
[Preview image: clinic exterior, golden hour]

Reply with:
✅ 1 2 3 — approve all
🔢 Numbers to approve (e.g. "1 3" skips Story 2)
✏️ "edit 2" — to change Story 2
⏭️ "skip" — publish nothing today
```

### Response paths

**"✅" or "1 2 3"**
→ "Done! Stories scheduled for 8am, 12pm, 6pm. Have a great day! 🙌"

**"1 3" (partial)**
→ "Got it. Stories 1 and 3 scheduled. Story 2 skipped."

**"edit 2"**
→ "What would you like to change about Story 2? Reply with the new caption, or say 'photo' to pick a different image."
→ Dentist replies: "Change the name to Maria, not Maya"
→ "Updated! Story 2 now reads: 'Meet our hygienist Maria...' Approved?"
→ "yes" → scheduled

**"skip"**
→ "No stories today. See you tomorrow! ☀️"

**No reply by 9am**
→ System auto-publishes Story 1 only (safest: tips, no personal info)
→ Stories 2 and 3 held
→ 9:15am message: "Story 1 published automatically (no response received). Stories 2 and 3 held — reply '2 3' to approve or 'skip' to pass."

### Edge cases

| Situation | System behavior |
|-----------|----------------|
| Doctor on vacation | Pre-set "away mode" — system publishes 1 auto-approved tip/day |
| Story content feels wrong | "wrong" → flags to human reviewer, holds story |
| Wants to add own photo | "my photo" → system sends upload link |
| Repeated edits same element | Learns preference, stops suggesting that type |

---

## Flow 2: WhatsApp Weekly Batch (Sunday Review)

**Time commitment: ~5–8 minutes, once/week**

### Sunday 9am — Weekly bundle

```
Good morning Dr. Sarah! This week's Instagram plan is ready 📋

STORIES (21 total — 3/day Mon–Sun)
FEED POSTS (7 total — 1/day)

I'll send them in groups. Reply any time to approve, edit, or skip.

--- MONDAY ---

📱 Stories (Mon):
  M1: Motivation Monday quote — "Confidence starts with a smile"
  M2: Office tour — front desk area
  M3: New patient offer — "First cleaning + X-ray $99"

🖼️ Feed Post (Mon):
  Before/after composite (4 photos, no faces)
  Caption: "Small changes, big confidence..."

Reply: "M all" = approve all Monday content
Or: "M1 M3 Mf" = approve specific items
Or: "M edit M2" = edit Monday story 2

--- TUESDAY ---
[continues...]

When done, reply "done" for a summary.
```

### Approval shorthand

| Reply | Meaning |
|-------|---------|
| `all` | Approve everything for the week |
| `M all` | Approve all Monday content |
| `M1 M2 T1 Tf` | Approve specific items (T=Tuesday, f=feed) |
| `edit Wf` | Edit Wednesday's feed post |
| `skip Thu` | No content Thursday |
| `done` | Wrap up, show summary |

### End of session summary

```
Week locked! Here's your schedule:

Mon: 3 stories + feed post ✅
Tue: 3 stories + feed post ✅
Wed: 2 stories (skipped W2) + feed post ✅
Thu: Nothing scheduled ⏭️
Fri: 3 stories + feed post ✅
Sat: 2 stories ✅
Sun: 1 story (tip only) ✅

Total: 17 stories, 5 feed posts
Estimated reach: ~2,400 accounts

Have a great week! 💪
```

### Edge cases

| Situation | System behavior |
|-----------|----------------|
| No reply Sunday | Reminder Monday 8am: "Your week isn't approved yet — reply 'all' to auto-publish best content, or 'review' to see it." |
| Approves "all" without reviewing | System flags: "Just confirming — this approves 28 pieces of content unseen. Proceed?" |
| Wants to add a specific date (promo) | "add promo Friday: 20% off whitening" → inserts into Friday slots |
| Mid-week change | "cancel Thursday post" → cancels, offers replacement |

---

## Flow 3: Web Dashboard Weekly Review

**Time commitment: ~5 minutes/week**

### Sunday 9am — WhatsApp trigger message

```
Dr. Sarah, your weekly Instagram content is ready for review 📅

👉 Review this week: [link]
(opens your content calendar — works on phone or desktop)

Or reply "all" to approve everything without reviewing.

Link expires Monday 11:59pm.
```

### Web experience (what they see on phone)

**Landing screen:**
- Clinic name + week dates in header
- "Approve All" button — prominent, top right
- Grid calendar: Mon–Sun columns, Stories row + Feed row
- Each cell = thumbnail + caption preview

**Interaction per post:**
- Tap cell → expand to full preview (image + caption + hashtags)
- Bottom sheet with 3 buttons: [Approve] [Edit] [Skip]
- Edit → inline text field for caption, tap "Swap Image" to browse AI alternatives (3 shown)
- Approve → green checkmark overlays cell, returns to grid

**Approve All flow:**
- Tap "Approve All" → confirmation sheet slides up: "Approving 28 pieces of content for [week dates]. This will auto-publish on schedule."
- [Confirm] [Review First]
- Confirm → all cells go green, "Week locked!" toast, WhatsApp confirmation sent

**Drag/Drop rescheduling (desktop):**
- Drag any post to a different day/slot
- System warns if moving a time-sensitive post (e.g. Saturday promo dragged to Tuesday)
- "Save Schedule" button locks changes

### Edge cases

| Situation | System behavior |
|-----------|----------------|
| Link opened on old phone/slow connection | Fallback: sends WhatsApp text version of Flow 2 |
| Dentist edits caption to something off-brand | AI flags with yellow warning: "This caption differs from your usual tone — looks good?" |
| Partially reviewed (exits before done) | Progress saved. WhatsApp: "You reviewed 14/28 posts. Tap to continue: [link]" |
| Forgets to approve by Monday | Auto-publishes AI top-pick for each slot, sends summary |

---

## Flow 4: Hybrid (Recommended)

**Time commitment: 15 sec/day (stories) + 5 min/week (feed posts)**

### Logic split

| Content type | Channel | Frequency | Time |
|-------------|---------|-----------|------|
| Daily stories (3/day) | WhatsApp | Every morning | ~15 sec |
| Feed posts (1/day) | Web dashboard | Sunday only | ~5 min |
| Urgent/timely posts | WhatsApp | As needed | ~30 sec |
| Analytics digest | WhatsApp | Monthly | Read-only |

### Daily story flow (weekday mornings, 7:45am)

Identical to Flow 1 — brief, 3-story bundle, approve with 1 reply.

Auto-approve safety valve: if no reply by 9am, best-scored story 1 publishes automatically. Doctor gets notified.

### Sunday web session (feed posts only)

```
Dr. Sarah — your feed posts for next week are ready 📸

7 posts planned. Takes about 5 minutes to review.

👉 Review feed posts: [link]

Or reply "auto" to let AI pick the best version of each.
```

Web dashboard shows feed posts only (not stories) — cleaner, less overwhelming. Stories column hidden unless "Show All" tapped.

### How the two channels connect

**Scenario A: Dentist edits a story that references a feed post**
→ WhatsApp edit updates the story
→ System checks: "Your story references Monday's feed post — want me to update that too?"
→ "yes" / "no"

**Scenario B: Dentist cancels a feed post on Sunday**
→ System auto-removes the story that teased that post
→ WhatsApp notification: "Removed Monday story 3 since it referenced the post you cancelled. I'll replace it with a tip."

**Scenario C: Dentist adds an urgent post (patient event, promo)**
→ WhatsApp: "promo: free whitening this Friday only"
→ System: "Got it! I'll create an urgent story + feed post for Friday. Want to see a preview before I schedule?"
→ Preview sent in WhatsApp as image + caption
→ "looks good" → published

**Scenario D: Doctor on vacation week**
→ Set once: "away next week"
→ System switches to auto-publish mode: 1 educational tip/day, no personal content, no promotions
→ No WhatsApp messages sent that week

### Weekly rhythm at a glance

```
SUN 9am   — 5 min web review (feed posts)
MON–SAT   — 15 sec WhatsApp (stories, each morning)
MON–SAT   — AI publishes on schedule, no action needed
MONTHLY   — WhatsApp digest: top posts, follower growth, best performing content
```

---

## System-Wide Rules (UX Principles)

1. **Never surprise the dentist.** Every auto-publish sends a notification after, not before.
2. **Default to safe content.** Auto-approve only runs on educational/tip content, never personal staff photos or promotions.
3. **One reply to approve.** No multi-step confirmation for simple approvals.
4. **Remember preferences.** If dentist skips behind-the-scenes content 3x, stop suggesting it.
5. **Exit always available.** "pause" at any time stops all content. "resume" restarts.
6. **No jargon.** Messages written at 8th grade reading level. No "engagement metrics" or "CTR."

---

## First-Time Onboarding (WhatsApp)

```
Hi Dr. Sarah! I'll be managing your Instagram content from now on.

Quick setup — 3 questions:

1. How would you describe your clinic's vibe?
   A) Friendly & warm  B) Professional & clinical  C) Fun & approachable

2. What do you want patients to feel when they see your posts?
   A) Reassured (we're trustworthy)  B) Educated (learn something)  C) Excited (special offers)

3. Do you want to show staff faces in content?
   A) Yes — we love it  B) Only with their permission each time  C) No — keep it anonymous

That's it! Your first content batch will be ready Sunday morning.
```

Setup takes 2 minutes. AI builds tone profile. No further config needed unless dentist wants to change it.
