'use client';

import { useClinic } from './PortalShell';
import { useClinicData } from '@/lib/hooks';
import { useT } from '@/lib/i18n';
import KpiCard from '@/components/KpiCard';
import OnboardingBar from '@/components/OnboardingBar';
import AttentionQueue from '@/components/AttentionQueue';
import LiveFeed from '@/components/LiveFeed';

export default function HomePage() {
  const { clinicId, token } = useClinic();
  const { data: clinic, isLoading } = useClinicData(clinicId);
  const { t } = useT();
  const basePath = `/clinic/${token}`;

  if (isLoading || !clinic) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-dim text-sm">{t('general.loading')}</div>
      </div>
    );
  }

  const storiesGenerated = clinic.stories.filter((s) => s.status === 'generated' || s.status === 'approved' || s.status === 'published').length;
  const reelsReady = clinic.reels.filter((r) => r.status === 'scripted' || r.status === 'generated' || r.status === 'approved' || r.status === 'published').length;
  const seoPublished = clinic.seoChannels.reduce((sum, ch) => sum + ch.postsPublished, 0);
  const aiScore = clinic.aiVisibility?.overallScore;
  const aiTrend = clinic.aiVisibility?.scoreTrend === 'up' ? 'up' as const
    : clinic.aiVisibility?.scoreTrend === 'down' ? 'down' as const
    : 'flat' as const;

  return (
    <div className="space-y-6">
      {/* Welcome + KPIs */}
      <div>
        <h1 className="font-heading text-xl font-bold mb-4">{t('home.welcome')}</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard
            icon="◧"
            label={t('home.storiesReady')}
            value={storiesGenerated}
            subtext={`/ ${clinic.stories.length} total`}
            trend="up"
          />
          <KpiCard
            icon="▶"
            label={t('home.reelsReady')}
            value={reelsReady}
            subtext={`/ ${clinic.reels.length} total`}
            color="var(--info)"
          />
          <KpiCard
            icon="◈"
            label={t('home.seoPublished')}
            value={seoPublished}
            subtext={`${clinic.seoChannels.length} channels`}
            color="var(--success)"
          />
          {aiScore !== undefined && (
            <KpiCard
              icon="🤖"
              label={t('ai.score')}
              value={aiScore}
              subtext={t('ai.scoreOf100')}
              trend={aiTrend}
              color="var(--accent)"
            />
          )}
        </div>
      </div>

      {/* Onboarding */}
      <OnboardingBar items={clinic.onboarding} />

      {/* Attention Queue + Live Feed side by side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AttentionQueue
          stories={clinic.stories}
          reels={clinic.reels}
          seoChannels={clinic.seoChannels}
          basePath={basePath}
        />
        <LiveFeed stories={clinic.stories} reels={clinic.reels} />
      </div>
    </div>
  );
}
