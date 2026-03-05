'use client';

import type { ActivityItem } from '@/types';

const PIPELINE_COLORS: Record<string, string> = {
  stories: 'bg-accent',
  reels: 'bg-info',
  seo: 'bg-success',
  system: 'bg-dim',
};

function timeAgo(ts: string): string {
  const diff = Date.now() - new Date(ts).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

export default function ActivityFeed({ items }: { items: ActivityItem[] }) {
  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <h3 className="font-heading text-sm font-semibold mb-3">Activity Feed</h3>
      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.id} className="flex gap-3 items-start">
            <div className="flex flex-col items-center">
              <span className={`w-2 h-2 rounded-full mt-1.5 ${PIPELINE_COLORS[item.pipeline] || 'bg-dim'}`} />
              <span className="w-px flex-1 bg-border mt-1" />
            </div>
            <div className="flex-1 pb-3">
              <p className="text-sm font-body text-foreground">{item.detail}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs text-accent font-body capitalize">{item.pipeline}</span>
                <span className="text-xs text-muted font-body">{timeAgo(item.timestamp)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
