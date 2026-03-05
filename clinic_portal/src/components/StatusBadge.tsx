'use client';

import { useT } from '@/lib/i18n';
import type { TranslationKey } from '@/lib/i18n';

interface StatusBadgeProps {
  status: string;
  className?: string;
}

export default function StatusBadge({ status, className = '' }: StatusBadgeProps) {
  const { t } = useT();
  const key = `status.${status}` as TranslationKey;
  const label = t(key);

  return (
    <span className={`badge-${status} text-xs font-medium px-2 py-0.5 rounded-full ${className}`}>
      {label}
    </span>
  );
}
