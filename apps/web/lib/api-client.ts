import { env } from '@/lib/env';

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function apiFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${env.apiUrl}${path}`, {
    ...init,
    headers: {
      'content-type': 'application/json',
      ...init?.headers,
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new ApiError(
      `Request to ${path} failed`,
      response.status,
    );
  }

  return (await response.json()) as T;
}

export type HealthResponse = {
  status: string;
  service?: string;
  version?: string;
};

export function getApiHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>('/health');
}

export type AEOResult = {
  brand: string;
  query: string;
  mentioned: boolean;
  position: number | null;
  context: string | null;
  provider: string;
};

export function getAEOCheck(
  brand: string,
  query: string,
  providers: string[] = ['groq'],
): Promise<AEOResult[]> {
  return apiFetch<AEOResult[]>('/api/v1/aeo/check', {
    method: 'POST',
    body: JSON.stringify({
      brand,
      query,
      providers,
    }),
  });
}

export type AuditIssue = {
  check: string;
  severity: string;
  message: string;
};

export type AuditReport = {
  url: string;
  status_code: number;
  score: number;
  issues: AuditIssue[];
  title: string | null;
  meta_description: string | null;
  word_count: number;
};

export function runAudit(url: string): Promise<AuditReport> {
  return apiFetch<AuditReport>('/api/v1/audit', {
    method: 'POST',
    body: JSON.stringify({ url }),
  });
}
