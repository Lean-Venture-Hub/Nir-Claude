---
name: create-website-from-template
description: Generate a complete clinic website from a template using CSV data or manual input. Creates content.md, selects template, generates HTML with real clinic data, images, and blog pages. Use when building a new clinic website, generating a site from a template, or creating a landing page for a dental/med spa client.
---

# Create Website From Template

Generate a complete, production-ready clinic website from a template + data source.

## Trigger

User asks to create a website for a clinic. Input can be:
- A row from a CSV file (e.g., `labeled-dentals.csv`, `outreach-leads.csv`)
- A clinic name + manual details
- A Google Maps URL

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| Clinic name | Yes | CSV `name` column or manual |
| Address | Yes | CSV `address` column or manual |
| Phone | Yes | CSV `phone` column or manual |
| Google rating | Yes | CSV `rating` column or Google Maps |
| Category | Yes | CSV `categories` column |
| Google Maps URL | Recommended | CSV `google_maps_url` column |
| Template number | Optional | User specifies (21 or 22), or auto-select |
| Language | Optional | Default: Hebrew. Can do both HE + EN |
| Reviews CSV | Optional | Pre-collected via dentist-reviews-collector skill |

---

## Step 1: Gather & Validate Data

### From CSV
Read the CSV row and extract all available fields. Map columns:
```
name → Clinic name
address → Address
city → City
phone → Phone
rating → Google rating
review_count → Review count
categories → Category
google_maps_url → Google Maps link
website → Existing website (for reference)
segment → Segment classification
```

### Check for Missing Critical Data
Flag and ask user about:
- [ ] No phone number → MUST get before proceeding
- [ ] No address → MUST get before proceeding
- [ ] No Google rating → Can scrape from Google Maps URL
- [ ] No reviews → Run dentist-reviews-collector skill first, or generate content without testimonials section
- [ ] No category → Infer from name (e.g., "מרפאת שיניים" = dental clinic)

### From Google Maps (if URL provided but data sparse)
Use `mcp__apify__call-actor` with `compass/Google-Maps-Scraper`:
```json
{
  "actor": "compass/Google-Maps-Scraper",
  "input": {
    "startUrls": [{"url": "<GOOGLE_MAPS_URL>"}],
    "maxCrawledPlacesPerSearch": 1,
    "language": "iw"
  }
}
```
Extract: name, address, phone, rating, reviewsCount, categories, openingHours.

---

## Step 2: Select Template

### Auto-Selection Logic
If user doesn't specify a template:

| Condition | Template | Reason |
|-----------|----------|--------|
| Clinic has 3+ reviews with text | 21 or 22 | Both work well with testimonials |
| Clinic has strong "About" story | 21 | Better about section layout |
| Clinic is more modern/minimalist | 22 | Cleaner visual style |
| Default | 21 | More versatile |

### Template Reference
- **Template 21**: Masonry services grid with offset cards, about section with image grid, darker color palette
- **Template 22**: Clean services grid, paragraph-based about section, outline borders on testimonials
- Both support Hebrew (RTL) and English (LTR)
- Templates location: `Dentists/templates/website/template-{N}/`

---

## Step 3: Create Folder & Content.md

### Folder Naming Convention
```
{index} - {transliterated-name}
```

**Transliteration rules** (Hebrew → Latin):
א→a, ב→b, ג→g, ד→d, ה→h, ו→v, ז→z, ח→kh, ט→t, י→y, כ→k, ל→l, מ→m, נ→n, ס→s, ע→a, פ→p, צ→tz, ק→k, ר→r, ש→sh, ת→t

- Replace spaces with `-`
- Remove quotes (`"`, `'`, `״`, `׳`)
- Lowercase everything
- Max 60 chars

**Determine index**: Check existing folders in `Dentists/reports/output/`, use next available number.

**Create folder structure:**
```
Dentists/reports/output/{index} - {name}/
├── content.md
├── index.html          (generated in Step 5)
├── blog.html           (generated in Step 6)
├── blog/               (generated in Step 6)
│   ├── sipurei-metuplim/
│   ├── briut-hapeh/
│   └── tipulim/
└── images/             (copied from template images)
```

### Generate content.md

Follow this exact format:

