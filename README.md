# 10sPilot

Turborepo monorepo for 10sPilot, built entirely on a **$0 stack**: Vercel Hobby (web),
Render/Fly free tier or Docker (API), Supabase free Postgres (database), and free-tier LLM
providers (Groq / Google Gemini).

## Structure

```
apps/
  web/        Next.js 16 (App Router, Turbopack, Tailwind v4)
  api/        FastAPI (Python 3.10+, SQLAlchemy, Pydantic v2)
packages/
  core/       shared types, zod schemas, constants, errors
  db/         Drizzle ORM schema + migrations (Postgres)
  ai/         AI provider clients (Groq, Gemini)
docs/         architecture, setup, deployment, roadmap
```

## Quick start

```bash
pnpm install                       # Node workspaces
./apps/api/scripts/bootstrap.sh    # Python venv for the API
cp .env.example .env

pnpm dev                           # web on :3000, api on :8000
```

## Common tasks

| Command | Description |
| --- | --- |
| `pnpm build` | Build every workspace |
| `pnpm lint` | Lint web (eslint) and api (ruff) |
| `pnpm typecheck` | `tsc --noEmit` + `mypy` |
| `pnpm test` | Run workspace tests (pytest) |
| `pnpm --filter @10spilot/db db:generate` | Generate SQL migrations from the Drizzle schema |

See [docs/](./docs) for architecture and deployment details.
