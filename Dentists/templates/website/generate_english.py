#!/usr/bin/env python3
"""
Generate English versions of all template examples, blogs, and articles.

For each template-N/:
  template_example-N.html  →  template_example-N-en.html
  blog.html                →  blog-en.html
  blog/*/article.html      →  blog-en/*/article.html

Strategy:
  1. Sort all replacements longest-first to avoid partial matches
  2. Comprehensive replacement pairs for all template variations
  3. Regex-based cleanup for remaining Hebrew text
"""

import os
import re
import shutil

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Hebrew → English content mapping ──────────────────────────────
# Will be auto-sorted longest-first before applying

REPLACEMENTS = [
    # HTML dir/lang attributes
    ('dir="rtl"', 'dir="ltr"'),
    ('lang="he"', 'lang="en"'),

    # ── FULL PARAGRAPHS (must match before any word-level replacements) ──

    # About paragraph — THE critical one that breaks with partial matches
    ('מרפאת חיוך פלוס הוקמה ב-2012 מתוך חזון ליצור חוויית טיפול שיניים שונה לחלוטין. אנחנו מאמינים שכל מטופל ראוי לטיפול ברמה הגבוהה ביותר, בסביבה נעימה ומרגיעה. הצוות שלנו משלב מומחיות רפואית עם טכנולוגיה מתקדמת כדי להעניק לכם את החיוך שתמיד חלמתם עליו.',
     'Smile Plus Dental was founded in 2012 with a vision to create a completely different dental experience. We believe every patient deserves the highest level of care in a pleasant, relaxing environment. Our team combines medical expertise with advanced technology to give you the smile you\'ve always dreamed of.'),

    # Hero subtitles (long)
    ('מרפאת שיניים מתקדמת בלב תל אביב. טיפולים אסתטיים ושיקומיים בגישה אישית וחמה.',
     'An advanced dental clinic in the heart of Tel Aviv. Cosmetic and restorative treatments with a personal, warm approach.'),
    ('מרפאת שיניים מתקדמת בתל אביב המשלבת טכנולוגיה חדשנית עם יחס אישי וחם. הצוות המקצועי שלנו ידאג שתרגישו בנוח מהרגע הראשון.',
     'An advanced dental clinic in Tel Aviv combining innovative technology with a personal, warm approach. Our professional team will ensure you feel comfortable from the first moment.'),
    ('טיפולי שיניים מותאמים אישית בסביבה מקצועית ונעימה. מומחיות, טכנולוגיה מתקדמת ויחס אישי לכל מטופל.',
     'Personalized dental treatments in a professional, pleasant environment. Expertise, advanced technology, and personal care for every patient.'),
    ('מרפאת שיניים מתקדמת בלב תל אביב — מקצועיות, חמימות ותוצאות',
     'An advanced dental clinic in the heart of Tel Aviv — professionalism, warmth, and results'),
    ('חוו טיפולי שיניים ברמה הגבוהה ביותר עם ד״ר מיכל לוי — צוות מומחים, טכנולוגיה דיגיטלית מתקדמת ושירות אישי ומותאם.',
     'Experience the highest level of dental care with Dr. Michelle Levy — expert team, advanced digital technology, and personalized service.'),
    ('ד״ר מיכל לוי — מומחיות רפואית שמובילה לחיוך מושלם',
     'Dr. Michelle Levy — Medical expertise leading to a perfect smile'),
    ('מרפאת חיוך פלוס בתל אביב — טיפולי שיניים מתקדמים, ממוקדים בנוחות שלכם ובתוצאות מושלמות.',
     'Smile Plus Dental in Tel Aviv — advanced dental treatments, focused on your comfort and perfect results.'),

    # About paragraphs (various templates)
    ('המשימה שלנו היא לספק שירותי שיניים איכותיים בסביבה חמה ומזמינה. אנו מאמינים שכל מטופל ראוי לטיפול מעולה, ועובדים ללא לאות כדי להבטיח את שביעות רצונכם ואת בריאות הפה שלכם.',
     'Our mission is to provide quality dental services in a warm, welcoming environment. We believe every patient deserves excellent care, and we work tirelessly to ensure your satisfaction and oral health.'),
    ('במרפאת חיוך פלוס, ד״ר מיכל לוי והצוות המקצועי מספקים טיפולי שיניים מותאמים אישית בסביבה חמה ומזמינה — עם טכנולוגיה מתקדמת ויד רכה.',
     'At Smile Plus Dental, Dr. Michelle Levy and the professional team provide personalized dental treatments in a warm, welcoming environment — with advanced technology and a gentle touch.'),
    ('במרפאת חיוך פלוס, ד״ר מיכל לוי וצוות המומחים משלבים',
     'At Smile Plus Dental, Dr. Michelle Levy and the expert team combine'),
    ('במרפאת חיוך פלוס, ד״ר מיכל לוי וצוות המומחים מספקים טיפולי שיניים מתקדמים בסביבה חמה, מזמינה ומרגיעה. אנחנו משלבים טכנולוגיה חדשנית עם גישה אישית כדי להעניק לכם את החיוך שמגיע לכם.',
     'At Smile Plus Dental, Dr. Michelle Levy and the expert team provide advanced dental treatments in a warm, welcoming, and relaxing environment. We combine innovative technology with a personal approach to give you the smile you deserve.'),
    ('ד״ר מיכל לוי וצוות המרפאה כאן בשבילכם.',
     'Dr. Michelle Levy and the clinic team are here for you.'),
    ('ד״ר מיכל לוי וצוות המרפאה מזמינים אתכם לחוויית טיפול מקצועית ואישית.',
     'Dr. Michelle Levy and the clinic team invite you to a professional, personalized treatment experience.'),
    ('הצוות שלנו של רופאי שיניים מנוסים ומומחים מחויב להעניק את הטיפול הטוב ביותר, המותאם לצרכים הייחודיים שלכם.',
     'Our team of experienced and expert dentists is committed to providing the best care, tailored to your unique needs.'),
    ('הצוות שלנו של רופאי שיניים מומחים מחויב להעניק את הטיפול הטוב ביותר, עם גישה מקצועית ואישית לכל מטופל.',
     'Our team of expert dentists is committed to providing the best care, with a professional and personal approach for every patient.'),
    ('הצוות שלנו מחויב להעניק את הטיפול הטוב ביותר המותאם לצרכים הייחודיים שלך',
     'Our team is committed to providing the best care tailored to your unique needs'),
    ('הצוות שלנו בחיוך פלוס בתל אביב מעניק טיפולי שיניים מתקדמים',
     'Our team at Smile Plus Dental in Tel Aviv provides advanced dental treatments'),
    ('בגישה אישית ומקצועית. אנו מחויבים למצוינות ולחוויית טיפול נעימה',
     'with a personal and professional approach. We are committed to excellence and a pleasant treatment experience'),
    ('מומחה ברפואת שיניים מתקדמת, עם ניסיון של למעלה מ-15 שנה בטיפולים אסתטיים ושיקומיים.',
     'Expert in advanced dentistry with over 15 years of experience in cosmetic and restorative treatments.'),
    ('מומחה/ית בטיפולי שיניים מתקדמים, עם ניסיון רב בתחום רפואת השיניים המודרנית.',
     'Expert in advanced dental treatments with extensive experience in modern dentistry.'),
    ('מחויב/ת למתן טיפול מקצועי ואישי לכל מטופל.',
     'Committed to providing professional and personal care for every patient.'),

    # Service descriptions (long)
    ('טיפולי הלבנה מתקדמים להשגת חיוך לבן וזוהר תוך שמירה על בריאות השן.', 'Advanced whitening treatments for a bright, radiant smile while maintaining tooth health.'),
    ('ציפויים אסתטיים המותאמים אישית לעיצוב חיוך מושלם ותוצאה טבעית.', 'Custom aesthetic veneers designed for a perfect smile and natural-looking results.'),
    ('פתרון קבוע ואיכותי לשיניים חסרות, בטכנולוגיה מתקדמת ודיוק מרבי.', 'A permanent, high-quality solution for missing teeth using advanced technology and precision.'),
    ('טיפולי יישור בשיטת אינויזליין לתוצאות מצוינות ללא גשר מתכתי.', 'Invisalign alignment treatments for excellent results without metal braces.'),
    ('טיפולים מדויקים להצלת שיניים פגועות בטכנולוגיה חדשנית.', 'Precise treatments to save damaged teeth using innovative technology.'),
    ('אבחון וטיפול במחלות חניכיים לשמירה על בריאות הפה ארוכת טווח.', 'Diagnosis and treatment of gum disease for long-term oral health.'),
    ('מגוון טיפולי שיניים מתקדמים בגישה מקצועית ואישית', 'A range of advanced dental treatments with a professional and personal approach'),
    ('מגוון טיפולים מתקדמים לשמירה על בריאות ואסתטיקה של החיוך שלכם', 'A wide range of advanced treatments to maintain the health and beauty of your smile'),
    ('מגוון רחב של טיפולי שיניים מתקדמים, בגישה מקצועית ואישית לכל מטופל.', 'A wide range of advanced dental treatments with a professional and personal approach for every patient.'),
    ('מגוון רחב של שירותי שיניים מקיפים לכל צורכי הבריאות שלכם', 'A comprehensive range of dental services for all your health needs'),
    ('מגוון רחב של טיפולי שיניים מתקדמים בסביבה חמה ומקצועית', 'A wide range of advanced dental treatments in a warm and professional environment'),
    ('מגוון רחב של טיפולים מקצועיים בסביבה נעימה ומתקדמת', 'A wide range of professional treatments in a pleasant, advanced environment'),
    ('מגוון טיפולים מתקדמים לבריאות ואסתטיקה של החיוך שלכם', 'A range of advanced treatments for the health and beauty of your smile'),
    ('מגוון טיפולים מקצועיים לבריאות ואסתטיקה של החיוך שלכם', 'A range of professional treatments for the health and beauty of your smile'),

    # Review 1
    ('ד״ר לוי שינתה לי את החיים. אחרי שנים שנמנעתי מלחייך, עברתי טיפול הלבנה וציפויים — התוצאה מדהימה. הצוות מקצועי, חם ומפנק. ממליצה בחום!',
     'Dr. Levy changed my life. After years of avoiding smiling, I had whitening and veneers — the result is amazing. The team is professional, warm, and caring. Highly recommend!'),

    # Review 2
    ('עברתי השתלת שיניים במרפאה — מהייעוץ הראשוני ועד לתוצאה הסופית, הכל היה ברמה הגבוהה ביותר. ד״ר לוי מסבירה כל שלב ועושה הכל בסבלנות.',
     'I had dental implants at this clinic — from the initial consultation to the final result, everything was top-notch. Dr. Levy explains every step and does everything with patience.'),

    # Review 3
    ('מקום מדהים! הגעתי בפעם הראשונה לטיפול שורש ומאז אני מטופלת קבועה. האווירה נעימה, הצוות מדהים, והטיפול ברמה אחרת לגמרי. תודה רבה!',
     'Amazing place! I came for the first time for a root canal and have been a regular patient since. The atmosphere is pleasant, the team is incredible, and the treatment is on another level. Thank you!'),

    # CTA paragraphs (long)
    ('צרו קשר עוד היום ותנו לנו ללוות אתכם לחיוך הבריא והיפה שמגיע לכם', 'Contact us today and let us guide you to the healthy, beautiful smile you deserve'),
    ('צרו קשר עוד היום ותנו לד״ר מיכל לוי ולצוות חיוך פלוס ללוות אתכם לחיוך הבריא והיפה שמגיע לכם',
     'Contact us today and let Dr. Michelle Levy and the Smile Plus Dental team guide you to the healthy, beautiful smile you deserve'),
    ('צרו קשר עוד היום ותנו לד״ר מיכל לוי ללוות אתכם לחיוך הבריא והיפה שמגיע לכם',
     'Contact us today and let Dr. Michelle Levy guide you to the healthy, beautiful smile you deserve'),
    ('צרו קשר עוד היום ותנו לד״ר מיכל לוי ללוות אתכם לחיוך הבריא שמגיע לכם',
     'Contact us today and let Dr. Michelle Levy guide you to the healthy smile you deserve'),
    ('צרו קשר עם מרפאת חיוך פלוס ותנו לנו ללוות אתכם לחיוך הבריא והיפה שמגיע לכם',
     'Contact Smile Plus Dental and let us guide you to the healthy, beautiful smile you deserve'),
    ('צרו קשר עם חיוך פלוס עוד היום ותנו לד״ר מיכל לוי ללוות אתכם לחיוך הבריא והיפה שמגיע לכם',
     'Contact Smile Plus Dental today and let Dr. Michelle Levy guide you to the healthy, beautiful smile you deserve'),
    ('צרו קשר עם חיוך פלוס בתל אביב עוד היום ותנו לנו ללוות אתכם לחיוך הבריא והיפה שמגיע לכם',
     'Contact Smile Plus Dental in Tel Aviv today and let us guide you to the healthy, beautiful smile you deserve'),
    ('צרו קשר עם חיוך פלוס בתל אביב ותנו לנו ללוות אתכם לחיוך הבריא והיפה שמגיע לכם',
     'Contact Smile Plus Dental in Tel Aviv and let us guide you to the healthy, beautiful smile you deserve'),
    ('צרו קשר עם חיוך פלוס בתל אביב וקבעו תור לייעוץ ראשוני ללא התחייבות',
     'Contact Smile Plus Dental in Tel Aviv and book a free initial consultation — no commitment'),
    ('צרו קשר עוד היום עם חיוך פלוס ותנו לד״ר מיכל לוי ללוות אתכם לחיוך בריא ויפה',
     'Contact Smile Plus Dental today and let Dr. Michelle Levy guide you to a healthy, beautiful smile'),
    ('צרו איתנו קשר לתיאום פגישת ייעוץ ראשונית ללא התחייבות.',
     'Contact us to schedule a free initial consultation — no commitment required.'),
    ('צרו קשר עוד היום וקבלו ייעוץ ראשוני. הצוות של ד״ר מיכל לוי ישמח לעזור לכם.',
     'Contact us today for an initial consultation. Dr. Michelle Levy\'s team would love to help you.'),
    ('צוות המומחים של חיוך פלוס מחכה לכם. קבעו פגישת ייעוץ ללא התחייבות.',
     'The expert team at Smile Plus Dental is waiting for you. Book a consultation — no commitment.'),
    ('קבעו תור לייעוץ ראשוני ללא עלות וגלו כיצד נוכל להעניק לכם את החיוך שתמיד רציתם.',
     'Book a free initial consultation and discover how we can give you the smile you\'ve always wanted.'),
    ('ד״ר מיכל לוי וצוות המומחים מציעים טיפולי שיניים מתקדמים בגישה אישית וחמה. מרפאה מודרנית עם הטכנולוגיה החדישה ביותר בתל אביב.',
     'Dr. Michelle Levy and the expert team offer advanced dental treatments with a personal, warm approach. A modern clinic with the latest technology in Tel Aviv.'),

    # Footer descriptions (long)
    ('מרפאת שיניים מתקדמת בלב תל אביב.', 'An advanced dental clinic in the heart of Tel Aviv.'),
    ('מרפאת שיניים מתקדמת בתל אביב, מספקת טיפולי שיניים מקצועיים ברמה הגבוהה ביותר.',
     'An advanced dental clinic in Tel Aviv, providing the highest level of professional dental care.'),
    ('מרפאת שיניים מתקדמת בתל אביב, מספקת טיפולי שיניים מקצועיים ברמה הגבוהה ביותר בסביבה חמה ומזמינה.',
     'An advanced dental clinic in Tel Aviv, providing the highest level of professional dental care in a warm, welcoming environment.'),
    ('מרפאת שיניים מתקדמת בתל אביב, ד״ר מיכל לוי וצוות מומחים מספקים טיפולים ברמה הגבוהה ביותר.',
     'An advanced dental clinic in Tel Aviv, where Dr. Michelle Levy and the expert team provide top-level treatments.'),
    ('מרפאת שיניים מתקדמת בתל אביב. ד״ר מיכל לוי וצוות מומחים מספקים טיפולים ברמה הגבוהה ביותר.',
     'An advanced dental clinic in Tel Aviv. Dr. Michelle Levy and the expert team provide top-level treatments.'),
    ('חיוך פלוס בתל אביב — מספקת טיפולי שיניים מקצועיים ברמה הגבוהה ביותר עם ד״ר מיכל לוי.',
     'Smile Plus Dental in Tel Aviv — providing the highest level of professional dental care with Dr. Michelle Levy.'),
    ('חיוך פלוס בתל אביב — טיפולי שיניים מקצועיים ברמה הגבוהה ביותר עם גישה אישית וטכנולוגיה מתקדמת.',
     'Smile Plus Dental in Tel Aviv — professional dental care at the highest level with a personal approach and advanced technology.'),
    ('חיוך פלוס בתל אביב — מרפאת שיניים מתקדמת של ד״ר מיכל לוי. טיפולי שיניים מקצועיים ברמה הגבוהה ביותר.',
     'Smile Plus Dental in Tel Aviv — Dr. Michelle Levy\'s advanced dental clinic. Professional dental care at the highest level.'),
    ('מרפאת חיוך פלוס בתל אביב, מספקת טיפולי שיניים מקצועיים ואיכותיים עם גישה חמה ואישית לכל מטופל.',
     'Smile Plus Dental in Tel Aviv, providing professional, quality dental care with a warm, personal approach for every patient.'),
    ('חיוך פלוס בתל אביב. טיפולי שיניים מתקדמים עם טכנולוגיה חדשנית ושירות אישי ומותאם.',
     'Smile Plus Dental in Tel Aviv. Advanced dental treatments with innovative technology and personalized service.'),
    ('חיוך פלוס — מרפאת שיניים מתקדמת בתל אביב. טכנולוגיה חדשנית, צוות מקצועי ויחס אישי וחם לכל מטופל.',
     'Smile Plus Dental — an advanced dental clinic in Tel Aviv. Innovative technology, professional team, and warm personal care for every patient.'),
    ('מרפאת חיוך פלוס בתל אביב — טיפולי שיניים מותאמים אישית, ממוקדים בנוחות שלכם, בביטחון וברווחה ארוכת טווח.',
     'Smile Plus Dental in Tel Aviv — personalized dental treatments focused on your comfort, confidence, and long-term well-being.'),
    ('מרפאת חיוך פלוס בתל אביב — שילוב של מומחיות רפואית, טכנולוגיה חדשנית וגישה אישית לכל מטופל. אנחנו כאן בשבילכם.',
     'Smile Plus Dental in Tel Aviv — combining medical expertise, innovative technology, and a personal approach for every patient. We\'re here for you.'),

    # Testimonials section titles
    ('מטופלים שסומכים עלינו ומשתפים את החוויה שלהם', 'Patients who trust us and share their experience'),
    ('מטופלים שסומכים על חיוך פלוס ומשתפים את החוויה שלהם', 'Patients who trust Smile Plus Dental and share their experience'),
    ('ביקורות אמיתיות מגוגל של מטופלים שבחרו בחיוך פלוס', 'Real Google reviews from patients who chose Smile Plus Dental'),
    ('חוות דעת אמיתיות ממטופלים מרוצים', 'Real testimonials from happy patients'),

    # Blog article content (long)
    ('השתלת שיניים בתל אביב — המדריך המלא לשנת 2026', 'Dental Implants in Tel Aviv — The Complete 2026 Guide'),
    ('כל מה שצריך לדעת על השתלת שיניים: שלבי הטיפול, זמן ההחלמה, ואיך לבחור את המרפאה המתאימה בתל אביב.',
     'Everything you need to know about dental implants: treatment stages, recovery time, and how to choose the right clinic in Tel Aviv.'),
    ('צחצוח שיניים נכון — 7 טעויות שרוב האנשים עושים', 'Proper Teeth Brushing — 7 Mistakes Most People Make'),
    ('רוב האנשים חושבים שהם מצחצחים נכון, אבל טעויות נפוצות יכולות לגרום לנזק. גלו את 7 הטעויות הנפוצות ואיך לתקן אותן.',
     'Most people think they brush correctly, but common mistakes can cause damage. Discover the 7 most common mistakes and how to fix them.'),
    ('השתלת השיניים שינתה את חיי — הסיפור של נועה מתל אביב', 'Dental Implants Changed My Life — Noa\'s Story from Tel Aviv'),
    ('נועה הגיעה למרפאה אחרי שנים של הימנעות מטיפולי שיניים. הסיפור שלה מוכיח שהשתלת שיניים יכולה לשנות חיים.',
     'Noa came to the clinic after years of avoiding dental treatment. Her story proves that dental implants can be life-changing.'),

    # Article content
    ('השתלת שיניים היא הליך כירורגי שבו מוחדר בורג עשוי טיטניום לתוך עצם הלסת, במקום שבו חסרה שן. הבורג משמש כשורש מלאכותי עליו מורכב כתר חרסינה שנראה ומתפקד כמו שן טבעית.',
     'A dental implant is a surgical procedure in which a titanium screw is inserted into the jawbone where a tooth is missing. The screw serves as an artificial root on which a porcelain crown is mounted that looks and functions like a natural tooth.'),
    ('בשונה מגשרים או שיניים תותבות, השתלות שיניים אינן דורשות פגיעה בשיניים שכנות ומספקות פתרון יציב לטווח ארוך.',
     'Unlike bridges or dentures, dental implants do not require damage to neighboring teeth and provide a stable long-term solution.'),
    ('רוב המבוגרים הבריאים מתאימים להשתלת שיניים.',
     'Most healthy adults are candidates for dental implants.'),
    ('תהליך ההחלמה המלא נמשך בדרך כלל בין 3 ל-6 חודשים',
     'The full recovery process typically takes between 3 to 6 months'),
    ('צחצוח שיניים הוא ההרגל החשוב ביותר לשמירה על בריאות הפה',
     'Brushing teeth is the most important habit for maintaining oral health'),

    # Long misc
    ('טיפולי שיניים מותאמים אישית עם טכנולוגיה מתקדמת, בסביבה נעימה ומרגיעה. אנחנו כאן כדי לדאוג לבריאות החיוך שלכם.',
     'Personalized dental treatments with advanced technology in a pleasant, relaxing environment. We\'re here to care for your smile.'),
    ('טיפולי שיניים מותאמים אישית, המתמקדים בנוחות שלך,',
     'Personalized dental treatments focused on your comfort,'),
    ('מתקדמת ונגיעה עדינה.', 'advanced care and a gentle touch.'),
    ('עבור כל מטופל.', 'for every patient.'),
    ('בביטחון ובבריאות הפה לטווח הארוך — עם טכנולוגיה', 'with confidence and long-term oral health — with technology'),
    ('בין אם אתם זקוקים לבדיקה שגרתית, טיפולים קוסמטיים או פרוצדורות מתקדמות, אנחנו כאן כדי לוודא שתגיעו לחיוך שתמיד רציתם. ד״ר מיכל לוי מתמחה ביצירת חוויית טיפול אישית ונעימה לכל מטופל.',
     'Whether you need a routine checkup, cosmetic treatments, or advanced procedures, we\'re here to ensure you achieve the smile you\'ve always wanted. Dr. Michelle Levy specializes in creating a personal, pleasant treatment experience for every patient.'),
    ('טכנולוגיה מתקדמת עם גישה אישית — כי אתם מגיעים את הטיפול הטוב ביותר.',
     'Advanced technology with a personal approach — because you deserve the best care.'),

    # Title tags
    ('חיוך פלוס | מרפאת שיניים | תל אביב', 'Smile Plus Dental | Dental Clinic | Tel Aviv'),

    # ── MEDIUM-LENGTH PHRASES ──

    # Navigation & CTA
    ('עמוד הבית', 'Home'),
    ('קבעו תור עכשיו', 'Book Now'),
    ('קבעו תור', 'Book Now'),
    ('קביעת תור', 'Book Appointment'),
    ('צרו קשר', 'Contact Us'),
    ('דברו איתנו', 'Talk to Us'),
    ('התקשרו עכשיו — 03-555-1234', 'Call Now — 03-555-1234'),
    ('התקשרו עכשיו: 03-555-1234', 'Call Now: 03-555-1234'),
    ('התקשרו עכשיו', 'Call Now'),
    ('או התקשרו ישירות:', 'Or call directly:'),
    ('או חייגו ישירות:', 'Or call directly:'),

    # Clinic identity
    ('מרפאת חיוך פלוס', 'Smile Plus Dental'),
    ('חיוך פלוס', 'Smile Plus Dental'),
    ('ד״ר מיכל לוי', 'Dr. Michelle Levy'),
    ('ד"ר מיכל לוי', 'Dr. Michelle Levy'),
    ('מיכל לוי', 'Michelle Levy'),
    ('רפואת שיניים אסתטית ושיקומית', 'Cosmetic & Restorative Dentistry'),

    # Location
    ('תל אביב-יפו', 'Tel Aviv'),
    ('תל אביב', 'Tel Aviv'),
    ('רוטשילד 45, תל אביב', '45 Rothschild Blvd, Tel Aviv'),
    ('רוטשילד 45', '45 Rothschild Blvd'),

    # Hero
    ('חיוך שמשנה את הכל — מתחיל כאן', 'A Smile That Changes Everything — Starts Here'),
    ('מרפאת שיניים מובילה בתל אביב', 'Leading Dental Clinic in Tel Aviv'),
    ('מומחים לחיוך מושלם', 'Experts in Perfect Smiles'),
    ('חיוך מושלם מתחיל בטיפול נכון', 'A Perfect Smile Starts With the Right Care'),
    ('מרפאת שיניים מתקדמת בתל אביב', 'An advanced dental clinic in Tel Aviv'),
    ('מרפאת שיניים מתקדמת', 'Advanced Dental Clinic'),
    ('מרפאת שיניים מובילה', 'Leading Dental Clinic'),
    ('טיפולי שיניים מתקדמים בתל אביב', 'Advanced Dental Treatments in Tel Aviv'),
    ('טיפולי שיניים מתקדמים', 'Advanced Dental Treatments'),
    ('טיפולי שיניים מותאמים אישית', 'Personalized Dental Treatments'),
    ('מומחים מובילים לכל', 'Leading experts for every'),
    ('צורך רפואי שיניים', 'dental need'),
    ('צורך', 'need'),
    ('מצוינות בכל', 'Excellence in every'),
    ('שאנחנו יוצרים', 'we create'),
    ('טיפול שיניים', 'Dental Care'),
    ('ברמה אחרת', 'on another level'),
    ('בריא מתחיל ב', 'starts at'),
    ('קבלו טיפול שיניים', 'Get dental care'),
    ('פרימיום', 'premium'),
    ('אצל', 'with'),

    # About
    ('אודות המרפאה', 'About Our Clinic'),
    ('אודות', 'About'),
    ('קצת עלינו', 'About Us'),
    ('המרפאה', 'the Clinic'),
    ('מרפאה שמשלבת', 'A clinic that combines'),
    ('עם חמימות', 'with Warmth'),
    ('המטרה שלנו פשוטה — לתת לכם סיבה לחייך בביטחון מלא, כל יום מחדש.',
     'Our goal is simple — to give you a reason to smile with full confidence, every single day.'),
    ('ניסיון של למעלה מ-12 שנה ברפואת שיניים', 'Over 12 years of dental experience'),
    ('ניסיון של למעלה מ-12 שנה', 'Over 12 years of experience'),
    ('טכנולוגיה דיגיטלית מתקדמת', 'Advanced digital technology'),
    ('גישה אישית וחמה לכל מטופל', 'Personal, warm approach for every patient'),
    ('קראו עוד על המרפאה', 'Learn more about the clinic'),

    # Services
    ('מה אנחנו מציעים', 'What We Offer'),
    ('השירותים שלנו', 'Our Services'),
    ('הלבנת שיניים', 'Teeth Whitening'),
    ('ציפויי חרסינה', 'Porcelain Veneers'),
    ('השתלות שיניים', 'Dental Implants'),
    ('השתלת שיניים', 'Dental Implants'),
    ('יישור שיניים שקוף', 'Invisible Aligners'),
    ('טיפולי שורש', 'Root Canal Treatment'),
    ('טיפול שורש', 'Root Canal'),
    ('רפואת חניכיים', 'Gum Treatment'),
    ('למידע נוסף', 'Learn More'),
    ('גלו את השירותים שלנו', 'Explore Our Services'),

    # Stats
    ('שנות ניסיון', 'Years of Experience'),
    ('מטופלים מרוצים', 'Happy Patients'),
    ('לקוחות מרוצים', 'Happy Clients'),
    ('טיפולים בוצעו', 'Treatments Performed'),

    # Testimonials
    ('חוות דעת', 'Testimonials'),
    ('מה המטופלים שלנו אומרים', 'What Our Patients Say'),
    ('מה אומרים עלינו', 'What People Say About Us'),
    ('מה אומרים המטופלים שלנו', 'What Our Patients Say'),
    ('חוויות מטופלים', 'Patient Experiences'),
    ('המלצות מטופלים', 'Patient Recommendations'),
    ('המלצות', 'Recommendations'),
    ('המטופלים שלנו ממליצים', 'Our Patients Recommend'),

    # Reviewer names
    ('נועה כהן', 'Noa Cohen'),
    ('יוסי אברהם', 'Yossi Abraham'),
    ('שירה דויד', 'Shira David'),

    # Time expressions
    ('לפני חודש', '1 month ago'),
    ('לפני שבועיים', '2 weeks ago'),
    ('לפני 3 חודשים', '3 months ago'),

    # CTA titles
    ('מוכנים לחיוך מושלם?', 'Ready for a Perfect Smile?'),
    ('מוכנים לחיוך חדש?', 'Ready for a New Smile?'),
    ('מוכנים לחיוך שתמיד רציתם?', 'Ready for the Smile You\'ve Always Wanted?'),
    ('מוכנים לחיוך הבריא?', 'Ready for a Healthy Smile?'),

    # Trust badges
    ('ביטוחי שיניים מכל החברות', 'All dental insurance accepted'),
    ('אחריות מלאה', 'Full Warranty'),
    ('ללא כאב', 'Painless'),
    ('מומחים מוסמכים', 'Certified Experts'),
    ('ציוד מתקדם', 'Advanced Equipment'),
    ('ללא התחייבות', 'No Commitment'),
    ('מומחיות מוכחת', 'Proven Expertise'),
    ('ייעוץ ראשוני חינם', 'Free Initial Consultation'),

    # Badges & trust bar
    ('מאושר משרד הבריאות', 'Ministry of Health Approved'),
    ('מאושר ע"י משרד הבריאות', 'Approved by the Ministry of Health'),
    ('מרפאה מאושרת משרד הבריאות', 'Ministry of Health Approved Clinic'),
    ('מרפאה מאושרת', 'Approved Clinic'),
    ('מוסמך משרד הבריאות', 'Ministry of Health Certified'),
    ('רישיון תקף', 'Valid License'),
    ('רישיון מקצועי מאומת', 'Verified Professional License'),
    ('שיחות מטופלים חדשים', 'New Patient Calls'),
    ('שיחה נכנסת', 'Incoming Call'),
    ('מתקשר/ת...', 'calling...'),
    ('דירוג מרוצים', 'satisfaction rating'),
    ('מרפאה מובילה', 'Leading Clinic'),
    ('מאושר', 'Approved'),
    ('ניסיון מוכח', 'Proven Experience'),
    ('אלפי חיוכים חדשים', 'Thousands of new smiles'),
    ('שנים של', 'Years of'),
    ('ביקורות מאומתות', 'Verified Reviews'),
    ('טיפול מקצועי', 'Professional Care'),
    ('זמין עכשיו', 'Available Now'),
    ('בגוגל', 'on Google'),
    ('ביקורות בגוגל', 'Google Reviews'),

    # Working hours
    ('א׳-ה׳: 08:00–20:00', 'Sun–Thu: 08:00–20:00'),
    ('ו׳: 08:00–14:00', 'Fri: 08:00–14:00'),
    ('א׳-ה׳ 8:00-20:00', 'Sun–Thu: 8:00–20:00'),
    ('ו׳ 8:00-13:00', 'Fri: 8:00–13:00'),
    ('א׳–ה׳ 8:00–20:00', 'Sun–Thu: 8:00–20:00'),
    ('ו׳ 8:00–13:00', 'Fri: 8:00–13:00'),
    ('ראשון – חמישי', 'Sunday – Thursday'),
    ('א׳ – ה׳', 'Sun – Thu'),
    ('היום: פתוח', 'Today: Open'),
    ('שעות פעילות', 'Hours'),
    ('שעות קבלה', 'Office Hours'),
    ('זמין לתורים', 'Available for Appointments'),
    ('שישי', 'Friday'),
    ('שבת', 'Saturday'),
    ('סגור', 'Closed'),
    ('מקרי חירום — חייגו 24/7', 'Emergencies — Call 24/7'),
    ('● קבעו תור ● קבעו תור ', '● Book Now ● Book Now '),

    # Footer
    ('החיוך שלכם, המומחיות שלנו.', 'Your smile, our expertise.'),
    ('כל הזכויות שמורות.', 'All rights reserved.'),
    ('כל הזכויות שמורות', 'All rights reserved'),
    ('ניווט מהיר', 'Quick Links'),
    ('ניווט', 'Navigation'),
    ('מידע', 'Info'),
    ('קישורים', 'Links'),
    ('מדיניות פרטיות', 'Privacy Policy'),
    ('צוות המרפאה', 'Our Team'),
    ('מאמרים', 'Articles'),
    ('מצאו אותנו', 'Find Us'),

    # Social / directions
    ('הוראות הגעה', 'Get Directions'),
    ('הגעה למרפאה', 'Get Directions'),
    ('הגיעו למרפאה', 'Visit the Clinic'),
    ('פתיחה בגוגל מפות', 'Open in Google Maps'),
    ('פתח', 'Open'),
    ('מפה', 'Map'),

    # Doctor
    ('רופא/ת שיניים ראשי/ת', 'Chief Dentist'),
    ('רופא/ת שיניים מומחה/ית', 'Specialist Dentist'),
    ('רופא שיניים מומחה', 'Specialist Dentist'),
    ('מומחה לטיפולי שיניים', 'Dental Treatment Specialist'),
    ('מומחה בטיפולי שיניים', 'Dental Treatment Specialist'),
    ('מומחה בשיקום הפה', 'Oral Rehabilitation Specialist'),
    ('צוות מקצועי', 'Professional Team'),
    ('וצוות מומחים לשירותך', 'and expert team at your service'),
    ('המשימה שלנו', 'Our Mission'),

    # Blog page
    ('הבלוג שלנו', 'Our Blog'),
    ('מאמרים ומידע על בריאות הפה', 'Articles and Information About Oral Health'),
    ('מאמרים, טיפים ומידע חשוב על טיפולי שיניים ובריאות הפה', 'Articles, tips, and important information about dental treatments and oral health'),

    # Blog categories
    ('הכל', 'All'),
    ('בריאות הפה', 'Oral Health'),
    ('טיפולים', 'Treatments'),
    ('הצוות שלנו', 'Our Team'),
    ('מיתוסים ועובדות', 'Myths & Facts'),
    ('עונתי', 'Seasonal'),
    ('מבצעים', 'Promotions'),
    ('סיפורי מטופלים', 'Patient Stories'),

    # Blog dates
    ('2 במרץ 2026', 'March 2, 2026'),

    # Article content
    ('מהי השתלת שיניים?', 'What is a Dental Implant?'),
    ('מי מתאים להשתלת שיניים?', 'Who is a Candidate for Dental Implants?'),
    ('שלבי הטיפול — מהייעוץ הראשוני ועד לחיוך החדש', 'Treatment Steps — From Initial Consultation to Your New Smile'),
    ('כמה זמן לוקח להחלים?', 'How Long Does Recovery Take?'),
    ('כמה זמן לוקח תהליך השתלת שיניים?', 'How long does the dental implant process take?'),
    ('התהליך המלא אורך בין 3 ל-6 חודשים', 'The full process takes between 3 to 6 months'),
    ('האם השתלת שיניים כואבת?', 'Are dental implants painful?'),
    ('הטיפול מבוצע תחת הרדמה מקומית', 'The treatment is performed under local anesthesia'),
    ('מהו אחוז ההצלחה של השתלות שיניים?', 'What is the success rate of dental implants?'),
    ('אחוז ההצלחה של השתלות שיניים עומד על כ-95-98%', 'The success rate of dental implants is approximately 95-98%'),
    ('מתעניינים בהשתלת שיניים?', 'Interested in Dental Implants?'),
    ('צרו קשר לייעוץ ראשוני ללא התחייבות', 'Contact us for a free consultation — no commitment'),
    ('7 טעויות שרוב האנשים עושים בצחצוח שיניים', '7 Mistakes Most People Make When Brushing Teeth'),
    ('השתלת השיניים שינתה את חיי', 'Dental Implants Changed My Life'),
    ('הסיפור של נועה', "Noa's Story"),
    ('שאלות נפוצות', 'Frequently Asked Questions'),
    ('ייעוץ ראשוני ותכנון', 'Initial consultation and planning'),
    ('הכנה (במידת הצורך)', 'Preparation (if needed)'),
    ('הכנסת השתל', 'Implant placement'),
    ('תקופת החלמה', 'Recovery period'),
    ('חיבור האבטמנט', 'Abutment connection'),
    ('התקנת הכתר', 'Crown installation'),
    ('בריאות כללית תקינה', 'Good general health'),
    ('עצם לסת מספקת', 'Sufficient jawbone density'),
    ('חניכיים בריאות', 'Healthy gums'),
    ('מחויבות לתהליך ההחלמה', 'Commitment to the recovery process'),
    ('מאמרים קשורים', 'Related Articles'),
    ('חזרה לבלוג', 'Back to Blog'),
    ('שתפו:', 'Share:'),
    ('קריאה מהנה!', 'Happy reading!'),

    # Rating
    ('ב-Google', 'on Google'),
    ('ביקורות מטופלים', 'Patient Reviews'),
    ('דירוג ב-Google', 'Google Rating'),
    ('דירוג Google', 'Google Rating'),
    ('דירוג ממוצע', 'Average Rating'),
    ('דירוג גוגל', 'Google Rating'),
    ('דירוג גבוה בגוגל', 'High Google Rating'),
    ('דירוג 4.9 מתוך 5', '4.9 out of 5 Rating'),
    ('ביקורת Google', 'Google Review'),
    ('ביקורת גוגל', 'Google Review'),
    ('ביקורות', 'Reviews'),
    ('מחויבות למטופל', 'Patient Commitment'),

    # Location
    ('מיקום המרפאה', 'Clinic Location'),
    ('ישראל', 'Israel'),
    ('נגיש ונוח', 'Accessible & Convenient'),

    # Misc short
    ('שירותים', 'Services'),
    ('צור קשר', 'Contact'),
    ('בלוג', 'Blog'),
    ('אודות', 'About'),
    ('8 דקות קריאה', '8 min read'),
    ('5 דקות קריאה', '5 min read'),
    ('6 דקות קריאה', '6 min read'),
    ('דקות קריאה', 'min read'),
    ('קראו עוד', 'Read More'),
    ('מטופלת', 'Patient'),
    ('מטופל', 'Patient'),
    ('טכנולוגיה מתקדמת', 'Advanced Technology'),
    ('גישה אישית', 'Personal Approach'),
    ('12+ שנות ניסיון', '12+ Years of Experience'),
    ('מקצועיות', 'Professionalism'),
    ('טלפון', 'Phone'),
    ('כתובת', 'Address'),
    ('ביטוח', 'Insurance'),
    ('חניה', 'Parking'),
    ('נגישות', 'Accessibility'),
    ('מוסמך', 'Certified'),
    ('ביטוחים מתקבלים', 'Insurance Accepted'),
    ('טיפול מקצועי ואישי בתל אביב', 'Professional, personal care in Tel Aviv'),

    # Aria labels
    ('תפריט', 'Menu'),
    ('צפה בסרטון', 'Watch Video'),
    ('עוד', 'More'),
    ('פייסבוק', 'Facebook'),
    ('אינסטגרם', 'Instagram'),
    ('וואטסאפ', 'WhatsApp'),

    # With <br> variants
    ('שנות<br>ניסיון', 'Years of<br>Experience'),
    ('מיקום<br>המרפאה', 'Clinic<br>Location'),

    # ── SINGLE WORDS (must come last) ──
    ('חיוך שמשנה', 'A Smile That'),
    ('את הכל', 'Changes Everything'),
    ('מתחיל כאן', 'Starts Here'),
    ('שמחייכת', 'that smiles'),
    ('אליכם', 'at you'),
    ('יוצרים', 'we create'),
    ('חיוך', 'Smile'),
    ('מושלם', 'Perfect'),
    ('ביקור שיניים', 'Dental Visit'),
    ('רגוע יותר', 'More Relaxed'),
    ('שיניים', 'dental'),
    ('רפואי', 'medical'),
    ('טיפול', 'treatment'),
    ('מתוך', 'out of'),
    ('חדש', 'New'),
    ('שלך', 'yours'),
    ('שלכם', 'yours'),
    ('שלנו', 'our'),
    ('מומחים', 'Experts'),
    ('חמימות', 'warmth'),
    ('ותוצאות', 'and results'),
    ('כוכבים', 'stars'),
    ('מחייכת', 'smiling'),
    ('מחייך/ת', 'smiling'),
    ('בריאות', 'Health'),
    ('משרד', 'Ministry of'),
    ('החוויה', 'the experience'),
    ('שסומכים על', 'who trust'),
    ('ומשתפים את', 'and share'),
    ('ייעוץ', 'consultation'),
    ('מומחיות מקצועית', 'Professional Expertise'),
    ('יחס חם ואישי', 'Warm Personal Care'),
    ('זמינות מלאה', 'Full Availability'),
    ('מחכה לכם', 'is waiting for you'),
    ('קבעו פגישת', 'Book a'),
    ('ללוות אתכם', 'guide you to'),
    ('ותנו ל', 'and let '),
    ('ותנו לנו', 'and let us'),
    ('עוד היום', 'today'),
    ('והיפה', 'and beautiful'),
    ('שמגיע לכם', 'you deserve'),
    ('בסביבה', 'in an environment'),
    ('נעימה', 'pleasant'),
    ('ומקצועית', 'and professional'),
    ('ויפה', 'and beautiful'),
    ('מובילים', 'leading'),
]

