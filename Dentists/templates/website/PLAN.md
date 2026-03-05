# S4 Template Refactoring Plan

## Goal
All 20 templates → complete, stunning landing pages with 4 standard sections + standardized nav/footer.

## Required Sections (every template)
1. **Hero** — unique per template (the design differentiator)
2. **About** — clinic info, doctor card, address/contact details
3. **Services** — 4-6 service cards with icons
4. **Testimonials** — real Google reviews (3 cards max)
5. **Contact/CTA** — phone, address, Google Maps link
6. **Footer** — minimal: clinic name, city, copyright

## Standard Navigation
- Logo (clinic name)
- Links: אודות | שירותים | ביקורות | צור קשר
- CTA button: phone or "קבעו תור"

## Template Audit & Status

| # | Design Style | Current State | Sections | Priority | Status |
|---|---|---|---|---|---|
| 1 | Clean blue split-hero | Hero only | H | HIGH | TODO |
| 2 | Warm minimalist | Hero only | H | HIGH | TODO |
| 3 | Stats hero | Hero only | H | MED | TODO |
| 4 | Blue + service cards | Hero + Services | H,S | MED | TODO |
| 5 | Dark float cards | Hero + Services | H,S | MED | TODO |
| 6 | Bento charcoal/coral | Complete | H,A,S,T,F | LOW | FIX NAV |
| 7 | Teal gradient | Hero + Footer | H,F | HIGH | TODO |
| 8 | Grid + hours | Hero + About + Hours | H,A,Hr | MED | TODO |
| 9 | Dark elegant | Hero + Footer | H,F | MED | TODO |
| 10 | Blue corporate | Hero only | H | MED | TODO |
| 11 | Animated dark | Hero + Services | H,S,F | MED | TODO |
| 12 | Overlay cards | Hero + Services | H,S | MED | TODO |
| 13 | Bento tiles | BUGGY (empty hero) | A,S,T,F | HIGH | FIX |
| 14 | Organic blobs | Hero + Footer | H,F | MED | TODO |
| 15 | Clean corporate | Hero only | H | LOW | TODO |
| 16 | Bold gradient | BUGGY (empty secs) | H,S,T,F | HIGH | FIX |
| 17 | Warm sand/teal | Complete | H,A,S,T,CTA,F | LOW | GOLD STD |
| 18 | Dark mint gradient | Complete | H,A,S,T,C,F | LOW | FIX NAV |
| 19 | Bold geometric | Hero + Services + T | H,S,T,F | MED | ADD A,C |
| 20 | Soft rounded | Hero + Testimonials | H,T,F | MED | ADD A,S,C |

## Placeholder System
All templates use these tokens (Python script does string replacement):
- `{{CLINIC_NAME}}`, `{{DOCTOR_PREFIX}}`, `{{DOCTOR_NAME}}`, `{{CITY}}`
- `{{ADDRESS}}`, `{{PHONE}}`, `{{RATING}}`, `{{REVIEW_COUNT}}`
- `{{GOOGLE_MAPS_URL}}`
- `{{SERVICE_1_NAME}}` through `{{SERVICE_6_NAME}}`
- `{{SERVICE_1_DESC}}` through `{{SERVICE_6_DESC}}`
- `{{REVIEW_1_TEXT}}`, `{{REVIEW_1_AUTHOR}}`, `{{REVIEW_1_STARS}}` (1-3)
- Conditional blocks: `<!-- IF:PHONE -->...<!-- ENDIF:PHONE -->`
- Conditional blocks: `<!-- IF:REVIEWS -->...<!-- ENDIF:REVIEWS -->`

## Execution Order
1. Fix buggy templates (T13, T16)
2. Complete near-done templates (T6, T18, T19, T20)
3. Add sections to partial templates (T4, T5, T8, T11, T12)
4. Complete hero-only templates (T1, T2, T3, T7, T9, T10, T14, T15)
5. Standardize all nav/footer + add placeholders
6. Update Python generator to use template files
