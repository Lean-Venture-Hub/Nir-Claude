'use client';

import Link from 'next/link';
import { useClinic } from '../../PortalShell';
import { useAiVisibility } from '@/lib/hooks';
import { useT } from '@/lib/i18n';
import AiScoreHero from '@/components/ai-visibility/AiScoreHero';
import PlatformCoverage from '@/components/ai-visibility/PlatformCoverage';
import QueryPerformance from '@/components/ai-visibility/QueryPerformance';
import OptimizationChecklist from '@/components/ai-visibility/OptimizationChecklist';
import CompetitorComparison from '@/components/ai-visibility/CompetitorComparison';
import { useClinicData } from '@/lib/hooks';

export default function AiVisibilityPage() {
  const { clinicId, token } = useClinic();
  const { data: aiData, isLoading } = useAiVisibility(clinicId);
  const { data: clinic } = useClinicData(clinicId);
  const { t } = useT();

  if (isLoading || !aiData) {
    return (
      <div className="flex items-center justify-center min-h-[60vh] text-dim text-sm">
        {t('general.loading')}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Link
          href={`/clinic/${token}/seo`}
          className="text-sm text-dim hover:text-accent transition-colors"
        >
          ← {t('ai.back')}
        </Link>
        <h1 className="font-heading text-xl font-bold">{t('ai.title')}</h1>
      </div>

      {/* Score Hero */}
      <AiScoreHero data={aiData} />

      {/* Platform Coverage + Competitor side by side on desktop */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <PlatformCoverage platforms={aiData.platforms} />
        <CompetitorComparison
          competitors={aiData.competitors}
          clinicName={clinic?.name ?? ''}
          clinicScore={aiData.overallScore}
        />
      </div>

      {/* Query Performance */}
      <QueryPerformance queries={aiData.queries} />

      {/* Optimization Checklist */}
      <OptimizationChecklist checks={aiData.optimizationChecklist} />
    </div>
  );
}
