---
name: template-creator
description: Create a beautiful, responsive single-file HTML website template for a specific business vertical. Uses vertical research, design playbook, animation patterns, and design trends to produce production-grade templates with placeholder content. Use when building a new template for a vertical (e.g., auto repair, landscaping, dentist) — not for filling templates with real data.
---

# Template Creator

Create stunning, production-grade single-file HTML templates for a specific business vertical. The output is a reusable template that the `create-website-from-template` skill later fills with real business data.

## Trigger

- "Create a template for [vertical]"
- "Build a new [vertical] website template"
- "Design a template for auto repair shops"
- "Make a dark/bold/minimal template for [vertical]"
- "Create template variant for [vertical]"

## Prerequisites
- `vertical-research` → `research/{vertical-name}.md` must exist
- `web-design-research` → `design-inspiration/sites.csv` must exist (run at least once)

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Vertical name | Yes | — |
| Template style/variant | No | Determined from vertical research |
| Language | No | Hebrew (RTL) |
| Dark or light | No | Determined from vertical research |

---

## Step 0: Load Context (CRITICAL — read before designing)

Read ALL of these files before writing any code:

| File | Why |
|------|-----|
| `research/{vertical}.md` | Vertical-specific: color palettes, hero patterns, sections, services, psychology, anti-patterns |
| `design-inspiration/web-design-playbook.md` | **Consolidated playbook**: typography, color, hero patterns, animation stack (GSAP/Lenis/ScrollTrigger), CSS techniques, section patterns, responsive/RTL, performance/SEO, 2026 trends, anti-patterns |
| `feedback/gallery-feedback.json` | (if exists) Gallery likes & comments — shows which templates users prefer and design direction notes |
| `feedback/sections-feedback.json` | (if exists) Section ratings & bugs — shows which section patterns work well and which have issues |

Also check existing templates for this vertical:
```
ls templates/{vertical}/website/
```
Determine the next template number (e.g., if template-22 exists, create template-23).

**If the vertical research file doesn't exist**, tell the user to run the `vertical-research` skill first.

---

## Step 0.5: Read Feedback (if available)

Check `feedback/` for `gallery-feedback.json` and `sections-feedback.json`. If either exists, read them and note:

- **Liked templates** → replicate their design patterns, color palettes, and layout approaches
- **Comments** → treat as design direction notes (e.g., "hero felt too busy" = simpler hero next time)
- **High-rated sections** (rating >= 7) → replicate those section patterns
- **Low-rated sections** (rating <= 3) → avoid those patterns or rethink them
- **Bugs** → don't repeat the same issues (e.g., if a scroll animation bug was flagged, double-check Layer 4 checklist for that pattern)

This step is optional — if no feedback files exist, skip and proceed to Step 1.

---

## Step 1: Design Decisions

Before coding, make explicit decisions for each of these. Write them as a comment block at the top of the HTML file.

### From vertical research (`research/{vertical}.md`):
- **Color palette** — pick one from the vertical's palette table
- **Hero pattern** — pick from the vertical's hero patterns list
- **Section order** — follow the vertical's "Must-Have Sections" priority order
- **Trust signals** — what Tier 1 signals to include
- **Photography style** — what the vertical's photography rules specify
- **CTA copy** — pick from the vertical's CTA patterns
- **Tone** — follow the vertical's tone of voice guidelines

### From design playbook + trends:
- **Font pairing** — pick from playbook §1 or trends §1, must match the vertical's vibe
- **Animation tier** — decide which animations to include (see Layer 4 below)
- **Effects** — which effects from the effects library (glass, gradient text, grain, etc.)

### Template identity:
- **Variant name** — descriptive (e.g., "dark-professional", "warm-community", "bold-modern")
- **Mood** — 3 adjectives that define this template's personality

Document all decisions in a design brief comment at the top of the HTML:
```html
<!--
  TEMPLATE DESIGN BRIEF
  Vertical: Auto Repair
  Variant: dark-professional
  Mood: Trustworthy, Technical, Bold
  Palette: Charcoal #1a1a1a + Red accent #E53E3E + Off-white text #f5f5f5
  Fonts: Cabinet Grotesk (display) + Inter (body)
  Hero: Full-width photo with dark overlay + trust badges
  Animation: IO reveals + GSAP hero entrance + Lenis smooth scroll
  Sections: Nav → Hero → Trust Bar → Services → About → Reviews → CTA → Footer
-->
```

