import { NextResponse } from 'next/server';
import { getClinicDetail, writeClinicDetail } from '@/lib/data';

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  const clinic = getClinicDetail(id);
  if (!clinic) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json({ stories: clinic.stories });
}

export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  const clinic = getClinicDetail(id);
  if (!clinic) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  const body = await request.json();
  const { storyId, updates } = body as {
    storyId?: string;
    updates?: Record<string, unknown>;
  };

  // Bulk approve: { bulkApprove: true, week: N }
  if (body.bulkApprove && body.week) {
    clinic.stories = clinic.stories.map((s) =>
      s.week === body.week && (s.status === 'generated' || s.status === 'pending')
        ? { ...s, status: 'approved' as const, approvedAt: new Date().toISOString() }
        : s
    );
    writeClinicDetail(id, clinic);
    return NextResponse.json({ ok: true, updated: clinic.stories.filter((s) => s.week === body.week).length });
  }

  // Single story update
  if (storyId && updates) {
    clinic.stories = clinic.stories.map((s) =>
      s.id === storyId ? { ...s, ...updates } : s
    );
    writeClinicDetail(id, clinic);
    return NextResponse.json({ ok: true });
  }

  return NextResponse.json({ error: 'Invalid request' }, { status: 400 });
}