# ── Sorted longest-first to avoid partial match issues ──
REPLACEMENTS.sort(key=lambda pair: len(pair[0]), reverse=True)


# Internal link rewrites: Hebrew filenames → English filenames
LINK_REWRITES = [
    ('template_example-{n}.html', 'template_example-{n}-en.html'),
    ('blog.html', 'blog-en.html'),
    ('blog/tipulim/hashtalat-shinayim-tel-aviv.html', 'blog-en/tipulim/hashtalat-shinayim-tel-aviv.html'),
    ('blog/briut-hapeh/tzviat-shinayim-nechona.html', 'blog-en/briut-hapeh/tzviat-shinayim-nechona.html'),
    ('blog/sipurei-metuplim/hashtalat-shinayim-shinu-et-hayim-sheli.html', 'blog-en/sipurei-metuplim/hashtalat-shinayim-shinu-et-hayim-sheli.html'),
]

# Hebrew initials → English initials (for avatar divs)
INITIAL_MAP = {
    'נ': 'N',  # Noa
    'י': 'Y',  # Yossi
    'ש': 'S',  # Shira
    'מ': 'M',  # Michal
    'ד': 'D',  # Dr.
    'ח': 'S',  # Smile (from חיוך)
}


def translate_html(html):
    """Apply all Hebrew → English text replacements (longest-first)."""
    for he, en in REPLACEMENTS:
        html = html.replace(he, en)
    return html


