'use client';

import { useT } from '@/lib/i18n';
import type { OnboardingItem } from '@/types';

interface OnboardingBarProps {
  items: OnboardingItem[];
}

export default function OnboardingBar({ items }: OnboardingBarProps) {
  const { t } = useT();
  const completed = items.filter((i) => i.completed).length;
  const total = items.length;
  const pct = Math.round((completed / total) * 100);

  if (pct >= 100) return null;

  return (
    <div className="bg-card border border-border rounded-2xl p-5 fade-up">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-heading text-sm font-semibold">{t('home.onboarding')}</h3>
        <span className="text-xs text-accent font-heading font-bold">{pct}%</span>
      </div>
      <div className="w-full h-2 bg-background rounded-full overflow-hidden mb-3">
        <div
          className="h-full bg-accent rounded-full bar-animate"
          style={{ width: `${pct}%` }}
        />
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {items.map((item) => (
          <div
            key={item.key}
            className={`text-xs px-2 py-1.5 rounded-lg border ${
              item.completed
                ? 'border-success/20 text-success bg-success/5'
                : 'border-border text-dim bg-background'
            }`}
          >
            <span className="me-1">{item.completed ? '✓' : '○'}</span>
            {item.label}
          </div>
        ))}
      </div>
    </div>
  );
}
