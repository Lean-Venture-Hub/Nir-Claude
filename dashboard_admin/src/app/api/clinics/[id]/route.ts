import { NextResponse } from 'next/server';
import { getClinicDetail } from '@/lib/data';

export const dynamic = 'force-dynamic';

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const numId = parseInt(id, 10);
  if (isNaN(numId)) return NextResponse.json({ error: 'Invalid ID' }, { status: 400 });

  const data = getClinicDetail(numId);
  if (!data) return NextResponse.json({ error: 'Clinic not found' }, { status: 404 });
  return NextResponse.json(data);
}