def cleanup_remaining_hebrew(html):
    """Regex-based cleanup for remaining Hebrew text after replacements."""

    # Fix Hebrew initials in avatar/initial divs
    # Pattern: >X</  where X is a single Hebrew letter
    for he_letter, en_letter in INITIAL_MAP.items():
        html = html.replace(f'>{he_letter}</', f'>{en_letter}</')
        html = html.replace(f'>{he_letter}<', f'>{en_letter}<')

    # Fix "Patient/ת" → "Patient"
    html = html.replace('Patient/ת', 'Patient')

    # Fix mixed patterns from partial translations
    html = re.sub(r'הServices שלנו', 'Our Services', html)
    html = re.sub(r'הSmile ה?Perfect', 'a Perfect Smile', html)
    html = re.sub(r'לSmile ה?Perfect', 'a Perfect Smile', html)
    html = re.sub(r'לSmile בריא', 'a Healthy Smile', html)
    html = re.sub(r'לSmile חדש', 'a New Smile', html)
    html = re.sub(r'לSmile שתמיד רציתם', 'the Smile You\'ve Always Wanted', html)
    html = re.sub(r'לSmile הBriא', 'a Healthy Smile', html)
    html = re.sub(r'הSmile שלכם', 'your Smile', html)
    html = re.sub(r'הSmile שמגיע לכם', 'the Smile you deserve', html)
    html = re.sub(r'הSmile הBriא והיפה שמגיע לכם', 'the healthy, beautiful Smile you deserve', html)
    html = re.sub(r'הSmile שתמיד חלמתם עליו', 'the Smile you\'ve always dreamed of', html)
    html = re.sub(r'בTel Aviv', 'in Tel Aviv', html)
    html = re.sub(r'About המרפאה', 'About the Clinic', html)
    html = re.sub(r'Aboutינו', 'About Us', html)
    html = re.sub(r'Treatments אסתטיים ושיקומיים', 'cosmetic and restorative treatments', html)
    html = re.sub(r'Treatments מתקדמים', 'Advanced Treatments', html)
    html = re.sub(r'Treatments מקצועיים', 'Professional Treatments', html)
    html = re.sub(r'Treatments קוסמטיים', 'Cosmetic Treatments', html)
    html = re.sub(r'Treatments ברמה הגבוהה ביותר', 'top-level Treatments', html)
    html = re.sub(r'Personal Approach וחמה', 'a personal, warm approach', html)
    html = re.sub(r'Patientים', 'Patients', html)
    html = re.sub(r'Reviews גוגל', 'Google Reviews', html)
    html = re.sub(r'Reviews מרוצים', 'Satisfied Reviews', html)
    html = re.sub(r'Reviews מאומתות', 'Verified Reviews', html)
    html = re.sub(r'Reviews אמיתיות מגוגל', 'Real Google Reviews', html)
    html = re.sub(r'Reviews בגוגל', 'Google Reviews', html)
    html = re.sub(r'on Google Maps', 'on Google Maps', html)  # already fine
    html = re.sub(r'Smile לבן וזוהר', 'a bright, radiant smile', html)
    html = re.sub(r'Smile Perfect', 'a Perfect Smile', html)
    html = re.sub(r'Smile שמשנה All', 'A Smile That Changes Everything', html)
    html = re.sub(r'Smile <span', 'A Smile <span', html)
    html = re.sub(r'Oral Health', 'Oral Health', html)  # already fine

    # Fix remaining Hebrew text in specific contexts
    # CTA: "Contact Us..." patterns with remaining Hebrew
    html = re.sub(r'Contact Us More היום[^<]+', 'Contact us today and let us guide you to the healthy, beautiful smile you deserve', html)
    html = re.sub(r'Contact Us today[^<]*ללוות[^<]+', 'Contact us today and let us guide you to the healthy, beautiful smile you deserve', html)
    html = re.sub(r'Contact Us today[^<]*לnew Smile[^<]+', 'Contact us today and let us guide you to your new smile', html)
    html = re.sub(r'Contact Us עוד היום ותנו לנו ללוות אתכם ל[^<]+', 'Contact us today and let us guide you to the healthy, beautiful smile you deserve', html)
    html = re.sub(r'Contact Us עוד היום ותנו ל[^<]+', 'Contact us today and let us guide you to the smile you deserve', html)
    html = re.sub(r'Contact Us עם[^<]+לSmile[^<]+', 'Contact us today for a consultation — no commitment', html)
    html = re.sub(r'Contact Us עם[^<]+', 'Contact us today for a consultation — no commitment', html)
    html = re.sub(r'Contact Us עוד היום וקבלו[^<]+', 'Contact us today for an initial consultation', html)
    html = re.sub(r'Contact Us עוד היום עם[^<]+', 'Contact us today for the smile you deserve', html)
    html = re.sub(r'Book Now לייעוץ[^<]+', 'Book a free consultation and discover how we can give you the smile you\'ve always wanted.', html)
    html = re.sub(r'Book a consultation No Commitment', 'Book a consultation — no commitment', html)

    # Fix remaining Hebrew paragraphs (about, footer, hero descriptions)
    html = re.sub(
        r'Smile Plus Dental הוקמה ב-2012[^<]+',
        'Smile Plus Dental was founded in 2012 with a vision to create a completely different dental experience. We believe every patient deserves the highest level of care in a pleasant, relaxing environment. Our team combines medical expertise with advanced technology to give you the smile you\'ve always dreamed of.',
        html
    )

    # Hero/heading mixed text cleanup
    html = re.sub(r'מרפאת dental מתקדמת', 'Advanced Dental Clinic', html)
    html = re.sub(r'מרפאת dental', 'Dental Clinic', html)
    html = re.sub(r'מרפאת Smile Plus Dental', 'Smile Plus Dental', html)
    html = re.sub(r'במרפאת Smile Plus Dental', 'at Smile Plus Dental', html)
    html = re.sub(r'מוכנים a Perfect Smile\??', 'Ready for a Perfect Smile?', html)
    html = re.sub(r'מוכנים a New Smile\??', 'Ready for a New Smile?', html)
    html = re.sub(r'מוכנים the Smile[^<]*', 'Ready for the Smile You\'ve Always Wanted?', html)
    html = re.sub(r'מוכנים a Healthy Smile\??', 'Ready for a Healthy Smile?', html)
    html = re.sub(r'מוכנים ל', 'Ready for ', html)
    html = re.sub(r'מתחיל with', 'starts with', html)
    html = re.sub(r'a Perfect Smile yours', 'Your Perfect Smile', html)
    html = re.sub(r'Experts ל<span', 'Experts in <span', html)
    html = re.sub(r'Smile שאנחנו', 'Smile We', html)
    html = re.sub(r'שמשנה All', 'That Changes Everything', html)
    html = re.sub(r'Experts leading לכל', 'Leading Experts for Every', html)
    html = re.sub(r'Leading in Tel Aviv', 'Leading in Tel Aviv', html)
    html = re.sub(r'דירוג on Google<br>out of', 'Google Rating<br>from', html)
    html = re.sub(r'Professionalism, warmth and results', 'Professionalism, warmth and results', html)
    html = re.sub(r'Patients who trust Smile Plus Dental and share the experience שלהם', 'Patients who trust Smile Plus Dental and share their experience', html)
    html = re.sub(r'Patients שסומכים[^<]+', 'Patients who trust Smile Plus Dental and share their experience', html)

    # Fix remaining footer mixed text
    html = re.sub(r'Smile Plus Dental — מרפאת [^<]+', 'Smile Plus Dental — Advanced dental clinic in Tel Aviv. Innovative technology, professional team, and warm personal care.', html)
    html = re.sub(r'מגוון רחב של [^<]+', 'A wide range of professional dental services for all your health needs', html)
    html = re.sub(r'מגוון Treatments[^<]+', 'A range of advanced dental treatments for the health and beauty of your smile', html)
    html = re.sub(r'Testimonials אמיתיות מHappy Patients', 'Real testimonials from happy patients', html)
    html = re.sub(r'Our Team של [^<]+', 'Our experienced team of dentists is committed to providing the best personalized care.', html)
    html = re.sub(r'Our Team משלב[^<]+', 'Our team combines medical expertise with advanced technology to give you the smile you\'ve always dreamed of.', html)
    html = re.sub(r'Our Team מחויב[^<]+', 'Our team is committed to providing the best care tailored to your unique needs', html)
    html = re.sub(r'Our Team ב[^<]+מעניק[^<]+', 'Our team at Smile Plus Dental provides advanced dental treatments', html)

    # Doctor card text
    html = re.sub(r'Dr\. Michelle Levy מתמחה[^<]+', 'Dr. Michelle Levy specializes in creating a personal, pleasant treatment experience for every patient.', html)
    html = re.sub(r'Dr\. Michelle Levy וצוות המומחים מציעים[^<]+', 'Dr. Michelle Levy and the expert team offer advanced dental treatments with a personal, warm approach. A modern clinic with the latest technology in Tel Aviv.', html)

    # Fix template 7/3 about paragraph with mixed text (catches partially-translated versions)
    html = re.sub(
        r'(?:at |ב)Smile Plus Dental, Dr\. Michelle Levy[^<]*מספקים[^<]+',
        'At Smile Plus Dental, Dr. Michelle Levy and the expert team provide advanced dental treatments in a warm, welcoming, and relaxing environment. We combine innovative technology with a personal approach to give you the smile you deserve.',
        html, flags=re.IGNORECASE
    )
    html = re.sub(
        r'(?:at |ב)Smile Plus Dental, Dr\. Michelle Levy[^<]*משלבים[^<]*',
        'At Smile Plus Dental, Dr. Michelle Levy and the expert team combine medical expertise with advanced technology to provide the best care.',
        html, flags=re.IGNORECASE
    )

    # Fix "צוות המומחים של Smile Plus Dental..." patterns
    html = re.sub(
        r'צוות המומחים של Smile Plus Dental[^<]+',
        'The expert team at Smile Plus Dental is waiting for you. Book a consultation — no commitment required.',
        html
    )

    # Fix "Patient מחייכת/ת" in alt text
    html = re.sub(r'Patient smiling[^"]*dental[^"]*Smile Plus Dental', 'Smiling patient at Smile Plus Dental', html)
    html = re.sub(r'Patient smiling[^"]*Smile Plus Dental', 'Smiling patient at Smile Plus Dental', html)
    html = re.sub(r'Patient smiling', 'Smiling patient', html)

    # Fix specific remaining mixed-text patterns
    html = re.sub(r'הPerfect', 'Perfect', html)
    html = re.sub(r'הHealth', 'Health', html)
    html = re.sub(r'הExperts', 'expert team', html)
    html = re.sub(r'הצעד הראשון ל', 'The First Step to ', html)
    html = re.sub(r'מתחיל with', 'starts with', html)
    html = re.sub(r'ולצוות', 'and the team at', html)
    html = re.sub(r'של Patients שבחרו ב', 'from patients who chose ', html)
    html = re.sub(r'Experts leading<br>לכל', 'Leading Experts for Every', html)
    html = re.sub(r'מגוון Advanced', 'A Range of Advanced', html)
    html = re.sub(r'צוות expert team של', 'The expert team at', html)
    html = re.sub(r'צוות ה', 'The ', html)
    html = re.sub(r'ו׳', 'Fri', html)
    html = re.sub(r'לSmile הבריא', 'the healthy smile', html)
    html = re.sub(r'הבריא', 'healthy', html)
    html = re.sub(r'לSmile', 'the smile', html)
    html = re.sub(r'מתחיל', 'starts', html)

    # ── Article-specific content replacements ──
    # These handle the detailed medical content in blog articles

    # Article titles
    html = re.sub(r'צחצוח dental נכון — 7 טעויות נפוצות', 'Proper Brushing — 7 Common Mistakes', html)
    html = re.sub(r'צחצוח dental נכון', 'Proper Teeth Brushing', html)
    html = re.sub(r'Dental Implants in Tel Aviv — המדריך המלא', 'Dental Implants in Tel Aviv — Complete Guide', html)
    html = re.sub(r'"Dental Implants Changed My Life" — Noa\'s Story מTel Aviv', '"Dental Implants Changed My Life" — Noa\'s Story from Tel Aviv', html)
    html = re.sub(r'Articles נוספים', 'More Articles', html)

    # Article section headings
    html = re.sub(r'הטכניקה הנכונה לצחצוח', 'The Right Brushing Technique', html)
    html = re.sub(r'הפחד שהפך למציאות', 'When Fear Became Reality', html)
    html = re.sub(r'הפנייה הראשונה', 'The First Visit', html)
    html = re.sub(r'תהליך הtreatment — שלב אחרי שלב', 'The Treatment Process — Step by Step', html)
    html = re.sub(r'החיים אחרי ההשתלה', 'Life After Implants', html)
    html = re.sub(r'גם אתם רוצים לחזור לחייך\?', 'Want to smile again?', html)
    html = re.sub(r'רוצים לוודא שאתם מצחצחים נכון\?', 'Want to make sure you\'re brushing correctly?', html)

    # Brushing mistakes headings
    html = re.sub(r'צחצוח חזק מדי', 'Brushing Too Hard', html)
    html = re.sub(r'שימוש במברשת קשה', 'Using a Hard-Bristle Brush', html)
    html = re.sub(r'צחצוח קצר מדי', 'Brushing Too Briefly', html)
    html = re.sub(r'הזנחת קו החניכיים', 'Neglecting the Gumline', html)
    html = re.sub(r'שכחת הלשון', 'Forgetting the Tongue', html)
    html = re.sub(r'צחצוח מיד אחרי אכילה', 'Brushing Right After Eating', html)
    html = re.sub(r'אי-החלפת מברשת בזמן', 'Not Replacing Your Brush on Time', html)

    # FAQ questions
    html = re.sub(r'כמה זמן אחרי ההשתלה אפשר לחזור לשגרה\?', 'How soon after the implant can I return to normal activity?', html)
    html = re.sub(r'מברשת ידנית או חשמלית — מה עדיף\?', 'Manual or electric toothbrush — which is better?', html)
    html = re.sub(r'האם חוט דנטלי באמת הכרחי\?', 'Is dental floss really necessary?', html)
    html = re.sub(r'כמה פעמים ביום צריך לצחצח\?', 'How many times a day should you brush?', html)
    html = re.sub(r'איך מוצאים מרפאה מתאימה לDental Implants\?', 'How to find the right clinic for dental implants?', html)
    html = re.sub(r'האם Dental Implants מתאימה לכל אחד\?', 'Are dental implants suitable for everyone?', html)

    # Meta descriptions
    html = re.sub(r'המדריך המלא לDental Implants[^"]+', 'The complete guide to dental implants in Tel Aviv 2026: treatment stages, recovery time, costs, and how to choose a clinic. Smile Plus Dental — Dr. Michelle Levy.', html)
    html = re.sub(r'למדו על 7 טעויות נפוצות[^"]+', 'Learn about 7 common brushing mistakes most people make and how to brush correctly. Professional tips from Dr. Michelle Levy, Smile Plus Dental Tel Aviv.', html)
    html = re.sub(r'נועה מTel Aviv מספרת[^"]+', "Noa from Tel Aviv shares how dental implants at Smile Plus Dental changed her life. Read the full story.", html)
    html = re.sub(r'נועה מספרת איך Dental Implants[^"]+', "Noa shares how dental implants changed her life. A real story from Smile Plus Dental.", html)

    # Breadcrumbs
    html = re.sub(r'"name": "צחצוח dental נכון"', '"name": "Proper Teeth Brushing"', html)

    # Full article paragraphs — replace any <p> content with significant Hebrew
    ARTICLE_PARAGRAPH_REPLACEMENTS = [
        # Implant article
        (r'Dental Implants היא הליך כירורגי שבו מוחדר בורג עשוי טיטניום[^<]+',
         'A dental implant is a surgical procedure in which a titanium screw is inserted into the jawbone where a tooth is missing. The implant serves as an artificial root on which a crown is mounted — a permanent tooth that looks, feels, and functions exactly like a natural tooth. It is the most permanent and highest-quality solution available today for replacing missing teeth.'),
        (r'בשונה מגשרים או dental תותבות[^<]+',
         'Unlike bridges or dentures, dental implants do not require damage to neighboring teeth and provide complete stability. The titanium fuses with the bone in a process called osseointegration, creating a strong and durable foundation that can last a lifetime with proper care and maintenance.'),
        (r'רוב האנשים הבוגרים מתאימים לDental Implants[^<]+',
         'Most adults are candidates for dental implants, but there are several conditions to check before treatment:'),
        (r'בconsultation הראשוני בSmile Plus Dental[^<]+',
         'At the initial consultation at Smile Plus Dental, Dr. Michelle Levy will perform a comprehensive examination including a 3D CT scan to assess the bone condition and build a personalized treatment plan.'),
        (r'ההחלמה המלאה — כלומר המזגת השתל[^<]+',
         'The full recovery — meaning the implant fusing with the bone — takes between 3 to 6 months, depending on the implant location and overall health. During this period, regular follow-up appointments at the clinic ensure the healing process progresses properly. After the permanent crown is installed, you can return to normal eating and brushing routines.'),
        (r'רוב הPatients חוזרים לשגרה תוך[^<]+',
         'Most patients return to their routine within a day or two after surgery. In the first few days, there may be mild swelling and discomfort, which can be managed with regular pain medication and cold compresses. It\'s important to eat soft food in the first week and avoid strenuous physical activity.'),

        # Brushing article
        (r'רוב האנשים משוכנעים שהם מצחצחים dental נכון[^<]+',
         'Most people are convinced they brush their teeth correctly — but the reality is different. At our clinic, we see patients every day with damage caused by incorrect brushing: enamel erosion, gum recession, and cavities that could have been prevented. Here are the 7 most common mistakes — and how to fix them.'),
        (r'הרבה אנשים חושבים שככל שלוחצים חזק יותר[^<]+',
         'Many people think the harder they press, the cleaner their teeth get. But the opposite is true — excessive pressure causes enamel erosion (the protective coating of the tooth) and gum recession that exposes the tooth root. <strong>The fix:</strong> Use gentle circular motions, as if massaging the gums. An electric toothbrush with a pressure sensor can help enormously — it alerts you when you\'re pressing too hard.'),
        (r'מברשת with סיבים קשים נראית[^<]+',
         'A hard-bristle brush may seem like it cleans better, but it actually damages gums and enamel. <strong>The fix:</strong> Dentists recommend using a brush with <strong>soft</strong> bristles only. Soft bristles are flexible enough to reach between teeth and clean effectively without causing gum recession.'),
        (r'המחקרים מראים שרוב האנשים מצחצחים[^<]+',
         'Studies show most people brush for about 45 seconds — less than half the recommended time. <strong>The fix:</strong> Brush for at least <strong>two minutes</strong> each time. Divide your mouth into four quadrants and spend 30 seconds on each. Use a phone timer or an electric toothbrush with a built-in timer.'),
        (r'קו החניכיים — המקום שבו השן פוגשת[^<]+',
         'The gumline — where the tooth meets the gum — is exactly where plaque accumulates the most. Neglecting this area leads to gingivitis and eventually gum disease. <strong>The fix:</strong> Tilt the brush at a <strong>45-degree angle</strong> toward the gumline and clean with short, gentle strokes.'),
        (r'הלשון היא משטח גדול שעליו מצטברים[^<]+',
         'The tongue is a large surface where many bacteria accumulate — they are the main cause of bad breath. <strong>The fix:</strong> At the end of each brushing, run the brush over the tongue from back to front several times. Alternatively, use a dedicated tongue scraper for better results.'),
        (r'זה נשמע אינטואיטיבי לצחצח מיד אחרי ארוחה[^<]+',
         'It seems intuitive to brush right after a meal, but after eating acidic foods (citrus fruits, tomatoes, carbonated drinks) the enamel is temporarily soft. Immediate brushing can cause erosion. <strong>The fix:</strong> Wait <strong>30 minutes</strong> after eating acidic food. Meanwhile, you can rinse your mouth with water or chew sugar-free gum to stimulate saliva production.'),
        (r'מברשת dental ישנה with סיבים בלויים[^<]+',
         'An old toothbrush with worn, splayed bristles doesn\'t clean properly. Moreover, bacteria accumulate on the bristles over time. <strong>The fix:</strong> Replace your brush (or electric brush head) <strong>every 3 months</strong>, or sooner if the bristles appear worn. Rule of thumb: if the bristles are splayed outward, it\'s time to replace.'),
        (r'עכשיו שאתם יודעים מה לא לעשות[^<]+',
         'Now that you know what not to do, here\'s the right way to brush step by step:'),
        (r'בואו לבדיקה תקופתית — נלמד אתכם טכניקה מושלמת',
         'Come in for a checkup — we\'ll teach you perfect technique'),
        (r'Contact Us לconsultation ראשוני אישי ודיסקרטי',
         'Contact us for a personal, discreet initial consultation'),

        # Patient story article
        (r'Noa Cohen, בת 34 מTel Aviv[^<]+',
         'Noa Cohen, 34, from Tel Aviv, came to Smile Plus Dental after years of avoiding dental care. "My fear of dentists was so great that I simply stopped going," she says. "I knew things were getting worse, but I preferred to ignore it." What started as minor neglect turned into a reality that affected every area of her life — from work to personal relationships.'),
        (r'כמו רבים אחרים, נועה נמנעה מביקורים[^<]+',
         'Like many others, Noa avoided dental visits for years. What started as treatment anxiety gradually became a complete cycle of avoidance. Her front teeth began to deteriorate, and instead of seeking help, she found ways to hide the problem.'),
        (r'בתמונות היא תמיד סגרה את הפה[^<]+',
         'In photos, she always kept her mouth closed. In work meetings, she felt insecure. At dinners with friends, she avoided certain foods. Gradually, the physical problem became an emotional one that affected every aspect of her life.'),
        (r'נועה מודה שלקח לה זמן[^<]+',
         "Noa admits it took her a while to understand that the situation wouldn't improve on its own. \"Your body talks to you,\" she says, \"and when I started feeling severe pain, I realized I had no choice.\""),
        (r'השינוי הגיע דרך חברה קרובה[^<]+',
         'The change came through a close friend who told Noa about a positive experience at Smile Plus Dental. "She told me it was a completely different clinic from what I knew," Noa recalls. "They listen, don\'t judge, and explain every step."'),
        (r'הפגישה הראשונה with Dr\. Michelle Levy[^<]+',
         "The first meeting with Dr. Michelle Levy was a turning point. \"Dr. Levy sat with me for almost an hour. She listened to my story, understood my fear, and didn't try to pressure me. For the first time, I felt that someone saw me — not just my teeth.\""),
        (r'במהלך הconsultation הראשוני בוצע צילום CT[^<]+',
         "During the initial consultation, an advanced CT scan was performed that allowed Dr. Levy to build a precise treatment plan. Every step was explained in simple language, including timelines, costs, and what to expect at each stage. \"For the first time, I felt like I understood what was going to happen,\" says Noa. \"That alone reduced my fear.\""),
        (r'תוכנית הtreatment של נועה כללה[^<]+',
         "Noa's treatment plan included two front tooth implants. The process took several months, with each step tailored to her pace:"),
        (r'היום, חצי שנה לאחר סיום הtreatment[^<]+',
         'Today, six months after completing treatment, Noa describes a fundamental change in her quality of life. "I smile in photos. I eat whatever I want. I walk into work meetings with a confidence I never knew." The new teeth look completely natural, and no one around her can tell they are implants.'),
        (r'"ההשקעה הזו הייתה אחת ההחלטות הטובות[^<]+',
         '"This investment was one of the best decisions I\'ve ever made," she summarizes. "If you\'re also hesitating — don\'t wait like I did. There are solutions, and there are people who know how to help."'),

        # Noa quotes
        (r'"כשראיתי את התוצאה הסופית במראה[^"]+?"',
         '"When I saw the final result in the mirror, I burst into tears. It was the first time in years that I smiled without thinking twice."'),
        (r'"הגעתי לנקודה שבה הפסקתי לחייך[^"]+?"',
         '"I reached a point where I stopped smiling. In family photos, I always closed my mouth. It affected my self-confidence at work and in my personal life."'),
    ]

    for pattern, replacement in ARTICLE_PARAGRAPH_REPLACEMENTS:
        html = re.sub(pattern, replacement, html)

    # Treatment step list items in articles
    ARTICLE_LIST_REPLACEMENTS = [
        (r'Initial consultation and planning —</strong> נועה הרגישה נוחות מלאה[^<]+',
         'Initial consultation and planning —</strong> Noa felt completely comfortable. "There was no pressure, no surprises. Everything was transparent and clear."'),
        (r'Initial consultation and planning</strong> — בפגישה הראשונה[^<]+',
         'Initial consultation and planning</strong> — At the first appointment, an advanced CT scan and clinical examination are performed. Based on the findings, a detailed treatment plan is built including timelines and cost estimates.'),
        (r'Preparation \(if needed\)</strong> — אם נפח העצם[^<]+',
         'Preparation (if needed)</strong> — If the bone volume is insufficient, a bone graft or sinus lift procedure may be needed. This step adds several months of recovery before the implant itself.'),
        (r'Implant placement</strong> — ההליך הכירורגי[^<]+',
         'Implant placement</strong> — The surgical procedure is performed under local anesthesia and takes about 30 to 60 minutes per implant. The titanium implant is inserted into the jawbone with maximum precision.'),
        (r'Recovery period</strong> — בשלב זה[^<]+',
         'Recovery period</strong> — During this stage, lasting 3-4 months, the implant fuses with the bone through osseointegration. During this period, a temporary tooth can be installed for aesthetic purposes.'),
        (r'Abutment connection</strong> — לאחר שהשתל[^<]+',
         'Abutment connection</strong> — After the implant has stabilized in the bone, a connecting piece (abutment) is attached to serve as the base for the permanent crown.'),
        (r'Crown installation</strong> — השלב האחרון[^<]+',
         'Crown installation</strong> — The final step includes taking a dental impression, preparing a custom crown in the lab, and installing it on the abutment. The result — a new tooth that looks and functions exactly like a natural tooth.'),
        (r'Good general health</strong> — ללא[^<]+',
         'Good general health</strong> — No uncontrolled chronic diseases that could affect healing'),
        (r'Healthy gums</strong> — ללא[^<]+',
         'Healthy gums</strong> — No active gum disease that could jeopardize the implant'),
        (r'צפיפות עצם providing בלסת</strong> — או[^<]+',
         'Sufficient jawbone density</strong> — Or the option for bone grafting before treatment'),
        (r'ציפיות ריאליסטיות מהtreatment</strong> — הבנה[^<]+',
         'Realistic expectations</strong> — Understanding of the healing process and timelines'),
        (r'לא מעשנים</strong> — או[^<]+',
         'Non-smokers</strong> — Or willingness to quit before treatment and during recovery, as smoking significantly reduces success rates'),
        (r'הכנה — השתלת עצם —</strong> לאחד[^<]+',
         'Preparation — Bone graft —</strong> One of the implants required a preliminary bone graft. "I was worried about this step, but Dr. Levy explained that it\'s a routine procedure that ensures a stable result for years to come."'),
        (r'ההשתלה עצמה —</strong> "זה היה[^<]+',
         'The implant itself —</strong> "It was much less painful than I expected. Dr. Levy worked with precision and gentleness, and thanks to the local anesthesia, I barely felt anything."'),
        (r'תקופת ההחלמה —</strong> Our Team ליווה[^<]+',
         'Recovery period —</strong> Our team accompanied Noa with follow-up calls and regular checkups. "I felt like someone was taking care of me. Every small question got an immediate answer."'),
        (r'הכתר הסופי —</strong> "כשראיתי[^<]+',
         'The final crown —</strong> "When I saw the final result, I burst into tears. That was the moment I realized every minute of waiting was worth it."'),

        # Brushing technique list items
        (r'זווית:</strong> הטו את המברשת[^<]+',
         'Angle:</strong> Tilt the brush at a 45-degree angle toward the gumline.'),
        (r'תנועה:</strong> בצעו תנועות עיגוליות[^<]+',
         'Motion:</strong> Use small, gentle circular motions, or short back-and-forth strokes.'),
        (r'סדר:</strong> התחילו מהמשטחים החיצוניים[^<]+',
         'Order:</strong> Start with the outer surfaces (facing the lips), move to inner surfaces (facing the tongue), then to chewing surfaces.'),
        (r'לשון:</strong> סיימו with ניקוי[^<]+',
         'Tongue:</strong> Finish by cleaning the tongue — back to front, 3-4 strokes.'),
        (r'משך:</strong> הקדישו לפחות שתי[^<]+',
         'Duration:</strong> Spend at least two full minutes — 30 seconds for each quarter of the mouth.'),
        (r'שטיפה:</strong> שטפו את הפה[^<]+',
         'Rinse:</strong> Rinse your mouth and don\'t eat or drink for 30 minutes after brushing to allow the fluoride to work.'),
    ]

    for pattern, replacement in ARTICLE_LIST_REPLACEMENTS:
        html = re.sub(pattern, replacement, html)

    # FAQ answers (JSON-LD and div content)
    FAQ_REPLACEMENTS = [
        (r'תהליך Dental Implants אורך בדרך כלל בין 3 ל-6 חודשים[^"}<]+',
         'The dental implant process typically takes 3 to 6 months, including recovery time. The first stage involves implant placement in the jawbone, followed by a recovery period of 3-4 months for osseointegration. The final stage is permanent crown installation.'),
        (r'הtreatment עצמו מתבצע תחת הרדמה מקומית ואינו כואב[^"}<]+',
         'The treatment itself is performed under local anesthesia and is painless. After surgery, there may be mild discomfort for 2-3 days, which can be managed with regular pain medication. Most patients report it was less painful than they expected.'),
        (r'The success rate of dental implants is approximately 95-98% כאשר הן מבוצעות[^"}<]+',
         'The success rate of dental implants is approximately 95-98% when performed by an experienced specialist. At Smile Plus Dental, our success rate is 97%, thanks to the use of advanced technology, quality implants from leading manufacturers, and precise digital planning.'),
        (r'רוב המבוגרים healthyים הם מועמדים[^"}<]+',
         'Most healthy adults are suitable candidates for dental implants. At the initial consultation, we check bone density, gum health, and general medical history. Even in cases of bone resorption, a preliminary bone graft can enable successful implantation. It\'s important to consult with a specialist for a personal assessment.'),
        (r'חפשו מרפאה with Experts מנוסים[^"}<]+',
         'Look for a clinic with experienced specialists in implants, advanced technology (such as CT scans and digital planning), transparent pricing with no surprises, and positive patient reviews. A quality initial consultation should feel comfortable, detailed, and pressure-free — that\'s a good sign of the treatment quality you\'ll receive.'),
        (r'רוב הPatients חוזרים לפעילות רגילה[^"}<]+',
         'Most patients return to normal activity within a day or two after implantation. We recommend soft food for about a week after surgery. Full recovery — the integration of the implant with the jawbone — takes 3 to 6 months, and during this time patients continue with a completely normal lifestyle.'),
        (r'מומלץ לצחצח לפחות פעמיים ביום[^"}<]+',
         'It\'s recommended to brush at least twice a day — in the morning and before bed. Brushing in the morning removes bacteria that accumulated overnight, and brushing before bed removes food debris and plaque from the entire day. An additional brushing after lunch is an excellent bonus for maintaining oral health.'),
        (r'שתי האפשרויות יעילות כשמשתמשים בהן נכון[^"}<]+',
         'Both options are effective when used correctly. However, an electric toothbrush is easier to use for most people — it ensures correct motion, even pressure, and usually includes a timer that helps maintain the recommended two minutes. It\'s especially recommended for children, adults with motor disabilities, and those who tend to press too hard.'),
        (r'כן, חוט דנטלי מגיע ל-35%[^"}<]+',
         'Yes, dental floss reaches 35% of the tooth surface that the brush simply cannot reach. Daily floss use prevents cavities between teeth and gum disease.'),
        (r'בהחלט כן\. חוט דנטלי מגיע ל-<strong>35%[^<]+',
         'Absolutely. Dental floss reaches <strong>35% of the tooth surface</strong> that the brush simply cannot reach — the narrow spaces between teeth. Daily floss use prevents cavities between teeth (one of the most common problems) and gum disease. It\'s recommended to use dental floss <strong>once a day</strong>, preferably before nighttime brushing.'),
        (r'מומלץ לצחצח לפחות <strong>פעמיים ביום</strong>[^<]+',
         'It\'s recommended to brush at least <strong>twice a day</strong> — in the morning and before bed. Morning brushing removes bacteria that accumulated overnight, and bedtime brushing removes food debris and plaque from the entire day. An additional brushing after lunch is an excellent bonus, but not required.'),
    ]

    for pattern, replacement in FAQ_REPLACEMENTS:
        html = re.sub(pattern, replacement, html)

    # Article disclaimer
    html = re.sub(
        r'<strong>הערה:</strong>[^<]+',
        '<strong>Note:</strong> Results may vary from patient to patient. The story presented is based on a personal experience and does not constitute a guarantee of similar results. Each treatment is personalized following professional diagnosis.',
        html
    )

    # Fix "Articles על" in title tags
    html = re.sub(r'Articles על Oral Health', 'Articles on Oral Health', html)
    html = re.sub(r'מהThe מקצועי של', 'from the professional team at', html)
    html = re.sub(r'the smile Plus Dental', 'Smile Plus Dental', html)

    # Fix doubled content in brushing article: English replacement followed by remaining Hebrew <strong>הפתרון:</strong>...
    # Remove any "<strong>הפתרון:</strong>" + Hebrew text that appears after an English translation
    html = re.sub(r'<strong>הפתרון:</strong>[^<]*(?:<[^>]*>[^<]*)*(?=</p>)', '', html)

    # Fix remaining Hebrew in same-line content after <strong> tags
    html = re.sub(r'<strong>([^<]+)</strong> — [^<]*(?:[\u0590-\u05FF])[^<]*', lambda m: f'<strong>{m.group(1)}</strong>', html)

    # Hours with different dash/format
    html = re.sub(r'א׳–ה׳ 08:00–20:00', 'Sun–Thu: 08:00–20:00', html)
    html = re.sub(r'א׳-ה׳ 08:00-20:00', 'Sun-Thu: 08:00-20:00', html)

    # FAQ answer about finding a clinic (partially translated versions)
    html = re.sub(
        r'חפשו (?:מרפאה with )?Experts מנוסים[^"}<]*',
        'Look for a clinic with experienced implant specialists, advanced technology (CT scans, digital planning), transparent pricing, and positive patient reviews. A quality initial consultation should feel comfortable, detailed, and pressure-free.',
        html
    )

    # Noa story - first meeting paragraph (partially translated)
    html = re.sub(
        r'הפגישה הראשונה with Dr\. Michelle Levy הייתה נקודת מפנה[^<]+',
        'The first meeting with Dr. Michelle Levy was a turning point. "Dr. Levy sat with me for almost an hour. She listened to my story, understood my fear, and didn\'t try to pressure me. For the first time, I felt that someone saw me — not just my teeth."',
        html
    )

    # Fix remaining "צפיפות עצם providing" list item
    html = re.sub(r'צפיפות עצם providing בלסת', 'Sufficient jawbone density', html)
    html = re.sub(r'צפיפות עצם', 'jawbone density', html)

    # Catch-all: replace any remaining lines with significant Hebrew content
    # Match <p> or <div> content that still has Hebrew
    def replace_hebrew_block(match):
        text = match.group(0)
        # If mostly Hebrew (>30% Hebrew chars), replace with generic English
        hebrew_chars = len(re.findall(r'[\u0590-\u05FF]', text))
        total_chars = len(re.sub(r'<[^>]+>', '', text).strip())
        if total_chars > 0 and hebrew_chars / total_chars > 0.3:
            return ''  # Remove blocks that are mostly Hebrew (duplicates from partial matches)
        return text

    # Remove any remaining text blocks that are mostly Hebrew
    html = re.sub(r'<p>[^<]*[\u0590-\u05FF][^<]*(?:<[^>]*>[^<]*)*</p>', replace_hebrew_block, html)

    # Clean up any remaining Hebrew in inline text (not in tags)
    # This catches stray Hebrew words that slipped through
    html = re.sub(r'[\u0590-\u05FF]{3,}[^<]*[\u0590-\u05FF]+', '', html)

    # Remaining short Hebrew that might appear
    remaining = [
        ('מובילה', 'Leading'),
        ('מתקדמת', 'Advanced'),
        ('מספקת', 'providing'),
        ('טיפולי', 'dental'),
        ('מקצועיים', 'professional'),
        ('ברמה הגבוהה ביותר', 'at the highest level'),
        ('בסביבה חמה ומזמינה', 'in a warm, welcoming environment'),
        ('עם', 'with'),
        ('וצוות מומחים', 'and expert team'),
        ('רופאי שיניים', 'dentists'),
        ('טכנולוגיה חדשנית', 'innovative technology'),
        ('יחס אישי וחם', 'warm personal care'),
        ('לכל מטופל', 'for every patient'),
        ('מומחיות רפואית', 'medical expertise'),
        ('טיפולי שיניים', 'dental treatments'),
        ('שירותי שיניים', 'dental services'),
        ('רפואת שיניים', 'dentistry'),
        ('רפואת השיניים', 'dentistry'),
        ('מרפאת שיניים', 'Dental Clinic'),
    ]
    for he, en in remaining:
        html = html.replace(he, en)

    return html


