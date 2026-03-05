#!/usr/bin/env python3
"""Generate synthetic aiVisibility data for all clinic JSON files."""
import json
import os
import random
import hashlib
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'dashboard_admin', 'data')
CLINICS_DIR = os.path.join(DATA_DIR, 'clinics')

# Hebrew queries by city
QUERY_TEMPLATES = [
    "רופא שיניים {city}",
    "מרפאת שיניים {city}",
    "השתלת שיניים {city}",
    "יישור שיניים {city}",
    "הלבנת שיניים {city}",
    "רופא שיניים ילדים {city}",
    "טיפול שורש {city}",
    "כתרים וגשרים {city}",
    "שיניים תותבות {city}",
    "רופא שיניים חירום {city}",
    "ציפוי חרסינה {city}",
    "ניקוי אבנית {city}",
]

PLATFORMS = ['google_aio', 'chatgpt', 'perplexity', 'gemini']

PLATFORM_LABELS = {
    'google_aio': 'Google AI Overview',
    'chatgpt': 'ChatGPT',
    'perplexity': 'Perplexity',
    'gemini': 'Gemini',
}

OPTIMIZATION_CHECKS = [
    ('structured_data', 'סכמת נתונים מובנים (Schema.org)', 'high', 'מגדיל סיכוי להופעה ב-AI ב-40%'),
    ('nap_consistency', 'עקביות שם-כתובת-טלפון', 'high', 'בסיס לזיהוי עסק ע"י AI'),
    ('review_volume', 'נפח ביקורות (50+)', 'high', 'AI מעדיף עסקים עם ביקורות רבות'),
    ('review_recency', 'ביקורות עדכניות (30 יום)', 'medium', 'סיגנל עדכניות למנועי AI'),
    ('faq_content', 'תוכן שאלות נפוצות באתר', 'medium', 'תואם פורמט שאילתות AI'),
    ('local_citations', 'נוכחות במדריכים מקומיים', 'medium', 'מחזק אמינות מקור'),
    ('https_mobile', 'HTTPS + מותאם למובייל', 'low', 'דרישת בסיס לכל מנועי AI'),
    ('gbp_complete', 'פרופיל Google Business מלא', 'high', 'מקור ראשי ל-Google AIO'),
    ('topic_authority', 'סמכות תוכנית (3+ מאמרים)', 'medium', 'מחזק מומחיות בנושא'),
]


def seed_rng(clinic_id: int):
    """Deterministic random per clinic."""
    random.seed(hashlib.md5(f'geo-{clinic_id}-2026'.encode()).hexdigest())


def compute_base_score(clinic: dict) -> float:
    """Derive base AI score from real clinic signals."""
    rating = clinic.get('rating', 3.0)
    reviews = clinic.get('reviewCount', 0)
    site = clinic.get('siteScore', 0)
    onboarding = clinic.get('onboarding', [])
    ob_pct = sum(1 for o in onboarding if o.get('completed')) / max(len(onboarding), 1)

    # Weighted formula: rating (30%) + reviews (25%) + site (25%) + onboarding (20%)
    rating_score = (rating / 5.0) * 30
    review_score = min(reviews / 100, 1.0) * 25
    site_score = (site / 100) * 25
    ob_score = ob_pct * 20
    return rating_score + review_score + site_score + ob_score


def generate_platforms(base_score: float, city: str) -> list:
    """Generate platform coverage based on score."""
    platforms = []
    for p in PLATFORMS:
        # Higher score → more likely to be mentioned
        threshold = random.uniform(30, 55)
        if base_score >= threshold:
            mentioned = 'yes'
        elif base_score >= threshold - 15:
            mentioned = 'partial'
        else:
            mentioned = 'no'

        sentiment = None
        if mentioned != 'no':
            sentiment = random.choices(
                ['positive', 'neutral', 'negative'],
                weights=[60, 30, 10]
            )[0]

        # Sample queries that triggered mention
        n_queries = random.randint(1, 3) if mentioned != 'no' else 0
        sample_qs = random.sample(
            [q.format(city=city) for q in QUERY_TEMPLATES],
            min(n_queries, len(QUERY_TEMPLATES))
        )

        platforms.append({
            'platform': p,
            'mentioned': mentioned,
            'sentiment': sentiment,
            'sampleQueries': sample_qs,
        })
    return platforms


def generate_queries(city: str, platforms_data: list, competitors: list) -> list:
    """Generate query performance table."""
    n_queries = random.randint(5, 8)
    chosen = random.sample(QUERY_TEMPLATES, min(n_queries, len(QUERY_TEMPLATES)))
    queries = []
    for qt in chosen:
        query = qt.format(city=city)
        plat_results = {}
        for p in PLATFORMS:
            # Check if this platform mentions clinic at all
            pd = next((x for x in platforms_data if x['platform'] == p), None)
            if pd and pd['mentioned'] == 'yes':
                plat_results[p] = random.random() > 0.2
            elif pd and pd['mentioned'] == 'partial':
                plat_results[p] = random.random() > 0.5
            else:
                plat_results[p] = random.random() > 0.85

        comp_mentioned = [c['name'] for c in competitors if random.random() > 0.5]
        trend = random.choice(['up', 'down', 'stable', 'new'])
        queries.append({
            'query': query,
            'platforms': plat_results,
            'competitorsMentioned': comp_mentioned[:2],
            'trend': trend,
        })
    return queries


