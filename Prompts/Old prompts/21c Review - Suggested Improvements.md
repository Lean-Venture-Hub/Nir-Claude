# Review: 21c Video Editing Prompt - Improvement Suggestions

## Executive Summary

The 21c prompt is well-structured with clear objectives and comprehensive process steps. However, it lacks concrete examples, has some ambiguous terminology, and could benefit from clearer decision trees for edge cases.

**Overall Score: 7/10**
- Structure: 9/10 ✅
- Clarity: 7/10 ⚠️
- Examples: 0/10 ❌ (Biggest gap)
- Completeness: 8/10 ✅
- Actionability: 7/10 ⚠️

---

## Critical Gap: Missing Examples

### Issue
The prompt provides a comprehensive template but **ZERO concrete examples** showing:
- What actual UserInput looks like
- How to transform UserInput into final prompt
- What a completed, filled-in template looks like

### Impact
- AI models learn best from examples (few-shot learning)
- Users can't visualize expected output
- Ambiguities in process aren't resolved by seeing real cases

### Recommendation: Add 3-5 Examples

**Suggested Example Structure:**

```markdown
## Examples

### Example 1: Simple Text Change
**UserInput**: "Change the headline to 'Transform Your Workflow' and make the CTA button say 'Start Free Trial'"

**CompanyInfo**: Productivity SaaS, blue (#2563EB) brand color
**Brand**: Professional, modern, B2B tone

**Generated Prompt**:
```
Preserve brand integrity - maintain logo, brand colors, and core messaging unless explicitly specified otherwise in edit requests below.

EDIT OVERVIEW:
Update text elements (headline and CTA) to new messaging while maintaining all visual design and brand consistency.

PRIMARY EDITS (Priority 1):
- Edit 1: Replace headline text
  - Timecode: 0:00 - 0:05 (or whenever headline is visible)
  - Current text: [original headline]
  - New text: "Transform Your Workflow"
  - Keep existing: Font, size, color, position, animation timing

- Edit 2: Update CTA button text
  - Timecode: 0:03 - 0:05 (or whenever CTA is visible)
  - Current text: [original CTA]
  - New text: "Start Free Trial"
  - Keep existing: Button design, color, position, animation

SECONDARY EDITS (Priority 2):
- None required

VISUAL ENHANCEMENTS:
- Maintain all existing visual styling
- Ensure text remains readable with existing background

TEXT/GRAPHIC CHANGES:
- Headline: "Transform Your Workflow" (exact capitalization)
- CTA: "Start Free Trial" (exact capitalization)
- All other text unchanged

AUDIO ADJUSTMENTS:
- No audio changes required

TECHNICAL SPECIFICATIONS:
- Original duration: Unchanged
- Aspect ratio: Maintain original
- Resolution: Match original (minimum 1080p)
- Frame rate: Match original
- Export format: MP4
- Quality: Maximum, professional-grade output