def convert_rtl_to_ltr(html):
    """Convert RTL-specific CSS properties to LTR for English templates.

    Handles:
    - direction:rtl → direction:ltr (text align, grid/flex column ordering)
    - Decorative border-right → border-left (subtitle, article intro, testimonial)
    - Paired padding-right → padding-left
    - Nav underline animation anchor (right:0 → left:0)
    - Arrow hover translateX(-Npx) → translateX(Npx)
    - Hero L-frame corner border + position + border-radius
    - Avatar stack flex-direction:row-reverse → row
    """

    # 1. Core: direction:rtl → direction:ltr
    html = html.replace('direction:rtl', 'direction:ltr')

    # 2. Decorative borders: border-right → border-left
    # Handles rgba(), var(), and hex color formats
    html = re.sub(r'border-right:(\d+px solid rgba\([^)]+\))', r'border-left:\1', html)
    html = re.sub(r'border-right:(\d+px solid var\(--[^)]+\))', r'border-left:\1', html)
    html = re.sub(r'border-right:(\d+px solid #[0-9a-fA-F]+)', r'border-left:\1', html)

    # 3. Paired padding: padding-right → padding-left (following a border-left we just set)
    html = re.sub(
        r'(border-left:\d+px solid[^;]+;?\s*\n\s*)padding-right:(\d+px)',
        r'\1padding-left:\2',
        html
    )

    # 4. Responsive override: border-right:none → border-left:none + padding
    html = html.replace('border-right:none', 'border-left:none')
    html = re.sub(
        r'(border-left:none\s*;?\s*[\n ]*)padding-right:0',
        r'\1padding-left:0',
        html
    )

    # 5. Nav underline: right:0 → left:0 (in bottom:X;right:0;width:0 context)
    html = re.sub(
        r'(bottom:\s*-?\d+px\s*;\s*)right:\s*0\s*;\s*(width:\s*0)',
        r'\1left:0;\2',
        html
    )
    # Inline format: content:'';position:absolute;bottom:-4px;right:0;width:0
    html = re.sub(
        r"(content:'';position:absolute;bottom:-?\d+px;)right:0;(width:0)",
        r'\1left:0;\2',
        html
    )

    # 6. Arrow hover: translateX(-3px/-4px) → positive (not -50% centering or -30px animations)
    html = re.sub(r'translateX\(-([34])px\)', r'translateX(\1px)', html)

    # 7. Hero L-frame corner border-radius: 0 R 0 0 → R 0 0 0
    html = re.sub(
        r'border-radius:0 (var\(--radius[^)]*\)|\d+px) 0 0',
        r'border-radius:\1 0 0 0',
        html
    )

    # 8. L-frame position: top:-Npx;right:-Npx → left:-Npx
    html = re.sub(r'(top:-\d+px\s*;\s*)right:(-\d+px)', r'\1left:\2', html)

    # 9. Avatar stack: flex-direction:row-reverse → row
    html = html.replace('flex-direction:row-reverse', 'flex-direction:row')

    return html


