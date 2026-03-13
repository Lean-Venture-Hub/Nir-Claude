# Placeholder Contract

**Purpose:** Defines exact placeholder tokens used in all website templates. `template-creator` inserts these; `create-website-from-template` replaces them with real data.

## Format

All placeholders use double curly braces: `{{FIELD_NAME}}`
- SCREAMING_SNAKE_CASE
- No spaces inside braces
- Every placeholder must appear in this contract

## Required Placeholders

### Business Identity
| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{BUSINESS_NAME}}` | Full business name | מוסך אלון, Nova Dental |
| `{{BUSINESS_NAME_SHORT}}` | Short/logo name | אלון, Nova |
| `{{OWNER_NAME}}` | Owner/doctor name with title | ד״ר מיכל לוי, John Smith |
| `{{PHONE}}` | Phone number (displayed) | 077-000-0000 |
| `{{PHONE_TEL}}` | Phone for tel: link | +972770000000 |
| `{{ADDRESS}}` | Full address | רחוב הרצל 42, תל אביב |
| `{{CITY}}` | City name | תל אביב, Houston |
| `{{GOOGLE_MAPS_URL}}` | Google Maps link | https://maps.google.com/... |
| `{{GOOGLE_RATING}}` | Star rating | 4.8 |
| `{{REVIEW_COUNT}}` | Number of reviews | 127 |

### Content
| Placeholder | Description |
|-------------|-------------|
| `{{HERO_HEADLINE}}` | Main hero H1 text |
| `{{HERO_SUBTITLE}}` | Hero subheadline |
| `{{HERO_EYEBROW}}` | Small label above headline |
| `{{ABOUT_TEXT}}` | About section paragraph(s) |
| `{{CTA_TEXT}}` | Primary CTA button text |

### Services (repeat pattern for 1-6)
| Placeholder | Description |
|-------------|-------------|
| `{{SERVICE_1_TITLE}}` | Service name |
| `{{SERVICE_1_DESC}}` | 1-sentence description |
| `{{SERVICE_1_IMAGE}}` | Image filename |
| ... through `{{SERVICE_6_*}}` | |

### Reviews (repeat pattern for 1-5)
| Placeholder | Description |
|-------------|-------------|
| `{{REVIEW_1_NAME}}` | Reviewer name |
| `{{REVIEW_1_TEXT}}` | Review text |
| `{{REVIEW_1_STARS}}` | Star count (1-5) |
| `{{REVIEW_1_DATE}}` | Review date |
| ... through `{{REVIEW_5_*}}` | |

### SEO & Meta
| Placeholder | Description |
|-------------|-------------|
| `{{META_TITLE}}` | Page title tag |
| `{{META_DESCRIPTION}}` | Meta description |
| `{{SCHEMA_TYPE}}` | JSON-LD @type (MedicalClinic, AutoRepair, etc.) |
| `{{OG_IMAGE}}` | Open Graph image path |

### Images
| Placeholder | Description | Dimensions |
|-------------|-------------|------------|
| `{{HERO_IMAGE}}` | Hero background | 1920x1080 |
| `{{ABOUT_IMAGE}}` | About section photo | 800x600 |
| `{{SERVICE_N_IMAGE}}` | Service card images | 600x400 |

## Rules

1. Templates MUST use these exact placeholders — no variations
2. `create-website-from-template` does string replacement of all `{{*}}` tokens
3. If a section is optional (e.g., reviews), use `{{REVIEW_1_NAME}}` etc. — the filling skill removes the entire section if no reviews exist
4. Images use relative paths: `images/hero.jpg`, `images/service-1.jpg`
5. For Hebrew templates, placeholder VALUES are in Hebrew but placeholder KEYS are always English

## Template Manifest

Every template should include a `template-manifest.json` alongside the HTML:

```json
{
  "id": 23,
  "name": "Dark Professional",
  "vertical": "auto-repair",
  "variant": "dark-professional",
  "language": "he",
  "has_english": true,
  "schema_type": "AutoRepair",
  "sections": ["nav", "hero", "trust-bar", "services", "about", "reviews", "cta", "footer"],
  "placeholders": ["BUSINESS_NAME", "PHONE", "...all used placeholders"],
  "images_required": ["hero.jpg", "about.jpg", "service-1.jpg", "..."],
  "fonts": ["Cabinet Grotesk", "Inter"],
  "color_mode": "dark"
}
```
