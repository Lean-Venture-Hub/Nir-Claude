'use client';

import type { PipelineStatus } from '@/types';

const STATUS_COLORS = {
  healthy: 'var(--success)',
  warning: 'var(--warning)',
  critical: 'var(--error)',
};

export default function PipelineStatusBar({ pipeline }: { pipeline: PipelineStatus }) {
  const completedPct = (pipeline.completed / pipeline.total) * 100;
  const inProgressPct = (pipeline.inProgress / pipeline.total) * 100;
  const failedPct = (pipeline.failed / pipeline.total) * 100;

  return (
    <div className="bg-card border border-border rounded-2xl p-5 hover:border-border-hover transition-colors">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h3 className="font-heading text-sm font-semibold">{pipeline.label}</h3>
          <span className="text-xs text-dim font-body">
            {pipeline.completed.toLocaleString()} / {pipeline.total.toLocaleString()}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span
            className="w-2 h-2 rounded-full"
            style={{ backgroundColor: STATUS_COLORS[pipeline.status] }}
          />
          <span className="text-xs capitalize font-body" style={{ color: STATUS_COLORS[pipeline.status] }}>
            {pipeline.status}
          </span>
        </div>
      </div>

      <div className="h-3 bg-[rgba(255,255,255,0.05)] rounded-full overflow-hidden flex">
        <div
          className="h-full bg-success bar-animate rounded-l-full"
          style={{ width: `${completedPct}%` }}
        />
        <div
          className="h-full bg-accent bar-animate"
          style={{ width: `${inProgressPct}%` }}
        />
        <div
          className="h-full bg-error bar-animate rounded-r-full"
          style={{ width: `${failedPct}%` }}
        />
      </div>

      <div className="flex gap-4 mt-2 text-xs text-dim font-body">
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-full bg-success" /> Completed {completedPct.toFixed(0)}%
        </span>
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-full bg-accent" /> In Progress {inProgressPct.toFixed(0)}%
        </span>
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-full bg-error" /> Failed {failedPct.toFixed(0)}%
        </span>
      </div>
    </div>
  );
}
