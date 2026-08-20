# Local setup

## Prerequisites

- Node >= 20.9 and pnpm 9 (`npm i -g pnpm@9`)
- Python >= 3.10
- A Postgres database (local Docker or a free Supabase project)

## Steps

```bash
pnpm install
./apps/api/scripts/bootstrap.sh
cp .env.example .env    # fill in DATABASE_URL and an AI key
pnpm dev
```

- Web: http://localhost:3000
- API: http://localhost:8000 (OpenAPI docs at `/docs`)

## Database

```bash
pnpm --filter @10spilot/db db:generate
pnpm --filter @10spilot/db db:migrate
```
