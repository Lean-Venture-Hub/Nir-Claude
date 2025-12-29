# Ad Analysis Parameters - Quick Reference

## TL;DR

This document defines the 11 strategic parameters extracted from every ad in ScaleFox's competitive intelligence library. These parameters enable sophisticated filtering, pattern recognition, and remix capabilities. Use this as a reference when analyzing ads or building search queries across the ad library.

**Core Use Cases:**
- Filter ads by creative approach (e.g., "show me Enemy-Focused ads using PAS framework")
- Identify winning patterns (e.g., "which Hook Shapes work best at Top funnel?")
- Find remix candidates (e.g., "contrarian techniques + Minimalist + Provocative Question")
- Learn from competitors (e.g., "how do they tap Fear emotion in Product Demo archetypes?")

---

## Quick Reference: All Parameters & Tags (JSON)

```json
{
  "parameters": {
    "creative_angle": {
      "type": "multi-select",
      "tags": ["Analogy Ads", "Typographic Treatment", "Understatement", "Cliché + Twist", "Visual Metaphor", "Contrast/Before-After", "Enemy-Focused", "Insider Reference", "Hybrid", "None of the above"]
    },
    "contrarian_techniques": {
      "type": "multi-select",
      "tags": ["Analogical Transfer", "Temporal Inversion", "Enemy Creation", "Silence Breaking", "Scale Manipulation", "Role Reversal", "Benefit Negation", "Cost Reframe", "Invisible Made Visible", "Contradiction Resolution", "None (Proven Pattern)"]
    },
    "human_truth_core_emotion": {
      "type": "multi-select",
      "tags": ["Relief", "Fear", "Control", "Status Anxiety", "Calm", "Confidence", "Frustration", "Overwhelm", "Time Scarcity", "Identity/Belonging", "Validation", "Hope", "Pride", "Shame Avoidance", "Other"]
    },
    "copy_framework": {
      "type": "multi-select",
      "tags": ["AIDA (Attention-Interest-Desire-Action)", "PAS (Pain-Agitate-Solution)", "JTBD (Jobs-To-Be-Done)", "Golden Circle (Why-How-What)", "Before-After-Bridge", "Problem-Promise-Proof-Proposal", "Feature-Advantage-Benefit (FAB)", "Anti-Pattern → Philosophy → Proof", "Hook-Story-Offer", "Question-Answer-CTA", "Stat-Insight-Action", "None/Unclear"]
    },
    "rhetorical_devices": {
      "type": "multi-select",
      "tags": ["Paradox", "Chiasmus", "Asyndeton", "Alliteration", "Antithesis", "Metaphor", "Personification", "Hyperbole", "Understatement", "Rhetorical Question", "Repetition", "Specific Numbers", "Contrast", "Anaphora", "None detected"]
    },
    "big_idea_category": {
      "type": "single-select",
      "tags": ["Time Theft/Recovery", "Invisible Problem Made Visible", "Anti-Category Stance", "Role Reversal", "Hidden Cost Exposure", "Status Quo as Enemy", "Scale Dramatization", "Transformation Promise", "Identity/Tribe Creation", "Simplification/Reduction", "Capability Unlock", "Risk Mitigation", "Other"]
    },
    "the_enemy": {
      "type": "multi-select",
      "tags": ["Meetings", "Status Quo", "Complexity", "Tool Sprawl", "Data Overload", "Manual Process", "Competitor Category", "Industry Practice", "Time Waste", "Burnout", "Inefficiency", "Lack of Control", "Uncertainty", "Other"]
    },
    "emotional_win": {
      "type": "multi-select",
      "tags": ["Time Reclaimed", "Control Restored", "Clarity Achieved", "Status Elevated", "Confidence Gained", "Relief from Burden", "Simplicity", "Peace of Mind", "Capability Unlocked", "Recognition/Validation", "Belonging", "Pride", "Other"]
    },
    "hook_shape": {
      "type": "multi-select",
      "tags": ["Contradiction", "Unspoken Truth", "Pattern Break", "Reframe", "Personal Stake", "Odd Observation", "Economic Shift", "False Consensus", "Provocative Question", "None/Generic"]
    },
    "ad_archetype": {
      "type": "single-select",
      "tags": ["Testimonial", "Thought Leadership", "Product Demo", "Data-Backed Insight", "Limited-Time Offer", "Case Study / Success Story", "Event Invitation", "Lead Magnet", "Competitive Comparison", "Founder Story", "Trend-Jacking", "Employee Spotlight", "Checklist / How-To", "Poll / Survey", "Pain-Point → Solution", "Before/After", "Press", "Prompt Demo", "Point Out", "Other"]
    },
    "ad_style": {
      "type": "multi-select",
      "tags": ["Bold Colors", "Minimalist", "Authentic UGC", "Illustration-Led", "Cinematic", "Infographic", "Glassmorphism", "3D / CGI", "Gradient Overlay", "Duotone", "Dark Mode", "Retro / Vintage", "Motion Graphics", "Isometric", "Hand-Drawn Sketch", "Other"]
    }
  },
  "summary": {
    "total_parameters": 11,
    "multi_select_parameters": 8,
    "single_select_parameters": 3,
    "total_unique_tags": 151
  }
}
```

