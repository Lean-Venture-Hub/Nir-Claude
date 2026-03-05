import { NextResponse } from 'next/server';
import { getClinicDetail, writeClinicDetail, getPhotoUploadDir } from '@/lib/data';
import fs from 'fs';
import path from 'path';

export async function POST(
  request: Request,
  { params }: { params: Promise<{ clinicId: string }> }
) {
  const { clinicId } = await params;
  const id = parseInt(clinicId, 10);
  const clinic = getClinicDetail(id);
  if (!clinic) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  const formData = await request.formData();
  const file = formData.get('photo') as File | null;
  if (!file) return NextResponse.json({ error: 'No file' }, { status: 400 });

  const uploadDir = getPhotoUploadDir(id);
  const filename = `${Date.now()}-${file.name.replace(/[^a-zA-Z0-9._-]/g, '')}`;
  const filepath = path.join(uploadDir, filename);

  const buffer = Buffer.from(await file.arrayBuffer());
  fs.writeFileSync(filepath, buffer);

  // Add to portal settings photo vault
  const photoUrl = `/photos/${filename}`;
  if (!clinic.portalSettings) {
    clinic.portalSettings = {
      autoApproveRules: { stories: false, reels: false, seo: false },
      toneOfVoice: 'professional',
      notificationPrefs: { email: true, whatsapp: false, weeklyDigest: true },
      brandColors: clinic.colors,
      photoVault: [],
    };
  }
  clinic.portalSettings.photoVault.push(photoUrl);
  writeClinicDetail(id, clinic);

  return NextResponse.json({ ok: true, photoUrl, filename });
}
