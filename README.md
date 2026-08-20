# 10sPilot

Autonomous SEO / AEO / GEO copilot, built entirely on a **$0 stack**: Vercel Hobby (web),
Render or Fly free tier (API), Supabase free Postgres, Serper.dev + Google Search Console for
ranking data, and Groq / Gemini free tiers for generation.

## Structure

```
apps/
  web/                Next.js 16 (App Router, Turbopack, Tailwind v4)
    app/(app)/        dashboard, projects, keywords, content, audit, rankings, ai-citations, workflow
  api/                FastAPI (Python 3.10+)
    app/modules/      serp_engine, keyword_engine, content_engine, audit_engine,
                      aeo_engine, geo_engine, citation_monitor, link_engine, workflow_engine
    app/tools/        MCP tools (get_rankings, audit_page, generate_content, ...)
packages/
  core/               shared types, zod schemas, constants, errors
  db/                 Prisma schema (schema.prisma) + client
  ai/                 TypeScript AI provider clients (Groq, Gemini)
docs/                 architecture, setup, deployment, engines, roadmap
```

## Quick start

```bash
pnpm install
./apps/api/scripts/bootstrap.sh
cp .env.example .env

pnpm dev            # web on :3000, api on :8000 (docs at /docs)
```

## Common tasks

| Command | Description |
| --- | --- |
| `pnpm build` | Build every workspace |
| `pnpm lint` | eslint (web), ruff (api), prisma format check (db) |
| `pnpm typecheck` | `tsc --noEmit` + `mypy` |
| `pnpm test` | pytest suite for the engines and tools |
| `pnpm --filter @10spilot/db db:migrate` | Create and apply a Prisma migration |

See [docs/](./docs) for the engine catalogue and deployment details.
