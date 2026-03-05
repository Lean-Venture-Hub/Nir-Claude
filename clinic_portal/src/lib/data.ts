import fs from 'fs';
import path from 'path';
import os from 'os';
import type { ClinicDetail, TemplateInfo } from '@/types';

const DATA_DIR = path.join(process.cwd(), '..', 'dashboard_admin', 'data');

function readJSON<T>(filePath: string): T | null {
  try {
    const raw = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

function clinicPath(id: number): string {
  const padded = String(id).padStart(3, '0');
  return path.join(DATA_DIR, 'clinics', `clinic-${padded}.json`);
}

export function getClinicDetail(id: number): ClinicDetail | null {
  return readJSON<ClinicDetail>(clinicPath(id));
}

export function writeClinicDetail(id: number, data: ClinicDetail): boolean {
  const target = clinicPath(id);
  const tmpPath = path.join(os.tmpdir(), `clinic-${id}-${Date.now()}.tmp`);
  try {
    fs.writeFileSync(tmpPath, JSON.stringify(data, null, 2), 'utf-8');
    fs.renameSync(tmpPath, target);
    return true;
  } catch {
    try { fs.unlinkSync(tmpPath); } catch { /* ignore */ }
    return false;
  }
}

export function getTemplates(): TemplateInfo[] {
  try {
    const raw = fs.readFileSync(path.join(DATA_DIR, 'templates.json'), 'utf-8');
    const parsed = JSON.parse(raw);
    return (parsed.templates ?? []).map((t: Record<string, unknown>) => ({
      id: t.id,
      name: t.name,
      category: t.category,
      previewPath: t.previewPath,
    }));
  } catch {
    return [];
  }
}

export function getPhotoUploadDir(clinicId: number): string {
  const dir = path.join(DATA_DIR, 'clinics', `clinic-${String(clinicId).padStart(3, '0')}`, 'photos');
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  return dir;
}
