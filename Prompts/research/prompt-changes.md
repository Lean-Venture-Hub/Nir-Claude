# Prompt Changes: Creative Quality Improvement

**Implementation Date**: 2025-12-23
**Strategy**: Option A (Creative Divergence Engine) + Option B (Hook Innovation Lab) + Quick Wins
**Goal**: Significantly improve ad creative quality by reducing generic/obvious patterns

---

## Change Summary

| Prompt | Change Type | Impact | Priority |
|--------|------------|---------|----------|
| NEW #22 | Create new prompt | Highest | Critical |
| #14 Brief Creator | Enhance Rare Angles + Hooks | High | Critical |
| #17 Template Gen | Add surprise mandate | Medium | Quick Win |
| #20 Ad Analysis | Add creativity audits | Medium | Quick Win |
| NEW library | Generic patterns database | Medium | Quick Win |

---

## 1. NEW PROMPT #22: Creative Divergence Engine

**File**: `22 Creative Divergence Engine.md`
**Position**: Executes AFTER Prompt #14 (Brief Creator), BEFORE Prompt #17 (Template Generation)
**Purpose**: Inserts a creative ideation stage that generates 3-5 wildly different visual concepts using metaphors, lateral thinking, and non-obvious approaches

### Key Components

**Role**
Visual concept strategist specializing in divergent thinking and metaphorical translation

**Input**
- Brief from Prompt #14
- Company info
- Brand guidelines
- Campaign objective

**Process**
1. Analyze brief's core message
2. Generate 3-5 divergent visual concepts using:
   - **Analogical Transfer**: Map concept to unrelated domain (e.g., "security" → fortress → moat → castle)
   - **Temporal Shift**: Show before/after, past/future contrast
   - **Scale Manipulation**: Zoom in/out dramatically (microscopic/cosmic view)
   - **Enemy Creation**: Define what you're NOT (anti-pattern positioning)
   - **Negative Space**: What's missing is the message
   - **Personification**: Abstract concepts as characters
   - **Contradiction**: Visual paradox that resolves to insight
   - **Cultural Remix**: Blend unexpected cultural references

