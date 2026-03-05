import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Clinic Portal — Content Dashboard',
  description: 'Manage your clinic content pipeline',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="he" dir="rtl">
      <body className="noise-overlay antialiased">
        {children}
      </body>
    </html>
  );
}
