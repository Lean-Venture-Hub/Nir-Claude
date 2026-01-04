# Review: 23 Create Image Variation - Improvement Suggestions

## Executive Summary

The 23 prompt has good structural foundation and clear mission, but suffers from repetitive content, brief examples, undefined quality terms, and context inefficiency (15KB). Needs consolidation, concrete examples, and quantified standards.

**Overall Score: 6.5/10**
- Structure: 7/10 ✅
- Clarity: 6/10 ⚠️
- Examples: 4/10 ❌ (Too brief, lack detail)
- Completeness: 8/10 ✅
- Actionability: 5/10 ⚠️
- Context Efficiency: 4/10 ❌ (Too much repetition, 15KB)

---

## Critical Issues

### 1. Examples Are Too Brief and Generic ❌

**Current State:**
Lines 354-392 have 3 "scenarios" that are just bullet lists:
```markdown
### Scenario 1: Conservative Variation
- DIFFERENT professional woman (new person, different appearance)
- DIFFERENT standing desk (new furniture, different style)
- Same composition structure, proportions, lighting mood
```

**Problems:**
- Doesn't show actual OUTPUT
- Doesn't demonstrate how to apply the framework
- Doesn't show what "entirely new visual elements" means in practice
- No visual descriptions - just abstract concepts

**Compare to 21c (good example):**
21c has 5 detailed examples with:
- UserInput (what user says)
- Brand Context (brand info)
- Edit Execution (detailed, quantitative instructions)
- Technical Specs
- Result description

**Impact:** AI models learn best from concrete examples. These are too abstract.

### Recommendation: Add 3-5 Detailed Examples

**Example structure needed:**

```markdown
## Example 1: Conservative Variation - Professional Context

**Original Ad Visual Description:**
- Person: Professional woman, 30s, business casual (white blouse), at standing desk
- Setting: Modern office, white walls, natural window light from left
- Product: Laptop showing dashboard UI
- Colors: Brand blue (#2563EB) in UI, whites, grays
- Layout: Person left third, screen right two-thirds, headline bottom
- Mood: Focused productivity, clean professional

**BriefJSON Context:**
- Campaign: Productivity software for remote workers
- Message: "Stay organized, work efficiently"
- Audience: Remote professionals, 25-40, tech-savvy
- Tone: Professional but approachable

**Your Variation (Conservative Approach):**

**NEW Visual Elements Generated:**
- Person: DIFFERENT woman (different ethnicity, early 40s, navy cardigan instead of white blouse, different hairstyle, different facial features)
- Desk: DIFFERENT standing desk (walnut wood vs. white, different monitor arm, different desk accessories)
- Office: DIFFERENT location (home office vs. corporate, different wall color - soft beige, different window placement - right side, plants instead of minimal)
- Laptop: DIFFERENT device (MacBook vs. Dell, different keyboard, different mouse)
- Lighting: Similar natural light but from opposite direction (right vs. left)

**Preserved Strategic Elements:**
- Same composition: Person left, screen right
- Same professional/modern vibe
- Same color scheme: Brand blue in UI, neutral workspace
- Same messaging focus: Organization and efficiency
- Same layout structure and proportions

**Text Variations:**
- Headline: "Work Smarter, From Anywhere" (alternative within brief framework)
- Body: "All your projects, one dashboard" (alternative benefit angle)
- CTA: "Start Free" (brief-aligned)

**Brand Consistency:**
- Logo: Brand logo (unchanged) - top right, same size
- Colors: Blue (#2563EB) in UI elements, maintained precisely
- Typography: Same font family, same hierarchy
- Quality: Professional photography aesthetic, high resolution

**Result:**
Structurally identical composition with entirely new people, furniture, location, and props. Same strategic message and professional tone. Different woman in different office with different equipment, but serving identical campaign goals.
```

**Add examples for:**
1. Conservative variation (as above)
2. Balanced variation (moderate changes)
3. Bold variation (dramatic creative shift)
4. Edge case: Original has people + product
5. Edge case: Abstract/illustration style original

