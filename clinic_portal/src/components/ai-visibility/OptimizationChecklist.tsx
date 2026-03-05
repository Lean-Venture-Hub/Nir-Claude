'use client';

import { useT } from '@/lib/i18n';
import type { AiOptimizationCheck } from '@/types';
import type { TranslationKey } from '@/lib/i18n';

interface OptimizationChecklistProps {
  checks: AiOptimizationCheck[];
}

export default function OptimizationChecklist({ checks }: OptimizationChecklistProps) {
  const { t } = useT();
  const completed = checks.filter((c) => c.completed).length;
  const pct = Math.round((completed / checks.length) * 100);

  const priorityLabel = (p: string) => t(`ai.${p}` as TranslationKey);
  const priorityColor = (p: string) => {
    switch (p) {
      case 'high': return 'text-error';
      case 'medium': return 'text-warning';
      default: return 'text-dim';
    }
  };

  // Group by priority
  const groups = ['high', 'medium', 'low'] as const;

  return (
    <div className="bg-card border border-border rounded-2xl p-6 fade-up">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-heading text-sm font-semibold text-dim">{t('ai.optimization')}</h2>
        <span className="text-xs text-accent font-heading font-bold">
          {completed}/{checks.length} {t('ai.completed')}
        </span>
      </div>

      {/* Progress bar */}
      <div className="w-full h-2 bg-background rounded-full overflow-hidden mb-4">
        <div
          className="h-full bg-accent rounded-full bar-animate"
          style={{ width: `${pct}%` }}
        />
      </div>

      {/* Grouped items */}
      <div className="space-y-3">
        {groups.map((priority) => {
          const items = checks.filter((c) => c.priority === priority);
          if (items.length === 0) return null;
          return (
            <div key={priority}>
              <div className={`text-[10px] font-heading font-bold uppercase mb-1.5 ${priorityColor(priority)}`}>
                {priorityLabel(priority)}
              </div>
              <div className="space-y-1.5">
                {items.map((item) => (
                  <div
                    key={item.key}
                    className={`flex items-start gap-2 text-xs px-3 py-2 rounded-lg border ${
                      item.completed
                        ? 'border-success/20 text-success bg-success/5'
                        : 'border-border text-dim bg-background'
                    }`}
                  >
                    <span className="mt-0.5 shrink-0">{item.completed ? '✓' : '○'}</span>
                    <div>
                      <div className="font-medium">{item.label}</div>
                      <div className="text-[10px] opacity-70 mt-0.5">{item.impact}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
