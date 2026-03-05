'use client';

import { useT } from '@/lib/i18n';
import type { AiPlatformCoverage } from '@/types';

interface PlatformCoverageProps {
  platforms: AiPlatformCoverage[];
}

const platformMeta: Record<string, { icon: string; label: string }> = {
  google_aio: { icon: '🔍', label: 'Google AIO' },
  chatgpt: { icon: '💬', label: 'ChatGPT' },
  perplexity: { icon: '🔎', label: 'Perplexity' },
  gemini: { icon: '✦', label: 'Gemini' },
};

export default function PlatformCoverage({ platforms }: PlatformCoverageProps) {
  const { t } = useT();

  const statusStyle = (mentioned: string) => {
    switch (mentioned) {
      case 'yes': return 'border-success/30 bg-success/5 text-success';
      case 'partial': return 'border-warning/30 bg-warning/5 text-warning';
      default: return 'border-error/30 bg-error/5 text-error';
    }
  };

  const statusLabel = (mentioned: string) => {
    switch (mentioned) {
      case 'yes': return t('ai.mentioned');
      case 'partial': return t('ai.partial');
      default: return t('ai.notMentioned');
    }
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-6 fade-up">
      <h2 className="font-heading text-sm font-semibold text-dim mb-4">{t('ai.platformCoverage')}</h2>
      <div className="grid grid-cols-2 gap-3">
        {platforms.map((p) => {
          const meta = platformMeta[p.platform] ?? { icon: '◈', label: p.platform };
          return (
            <div
              key={p.platform}
              className={`border rounded-xl p-4 ${statusStyle(p.mentioned)}`}
            >
              <div className="flex items-center gap-2 mb-2">
                <span className="text-lg">{meta.icon}</span>
                <span className="font-heading text-sm font-semibold">{meta.label}</span>
              </div>
              <span className="text-xs font-medium">{statusLabel(p.mentioned)}</span>
              {p.sentiment && (
                <div className="mt-1 text-[10px] opacity-70">
                  {p.sentiment === 'positive' ? '👍' : p.sentiment === 'negative' ? '👎' : '➖'}{' '}
                  {p.sentiment}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
