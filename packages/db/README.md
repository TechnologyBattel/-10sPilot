# @10spilot/db

Prisma schema (`schema.prisma`) and client for the 10sPilot Postgres database.

Models: `Project`, `Keyword`, `KeywordCluster`, `Content`, `Audit`, `Ranking`, `AiCitation`,
`WorkflowRun`.

```bash
pnpm --filter @10spilot/db db:generate   # generate the Prisma client
pnpm --filter @10spilot/db db:migrate    # create + apply a migration against $DATABASE_URL
pnpm --filter @10spilot/db db:seed       # demo project + keyword
```

Use the pooled Supabase connection string for `DATABASE_URL` and the direct one for
`DIRECT_DATABASE_URL` (Prisma migrations need a non-pooled connection).
