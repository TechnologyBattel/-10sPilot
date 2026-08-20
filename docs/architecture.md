# Architecture

```
                +---------------------------+
   browser ---> |  apps/web (Next.js 16)    |  Vercel Hobby
                +-------------+-------------+
                              | HTTP (NEXT_PUBLIC_API_URL)
                              v
                +---------------------------+
                |  apps/api (FastAPI)       |  Render / Fly free tier
                |  routes -> modules        |
                +------+-------------+------+
                       |             |
        +--------------+             +-----------------+
        v                                              v
+---------------------+                    +------------------------+
| serp_engine (free)  |                    | LLM providers (free)   |
| Serper.dev + GSC    |                    | Groq / Gemini          |
+---------------------+                    +------------------------+
                       |
                       v
             +---------------------+
             | Postgres (Supabase) |  Prisma schema in packages/db
             +---------------------+
```

`serp_engine` is the central data source: keyword research, content briefs and rankings all read
from it. `workflow_engine` is the autonomous agent — it plans a pipeline and executes it through
the MCP tool registry in `app/tools`, so every capability is reachable both over HTTP and as a
tool call.

## API layout

```
apps/api/app/
  api/v1/routes/        rankings, keywords, content, audit, ai-citations, links, workflow, tools
  modules/
    serp_engine/        free_serp.py (Serper + Search Console), service.py
    keyword_engine/     research.py, clustering.py
    content_engine/     prompts.py, service.py  (AEO + GEO optimized drafts)
    audit_engine/       checks.py, service.py   (technical SEO)
    aeo_engine/         optimizer.py            (Answer Engine Optimization)
    geo_engine/         optimizer.py            (Generative Engine Optimization)
    citation_monitor/   engines.py, service.py  (ChatGPT / Perplexity / Gemini)
    link_engine/        service.py              (internal linking)
    workflow_engine/    planner.py, service.py  (autonomous agent)
  tools/                MCP tools + registry
  core/                 config, errors, logging, security
  db/, models/, schemas/, services/
```

Note: the module and tool packages live under `apps/api/app/` so they are importable as
`app.modules.*` and `app.tools.*` — `app` is the Python package root of the service.

## Web layout

```
apps/web/
  app/(app)/            dashboard, projects, keywords, content, audit, rankings, ai-citations, workflow
  app/api/health        Next route handler
  components/ui         primitives (button, card, stat, empty-state, page-header)
  components/layout     sidebar + header
  lib/                  env, api client, nav
```

## Boundaries

- `apps/web` never talks to Postgres directly; it calls the API.
- `packages/core` has no framework dependencies and is safe to import anywhere.
- `packages/db` owns the schema; Prisma models are the source of truth.
- Every engine exposes a service class; routes and MCP tools are thin wrappers over it.
