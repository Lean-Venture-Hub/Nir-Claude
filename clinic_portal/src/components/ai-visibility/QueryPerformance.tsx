'use client';

import { useT } from '@/lib/i18n';
import type { AiQueryPerformance } from '@/types';

interface QueryPerformanceProps {
  queries: AiQueryPerformance[];
}

const PLATFORMS = ['google_aio', 'chatgpt', 'perplexity', 'gemini'] as const;
const PLATFORM_SHORT: Record<string, string> = {
  google_aio: 'AIO',
  chatgpt: 'GPT',
  perplexity: 'Perp',
  gemini: 'Gem',
};

export default function QueryPerformance({ queries }: QueryPerformanceProps) {
  const { t } = useT();

  const trendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return <span className="text-success">↑</span>;
      case 'down': return <span className="text-error">↓</span>;
      case 'new': return <span className="text-info">●</span>;
      default: return <span className="text-dim">→</span>;
    }
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-6 fade-up">
      <h2 className="font-heading text-sm font-semibold text-dim mb-4">{t('ai.queryPerformance')}</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-border text-dim">
              <th className="text-start py-2 pe-4 font-medium">{t('ai.query')}</th>
              {PLATFORMS.map((p) => (
                <th key={p} className="text-center py-2 px-2 font-medium">{PLATFORM_SHORT[p]}</th>
              ))}
              <th className="text-center py-2 ps-2 font-medium">{t('ai.trend')}</th>
            </tr>
          </thead>
          <tbody>
            {queries.map((q, i) => (
              <tr key={i} className="border-b border-border/50 hover:bg-background/50">
                <td className="py-2.5 pe-4 font-body">{q.query}</td>
                {PLATFORMS.map((p) => (
                  <td key={p} className="text-center py-2.5 px-2">
                    {q.platforms[p]
                      ? <span className="text-success font-bold">✓</span>
                      : <span className="text-dim">✗</span>
                    }
                  </td>
                ))}
                <td className="text-center py-2.5 ps-2">{trendIcon(q.trend)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
