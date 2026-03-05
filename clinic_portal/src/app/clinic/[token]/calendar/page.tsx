'use client';

import { useMemo, useCallback, useState } from 'react';
import { DndContext, DragEndEvent } from '@dnd-kit/core';
import { useClinic } from '../PortalShell';
import { useClinicData } from '@/lib/hooks';
import { useT } from '@/lib/i18n';
import CalendarDayCell from '@/components/calendar/CalendarDayCell';

const MONTH_NAMES_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const MONTH_NAMES_HE = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
const DAY_HEADERS_EN = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const DAY_HEADERS_HE = ['שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת', 'ראשון'];

interface CalItem {
  id: string;
  date: string;
  type: 'story' | 'reel' | 'seo';
  title: string;
  status: string;
  slot?: number;
}

export default function CalendarPage() {
  const { clinicId } = useClinic();
  const { data: clinic, isLoading, refresh } = useClinicData(clinicId);
  const { t, lang } = useT();
  const [paused, setPaused] = useState(false);

  // Determine range of months from story data
  const { allItems, monthRange } = useMemo(() => {
    if (!clinic) return { allItems: [] as CalItem[], monthRange: [] as string[] };

    const items: CalItem[] = [];

    clinic.stories.forEach((s) => {
      if (s.date) {
        items.push({
          id: s.id, date: s.date, type: 'story',
          title: `S${s.slot} ${s.contentType}`, status: s.status, slot: s.slot,
        });
      }
    });

    clinic.reels.forEach((r) => {
      // Place reels on the Monday of their week
      const firstStoryDate = clinic.stories.find((s) => s.week === r.week)?.date;
      if (firstStoryDate) {
        items.push({
          id: r.id, date: firstStoryDate, type: 'reel',
          title: r.theme, status: r.status,
        });
      }
    });

    clinic.seoChannels.forEach((ch) => {
      ch.posts?.forEach((p) => {
        if (p.publishDate) {
          items.push({
            id: p.id, date: p.publishDate, type: 'seo',
            title: `${ch.channel}: ${p.title}`, status: p.status,
          });
        }
      });
    });

    // Find min/max months
    const dates = items.map((i) => i.date).filter(Boolean).sort();
    if (dates.length === 0) return { allItems: items, monthRange: [] };

    const start = new Date(dates[0] + 'T00:00:00');
    const end = new Date(dates[dates.length - 1] + 'T00:00:00');

    const months: string[] = [];
    const cursor = new Date(start.getFullYear(), start.getMonth(), 1);
    while (cursor <= end || months.length < 3) {
      months.push(`${cursor.getFullYear()}-${String(cursor.getMonth() + 1).padStart(2, '0')}`);
      cursor.setMonth(cursor.getMonth() + 1);
    }

    return { allItems: items, monthRange: months };
  }, [clinic]);

  // Index items by date
  const itemsByDate = useMemo(() => {
    const map: Record<string, CalItem[]> = {};
    allItems.forEach((item) => {
      if (!map[item.date]) map[item.date] = [];
      map[item.date].push(item);
    });
    return map;
  }, [allItems]);

  // Current visible month
  const [monthIdx, setMonthIdx] = useState(() => {
    // Default to the month containing today, or first month
    const today = new Date().toISOString().slice(0, 7);
    const idx = monthRange.indexOf(today);
    return idx >= 0 ? idx : 0;
  });

  const currentMonth = monthRange[monthIdx] ?? monthRange[0];

  // Build the 6×7 grid for the current month
  const calendarGrid = useMemo(() => {
    if (!currentMonth) return [];

    const [year, month] = currentMonth.split('-').map(Number);
    const firstDay = new Date(year, month - 1, 1);

    // Day of week for the 1st (0=Sun, shift so Mon=0)
    const startDow = (firstDay.getDay() + 6) % 7;

    // Start from the Monday of the first week
    const gridStart = new Date(year, month - 1, 1 - startDow);

    // Always generate 6 weeks (42 days) for consistent grid
    const days: string[] = [];
    for (let i = 0; i < 42; i++) {
      const d = new Date(gridStart);
      d.setDate(d.getDate() + i);
      const y = d.getFullYear();
      const m = String(d.getMonth() + 1).padStart(2, '0');
      const dd = String(d.getDate()).padStart(2, '0');
      days.push(`${y}-${m}-${dd}`);
    }

    // Split into weeks
    const weeks: string[][] = [];
    for (let i = 0; i < days.length; i += 7) {
      weeks.push(days.slice(i, i + 7));
    }
    return weeks;
  }, [currentMonth]);

  const handleDragEnd = useCallback(async (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over || !active) return;
    await fetch(`/api/portal/${clinicId}/schedule`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ itemId: String(active.id), newDate: String(over.id) }),
    });
    refresh();
  }, [clinicId, refresh]);

  if (isLoading || !clinic) {
    return <div className="flex items-center justify-center min-h-[60vh] text-dim text-sm">{t('general.loading')}</div>;
  }

  const today = new Date().toISOString().slice(0, 10);
  const monthNames = lang === 'he' ? MONTH_NAMES_HE : MONTH_NAMES_EN;
  const dayHeaders = lang === 'he' ? DAY_HEADERS_HE : DAY_HEADERS_EN;
  const [curYear, curMonth] = (currentMonth ?? '2026-01').split('-').map(Number);

  // Count items per type for the legend
  const storyCount = allItems.filter((i) => i.type === 'story').length;
  const reelCount = allItems.filter((i) => i.type === 'reel').length;
  const seoCount = allItems.filter((i) => i.type === 'seo').length;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="font-heading text-xl font-bold">{t('calendar.title')}</h1>
        <button
          onClick={() => setPaused(!paused)}
          className={`px-4 py-1.5 text-xs rounded-lg font-medium transition-colors ${
            paused ? 'bg-success/15 text-success hover:bg-success/25' : 'bg-warning/15 text-warning hover:bg-warning/25'
          }`}
        >
          {paused ? t('action.resume') : t('action.pause')}
        </button>
      </div>

      {paused && (
        <div className="bg-warning/10 border border-warning/20 rounded-xl px-4 py-3 text-sm text-warning">
          Content schedule is paused. No new content will be published until resumed.
        </div>
      )}

      {/* Legend */}
      <div className="flex items-center gap-4 text-xs text-dim">
        <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-accent" /> Stories ({storyCount})</span>
        <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-info" /> Reels ({reelCount})</span>
        <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-success" /> SEO ({seoCount})</span>
        <span className="ms-auto text-muted">{t('calendar.dragToReschedule')}</span>
      </div>

      {/* Month navigator */}
      <div className="flex items-center justify-center gap-6 py-2">
        <button
          onClick={() => setMonthIdx(Math.max(0, monthIdx - 1))}
          disabled={monthIdx <= 0}
          className="w-8 h-8 flex items-center justify-center rounded-lg bg-card border border-border text-dim hover:text-foreground hover:border-border-hover disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          ‹
        </button>
        <div className="text-center min-w-[180px]">
          <div className="font-heading text-lg font-bold">{monthNames[curMonth - 1]}</div>
          <div className="text-xs text-muted">{curYear}</div>
        </div>
        <button
          onClick={() => setMonthIdx(Math.min(monthRange.length - 1, monthIdx + 1))}
          disabled={monthIdx >= monthRange.length - 1}
          className="w-8 h-8 flex items-center justify-center rounded-lg bg-card border border-border text-dim hover:text-foreground hover:border-border-hover disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          ›
        </button>
      </div>

      {/* Calendar grid */}
      <DndContext onDragEnd={handleDragEnd}>
        <div className="bg-card border border-border rounded-2xl overflow-hidden">
          {/* Day-of-week headers */}
          <div className="grid grid-cols-7 border-b border-border">
            {dayHeaders.map((d) => (
              <div key={d} className="text-center text-xs text-muted font-heading font-medium py-2 border-e border-border last:border-e-0">
                {d}
              </div>
            ))}
          </div>

          {/* Week rows */}
          {calendarGrid.map((week, wi) => (
            <div key={wi} className="grid grid-cols-7">
              {week.map((date) => {
                const [, m] = date.split('-').map(Number);
                return (
                  <CalendarDayCell
                    key={date}
                    date={date}
                    items={itemsByDate[date] ?? []}
                    isToday={date === today}
                    isCurrentMonth={m === curMonth}
                  />
                );
              })}
            </div>
          ))}
        </div>
      </DndContext>
    </div>
  );
}
