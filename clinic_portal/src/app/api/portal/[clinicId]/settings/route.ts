import { NextResponse } from 'next/server';
import { getClinicDetail, writeClinicDetail } from '@/lib/data';
import type { ClinicPortalSettings } from '@/types';

const DEFAULT_SETTINGS: ClinicPortalSettings = {
  autoApproveRules: { stories: false, reels: false, seo: false },
  toneOfVoice: 'professional',
  notificationPrefs: { email: true, whatsapp: false, weeklyDigest: true },
  brandColors: { primary: '#16a34a', accent: '#e8a849' },
  photoVault: [],
};

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  const clinic = getClinicDetail(id);
  if (!clinic) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  const settings = clinic.portalSettings ?? {
    ...DEFAULT_SETTINGS,
    brandColors: clinic.colors,
  };

  return NextResponse.json(settings);
}

export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  const clinic = getClinicDetail(id);
  if (!clinic) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  const updates = await request.json() as Partial<ClinicPortalSettings>;
  clinic.portalSettings = {
    ...(clinic.portalSettings ?? { ...DEFAULT_SETTINGS, brandColors: clinic.colors }),
    ...updates,
  };

  // Also sync brand colors to the main clinic object
  if (updates.brandColors) {
    clinic.colors = updates.brandColors;
  }

  writeClinicDetail(id, clinic);
  return NextResponse.json({ ok: true });
}