---

### 2. Massive Repetition - Same Message 7+ Times ❌

**The Problem:**
The core message "create entirely new visual elements" appears in:

1. Line 30: Success Criteria
2. Lines 75-76: THE MANDATE section header
3. Lines 86-92: PROHIBITED list (what not to do)
4. Lines 94-100: REQUIRED list (what to do)
5. Lines 104-111: Visual Element Checklist
6. Lines 182-192: Hard Constraints #1
7. Lines 331-332: Negative List
8. Lines 397-398: Critical Reminder

**Impact:**
- Wastes ~40% of context window
- Makes prompt harder to scan
- Dilutes other important information
- 15KB total size (should be <10KB)

### Recommendation: Consolidate to ONE Section

**Consolidate into a single, powerful section:**

```markdown
## Visual Originality Requirement (CRITICAL)

**Core Principle:** Generate entirely new visual elements for every variation.

Think of this as a **new photoshoot** for the same campaign:
- Different models/actors
- Different location/set
- Different props/equipment
- Same strategic concept, completely fresh execution

**Prohibited:**
- Reusing same person/people from original
- Reusing same location/setting from original
- Reusing same furniture/objects from original

**Required:**
- Generate different people (similar demographic/age/vibe)
- Generate different settings (similar aesthetic/mood)
- Generate different objects (similar function/style)
- Preserve concept, emotion, and strategic message

**Pre-Generation Checklist:**
[ ] People: New individuals planned
[ ] Setting: New location planned
[ ] Objects: New props/furniture planned
[ ] Lighting: Similar mood, new environment
[ ] Composition: Similar structure, new elements

**Metaphor:** Same song, different recording session. Same strategic melody, completely different creative performance.
```

Then **delete** all other repetitions. Reference this section instead.

**Estimated savings:** Reduce from 15KB to ~10KB

---

### 3. Undefined Qualitative Terms ❌

**Vague terms used without definition:**
- "Scroll-stopping power" (lines 29, 314)
- "Professional" aesthetic (line 347)
- "Clean spacing" (line 28)
- "High contrast" (line 28)
- "Clear hierarchy" (line 214)

**Compare to 21c:**
21c now defines terms quantitatively:
- "Professional" = No artifacts, frame-accurate, ±1 frame sync, 1080p min, 8 Mbps
- "Smooth" = Minimum 12 frames, no jumps, 0.3s crossfades

### Recommendation: Add Quality Definitions Section

```markdown
## Quality Standards (Defined)

**Scroll-stopping power:**
- High contrast focal point (subject 40%+ lighter/darker than background)
- Human face or emotional expression in first visual scan (if people)
- Bold typography (headline ≥24px at 1080px canvas)
- Unexpected composition or color that breaks pattern

**Professional advertising quality:**
- Minimum resolution: 1080×1080 (square), 1920×1080 (landscape)
- No visible compression artifacts or pixelation
- Sharp focus on primary subject
- Proper lighting (no blown highlights, crushed shadows)
- Clean edges and professional retouching

**High contrast:**
- Text/background contrast ≥ 4.5:1 (WCAG AA standard)
- Primary subject contrast ≥ 3:1 vs. background
- Use overlays (8-15% opacity) if needed for readability

**Clean spacing:**
- Minimum 60px margins from all edges
- Breathing room: 20px minimum between distinct elements
- Text line-height: 1.3-1.5x font size
- CTA button padding: minimum 12px vertical, 20px horizontal

**Clear hierarchy:**
- Visual size order: Headline largest → Body medium → CTA prominent → Logo smallest
- Contrast priority: Headline highest contrast → CTA second → Body readable
- Reading flow: Top-to-bottom or Z-pattern (top-left → top-right → bottom-left → CTA)
```

---

### 4. Confusing Multi-Process Structure ⚠️

**Current State - THREE different processes:**
1. **Analysis Phase** (lines 36-67): 4 steps
2. **Implementation Steps** (lines 166-176): 9 steps
3. **Step-by-Step** (lines 277-290): 12 steps

