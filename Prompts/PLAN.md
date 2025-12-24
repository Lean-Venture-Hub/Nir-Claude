# Current PLAN – Ad Creative Quality Improvement Initiative

## Phase 1 Status: ✅ COMPLETE (2025-12-23)

| Step | Agent(s) | Status | Output File | Verification |
|------|----------|--------|-------------|--------------|
| 1 | orchestrator | ✅ Completed | /Prompts/research/creative-quality-diagnosis.md | orchestrator |
| 2 | orchestrator | ✅ Completed | /Prompts/research/creative-improvement-playbook.md | critic |
| 3 | claude | ✅ Completed | /Prompts/22 Creative Divergence Engine.md | user testing |
| 4 | claude | ✅ Completed | Enhanced /Prompts/14 Brief Creator.md (Hook Innovation Lab) | user testing |
| 5 | claude | ✅ Completed | Enhanced /Prompts/17 Template Generation Prompt.md (Surprise Mandate) | user testing |
| 6 | claude | ✅ Completed | Enhanced /Prompts/20 analyze ad output.md (Creativity Audits) | user testing |
| 7 | claude | ✅ Completed | /Prompts/research/generic-patterns-to-avoid.md | reference |
| 8 | claude | ✅ Completed | /Prompts/research/prompt-changes.md | documentation |

## Problem Statement

ScaleFox's current ad pipeline (Brief Creator #14 → Template Generation #17) produces ads that are too generic and obvious. The competitive intelligence value is being diluted by formulaic creative execution.

## Root Cause Analysis

