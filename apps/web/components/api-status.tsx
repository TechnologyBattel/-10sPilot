'use client';

import { useEffect, useState } from 'react';

import { getApiHealth, type HealthResponse } from '@/lib/api-client';

export function ApiStatus() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let active = true;
    getApiHealth()
      .then((data) => active && setHealth(data))
      .catch(() => active && setFailed(true));
    return () => {
      active = false;
    };
  }, []);

  const label = health ? `API ${health.status} · v${health.version}` : failed ? 'API offline' : 'Checking API…';
  const dot = health ? 'bg-green-500' : failed ? 'bg-red-500' : 'bg-yellow-500';

  return (
    <span
      data-testid="api-status"
      className="inline-flex items-center gap-2 rounded-full border border-black/10 px-3 py-1 text-xs dark:border-white/20"
    >
      <span className={`size-2 rounded-full ${dot}`} />
      {label}
    </span>
  );
}
