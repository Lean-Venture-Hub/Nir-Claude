'use client';

interface KpiCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  icon: string;
  trend?: 'up' | 'down' | 'flat';
  color?: string;
}

export default function KpiCard({ label, value, subtext, icon, trend, color = 'var(--accent)' }: KpiCardProps) {
  return (
    <div className="bg-card border border-border rounded-2xl p-5 hover:border-border-hover transition-colors fade-up">
      <div className="flex items-start justify-between mb-3">
        <span className="text-2xl">{icon}</span>
        {trend && (
          <span className={`text-xs font-body ${
            trend === 'up' ? 'text-success' : trend === 'down' ? 'text-error' : 'text-dim'
          }`}>
            {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'}
          </span>
        )}
      </div>
      <div className="font-heading text-3xl font-bold tracking-tight" style={{ color }}>
        {typeof value === 'number' ? value.toLocaleString() : value}
      </div>
      <div className="text-sm text-dim font-body mt-1">{label}</div>
      {subtext && <div className="text-xs text-muted font-body mt-0.5">{subtext}</div>}
    </div>
  );
}
