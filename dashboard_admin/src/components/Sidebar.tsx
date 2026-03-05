'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const NAV_ITEMS = [
  { href: '/', label: 'Command Center', icon: '◆' },
  { href: '/clinics', label: 'Clinic Roster', icon: '◫' },
  { href: '/calendar', label: 'Calendar', icon: '▦' },
  { href: '/templates', label: 'Templates', icon: '◧' },
  { href: '/budget', label: 'Budget', icon: '◈' },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-screen w-56 border-r border-border bg-card flex flex-col z-30">
      <div className="p-5 border-b border-border">
        <h1 className="font-heading text-xl font-bold tracking-tight text-accent">
          Mission Control
        </h1>
        <p className="text-xs text-dim mt-1 font-body">Content Machine · 439 Clinics</p>
      </div>

      <nav className="flex-1 py-3">
        {NAV_ITEMS.map((item) => {
          const isActive =
            item.href === '/'
              ? pathname === '/'
              : pathname.startsWith(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-5 py-2.5 text-sm font-body transition-colors ${
                isActive
                  ? 'text-accent bg-[var(--accent-glow)] border-r-2 border-accent'
                  : 'text-dim hover:text-foreground hover:bg-card-hover'
              }`}
            >
              <span className="text-base">{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-2 text-xs text-muted">
          <span className="w-2 h-2 rounded-full bg-success pulse" />
          Agent connected
        </div>
      </div>
    </aside>
  );
}
