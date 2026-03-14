## TL;DR

8 templates had scroll/animation bugs across 2 verticals. All stem from 5 recurring patterns that the template-creator skill doesn't guard against and the audit skill doesn't check for. Below: exact additions to each skill.

---

## Template-Creator Skill — Additions to Layer 4 (Scroll Animations)

Add these mandatory rules after the existing Layer 4 checklist (line ~176 in SKILL.md):

### New checklist items for Layer 4:

```markdown
### Layer 4: Scroll Animations (continued — MANDATORY guards)

- [ ] **Pinned slide pattern**: When using ScrollTrigger pin with multiple slides (stats, reviews, testimonials), EVERY slide must have an explicit fade-OUT animation when leaving its range. Never just remove a class — always `gsap.to(el, {opacity:0, duration:0.4})` on exit
- [ ] **SplitType rule**: NEVER wrap words in `<span class="word">` manually if SplitType is also called on that element. Let SplitType handle all splitting. One or the other, never both
- [ ] **Lenis + GSAP integration**: When using Lenis with GSAP, use ONLY `gsap.ticker.add((time) => lenis.raf(time * 1000))`. NEVER add a separate `requestAnimationFrame` loop — this causes double-speed scrolling
- [ ] **Initial hidden state contract**: If an element starts at `opacity:0` in CSS and relies on JS to reveal it, the `@media(prefers-reduced-motion:reduce)` block MUST include that element with `opacity:1!important;transform:none!important`
- [ ] **CSS .visible pattern**: If using IntersectionObserver to add `.visible` class, the element CSS MUST start at `opacity:0;transform:translateY(30px)` and a `.visible` rule MUST exist with `opacity:1;transform:translateY(0)`. Never start at `opacity:1` — scroll reveal becomes a no-op
- [ ] **Animation initial state**: Elements with CSS animations (e.g., `fadeInUp`) MUST start at `opacity:0`, not `opacity:1`. Starting at 1 causes a flash before the animation kicks in
- [ ] **GSAP registerPlugin order**: `gsap.registerPlugin(ScrollTrigger)` MUST appear before ANY ScrollTrigger usage in the script, including Lenis ScrollTrigger.update references
- [ ] **z-index on overlapping slides**: When pinned sections have conclusion/summary overlays, set `zIndex:5` on the conclusion element to prevent z-fighting with exiting slides
```

---

## Audit Skill — Additions to Step 3e (Scroll & Animation Check)

Replace the current 3e section (lines 137-143 in SKILL.md) with this expanded version:

```markdown
### 3e: Scroll & Animation Check (CRITICAL — must catch all patterns)

Use Playwright to scroll through the full page and verify animations work correctly.

**Basic scroll checks:**
- [ ] `.reveal` / `.animate-on-scroll` elements become `.visible` on scroll
- [ ] No layout jumps or shifts during scroll
- [ ] Lazy-loaded images load when scrolled into view
- [ ] Navbar becomes fixed/frosted on scroll

**Pinned section checks (stats, reviews, testimonials with ScrollTrigger pin):**
- [ ] Scroll through each pinned section slowly — each slide must appear AND disappear cleanly
- [ ] No overlapping text between slides at any scroll position
- [ ] Conclusion/summary slide appears only after all slides have exited
- [ ] Take a screenshot mid-transition between slides to verify no overlap

**Animation code audit (read the JS, not just visual):**
- [ ] If SplitType is used, verify no manual `<span class="word">` wrappers exist on the same element
- [ ] If Lenis is used, verify only ONE raf integration exists (gsap.ticker.add OR requestAnimationFrame, never both)
- [ ] If elements have `opacity:0` in CSS, verify they're included in `@media(prefers-reduced-motion:reduce)` overrides
- [ ] If `.visible` class is added by JS observer, verify `.visible` CSS rule exists AND initial state is `opacity:0`
- [ ] If CSS animation classes (e.g., `.anim-in`) exist, verify initial `opacity` is `0` not `1`
- [ ] Verify `gsap.registerPlugin(ScrollTrigger)` appears before any ScrollTrigger usage

**Overlap detection (automated):**
Run this Playwright evaluate at multiple scroll positions through pinned sections:
```js
// Check for overlapping visible text elements in pinned sections
const visible = [...document.querySelectorAll('.stat-slide, .review-slide, [class*="slide"]')]
  .filter(el => getComputedStyle(el).opacity > 0.5);
if (visible.length > 1) console.error('OVERLAP: multiple slides visible simultaneously');
```
```

---

## Severity Addition

Add to the audit skill's Severity Levels section:

```markdown
- **CRITICAL:** ... overlapping content in pinned scroll sections, scroll animations that never trigger (opacity:1 initial state with .visible pattern)
```
