#!/usr/bin/env python3
"""Generate template_example-N.html files with realistic Hebrew dental clinic content."""

import os, re, glob

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Realistic fake clinic data ──────────────────────────────────────
DATA = {
    # Core
    "CLINIC_NAME": "מרפאת חיוך פלוס",
    "DOCTOR_PREFIX": "ד״ר",
    "DOCTOR_NAME": "מיכל לוי",
    "DOCTOR_INITIAL": "מ",
    "DOCTOR_SPECIALTY": "רפואת שיניים אסתטית ושיקומית",
    "CITY": "תל אביב",
    "ADDRESS": "רוטשילד 45",
    "PHONE": "03-555-1234",
    "EMAIL": "info@smileplus.co.il",
    "GOOGLE_MAPS_URL": "#",
    "LOGO_LETTER": "ח",

    # Rating
    "RATING": "4.9",
    "REVIEW_COUNT": "187",

    # Hero variants
    "HERO_TITLE": "חיוך שמשנה את הכל — מתחיל כאן",
    "HERO_SUBTITLE": "מרפאת שיניים מתקדמת בלב תל אביב. טיפולים אסתטיים ושיקומיים בגישה אישית וחמה.",
    "HERO_DESCRIPTION": "מרפאת שיניים מתקדמת בלב תל אביב. טיפולים אסתטיים ושיקומיים בגישה אישית וחמה.",
    "HERO_BADGE_TEXT": "מומחים לחיוך מושלם",
    "HERO_TAG": "מרפאת שיניים מובילה בתל אביב",
    "HERO_LINE_1": "חיוך שמשנה",
    "HERO_LINE_2": "את הכל",
    "HERO_LINE_3": "מתחיל כאן",
    "HERO_HEADLINE_1": "חיוך שמשנה",
    "HERO_HEADLINE_2": "את הכל",
    "HERO_HEADLINE_HIGHLIGHT": "מתחיל כאן",
    "HEADLINE": "חיוך מושלם מתחיל בטיפול נכון",
    "HEADLINE_1": "חיוך",
    "HEADLINE_2": "מושלם",
    "HEADLINE_3": "מתחיל כאן",
    "TAGLINE": "מרפאת שיניים מובילה בתל אביב",

    # About
    "ABOUT_TEXT": "מרפאת חיוך פלוס הוקמה ב-2012 מתוך חזון ליצור חוויית טיפול שיניים שונה לחלוטין. אנחנו מאמינים שכל מטופל ראוי לטיפול ברמה הגבוהה ביותר, בסביבה נעימה ומרגיעה. הצוות שלנו משלב מומחיות רפואית עם טכנולוגיה מתקדמת כדי להעניק לכם את החיוך שתמיד חלמתם עליו.",
    "ABOUT_HEADING": "אודות המרפאה",
    "ABOUT_BULLET_1": "ניסיון של למעלה מ-12 שנה ברפואת שיניים",
    "ABOUT_BULLET_2": "טכנולוגיה דיגיטלית מתקדמת",
    "ABOUT_BULLET_3": "גישה אישית וחמה לכל מטופל",
    "MISSION_TEXT": "המטרה שלנו פשוטה — לתת לכם סיבה לחייך בביטחון מלא, כל יום מחדש.",

    # Images
    "HERO_IMAGE": "images/image2.png",
    "HERO_IMAGE_ALT": "מרפאת חיוך פלוס — תל אביב",
    "ABOUT_IMAGE": "images/image7.png",
    "ABOUT_IMAGE_ALT": "ד״ר מיכל לוי — מרפאת חיוך פלוס",
    "DOCTOR_IMAGE": "images/image9.png",

    # Features
    "FEATURE_1": "טכנולוגיה מתקדמת",
    "FEATURE_2": "גישה אישית",
    "EXPLORE_LABEL": "גלו את השירותים שלנו",

    # CTA variants
    "CTA_LABEL": "קבעו תור עכשיו",
    "CTA_BUTTON_TEXT": "קבעו תור עכשיו",
    "CTA_PRIMARY_TEXT": "קבעו תור עכשיו",
    "CTA_SECONDARY_TEXT": "דברו איתנו",
    "CTA_TEXT": "קבעו תור עכשיו",
    "CTA_HEADING": "מוכנים לחיוך חדש?",
    "CTA_SUBTITLE": "צרו איתנו קשר לתיאום פגישת ייעוץ ראשונית ללא התחייבות.",
    "CTA_CONTACT_TEXT": "צרו קשר",
    "BADGE_TEXT": "● קבעו תור ● קבעו תור ",

    # Contact
    "CONTACT_TITLE": "מוכנים לחיוך חדש?",
    "CONTACT_SUBTITLE": "צרו איתנו קשר לתיאום פגישת ייעוץ ראשונית ללא התחייבות.",
    "CONTACT_LABEL": "צור קשר",

    # Services
    "SERVICES_TITLE": "השירותים שלנו",
    "SERVICES_SUBTITLE": "מגוון טיפולי שיניים מתקדמים בגישה מקצועית ואישית",
    "SERVICES_LABEL": "שירותים",
    "SERVICE_1_NAME": "הלבנת שיניים",
    "SERVICE_1_DESC": "טיפולי הלבנה מתקדמים להשגת חיוך לבן וזוהר תוך שמירה על בריאות השן.",
    "SERVICE_2_NAME": "ציפויי חרסינה",
    "SERVICE_2_DESC": "ציפויים אסתטיים המותאמים אישית לעיצוב חיוך מושלם ותוצאה טבעית.",
    "SERVICE_3_NAME": "השתלות שיניים",
    "SERVICE_3_DESC": "פתרון קבוע ואיכותי לשיניים חסרות, בטכנולוגיה מתקדמת ודיוק מרבי.",
    "SERVICE_4_NAME": "יישור שיניים שקוף",
    "SERVICE_4_DESC": "טיפולי יישור בשיטת אינויזליין לתוצאות מצוינות ללא גשר מתכתי.",
    "SERVICE_5_NAME": "טיפולי שורש",
    "SERVICE_5_DESC": "טיפולים מדויקים להצלת שיניים פגועות בטכנולוגיה חדשנית.",
    "SERVICE_6_NAME": "רפואת חניכיים",
    "SERVICE_6_DESC": "אבחון וטיפול במחלות חניכיים לשמירה על בריאות הפה ארוכת טווח.",

    # Stats
    "STAT_1_NUMBER": "12+",
    "STAT_1_LABEL": "שנות ניסיון",
    "STAT_2_NUMBER": "4,800+",
    "STAT_2_LABEL": "מטופלים מרוצים",
    "STAT_3_NUMBER": "4.9",
    "STAT_3_LABEL": "דירוג ב-Google",
    "STAT_4_NUMBER": "15K+",
    "STAT_4_LABEL": "טיפולים בוצעו",
    "EXPERIENCE_YEARS": "12",
    "EXPERIENCE_LABEL": "שנות ניסיון",
    "HAPPY_PATIENTS_COUNT": "4,800+",
    "HAPPY_PATIENTS_TEXT": "מטופלים מרוצים",

    # Reviews
    "TESTIMONIALS_TITLE": "מה המטופלים שלנו אומרים",
    "TESTIMONIALS_LABEL": "ביקורות",

    "REVIEW_1_TEXT": "ד״ר לוי שינתה לי את החיים. אחרי שנים שנמנעתי מלחייך, עברתי טיפול הלבנה וציפויים — התוצאה מדהימה. הצוות מקצועי, חם ומפנק. ממליצה בחום!",
    "REVIEW_1_AUTHOR": "נועה כהן",
    "REVIEW_1_INITIAL": "נ",
    "REVIEW_1_AUTHOR_INITIAL": "נ",
    "REVIEW_1_DATE": "לפני חודש",
    "REVIEW_1_ROLE": "מטופלת",
    "REVIEW_1_TREATMENT": "הלבנת שיניים",
    "REVIEW_1_STARS_HTML": "&#9733;&#9733;&#9733;&#9733;&#9733;",

    "REVIEW_2_TEXT": "עברתי השתלת שיניים במרפאה — מהייעוץ הראשוני ועד לתוצאה הסופית, הכל היה ברמה הגבוהה ביותר. ד״ר לוי מסבירה כל שלב ועושה הכל בסבלנות.",
    "REVIEW_2_AUTHOR": "יוסי אברהם",
    "REVIEW_2_INITIAL": "י",
    "REVIEW_2_AUTHOR_INITIAL": "י",
    "REVIEW_2_DATE": "לפני שבועיים",
    "REVIEW_2_ROLE": "מטופל",
    "REVIEW_2_TREATMENT": "השתלת שיניים",
    "REVIEW_2_STARS_HTML": "&#9733;&#9733;&#9733;&#9733;&#9733;",

    "REVIEW_3_TEXT": "מקום מדהים! הגעתי בפעם הראשונה לטיפול שורש ומאז אני מטופלת קבועה. האווירה נעימה, הצוות מדהים, והטיפול ברמה אחרת לגמרי. תודה רבה!",
    "REVIEW_3_AUTHOR": "שירה דויד",
    "REVIEW_3_INITIAL": "ש",
    "REVIEW_3_AUTHOR_INITIAL": "ש",
    "REVIEW_3_DATE": "לפני 3 חודשים",
    "REVIEW_3_ROLE": "מטופלת",
    "REVIEW_3_TREATMENT": "טיפול שורש",
    "REVIEW_3_STARS_HTML": "&#9733;&#9733;&#9733;&#9733;&#9733;",

    # Avatars
    "AVATAR_1_LETTER": "נ",
    "AVATAR_2_LETTER": "י",
    "AVATAR_3_LETTER": "ש",
    "AVATAR_4_LETTER": "ד",

    # Trust
    "TRUST_1": "ביטוחי שיניים מכל החברות",
    "TRUST_2": "טכנולוגיה דיגיטלית מתקדמת",
    "TRUST_3": "ניסיון של למעלה מ-12 שנה",

    # Micro badges
    "MICRO_BADGE_1": "טכנולוגיה מתקדמת",
    "MICRO_BADGE_2": "גישה אישית",
    "MICRO_BADGE_3": "12+ שנות ניסיון",

    # Working hours
    "WORKING_HOURS_1": "א׳-ה׳: 08:00–20:00",
    "WORKING_HOURS_2": "ו׳: 08:00–14:00",
    "HOURS_ROW1_DAYS": "ראשון – חמישי",
    "HOURS_ROW1_TIME": "08:00 – 20:00",
    "HOURS_ROW2_DAYS": "שישי",
    "HOURS_ROW2_TIME": "08:00 – 14:00",
    "HOURS_ROW3_DAYS": "שבת",
    "HOURS_ROW3_TIME": "סגור",
    "EMERGENCY_TEXT": "מקרי חירום — חייגו 24/7",

    # Footer
    "FOOTER_DESC": "מרפאת שיניים מתקדמת בלב תל אביב.",
    "FOOTER_DESCRIPTION": "מרפאת שיניים מתקדמת בלב תל אביב.",
    "FOOTER_TAGLINE": "החיוך שלכם, המומחיות שלנו.",
}


def generate_examples():
    templates = sorted(glob.glob(os.path.join(TEMPLATE_DIR, "template-[0-9]*.html")))
    print(f"Found {len(templates)} templates")

    for tpl_path in templates:
        fname = os.path.basename(tpl_path)
        num = fname.replace("template-", "").replace(".html", "")
        out_name = f"template_example-{num}.html"
        out_path = os.path.join(TEMPLATE_DIR, out_name)

        with open(tpl_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Remove conditional comments (IF/ENDIF) — keep content inside
        html = re.sub(r'<!--\s*IF:[A-Z_]+\s*-->', '', html)
        html = re.sub(r'<!--\s*ENDIF:[A-Z_]+\s*-->', '', html)

        # Replace all {{VARIABLE}} placeholders
        def replacer(match):
            key = match.group(1)
            if key in DATA:
                return DATA[key]
            else:
                print(f"  ⚠ {fname}: missing key {key}")
                return match.group(0)

        html = re.sub(r'\{\{([A-Z_0-9]+)\}\}', replacer, html)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  ✓ {out_name}")

    print(f"\nDone! Generated {len(templates)} example files.")


if __name__ == "__main__":
    generate_examples()
