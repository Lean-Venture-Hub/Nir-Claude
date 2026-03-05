'use client';

import { useCallback } from 'react';
import { useClinic } from '../PortalShell';
import { useClinicData } from '@/lib/hooks';
import { useT } from '@/lib/i18n';
import ReelCard from '@/components/reels/ReelCard';

export default function ReelsPage() {
  const { clinicId } = useClinic();
  const { data: clinic, isLoading, refresh } = useClinicData(clinicId);
  const { t } = useT();

  const patchReel = useCallback(async (reelId: string, updates: Record<string, unknown>) => {
    await fetch(`/api/portal/${clinicId}/reels`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reelId, updates }),
    });
    refresh();
  }, [clinicId, refresh]);

  if (isLoading || !clinic) {
    return <div className="flex items-center justify-center min-h-[60vh] text-dim text-sm">{t('general.loading')}</div>;
  }

  return (
    <div className="space-y-4">
      <h1 className="font-heading text-xl font-bold">{t('reels.title')}</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {clinic.reels.map((reel) => (
          <ReelCard
            key={reel.id}
            reel={reel}
            onApproveScript={(id) => patchReel(id, { scriptApproved: true, approvedAt: new Date().toISOString() })}
            onApproveVideo={(id) => patchReel(id, { videoApproved: true, status: 'approved', approvedAt: new Date().toISOString() })}
            onReject={(id) => patchReel(id, { status: 'rejected', rejectedAt: new Date().toISOString() })}
            onEditScript={(id, text) => patchReel(id, { scriptText: text })}
            onRequestRevision={(id, note) => patchReel(id, { revisionRequest: note })}
          />
        ))}
      </div>
    </div>
  );
}
