---
name: testing-10spilot-local
description: How to run and end-to-end test the 10sPilot monorepo (Next.js web on :3000 + FastAPI on :8000) locally in a browser.
---

# Running 10sPilot locally for E2E testing

## Setup
- `export PATH=$HOME/.local/bin:$PATH` (pnpm lives there).
- `pnpm install` from the repo root, then `./apps/api/scripts/bootstrap.sh` (creates `apps/api/.venv`).
- `cp .env.example .env` if `.env` is missing. `NEXT_PUBLIC_API_URL` defaults to `http://localhost:8000`
  in `apps/web/lib/env.ts`, so the web app works even without an `.env`.
- Start both apps with `pnpm dev` from the repo root (turbo: Next 16 turbopack on :3000, uvicorn on :8000).
  Redirect to a log file and poll it; turbo's dev task never exits.
- To restart only the API: `cd apps/api && ./.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000`.

## No external API keys
Serper / Groq / OpenAI / Perplexity keys are typically absent. Engines that need them report missing
credentials — that is expected, not a failure. All dashboard pages are static shells with empty states,
so don't expect live data anywhere.

## Key smoke checks
- `GET /health` and `GET /api/v1/health` → `{"status":"ok","service":"10sPilot API","version":"0.1.0"}`.
- `GET /docs` → Swagger UI; `GET /api/v1/tools` → JSON array of the MCP tool registry.
- Web: `/` landing → "Open dashboard" button → `/dashboard`. Sidebar has 8 routes:
  dashboard, projects, keywords, content, audit, rankings, ai-citations, workflow.

## Proving web→API wiring (the useful assertion)
`apps/web/components/api-status.tsx` renders a pill with `data-testid="api-status"` in the dashboard
header. It reads `API ok · v0.1.0` (green dot) on success, `API offline` (red) on fetch failure, and
`Checking API…` (yellow) while pending. To prove it's actually live rather than hardcoded, kill the
uvicorn process (`pkill -f "uvicorn app.main:app"`), hard-reload the dashboard and confirm the pill
flips to red "API offline", then restart the API and confirm it returns to green.

## Devin Secrets Needed
None for the golden path. `SERPER_API_KEY`, `GROQ_API_KEY`, `OPENAI_API_KEY`, `PERPLEXITY_API_KEY`
would be required only to exercise the live SEO/AEO engines.
