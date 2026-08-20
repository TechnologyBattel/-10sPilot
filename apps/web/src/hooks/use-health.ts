'use client';

import { useEffect, useState } from 'react';

import { apiFetch } from '@/lib/api-client';

type Health = { status: string; service: string; version: string };

export function useHealth() {
  const [health, setHealth] = useState<Health | null>(null);

  useEffect(() => {
    let active = true;
    apiFetch<Health>('/api/v1/health')
      .then((data) => {
        if (active) setHealth(data);
      })
      .catch(() => {
        if (active) setHealth(null);
      });
    return () => {
      active = false;
    };
  }, []);

  return health;
}