**Where creativity is lost:**
1. Brief Creator (#14) - Over-systematized with 10+ frameworks creating pattern convergence
2. Template Generation (#17) - Temperature control is insufficient; focuses on compliance over originality
3. Missing creative divergence stage between brief and template
4. No mechanism to inject unexpected angles beyond "rare angles" section
5. PRISM humanization layer exists but doesn't prevent generic visual execution

## Strategic Approaches (Multi-Pronged)

### Approach A: Creative Divergence Engine (NEW PROMPT)
**Insert between Brief Creator and Template Generation**
- Takes briefs as input
- Generates 3-5 wildly different visual concepts per brief
- Uses lateral thinking, metaphors, unexpected juxtapositions
- Output: Rich visual concept descriptions (not templates yet)

### Approach B: Hook Innovation Lab (ENHANCE EXISTING)
**Upgrade Brief Creator's "Rare Angles" section**
- Create dedicated sub-prompt focused purely on non-obvious hooks
- Use techniques: analogical reasoning, pattern inversion, cultural references, data storytelling
- Separate temperature control for hook generation (can run hot while brief stays precise)

### Approach C: Visual Concept Architect (NEW PROMPT)
**Pre-template visual ideation stage**
- Analyzes brief + competitive insights
- Generates unexpected visual metaphors and composition ideas
- Uses AI image analysis of top-performing unconventional ads
- Output: Visual concept library to inform template generation

### Approach D: Template Generation Overhaul (MAJOR REVISION)
**Enhance Prompt #17 with:**
- Split temperature into 3 axes: Layout (0-1), Color (0-1), Concept (0-1)
- Add "creative constraint removal" mode
- Inject unexpected visual elements library
- Reference visual concept architect outputs

### Approach E: Two-Track Brief System (ARCHITECTURE CHANGE)
**Parallel brief generation:**
- Track 1: Current systematic approach (safe, proven)
- Track 2: Experimental track with loosened constraints
- User selects balance or A/B tests both

## Quick Wins (Immediate Impact)

1. Add "visual surprise requirement" to Template Generation prompt
2. Expand Rare Angles section in Brief Creator with 10+ contrarian thinking techniques
3. Create negative example library of "generic ad patterns to avoid"
4. Inject "one unexpected element" mandate in every ad

## Implementation Priority

**Phase 1 (This Week):**
- Step 1-2: Diagnosis and playbook (analysis)
- Step 3: Creative Divergence Engine prompt
- Step 4: Hook Innovation Lab enhancement

**Phase 2 (Next Week):**
- Step 5: Visual Concept Architect prompt
- Step 6: Integration strategy

**Phase 3 (Following Week):**
- Template Generation overhaul
- Two-track system architecture

## Success Metrics

- Ads score >4/5 on "Originality" dimension (currently in prompt #20)
- Ads score >4/5 on "Non-Obvious" dimension (currently in prompt #20)
- User feedback: "less generic" qualitative assessment
- A/B test: new creative approach vs. current pipeline CTR comparison

---

## Phase 1 Completion Summary (2025-12-23)

### What Was Delivered

**New Prompts:**
1. **22 Creative Divergence Engine.md** (~3.5KB)
   - NEW prompt that sits between Brief Creator (#14) and Template Generation (#17)
   - Generates 3-5 wildly different visual concepts using 10 contrarian techniques
   - Outputs divergent concepts with surprise scores for user selection

**Enhanced Prompts:**
2. **14 Brief Creator.md** - Hook Innovation Lab
   - Expanded "Rare Angles" section with 10 contrarian techniques
   - Added "Hook Innovation Modes" combining techniques
   - Hook temperature check (Cold → Warm → Hot)

3. **17 Template Generation Prompt.md** - Surprise Mandate
   - Added surprise element requirement to Success Criteria
   - New "Surprise Mandate" section with 10 approved techniques
   - Temperature-scaled implementation
   - Updated audit checklist

4. **20 analyze ad output.md** - Creativity Audits
   - Added "Creativity Audit Deep Checks" section
   - Detailed Originality and Non-Obvious assessment scales
   - Generic pattern detection
   - Creativity failure modes

**Reference Files:**
5. **research/generic-patterns-to-avoid.md** (~5KB)
   - 20 most overused B2B ad patterns (visual, composition, copy clichés)
   - 6 audit tests (Swap, Stock Photo, Competitor, etc.)
   - Creative quality tiers
   - Replacement philosophy

6. **research/prompt-changes.md** (~4.3KB)
   - Comprehensive specification of all changes
   - Before/after examples
   - Implementation roadmap
   - Success metrics and rollback plan

### Workflow Changes

**Before:**
Brief Creator (#14) → Template Generation (#17)

**After:**
Brief Creator (#14) → **Creative Divergence Engine (#22)** → [User selects concept] → Template Generation (#17)

**Fast Path Option:** Users can skip #22 for speed over creativity

### Expected Impact

- **Originality:** Target ≥4/5 on 80% of concepts
- **Non-Obvious:** Target ≥4/5 on 60% of concepts
- **Pattern Avoidance:** Zero usage of 20 generic patterns
- **Differentiation:** 3-5 wildly different concepts per brief (vs 6 similar)

### Next Actions Required

1. **User Testing (THIS WEEK)**
   - Test new workflow with 5-10 sample briefs
   - Different industries to validate versatility
   - Measure before/after originality scores
   - Gather user feedback on creative quality

2. **Phase 2 Decision (NEXT WEEK)**
   - If Phase 1 results are strong: maintain and optimize
   - If more improvement needed: proceed with Phase 2
     * Visual Concept Architect (Prompt #24)
     * Multi-axis temperature system
     * Two-track brief architecture

3. **Documentation**
   - Update main CLAUDE.md with new prompt #22
   - Add workflow diagram showing new creative stage
   - Create user guide for when to use divergent concepts vs fast path

### Files Modified

- ✅ `22 Creative Divergence Engine.md` - NEW
- ✅ `14 Brief Creator.md` - ENHANCED
- ✅ `17 Template Generation Prompt.md` - ENHANCED
- ✅ `20 analyze ad output.md` - ENHANCED
- ✅ `research/generic-patterns-to-avoid.md` - NEW
- ✅ `research/prompt-changes.md` - NEW
- ✅ `PLAN.md` - UPDATED
- ✅ `progress-log.md` - UPDATED
