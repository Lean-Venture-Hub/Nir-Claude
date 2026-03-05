import { resolveToken } from '@/lib/auth';
import { getClinicDetail } from '@/lib/data';
import PortalShell from './PortalShell';

interface LayoutProps {
  children: React.ReactNode;
  params: Promise<{ token: string }>;
}

export default async function ClinicLayout({ children, params }: LayoutProps) {
  const { token } = await params;
  const clinicId = resolveToken(token);

  if (!clinicId) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center fade-up">
          <div className="text-6xl mb-4">🔗</div>
          <h1 className="font-heading text-2xl font-bold text-accent mb-2">קישור לא תקין</h1>
          <p className="text-dim text-sm">Invalid link. Please use the link sent to your email.</p>
        </div>
      </div>
    );
  }

  const clinic = getClinicDetail(clinicId);
  if (!clinic) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center fade-up">
          <div className="text-6xl mb-4">❌</div>
          <h1 className="font-heading text-2xl font-bold text-error mb-2">שגיאה</h1>
          <p className="text-dim text-sm">Clinic data not found.</p>
        </div>
      </div>
    );
  }

  return (
    <PortalShell clinicId={clinicId} clinicName={clinic.name} token={token}>
      {children}
    </PortalShell>
  );
}
