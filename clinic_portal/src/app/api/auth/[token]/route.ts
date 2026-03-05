import { NextResponse } from 'next/server';
import { resolveToken } from '@/lib/auth';

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ token: string }> }
) {
  const { token } = await params;
  const clinicId = resolveToken(token);

  if (!clinicId) {
    return NextResponse.json({ error: 'Invalid token' }, { status: 404 });
  }

  return NextResponse.json({ clinicId });
}