def generate_checklist(clinic: dict, base_score: float) -> list:
    """Generate optimization checklist correlated with clinic data."""
    checks = []
    onboarding = {o['key']: o['completed'] for o in clinic.get('onboarding', [])}
    reviews = clinic.get('reviewCount', 0)
    site = clinic.get('siteScore', 0)

    for key, label, priority, impact in OPTIMIZATION_CHECKS:
        # Determine completion based on real signals
        if key == 'review_volume':
            completed = reviews >= 50
        elif key == 'review_recency':
            completed = random.random() < 0.6 if reviews > 20 else random.random() < 0.2
        elif key == 'gbp_complete':
            completed = onboarding.get('gbp', False)
        elif key == 'https_mobile':
            completed = site >= 40
        elif key == 'structured_data':
            completed = site >= 60 and random.random() > 0.3
        elif key == 'nap_consistency':
            completed = random.random() < (base_score / 100)
        else:
            completed = random.random() < (base_score / 120)

        checks.append({
            'key': key,
            'label': label,
            'completed': completed,
            'priority': priority,
            'impact': impact,
        })
    return checks


def get_city_clinics() -> dict:
    """Build city → [clinic summary] mapping."""
    city_map = {}
    for fname in sorted(os.listdir(CLINICS_DIR)):
        if not fname.startswith('clinic-') or not fname.endswith('.json'):
            continue
        fpath = os.path.join(CLINICS_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            c = json.load(f)
        city = c.get('city', '?')
        if city not in city_map:
            city_map[city] = []
        city_map[city].append({
            'id': c['id'],
            'name': c['name'],
            'rating': c.get('rating', 3.0),
            'reviewCount': c.get('reviewCount', 0),
            'siteScore': c.get('siteScore', 0),
        })
    return city_map


def generate_competitors(clinic_id: int, city: str, city_clinics: dict) -> list:
    """Pick 2-3 competitors from same city."""
    same_city = [c for c in city_clinics.get(city, []) if c['id'] != clinic_id]
    if not same_city:
        return []
    n = min(random.randint(2, 3), len(same_city))
    chosen = random.sample(same_city, n)
    competitors = []
    for c in chosen:
        seed_rng(c['id'])
        comp_base = compute_base_score({
            'rating': c['rating'],
            'reviewCount': c['reviewCount'],
            'siteScore': c['siteScore'],
            'onboarding': [],
        })
        noise = random.uniform(-8, 8)
        score = max(10, min(95, round(comp_base + noise)))
        competitors.append({
            'name': c['name'],
            'aiScore': score,
            'platformsCovered': random.randint(1, 4),
            'shareOfVoice': round(random.uniform(5, 35), 1),
        })
    # Reset RNG for the original clinic
    seed_rng(clinic_id)
    return competitors


def main():
    city_clinics = get_city_clinics()
    updated = 0

    for fname in sorted(os.listdir(CLINICS_DIR)):
        if not fname.startswith('clinic-') or not fname.endswith('.json'):
            continue
        fpath = os.path.join(CLINICS_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            clinic = json.load(f)

        clinic_id = clinic['id']
        city = clinic.get('city', 'תל אביב')
        seed_rng(clinic_id)

        base_score = compute_base_score(clinic)
        noise = random.uniform(-8, 8)
        overall = max(10, min(95, round(base_score + noise)))

        # Last week score is close but different
        last_week = max(5, min(95, overall + random.randint(-5, 5)))
        if overall > last_week:
            trend = 'up'
        elif overall < last_week:
            trend = 'down'
        else:
            trend = 'stable'

        competitors = generate_competitors(clinic_id, city, city_clinics)
        seed_rng(clinic_id)  # Re-seed after competitor generation
        platforms = generate_platforms(base_score, city)
        queries = generate_queries(city, platforms, competitors)
        checklist = generate_checklist(clinic, base_score)

        clinic['aiVisibility'] = {
            'overallScore': overall,
            'scoreTrend': trend,
            'scoreLastWeek': last_week,
            'platforms': platforms,
            'queries': queries,
            'optimizationChecklist': checklist,
            'competitors': competitors,
            'lastUpdated': '2026-03-03T08:00:00Z',
        }

        # Atomic write
        tmp = fpath + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(clinic, f, indent=2, ensure_ascii=False)
        os.replace(tmp, fpath)
        updated += 1

    print(f'Updated {updated} clinic files with aiVisibility data.')


if __name__ == '__main__':
    main()
