#!/usr/bin/env python3
"""Generate English (LTR) versions of all Hebrew proposal templates."""

import os
import re
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Hebrew → English text replacements (order matters for longer strings first)
REPLACEMENTS = [
    # Title / page-level
    ('lang="he"', 'lang="en"'),
    ('dir="rtl"', 'dir="ltr"'),

    # Section titles
    ('דוח ניתוח דיגיטלי', 'Digital Analysis Report'),
    ('ניתוח דיגיטלי', 'Digital Analysis'),
    ('ניתוח מוניטין ותחזית שיפור', 'Reputation Analysis & Improvement Forecast'),
    ('השוואה מול מתחרים', 'Competitor Comparison'),
    ('מחשבון שיפור ציון', 'Rating Improvement Calculator'),
    ('איך נראה מוניטין חזק?', 'What Does Strong Reputation Look Like?'),

    # Hero / Masthead
    ('ד״ר מיטל שגב נויהוף', 'Dr. Meital Segev Neuhoff'),
    ('ד״ר מיטל שגב<br>נויהוף', 'Dr. Meital Segev<br>Neuhoff'),
    ('תל אביב', 'Tel Aviv'),
    ('פברואר 2026', 'February 2026'),
    ('גיליון מס׳ 1', 'Issue No. 1'),

    # Stats
    ('ציון Google', 'Google Rating'),
    ('ציון אתר', 'Website Score'),
    ('ביקורות חדשות (5★)', 'New Reviews (5★)'),
    ('ביקורות חדשות (5⭐)', 'New Reviews (5⭐)'),
    ('ביקורות חדשות', 'New Reviews'),
    ('הציון החדש', 'New Rating'),
    ('שיפור', 'Improvement'),
    ('ביקורות ב-Google', 'Reviews on Google'),
    ('ביקורות', 'Reviews'),
    ('היום', 'Today'),

    # Table headers / labels
    ('הזמנה אונליין', 'Online Booking'),
    ('פייסבוק', 'Facebook'),
    ('אינסטגרם', 'Instagram'),
    ('תמונות GBP', 'GBP Photos'),
    ('אתם', 'You'),
    ('אתר', 'Website'),

    # Competitor names (keep Hebrew names but provide context)
    ('מיודנט — ד״ר מקס', 'Myodent — Dr. Max'),
    ('מיודנט', 'Myodent'),
    ('ד״ר שירה חזק', 'Dr. Shira Hazak'),
    ('רופא שיניים בתל אביב', 'Dentist in Tel Aviv'),
    ('Care Laser', 'Care Laser'),  # already English

    # Callout / Alert content
    ('מיקום שלך: מקום 4 מתוך 4', 'Your Position: 4th out of 4'),
    ('לפי ביקורות. המתחרה המוביל מחזיק', 'by reviews. The leading competitor has'),
    ('— פי 31.5 ממך.', '— 31.5x more than you.'),
    ('פי 31.5 ממך', '31.5x more than you'),

    # Reputation insights
    ('ציון מצוין — אבל 24 ביקורות בלבד. מטופלים חדשים מחפשים כמות הוכחות, לא רק ציון. מרפאה עם 400+ ביקורות ו-5.0 נתפסת כאמינה בהרבה ממרפאה עם 24 ו-5.0.',
     'Excellent rating — but only 24 reviews. New patients look for volume of proof, not just score. A clinic with 400+ reviews and 5.0 is perceived as far more credible than one with 24 and 5.0.'),

    ('ציון מצוין — אבל 24 ביקורות בלבד. כמות נמוכה פוגעת באמינות ובדירוג.',
     'Excellent rating — but only 24 reviews. Low volume hurts both credibility and rankings.'),

    ('ציון מצוין', 'Excellent rating'),
    ('אבל 24 ביקורות בלבד', 'but only 24 reviews'),
    ('מטופלים חדשים מחפשים כמות הוכחות, לא רק ציון', 'New patients look for volume of proof, not just score'),
    ('הנוכחות הדיגיטלית שלך חזקה באיכות, אבל חסרה בכמות', 'Your digital presence is strong in quality, but lacking in volume'),
    ('כמות הוכחות', 'volume of proof'),

    # Urgency callout
    ('כל יום שעובר, מטופלים חדשים מחפשים רופא שיניים, רואים את מספר הביקורות, ובוחרים במתחרה.',
     'Every day that passes, new patients search for a dentist, see the review counts, and choose a competitor.'),
    ('10 ביקורות חדשות', '10 new reviews'),
    ('יכולות לשנות את התמונה', 'can change the picture'),

    ('דחיפות גבוהה:', 'High Urgency:'),
    ('הציון שלך מעולה, אבל הכמות הנמוכה שמה אותך במקום אחרון. כל חודש בלי תוכנית איסוף ביקורות — המתחרים מתרחקים.',
     'Your rating is excellent, but the low count puts you in last place. Every month without a review collection plan — competitors pull further ahead.'),
    ('עכשיו זה הזמן להגדיל כמות.', 'Now is the time to increase volume.'),

    ('הציון שלך מושלם, אבל עם 24 ביקורות בלבד אתה נראה "חדש" מול מתחרים עם מאות ביקורות. כל חודש שעובר ללא איסוף ביקורות מגדיל את הפער. מטופלים בוחרים לפי כמות ההוכחות — לא רק לפי ציון.',
     'Your rating is perfect, but with only 24 reviews you appear "new" compared to competitors with hundreds of reviews. Every month without review collection widens the gap. Patients choose by volume of proof — not just by score.'),

    ('למה חשוב לפעול עכשיו?', 'Why Act Now?'),

    # CTA
    ('רוצה לראות את הניתוח המלא?', 'Want to See the Full Analysis?'),
    ('כולל ניתוח ביקורות, מילות חיפוש, ונוכחות דיגיטלית מלאה.', 'Including review analysis, keyword research, and full digital presence audit.'),
    ('10 דקות בזום — רלוונטי?', '10 minutes on Zoom — interested?'),
    ('בואו נדבר', "Let's Talk"),

    # Footer
    ('מבוסס על נתונים ציבוריים מ-Google, easy.co.il ואתרי המרפאות', 'Based on public data from Google, easy.co.il and clinic websites'),
    ('מבוסס על נתונים ציבוריים', 'Based on public data'),

    # Calculator labels
    ('הדמיה — תוספת ביקורות חדשות בציון 5 כוכבים', 'Simulation — Adding new 5-star reviews'),

    # Alt text
    ('מרפאת שיניים — ד״ר מיטל שגב נויהוף', 'Dental Clinic — Dr. Meital Segev Neuhoff'),
    ('מרפאת שיניים מודרנית', 'Modern Dental Clinic'),

    # Misc small strings
    ('ניתוח דיגיטלי 001 /', 'Digital Analysis 001 /'),
]

