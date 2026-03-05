'use client';

import Link from 'next/link';
import { useT } from '@/lib/i18n';
import StatusBadge from '@/components/StatusBadge';
import type { SeoChannel } from '@/types';
import type { TranslationKey } from '@/lib/i18n';

interface SeoChannelCardProps {
  channel: SeoChannel;
  basePath: string;
}

const channelIcons: Record<string, string> = {
  blog: '📝', twitter: '🐦', reddit: '🔴', quora: '❓', gbp: '📍',
};

export default function SeoChannelCard({ channel, basePath }: SeoChannelCardProps) {
  const { t } = useT();
  const pct = channel.postsPlanned > 0
    ? Math.round((channel.postsPublished / channel.postsPlanned) * 100)
    : 0;

  const channelKey = `channel.${channel.channel}` as TranslationKey;

  return (
    <Link
      href={`${basePath}/seo/${channel.channel}`}
      className="bg-card border border-border rounded-2xl p-5 hover:border-border-hover transition-colors fade-up block group"
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-xl">{channelIcons[channel.channel] ?? '📄'}</span>
          <span className="font-heading text-sm font-semibold group-hover:text-accent transition-colors">
            {t(channelKey)}
          </span>
        </div>
        <StatusBadge status={channel.status} />
      </div>

      <div className="flex gap-4 mb-3 text-xs text-dim">
        <span>{t('seo.planned')}: {channel.postsPlanned}</span>
        <span>{t('seo.published')}: {channel.postsPublished}</span>
      </div>

      <div className="w-full h-2 bg-background rounded-full overflow-hidden">
        <div
          className="h-full bg-success rounded-full bar-animate"
          style={{ width: `${pct}%` }}
        />
      </div>
      <div className="text-xs text-muted mt-1 text-end">{pct}%</div>

      {channel.posts && (
        <div className="mt-3 text-xs text-dim">
          {channel.posts.filter((p) => p.status === 'draft').length} {t('status.draft')} · {channel.posts.filter((p) => p.status === 'approved').length} {t('status.approved')}
        </div>
      )}
    </Link>
  );
}
