'use client';

import { useState, useCallback, useMemo } from 'react';
import { useClinic } from '../PortalShell';
import { useClinicData } from '@/lib/hooks';
import { useT } from '@/lib/i18n';
import WeekSelector from '@/components/stories/WeekSelector';
import BulkApproveBar from '@/components/stories/BulkApproveBar';
import StoryCard from '@/components/stories/StoryCard';

export default function StoriesPage() {
  const { clinicId } = useClinic();
  const { data: clinic, isLoading, refresh } = useClinicData(clinicId);
  const { t } = useT();
  const [currentWeek, setCurrentWeek] = useState(1);
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const totalWeeks = useMemo(() => {
    if (!clinic) return 13;
    return Math.max(...clinic.stories.map((s) => s.week), 1);
  }, [clinic]);

  const weekStories = useMemo(() => {
    if (!clinic) return [];
    return clinic.stories.filter((s) => s.week === currentWeek);
  }, [clinic, currentWeek]);

  // Group by day
  const dayGroups = useMemo(() => {
    const groups: Record<number, typeof weekStories> = {};
    weekStories.forEach((s) => {
      if (!groups[s.day]) groups[s.day] = [];
      groups[s.day].push(s);
    });
    return Object.entries(groups)
      .sort(([a], [b]) => Number(a) - Number(b))
      .map(([day, stories]) => ({ day: Number(day), date: stories[0]?.date, stories }));
  }, [weekStories]);

  const patchStory = useCallback(async (storyId: string, updates: Record<string, unknown>) => {
    await fetch(`/api/portal/${clinicId}/stories`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ storyId, updates }),
    });
    refresh();
  }, [clinicId, refresh]);

  const handleApprove = useCallback((id: string) => {
    patchStory(id, { status: 'approved', approvedAt: new Date().toISOString() });
  }, [patchStory]);

  const handleReject = useCallback((id: string) => {
    patchStory(id, { status: 'rejected', rejectedAt: new Date().toISOString() });
  }, [patchStory]);

  const handleEditCaption = useCallback((id: string, caption: string) => {
    patchStory(id, { editedCaption: caption });
  }, [patchStory]);

  const toggleSelect = useCallback((id: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  const handleBulkApprove = useCallback(async () => {
    await fetch(`/api/portal/${clinicId}/stories`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bulkApprove: true, week: currentWeek }),
    });
    setSelected(new Set());
    refresh();
  }, [clinicId, currentWeek, refresh]);

  if (isLoading || !clinic) {
    return <div className="flex items-center justify-center min-h-[60vh] text-dim text-sm">{t('general.loading')}</div>;
  }

  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="font-heading text-xl font-bold">{t('stories.title')}</h1>
        <WeekSelector currentWeek={currentWeek} totalWeeks={totalWeeks} onWeekChange={setCurrentWeek} />
      </div>

      <BulkApproveBar
        selectedCount={selected.size}
        onBulkApprove={handleBulkApprove}
        onClear={() => setSelected(new Set())}
      />

      {/* Story cards in same grid as reels */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {dayGroups.flatMap(({ day, date, stories }) =>
          stories
            .sort((a, b) => a.slot - b.slot)
            .map((story) => (
              <StoryCard
                key={story.id}
                story={story}
                dayLabel={`${dayNames[(day - 1) % 7]} · ${date}`}
                onApprove={handleApprove}
                onReject={handleReject}
                onEditCaption={handleEditCaption}
                onSwapTemplate={() => {/* TODO: open template picker modal */}}
                onUploadPhoto={() => {/* TODO: open photo upload modal */}}
                selected={selected.has(story.id)}
                onSelect={toggleSelect}
              />
            ))
        )}
      </div>
    </div>
  );
}
