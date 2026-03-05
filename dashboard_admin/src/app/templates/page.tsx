'use client';

import { useTemplates } from '@/lib/hooks';
import type { TemplatesData, TemplateInfo } from '@/types';

function TemplateCard({ template }: { template: TemplateInfo }) {
  const successColor =
    template.renderSuccessRate >= 98
      ? 'text-success'
      : template.renderSuccessRate >= 95
        ? 'text-accent'
        : 'text-error';

  return (
    <div className="bg-card border border-border rounded-2xl overflow-hidden hover:border-border-hover transition-colors group">
      {/* Preview iframe */}
      <div className="h-48 bg-[rgba(255,255,255,0.02)] border-b border-border relative overflow-hidden">
        <iframe
          src={template.previewPath}
          className="w-[200%] h-[200%] origin-top-left scale-50 pointer-events-none"
          title={template.name}
          loading="lazy"
          sandbox="allow-same-origin"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-card/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>

      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-heading text-sm font-semibold">{template.name}</h3>
          <span className="text-xs px-2 py-0.5 rounded-full bg-accent/10 text-accent font-body capitalize">
            {template.category}
          </span>
        </div>

        <div className="grid grid-cols-3 gap-2 mt-3">
          <div className="text-center">
            <p className="font-heading text-lg font-bold text-foreground">
              {template.usageCount.toLocaleString()}
            </p>
            <p className="text-[10px] text-muted font-body">Uses</p>
          </div>
          <div className="text-center">
            <p className="font-heading text-lg font-bold text-foreground">
              {template.assignedClinics}
            </p>
            <p className="text-[10px] text-muted font-body">Clinics</p>
          </div>
          <div className="text-center">
            <p className={`font-heading text-lg font-bold ${successColor}`}>
              {template.renderSuccessRate}%
            </p>
            <p className="text-[10px] text-muted font-body">Success</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function TemplatesPage() {
  const { data, isLoading } = useTemplates();
  const templatesData = data as TemplatesData | undefined;

  if (isLoading || !templatesData) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="text-dim font-body">Loading templates...</div>
      </div>
    );
  }

  const templates = templatesData.templates;
  const totalUsage = templates.reduce((s, t) => s + t.usageCount, 0);
  const avgSuccess = (templates.reduce((s, t) => s + t.renderSuccessRate, 0) / templates.length).toFixed(1);

  return (
    <div className="p-8 space-y-6">
      <div className="fade-up">
        <p className="text-xs uppercase tracking-widest text-accent font-heading mb-1">Template Analytics</p>
        <h2 className="font-heading text-2xl font-bold">{templates.length} Templates</h2>
        <p className="text-sm text-dim font-body mt-1">
          {totalUsage.toLocaleString()} total renders · {avgSuccess}% avg success rate
        </p>
      </div>

      {/* Usage Distribution Bar */}
      <div className="bg-card border border-border rounded-2xl p-5">
        <h3 className="font-heading text-sm font-semibold mb-3">Usage Distribution</h3>
        <div className="space-y-2">
          {[...templates]
            .sort((a, b) => b.usageCount - a.usageCount)
            .map((t) => {
              const pct = (t.usageCount / totalUsage) * 100;
              return (
                <div key={t.id} className="flex items-center gap-3">
                  <span className="text-xs text-dim font-body w-6 text-right">{t.id}</span>
                  <div className="flex-1 h-4 bg-[rgba(255,255,255,0.03)] rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent/60 rounded-full bar-animate"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                  <span className="text-xs text-dim font-body w-16 text-right">
                    {t.usageCount.toLocaleString()}
                  </span>
                  <span className="text-xs text-muted font-body w-10 text-right">{pct.toFixed(1)}%</span>
                </div>
              );
            })}
        </div>
      </div>

      {/* Template Grid */}
      <div className="grid grid-cols-4 gap-4">
        {templates.map((t) => (
          <TemplateCard key={t.id} template={t} />
        ))}
      </div>
    </div>
  );
}
