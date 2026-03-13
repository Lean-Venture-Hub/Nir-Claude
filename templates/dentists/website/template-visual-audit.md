# Template Visual Audit (T11-T15)

**TL;DR:** 4 out of 5 templates have a critical opacity:0 bug where scroll-triggered animations never fire, making services, testimonials, and/or CTA sections invisible. Template-14 is the only one that works correctly out of the box. Template-13 also uses extra template variables (STARS_HTML, INITIAL, DATE) that may not be supported.

---

## Critical Bug: Missing IntersectionObserver (affects T11, T13, T15)

Templates use CSS classes like `anim-in` or `-inner` containers with `opacity: 0`, expecting JavaScript to add a `.visible` class on scroll. **No such JavaScript exists in these files.** Result: entire sections are invisible.

### Per-Template Opacity Bug Details

| Template | Invisible Elements | Severity |
|----------|-------------------|----------|
| T11 | About content, about visual, services header, all 4 service cards, all 3 testimonial cards, CTA inner | **Critical** - 80% of page invisible |
| T12 | None | OK |
| T13 | All 4 service cards, all 3 testimonial cards, entire CTA section | **Critical** - 60% of page invisible |
| T14 | None | OK |
| T15 | services-inner, testimonials-inner, cta-inner | **Critical** - 60% of page invisible |

### Fix Required
Either:
1. Add IntersectionObserver JS to each template to toggle `.visible` on scroll
2. Or remove the `opacity: 0` from `.anim-in` / `-inner` classes and use CSS-only animations with `animation-fill-mode: both` and appropriate delays

---

## Per-Template Detailed Audit

### Template 11
- **Hero:** Properly sized, good layout with doctor photo, rating badge, CTA buttons
- **About:** INVISIBLE (opacity:0 on about-content and about-visual)
- **Services:** Section header visible but all 4 service cards INVISIBLE
- **Testimonials:** Section header visible but all 3 review cards INVISIBLE
- **CTA:** INVISIBLE (opacity:0 on cta-inner)
- **Footer:** Visible, 4-column layout, looks good
- **Broken images:** None
- **Layout quality:** Good structure when visible, RTL correct
- **Overall:** Broken due to animation bug

### Template 12
- **Hero:** Good layout with clinic photo, rating card, doctor info badges
- **About:** Visible, clean 2-column layout with doctor card and badge
- **Services:** Visible, 4-column dark card grid
- **Testimonials:** Visible, 3-column card layout with stars
- **CTA:** Visible with trust badges
- **Footer:** Minimal but functional
- **Broken images:** None
- **Layout quality:** Professional, well-structured
- **Overall:** Best template - fully functional, no issues

### Template 13
- **Hero:** Dark theme, good layout with diamond accent, checkmarks
- **About:** Visible (dark cards with avatar initial, mission statement, rating)
- **Services:** Section header visible but all 4 cards INVISIBLE (opacity:0)
- **Testimonials:** Header visible but all 3 cards INVISIBLE (opacity:0)
- **CTA:** Entire section INVISIBLE (opacity:0)
- **Footer:** Visible, dark theme consistent
- **Extra template vars:** Uses `{{REVIEW_N_STARS_HTML}}`, `{{REVIEW_N_INITIAL}}`, `{{REVIEW_N_DATE}}`, `{{DOCTOR_INITIAL}}` - these display as raw text if not supported
- **Floating Google badge:** Nice touch (bottom-left)
- **Overall:** Broken due to animation bug + extra template variables

### Template 14
- **Hero:** Purple accent theme, circular doctor photo with decorative circle
- **About:** Visible, tooth icon placeholder, stats row
- **Services:** Visible, 4-column icon grid
- **Testimonials:** Visible, 3-column card layout with star ratings
- **CTA:** Visible, purple gradient background
- **Footer:** Full 4-column layout
- **Broken images:** None
- **Layout quality:** Clean, modern purple theme
- **Overall:** Fully functional, no issues

### Template 15
- **Hero:** Green/teal accent, doctor photo, rating badge, trust badges
- **Trust bar:** 4-icon bar (leading clinic, Google, approved, Top Rated) - nice feature
- **About:** Visible, 2-column with tooth icon and stats
- **Services:** Section padding visible but all content INVISIBLE (services-inner opacity:0)
- **Testimonials:** Section padding visible but all content INVISIBLE (testimonials-inner opacity:0)
- **CTA:** Content INVISIBLE (cta-inner opacity:0)
- **Footer:** Minimal but functional
- **Overall:** Broken due to animation bug. The massive blank white areas dominate the page.

---

## Summary Table

| Template | Theme | Hero | About | Services | Reviews | CTA | Footer | Status |
|----------|-------|------|-------|----------|---------|-----|--------|--------|
| T11 | Blue/White | OK | HIDDEN | HIDDEN | HIDDEN | HIDDEN | OK | BROKEN |
| T12 | Blue/White | OK | OK | OK | OK | OK | OK | GOOD |
| T13 | Dark/Navy | OK | OK | HIDDEN | HIDDEN | HIDDEN | OK | BROKEN |
| T14 | Purple | OK | OK | OK | OK | OK | OK | GOOD |
| T15 | Green/Teal | OK | OK | HIDDEN | HIDDEN | HIDDEN | OK | BROKEN |

**Screenshots saved:** audit-t11.png through audit-t15.png (in Playwright output dir)
