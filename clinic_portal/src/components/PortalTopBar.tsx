'use client';

import LangToggle from './LangToggle';
import HebrewText from './HebrewText';
import { useT } from '@/lib/i18n';

interface PortalTopBarProps {
  clinicName: string;
}

export default function PortalTopBar({ clinicName }: PortalTopBarProps) {
  const { lang } = useT();

  return (
    <header className="sticky top-0 z-30 h-12 bg-background/80 backdrop-blur-md border-b border-border flex items-center justify-between px-4 md:px-6">
      <div className="flex items-center gap-3">
        <span className="md:hidden font-heading text-accent font-bold text-sm">Portal</span>
        {lang === 'he' ? (
          <HebrewText className="text-sm font-medium">{clinicName}</HebrewText>
        ) : (
          <span className="text-sm font-medium text-dim">{clinicName}</span>
        )}
      </div>
      <div className="flex items-center gap-3">
        <LangToggle />
      </div>
    </header>
  );
}