**Problem:** Which one to follow? Overlapping guidance creates confusion.

### Recommendation: Consolidate to ONE Clear Process

```markdown
## Execution Process

### 1. Analyze Original Ad
- Extract core concept, visual strategy, layout structure
- Identify what makes it effective (preserve this)
- List all visual elements: people, settings, objects, lighting, composition

### 2. Parse Strategic Context
- Review briefJSON: campaign goals, messaging framework, audience
- Identify strategic boundaries (what must stay) vs. creative flexibility (what can vary)
- Determine variation approach: conservative/balanced/bold

### 3. Plan New Visual Elements
- Design entirely NEW people (similar vibe, different individuals)
- Design entirely NEW setting (similar mood, different location)
- Design entirely NEW objects (similar function, different style)
- Verify: Every element is newly generated

### 4. Generate Variation
- Create new imagery following plan
- Apply brand colors, typography, logo
- Explore messaging variations within brief framework
- Ensure quality standards met

### 5. Verify Quality
- Run Audit Checklist (all items pass)
- Confirm brief alignment maintained
- Validate brand consistency
```

**Delete the other two process sections** to eliminate confusion.

---

### 5. Variation Strategy Lacks Clear Decision Criteria ⚠️

**Current "When" statements are vague:**
- Conservative: "High-performing original, risk-averse brand, minimal creative exploration"
- Balanced: "Moderate creative exploration, A/B testing visual approaches, proven concept"
- Bold: "Maximum creative exploration, disruptive brand, testing new executions"

**Problem:** These don't help decide. When is a brand "risk-averse" vs. "moderate"?

### Recommendation: Add Decision Tree

```markdown
## Variation Approach Decision Tree

```
Start: What's the goal for this variation?

├─ Test minor messaging change only?
│  └─ Use CONSERVATIVE (minimal visual deviation)
│
├─ A/B test creative execution (different visual approach)?
│  └─ Use BALANCED (moderate exploration)
│
├─ Explore completely new creative direction?
│  └─ Use BOLD (maximum deviation)
│
└─ Not sure / general variation request?
   └─ Default to BALANCED

Additional factors to consider:
- Brand personality from Brand JSON:
  - Corporate/Professional → Lean conservative
  - Creative/Disruptive → Lean bold

- Campaign stage:
  - Early testing → Use balanced/bold for exploration
  - Proven winner → Use conservative for optimization

- Resource constraints:
  - Quick iteration → Conservative (faster)
  - Major refresh → Bold (more effort)
```
```

---

### 6. No Clear Output Format Specified ⚠️

**Missing:** What is the actual OUTPUT of this prompt?

- Just an image?
- Image + metadata?
- Image + description of what changed?
- Image + variation rationale?

### Recommendation: Add Output Specification

```markdown
## Output

**Primary Output:**
A single high-fidelity ad image (1080×1080 or 1920×1080) ready for digital advertising.

**Accompanying Metadata (optional but recommended):**
- Variation approach used: Conservative/Balanced/Bold
- Key visual changes: Brief description of new elements generated
- Strategic alignment: Confirmation that brief framework maintained
- Quality verification: Checklist completion status

**File specifications:**
- Format: PNG (for transparency support) or high-quality JPG
- Resolution: 1080×1080 (square), 1920×1080 (landscape), or 1080×1920 (vertical)
- Color space: sRGB
- Quality: Maximum (no visible compression)
```

---

### 7. BriefJSON Role Over-Emphasized But Unclear ⚠️

**The term "briefJSON" appears 15+ times** but the prompt never clearly explains:
- What specific elements to extract from it
- How to parse it
- What to do if it's missing or vague
- Examples of what briefJSON contains

### Recommendation: Add BriefJSON Parsing Guide