PRESERVE:
- Logo: Unchanged position, size, timing
- Brand colors: Blue (#2563EB) maintained throughout
- Core messaging: Product positioning unchanged
- Visual design: All animations, transitions, effects unchanged
- Quality: Match original video quality exactly

TRANSITION REQUIREMENTS:
- Text changes should appear seamlessly (no flicker or repositioning)
- Maintain all existing text animations and timing
- Ensure new text length fits existing design space

Style: Clean, precise text replacement maintaining all brand consistency and professional polish. Changes are purely textual with zero visual/structural modifications.
```
```

**Add variations:**
- Example 2: Color grading adjustment (simple visual enhancement)
- Example 3: Speed change + crop (multi-category edit)
- Example 4: Text + audio + timing changes (complex multi-edit)
- Example 5: Edge case - user requests brand color change (brand safety scenario)

---

## Ambiguous Terminology

### Issue: Undefined Qualitative Terms

Terms like "professional," "smooth," "natural," and "polished" appear throughout but lack quantitative definitions.

**Examples of ambiguity:**
- Line 14: "Creates smooth, polished results appropriate for professional advertising"
- Line 208: "All edits must be smooth and professional"
- Line 299: "Output must meet professional advertising standards"

### Recommendation: Define or Quantify

**Option 1: Add Definitions Section**

```markdown
## Terminology Definitions

**Professional advertising standards:**
- No visible compression artifacts or quality loss
- Frame-accurate edits (no frame skipping or stuttering)
- Audio sync maintained within ±1 frame
- Color consistency across all edited segments
- Text/graphics render at full resolution without aliasing
- Transitions minimum 12 frames (0.4s at 30fps) for smooth perception

**Smooth transitions:**
- No visible frame jumps or discontinuities
- Motion blur appropriate for speed changes
- Audio crossfades minimum 0.3s for music/ambient, 0.1s for dialogue
- Visual consistency maintained before/after edit points

**Brand-appropriate:**
- Colors match brand palette within 5% delta-E tolerance
- Visual style matches CompanyInfo industry positioning
- Tone aligns with Brand personality descriptors
```

**Option 2: Use Examples to Show Standards**

In each example, explicitly note what makes it "professional" or "smooth"

---

## Process Flow Clarity

### Issue: Linear Process But Complex Decisions

The 6-step process (Parse → Quality Check → Enrich → Safety → Construct) is clear, but lacks guidance for:
- What to do when steps conflict
- How to handle edge cases
- When to ask for clarification vs. make assumptions

### Recommendation: Add Decision Trees

**Example Decision Tree:**

```markdown
## Decision Tree: Handling Brand-Modifying Requests

```
UserInput requests brand element change
    │
    ├─→ Logo change requested?
    │   ├─→ YES → Flag for approval
    │   │         Note in output: "⚠️ LOGO CHANGE REQUESTED - requires brand approval"
    │   │         Provide alternative if possible
    │   │         Proceed with change documented clearly
    │   │
    │   └─→ NO → Continue to color check
    │
    ├─→ Brand color change requested?
    │   ├─→ Completely different palette?
    │   │   └─→ Flag high-risk, suggest brand-aligned alternative
    │   │
    │   └─→ Subtle adjustment (saturation, brightness)?
    │       └─→ Proceed with parameters specified
    │
    └─→ Core messaging change?
        ├─→ Contradicts CompanyInfo value props?
        │   └─→ Flag concern, proceed with user intent documented
        │
        └─→ Aligns with brand voice?
            └─→ Proceed normally
```
```

**Add decision trees for:**
- Conflicting edit requests (e.g., "make it faster but add more content")
- Technically infeasible requests
- Ambiguous timecode references
- Missing critical information

---

## Template Complexity

### Issue: Long Template May Overwhelm

The template (lines 162-214) is comprehensive but 50+ lines long, which may be:
- Intimidating for simple edits
- Harder to fill out correctly
- Less scannable for AI models

### Recommendation: Tiered Templates

**Provide 3 template sizes:**

**1. Minimal Template (simple edits):**
```markdown
Brand preservation: [Logo/colors/messaging to preserve]
Edit: [Specific change with timecode and parameters]
Technical specs: [Duration/resolution/format]
Quality: Professional, smooth integration
```

**2. Standard Template (most use cases):**
- Current template streamlined to ~25 lines
- Include only commonly used sections

**3. Comprehensive Template (complex edits):**
- Full current template for multi-category, complex edits

**Add guidance:**
```markdown
## Template Selection Guide

Use **Minimal Template** when:
- Single category edit (text only, color only, or timing only)
- Straightforward request with no ambiguity
- No brand element modifications

Use **Standard Template** when:
- 2-3 edit categories involved
- Some technical enrichment needed
- Standard brand preservation

Use **Comprehensive Template** when:
- Multi-category complex edits
- Brand modifications requested
- High-stakes video with detailed requirements
- Edge cases or special considerations
```

---

## Edge Cases & Error Handling

### Issue: Missing Guidance for Common Problems

No explicit handling for:
- Contradictory user requests
- Technically impossible edits
- Insufficient information
- Conflicting priorities

### Recommendation: Add Edge Case Section

```markdown
## Edge Case Handling

### Contradictory Requests
**Scenario**: User asks to "speed up to 30 seconds but add 15 seconds of new content"
**Action**:
1. Calculate if physically possible
2. If not, flag contradiction in output
3. Suggest resolution: "To fit 15s new content in 30s total, original content must be compressed to 15s (50% speed increase). Confirm this is acceptable or adjust target duration."

### Technically Infeasible Edits
**Scenario**: "Remove the person from the video but keep everything else"
**Action**:
1. Flag as advanced AI requirement (object removal)
2. Note limitations: "Person removal requires advanced AI inpainting. May result in artifacts. Recommend alternative: crop to exclude person, or replace with B-roll."

### Ambiguous Timecodes
**Scenario**: "Change the text in the middle"
**Action**:
1. Flag ambiguity in output
2. Provide best estimate: "Interpreting 'middle' as 50% point ([X] seconds). Specify exact timecode if different."

### Missing Critical Info
**Scenario**: User requests "change the headline" but doesn't provide new text
**Action**:
1. Cannot proceed without info
2. Output: "⚠️ MISSING REQUIRED INFO: New headline text not specified. Please provide exact text for headline replacement."

### Priority Conflicts
**Scenario**: Brand preservation vs. user intent clash
**Action**:
1. Document the conflict
2. Defer to user intent (per line 25-27)
3. Flag for review: "⚠️ User requested [X] which modifies [brand element]. Proceeding per user intent. Recommend brand team review."
```

---

## Quality Checklist Enhancement

### Issue: Checklist is Good But Could Be More Actionable

Current checklist (lines 216-259) is comprehensive but items are yes/no without guidance on **how** to ensure compliance.

### Recommendation: Add "How to Verify" Guidance

**Enhanced checklist format:**

```markdown
### Technical Completeness:

- [ ] **Specific timecodes provided for all edits**
  - How to verify: Every edit has format "Timecode: MM:SS - MM:SS" or "Timecode: MM:SS"
  - If missing: Add approximate timecode with flag "[estimated - confirm]"

- [ ] **Visual parameters specified (colors, positions, scales)**
  - How to verify: Any color mention includes hex code or RGB values
  - How to verify: Position uses specific terms (top-left, centered, offset +50px)
  - How to verify: Scale uses percentages or pixel dimensions
  - If missing: Add parameters with best estimate from brand guidelines

- [ ] **Text changes written verbatim with exact formatting**
  - How to verify: New text appears in quotes: "Exact New Text Here"
  - How to verify: Capitalization specified explicitly
  - How to verify: Special characters/punctuation included
  - If missing: Use title case as default, flag for confirmation

- [ ] **Duration and timing requirements stated**
  - How to verify: Original duration stated: "Original: Xs"
  - How to verify: Target duration stated: "Target: Ys"
  - How to verify: If unchanged: "Duration: Unchanged"
  - If missing: State "Duration: Maintain original [X]s"
```

---

## Output Format Improvements

### Issue: Structure vs. Template Redundancy

Lines 265-276 describe structure, but it duplicates the template section. This could confuse.

### Recommendation: Clarify Relationship

**Option 1: Merge sections**
```markdown
## Output Format & Template

The output follows this 10-section structure. Use the appropriate template tier (minimal/standard/comprehensive) based on edit complexity:

[Then show all three templates with the structure mapped]
```

**Option 2: Separate clearly**
```markdown
## Output Structure
[Current structure list - conceptual]

## Output Templates
[Minimal/Standard/Comprehensive templates - concrete]

**Relationship**: The structure defines *what* to include; the template shows *how* to format it.
```

---

## Suggested Additions

### 1. Add "Common Patterns" Section

Similar to the prompt engineering best practices guide:

```markdown
## Common Edit Patterns

### Pattern: Text-Only Update
**When**: User requests only text changes, no visual/audio modifications
**Template**: Use Minimal
**Key sections**: Text/Graphic Changes, Preserve (everything else)
**Example**: "Change headline to [X]"

### Pattern: Speed Adjustment
**When**: User requests timing changes (speed up, slow down, freeze frame)
**Template**: Use Standard
**Key sections**: Motion & Timing Edits, Technical Specs (duration change)
**Example**: "Slow down the product reveal to 50% speed"

### Pattern: Color Grading
**When**: User requests mood/tone adjustment through color
**Template**: Use Standard
**Key sections**: Visual Enhancements (specific color parameters)
**Example**: "Make it warmer and more vibrant"

### Pattern: Multi-Category Complex Edit
**When**: User requests changes across 3+ categories
**Template**: Use Comprehensive
**Example**: "Speed up the intro, change text, adjust colors, and trim to 15s"
```

### 2. Add "Failure Modes" Section

```markdown
## Common Failure Modes & Prevention

### Failure: Vague Parameters
**Symptom**: Output says "adjust color" without specific values
**Prevention**: Always include quantitative values (saturation +15%, brightness -10%)

### Failure: Missing Timecodes
**Symptom**: Edit described but no timing specified
**Prevention**: Every edit must have timecode, estimate if user didn't provide

### Failure: Contradictory Instructions
**Symptom**: Preserve brand colors but also change color palette
**Prevention**: Flag contradiction explicitly in output, provide resolution path

### Failure: No Quality Standards
**Symptom**: Output doesn't specify resolution, frame rate, export quality
**Prevention**: Technical Specifications section is mandatory, use defaults if not specified
```

### 3. Add "Terminology Glossary"

```markdown
## Video Editing Terminology

For clarity in generated prompts:

**Timecode**: MM:SS or HH:MM:SS format (e.g., "01:23" = 1 minute 23 seconds)
**Frame rate**: Frames per second - 30fps (standard), 60fps (smooth motion), 24fps (cinematic)
**Aspect ratio**: Width:Height - 16:9 (landscape), 9:16 (vertical), 1:1 (square)
**Color grading**: Adjusting colors for mood - saturation (color intensity), contrast (light/dark difference), temperature (warm/cool tones)
**Transition**: Visual connection between cuts - cut (instant), fade (gradual opacity), dissolve (blend)
**B-roll**: Supplementary footage used to cover edits or add context
```

---

## Priority Ranking of Improvements

### Must Have (Critical):
1. **Add 3-5 concrete examples** (biggest gap, highest impact)
2. **Define ambiguous terms** (reduces confusion and errors)
3. **Add edge case handling** (prevents failures on common problems)

### Should Have (High Value):
4. **Add decision trees** (makes complex scenarios easier to navigate)
5. **Tiered templates** (improves usability for simple vs complex edits)
6. **Enhanced checklist with verification guidance** (makes quality checks actionable)

### Nice to Have (Incremental):
7. **Common patterns section** (speeds up common use cases)
8. **Failure modes section** (proactive error prevention)
9. **Terminology glossary** (standardizes language)
10. **Output format clarification** (minor organizational improvement)

---

## Implementation Suggestions

### Phase 1: Critical Fixes (Week 1)
- Add Examples section with 5 concrete examples covering:
  - Simple text change
  - Visual enhancement (color grading)
  - Speed + structural edit
  - Complex multi-category edit
  - Edge case (brand conflict)

- Add Terminology Definitions section with quantitative standards

### Phase 2: High-Value Additions (Week 2)
- Add Decision Trees for:
  - Brand-modifying requests
  - Conflicting requirements
  - Missing information

- Create Tiered Templates (Minimal/Standard/Comprehensive)

### Phase 3: Polish (Week 3)
- Add Edge Case Handling section
- Enhance Quality Checklist with "How to Verify"
- Add Common Patterns section

---

## Specific Line-by-Line Suggestions

### Line 14: "Creates smooth, polished results"
**Change to**: "Creates smooth (no visible frame jumps, minimum 12-frame transitions), polished results suitable for paid advertising placement"

### Line 34: "unless explicitly requested and justified"
**Add**: "unless explicitly requested and justified (Note: Will require brand team approval flag in output)"

### Line 127-132: Technical optimization list
**Add**: "Add default values for missing specs:
- Resolution: Default 1080p minimum
- Frame rate: Match original (typically 30fps)
- Export format: Default MP4, H.264 codec
- Bitrate: Minimum 8 Mbps for 1080p"

### Line 147: "If violations detected: Adjust to comply while honoring user intent"
**Expand**: "If violations detected:
1. Flag violation explicitly in output: ⚠️ [BRAND SAFETY CONCERN]
2. Explain the conflict
3. Provide compliant alternative
4. If user intent is critical and conflicts with brand, proceed with user intent but document for review"

### After line 214: Add example
**Insert**: "See Examples section below for concrete applications of this template"

### Line 303: Final paragraph
**Add after**: "**Common pitfalls to avoid:**
- Never use vague terms without quantitative backup
- Never omit timecodes (estimate if needed)
- Never leave brand changes undocumented
- Never skip the Quality Checklist verification"

---

## Summary

The 21c prompt is well-structured and comprehensive but suffers from a critical lack of examples. Addressing this gap alone would significantly improve effectiveness.

**Quick Wins:**
- Add 5 examples (highest ROI improvement)
- Define "professional" and "smooth" quantitatively
- Add edge case handling section

**Estimated Impact:**
- Current effectiveness: 7/10
- With examples + definitions: 9/10
- With all suggested improvements: 9.5/10

The foundation is strong; these improvements will make it exceptional.
