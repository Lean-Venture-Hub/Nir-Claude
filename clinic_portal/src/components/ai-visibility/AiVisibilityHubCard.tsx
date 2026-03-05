'use client';

import Link from 'next/link';
import { useT } from '@/lib/i18n';
import type { AiVisibilityData } from '@/types';

interface AiVisibilityHubCardProps {
  data: AiVisibilityData;
  basePath: string;
}

export default function AiVisibilityHubCard({ data, basePath }: AiVisibilityHubCardProps) {
  const { t } = useT();
  const delta = data.overallScore - data.scoreLastWeek;
  const mentionedCount = data.platforms.filter((p) => p.mentioned !== 'no').length;

  const scoreColor =
    data.overallScore >= 70 ? 'text-success' :
    data.overallScore >= 40 ? 'text-warning' :
    'text-error';

  return (
    <Link
      href={`${basePath}/seo/ai-visibility`}
      className="bg-card border border-accent/30 rounded-2xl p-5 hover:border-accent transition-colors fade-up block group"
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-xl">🤖</span>
          <span className="font-heading text-sm font-semibold group-hover:text-accent transition-colors">
            {t('ai.title')}
          </span>
        </div>
        <span className="text-xs text-accent font-medium">{t('ai.viewDetails')} →</span>
      </div>

      <div className="flex items-center gap-6">
        {/* Score */}
        <div>
          <span className={`font-heading text-3xl font-bold ${scoreColor}`}>
            {data.overallScore}
          </span>
          <span className="text-xs text-dim ms-1">/100</span>
        </div>

        {/* Trend */}
        <div className="text-xs">
          <span className={
            data.scoreTrend === 'up' ? 'text-success' :
            data.scoreTrend === 'down' ? 'text-error' :
            'text-dim'
          }>
            {data.scoreTrend === 'up' ? '↑' : data.scoreTrend === 'down' ? '↓' : '→'}
            {delta > 0 ? '+' : ''}{delta}
          </span>
          <span className="text-dim ms-1">{t('ai.vsLastWeek')}</span>
        </div>

        {/* Platform coverage mini */}
        <div className="text-xs text-dim">
          {mentionedCount}/4 {t('ai.platforms')}
        </div>
      </div>
    </Link>
  );
}