---

## The 11 Strategic Parameters

### 1. Creative Angle (Multi-select)

**What it is:** The primary creative technique used to convey the message visually or conceptually.

**Why it matters:** Different angles resonate with different audiences and funnel stages. Knowing which angles competitors use helps identify oversaturated patterns and white-space opportunities.

**Tags:**
- `Analogy Ads` - Product benefit mapped to natural equivalent (e.g., owl = 360° vision)
- `Typographic Treatment` - Typography as primary visual element (e.g., CLOUD with cloud replacing O)
- `Understatement` - Deliberate restraint, anti-hyperbole ("Won't change your life. But Tuesdays will be better.")
- `Cliché + Twist` - Common saying with unexpected reversal ("Time is money, but meetings are bankrupting you")
- `Visual Metaphor` - Invisible concept made tangible through imagery (algorithm as physical machine)
- `Contrast/Before-After` - Dramatizes transformation or difference
- `Enemy-Focused` - Ad centers on defeating a villain/problem, not promoting product
- `Insider Reference` - Uses domain-specific knowledge for "they get me" effect
- `Hybrid` - Combines 2+ angles
- `None of the above` - Doesn't fit established patterns

**Typical usage:** Most ads use 1-2 angles. Select ALL that apply.

---

### 2. Contrarian Techniques (Multi-select)

**What it is:** Advanced techniques that challenge conventions or invert expectations (typically used in "brave angle" concepts).

**Why it matters:** Brave angles stand out in crowded feeds and create tribal identity. Tracking which contrarian techniques competitors avoid reveals positioning opportunities.