---

## Step 2: Build the Template

### Architecture: Single HTML File

```
template_example-{N}.html     — Hebrew (RTL) version
template_example-{N}-en.html  — English (LTR) version (if requested)
```

Everything inline — CSS in `<style>`, JS in `<script>`, images via relative paths to shared `images/` folder.

### Required Structure

Every template MUST include these structural elements:

```html
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{Business Name} | {Primary Service} | {City}</title>
  <meta name="description" content="{SEO description with location + service}">

  <!-- Fonts — pick from design decisions -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">

  <!-- JSON-LD structured data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "{appropriate schema type from vertical}",
    "name": "{Business Name}",
    "telephone": "{phone}",
    "address": { "@type": "PostalAddress", "addressLocality": "{city}" }
  }
  </script>

  <style>/* ALL CSS */</style>
</head>
<body>
  <!-- Sections per design decisions -->

  <!-- CDN scripts (only if GSAP/Lenis animations used) -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js" defer></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js" defer></script>
  <script src="https://cdn.jsdelivr.net/npm/lenis@1/dist/lenis.min.js" defer></script>

  <script>/* ALL JS */</script>
</body>
</html>
```

---

## Step 3: Apply the 7 Craft Layers

Reference the `modern-client-web-design` skill for full details. Here's the checklist:

### Layer 1: Typography
- [ ] Display + body font pairing from design decisions
- [ ] `clamp()` sizing for all headings and body
- [ ] Hero headline: tight letter-spacing (-1px to -2px), weight 700-900
- [ ] **Hero headline word-break**: MUST include `overflow-wrap:normal;word-break:keep-all;hyphens:none` — words in hero headlines must NEVER break mid-word across lines
- [ ] **Subtitle must be a separate element**: Hero subtitle/subheading MUST be in its own `<p>` tag with smaller font size — NEVER inside the `<h1>` tag. The `<h1>` is ONLY for the main headline.
- [ ] ALL-CAPS labels: `letter-spacing: 0.1em`
- [ ] RTL: use `Heebo` for Hebrew body text, display font can stay Latin