```markdown
## Using BriefJSON Strategic Context

**What BriefJSON Contains:**
- Campaign goals: Awareness/consideration/conversion objectives
- Messaging framework: Core value propositions and key messages
- Audience insights: Target demographic, psychographics, pain points
- Creative parameters: Tone (professional/playful), style guidelines
- Success metrics: What the campaign optimizes for

**How to Use It:**

**Extract Strategic Boundaries (must preserve):**
- Core message/positioning (can't change)
- Target audience (can't change)
- Campaign objective (can't change)
- Brand voice/tone (can't change)

**Identify Creative Flexibility (can vary):**
- Visual execution approach
- Specific imagery/metaphors used
- Headline phrasing (within message framework)
- Color palette variations (within brand system)
- Composition and layout

**If BriefJSON is Missing/Vague:**
- Default to BALANCED variation approach
- Infer campaign goals from CompanyInfo and ad context
- Preserve all messaging exactly as-is
- Focus variation purely on visual execution
```

---

### 8. Audit Checklist Not Actionable ⚠️

**Current checklist has subjective items:**
- "Scroll-stopping visual power present" - How to verify?
- "Variation explores creative alternatives" - How to measure?
- "Campaign goals from brief maintained" - How to confirm?

### Recommendation: Make Checklist Verifiable

```markdown
## Audit Checklist (Verification Guide)

### Visual Originality:
- [ ] **All people are new** (Verify: Different faces, clothing, poses than original)
- [ ] **All settings are new** (Verify: Different location, background, environment)
- [ ] **All objects are new** (Verify: Different furniture, props, equipment)

### Brand Consistency:
- [ ] **Logo unchanged** (Verify: Exact same logo file, same placement)
- [ ] **Brand colors accurate** (Verify: Hex codes match Brand JSON within ±5%)
- [ ] **Typography follows brand** (Verify: Font family matches guidelines)

### Quality Standards:
- [ ] **Contrast ≥ 4.5:1** (Verify: Use contrast checker tool on headline)
- [ ] **Resolution minimum 1080×1080** (Verify: Check image properties)
- [ ] **No compression artifacts** (Verify: Visual inspection at 100% zoom)

### Brief Alignment:
- [ ] **Messaging within framework** (Verify: Headline conveys same core message as brief)
- [ ] **Target audience appropriate** (Verify: Visuals match audience demographics from brief)
- [ ] **Campaign goals served** (Verify: Ad supports awareness/conversion/engagement goal)

### Copy Quality:
- [ ] **Headline ≤ 8 words** (Verify: Count words)
- [ ] **Body ≤ 12 words** (Verify: Count words)
- [ ] **CTA ≤ 3 words** (Verify: Count words)
- [ ] **No spelling errors** (Verify: Spell-check all text)
- [ ] **Grammar correct** (Verify: Review punctuation, capitalization)
```

---

### 9. Hard vs. Soft Constraints Unclear ⚠️

**Why are some constraints "hard" and others "soft"?**
What happens if violated?

### Recommendation: Clarify Constraint Types

```markdown
## Constraints

### HARD Constraints (Must Never Violate)
These are non-negotiable requirements. Violation = failed output.

1. **Visual Originality**: Never reuse original imagery
2. **Logo Integrity**: Never alter provided brand logo
3. **Readability**: Text contrast must meet WCAG AA (4.5:1)
4. **Platform Safety**: All elements within safe margins
5. **Copy Quality**: No spelling or grammar errors

**If violated:** Output is rejected, must regenerate

### SOFT Preferences (Optimize For)
These improve quality but aren't failures if missed.

1. **Tone**: Match brand voice from CompanyInfo
2. **Depth**: Use subtle lighting/gradients for visual interest
3. **Scroll-stopping**: High contrast, emotion, unexpected composition
4. **Authenticity**: Avoid generic stock aesthetic

**If missed:** Output acceptable but could be improved
```

---

## Context Efficiency Improvements

**Current size: ~15KB (405 lines)**
**Target size: <10KB (250-280 lines)**

### Consolidation Strategy:

**1. Eliminate Repetition (save ~30%):**
- Consolidate "new visual elements" messaging to ONE section
- Remove redundant process sections (3 → 1)
- Combine overlapping checklists

