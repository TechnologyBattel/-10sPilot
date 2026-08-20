# 2. Turborepo with pnpm workspaces

- Status: accepted

## Context

The repo hosts a Next.js app, a FastAPI service and three shared TypeScript packages, and must run
on free-tier infrastructure.

## Decision

Use pnpm workspaces for dependency management and Turborepo for task orchestration and caching.
The Python service is wrapped in thin `package.json` scripts so `turbo run` drives both stacks.

## Consequences

One command (`pnpm dev`, `pnpm build`, ...) covers both languages; the Python venv is managed by
`apps/api/scripts/bootstrap.sh` rather than pnpm.
