const rawBaseUrl = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
const BASE_URL = rawBaseUrl.replace(/\/+$/, '');

export const env = {
  apiUrl: BASE_URL,
  appUrl: process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000',
} as const;
