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
  return NextResponse.json({ seoChannels: clinic.seoChannels });
}

export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  const clinic = getClinicDetail(id);
  if (!clinic) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  const { channel, postId, updates } = await request.json() as {
    channel: string;
    postId?: string;
    updates: Record<string, unknown>;
  };

  clinic.seoChannels = clinic.seoChannels.map((ch) => {
    if (ch.channel !== channel) return ch;
    if (postId && ch.posts) {
      return {
        ...ch,
        posts: ch.posts.map((p) => (p.id === postId ? { ...p, ...updates } : p)),
      };
    }
    return { ...ch, ...updates };
  });

  writeClinicDetail(id, clinic);
  return NextResponse.json({ ok: true });
}
