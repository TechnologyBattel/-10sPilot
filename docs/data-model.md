# Data model

Prisma schema: `packages/db/schema.prisma`.

| Model | Purpose |
| --- | --- |
| `Project` | One domain being optimized; owns everything else |
| `Keyword` | Tracked term with intent, difficulty and opportunity |
| `KeywordCluster` | Topic group of keywords, optionally a pillar topic |
| `Content` | Brief/draft with AEO and GEO scores and publication status |
| `Audit` | Technical audit snapshot for a URL (score + issue list) |
| `Ranking` | Position, clicks and impressions for a keyword at a point in time |
| `AiCitation` | Whether an answer engine cited us for a prompt |
| `WorkflowRun` | Autonomous agent run with per-step results |

Enums: `SearchIntent`, `ContentStatus`, `WorkflowStatus`, `AiEngine`.

```bash
pnpm --filter @10spilot/db db:generate
pnpm --filter @10spilot/db db:migrate
```

Set `DATABASE_URL` to the pooled Supabase connection string and `DIRECT_DATABASE_URL` to the
direct one (Prisma migrations cannot run through the pooler).
