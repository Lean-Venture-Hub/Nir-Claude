import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import TopBar from "@/components/TopBar";

export const metadata: Metadata = {
  title: "Mission Control — Content Machine",
  description: "Dashboard for 439 dental clinics content pipeline",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="noise-overlay antialiased">
        <Sidebar />
        <TopBar />
        <main className="ml-56 pt-12 min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
