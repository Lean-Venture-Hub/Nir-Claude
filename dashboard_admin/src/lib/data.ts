import fs from 'fs';
import path from 'path';
import type {
  SystemStatus,
  ClinicIndex,
  ClinicDetail,
  CalendarData,
  TemplatesData,
  BudgetData,
} from '@/types';

const DATA_DIR = path.join(process.cwd(), 'data');

function readJSON<T>(filePath: string): T | null {
  try {
    const raw = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

export function getSystemStatus(): SystemStatus | null {
  return readJSON<SystemStatus>(path.join(DATA_DIR, 'system-status.json'));
}

export function getClinicIndex(): ClinicIndex | null {
  return readJSON<ClinicIndex>(path.join(DATA_DIR, 'clinics', 'index.json'));
}

export function getClinicDetail(id: number): ClinicDetail | null {
  const padded = String(id).padStart(3, '0');
  return readJSON<ClinicDetail>(
    path.join(DATA_DIR, 'clinics', `clinic-${padded}.json`)
  );
}

export function getCalendarData(): CalendarData | null {
  return readJSON<CalendarData>(path.join(DATA_DIR, 'calendar.json'));
}

export function getTemplatesData(): TemplatesData | null {
  return readJSON<TemplatesData>(path.join(DATA_DIR, 'templates.json'));
}

export function getBudgetData(): BudgetData | null {
  return readJSON<BudgetData>(path.join(DATA_DIR, 'budget.json'));
}
