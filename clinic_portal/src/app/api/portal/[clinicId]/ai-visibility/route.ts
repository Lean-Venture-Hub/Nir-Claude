import { NextResponse } from 'next/server';
import { getClinicDetail } from '@/lib/data';

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  if (isNaN(id)) {
    return NextResponse.json({ error: 'Invalid clinic ID' }, { status: 400 });
  }

  const clinic = getClinicDetail(id);
  if (!clinic) {
    return NextResponse.json({ error: 'Clinic not found' }, { status: 404 });
  }

  return NextResponse.json(clinic.aiVisibility ?? null);
}
