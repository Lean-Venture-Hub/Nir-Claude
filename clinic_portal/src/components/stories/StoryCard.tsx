'use client';

import { useState } from 'react';
import { useT } from '@/lib/i18n';
import StatusBadge from '@/components/StatusBadge';
import CaptionEditor from './CaptionEditor';
import type { StorySlot } from '@/types';

interface StoryCardProps {
  story: StorySlot;
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
  onEditCaption: (id: string, caption: string) => void;
  onSwapTemplate: (id: string) => void;
  onUploadPhoto: (id: string) => void;
  dayLabel?: string;
  selected?: boolean;
  onSelect?: (id: string) => void;
}

const contentTypeLabels: Record<string, string> = { A: 'Authority', P: 'Personal', R: 'Review' };

export default function StoryCard({
  story, onApprove, onReject, onEditCaption, onSwapTemplate, onUploadPhoto, dayLabel, selected, onSelect,
}: StoryCardProps) {
  const { t } = useT();
  const [editing, setEditing] = useState(false);
  const canApprove = story.status === 'generated' || story.status === 'pending';
  const canEdit = story.status !== 'published';

  return (
    <div className={`bg-card border rounded-2xl p-4 transition-all hover:border-border-hover ${
      selected ? 'border-accent ring-1 ring-accent/30' : 'border-border'
    }`}>
      {/* Day label */}
      {dayLabel && (
        <div className="text-xs text-muted mb-2 font-heading">{dayLabel}</div>
      )}
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {onSelect && canApprove && (
            <input
              type="checkbox"
              checked={selected}
              onChange={() => onSelect(story.id)}
              className="rounded border-border accent-[var(--accent)]"
            />
          )}
          <span className="text-xs text-muted">Slot {story.slot}</span>
          <span className="text-xs px-1.5 py-0.5 rounded bg-background text-dim">{contentTypeLabels[story.contentType]}</span>
        </div>
        <StatusBadge status={story.status} />
      </div>

      {/* Template preview area */}
      <div className="aspect-[9/16] bg-background rounded-xl mb-3 flex items-center justify-center relative overflow-hidden">
        {story.previewUrl ? (
          <img src={story.previewUrl} alt="" className="w-full h-full object-cover" />
        ) : (
          <div className="text-center">
            <div className="text-2xl text-muted mb-1">◧</div>
            <div className="text-xs text-muted">{story.templateId ? `T-${story.templateId}` : 'No template'}</div>
          </div>
        )}
        {story.ownerPhotoUrl && (
          <div className="absolute bottom-2 end-2 w-8 h-8 rounded-full bg-accent/20 border border-accent/30 flex items-center justify-center text-xs">📷</div>
        )}
      </div>

      {/* Caption */}
      {editing ? (
        <CaptionEditor
          caption={story.caption ?? ''}
          editedCaption={story.editedCaption}
          onSave={(text) => {
            onEditCaption(story.id, text);
            setEditing(false);
          }}
          onCancel={() => setEditing(false)}
        />
      ) : (
        <div className="mb-3">
          <p className="text-xs text-dim leading-relaxed line-clamp-2" dir="rtl">
            {story.editedCaption ?? story.caption ?? '—'}
          </p>
        </div>
      )}

      {/* Theme */}
      <div className="text-xs text-muted mb-3">{story.theme}</div>

      {/* Actions */}
      {canEdit && (
        <div className="flex flex-wrap gap-1.5">
          {canApprove && (
            <button
              onClick={() => onApprove(story.id)}
              className="flex-1 px-2 py-1.5 text-xs bg-success/15 text-success rounded-lg hover:bg-success/25 transition-colors font-medium"
            >
              {t('action.approve')}
            </button>
          )}
          {canApprove && (
            <button
              onClick={() => onReject(story.id)}
              className="px-2 py-1.5 text-xs bg-error/15 text-error rounded-lg hover:bg-error/25 transition-colors"
            >
              {t('action.reject')}
            </button>
          )}
          <button
            onClick={() => setEditing(true)}
            className="px-2 py-1.5 text-xs bg-background text-dim rounded-lg hover:text-foreground transition-colors"
          >
            {t('action.edit')}
          </button>
          <button
            onClick={() => onSwapTemplate(story.id)}
            className="px-2 py-1.5 text-xs bg-background text-dim rounded-lg hover:text-foreground transition-colors"
          >
            {t('action.swap')}
          </button>
          <button
            onClick={() => onUploadPhoto(story.id)}
            className="px-2 py-1.5 text-xs bg-background text-dim rounded-lg hover:text-foreground transition-colors"
          >
            📷
          </button>
        </div>
      )}
    </div>
  );
}
