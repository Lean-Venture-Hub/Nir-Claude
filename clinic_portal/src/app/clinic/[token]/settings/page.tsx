'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useClinic } from '../PortalShell';
import { useT } from '@/lib/i18n';
import type { ClinicPortalSettings } from '@/types';

const DEFAULT_SETTINGS: ClinicPortalSettings = {
  autoApproveRules: { stories: false, reels: false, seo: false },
  toneOfVoice: 'professional',
  notificationPrefs: { email: true, whatsapp: false, weeklyDigest: true },
  brandColors: { primary: '#16a34a', accent: '#e8a849' },
  photoVault: [],
};

export default function SettingsPage() {
  const { clinicId } = useClinic();
  const { t } = useT();
  const [settings, setSettings] = useState<ClinicPortalSettings>(DEFAULT_SETTINGS);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`/api/portal/${clinicId}/settings`)
      .then((r) => r.json())
      .then((data) => { setSettings(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, [clinicId]);

  const save = useCallback(async (updates: Partial<ClinicPortalSettings>) => {
    setSaving(true);
    const merged = { ...settings, ...updates };
    setSettings(merged);
    await fetch(`/api/portal/${clinicId}/settings`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    setSaving(false);
  }, [clinicId, settings]);

  const handlePhotoUpload = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('photo', file);
    const res = await fetch(`/api/portal/${clinicId}/photos`, { method: 'POST', body: formData });
    const data = await res.json();
    if (data.photoUrl) {
      setSettings((prev) => ({
        ...prev,
        photoVault: [...prev.photoVault, data.photoUrl],
      }));
    }
  }, [clinicId]);

  if (loading) {
    return <div className="flex items-center justify-center min-h-[60vh] text-dim text-sm">{t('general.loading')}</div>;
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="font-heading text-xl font-bold">{t('settings.title')}</h1>

      {/* Photo Vault */}
      <section className="bg-card border border-border rounded-2xl p-5 fade-up">
        <h2 className="font-heading text-sm font-semibold mb-3">{t('settings.photoVault')}</h2>
        <div className="grid grid-cols-4 sm:grid-cols-6 gap-2 mb-3">
          {settings.photoVault.map((url, i) => (
            <div key={i} className="aspect-square bg-background rounded-xl border border-border flex items-center justify-center text-xs text-muted overflow-hidden">
              <span>📷 {i + 1}</span>
            </div>
          ))}
          <button
            onClick={() => fileInputRef.current?.click()}
            className="aspect-square bg-background rounded-xl border border-dashed border-border-hover flex items-center justify-center text-dim hover:text-accent hover:border-accent transition-colors"
          >
            <span className="text-xl">+</span>
          </button>
        </div>
        <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={handlePhotoUpload} />
      </section>

      {/* Brand Colors */}
      <section className="bg-card border border-border rounded-2xl p-5 fade-up">
        <h2 className="font-heading text-sm font-semibold mb-3">{t('settings.brandColors')}</h2>
        <div className="flex gap-4">
          <div className="flex items-center gap-2">
            <label className="text-xs text-dim">Primary</label>
            <input
              type="color"
              value={settings.brandColors.primary}
              onChange={(e) => save({ brandColors: { ...settings.brandColors, primary: e.target.value } })}
              className="w-8 h-8 rounded-lg border border-border cursor-pointer"
            />
            <span className="text-xs text-muted">{settings.brandColors.primary}</span>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-xs text-dim">Accent</label>
            <input
              type="color"
              value={settings.brandColors.accent}
              onChange={(e) => save({ brandColors: { ...settings.brandColors, accent: e.target.value } })}
              className="w-8 h-8 rounded-lg border border-border cursor-pointer"
            />
            <span className="text-xs text-muted">{settings.brandColors.accent}</span>
          </div>
        </div>
      </section>

      {/* Tone of Voice */}
      <section className="bg-card border border-border rounded-2xl p-5 fade-up">
        <h2 className="font-heading text-sm font-semibold mb-3">{t('settings.toneOfVoice')}</h2>
        <div className="flex flex-wrap gap-2">
          {['professional', 'friendly', 'casual', 'formal', 'warm'].map((tone) => (
            <button
              key={tone}
              onClick={() => save({ toneOfVoice: tone })}
              className={`px-3 py-1.5 text-xs rounded-lg border transition-colors ${
                settings.toneOfVoice === tone
                  ? 'border-accent text-accent bg-accent/10'
                  : 'border-border text-dim hover:text-foreground hover:border-border-hover'
              }`}
            >
              {tone}
            </button>
          ))}
        </div>
      </section>

      {/* Auto Approve Rules */}
      <section className="bg-card border border-border rounded-2xl p-5 fade-up">
        <h2 className="font-heading text-sm font-semibold mb-3">{t('settings.autoApprove')}</h2>
        <div className="space-y-3">
          {(['stories', 'reels', 'seo'] as const).map((key) => (
            <label key={key} className="flex items-center justify-between">
              <span className="text-sm text-dim capitalize">{key}</span>
              <button
                onClick={() =>
                  save({
                    autoApproveRules: { ...settings.autoApproveRules, [key]: !settings.autoApproveRules[key] },
                  })
                }
                className={`w-10 h-6 rounded-full transition-colors relative ${
                  settings.autoApproveRules[key] ? 'bg-accent' : 'bg-background border border-border'
                }`}
              >
                <span
                  className={`absolute top-0.5 w-5 h-5 rounded-full bg-white transition-all ${
                    settings.autoApproveRules[key] ? 'end-0.5' : 'start-0.5'
                  }`}
                />
              </button>
            </label>
          ))}
        </div>
      </section>

      {/* Notification Preferences */}
      <section className="bg-card border border-border rounded-2xl p-5 fade-up">
        <h2 className="font-heading text-sm font-semibold mb-3">{t('settings.notifications')}</h2>
        <div className="space-y-3">
          {[
            { key: 'email' as const, label: 'Email' },
            { key: 'whatsapp' as const, label: 'WhatsApp' },
            { key: 'weeklyDigest' as const, label: 'Weekly Digest' },
          ].map(({ key, label }) => (
            <label key={key} className="flex items-center justify-between">
              <span className="text-sm text-dim">{label}</span>
              <button
                onClick={() =>
                  save({
                    notificationPrefs: { ...settings.notificationPrefs, [key]: !settings.notificationPrefs[key] },
                  })
                }
                className={`w-10 h-6 rounded-full transition-colors relative ${
                  settings.notificationPrefs[key] ? 'bg-accent' : 'bg-background border border-border'
                }`}
              >
                <span
                  className={`absolute top-0.5 w-5 h-5 rounded-full bg-white transition-all ${
                    settings.notificationPrefs[key] ? 'end-0.5' : 'start-0.5'
                  }`}
                />
              </button>
            </label>
          ))}
        </div>
      </section>

      {saving && (
        <div className="fixed bottom-4 end-4 bg-accent text-background text-xs px-4 py-2 rounded-lg fade-up z-50">
          Saving...
        </div>
      )}
    </div>
  );
}
