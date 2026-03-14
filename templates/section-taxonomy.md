# Section Taxonomy — All Templates

**TL;DR:** Across 22 dentist and 16 auto-repair templates, there are 5 universal sections (hero, about, services, testimonials/reviews, CTA/contact) plus 10+ vertical-specific sections. Auto-repair has significantly more section variety (blog, why-us, stats, trust bars, process, map).

---

## Universal Sections (both verticals)

| Section Class | ID | Dentists (22 templates) | Auto-Repair (16 templates) | Notes |
|---|---|---|---|---|
| `hero` | hero/home/- | 22/22 (100%) | 16/16 (100%) | Variants: `hero-bento` (D-13), `chapter-hero` (AR-14), `hero-wrap` (AR-10) |
| `about` | about/team | 21/22 (95%) | 16/16 (100%) | Missing in D-6. Variant: `chapter-about` (AR-14) |
| `services` | services | 22/22 (100%) | 16/16 (100%) | Variants: `services-section` (D-6), `features` (D-18), `services-wrap` (AR-10), `chapter-services` (AR-14), `specs` (AR-5) |
| `testimonials` / `reviews` | testimonials/reviews | 22/22 (100%) | 16/16 (100%) | Dentists use `testimonials`; Auto-repair uses `reviews`. Variants: `testimonials-section` (D-6), `chapter-reviews` (AR-14) |
| CTA/Contact | contact | 22/22 (100%) | 16/16 (100%) | Classes vary: `cta-section` (most common), `cta-banner`, `contact`, `contact-cta`, `cta`, `cta-map`, `contact-wrap`, `chapter-cta` |

## Dentist-Only Sections

| Section Class | Templates | Count |
|---|---|---|
| `stats-bar` | D-12 | 1 |
| `mid-section` | D-11 | 1 |
| `cta-banner animate-on-scroll` | D-16 | 1 |

## Auto-Repair-Only Sections

| Section Class | ID | Templates | Count |
|---|---|---|---|
| `blog` / `blog-preview` / `blog-section` | blog | AR-1,2,3,4,5,7,8,9,10,11,12,13,15,16 | 14/16 (88%) |
| `why` / `bento` | why | AR-2,5,11,12,13,15 | 6/16 (38%) |
| `trust-bar` | - | AR-1,3,11 | 3/16 (19%) |
| `stats-bar` / `stats-section` / `stats` / `chapter-stats` | stats/problem | AR-2,4,5,14 | 4/16 (25%) |
| `certs` | - | AR-4 | 1 |
| `transparency` (process) | process | AR-4,10 | 2/16 (13%) |
| `specials` | specials | AR-2 | 1 |
| `map-section` | - | AR-13 | 1 |
| `features` | features | AR-16 | 1 |

## Nav Variants

| Class | Vertical | Count |
|---|---|---|
| `nav` | Both | Most common (D: 10, AR: 9) |
| `navbar` | Both | D: 2 (D-9, D-21), AR: 1 (AR-8) |
| (no class) | Dentists | 5 (D-4,12,14,15,19,20) |
| `floating-nav` | Auto-repair | 2 (AR-9, AR-10) |
| `hero-nav` | Dentists | 1 (D-18) |
| `header-nav` + `mobile-menu` | Auto-repair | 2 (AR-10, AR-12) |

## Footer Variants

| Class | Dentists | Auto-Repair |
|---|---|---|
| `footer` | 18/22 | 14/16 |
| (no class) | 4/22 (D-14,19,20,22) | 1/16 (AR-7) |

## Section Order (canonical)

**Dentists:** nav > hero > about > services > testimonials > cta/contact > footer

**Auto-Repair:** nav > hero > [trust-bar] > [stats] > services > about > reviews > [why] > [blog] > cta/contact > [map] > footer

Key difference: auto-repair often puts services BEFORE about, and has blog + why-us sections that dentists lack.

## Animation Modifiers (CSS classes on sections)

| Modifier | Templates |
|---|---|
| `reveal` | D-2, D-9 |
| `fade-in` | D-21 |
| `animate-on-scroll` | D-16 |
| `gs-hidden` (GSAP) | AR-1 |
| `section-pad` | AR-15 |
