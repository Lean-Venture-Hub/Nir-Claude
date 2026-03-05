import fs from 'fs';
import path from 'path';
import type { TokenMap } from '@/types';

const DATA_DIR = path.join(process.cwd(), '..', 'dashboard_admin', 'data');
const TOKENS_PATH = path.join(DATA_DIR, 'tokens.json');

export function resolveToken(token: string): number | null {
  try {
    const raw = fs.readFileSync(TOKENS_PATH, 'utf-8');
    const tokenMap: TokenMap = JSON.parse(raw);
    return tokenMap[token] ?? null;
  } catch {
    return null;
  }
}