### Layer 2: Color & Theme
- [ ] CSS custom properties for all colors in `:root`
- [ ] No pure white (#fff) text — use #f5f5f5
- [ ] No pure black (#000) bg — use #0a0a0a or warmer
- [ ] Accent color from vertical palette
- [ ] Gradient or texture treatment on hero background

### Layer 3: Hero Section
- [ ] All 6 elements: eyebrow → H1 → subtitle → CTA → social proof → visual
- [ ] CTA with `tel:` link for tap-to-call
- [ ] Hero visual matches vertical's photography rules
- [ ] `min-height: 100dvh` on hero
- [ ] Staggered load animation (GSAP timeline)

### Layer 4: Scroll Animations
- [ ] Every section has entrance animation (IO-based fade+slide)
- [ ] Hero heading: GSAP timeline reveal on load
- [ ] Cards/features: stagger reveal on scroll
- [ ] `prefers-reduced-motion` CSS guard included
- [ ] **Pinned slide pattern**: When using ScrollTrigger pin with multiple slides (stats, reviews, testimonials), EVERY slide must have an explicit fade-OUT animation when leaving its range. Never just remove a class — always `gsap.to(el, {opacity:0, duration:0.4})` on exit
- [ ] **SplitType rule**: NEVER wrap words in `<span class="word">` manually if SplitType is also called on that element. Let SplitType handle all splitting. One or the other, never both
- [ ] **Lenis + GSAP integration**: When using Lenis with GSAP, use ONLY `gsap.ticker.add((time) => lenis.raf(time * 1000))`. NEVER add a separate `requestAnimationFrame` loop — this causes double-speed scrolling
- [ ] **NEVER hide content in CSS**: Content elements MUST be visible by default (`opacity:1` or no opacity set). GSAP `.from({opacity:0})` handles the animation — it temporarily sets opacity to 0 and animates to the element's natural visible state. NEVER add `opacity:0` to CSS classes like `.gsap-fade`, `.animate`, etc. If JS fails to load, content must still be visible.
- [ ] **No `.gsap-fade{opacity:0}` pattern**: This is the #1 cause of invisible content. Instead, just use `gsap.from(el, {opacity:0, y:30})` — GSAP handles both the initial hide and the reveal. The CSS should have NO opacity manipulation.
- [ ] **Gallery iframe compatibility**: Gallery thumbnails render templates in sandboxed iframes (`sandbox="allow-same-origin"`) which blocks ALL JavaScript. If you put `opacity:0` in CSS, gallery thumbnails show blank content. This is another reason to NEVER hide content in CSS — it must be visible without JS.
- [ ] **ScrollTrigger `once: true`**: EVERY `ScrollTrigger` animation MUST include `once: true` in its config. Without it, elements re-hide when scrolling back up, making sections appear "empty." The only exception is pinned/scrub animations that are designed to play in both directions.
- [ ] **Prefer `gsap.to()` over `gsap.from()`**: Use `gsap.set()` to pre-hide elements in JS, then `gsap.to()` to reveal. This is more predictable than `gsap.from()` which can cause flash-of-content or elements snapping back to hidden state on re-trigger.
- [ ] **GSAP registerPlugin order**: `gsap.registerPlugin(ScrollTrigger)` MUST appear before ANY ScrollTrigger usage in the script, including Lenis ScrollTrigger.update references
- [ ] **z-index on overlapping slides**: When pinned sections have conclusion/summary overlays, set `zIndex:5` on the conclusion element to prevent z-fighting with exiting slides
- [ ] **Lenis ScrollTrigger sync**: After Lenis init, ALWAYS add `lenis.on('scroll', ScrollTrigger.update)` so ScrollTrigger tracks Lenis scroll position correctly
- [ ] **Lenis reduced-motion gate**: Wrap ALL Lenis initialization (new Lenis + ticker + sync) inside `if (!prefersReducedMotion)` — smooth scroll should never run for users with reduced-motion preference
- [ ] **Close all CSS rules**: Verify every CSS selector block has a closing `}`. An unclosed rule silently breaks all CSS below it

- [ ] **SplitType + gradient text**: If using SplitType on an element with gradient text (`.gradient-text`, `-webkit-background-clip:text`), you MUST re-apply the gradient styles to the generated `<span>` children after splitting. SplitType replaces the element's innerHTML, breaking the gradient.

### Layer 4b: Layout Robustness
- [ ] **Equal-height cards**: Service cards, feature cards, testimonial cards in a grid/flex row MUST all be the same height. Use `display:grid` with `grid-template-rows:subgrid` or `display:flex` with `align-items:stretch` + flex-column on cards. NEVER add manual `margin-top` offsets to stagger card positions — it breaks equal-height alignment.
- [ ] **Color theme matches vertical**: The color palette must feel appropriate for the vertical. Auto repair = industrial/mechanical (dark greys, bold accents). Dentists = clean/clinical (whites, soft blues). Landscaping = earthy/natural (greens, browns). A warm beige palette on an auto repair site reads as "realtor" — validate that colors match the vertical's vibe, not just aesthetics in isolation.

### Layer 5: Micro-Interactions
- [ ] Button hover: translateY(-2px) + shadow glow
- [ ] Nav link underline reveal
- [ ] Card hover: subtle lift + shadow
- [ ] Smooth scroll via Lenis (disabled on touch)

### Layer 6: Responsive Layout
- [ ] Mobile-first CSS
- [ ] Breakpoints: 768px (tablet), 1024px (desktop)
- [ ] Tested at 375px width (all content visible, no overflow)
- [ ] 48px minimum tap targets
- [ ] Hamburger menu on mobile
- [ ] Sticky mobile CTA (tap-to-call bar)
- [ ] CSS logical properties for RTL (`margin-inline-start`, `text-align: start`)

### Layer 7: Performance & SEO
- [ ] JSON-LD structured data (schema type from vertical)
- [ ] Semantic HTML: `<header>`, `<main>`, `<section>`, `<footer>`, `<nav>`
- [ ] Single `<h1>` with primary keyword + location
- [ ] `<meta description>` with service + location
- [ ] Images: `width`/`height` attributes, `loading="lazy"` below fold
- [ ] `fetchpriority="high"` on hero image
- [ ] Font: `font-display: swap`

---

## Step 4: Demo Content (CRITICAL — NO {{PLACEHOLDER}} TOKENS)

**Templates MUST contain real, realistic demo content — NOT `{{PLACEHOLDER}}` tokens.**

Every template must look like a complete, finished website when opened in a browser. The `create-website-from-template` skill handles search-and-replace later — but the template itself must be a fully working demo site.

**NEVER use `{{TOKEN}}` syntax in the template HTML.** If even one `{{...}}` token remains, the template is BROKEN.

### Demo content per vertical:

Each vertical has a standard demo business. Use this data directly in the HTML:

**Auto Repair:**
- Business: Precision Auto Works | Owner: Mike Rodriguez | Phone: (555) 482-7193
- Location: 4821 Commerce St, Dallas, TX 75226 | Rating: 4.9 ★ (487 reviews) | Since: 2006
- Services: Oil Changes, Brake Repair, Engine Diagnostics, Tire Services, AC & Heating, Transmission

**Dentists:**
- Business: Smile Dental Studio | Doctor: Dr. Sarah Chen | Phone: (555) 321-8765
- Location: 1250 Oak Ave, Austin, TX 78701 | Rating: 4.8 ★ (312 reviews) | Since: 2010

**Landscaping:**
- Business: Green Valley Landscaping | Owner: Tom Parker | Phone: (555) 567-2389
- Location: 890 Garden Blvd, Phoenix, AZ 85004 | Rating: 4.9 ★ (256 reviews) | Since: 2008

**Veterinarians:**
- Business: Companion Animal Hospital | Doctor: Dr. Emily Brooks | Phone: (555) 789-4561
- Location: 3200 Pet Care Dr, Denver, CO 80202 | Rating: 4.9 ★ (394 reviews) | Since: 2012

**Med Spas:**
- Business: Radiance Med Spa | Director: Dr. Lisa Park | Phone: (555) 432-9876
- Location: 1800 Beauty Ln, Miami, FL 33101 | Rating: 4.8 ★ (268 reviews) | Since: 2015

**HVAC:**
- Business: Comfort Air Solutions | Owner: Ryan Mitchell | Phone: (555) 654-3210
- Location: 5500 Climate Way, Atlanta, GA 30301 | Rating: 4.9 ★ (423 reviews) | Since: 2004

### Content requirements:
- **Business name/owner/phone/address**: Use the demo data above directly in HTML
- **Services**: 6 real services from the vertical's services taxonomy
- **Reviews**: 3 realistic testimonials with names, stars, and review text
- **About text**: 2-3 sentences about the demo business
- **Team**: 3-4 team members with names and roles
- **FAQ**: 4-6 real Q&As relevant to the vertical
- **Images**: Use paths from the shared image folder (e.g., `../../images/template-images/{name}.jpg`)

### Verification:
After creating the template, run `grep -c '{{' template_example-{N}.html` — the count MUST be **0**.

---

## Step 5: Image Strategy

### Required images (template references these paths):
```
images/
├── hero.jpg          — hero background (1920x1080)
├── about.jpg         — about section photo (800x600)
├── service-1.jpg     — service card images (600x400 each)
├── service-2.jpg
├── service-3.jpg
├── service-4.jpg
├── service-5.jpg
├── service-6.jpg
├── gallery-1.jpg     — optional gallery (800x600 each)
├── gallery-2.jpg
├── gallery-3.jpg
└── og-image.jpg      — social sharing (1200x630)
```

For the template preview, use high-quality stock images from Unsplash/Pexels that match the vertical. Include the source URLs in a comment block so they can be replaced later.

---

## Step 6: Variant Support

When creating multiple variants for the same vertical, each variant should differ in:

| Dimension | Example variants |
|-----------|-----------------|
| Color mode | Dark vs. light |
| Personality | Professional vs. friendly vs. bold |
| Hero style | Photo bg vs. split layout vs. gradient |
| Layout density | Spacious/editorial vs. compact/info-dense |
| Animation level | Minimal (IO only) vs. full (GSAP + Lenis) |

Name variants descriptively: `template-23` (dark-professional), `template-24` (warm-community).

Each variant gets its own folder under `templates/{vertical}/website/template-{N}/`.

---

## Step 7: Output & File Structure

### Create this structure (ALL items are REQUIRED):
```
templates/{vertical}/website/template-{N}/
├── template_example-{N}.html        — main website template
├── template_example-{N}-en.html     — English LTR version (if requested)
├── template-manifest.json            — placeholder token manifest (format defined in PLACEHOLDER_CONTRACT.md)
├── blog.html                         — blog listing page with 3 article cards
└── blog/                             — 3 blog article pages
    ├── {article-1-slug}/index.html
    ├── {article-2-slug}/index.html
    └── {article-3-slug}/index.html
```

### template-manifest.json
Generate this file alongside the HTML. It lists every `{{PLACEHOLDER}}` token used in the template, its location (CSS selector or line context), and expected data type. See `templates/PLACEHOLDER_CONTRACT.md` for the exact format.

Images go in the shared `templates/{vertical}/images/` folder (or reference existing images if available).

### Blog & Demo Content (REQUIRED)

Every template MUST include a blog listing page and 3 blog posts with real demo content. Blog pages must match the template's exact visual design (colors, fonts, nav, footer).

**blog.html — Blog listing page:**
- Same nav and footer as main template (exact copy of HTML + CSS)
- Hero section with "Tips & Advice" or similar title
- 3 article cards: image, title, excerpt, "Read More" link
- Responsive grid layout
- Image paths: `../../images/template-images/{name}.jpg`

**Blog post pages — 3 articles (~800 words each):**
- Same nav and footer as main template
- Article hero with background image + dark overlay
- Breadcrumb: Home > Blog > Article Title
- Full article body with subheadings, lists, proper typography
- Author info section (owner name + title from placeholder data)
- Related articles section linking to the other 2 posts
- Image paths from blog post: `../../../../images/template-images/{name}.jpg`
- Each file is standalone (all CSS inline), under 15KB

**Blog topics by vertical:**

| Vertical | Article 1 | Article 2 | Article 3 |
|----------|-----------|-----------|-----------|
| auto-repair | Oil Change Guide | Brake Warning Signs | Check Engine Light |
| dentists | Dental Implants Guide | Teeth Whitening Options | When to See Emergency Dentist |
| landscaping | Lawn Care Seasonal Guide | Hardscaping vs Softscaping | Drought-Resistant Landscaping |
| veterinarians | Pet Vaccination Schedule | Signs Your Pet Needs Vet | Pet Nutrition Guide |
| med-spas | Botox vs Fillers Guide | Skin Care Routine by Age | Recovery After Laser Treatment |
| hvac | AC Maintenance Tips | When to Replace Your Furnace | Indoor Air Quality Guide |

For new verticals not listed, create 3 relevant educational articles that demonstrate expertise and help with SEO.

---

## Step 8: Self-Review

Before delivering, verify:

### Demo content check (BLOCKING — do this FIRST):
- [ ] Run `grep -c '{{' template_example-{N}.html` — MUST return **0**
- [ ] Business name, phone, address are real demo values (not placeholder tokens)
- [ ] Reviews have real names and text (not "Customer Name" or "Review Text")
- [ ] Services have real names (not "Service 1", "Service 2")
- [ ] About section has real paragraph text
- [ ] If count > 0: FIX immediately before proceeding

### Main template (open in Playwright at 1440x900 + 375x812):
- [ ] All sections render correctly
- [ ] Animations fire on scroll
- [ ] Hero looks complete with all 6 elements
- [ ] No horizontal overflow
- [ ] Colors match design brief
- [ ] Hamburger menu works on mobile
- [ ] All content is readable on mobile
- [ ] CTA is accessible (sticky bar or prominent button)

### Blog pages:
- [ ] blog.html exists with 3 article cards
- [ ] 3 blog post folders exist with index.html each
- [ ] Nav and footer match main template exactly
- [ ] Colors, fonts, spacing match main template
- [ ] Image paths are correct (relative to file location)
- [ ] Articles have real, useful content (~800 words each)
- [ ] Related articles link to the other 2 posts
- [ ] Mobile responsive

### Take screenshots:
- Desktop hero → `audit-screenshots/template_example-{N}-desktop.png`
- Mobile hero → `audit-screenshots/template_example-{N}-mobile.png`

---

## Output Summary

Print to chat:
```
Template created for {Vertical} — variant: {variant-name}

📁 templates/{vertical}/website/template-{N}/
📄 template_example-{N}.html (Hebrew RTL)

Design: {3-word mood} | {palette description} | {font pairing}
Sections: {list of sections included}
Animations: {animation tier summary}

Screenshots saved for review.
```

---

## Error Handling

- **No vertical research file**: Stop. Tell user to run `vertical-research` skill first.
- **Existing template number conflict**: Auto-increment to next available number.
- **User wants a style not in vertical research**: Adapt — use the vertical's content/sections but apply the requested style from the design playbook.
- **Template too large (>200KB HTML)**: Optimize — inline SVGs may need to be external, reduce animation code.
- **Playwright not available for review**: Skip self-review step, note it in output.