**Tags:**
- `Analogical Transfer` - Problem mapped to unexpected domain (B2B sales → Dating dynamics)
- `Temporal Inversion` - Shows past debt, not future gain (what's already lost)
- `Enemy Creation` - "Anti-X" positioning, tribal identity through rejection
- `Silence Breaking` - States unspoken industry truth with deadpan delivery
- `Scale Manipulation` - Zooms to micro-moment ("6-second detail killer") or macro-view ("Every company by 2027")
- `Role Reversal` - Flips perspective ("Your customers are managing YOU")
- `Benefit Negation` - Leads with what product *doesn't* do ("No dashboards. Zero meetings.")
- `Cost Reframe` - Shows time/dignity/opportunity cost, not just money
- `Invisible Made Visible` - Exposes hidden mechanism as physical thing
- `Contradiction Resolution` - Visual paradox that resolves meaningfully ("Growing slower scales faster")
- `None (Proven Pattern)` - Ad uses established patterns, not contrarian approach

**Typical usage:** Proven Pattern ads = "None". Brave Angles use 1-2 techniques. Select ALL that apply.

---

### 3. Human Truth / Core Emotion (Multi-select)

**What it is:** The primary human emotion or psychological truth the ad taps into.

**Why it matters:** B2B buyers are humans first. Ads that connect emotionally outperform feature-focused ads. This parameter reveals which emotions competitors leverage (and which they ignore).

**Tags:**
- `Relief` - Burden lifted, pressure released
- `Fear` - Risk, loss aversion, threat
- `Control` - Agency, empowerment, mastery
- `Status Anxiety` - Professional standing, peer perception
- `Calm` - Peace of mind, stress reduction
- `Confidence` - Self-assurance, capability
- `Frustration` - Active pain point, current struggle
- `Overwhelm` - Cognitive overload, too much complexity
- `Time Scarcity` - Not enough hours, stolen time
- `Identity/Belonging` - Tribe membership, "people like us"
- `Validation` - Recognition, being seen/heard
- `Hope` - Positive future state, aspiration
- `Pride` - Achievement, accomplishment
- `Shame Avoidance` - Preventing embarrassment or failure
- `Other` - Specify if different emotion is primary

**Typical usage:** Select 1-3 primary emotions. Focus on what the audience *feels*, not what the product does.

---

### 4. Copy Framework (Multi-select)

**What it is:** The persuasion structure used in the messaging (how the copy is organized to lead to action).

**Why it matters:** Different frameworks work better at different funnel stages. Tracking framework usage reveals what persuasion logic competitors rely on.

**Tags:**
- `AIDA (Attention-Interest-Desire-Action)` - Classic funnel structure
- `PAS (Pain-Agitate-Solution)` - Problem → make it worse → resolve
- `JTBD (Jobs-To-Be-Done)` - Focuses on functional job to accomplish
- `Golden Circle (Why-How-What)` - Starts with purpose/belief
- `Before-After-Bridge` - Current state → desired state → how to get there
- `Problem-Promise-Proof-Proposal` - 4P structure with evidence
- `Feature-Advantage-Benefit (FAB)` - What it is → why it matters → what you gain
- `Anti-Pattern → Philosophy → Proof` - Contrarian framework
- `Hook-Story-Offer` - Narrative-driven structure
- `Question-Answer-CTA` - Rhetorical question resolved by product
- `Stat-Insight-Action` - Data-driven persuasion
- `None/Unclear` - No clear framework detected

**Typical usage:** Ads may layer multiple frameworks. Select ALL present.

---

### 5. Rhetorical Devices (Multi-select)

**What it is:** Literary/linguistic techniques used to enhance persuasion and memorability.

**Why it matters:** Strong copy uses 2-4 rhetorical devices. This parameter helps identify what makes certain copy stick.

**Tags:**
- `Paradox` - Contradictory statement that reveals truth
- `Chiasmus` - Reversed parallel structure ("work to live, not live to work")
- `Asyndeton` - Deliberate omission of conjunctions for impact
- `Alliteration` - Repeated consonant sounds
- `Antithesis` - Contrasting ideas in parallel structure
- `Metaphor` - Direct comparison without "like" or "as"
- `Personification` - Human traits given to non-human things
- `Hyperbole` - Exaggeration for emphasis
- `Understatement` - Deliberate downplaying for effect
- `Rhetorical Question` - Question with implied answer
- `Repetition` - Strategic word/phrase repetition
- `Specific Numbers` - Concrete data points (not rounded)
- `Contrast` - Juxtaposition of opposites
- `Anaphora` - Repetition at start of successive clauses
- `None detected` - No clear rhetorical devices

**Typical usage:** Strong ads use 2-4 devices. Select ALL that apply.

---

### 6. Big Idea Category (Single-select)

**What it is:** The overarching conceptual territory the ad occupies.

**Why it matters:** Reveals high-level positioning strategy. If competitors cluster around 2-3 Big Ideas, other categories represent white space.

**Tags:**
- `Time Theft/Recovery` - Focus on hours lost or reclaimed
- `Invisible Problem Made Visible` - Shows hidden costs/issues
- `Anti-Category Stance` - Rejects industry norms
- `Role Reversal` - Flips expected relationship
- `Hidden Cost Exposure` - Reveals non-obvious expenses
- `Status Quo as Enemy` - Current way is the villain
- `Scale Dramatization` - Magnifies impact (micro or macro)
- `Transformation Promise` - Before/after change
- `Identity/Tribe Creation` - "People like us" positioning
- `Simplification/Reduction` - Less is more, minimalism
- `Capability Unlock` - Enables new possibilities
- `Risk Mitigation` - Safety, security, protection
- `Other` - Specify if different category

**Typical usage:** Select ONE primary category that best captures the core idea.

---

### 7. The Enemy (Multi-select)

**What it is:** What the ad positions against (the problem, villain, or status quo being fought).

**Why it matters:** Defining a clear enemy creates urgency and tribal identity. This parameter reveals which enemies competitors rally against (and which are underused).

**Tags:**
- `Meetings` - Time wasted in unnecessary meetings
- `Status Quo` - "The way it's always been done"
- `Complexity` - Overcomplicated systems/processes
- `Tool Sprawl` - Too many disconnected tools
- `Data Overload` - Dashboard fatigue, metric paralysis
- `Manual Process` - Tedious, repetitive work
- `Competitor Category` - Entire competitive set
- `Industry Practice` - Broken standard approach
- `Time Waste` - General inefficiency
- `Burnout` - Unsustainable pace
- `Inefficiency` - Slow, bloated workflows
- `Lack of Control` - Feeling powerless
- `Uncertainty` - Not knowing what's working
- `Other` - Specify if different enemy

**Typical usage:** Some ads have multiple villains. Select ALL enemies present.

---

### 8. Emotional Win (Multi-select)

**What it is:** The emotional payoff the audience achieves by using the product (not features, but feelings).

**Why it matters:** The "after" state must be emotionally resonant, not just functionally better. This parameter connects product to felt outcomes.

**Tags:**
- `Time Reclaimed` - Hours returned, schedule freedom
- `Control Restored` - Agency, command over situation
- `Clarity Achieved` - Understanding, visibility, insight
- `Status Elevated` - Professional standing improved
- `Confidence Gained` - Self-assurance, reduced imposter syndrome
- `Relief from Burden` - Weight lifted, stress removed
- `Simplicity` - Cognitive ease, elegance
- `Peace of Mind` - Worry eliminated, safety
- `Capability Unlocked` - New skills/possibilities enabled
- `Recognition/Validation` - Being seen, acknowledged
- `Belonging` - Joining a tribe, "people like us"
- `Pride` - Accomplishment, achievement
- `Other` - Specify if different

**Typical usage:** Select 1-3 primary emotional wins. Focus on feelings, not functional outcomes.

---

### 9. Hook Shape (Multi-select)

**What it is:** The psychological trigger used to stop the scroll (based on ScaleFox Hook Toolkit).

**Why it matters:** Different hook shapes appeal to different psychological states. Effective hooks violate expectations or surface unspoken truths.

**Tags:**
- `Contradiction` - "Everyone's doing X; Y is actually happening"
- `Unspoken Truth` - Surfaces insider knowledge or taboo
- `Pattern Break` - "You were told X. Here's what's missing"
- `Reframe` - "X isn't about Y. It's about Z"
- `Personal Stake` - "I lost/made/learned X by doing Y"
- `Odd Observation` - "Noticed something weird about X…"
- `Economic Shift` - "X just changed; most people missed it"
- `False Consensus` - "90% think X. They're wrong"
- `Provocative Question` - Question that forces self-reflection
- `None/Generic` - Standard hook, no clear shape

**Typical usage:** Most ads use 1-2 shapes. Select ALL hook shapes present.

**Reference:** See `hook-toolkit.md` for detailed examples and usage guidance.

---

### 10. Ad Archetype (Single-select)

**What it is:** The structural format and primary purpose of the ad.

**Why it matters:** Different archetypes perform better at different funnel stages and with different audience maturity levels.

**Tags:**
- `Testimonial` - Customer endorsement, social proof
- `Thought Leadership` - Unique POV, authority building
- `Product Demo` - Feature/workflow in action
- `Data-Backed Insight` - Compelling stat or benchmark
- `Limited-Time Offer` - Urgency/scarcity driver
- `Case Study / Success Story` - Customer results narrative
- `Event Invitation` - Webinar, conference, session promo
- `Lead Magnet` - Gated asset offer (ebook, checklist)
- `Competitive Comparison` - Positioning against rivals
- `Founder Story` - Personal narrative from leadership
- `Trend-Jacking` - Aligns with hot news/industry trend
- `Employee Spotlight` - Staff culture, employer brand
- `Checklist / How-To` - Step-by-step tips
- `Poll / Survey` - Interactive question
- `Pain-Point → Solution` - Problem framing + resolution
- `Before/After` - Transformation demonstration
- `Press` - Credibility through media mentions
- `Prompt Demo` - Urges demo sign-up
- `Point Out` - Highlights specific USP
- `Other` - Specify if different

**Typical usage:** Select ONE primary archetype. Choose the best fit even if ad has secondary elements.

**Reference:** See `ad-archetype.csv` for full definitions, strengths, weaknesses, and funnel fit.

---

### 11. Ad Style (Multi-select)

**What it is:** The visual aesthetic and design approach.

**Why it matters:** Visual style signals brand positioning and affects scroll-stopping power. Different styles resonate with different ICPs and industries.

**Tags:**
- `Bold Colors` - Saturated, high-contrast palette
- `Minimalist` - Clean, whitespace-heavy, essentials only
- `Authentic UGC` - Raw, user-generated aesthetic
- `Illustration-Led` - Custom illustrations, vectors, icons
- `Cinematic` - High-def visuals, dramatic framing
- `Infographic` - Data visualized with charts/icons
- `Glassmorphism` - Frosted-glass blur layers
- `3D / CGI` - Photoreal or stylized 3D renders
- `Gradient Overlay` - Smooth multicolor blends
- `Duotone` - Two-color visual treatment
- `Dark Mode` - Light text on dark background
- `Retro / Vintage` - Nostalgic, past-decade aesthetic
- `Motion Graphics` - Animated typography/icons
- `Isometric` - 30° pseudo-3D technical view
- `Hand-Drawn Sketch` - Loose, personal illustration style
- `Other` - Specify if different

**Typical usage:** Ads may combine multiple visual approaches (e.g., "Minimalist + Bold Colors"). Select ALL styles present.

**Reference:** See `ad-styles.csv` for full definitions, compatible archetypes, and media formats.

---

## Usage Patterns & Best Practices

### Filtering Examples

**Find brave, contrarian ads:**
```
contrarian_techniques: ["Enemy Creation", "Silence Breaking"]
+ hook_shape: ["Contradiction", "Unspoken Truth"]
+ creative_angle: ["Enemy-Focused"]
```

**Find top-funnel awareness ads:**
```
funnel_stage: "Top"
+ hook_shape: ["Provocative Question", "Odd Observation"]
+ ad_archetype: ["Thought Leadership", "Data-Backed Insight"]
```

**Find remix candidates (high replaceability):**
```
creative_angle: ["Visual Metaphor", "Analogy Ads"]
+ ad_style: ["Minimalist", "Illustration-Led"]
+ (exclude ads with many Company_Specific elements)
```

**Find emotional, human-first ads:**
```
human_truth_core_emotion: ["Relief", "Control", "Time Scarcity"]
+ emotional_win: ["Time Reclaimed", "Peace of Mind"]
+ rhetorical_devices: ["Specific Numbers", "Contrast"]
```

---

### Cross-Parameter Insights

**Emotional Architecture Mapping:**
- Human Truth (what they feel) → The Enemy (what causes it) → Emotional Win (how product resolves it)
- Example: `Frustration` → `Meetings` → `Time Reclaimed`

**Creative-Framework Pairing:**
- Certain creative angles work better with specific frameworks
- Example: `Enemy-Focused` + `PAS` = powerful pain amplification
- Example: `Visual Metaphor` + `Before-After-Bridge` = transformation clarity

**Hook-Archetype Fit:**
- Different hook shapes suit different archetypes
- Example: `Personal Stake` works well in `Case Study / Success Story`
- Example: `Provocative Question` fits `Thought Leadership`

**Style-Creative Alignment:**
- Contrarian ads often use `Bold Colors` or `Authentic UGC` (disruptive, attention-grabbing)
- Traditional approaches often use `Minimalist` or `Infographic` (safe, clear)
- `Enemy-Focused` creative angle pairs well with strong visual contrast

---

## Parameter Hierarchy

**Strategic (Big Picture):**
1. Big Idea Category
2. Ad Archetype

**Emotional (Psychological):**
3. Human Truth / Core Emotion
4. The Enemy
5. Emotional Win

**Execution (Creative):**
6. Creative Angle
7. Contrarian Techniques
8. Hook Shape
9. Copy Framework
10. Rhetorical Devices
11. Ad Style

---

## Version History

**v1.0** - 2025-12-28
- Initial parameter set based on Brief Creator v2 framework
- Integrated ScaleFox Inner Frameworks (hook-toolkit, ad-archetype, ad-styles, copywriting-framework)
- 11 parameters: 8 multi-select, 3 single-select

---

## Related Files

- `hook-toolkit.md` - Detailed hook shape definitions and examples
- `ad-archetype.csv` - Full archetype definitions, funnel fit, compatible media
- `ad-styles.csv` - Visual style definitions, strengths, weaknesses
- `copywriting-framework.csv` - Copy framework testing themes
- `../Prompts/4d analyze image ad.md` - Full analysis prompt using these parameters
- `../Prompts/14c Brief Creator v2.md` - Strategic framework these parameters derive from
