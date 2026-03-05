'use client';

import type { Alert } from '@/types';

const LEVEL_STYLES = {
  info: { bg: 'bg-info/10', border: 'border-info/20', dot: 'bg-info', text: 'text-info' },
  warning: { bg: 'bg-warning/10', border: 'border-warning/20', dot: 'bg-warning', text: 'text-warning' },
  error: { bg: 'bg-error/10', border: 'border-error/20', dot: 'bg-error', text: 'text-error' },
};

function timeAgo(ts: string): string {
  const diff = Date.now() - new Date(ts).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

export default function AlertsList({ alerts }: { alerts: Alert[] }) {
  if (!alerts.length) return null;

  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <h3 className="font-heading text-sm font-semibold mb-3">Alerts</h3>
      <div className="space-y-2">
        {alerts.map((alert) => {
          const s = LEVEL_STYLES[alert.level];
          return (
            <div
              key={alert.id}
              className={`${s.bg} border ${s.border} rounded-xl px-4 py-2.5 flex items-start gap-3`}
            >
              <span className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${s.dot}`} />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-body text-foreground">{alert.message}</p>
                <div className="flex items-center gap-2 mt-1">
                  {alert.pipeline && (
                    <span className="text-xs text-muted font-body capitalize">{alert.pipeline}</span>
                  )}
                  <span className="text-xs text-muted font-body">{timeAgo(alert.timestamp)}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
