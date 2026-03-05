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
  return NextResponse.json({ reels: clinic.reels });
}

export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  const clinic = getClinicDetail(id);
  if (!clinic) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  const { reelId, updates } = await request.json() as {
    reelId: string;
    updates: Record<string, unknown>;
  };

  clinic.reels = clinic.reels.map((r) =>
    r.id === reelId ? { ...r, ...updates } : r
  );

  writeClinicDetail(id, clinic);
  return NextResponse.json({ ok: true });
}
