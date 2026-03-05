'use client';

import { useT } from '@/lib/i18n';

export default function LangToggle() {
  const { lang, setLang } = useT();

  return (
    <button
      onClick={() => setLang(lang === 'he' ? 'en' : 'he')}
      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-card border border-border hover:border-border-hover text-xs text-dim hover:text-foreground transition-colors"
      title={lang === 'he' ? 'Switch to English' : 'עבור לעברית'}
    >
      <span className="text-sm">{lang === 'he' ? '🇬🇧' : '🇮🇱'}</span>
      <span>{lang === 'he' ? 'EN' : 'עב'}</span>
    </button>
  );
}
