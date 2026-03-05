'use client';

import { useT } from '@/lib/i18n';
import type { StorySlot, ReelItem } from '@/types';

interface LiveFeedProps {
  stories: StorySlot[];
  reels: ReelItem[];
}

interface FeedItem {
  id: string;
  action: string;
  detail: string;
  pipeline: 'stories' | 'reels' | 'seo';
  timestamp: string;
}

export default function LiveFeed({ stories, reels }: LiveFeedProps) {
  const { t } = useT();

  // Generate feed from recent status changes
  const feedItems: FeedItem[] = [];

  // Recently generated/published stories
  stories
    .filter((s) => s.status === 'generated' || s.status === 'published' || s.status === 'approved')
    .slice(-10)
    .forEach((s) => {
      feedItems.push({
        id: s.id,
        action: s.status === 'generated' ? 'Story created' : s.status === 'approved' ? 'Story approved' : 'Story published',
        detail: `${s.theme} — Day ${s.day}`,
        pipeline: 'stories',
        timestamp: s.approvedAt ?? s.date,
      });
    });

  // Recently generated reels
  reels
    .filter((r) => r.status !== 'pending')
    .slice(-5)
    .forEach((r) => {
      feedItems.push({
        id: r.id,
        action: `Reel ${r.status}`,
        detail: `${r.theme} — Week ${r.week}`,
        pipeline: 'reels',
        timestamp: r.approvedAt ?? '',
      });
    });

  const pipelineColors = {
    stories: 'bg-accent',
    reels: 'bg-info',
    seo: 'bg-success',
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-5 fade-up">
      <h3 className="font-heading text-sm font-semibold mb-3">{t('home.liveFeed')}</h3>
      <div className="space-y-3 max-h-64 overflow-y-auto">
        {feedItems.length === 0 ? (
          <div className="text-sm text-dim text-center py-4">No recent activity</div>
        ) : (
          feedItems.slice(0, 10).map((item) => (
            <div key={item.id} className="flex items-start gap-3">
              <div className="mt-1.5">
                <div className={`w-2 h-2 rounded-full ${pipelineColors[item.pipeline]}`} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm">{item.action}</div>
                <div className="text-xs text-dim truncate">{item.detail}</div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
