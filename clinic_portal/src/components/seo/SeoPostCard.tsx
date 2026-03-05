'use client';

import { useState } from 'react';
import { useT } from '@/lib/i18n';
import StatusBadge from '@/components/StatusBadge';
import type { SeoPost } from '@/types';

interface SeoPostCardProps {
  post: SeoPost;
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
  onEdit: (id: string, updates: { editedTitle?: string; editedExcerpt?: string }) => void;
}

export default function SeoPostCard({ post, onApprove, onReject, onEdit }: SeoPostCardProps) {
  const { t } = useT();
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(post.editedTitle ?? post.title);
  const [excerpt, setExcerpt] = useState(post.editedExcerpt ?? post.excerpt ?? '');

  const canApprove = post.status === 'draft' || post.status === 'pending';

  return (
    <div className="bg-card border border-border rounded-2xl p-4 hover:border-border-hover transition-colors fade-up">
      <div className="flex items-center justify-between mb-2">
        <StatusBadge status={post.status} />
        {post.publishDate && <span className="text-xs text-muted">{post.publishDate}</span>}
      </div>

      {editing ? (
        <div className="space-y-2 mb-3">
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent"
            dir="rtl"
          />
          <textarea
            value={excerpt}
            onChange={(e) => setExcerpt(e.target.value)}
            className="w-full bg-background border border-border rounded-lg px-3 py-2 text-xs resize-none focus:outline-none focus:border-accent"
            rows={3}
            dir="rtl"
          />
          <div className="flex gap-2 justify-end">
            <button onClick={() => setEditing(false)} className="px-3 py-1 text-xs text-dim">{t('action.cancel')}</button>
            <button
              onClick={() => {
                onEdit(post.id, { editedTitle: title, editedExcerpt: excerpt });
                setEditing(false);
              }}
              className="px-3 py-1 text-xs bg-accent text-background rounded-lg font-medium"
            >
              {t('action.save')}
            </button>
          </div>
        </div>
      ) : (
        <>
          <h4 className="text-sm font-medium mb-1" dir="rtl">{post.editedTitle ?? post.title}</h4>
          {(post.editedExcerpt ?? post.excerpt) && (
            <p className="text-xs text-dim line-clamp-2 mb-3" dir="rtl">{post.editedExcerpt ?? post.excerpt}</p>
          )}
        </>
      )}

      <div className="flex flex-wrap gap-1.5">
        {canApprove && (
          <button
            onClick={() => onApprove(post.id)}
            className="flex-1 px-3 py-1.5 text-xs bg-success/15 text-success rounded-lg hover:bg-success/25 transition-colors font-medium"
          >
            {t('action.approve')}
          </button>
        )}
        {canApprove && (
          <button
            onClick={() => onReject(post.id)}
            className="px-3 py-1.5 text-xs bg-error/15 text-error rounded-lg hover:bg-error/25 transition-colors"
          >
            {t('action.reject')}
          </button>
        )}
        {post.status !== 'published' && !editing && (
          <button
            onClick={() => setEditing(true)}
            className="px-3 py-1.5 text-xs bg-background text-dim rounded-lg hover:text-foreground transition-colors"
          >
            {t('action.edit')}
          </button>
        )}
      </div>
    </div>
  );
}
