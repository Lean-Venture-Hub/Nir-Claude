'use client';

import useSWR from 'swr';
import type { ClinicDetail, AiVisibilityData } from '@/types';

const fetcher = (url: string) => fetch(url).then((r) => {
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json();
});

export function usePolling<T>(endpoint: string | null, interval = 15000) {
  const { data, error, isLoading, mutate } = useSWR<T>(endpoint, fetcher, {
    refreshInterval: interval,
    revalidateOnFocus: true,
  });
  return { data, error, isLoading, refresh: mutate };
}

export function useClinicData(clinicId: number | null) {
  return usePolling<ClinicDetail>(
    clinicId ? `/api/portal/${clinicId}` : null,
    15000
  );
}

export function useAiVisibility(clinicId: number | null) {
  return usePolling<AiVisibilityData>(
    clinicId ? `/api/portal/${clinicId}/ai-visibility` : null,
    60000
  );
}

export function useAuth(token: string) {
  return usePolling<{ clinicId: number }>(
    `/api/auth/${token}`,
    0 // no polling for auth
  );
}
