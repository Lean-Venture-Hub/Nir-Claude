'use client';

import { useState } from 'react';
import { useT } from '@/lib/i18n';

interface CaptionEditorProps {
  caption: string;
  editedCaption?: string;
  onSave: (newCaption: string) => void;
  onCancel: () => void;
}

export default function CaptionEditor({ caption, editedCaption, onSave, onCancel }: CaptionEditorProps) {
  const [text, setText] = useState(editedCaption ?? caption);
  const { t } = useT();

  return (
    <div className="space-y-2">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full bg-background border border-border rounded-xl p-3 text-sm text-foreground resize-none focus:outline-none focus:border-accent"
        rows={3}
        dir="rtl"
      />
      <div className="flex gap-2 justify-end">
        <button
          onClick={onCancel}
          className="px-3 py-1.5 text-xs text-dim hover:text-foreground transition-colors"
        >
          {t('action.cancel')}
        </button>
        <button
          onClick={() => onSave(text)}
          className="px-3 py-1.5 text-xs bg-accent text-background rounded-lg hover:bg-accent/80 transition-colors font-medium"
        >
          {t('action.save')}
        </button>
      </div>
    </div>
  );
}
