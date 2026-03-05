'use client';

import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export function usePolling<T>(endpoint: string, interval = 10000) {
  const { data, error, isLoading, mutate } = useSWR<T>(endpoint, fetcher, {
    refreshInterval: interval,
    revalidateOnFocus: true,
  });
  return { data, error, isLoading, refresh: mutate };
}

export function useSystemStatus() {
  return usePolling('/api/status', 10000);
}

export function useClinicIndex() {
  return usePolling('/api/clinics', 30000);
}

export function useClinicDetail(id: number) {
  return usePolling(`/api/clinics/${id}`, 15000);
}

export function useCalendar() {
  return usePolling('/api/calendar', 30000);
}

export function useTemplates() {
  return usePolling('/api/templates', 30000);
}

export function useBudget() {
  return usePolling('/api/budget', 30000);
}