3. For each concept, specify:
   - **Visual metaphor** (1 sentence)
   - **Execution direction** (composition, color mood, style)
   - **Surprise element** (what's unexpected)
   - **Rationale** (why this works for the message)

**Output Format**
```json
{
  "divergent_concepts": [
    {
      "concept_id": 1,
      "visual_metaphor": "One-line metaphor description",
      "execution_direction": "How to execute visually",
      "surprise_element": "What's unexpected",
      "rationale": "Why this works",
      "technique_used": "Analogical Transfer | Temporal Shift | etc."
    }
  ],
  "recommended_concept": 1,
  "recommendation_reason": "Why this one is strongest"
}
```

**Success Criteria**
- Each concept feels p < 0.15 (unexpected but plausible)
- No generic B2B clichés (handshakes, arrows up, lightbulbs)
- Visual metaphor is immediately graspable but non-obvious
- Executes within brand guidelines and platform constraints

**Integration Point**
User selects 1 concept → feeds into Prompt #17 as `divergent_concept_input`

---

## 2. ENHANCE PROMPT #14: Hook Innovation Lab

**File**: `14 Brief Creator.md`
**Changes**: Expand Rare Angles methodology + enhance Hooks Toolkit

### Change 2A: Rare Angles Enhancement (Lines 149-158)

**CURRENT (B2. Rare Angles section)**:
```markdown
Use this Tail-Sampling Routine:
- Mainstream Map: one-liner summary of what everyone says.
- Inversion/Orthogonal: flip, negate, or sidestep the premise.
- Unexpected Insight First: lead with the sharpest delta.
- Tail Check: does this feel p < 0.10 vs. feed norms? keep it if yes.
- PRISM: make it read human, not optimized.
```

**NEW (Replace lines 149-158)**:
```markdown
Use this Tail-Sampling Routine with 10 Contrarian Techniques:

**Step 1: Mainstream Map**
One-liner: what 90% of competitors say about this problem/solution.

**Step 2: Apply Contrarian Technique** (choose 1-2 per concept):

1. **Analogical Transfer** - Map the problem to a completely different domain
   - Example: B2B sales → Dating (rejection, timing, compatibility)
   - Example: Cloud security → Medieval fortress defense

2. **Temporal Inversion** - Flip the time frame
   - Instead of "future-proof", talk about "past-debt" you're fixing
   - Instead of "what you'll gain", show "what you've already lost"

3. **Enemy Creation** - Define yourself by what you oppose
   - "We're the anti-dashboard" / "For people who hate networking events"
   - Creates tribal identity through shared rejection

4. **Silence Breaking** - Say the thing everyone thinks but won't say
   - "Your current tool is lying to you" / "Nobody reads your reports"
   - Unspoken industry truth exposed

5. **Scale Manipulation** - Zoom dramatically in or out
   - Micro: "The 6-second moment that kills deals"
   - Macro: "Every company will face this by 2027"

6. **Role Reversal** - Swap who has the problem
   - "Your customers are managing YOU" / "The intern sees what the CEO can't"

7. **Benefit Negation** - Lead with what you DON'T do
   - "No dashboards" / "Zero meetings required" / "We don't automate everything"

8. **Cost Reframe** - Change the cost dimension
   - Not money cost → time cost, dignity cost, opportunity cost
   - "Costs you 3 hours/week" hits harder than "$X/month"

9. **Invisible Made Visible** - Expose hidden mechanisms
   - "Here's why your ads stop working after 14 days"
   - Reveal the algorithm/system/pattern invisible to users

10. **Contradiction Resolution** - Present paradox that resolves to insight
    - "The best leaders are the worst managers"
    - "Growing slower is how you scale faster"

**Step 3: Unexpected Insight First**
Lead with the sharpest delta from mainstream thinking.

**Step 4: Tail Check**
Does this feel p < 0.10 vs. LinkedIn feed norms? If yes, proceed. If no, try different technique.

**Step 5: PRISM Application**
Make it read human, not optimized. No hype language.

**Rare Angle Quality Gates**:
- ✓ Feels slightly uncomfortable (good sign)
- ✓ Can't find 5 similar examples in competitor feed
- ✓ Makes reader stop and reconsider premise
- ✗ Avoids being contrarian just for shock value
- ✗ Stays truthful and defensible
```

### Change 2B: Hooks Toolkit Enhancement (Lines 116-132)

**ADD AFTER LINE 132** (after banned/greenlit phrases):

### Change 2C: JSON Output Schema Update (Lines 295-298)

**ADD TO BRIEF OBJECT** (after "Hook concept" field):

```json
"Mainstream_one_liner": "",
"Contrarian_angles_chosen": ""
```

**Field Documentation**:
- **Mainstream_one_liner**: For rare_angle concepts only. One-line summary of what 90% of competitors say (from Step 1 of Rare Angles routine). Leave empty for competitor_success concepts.
- **Contrarian_angles_chosen**: For rare_angle concepts only. List the contrarian technique(s) used (e.g., "Analogical Transfer", "Silence Breaking + Temporal Inversion"). Leave empty for competitor_success concepts.

**Purpose**: Enables tracking which contrarian techniques produce best results, helping optimize rare angle generation over time.

**Updated Quality Checklist** (Line 325):
- Old: "Audit Trail: for Rare Angles, include a 1-line tail_note (outside the JSON) explaining the inversion used."
- New: "Audit Trail: for Rare Angles, include a 1-line tail_note (outside the JSON) explaining the inversion used. Also populate Mainstream_one_liner and Contrarian_angles_chosen fields in JSON."

```markdown
### Hook Innovation Modes

When crafting hooks for Rare Angles, combine toolkit shapes with contrarian techniques:

**Contradiction + Enemy Creation**
"Everyone's buying marketing automation. You're buying busywork."

**Silence Breaking + Temporal Inversion**
"You didn't lose the deal today. You lost it 3 weeks ago when..."

**Pattern Break + Scale Manipulation**
"You were told to scale headcount. The real limit is this 11-minute bottleneck."

**Reframe + Invisible Made Visible**
"ROI isn't about revenue. It's about recovered founder hours."

**Personal Stake + Cost Reframe**
"I wasted $40K before realizing it wasn't budget—it was 6 seconds of copy."

**Hook Temperature Check**:
- Cold (generic): "Transform your marketing workflow"
- Warm (decent): "Marketing automation without the bloat"
- Hot (rare angle): "Your marketing stack is managing you now"
```

---

## 3. ENHANCE PROMPT #17: Surprise Mandate

**File**: `17 Template Generation Prompt.md`
**Change**: Add mandatory surprise element requirement

### Change 3A: Add to Success Criteria (After Line 23)

**INSERT AFTER LINE 23**:
```markdown
- Surprise element: At least ONE unexpected visual/compositional choice that breaks pattern
```

### Change 3B: Add Surprise Mandate Section (After Line 106)

**INSERT NEW SECTION AFTER LINE 106** (after Soft Preferences):

```markdown
## Surprise Mandate

Every ad MUST include at least ONE unexpected element that breaks predictable patterns:

**Approved Surprise Techniques**:
- **Scale Contrast**: Dramatically oversized or undersized element (e.g., giant emoji, tiny product)
- **Color Inversion**: Use opposite of expected brand palette in one focal area
- **Negative Space Message**: Key element communicated by what's NOT there
- **Layering Paradox**: Impossible depth or perspective (Escher-like but subtle)
- **Texture Clash**: Mix incompatible textures (organic + digital, rough + smooth)
- **Cropping Boldness**: Unexpected crop that hides expected element
- **Typography Break**: One word in radically different font/size/orientation
- **Pattern Disruption**: Regular grid broken by single rogue element
- **Movement Implication**: Static image clearly implies motion/direction
- **Empty-Focus**: Most prominent space is empty; message at edges

**Surprise Quality Gates**:
- ✓ Makes viewer do a double-take (0.5 second pause)
- ✓ Doesn't violate brand guidelines
- ✓ Enhances message, doesn't distract
- ✓ Can't be found in 80%+ of competitor ads
- ✗ Avoids gimmicks (lens flare, excessive gradients, clichéd effects)
- ✗ Maintains accessibility (contrast, legibility)

**Implementation**:
At temperature 0.0-0.4: Choose ONE subtle surprise (e.g., unexpected crop, scale contrast)
At temperature 0.5-0.7: Choose TWO moderate surprises
At temperature 0.8-1.0: Full creative reinterpretation with multiple surprise elements

**Note**: Refer to `generic-patterns-to-avoid.md` to ensure surprise element isn't replacing one cliché with another.
```

### Change 3C: Update Audit Section (Line 140-150)

**REPLACE LINE 141** (current audit checklist):

**CURRENT**:
```markdown
- Does the Ad has a scroll stopping effect? YES/NO
```

**NEW**:
```markdown
- Does the Ad has a scroll stopping effect? YES/NO
- Surprise element present (≥1 unexpected choice): YES/NO
- Surprise enhances message (not gimmick): YES/NO
```

---

## 4. ENHANCE PROMPT #20: Creativity Audits

**File**: `20 analyze ad output.md`
**Change**: Add originality and non-obvious metrics to creative quality section

### Change 4A: Already Present (Lines 60-61)

**GOOD NEWS**: Prompt #20 already has these metrics!
```markdown
- **Originality**: Fresh approach, not generic ___/5
- **Non-Obvious**: Avoids clichés and predictable patterns ___/5
```

### Change 4B: Enhance Audit Guidance (ADD NEW SECTION)

**INSERT AFTER LINE 308** (after Video Motion Philosophy):

```markdown
### Creativity Audit Deep Checks

When scoring **Originality** and **Non-Obvious**, use these tests:

**Originality Assessment (1-5)**:
- 5 = Cannot find similar visual approach in competitor set; truly novel
- 4 = Rare approach; maybe 1-2 similar examples exist
- 3 = Moderately fresh; small twist on common pattern
- 2 = Derivative; clear template/trend-following
- 1 = Generic; looks like 20+ other ads in category

**Non-Obvious Assessment (1-5)**:
- 5 = Subverts expectations; requires 2+ seconds to parse meaning
- 4 = Clear surprise element; breaks predictable pattern
- 3 = Competent execution but follows expected formula
- 2 = Relies on clichés (handshakes, arrows up, light bulbs)
- 1 = Painfully obvious; first-thought creative

**Generic Pattern Detection**:
Cross-reference against `generic-patterns-to-avoid.md`. Flag if ad uses ≥2 patterns from that list.

**Creativity Failure Modes**:
- Template-thinking: Looks like it came from a Canva search
- Hype over substance: Relies on superlatives instead of visual idea
- Stock photo syndrome: Could apply to any company in vertical
- CTA-first design: Entire ad is just a CTA button dressed up
- Color-only differentiation: Only unique thing is brand color swap

**Scoring Guidance**:
- An ad can score 5/5 on Originality but 2/5 on Non-Obvious (novel but still predictable)
- An ad can score 3/5 on Originality but 5/5 on Non-Obvious (familiar execution, surprising angle)
- Target: Every ad should score ≥4 on at least ONE of these metrics
```

---

## 5. NEW FILE: Generic Patterns Library

**File**: `research/generic-patterns-to-avoid.md`
**Purpose**: Database of overused B2B visual clichés to avoid

### Content Structure

```markdown
# Generic Patterns to Avoid

20 most overused B2B ad patterns that signal lazy creative thinking.

## Visual Clichés

1. **Corporate Handshake** - Two hands shaking (trust, partnership)
2. **Upward Arrow/Graph** - Growth chart going up-right
3. **Light Bulb** - Innovation, ideas, "aha moment"
4. **Jigsaw Puzzle Pieces** - Integration, fitting together
5. **Mountain Climb/Summit** - Achievement, reaching goals
6. **Maze/Labyrinth** - Complexity, finding the path
7. **Key Unlocking** - Access, solutions, unlocking value
8. **Bridge Connecting** - Bridging gaps, connection
9. **Gears Turning** - Efficiency, systems working together
10. **Rocket Launch** - Growth, speed, scaling

## Composition Clichés

11. **Center-logo Lockup** - Logo dead-center with tagline below
12. **Left-right Split** - Before/after or VS comparison (when obvious)
13. **Floating Product Hero** - Product on gradient background, nothing else
14. **Quote-card Template** - Testimonial quote in quotation marks, headshot
15. **Checklist on Color** - Bullet list of features on solid background

## Copy Clichés

16. **Question Hook Pattern** - "Struggling with X?" "Tired of Y?" "Ready to Z?"
17. **Power Words Spam** - Revolutionary, game-changing, industry-leading, next-gen
18. **Social Proof Stack** - "Join 10,000+ companies" as primary message
19. **Vague Benefit Claim** - "Work smarter" "Grow faster" "Scale effortlessly"
20. **CTA-only Creative** - Entire ad is just "Download Now" with logo

## When These ARE Acceptable

Some patterns work IF subverted:
- Upward arrow → Show it going DOWN with contrarian message
- Corporate handshake → Show hands NOT shaking (enemy creation)
- Checklist → Make items surprising/contradictory
- Center logo → Break it with asymmetric surprise element

## Replacement Philosophy

Instead of reaching for these patterns:
1. Use visual metaphor from different domain
2. Show the mechanism, not the symbol (HOW it works, not THAT it works)
3. Lead with the insight, let visual follow naturally
4. Make the "wrong" choice deliberately (Creative Divergence Engine)
5. Show consequence/cost of NOT using solution instead of benefit

## Audit Questions

- If I removed the logo, could this be ANY company? (FAIL)
- Would a stock photo site tag this with generic terms? (FAIL)
- Can I find 5+ similar ads in competitor research? (FAIL)
- Does this visual require explanation to connect to message? (FAIL)
- Would this work on a conference banner in 2015? (FAIL)
```

---

## Implementation Priority

### Phase 1: Foundation (Week 1)
1. ✅ Create Prompt #22: Creative Divergence Engine
2. ✅ Create `generic-patterns-to-avoid.md`
3. ✅ Enhance Prompt #14: Hook Innovation Lab (Changes 2A + 2B)

### Phase 2: Integration (Week 1)
4. ✅ Enhance Prompt #17: Surprise Mandate (Changes 3A + 3B + 3C)
5. ✅ Enhance Prompt #20: Creativity Audits (Change 4B)

### Phase 3: Testing (Week 2)
6. Run 10 test campaigns through updated pipeline
7. Score before/after on Originality + Non-Obvious metrics
8. Measure user feedback on "generic vs. creative" perception

---

## Success Metrics

**Before** (baseline from user feedback):
- Ads feel "too generic and obvious"
- High pattern repetition across outputs
- Low differentiation from competitors

**After** (target):
- Originality score: ≥4/5 on 80% of concepts
- Non-Obvious score: ≥4/5 on 60% of concepts
- Zero usage of patterns from generic-patterns-to-avoid.md
- User feedback: "More creative, less predictable"
- Divergent concepts: 3-5 wildly different options per brief

---

## Integration with Existing Workflow

**Current Flow**:
1. Company Info (#1)
2. Target Audience (#2)
3. Competitive Analysis (#4-8)
4. Brief Creator (#14) → outputs 6 concepts
5. Template Generation (#17) → creates ad image
6. Analyze Ad Output (#20) → QA check

**New Flow** (with improvements):
1. Company Info (#1)
2. Target Audience (#2)
3. Competitive Analysis (#4-8)
4. **Brief Creator (#14)** ← ENHANCED with Hook Innovation Lab
5. **→ Creative Divergence Engine (#22)** ← NEW STEP (outputs 3-5 visual concepts)
6. **User selects 1 concept** (or proceeds without selection for traditional flow)
7. **Template Generation (#17)** ← ENHANCED with Surprise Mandate + selected divergent concept
8. **Analyze Ad Output (#20)** ← ENHANCED with Creativity Audits
9. Publish or iterate

**Optional Fast Path**: Users can skip #22 if they want speed over creativity

---

## Files Modified Summary

| File | Lines Changed | Type |
|------|---------------|------|
| `22 Creative Divergence Engine.md` | NEW FILE | Creation |
| `14 Brief Creator.md` | Lines 149-158 (replace) + after 132 (add) | Enhancement |
| `17 Template Generation Prompt.md` | After 23 (add) + after 106 (add) + line 141 (replace) | Enhancement |
| `20 analyze ad output.md` | After 308 (add) | Enhancement |
| `research/generic-patterns-to-avoid.md` | NEW FILE | Reference |

---

## Rollback Plan

If changes reduce output quality or break workflow:
1. Keep Prompt #22 as optional (users can skip)
2. Make Surprise Mandate temperature-dependent (only at 0.6+)
3. Revert Rare Angles to original if too extreme
4. Keep creativity audits in #20 (no downside)
5. Generic patterns library remains as reference only

---

## Next Steps

1. ✅ Create all new files and enhancements
2. Test with 5 sample briefs (different industries)
3. Compare outputs before/after changes
4. Gather user feedback on creative quality
5. Iterate based on results
6. Update PLAN.md with implementation status
