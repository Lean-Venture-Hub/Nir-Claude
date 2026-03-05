'use client';

import { useState } from 'react';
import { useT } from '@/lib/i18n';
import StatusBadge from '@/components/StatusBadge';
import ScriptEditor from './ScriptEditor';
import type { ReelItem } from '@/types';

interface ReelCardProps {
  reel: ReelItem;
  onApproveScript: (id: string) => void;
  onApproveVideo: (id: string) => void;
  onReject: (id: string) => void;
  onEditScript: (id: string, script: string) => void;
  onRequestRevision: (id: string, note: string) => void;
}

export default function ReelCard({
  reel, onApproveScript, onApproveVideo, onReject, onEditScript, onRequestRevision,
}: ReelCardProps) {
  const { t } = useT();
  const [showScript, setShowScript] = useState(false);
  const [showRevision, setShowRevision] = useState(false);
  const [revisionNote, setRevisionNote] = useState('');

  const canApproveScript = reel.status === 'scripted' && !reel.scriptApproved;
  const canApproveVideo = reel.status === 'generated' && reel.scriptApproved;
  const canReject = reel.status !== 'published' && reel.status !== 'rejected';

  return (
    <>
      <div className="bg-card border border-border rounded-2xl p-5 hover:border-border-hover transition-colors fade-up">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-lg">▶</span>
            <span className="font-heading text-sm font-semibold">{reel.theme}</span>
          </div>
          <StatusBadge status={reel.status} />
        </div>

        {/* Info */}
        <div className="flex gap-4 mb-3 text-xs text-dim">
          <span>{t('general.week')} {reel.week}</span>
          {reel.duration != null && <span>{reel.duration}s</span>}
          {reel.cost != null && <span>${reel.cost.toFixed(2)}</span>}
        </div>

        {/* Video preview placeholder */}
        <div className="aspect-video bg-background rounded-xl mb-3 flex items-center justify-center">
          <div className="text-center">
            <div className="text-3xl text-muted mb-1">▶</div>
            <div className="text-xs text-muted">{reel.status === 'generated' ? 'Video ready' : reel.status === 'scripted' ? 'Script ready' : reel.status}</div>
          </div>
        </div>

        {/* Script preview */}
        {reel.scriptText && (
          <div
            className="text-xs text-dim leading-relaxed line-clamp-3 mb-3 cursor-pointer hover:text-foreground transition-colors"
            dir="rtl"
            onClick={() => setShowScript(true)}
          >
            {reel.scriptText}
          </div>
        )}

        {/* Revision request display */}
        {reel.revisionRequest && (
          <div className="text-xs text-warning bg-warning/10 rounded-lg px-3 py-2 mb-3">
            Revision: {reel.revisionRequest}
          </div>
        )}

        {/* Actions */}
        <div className="flex flex-wrap gap-1.5">
          {canApproveScript && (
            <button
              onClick={() => onApproveScript(reel.id)}
              className="flex-1 px-3 py-1.5 text-xs bg-success/15 text-success rounded-lg hover:bg-success/25 transition-colors font-medium"
            >
              {t('reels.approveScript')}
            </button>
          )}
          {canApproveVideo && (
            <button
              onClick={() => onApproveVideo(reel.id)}
              className="flex-1 px-3 py-1.5 text-xs bg-success/15 text-success rounded-lg hover:bg-success/25 transition-colors font-medium"
            >
              {t('reels.approveVideo')}
            </button>
          )}
          {(reel.status === 'scripted' || reel.status === 'generated') && (
            <button
              onClick={() => setShowScript(true)}
              className="px-3 py-1.5 text-xs bg-background text-dim rounded-lg hover:text-foreground transition-colors"
            >
              {t('action.edit')}
            </button>
          )}
          {canReject && (
            <button
              onClick={() => setShowRevision(true)}
              className="px-3 py-1.5 text-xs bg-warning/15 text-warning rounded-lg hover:bg-warning/25 transition-colors"
            >
              {t('action.requestRevision')}
            </button>
          )}
          {canReject && (
            <button
              onClick={() => onReject(reel.id)}
              className="px-3 py-1.5 text-xs bg-error/15 text-error rounded-lg hover:bg-error/25 transition-colors"
            >
              {t('action.reject')}
            </button>
          )}
        </div>
      </div>

      {/* Script Editor Modal */}
      {showScript && (
        <ScriptEditor
          script={reel.scriptText ?? ''}
          onSave={(text) => onEditScript(reel.id, text)}
          onClose={() => setShowScript(false)}
        />
      )}

      {/* Revision Request Modal */}
      {showRevision && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={() => setShowRevision(false)}>
          <div className="bg-card border border-border rounded-2xl p-6 w-full max-w-md mx-4 fade-up" onClick={(e) => e.stopPropagation()}>
            <h3 className="font-heading text-lg font-semibold mb-4">{t('action.requestRevision')}</h3>
            <textarea
              value={revisionNote}
              onChange={(e) => setRevisionNote(e.target.value)}
              placeholder="What needs to change?"
              className="w-full bg-background border border-border rounded-xl p-3 text-sm text-foreground resize-none focus:outline-none focus:border-accent"
              rows={4}
            />
            <div className="flex gap-2 justify-end mt-4">
              <button onClick={() => setShowRevision(false)} className="px-4 py-2 text-sm text-dim">{t('action.cancel')}</button>
              <button
                onClick={() => {
                  onRequestRevision(reel.id, revisionNote);
                  setShowRevision(false);
                  setRevisionNote('');
                }}
                className="px-4 py-2 text-sm bg-warning text-background rounded-lg font-medium"
              >
                {t('action.requestRevision')}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
