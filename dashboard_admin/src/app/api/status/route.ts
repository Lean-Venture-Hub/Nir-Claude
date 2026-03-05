import { NextResponse } from 'next/server';
import { getSystemStatus } from '@/lib/data';

export const dynamic = 'force-dynamic';

export async function GET() {
  const data = getSystemStatus();
  if (!data) return NextResponse.json({ error: 'No data' }, { status: 404 });
  return NextResponse.json(data);
}
