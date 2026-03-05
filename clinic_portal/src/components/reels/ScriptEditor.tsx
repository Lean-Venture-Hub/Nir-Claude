'use client';

import { useState } from 'react';
import { useT } from '@/lib/i18n';

interface ScriptEditorProps {
  script: string;
  onSave: (text: string) => void;
  onClose: () => void;
}

export default function ScriptEditor({ script, onSave, onClose }: ScriptEditorProps) {
  const [text, setText] = useState(script);
  const { t } = useT();

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-card border border-border rounded-2xl p-6 w-full max-w-lg mx-4 fade-up" onClick={(e) => e.stopPropagation()}>
        <h3 className="font-heading text-lg font-semibold mb-4">{t('reels.script')}</h3>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full bg-background border border-border rounded-xl p-4 text-sm text-foreground resize-none focus:outline-none focus:border-accent"
          rows={10}
          dir="rtl"
        />
        <div className="flex gap-2 justify-end mt-4">
          <button onClick={onClose} className="px-4 py-2 text-sm text-dim hover:text-foreground transition-colors">
            {t('action.cancel')}
          </button>
          <button
            onClick={() => { onSave(text); onClose(); }}
            className="px-4 py-2 text-sm bg-accent text-background rounded-lg hover:bg-accent/80 transition-colors font-medium"
          >
            {t('action.save')}
          </button>
        </div>
      </div>
    </div>
  );
}
