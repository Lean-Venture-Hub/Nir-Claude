'use client';

import { useT } from '@/lib/i18n';

interface BulkApproveBarProps {
  selectedCount: number;
  onBulkApprove: () => void;
  onClear: () => void;
}

export default function BulkApproveBar({ selectedCount, onBulkApprove, onClear }: BulkApproveBarProps) {
  const { t } = useT();
  if (selectedCount === 0) return null;

  return (
    <div className="sticky top-12 z-20 bg-accent/10 backdrop-blur-md border border-accent/20 rounded-xl px-4 py-3 flex items-center justify-between mb-4 fade-up">
      <span className="text-sm text-accent font-medium">
        {selectedCount} selected
      </span>
      <div className="flex gap-2">
        <button
          onClick={onClear}
          className="px-3 py-1.5 text-xs text-dim hover:text-foreground transition-colors"
        >
          {t('action.cancel')}
        </button>
        <button
          onClick={onBulkApprove}
          className="px-4 py-1.5 text-xs bg-accent text-background rounded-lg hover:bg-accent/80 transition-colors font-medium"
        >
          {t('action.bulkApprove')} ({selectedCount})
        </button>
      </div>
    </div>
  );
}
