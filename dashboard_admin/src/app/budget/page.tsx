'use client';

import { useBudget } from '@/lib/hooks';
import type { BudgetData, MonthlyBudget } from '@/types';

function BudgetGauge({ current, budget, label }: { current: number; budget: number; label: string }) {
  const pct = (current / budget) * 100;
  const isOver = pct > 100;
  const barPct = Math.min(pct, 100);

  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-heading text-sm font-semibold">{label}</h3>
        <span className={`text-xs font-body ${isOver ? 'text-error' : pct > 85 ? 'text-warning' : 'text-success'}`}>
          {pct.toFixed(0)}%
        </span>
      </div>

      <div className="flex items-end gap-4 mb-3">
        <div>
          <p className={`font-heading text-3xl font-bold ${isOver ? 'text-error' : 'text-accent'}`}>
            ${current.toLocaleString()}
          </p>
          <p className="text-xs text-dim font-body">of ${budget.toLocaleString()} budget</p>
        </div>
        {isOver && (
          <span className="text-xs px-2 py-1 rounded-full bg-error/10 text-error font-body">
            ${(current - budget).toLocaleString()} over
          </span>
        )}
      </div>

      <div className="h-4 bg-[rgba(255,255,255,0.05)] rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full bar-animate ${
            isOver ? 'bg-error' : pct > 85 ? 'bg-warning' : 'bg-success'
          }`}
          style={{ width: `${barPct}%` }}
        />
      </div>
    </div>
  );
}

function PipelineCostTable({ month }: { month: MonthlyBudget }) {
  const rows = [
    { label: 'Instagram Stories', value: month.stories, color: 'text-accent', desc: '439 clinics × $2.20/clinic' },
    { label: 'Instagram Reels', value: month.reels, color: 'text-info', desc: '439 clinics × $4.50/clinic' },
    { label: 'Local SEO', value: month.seo, color: 'text-success', desc: '439 clinics × $3.64/clinic' },
  ];

  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <h3 className="font-heading text-sm font-semibold mb-4">Pipeline Cost Breakdown — {month.month}</h3>
      <div className="space-y-3">
        {rows.map((row) => {
          const pct = (row.value / month.total) * 100;
          return (
            <div key={row.label}>
              <div className="flex items-center justify-between mb-1">
                <div>
                  <span className={`text-sm font-body ${row.color}`}>{row.label}</span>
                  <span className="text-xs text-muted font-body ml-2">{row.desc}</span>
                </div>
                <span className="font-heading text-sm font-semibold">${row.value.toLocaleString()}</span>
              </div>
              <div className="h-2 bg-[rgba(255,255,255,0.05)] rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full bar-animate ${
                    row.color === 'text-accent' ? 'bg-accent' : row.color === 'text-info' ? 'bg-info' : 'bg-success'
                  }`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
        <div className="border-t border-border pt-3 flex items-center justify-between">
          <span className="text-sm font-body text-foreground font-medium">Total</span>
          <span className="font-heading text-lg font-bold text-foreground">${month.total.toLocaleString()}</span>
        </div>
      </div>
    </div>
  );
}

function MonthlyTrend({ history, current }: { history: MonthlyBudget[]; current: MonthlyBudget }) {
  const allMonths = [...history, current];
  const maxTotal = Math.max(...allMonths.map((m) => m.total));

  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <h3 className="font-heading text-sm font-semibold mb-4">Monthly Trend</h3>
      <div className="flex items-end gap-3 h-40">
        {allMonths.map((m, i) => {
          const storiesPct = (m.stories / maxTotal) * 100;
          const reelsPct = (m.reels / maxTotal) * 100;
          const seoPct = (m.seo / maxTotal) * 100;
          const isLast = i === allMonths.length - 1;

          return (
            <div key={m.month} className="flex-1 flex flex-col items-center gap-1">
              <div className="w-full flex flex-col-reverse gap-0.5" style={{ height: '120px' }}>
                <div className="bg-accent rounded-t-sm bar-animate" style={{ height: `${storiesPct}%` }} />
                <div className="bg-info rounded-sm bar-animate" style={{ height: `${reelsPct}%` }} />
                <div className="bg-success rounded-b-sm bar-animate" style={{ height: `${seoPct}%` }} />
              </div>
              <span className="text-xs text-dim font-body">${m.total.toLocaleString()}</span>
              <span className={`text-xs font-body ${isLast ? 'text-accent' : 'text-muted'}`}>
                {m.month.split(' ')[0]}
              </span>
              {m.total > m.budget && (
                <span className="text-[10px] text-error font-body">over</span>
              )}
            </div>
          );
        })}
      </div>

      <div className="flex gap-4 mt-4 text-xs text-dim font-body justify-center">
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-accent" /> Stories</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-info" /> Reels</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-success" /> SEO</span>
      </div>
    </div>
  );
}

export default function BudgetPage() {
  const { data, isLoading } = useBudget();
  const budget = data as BudgetData | undefined;

  if (isLoading || !budget) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="text-dim font-body">Loading budget data...</div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6">
      <div className="fade-up">
        <p className="text-xs uppercase tracking-widest text-accent font-heading mb-1">Cost & Budget</p>
        <h2 className="font-heading text-2xl font-bold">Monthly Spend Tracking</h2>
        <p className="text-sm text-dim font-body mt-1">
          Avg ${budget.perClinicAvg.total}/clinic/month across 439 clinics
        </p>
      </div>

      {/* Main Gauge */}
      <BudgetGauge
        current={budget.currentMonth.total}
        budget={budget.monthlyBudget}
        label={budget.currentMonth.month}
      />

      {/* Per-Clinic Averages */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Stories/Clinic', value: budget.perClinicAvg.stories, color: 'var(--accent)' },
          { label: 'Reels/Clinic', value: budget.perClinicAvg.reels, color: 'var(--info)' },
          { label: 'SEO/Clinic', value: budget.perClinicAvg.seo, color: 'var(--success)' },
          { label: 'Total/Clinic', value: budget.perClinicAvg.total, color: 'var(--text-primary)' },
        ].map((item) => (
          <div key={item.label} className="bg-card border border-border rounded-2xl p-4 text-center">
            <p className="text-xs text-dim font-body">{item.label}</p>
            <p className="font-heading text-2xl font-bold" style={{ color: item.color }}>
              ${item.value.toFixed(2)}
            </p>
            <p className="text-[10px] text-muted font-body">per month</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <PipelineCostTable month={budget.currentMonth} />
        <MonthlyTrend history={budget.history} current={budget.currentMonth} />
      </div>
    </div>
  );
}
