# Local setup

## Prerequisites

- Node >= 20.9 and pnpm 9 (`npm i -g pnpm@9`)
- Python >= 3.10
- A Postgres database (local Docker or a free Supabase project)

## Steps

```bash
pnpm install
./apps/api/scripts/bootstrap.sh
cp .env.example .env
pnpm dev
```

- Web: http://localhost:3000 (the header shows live API health)
- API: http://localhost:8000 — OpenAPI docs at `/docs`, health at `/api/v1/health`

## Keys (all free)

| Variable | Where to get it |
| --- | --- |
| `SERPER_API_KEY` | serper.dev — 2,500 free searches |
| `GSC_ACCESS_TOKEN`, `GSC_SITE_URL` | Google Search Console API for a verified property |
| `GROQ_API_KEY` | console.groq.com |
| `GOOGLE_API_KEY` | aistudio.google.com |

`OPENAI_API_KEY` and `PERPLEXITY_API_KEY` are optional; without them the citation monitor reports
those engines as unavailable instead of failing the run.