**2. Compress Examples (save ~10%):**
- Keep 3-5 examples but make them more compact
- Use table format for visual elements comparison
- Focus on key differentiators, not every detail

**3. Streamline Sections (save ~10%):**
- Merge "Soft Preferences" into relevant constraint sections
- Combine "Copy Rules" with "Hard Constraints"
- Integrate "Accessibility" into "Quality Standards"

**4. Remove Redundant Text (save ~5%):**
- "Brief alignment" mentioned 10+ times - reduce to 3-4
- Simplify language (shorter sentences, fewer adjectives)

---

## Suggested New Structure (Optimized)

```markdown
# Create Image Variation

## Role & Mission (100 words)
[Concise objective]

## Inputs (50 words)
[List inputs]

## Quality Standards Defined (150 words)
[Quantitative definitions of scroll-stopping, professional, high contrast, clean spacing, clear hierarchy]

## Visual Originality Requirement (200 words)
[THE consolidated section on creating new elements - replaces 7 current sections]

## Execution Process (150 words)
[Single 5-step process - replaces 3 current processes]

## Variation Approaches + Decision Tree (200 words)
[Conservative/Balanced/Bold with clear decision criteria]

## Constraints (250 words)
[Hard constraints (with violations = fail) + Soft preferences integrated]

## BriefJSON Usage Guide (150 words)
[How to parse and use strategic context]

## Examples (1500 words)
[3-5 DETAILED examples with visual descriptions, brand context, new elements, results]

## Audit Checklist (200 words)
[Verifiable checklist with how-to-check guidance]

## Output Specification (100 words)
[What the final output should be]

Total: ~2700 words, ~9KB
```

---

## Priority Ranking

### Must Have (Critical):
1. **Add detailed examples** (biggest gap - compare to 21c quality)
2. **Define quality terms quantitatively** (scroll-stopping, professional, etc.)
3. **Consolidate repetition** (new visual elements message repeated 7+ times)
4. **Single clear process** (currently has 3 confusing processes)

### Should Have (High Value):
5. **Decision tree for variation approach** (when to use conservative/balanced/bold)
6. **BriefJSON parsing guide** (over-mentioned but under-explained)
7. **Verifiable audit checklist** (make it actionable)
8. **Output specification** (what is the deliverable?)

### Nice to Have (Incremental):
9. **Clarify hard vs soft constraints** (and consequences)
10. **Context optimization** (reduce from 15KB to <10KB)

---

## Comparison to 21c (Now High Quality)

**21c Strengths to Adopt:**
- ✅ 5 detailed examples with full execution details
- ✅ Quantified quality standards (professional = X, smooth = Y)
- ✅ Single clear process (not multiple)
- ✅ Concrete output specification
- ✅ ~11KB size (efficient but comprehensive)

**23 Current Weaknesses:**
- ❌ 3 brief examples lacking detail
- ❌ Vague quality terms (no definitions)
- ❌ 3 overlapping processes
- ❌ No output specification
- ❌ ~15KB with massive repetition

---

## Quick Wins (Highest ROI)

**Week 1: Examples + Definitions**
1. Add 3-5 detailed examples (like 21c quality)
2. Add Quality Standards Defined section with quantitative criteria
**Estimated improvement: 6.5/10 → 8/10**

**Week 2: Consolidation**
3. Consolidate "new visual elements" to ONE section
4. Merge 3 processes into 1 clear process
**Estimated improvement: 8/10 → 8.5/10**

**Week 3: Polish**
5. Add decision tree for variation approaches
6. Add BriefJSON parsing guide
7. Make audit checklist verifiable
**Estimated improvement: 8.5/10 → 9/10**

---

## Summary

The 23 prompt has good bones but needs:
- **Concrete examples** (biggest gap)
- **Defined standards** (quantify quality terms)
- **Reduced repetition** (40% is redundant)
- **Clear process** (consolidate 3 into 1)
- **Better guidance** (decision trees, parsing guides)

Foundation is solid; execution needs tightening and examples.
