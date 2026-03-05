'use client';

import { useT } from '@/lib/i18n';
import type { AiCompetitor } from '@/types';

interface CompetitorComparisonProps {
  competitors: AiCompetitor[];
  clinicName: string;
  clinicScore: number;
}

export default function CompetitorComparison({ competitors, clinicName, clinicScore }: CompetitorComparisonProps) {
  const { t } = useT();

  const allEntries = [
    { name: clinicName, score: clinicScore, isClinic: true },
    ...competitors.map((c) => ({ name: c.name, score: c.aiScore, isClinic: false })),
  ].sort((a, b) => b.score - a.score);

  const maxScore = Math.max(...allEntries.map((e) => e.score), 1);

  return (
    <div className="bg-card border border-border rounded-2xl p-6 fade-up">
      <h2 className="font-heading text-sm font-semibold text-dim mb-4">{t('ai.competitors')}</h2>
      <div className="space-y-3">
        {allEntries.map((entry, i) => (
          <div key={i}>
            <div className="flex items-center justify-between mb-1">
              <span className={`text-xs font-body truncate max-w-[200px] ${
                entry.isClinic ? 'font-bold text-accent' : 'text-dim'
              }`}>
                {entry.isClinic ? `⭐ ${t('ai.yourClinic')}` : entry.name}
              </span>
              <span className={`text-xs font-heading font-bold ${
                entry.isClinic ? 'text-accent' : 'text-dim'
              }`}>
                {entry.score}
              </span>
            </div>
            <div className="w-full h-3 bg-background rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full bar-animate ${
                  entry.isClinic ? 'bg-accent' : 'bg-border-hover'
                }`}
                style={{ width: `${(entry.score / maxScore) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Share of voice footer */}
      {competitors.length > 0 && (
        <div className="mt-4 pt-3 border-t border-border">
          <div className="text-[10px] text-dim font-heading uppercase mb-2">{t('ai.shareOfVoice')}</div>
          <div className="flex gap-2 flex-wrap">
            {competitors.map((c, i) => (
              <span key={i} className="text-[10px] text-dim bg-background px-2 py-1 rounded-md">
                {c.name.substring(0, 15)}{c.name.length > 15 ? '…' : ''}: {c.shareOfVoice}%
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
