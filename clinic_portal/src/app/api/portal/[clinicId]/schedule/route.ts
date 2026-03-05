import { NextResponse } from 'next/server';
import { getClinicDetail, writeClinicDetail } from '@/lib/data';
import type { CalendarItem } from '@/types';

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  const clinic = getClinicDetail(id);
  if (!clinic) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  // Build unified calendar from all content types
  const items: CalendarItem[] = [];

  clinic.stories.forEach((s) => {
    items.push({
      id: s.id,
      date: s.date,
      type: 'story',
      title: `${s.theme} — Slot ${s.slot}`,
      status: s.status,
      slot: s.slot,
    });
  });

  clinic.reels.forEach((r) => {
    items.push({
      id: r.id,
      date: '', // reels don't have individual dates, use week
      type: 'reel',
      title: r.theme,
      status: r.status,
    });
  });

  clinic.seoChannels.forEach((ch) => {
    ch.posts?.forEach((p) => {
      items.push({
        id: p.id,
        date: p.publishDate ?? '',
        type: 'seo',
        title: p.title,
        status: p.status,
        channel: ch.channel,
      });
    });
  });

  return NextResponse.json({ items });
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  const clinic = getClinicDetail(id);
  if (!clinic) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  const { itemId, newDate } = await request.json() as {
    itemId: string;
    newDate: string;
  };

  // Find and update the story date
  const story = clinic.stories.find((s) => s.id === itemId);
  if (story) {
    story.date = newDate;
    writeClinicDetail(id, clinic);
    return NextResponse.json({ ok: true });
  }

  return NextResponse.json({ error: 'Item not found' }, { status: 404 });
}
