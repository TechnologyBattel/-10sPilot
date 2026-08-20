# Deployment ($0 stack)

| Layer | Service | Free tier notes |
| --- | --- | --- |
| Web | Vercel Hobby | root directory `apps/web`, build `pnpm build`, install `pnpm install` |
| API | Render free web service or Fly.io | uses `apps/api/Dockerfile`; free instances sleep when idle |
| Database | Supabase Postgres | set `DATABASE_URL` (use the pooled connection string) |
| AI | Groq or Google Gemini | both offer free API keys; select with `AI_PROVIDER` |
| CI | GitHub Actions | `.github/workflows/ci.yml` |

## Environment variables

Copy `.env.example`. The web app only needs `NEXT_PUBLIC_*` values; the API needs
`DATABASE_URL`, `API_CORS_ORIGINS` and `API_SECRET_KEY`.
