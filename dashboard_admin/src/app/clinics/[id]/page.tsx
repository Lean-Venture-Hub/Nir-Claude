'use client';

import { useParams } from 'next/navigation';
import Link from 'next/link';
import { useClinicDetail } from '@/lib/hooks';
import type { ClinicDetail } from '@/types';
import HebrewText from '@/components/HebrewText';

function OnboardingChecklist({ items }: { items: ClinicDetail['onboarding'] }) {
  const completed = items.filter((i) => i.completed).length;
  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-heading text-sm font-semibold">Onboarding</h3>
        <span className="text-xs text-accent font-body">{completed}/{items.length} complete</span>
      </div>
      <div className="space-y-2">
        {items.map((item) => (
          <div key={item.key} className="flex items-center gap-3">
            <span className={`w-5 h-5 rounded-md border flex items-center justify-center text-xs ${
              item.completed
                ? 'bg-success/20 border-success/40 text-success'
                : 'border-border text-muted'
            }`}>
              {item.completed ? '✓' : ''}
            </span>
            <span className={`text-sm font-body ${item.completed ? 'text-foreground' : 'text-dim'}`}>
              {item.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function StoryCalendarGrid({ stories }: { stories: ClinicDetail['stories'] }) {
  const weeks: Record<number, typeof stories> = {};
  stories.forEach((s) => {
    const week = Math.ceil(s.day / 7);
    if (!weeks[week]) weeks[week] = [];
    weeks[week].push(s);
  });

  const statusColor: Record<string, string> = {
    published: 'bg-success',
    generated: 'bg-accent',
    pending: 'bg-[rgba(255,255,255,0.1)]',
    failed: 'bg-error',
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <h3 className="font-heading text-sm font-semibold mb-4">Story Calendar (90 Days)</h3>
      <div className="flex flex-wrap gap-0.5">
        {stories.map((s, i) => (
          <div
            key={i}
            className={`w-2 h-2 rounded-sm ${statusColor[s.status]}`}
            title={`Day ${s.day} Slot ${s.slot}: ${s.status} (${s.theme})`}
          />
        ))}
      </div>
      <div className="flex gap-4 mt-3 text-xs text-dim font-body">
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-success" /> Published</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-accent" /> Generated</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-[rgba(255,255,255,0.1)]" /> Pending</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-error" /> Failed</span>
      </div>
    </div>
  );
}

function ReelCards({ reels }: { reels: ClinicDetail['reels'] }) {
  const statusColor: Record<string, string> = {
    published: 'text-success',
    generated: 'text-accent',
    scripted: 'text-info',
    pending: 'text-muted',
    failed: 'text-error',
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <h3 className="font-heading text-sm font-semibold mb-4">Reels ({reels.length})</h3>
      <div className="grid grid-cols-4 gap-3">
        {reels.map((reel) => (
          <div key={reel.id} className="border border-border rounded-xl p-3 hover:border-border-hover transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-dim font-body">Week {reel.week}</span>
              <span className={`text-xs capitalize font-body ${statusColor[reel.status]}`}>{reel.status}</span>
            </div>
            <p className="text-xs font-body text-foreground">{reel.theme}</p>
            <p className="text-xs text-muted font-body mt-1">${reel.cost.toFixed(2)}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function SeoChannels({ channels }: { channels: ClinicDetail['seoChannels'] }) {
  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <h3 className="font-heading text-sm font-semibold mb-4">SEO Channels</h3>
      <div className="grid grid-cols-5 gap-3">
        {channels.map((ch) => {
          const pct = ch.postsPlanned > 0 ? (ch.postsPublished / ch.postsPlanned) * 100 : 0;
          return (
            <div key={ch.channel} className="border border-border rounded-xl p-3 text-center">
              <p className="text-xs font-body text-foreground mb-1">{ch.label}</p>
              <p className="font-heading text-lg font-bold text-accent">
                {ch.postsPublished}/{ch.postsPlanned}
              </p>
              <div className="w-full h-1.5 bg-[rgba(255,255,255,0.05)] rounded-full mt-2">
                <div className="h-full bg-success rounded-full" style={{ width: `${pct}%` }} />
              </div>
              <span className={`text-xs mt-1 inline-block capitalize font-body ${
                ch.status === 'active' ? 'text-success' : ch.status === 'paused' ? 'text-warning' : 'text-muted'
              }`}>{ch.status}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function CostBreakdown({ costs }: { costs: ClinicDetail['costs'] }) {
  const latest = costs[costs.length - 1];
  if (!latest) return null;

  return (
    <div className="bg-card border border-border rounded-2xl p-5">
      <h3 className="font-heading text-sm font-semibold mb-4">Cost Breakdown</h3>
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Stories', value: latest.stories, color: 'text-accent' },
          { label: 'Reels', value: latest.reels, color: 'text-info' },
          { label: 'SEO', value: latest.seo, color: 'text-success' },
          { label: 'Total', value: latest.total, color: 'text-foreground' },
        ].map((item) => (
          <div key={item.label} className="text-center">
            <p className="text-xs text-dim font-body">{item.label}</p>
            <p className={`font-heading text-xl font-bold ${item.color}`}>${item.value.toFixed(2)}</p>
          </div>
        ))}
      </div>
      {costs.length > 1 && (
        <div className="mt-4 border-t border-border pt-3">
          <p className="text-xs text-dim font-body mb-2">Monthly History</p>
          <div className="flex gap-2">
            {costs.map((c, i) => (
              <div key={i} className="flex-1 text-center border border-border rounded-lg p-2">
                <p className="text-xs text-muted font-body">{c.month}</p>
                <p className="text-sm font-heading font-semibold text-foreground">${c.total.toFixed(2)}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function ClinicDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data, isLoading } = useClinicDetail(parseInt(id, 10));
  const clinic = data as ClinicDetail | undefined;

  if (isLoading || !clinic) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="text-dim font-body">Loading clinic details...</div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6">
      <div className="fade-up">
        <Link href="/clinics" className="text-xs text-dim font-body hover:text-accent transition-colors">
          ← Back to Roster
        </Link>
        <div className="flex items-center gap-4 mt-2">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center text-lg font-heading font-bold"
            style={{ backgroundColor: clinic.colors?.primary || '#e8a849', color: '#08080a' }}
          >
            {clinic.id}
          </div>
          <div>
            <h2 className="font-heading text-2xl font-bold">
              <HebrewText>{clinic.name}</HebrewText>
            </h2>
            <p className="text-sm text-dim font-body">
              {clinic.city} · {clinic.segmentName}
              {clinic.rating ? ` · ${clinic.rating} ★` : ''}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <OnboardingChecklist items={clinic.onboarding} />
        <div className="col-span-2">
          <StoryCalendarGrid stories={clinic.stories} />
        </div>
      </div>

      <ReelCards reels={clinic.reels} />
      <SeoChannels channels={clinic.seoChannels} />
      <CostBreakdown costs={clinic.costs} />
    </div>
  );
}
