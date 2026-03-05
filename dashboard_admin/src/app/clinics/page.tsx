'use client';

import { useState, useMemo } from 'react';
import Link from 'next/link';
import { useClinicIndex } from '@/lib/hooks';
import type { ClinicIndex, ClinicSummary } from '@/types';
import HebrewText from '@/components/HebrewText';

type SortKey = 'name' | 'city' | 'segmentName' | 'rating' | 'onboardingPct' | 'storiesCompleted';
type SortDir = 'asc' | 'desc';

function CompletionBar({ completed, total, color = 'bg-accent' }: { completed: number; total: number; color?: string }) {
  const pct = total > 0 ? (completed / total) * 100 : 0;
  return (
    <div className="flex items-center gap-2">
      <div className="w-16 h-1.5 bg-[rgba(255,255,255,0.05)] rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs text-muted font-body">{pct.toFixed(0)}%</span>
    </div>
  );
}

export default function ClinicRoster() {
  const { data, isLoading } = useClinicIndex();
  const clinics = (data as ClinicIndex | undefined)?.clinics ?? [];

  const [search, setSearch] = useState('');
  const [cityFilter, setCityFilter] = useState('');
  const [segmentFilter, setSegmentFilter] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('name');
  const [sortDir, setSortDir] = useState<SortDir>('asc');

  const cities = useMemo(() => [...new Set(clinics.map((c) => c.city).filter(Boolean))].sort(), [clinics]);
  const segments = useMemo(() => [...new Set(clinics.map((c) => c.segmentName).filter(Boolean))].sort(), [clinics]);

  const filtered = useMemo(() => {
    let result = clinics;
    if (search) {
      const q = search.toLowerCase();
      result = result.filter((c) => c.name.toLowerCase().includes(q) || c.city.toLowerCase().includes(q));
    }
    if (cityFilter) result = result.filter((c) => c.city === cityFilter);
    if (segmentFilter) result = result.filter((c) => c.segmentName === segmentFilter);

    result.sort((a, b) => {
      const av = a[sortKey] ?? '';
      const bv = b[sortKey] ?? '';
      const cmp = typeof av === 'number' ? (av as number) - (bv as number) : String(av).localeCompare(String(bv));
      return sortDir === 'asc' ? cmp : -cmp;
    });

    return result;
  }, [clinics, search, cityFilter, segmentFilter, sortKey, sortDir]);

  function toggleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  }

  const SortHeader = ({ label, field }: { label: string; field: SortKey }) => (
    <th
      className="text-left px-3 py-2 text-xs text-dim font-body cursor-pointer hover:text-foreground select-none"
      onClick={() => toggleSort(field)}
    >
      {label} {sortKey === field ? (sortDir === 'asc' ? '↑' : '↓') : ''}
    </th>
  );

  if (isLoading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="text-dim font-body">Loading clinic roster...</div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6">
      <div className="fade-up">
        <p className="text-xs uppercase tracking-widest text-accent font-heading mb-1">Clinic Roster</p>
        <h2 className="font-heading text-2xl font-bold">{filtered.length} of {clinics.length} Clinics</h2>
      </div>

      {/* Filters */}
      <div className="flex gap-3 flex-wrap">
        <input
          type="text"
          placeholder="Search by name or city..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-card border border-border rounded-xl px-4 py-2 text-sm font-body text-foreground placeholder:text-muted focus:outline-none focus:border-accent/40 w-72"
        />
        <select
          value={cityFilter}
          onChange={(e) => setCityFilter(e.target.value)}
          className="bg-card border border-border rounded-xl px-4 py-2 text-sm font-body text-foreground focus:outline-none focus:border-accent/40"
        >
          <option value="">All Cities</option>
          {cities.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        <select
          value={segmentFilter}
          onChange={(e) => setSegmentFilter(e.target.value)}
          className="bg-card border border-border rounded-xl px-4 py-2 text-sm font-body text-foreground focus:outline-none focus:border-accent/40"
        >
          <option value="">All Segments</option>
          {segments.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {/* Table */}
      <div className="bg-card border border-border rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-border">
              <tr>
                <th className="text-left px-3 py-2 text-xs text-dim font-body w-10">#</th>
                <SortHeader label="Name" field="name" />
                <SortHeader label="City" field="city" />
                <SortHeader label="Segment" field="segmentName" />
                <SortHeader label="Rating" field="rating" />
                <SortHeader label="Onboarding" field="onboardingPct" />
                <th className="text-left px-3 py-2 text-xs text-dim font-body">Stories</th>
                <th className="text-left px-3 py-2 text-xs text-dim font-body">Reels</th>
                <th className="text-left px-3 py-2 text-xs text-dim font-body">SEO</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((clinic: ClinicSummary) => (
                <tr
                  key={clinic.id}
                  className="border-b border-border hover:bg-card-hover transition-colors"
                >
                  <td className="px-3 py-2.5 text-xs text-muted">{clinic.id}</td>
                  <td className="px-3 py-2.5">
                    <Link href={`/clinics/${clinic.id}`} className="text-sm font-body text-foreground hover:text-accent transition-colors">
                      <HebrewText>{clinic.name}</HebrewText>
                    </Link>
                  </td>
                  <td className="px-3 py-2.5 text-sm text-dim font-body">{clinic.city}</td>
                  <td className="px-3 py-2.5">
                    <span className="text-xs px-2 py-0.5 rounded-full bg-accent/10 text-accent font-body">
                      {clinic.segmentName}
                    </span>
                  </td>
                  <td className="px-3 py-2.5 text-sm font-body">
                    {clinic.rating ? (
                      <span className="text-accent">{clinic.rating.toFixed(1)} ★</span>
                    ) : (
                      <span className="text-muted">—</span>
                    )}
                  </td>
                  <td className="px-3 py-2.5">
                    <CompletionBar completed={clinic.onboardingPct} total={100} color="bg-accent" />
                  </td>
                  <td className="px-3 py-2.5">
                    <CompletionBar completed={clinic.storiesCompleted} total={clinic.storiesTotal} color="bg-success" />
                  </td>
                  <td className="px-3 py-2.5">
                    <CompletionBar completed={clinic.reelsCompleted} total={clinic.reelsTotal} color="bg-info" />
                  </td>
                  <td className="px-3 py-2.5">
                    <CompletionBar completed={clinic.seoCompleted} total={clinic.seoTotal} color="bg-success" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
