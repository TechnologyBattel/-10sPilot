# Architecture

```
                +---------------------+
   browser ---> |  apps/web (Next 16) |  Vercel Hobby
                +----------+----------+
                           | HTTP (NEXT_PUBLIC_API_URL)
                           v
                +---------------------+
                | apps/api (FastAPI)  |  Render / Fly free tier
                +----------+----------+
                           |
                           v
                +---------------------+
                | Postgres (Supabase) |
                +---------------------+

shared TypeScript:
  packages/core -> types, zod schemas, constants, errors
  packages/db   -> Drizzle schema + migrations
  packages/ai   -> Groq / Gemini providers
```

## Repository layout

```
apps/web/src
  app/(marketing)      public pages
  app/(dashboard)      authenticated app shell
  app/api/health       Next route handler
  components/ui        primitives
  components/layout    shell components
  hooks/               client hooks
  lib/                 env + API client helpers

apps/api/app
  api/v1/routes        HTTP endpoints
  core                 settings, logging, security
  db                   engine + session
  models               SQLAlchemy models
  schemas              Pydantic models
  services             business logic
  workers              background jobs
```

## Boundaries

- `apps/web` never talks to Postgres directly; it calls the API.
- `packages/core` has no framework dependencies and is safe to import anywhere.
- `packages/db` is the only place that defines database schema.
- `packages/ai` hides provider differences behind the `AiProvider` interface.