# CSS direction fixes
CSS_REPLACEMENTS = [
    ('direction: rtl', 'direction: ltr'),
    ('direction:rtl', 'direction:ltr'),
    # border-right used as accent → border-left in LTR
    ('border-right: 4px solid var(--danger)', 'border-left: 4px solid var(--danger)'),
    ('border-right: 4px solid var(--accent)', 'border-left: 4px solid var(--accent)'),
    ('border-right: 4px solid var(--divider)', 'border-left: 4px solid var(--divider)'),
    ('border-right: 6px solid #6b9bd2', 'border-left: 6px solid #6b9bd2'),
    ('border-right: 6px solid var(--6b9bd2)', 'border-left: 6px solid var(--6b9bd2)'),
    ('border-right: 8px solid #8b6baf', 'border-left: 8px solid #8b6baf'),
    ('border-right: 5px solid var(--ac)', 'border-left: 5px solid var(--ac)'),
    ('border-left: 6px solid #111', 'border-left: 6px solid #111'),  # this one stays
    # text-align for labels
    ('text-align: right !important', 'text-align: left !important'),
    ('text-align:right', 'text-align:left'),
    ('padding-right: 16px !important', 'padding-left: 16px !important'),
    ('padding-right: 8px !important', 'padding-left: 8px !important'),
    # Flex start for RTL labels
    ('justify-content:flex-start', 'justify-content:flex-start'),  # stays same in LTR
]


def convert_template(filepath):
    """Convert a single Hebrew template to English."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply text replacements
    for heb, eng in REPLACEMENTS:
        content = content.replace(heb, eng)

    # Apply CSS replacements
    for old, new in CSS_REPLACEMENTS:
        content = content.replace(old, new)

    # Build output path: template-X-name.html → template-X-name-en.html
    base, ext = os.path.splitext(filepath)
    out_path = f"{base}-en{ext}"

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return out_path


def main():
    pattern = os.path.join(SCRIPT_DIR, 'template-*.html')
    files = sorted(glob.glob(pattern))

    # Skip any existing -en files
    files = [f for f in files if not f.endswith('-en.html')]

    print(f"Found {len(files)} Hebrew templates to convert:")
    for filepath in files:
        out = convert_template(filepath)
        name = os.path.basename(out)
        print(f"  Created: {name}")

    print(f"\nDone! Created {len(files)} English templates.")


if __name__ == '__main__':
    main()
