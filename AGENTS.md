# Agent notes

- Package manager: **pnpm** (workspaces + Turborepo). Node >= 20.9.
- The Python API lives in `apps/api` and uses a local `.venv` created by `apps/api/scripts/bootstrap.sh`.
  Its `package.json` scripts are thin wrappers so Turbo can orchestrate them.
- Shared TypeScript packages export source directly (`src/index.ts`); `apps/web` lists them in
  `transpilePackages`.
- Before committing: `pnpm lint && pnpm typecheck && pnpm test`.
