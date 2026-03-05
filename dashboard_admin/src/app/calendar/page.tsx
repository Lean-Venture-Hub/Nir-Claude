'use client';

import { useState, useMemo } from 'react';
import { useCalendar } from '@/lib/hooks';
import type { CalendarData, CalendarSlot } from '@/types';

const TYPE_LABELS: Record<string, string> = { A: 'Auto', P: 'Photo', R: 'Review' };

function SlotCell({ slot }: { slot: CalendarSlot['slots'][0]; }) {
  const pct = slot.total > 0 ? (slot.published / slot.total) * 100 : 0;
  const genPct = slot.total > 0 ? (slot.generated / slot.total) * 100 : 0;
  const isComplete = pct > 90;
  const isFuture = slot.generated === 0 && slot.published === 0;

  return (
    <div className={`border rounded-lg p-2 text-center transition-colors ${
      isFuture
        ? 'border-border bg-[rgba(255,255,255,0.02)]'
        : isComplete
          ? 'border-success/20 bg-success/5'
          : 'border-accent/20 bg-accent/5'
    }`}>
      <div className="text-xs text-muted font-body">{slot.time}</div>
      <div className="text-xs text-dim font-body">{TYPE_LABELS[slot.contentType]}</div>
      {!isFuture && (
        <>
          <div className="font-heading text-sm font-bold mt-1" style={{
            color: isComplete ? 'var(--success)' : 'var(--accent)'
          }}>
            {pct.toFixed(0)}%
          </div>
          <div className="w-full h-1 bg-[rgba(255,255,255,0.05)] rounded-full mt-1">
            <div className="h-full bg-success rounded-full" style={{ width: `${pct}%` }} />
          </div>
          <div className="text-[10px] text-muted font-body mt-0.5">
            {slot.published}/{slot.total} pub · {slot.generated} gen
          </div>
        </>
      )}
      {isFuture && <div className="text-xs text-muted font-body mt-1">Scheduled</div>}
    </div>
  );
}

export default function CalendarPage() {
  const { data, isLoading } = useCalendar();
  const calendar = data as CalendarData | undefined;
  const [currentWeek, setCurrentWeek] = useState(10);

  const weeks = useMemo(() => {
    if (!calendar?.days) return [];
    const grouped: Record<number, CalendarSlot[]> = {};
    calendar.days.forEach((d) => {
      if (!grouped[d.weekNumber]) grouped[d.weekNumber] = [];
      grouped[d.weekNumber].push(d);
    });
    return Object.entries(grouped).map(([w, days]) => ({
      week: parseInt(w),
      theme: days[0]?.theme || '',
      days,
    }));
  }, [calendar]);

  const weekData = weeks.find((w) => w.week === currentWeek);

  if (isLoading || !calendar) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="text-dim font-body">Loading calendar...</div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6">
      <div className="fade-up">
        <p className="text-xs uppercase tracking-widest text-accent font-heading mb-1">Content Calendar</p>
        <h2 className="font-heading text-2xl font-bold">13-Week Production Schedule</h2>
        <p className="text-sm text-dim font-body mt-1">439 clinics × 3 stories/day = 1,317 assets per day</p>
      </div>

      {/* Week Navigator */}
      <div className="flex gap-1 bg-card border border-border rounded-2xl p-2 overflow-x-auto">
        {weeks.map((w) => {
          const isActive = w.week === currentWeek;
          const isCurrent = w.week === 10;
          return (
            <button
              key={w.week}
              onClick={() => setCurrentWeek(w.week)}
              className={`px-3 py-2 rounded-xl text-xs font-body whitespace-nowrap transition-colors ${
                isActive
                  ? 'bg-accent/20 text-accent border border-accent/30'
                  : 'hover:bg-card-hover text-dim'
              } ${isCurrent ? 'ring-1 ring-accent/40' : ''}`}
            >
              W{w.week}: {w.theme}
            </button>
          );
        })}
      </div>

      {/* Day/Slot Grid */}
      {weekData && (
        <div className="bg-card border border-border rounded-2xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-heading text-sm font-semibold">
              Week {weekData.week}: {weekData.theme}
            </h3>
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentWeek(Math.max(1, currentWeek - 1))}
                className="px-3 py-1 text-xs bg-card-hover border border-border rounded-lg hover:border-border-hover font-body"
              >
                ← Prev
              </button>
              <button
                onClick={() => setCurrentWeek(Math.min(13, currentWeek + 1))}
                className="px-3 py-1 text-xs bg-card-hover border border-border rounded-lg hover:border-border-hover font-body"
              >
                Next →
              </button>
            </div>
          </div>

          <div className="grid grid-cols-7 gap-3">
            {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day) => (
              <div key={day} className="text-center text-xs text-muted font-body pb-2">{day}</div>
            ))}
            {weekData.days.map((day) => (
              <div key={day.day} className="space-y-1">
                <div className="text-xs text-dim font-body text-center mb-1">
                  Day {day.day}
                  <br />
                  <span className="text-muted">{day.date}</span>
                </div>
                {day.slots.map((slot) => (
                  <SlotCell key={slot.slot} slot={slot} />
                ))}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Summary */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Total Days', value: calendar.totalDays },
          { label: 'Total Weeks', value: calendar.totalWeeks },
          { label: 'Assets/Day', value: '1,317' },
          { label: 'Total Assets', value: (calendar.totalDays * 3 * 439).toLocaleString() },
        ].map((s) => (
          <div key={s.label} className="bg-card border border-border rounded-2xl p-4 text-center">
            <p className="text-xs text-dim font-body">{s.label}</p>
            <p className="font-heading text-2xl font-bold text-accent">{s.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