```markdown
# {Clinic Name Hebrew} — חבילת תוכן

## פרטי המרפאה
- **שם:** {full name}
- **שם מקוצר:** {short name}
- **רופא/ה:** {doctor name — extract from clinic name or ask user}
- **קטגוריה:** {category}
- **כתובת:** {full address}
- **טלפון:** {phone}
- **דירוג גוגל:** {rating} ({review_count} ביקורות)
- **סגמנט:** {segment}
- **Google Maps:** {url}

---

## תוכן לאתר

### Hero
- **כותרת:** {compelling headline — specific to this clinic's specialty}
- **תת-כותרת:** {subtitle with doctor name + city + value prop}

### אודות
{2-3 sentence paragraph about the clinic. Must mention doctor name, location, specialties. NOT generic.}

### שירותים
- {Service 1 — specific to this clinic's actual specialties}
- {Service 2}
- {Service 3}
- {Service 4}
- {Service 5}
- {Service 6}

---

## מאמרי בלוג

### מאמר 1: {title relevant to clinic's top service}
{3-5 sentences}

### מאמר 2: {title relevant to clinic's second service}
{3-5 sentences}

### מאמר 3: {title relevant to local area/general dental}
{3-5 sentences}

---

## ביקורות גוגל אמיתיות

- **{Reviewer Name}** ★★★★★
  > {Exact review text — NEVER fabricate reviews}
  _{timestamp}_

{Include ALL reviews with text. Skip reviews with no text.}
```

**CRITICAL RULES for content.md:**
- Hero headline must be UNIQUE to this clinic — reference their specialty or differentiator
- About paragraph must mention doctor name and city — NEVER generic
- Services must reflect what the clinic ACTUALLY does (check Google Maps categories)
- Reviews must be REAL — copy verbatim from reviews CSV or Google. NEVER invent reviews.
- If no reviews exist, omit the reviews section entirely

---

## Step 4: Copy Images

Copy template images to the website folder:
```bash
cp -r Dentists/templates/images/template-images/* "{output-folder}/images/"
```

These are generic dental images. If the clinic has specific photos (from their existing website or Google), note this for the user to replace later.

---

## Step 5: Generate HTML

Read the template HTML file: `Dentists/templates/website/template-{N}/template_example-{N}.html`

**Replace all template content with content.md data:**

| Template element | Replace with |
|-----------------|-------------|
| Hero `<h1>` spans | `כותרת` from content.md (split into 2-3 `<span class="line">` elements) |
| Hero `<p class="hero-subtitle">` | `תת-כותרת` |
| Navbar logo text | Clinic short name |
| About paragraph(s) | `אודות` text |
| About image alt | Doctor name |
| Service card titles | Service names from `שירותים` |
| Service card descriptions | Generate 1-sentence descriptions for each service |
| Service card images | Map to closest matching `service-*.jpg` |
| Testimonial cards | Reviews from content.md (name, stars, text, avatar initials) |
| CTA phone number | `טלפון` (both display and `tel:` link) |
| CTA address | `כתובת` |
| Footer clinic name | Short name |
| `<title>` | `{Clinic Name} | {Category}` |
| `<meta description>` | Generated from hero subtitle |

**Save as `{output-folder}/index.html`**

### Image path adjustment
Update all image `src` paths from `../../images/template-images/` to `images/` since the generated site has images in a local subfolder.

---

## Step 6: Generate Blog Pages

Read blog template from `Dentists/templates/website/template-{N}/blog.html` and individual article templates.

For each article in content.md:
1. Create the article HTML from the blog article template
2. Replace title, body text, clinic name
3. Save to appropriate `blog/` subfolder

Generate `blog.html` listing page linking to all articles.

---

## Step 7: Generate English Version (Optional)

If user requests English version:
1. Translate content.md to English (maintain same structure)
2. Generate `index-en.html` using the `-en.html` template variant
3. Change `dir="rtl"` → `dir="ltr"`, `lang="he"` → `lang="en"`
4. Swap font: Heebo → Inter
5. Generate English blog pages in `blog-en/`

---

## Step 8: Final Checklist

Before declaring done, verify:
- [ ] content.md has ALL fields filled (no placeholders)
- [ ] index.html renders without errors
- [ ] All images referenced exist in `images/` folder
- [ ] Phone number is formatted correctly
- [ ] No template placeholder text remains (search for "Nova Dental", "ד"ר דוגמה", "Lorem")
- [ ] Clinic name appears in: navbar, hero, about, footer, `<title>`
- [ ] Reviews are real (from content.md, not fabricated)

**Recommend running `website-from-template-audit` skill after generation to do a full visual + content verification.**

---

## Output Summary

Print to chat:
```
✅ Website generated for {Clinic Name}
📁 Folder: Dentists/reports/output/{folder-name}/
📄 Files: index.html, content.md, blog.html, 3 blog articles
🖼️ Images: {count} files in images/
⚠️ Notes: {any warnings — missing reviews, generic images, etc.}

→ Run website-from-template-audit to verify before deploying.
```

---

## Error Handling

- **CSV row has no phone**: Ask user. Do not generate without phone.
- **No reviews available**: Generate site without testimonials section. Add note in content.md.
- **Template file not found**: Check `Dentists/templates/website/` for available templates and list them.
- **Folder name collision**: Append `-2`, `-3` etc. to folder name.
- **Services too vague** (e.g., just "רופא שיניים"): Infer common services for the category and ask user to confirm.
