'use client';

import { useClinic } from '../PortalShell';
import { useClinicData } from '@/lib/hooks';
import { useT } from '@/lib/i18n';
import SeoChannelCard from '@/components/seo/SeoChannelCard';
import AiVisibilityHubCard from '@/components/ai-visibility/AiVisibilityHubCard';

export default function SeoPage() {
  const { clinicId, token } = useClinic();
  const { data: clinic, isLoading } = useClinicData(clinicId);
  const { t } = useT();
  const basePath = `/clinic/${token}`;

  if (isLoading || !clinic) {
    return <div className="flex items-center justify-center min-h-[60vh] text-dim text-sm">{t('general.loading')}</div>;
  }

  return (
    <div className="space-y-4">
      <h1 className="font-heading text-xl font-bold">{t('seo.title')}</h1>

      {/* AI Visibility hub card — prominent, full-width */}
      {clinic.aiVisibility && (
        <AiVisibilityHubCard data={clinic.aiVisibility} basePath={basePath} />
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {clinic.seoChannels.map((channel) => (
          <SeoChannelCard key={channel.channel} channel={channel} basePath={basePath} />
        ))}
      </div>
    </div>
  );
}
