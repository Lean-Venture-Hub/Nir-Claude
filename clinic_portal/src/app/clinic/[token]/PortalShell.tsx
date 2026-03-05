'use client';

import { createContext, useContext } from 'react';
import { LangProvider } from '@/lib/i18n';
import PortalNav from '@/components/PortalNav';
import PortalTopBar from '@/components/PortalTopBar';

interface ClinicContext {
  clinicId: number;
  clinicName: string;
  token: string;
}

const ClinicCtx = createContext<ClinicContext>({ clinicId: 0, clinicName: '', token: '' });
export function useClinic() { return useContext(ClinicCtx); }

interface PortalShellProps {
  clinicId: number;
  clinicName: string;
  token: string;
  children: React.ReactNode;
}

export default function PortalShell({ clinicId, clinicName, token, children }: PortalShellProps) {
  const basePath = `/clinic/${token}`;

  return (
    <ClinicCtx.Provider value={{ clinicId, clinicName, token }}>
      <LangProvider>
        <div className="min-h-screen">
          <PortalNav basePath={basePath} />
          <div className="md:ms-56">
            <PortalTopBar clinicName={clinicName} />
            <main className="p-4 md:p-6 pb-20 md:pb-6">
              {children}
            </main>
          </div>
        </div>
      </LangProvider>
    </ClinicCtx.Provider>
  );
}
