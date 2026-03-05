'use client';

import { useEffect, useState } from 'react';

export default function TopBar() {
  const [time, setTime] = useState('');

  useEffect(() => {
    const update = () => setTime(new Date().toLocaleTimeString('en-US', { hour12: false }));
    update();
    const iv = setInterval(update, 1000);
    return () => clearInterval(iv);
  }, []);

  return (
    <header className="sticky top-0 z-20 h-12 border-b border-border bg-card/80 backdrop-blur-xl flex items-center justify-between px-6 ml-56">
      <div className="flex items-center gap-3">
        <span className="w-2 h-2 rounded-full bg-success pulse" />
        <span className="text-xs text-dim font-body">Live · Polling every 10s</span>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-xs text-muted font-mono">{time}</span>
        <span className="text-xs text-dim font-body">March 2, 2026</span>
      </div>
    </header>
  );
}
