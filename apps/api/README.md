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
  api/v1/routes/   HTTP endpoints
  core/            config, logging, security
  db/              engine + session
  models/          SQLAlchemy models
  schemas/         Pydantic request/response models
  services/        business logic
  workers/         background jobs
tests/
```
