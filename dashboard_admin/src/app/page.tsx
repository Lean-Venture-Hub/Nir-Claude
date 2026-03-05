'use client';

import { useSystemStatus } from '@/lib/hooks';
import type { SystemStatus } from '@/types';
import KpiCard from '@/components/KpiCard';
import PipelineStatusBar from '@/components/PipelineStatusBar';
import AlertsList from '@/components/AlertsList';
import ActivityFeed from '@/components/ActivityFeed';

export default function CommandCenter() {
  const { data, isLoading } = useSystemStatus();
  const status = data as SystemStatus | undefined;

  if (isLoading || !status) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="text-dim font-body">Loading mission data...</div>
      </div>
    );
  }

  const budgetPct = ((status.budget.spent / status.budget.totalBudget) * 100).toFixed(0);

  return (
    <div className="p-8 space-y-6">
      {/* Header */}
      <div className="fade-up">
        <p className="text-xs uppercase tracking-widest text-accent font-heading mb-1">Command Center</p>
        <h2 className="font-heading text-2xl font-bold">Content Machine Health</h2>
        <p className="text-sm text-dim font-body mt-1">
          Last updated: {new Date(status.lastUpdated).toLocaleTimeString()}
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-4 gap-4">
        <KpiCard
          icon="◈"
          label="Budget Used"
          value={`$${status.budget.spent.toLocaleString()}`}
          subtext={`${budgetPct}% of $${status.budget.totalBudget.toLocaleString()}`}
          trend={parseInt(budgetPct) > 85 ? 'up' : 'flat'}
          color="var(--accent)"
        />
        <KpiCard
          icon="◧"
          label="Stories Generated"
          value={status.kpis.storiesGenerated}
          subtext={`of ${status.pipelines[0]?.total.toLocaleString()} planned`}
          trend="up"
          color="var(--success)"
        />
        <KpiCard
          icon="▶"
          label="Reels Generated"
          value={status.kpis.reelsGenerated}
          subtext={`of ${status.pipelines[1]?.total.toLocaleString()} planned`}
          trend="up"
          color="var(--info)"
        />
        <KpiCard
          icon="◉"
          label="SEO Posts Published"
          value={status.kpis.seoPostsPublished}
          subtext={`of ${status.pipelines[2]?.total.toLocaleString()} planned`}
          trend="up"
          color="var(--success)"
        />
      </div>

      {/* Pipeline Status Bars */}
      <div className="space-y-3">
        <h3 className="font-heading text-sm font-semibold text-dim uppercase tracking-wider">Pipeline Health</h3>
        <div className="grid grid-cols-3 gap-4">
          {status.pipelines.map((p) => (
            <PipelineStatusBar key={p.name} pipeline={p} />
          ))}
        </div>
      </div>

      {/* Alerts + Activity Feed */}
      <div className="grid grid-cols-2 gap-4">
        <AlertsList alerts={status.alerts} />
        <ActivityFeed items={status.activity} />
      </div>
    </div>
  );
}
