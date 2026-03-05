'use client';

import { createContext, useContext, useState, useCallback, useEffect } from 'react';
import React from 'react';

export type Lang = 'he' | 'en';

const translations = {
  // Navigation
  'nav.home': { he: 'ראשי', en: 'Home' },
  'nav.stories': { he: 'סטוריז', en: 'Stories' },
  'nav.reels': { he: 'רילס', en: 'Reels' },
  'nav.seo': { he: 'SEO', en: 'SEO' },
  'nav.calendar': { he: 'לוח שנה', en: 'Calendar' },
  'nav.settings': { he: 'הגדרות', en: 'Settings' },

  // Home
  'home.welcome': { he: 'ברוך הבא', en: 'Welcome' },
  'home.storiesReady': { he: 'סטוריז מוכנים', en: 'Stories Ready' },
  'home.reelsReady': { he: 'רילס מוכנים', en: 'Reels Ready' },
  'home.seoPublished': { he: 'פוסטים שפורסמו', en: 'Posts Published' },
  'home.needsAttention': { he: 'דורש תשומת לב', en: 'Needs Attention' },
  'home.onboarding': { he: 'הגדרת חשבון', en: 'Account Setup' },
  'home.liveFeed': { he: 'פעילות אחרונה', en: 'Recent Activity' },

  // Actions
  'action.approve': { he: 'אישור', en: 'Approve' },
  'action.reject': { he: 'דחייה', en: 'Reject' },
  'action.edit': { he: 'עריכה', en: 'Edit' },
  'action.save': { he: 'שמירה', en: 'Save' },
  'action.cancel': { he: 'ביטול', en: 'Cancel' },
  'action.upload': { he: 'העלאה', en: 'Upload' },
  'action.swap': { he: 'החלפת תבנית', en: 'Swap Template' },
  'action.bulkApprove': { he: 'אישור הכל', en: 'Approve All' },
  'action.requestRevision': { he: 'בקשת תיקון', en: 'Request Revision' },
  'action.pause': { he: 'השהייה', en: 'Pause' },
  'action.resume': { he: 'המשך', en: 'Resume' },

  // Status
  'status.pending': { he: 'ממתין', en: 'Pending' },
  'status.generated': { he: 'נוצר', en: 'Generated' },
  'status.approved': { he: 'אושר', en: 'Approved' },
  'status.rejected': { he: 'נדחה', en: 'Rejected' },
  'status.published': { he: 'פורסם', en: 'Published' },
  'status.failed': { he: 'נכשל', en: 'Failed' },
  'status.scripted': { he: 'תסריט מוכן', en: 'Scripted' },
  'status.draft': { he: 'טיוטה', en: 'Draft' },
  'status.active': { he: 'פעיל', en: 'Active' },
  'status.paused': { he: 'מושהה', en: 'Paused' },

  // Stories
  'stories.title': { he: 'סטוריז שבועי', en: 'Weekly Stories' },
  'stories.week': { he: 'שבוע', en: 'Week' },
  'stories.caption': { he: 'כיתוב', en: 'Caption' },
  'stories.template': { he: 'תבנית', en: 'Template' },
  'stories.photo': { he: 'תמונה', en: 'Photo' },
  'stories.bulkApprove': { he: 'אישור כל הסטוריז בשבוע', en: 'Approve All Stories This Week' },

  // Reels
  'reels.title': { he: 'רילס', en: 'Reels' },
  'reels.script': { he: 'תסריט', en: 'Script' },
  'reels.video': { he: 'וידאו', en: 'Video' },
  'reels.approveScript': { he: 'אישור תסריט', en: 'Approve Script' },
  'reels.approveVideo': { he: 'אישור וידאו', en: 'Approve Video' },

  // SEO
  'seo.title': { he: 'SEO ותוכן', en: 'SEO & Content' },
  'seo.channel': { he: 'ערוץ', en: 'Channel' },
  'seo.posts': { he: 'פוסטים', en: 'Posts' },
  'seo.planned': { he: 'מתוכנן', en: 'Planned' },
  'seo.published': { he: 'פורסם', en: 'Published' },

  // Calendar
  'calendar.title': { he: 'לוח תוכן', en: 'Content Calendar' },
  'calendar.dragToReschedule': { he: 'גרור לשינוי תאריך', en: 'Drag to reschedule' },

  // Settings
  'settings.title': { he: 'הגדרות', en: 'Settings' },
  'settings.photoVault': { he: 'גלריית תמונות', en: 'Photo Vault' },
  'settings.brandColors': { he: 'צבעי מותג', en: 'Brand Colors' },
  'settings.toneOfVoice': { he: 'טון דיבור', en: 'Tone of Voice' },
  'settings.autoApprove': { he: 'אישור אוטומטי', en: 'Auto Approve' },
  'settings.notifications': { he: 'התראות', en: 'Notifications' },

  // SEO Channels
  'channel.blog': { he: 'בלוג', en: 'Blog' },
  'channel.twitter': { he: 'טוויטר', en: 'Twitter' },
  'channel.reddit': { he: 'רדיט', en: 'Reddit' },
  'channel.quora': { he: 'קוורה', en: 'Quora' },
  'channel.gbp': { he: 'Google Business', en: 'Google Business' },

  // AI Visibility
  'ai.title': { he: 'נראות AI', en: 'AI Visibility' },
  'ai.subtitle': { he: 'איך מנועי AI רואים את המרפאה שלך', en: 'How AI engines see your clinic' },
  'ai.score': { he: 'ציון AI', en: 'AI Score' },
  'ai.scoreOf100': { he: 'מתוך 100', en: 'out of 100' },
  'ai.vsLastWeek': { he: 'לעומת שבוע שעבר', en: 'vs last week' },
  'ai.platformCoverage': { he: 'כיסוי פלטפורמות', en: 'Platform Coverage' },
  'ai.queryPerformance': { he: 'ביצועי שאילתות', en: 'Query Performance' },
  'ai.optimization': { he: 'רשימת אופטימיזציה', en: 'Optimization Checklist' },
  'ai.competitors': { he: 'השוואת מתחרים', en: 'Competitor Comparison' },
  'ai.mentioned': { he: 'מוזכר', en: 'Mentioned' },
  'ai.partial': { he: 'חלקי', en: 'Partial' },
  'ai.notMentioned': { he: 'לא מוזכר', en: 'Not Mentioned' },
  'ai.query': { he: 'שאילתה', en: 'Query' },
  'ai.trend': { he: 'מגמה', en: 'Trend' },
  'ai.high': { he: 'גבוה', en: 'High' },
  'ai.medium': { he: 'בינוני', en: 'Medium' },
  'ai.low': { he: 'נמוך', en: 'Low' },
  'ai.completed': { he: 'הושלמו', en: 'Completed' },
  'ai.shareOfVoice': { he: 'נתח קול', en: 'Share of Voice' },
  'ai.yourClinic': { he: 'המרפאה שלך', en: 'Your Clinic' },
  'ai.lastUpdated': { he: 'עודכן לאחרונה', en: 'Last updated' },
  'ai.viewDetails': { he: 'צפייה בפרטים', en: 'View Details' },
  'ai.back': { he: 'חזרה', en: 'Back' },
  'ai.platforms': { he: 'פלטפורמות', en: 'Platforms' },

  // General
  'general.loading': { he: 'טוען...', en: 'Loading...' },
  'general.error': { he: 'שגיאה', en: 'Error' },
  'general.notFound': { he: 'לא נמצא', en: 'Not Found' },
  'general.invalidToken': { he: 'קישור לא תקין', en: 'Invalid Link' },
  'general.day': { he: 'יום', en: 'Day' },
  'general.week': { he: 'שבוע', en: 'Week' },
} as const;

export type TranslationKey = keyof typeof translations;

interface LangContextValue {
  lang: Lang;
  setLang: (lang: Lang) => void;
  t: (key: TranslationKey) => string;
  dir: 'rtl' | 'ltr';
}

const LangContext = createContext<LangContextValue>({
  lang: 'he',
  setLang: () => {},
  t: (key) => key,
  dir: 'rtl',
});

export function LangProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLangState] = useState<Lang>('he');

  useEffect(() => {
    const saved = localStorage.getItem('portal-lang') as Lang | null;
    if (saved === 'en' || saved === 'he') setLangState(saved);
  }, []);

  const setLang = useCallback((newLang: Lang) => {
    setLangState(newLang);
    localStorage.setItem('portal-lang', newLang);
    document.documentElement.lang = newLang;
    document.documentElement.dir = newLang === 'he' ? 'rtl' : 'ltr';
  }, []);

  const t = useCallback(
    (key: TranslationKey) => translations[key]?.[lang] ?? key,
    [lang]
  );

  const dir = lang === 'he' ? 'rtl' : 'ltr';

  return React.createElement(
    LangContext.Provider,
    { value: { lang, setLang, t, dir } },
    children
  );
}

export function useT() {
  return useContext(LangContext);
}
