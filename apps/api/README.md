# @10spilot/api

FastAPI backend for 10sPilot.

```bash
./scripts/bootstrap.sh                 # create .venv and install deps
pnpm --filter @10spilot/api dev        # http://localhost:8000 (docs at /docs)
pnpm --filter @10spilot/api test
```

Layout:

```
app/
  api/v1/routes/   HTTP endpoints (rankings, keywords, content, audit, ai-citations, links, workflow, tools)
  modules/         the nine engines (see ../../docs/engines.md)
  tools/           MCP tools + registry
  core/            config, errors, logging, security
  db/              engine + session
  models/          SQLAlchemy models
  schemas/         shared Pydantic models
  services/        cross-engine services (LLM client)
  workers/         background jobs
tests/
```
