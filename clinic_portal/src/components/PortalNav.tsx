'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useT } from '@/lib/i18n';

const navItems = [
  { key: 'nav.home' as const, path: '', icon: '◆' },
  { key: 'nav.stories' as const, path: '/stories', icon: '◧' },
  { key: 'nav.reels' as const, path: '/reels', icon: '▶' },
  { key: 'nav.seo' as const, path: '/seo', icon: '◈' },
  { key: 'nav.calendar' as const, path: '/calendar', icon: '▦' },
  { key: 'nav.settings' as const, path: '/settings', icon: '⚙' },
];

export default function PortalNav({ basePath }: { basePath: string }) {
  const pathname = usePathname();
  const { t } = useT();

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden md:flex fixed top-0 start-0 h-screen w-56 bg-card border-e border-border flex-col z-40">
        <div className="p-5 border-b border-border">
          <div className="font-heading text-lg font-bold text-accent">Clinic Portal</div>
        </div>
        <nav className="flex-1 py-4">
          {navItems.map((item) => {
            const href = `${basePath}${item.path}`;
            const isActive = item.path === ''
              ? pathname === basePath
              : pathname?.startsWith(href);
            return (
              <Link
                key={item.key}
                href={href}
                className={`flex items-center gap-3 px-5 py-2.5 text-sm transition-colors ${
                  isActive
                    ? 'text-accent bg-[var(--accent-glow)] border-e-2 border-accent'
                    : 'text-dim hover:text-foreground hover:bg-card-hover'
                }`}
              >
                <span className="text-base w-5 text-center">{item.icon}</span>
                <span>{t(item.key)}</span>
              </Link>
            );
          })}
        </nav>
        <div className="p-4 border-t border-border">
          <div className="flex items-center gap-2 text-xs text-dim">
            <span className="w-2 h-2 rounded-full bg-success pulse" />
            <span>AI Assistant Active</span>
          </div>
        </div>
      </aside>

      {/* Mobile bottom tab bar */}
      <nav className="md:hidden fixed bottom-0 inset-x-0 bg-card border-t border-border z-40 flex">
        {navItems.map((item) => {
          const href = `${basePath}${item.path}`;
          const isActive = item.path === ''
            ? pathname === basePath
            : pathname?.startsWith(href);
          return (
            <Link
              key={item.key}
              href={href}
              className={`flex-1 flex flex-col items-center gap-0.5 py-2 text-xs transition-colors ${
                isActive ? 'text-accent' : 'text-dim'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span>{t(item.key)}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
}
