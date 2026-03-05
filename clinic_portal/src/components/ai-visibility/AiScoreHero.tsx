'use client';

import { useT } from '@/lib/i18n';
import type { AiVisibilityData } from '@/types';

interface AiScoreHeroProps {
  data: AiVisibilityData;
}

export default function AiScoreHero({ data }: AiScoreHeroProps) {
  const { t } = useT();
  const delta = data.overallScore - data.scoreLastWeek;
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (data.overallScore / 100) * circumference;

  const scoreColor =
    data.overallScore >= 70 ? 'var(--success)' :
    data.overallScore >= 40 ? 'var(--warning, #f59e0b)' :
    'var(--error)';

  return (
    <div className="bg-card border border-border rounded-2xl p-6 fade-up">
      <h2 className="font-heading text-sm font-semibold text-dim mb-4">{t('ai.score')}</h2>
      <div className="flex items-center gap-8">
        {/* Circular progress */}
        <div className="relative w-32 h-32 shrink-0">
          <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="54" fill="none" stroke="var(--border)" strokeWidth="8" />
            <circle
              cx="60" cy="60" r="54" fill="none"
              stroke={scoreColor}
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              className="transition-all duration-1000"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="font-heading text-3xl font-bold" style={{ color: scoreColor }}>
              {data.overallScore}
            </span>
            <span className="text-[10px] text-dim">{t('ai.scoreOf100')}</span>
          </div>
        </div>

        {/* Trend info */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className={`text-lg ${
              data.scoreTrend === 'up' ? 'text-success' :
              data.scoreTrend === 'down' ? 'text-error' :
              'text-dim'
            }`}>
              {data.scoreTrend === 'up' ? '↑' : data.scoreTrend === 'down' ? '↓' : '→'}
            </span>
            <span className="text-sm font-body">
              {delta > 0 ? '+' : ''}{delta} {t('ai.vsLastWeek')}
            </span>
          </div>
          <p className="text-xs text-dim">{t('ai.subtitle')}</p>
        </div>
      </div>
    </div>
  );
}
