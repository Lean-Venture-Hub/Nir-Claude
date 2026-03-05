'use client';

import { useT } from '@/lib/i18n';
import StatusBadge from './StatusBadge';
import type { StorySlot, ReelItem, SeoChannel } from '@/types';

interface AttentionItem {
  id: string;
  type: 'story' | 'reel' | 'seo';
  title: string;
  status: string;
  action: string;
}

interface AttentionQueueProps {
  stories: StorySlot[];
  reels: ReelItem[];
  seoChannels: SeoChannel[];
  basePath: string;
}

export default function AttentionQueue({ stories, reels, seoChannels, basePath }: AttentionQueueProps) {
  const { t } = useT();

  const items: AttentionItem[] = [];

  // Stories needing approval (generated but not approved)
  stories
    .filter((s) => s.status === 'generated')
    .slice(0, 5)
    .forEach((s) => {
      items.push({
        id: s.id,
        type: 'story',
        title: `${s.theme} — ${t('general.day')} ${s.day}, Slot ${s.slot}`,
        status: s.status,
        action: t('action.approve'),
      });
    });

  // Reels needing attention (scripted = needs script approval)
  reels
    .filter((r) => r.status === 'scripted' || r.status === 'generated')
    .slice(0, 3)
    .forEach((r) => {
      items.push({
        id: r.id,
        type: 'reel',
        title: `${r.theme} — ${t('general.week')} ${r.week}`,
        status: r.status,
        action: r.status === 'scripted' ? t('reels.approveScript') : t('reels.approveVideo'),
      });
    });

  // SEO posts needing approval
  seoChannels.forEach((ch) => {
    ch.posts
      ?.filter((p) => p.status === 'draft')
      .slice(0, 2)
      .forEach((p) => {
        items.push({
          id: p.id,
          type: 'seo',
          title: `${ch.label} — ${p.title}`,
          status: p.status,
          action: t('action.approve'),
        });
      });
  });

  if (items.length === 0) {
    return (
      <div className="bg-card border border-border rounded-2xl p-5 fade-up">
        <h3 className="font-heading text-sm font-semibold mb-3">{t('home.needsAttention')}</h3>
        <div className="text-sm text-dim text-center py-4">
          ✓ {t('general.loading') === 'Loading...' ? 'All caught up!' : 'הכל מעודכן!'}
        </div>
      </div>
    );
  }

  const typeColors = { story: 'text-accent', reel: 'text-info', seo: 'text-success' };
  const typeIcons = { story: '◧', reel: '▶', seo: '◈' };
  const typeLinks = { story: '/stories', reel: '/reels', seo: '/seo' };

  return (
    <div className="bg-card border border-border rounded-2xl p-5 fade-up">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-heading text-sm font-semibold">{t('home.needsAttention')}</h3>
        <span className="text-xs text-warning font-heading font-bold">{items.length}</span>
      </div>
      <div className="space-y-2">
        {items.slice(0, 8).map((item) => (
          <a
            key={item.id}
            href={`${basePath}${typeLinks[item.type]}`}
            className="flex items-center gap-3 px-3 py-2 rounded-xl bg-background hover:bg-card-hover transition-colors group"
          >
            <span className={`text-sm ${typeColors[item.type]}`}>{typeIcons[item.type]}</span>
            <span className="flex-1 text-sm text-dim group-hover:text-foreground truncate">{item.title}</span>
            <StatusBadge status={item.status} />
          </a>
        ))}
      </div>
    </div>
  );
}
