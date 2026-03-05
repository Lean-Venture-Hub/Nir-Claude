import { NextResponse } from 'next/server';
import { getTemplatesData } from '@/lib/data';

export const dynamic = 'force-dynamic';

export async function GET() {
  const data = getTemplatesData();
  if (!data) return NextResponse.json({ error: 'No data' }, { status: 404 });
  return NextResponse.json(data);
}
