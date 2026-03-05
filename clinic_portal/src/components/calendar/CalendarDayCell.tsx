'use client';

import { useDroppable } from '@dnd-kit/core';
import type { CalendarItem } from '@/types';

interface CalendarDayCellProps {
  date: string;
  items: CalendarItem[];
  isToday: boolean;
  isCurrentMonth: boolean;
}

const typeColors: Record<string, string> = {
  story: 'border-s-accent',
  reel: 'border-s-info',
  seo: 'border-s-success',
};

const typeDots: Record<string, string> = {
  story: 'bg-accent',
  reel: 'bg-info',
  seo: 'bg-success',
};

export default function CalendarDayCell({ date, items, isToday, isCurrentMonth }: CalendarDayCellProps) {
  const { setNodeRef, isOver } = useDroppable({ id: date });
  const day = new Date(date + 'T00:00:00').getDate();

  return (
    <div
      ref={setNodeRef}
      className={`min-h-[90px] border-b border-e border-border p-1.5 transition-colors ${
        isOver ? 'bg-accent/5' : ''
      } ${!isCurrentMonth ? 'opacity-30' : ''}`}
    >
      {/* Day number */}
      <div className={`text-xs font-heading font-semibold mb-1 ${
        isToday
          ? 'text-background bg-accent w-5 h-5 rounded-full flex items-center justify-center'
          : 'text-dim'
      }`}>
        {day}
      </div>

      {/* Content items */}
      <div className="space-y-0.5">
        {items.slice(0, 3).map((item) => (
          <div
            key={item.id}
            className={`text-[10px] leading-tight px-1 py-0.5 rounded border-s-2 ${typeColors[item.type]} bg-background/60 truncate cursor-grab active:cursor-grabbing`}
            data-id={item.id}
          >
            {item.title}
          </div>
        ))}
        {items.length > 3 && (
          <div className="text-[10px] text-muted ps-1">+{items.length - 3}</div>
        )}
      </div>

      {/* Dot summary when too small (mobile) */}
      {items.length > 0 && (
        <div className="flex gap-0.5 mt-1 md:hidden">
          {Array.from(new Set(items.map((i) => i.type))).map((type) => (
            <span key={type} className={`w-1.5 h-1.5 rounded-full ${typeDots[type]}`} />
          ))}
        </div>
      )}
    </div>
  );
}
