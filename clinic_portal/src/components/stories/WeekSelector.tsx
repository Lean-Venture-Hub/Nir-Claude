'use client';

import { useT } from '@/lib/i18n';

interface WeekSelectorProps {
  currentWeek: number;
  totalWeeks: number;
  onWeekChange: (week: number) => void;
}

export default function WeekSelector({ currentWeek, totalWeeks, onWeekChange }: WeekSelectorProps) {
  const { t } = useT();

  return (
    <div className="flex items-center gap-4">
      <button
        onClick={() => onWeekChange(Math.max(1, currentWeek - 1))}
        disabled={currentWeek <= 1}
        className="w-8 h-8 flex items-center justify-center rounded-lg bg-card border border-border text-dim hover:text-foreground hover:border-border-hover disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        ‹
      </button>
      <span className="font-heading text-sm font-semibold min-w-[100px] text-center">
        {t('stories.week')} {currentWeek} / {totalWeeks}
      </span>
      <button
        onClick={() => onWeekChange(Math.min(totalWeeks, currentWeek + 1))}
        disabled={currentWeek >= totalWeeks}
        className="w-8 h-8 flex items-center justify-center rounded-lg bg-card border border-border text-dim hover:text-foreground hover:border-border-hover disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        ›
      </button>
    </div>
  );
}