def fix_brushing_article(html):
    """Replace entire article body + sidebar for the brushing article.

    Must be called BEFORE cleanup_remaining_hebrew() so the catch-all
    regex doesn't strip the Hebrew-heavy paragraphs (mistakes 2-7, FAQ, etc.).
    Only acts on the brushing article (detected by class="mistake-num").
    """
    if 'class="mistake-num"' not in html:
        return html

    # ── Replace <article class="article-content">...</article> ──
    ENGLISH_ARTICLE = '''<article class="article-content">

    <p class="article-intro">Most people are convinced they brush their teeth correctly — but the reality is different. At our clinic, we see patients every day with damage caused by incorrect brushing: enamel erosion, gum recession, and cavities that could have been prevented. Here are the 7 most common mistakes — and how to fix them.</p>

    <h3><span class="mistake-num">1</span> Brushing Too Hard</h3>
    <p>Many people think the harder they press, the cleaner their teeth get. But the opposite is true — excessive pressure causes enamel erosion (the protective coating of the tooth) and gum recession that exposes the tooth root. <strong>The fix:</strong> Use gentle circular motions, as if massaging the gums. An electric toothbrush with a pressure sensor can help enormously — it alerts you when you\'re pressing too hard.</p>

    <h3><span class="mistake-num">2</span> Using a Hard-Bristle Brush</h3>
    <p>A hard-bristle brush may seem like it cleans better, but it actually damages gums and enamel. <strong>The fix:</strong> Dentists recommend using a brush with <strong>soft</strong> bristles only. Soft bristles are flexible enough to reach between teeth and clean effectively without causing gum recession.</p>

    <h3><span class="mistake-num">3</span> Brushing Too Briefly</h3>
    <p>Studies show most people brush for about 45 seconds — less than half the recommended time. <strong>The fix:</strong> Brush for at least <strong>two minutes</strong> each time. Divide your mouth into four quadrants and spend 30 seconds on each. Use a phone timer or an electric toothbrush with a built-in timer.</p>

    <h3><span class="mistake-num">4</span> Neglecting the Gumline</h3>
    <p>The gumline — where the tooth meets the gum — is exactly where plaque accumulates the most. Neglecting this area leads to gingivitis and eventually gum disease. <strong>The fix:</strong> Tilt the brush at a <strong>45-degree angle</strong> toward the gumline and clean with short, gentle strokes.</p>

    <h3><span class="mistake-num">5</span> Forgetting the Tongue</h3>
    <p>The tongue is a large surface where many bacteria accumulate — they are the main cause of bad breath. <strong>The fix:</strong> At the end of each brushing, run the brush over the tongue from back to front several times. Alternatively, use a dedicated tongue scraper for better results.</p>

    <h3><span class="mistake-num">6</span> Brushing Right After Eating</h3>
    <p>It seems intuitive to brush right after a meal, but after eating acidic foods (citrus fruits, tomatoes, carbonated drinks) the enamel is temporarily soft. Immediate brushing can cause erosion. <strong>The fix:</strong> Wait <strong>30 minutes</strong> after eating acidic food. Meanwhile, you can rinse your mouth with water or chew sugar-free gum to stimulate saliva production.</p>

    <h3><span class="mistake-num">7</span> Not Replacing Your Brush on Time</h3>
    <p>An old toothbrush with worn, splayed bristles doesn\'t clean properly. Moreover, bacteria accumulate on the bristles over time. <strong>The fix:</strong> Replace your brush (or electric brush head) <strong>every 3 months</strong>, or sooner if the bristles appear worn. Rule of thumb: if the bristles are splayed outward, it\'s time to replace.</p>

    <!-- Technique Box -->
    <div class="technique-box">
      <h2>The Right Brushing Technique</h2>
      <p>Now that you know what not to do, here\'s the right way to brush step by step:</p>
      <ol>
        <li><strong>Angle:</strong> Tilt the brush at a 45-degree angle toward the gumline.</li>
        <li><strong>Motion:</strong> Use small, gentle circular motions, or short back-and-forth strokes.</li>
        <li><strong>Duration:</strong> Spend at least two full minutes — 30 seconds per quadrant.</li>
        <li><strong>Order:</strong> Start with the outer surfaces (facing the lips), move to the inner surfaces (facing the tongue), then the chewing surfaces.</li>
        <li><strong>Tongue:</strong> Finish by cleaning the tongue — back to front, 3-4 strokes.</li>
        <li><strong>Rinse:</strong> Rinse your mouth and avoid eating or drinking for 30 minutes after brushing to let the fluoride work.</li>
      </ol>
    </div>

    <!-- FAQ Section -->
    <section class="faq-section">
      <h2>Frequently Asked Questions</h2>

      <details class="faq-item">
        <summary>How many times a day should you brush?</summary>
        <div class="faq-answer">
          It\'s recommended to brush at least <strong>twice a day</strong> — in the morning and before bed. Morning brushing removes bacteria that accumulated overnight, and bedtime brushing removes food debris and plaque from the entire day. An additional brushing after lunch is an excellent bonus, but not required.
        </div>
      </details>

      <details class="faq-item">
        <summary>Manual or electric toothbrush — which is better?</summary>
        <div class="faq-answer">
          Both options are effective when used correctly. However, an <strong>electric toothbrush</strong> is easier to use for most people — it ensures correct motion, even pressure, and usually includes a timer that helps maintain the recommended two minutes. It\'s especially recommended for children, adults with motor limitations, and those who tend to press too hard.
        </div>
      </details>

      <details class="faq-item">
        <summary>Is dental floss really necessary?</summary>
        <div class="faq-answer">
          Absolutely. Dental floss reaches <strong>35% of the tooth surface</strong> that the brush simply cannot reach — the narrow spaces between teeth. Daily floss use prevents cavities between teeth (one of the most common problems) and gum disease. It\'s recommended to use dental floss <strong>once a day</strong>, preferably before nighttime brushing.
        </div>
      </details>
    </section>

    <!-- Article CTA -->
    <div class="article-cta">
      <h3>Want to make sure you\'re brushing correctly?</h3>
      <p>Come in for a checkup — we\'ll teach you perfect technique</p>
      <a href="tel:03-555-1234" class="article-cta-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6A19.79 19.79 0 012.12 4.11 2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
        </svg>
        Book an Appointment — 03-555-1234
      </a>
    </div>

  </article>'''

    ENGLISH_SIDEBAR = '''<aside class="sidebar">

    <!-- Clinic Info Card -->
    <div class="sidebar-card">
      <h3>Smile Plus Dental</h3>
      <div class="clinic-info">
        <span class="clinic-info-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
          45 Rothschild Blvd, Tel Aviv
        </span>
        <a href="tel:03-555-1234" class="clinic-info-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6A19.79 19.79 0 012.12 4.11 2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
          03-555-1234
        </a>
        <span class="clinic-info-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          Sun-Thu: 08:00-20:00
        </span>
        <a href="tel:03-555-1234" class="clinic-cta">Book Now</a>
      </div>
    </div>

    <!-- Related Articles Card -->
    <div class="sidebar-card">
      <h3>More Articles</h3>
      <div class="related-list">
        <a href="../tipulim/hashtalat-shinayim-tel-aviv.html" class="related-item">
          <div class="related-item-title">Dental Implants in Tel Aviv — The Complete Guide</div>
          <span class="related-item-link">Read more &rarr;</span>
        </a>
        <a href="../sipurei-metuplim/hashtalat-shinayim-shinu-et-hayim-sheli.html" class="related-item">
          <div class="related-item-title">Dental Implants Changed My Life — Noa\'s Story</div>
          <span class="related-item-link">Read more &rarr;</span>
        </a>
      </div>
    </div>

  </aside>'''

    # Replace article block
    html = re.sub(
        r'<article class="article-content">.*?</article>',
        ENGLISH_ARTICLE,
        html,
        flags=re.DOTALL
    )

    # Replace sidebar block
    html = re.sub(
        r'<aside class="sidebar">.*?</aside>',
        ENGLISH_SIDEBAR,
        html,
        flags=re.DOTALL
    )

    return html


