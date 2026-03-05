'use client';

import { useCallback, useMemo } from 'react';
import { useParams } from 'next/navigation';
import { useClinic } from '../../PortalShell';
import { useClinicData } from '@/lib/hooks';
import { useT } from '@/lib/i18n';
import type { TranslationKey } from '@/lib/i18n';
import SeoPostCard from '@/components/seo/SeoPostCard';

export default function SeoChannelPage() {
  const { clinicId } = useClinic();
  const { channel } = useParams<{ channel: string }>();
  const { data: clinic, isLoading, refresh } = useClinicData(clinicId);
  const { t } = useT();

  const seoChannel = useMemo(
    () => clinic?.seoChannels.find((ch) => ch.channel === channel),
    [clinic, channel]
  );

  const patchPost = useCallback(async (postId: string, updates: Record<string, unknown>) => {
    await fetch(`/api/portal/${clinicId}/seo`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ channel, postId, updates }),
    });
    refresh();
  }, [clinicId, channel, refresh]);

  if (isLoading || !clinic) {
    return <div className="flex items-center justify-center min-h-[60vh] text-dim text-sm">{t('general.loading')}</div>;
  }

  if (!seoChannel) {
    return <div className="flex items-center justify-center min-h-[60vh] text-dim text-sm">{t('general.notFound')}</div>;
  }

  const channelKey = `channel.${channel}` as TranslationKey;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <button onClick={() => window.history.back()} className="text-dim hover:text-foreground transition-colors">←</button>
        <h1 className="font-heading text-xl font-bold">{t(channelKey)}</h1>
      </div>

      {seoChannel.posts && seoChannel.posts.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {seoChannel.posts.map((post) => (
            <SeoPostCard
              key={post.id}
              post={post}
              onApprove={(id) => patchPost(id, { status: 'approved', approvedAt: new Date().toISOString() })}
              onReject={(id) => patchPost(id, { status: 'rejected', rejectedAt: new Date().toISOString() })}
              onEdit={(id, updates) => patchPost(id, updates)}
            />
          ))}
        </div>
      ) : (
        <div className="bg-card border border-border rounded-2xl p-8 text-center">
          <div className="text-2xl text-muted mb-2">◈</div>
          <div className="text-sm text-dim">No posts yet for this channel</div>
        </div>
      )}
    </div>
  );
}