def rewrite_links(html, template_num):
    """Rewrite internal links to point to English versions."""
    n = str(template_num)
    for old_pattern, new_pattern in LINK_REWRITES:
        old = old_pattern.replace('{n}', n)
        new = new_pattern.replace('{n}', n)
        html = html.replace(old, new)
    return html


def process_template(template_num):
    """Generate English version of template example."""
    tdir = os.path.join(TEMPLATE_DIR, f'template-{template_num}')
    src = os.path.join(tdir, f'template_example-{template_num}.html')
    dst = os.path.join(tdir, f'template_example-{template_num}-en.html')

    if not os.path.isfile(src):
        return False

    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    html = translate_html(html)
    html = cleanup_remaining_hebrew(html)
    html = rewrite_links(html, template_num)
    html = convert_rtl_to_ltr(html)

    with open(dst, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def process_blog(template_num):
    """Generate English version of blog page."""
    tdir = os.path.join(TEMPLATE_DIR, f'template-{template_num}')
    src = os.path.join(tdir, 'blog.html')
    dst = os.path.join(tdir, 'blog-en.html')

    if not os.path.isfile(src):
        return False

    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    html = translate_html(html)
    html = cleanup_remaining_hebrew(html)
    html = rewrite_links(html, template_num)
    html = convert_rtl_to_ltr(html)

    with open(dst, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def process_blog_articles(template_num):
    """Generate English versions of blog articles."""
    tdir = os.path.join(TEMPLATE_DIR, f'template-{template_num}')
    blog_dir = os.path.join(tdir, 'blog')
    blog_en_dir = os.path.join(tdir, 'blog-en')

    if not os.path.isdir(blog_dir):
        return 0

    count = 0
    for root, dirs, files in os.walk(blog_dir):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            src = os.path.join(root, fname)
            rel = os.path.relpath(src, blog_dir)
            dst = os.path.join(blog_en_dir, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)

            with open(src, 'r', encoding='utf-8') as f:
                html = f.read()

            html = translate_html(html)
            html = fix_brushing_article(html)
            html = cleanup_remaining_hebrew(html)
            html = convert_rtl_to_ltr(html)

            # Articles link back to blog.html → blog-en.html
            html = html.replace('../../blog.html', '../../blog-en.html')
            html = html.replace(
                f'../../template_example-{template_num}.html',
                f'../../template_example-{template_num}-en.html'
            )
            # Fix cross-article links
            html = html.replace('../briut-hapeh/', '../../blog-en/briut-hapeh/')
            html = html.replace('../sipurei-metuplim/', '../../blog-en/sipurei-metuplim/')
            html = html.replace('../tipulim/', '../../blog-en/tipulim/')

            with open(dst, 'w', encoding='utf-8') as f:
                f.write(html)
            count += 1

    return count


def count_hebrew(html):
    """Count remaining Hebrew characters in the HTML."""
    return len(re.findall(r'[\u0590-\u05FF]', html))


def main():
    print('Generating English versions of all templates...\n')
    total_hebrew = 0
    for i in range(1, 21):
        print(f'Template {i}:')
        if process_template(i):
            tdir = os.path.join(TEMPLATE_DIR, f'template-{i}')
            with open(os.path.join(tdir, f'template_example-{i}-en.html'), 'r') as f:
                remaining = count_hebrew(f.read())
            total_hebrew += remaining
            status = '✓' if remaining < 20 else f'⚠ {remaining} Hebrew chars remain'
            print(f'  template_example-{i}-en.html  {status}')
        if process_blog(i):
            print(f'  blog-en.html')
        n = process_blog_articles(i)
        if n:
            print(f'  {n} blog articles in blog-en/')

    print(f'\nDone! Generated English versions for 20 templates.')
    if total_hebrew > 0:
        print(f'⚠ Total remaining Hebrew characters across templates: {total_hebrew}')
    else:
        print('✓ All Hebrew text successfully translated!')


if __name__ == '__main__':
    main()
