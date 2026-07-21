# Monorepo Migration

## Current State → Target State

Orchestra currently operates 7 separate GitHub repositories: `orchestra-web` (Next.js frontend), `orchestra-api` (Go API gateway), `orchestra-catalog-service`, `orchestra-template-service`, `orchestra-plugin-service`, `orchestra-docs` (Docusaurus), and `orc-cli`. The migration consolidates these into a single `orchestra-platform` monorepo using Turborepo.

## Repository Structure

```
orchestra-platform/
├── apps/
│   ├── web/          # Next.js 14 frontend + BFF
│   ├── api/          # Go API gateway
│   └── docs/         # Docusaurus documentation site
├── packages/
│   ├── ui/           # Shared React component library
│   ├── config/       # Shared configuration (ESLint, Prettier, Tailwind, TypeScript)
│   ├── tsconfig/     # Base TypeScript configurations
│   └── eslint-config/# Shared ESLint configuration
├── tools/
│   └── orc-cli/      # Developer CLI (Go)
├── turbo.json        # Turborepo pipeline configuration
└── pnpm-workspace.yaml
```

## Turborepo Configuration

Pipeline defined in `turbo.json`:

- `build`: Depends on `^build` (upstream packages). Caches output in `.turbo/`. Go services use Docker layer caching for dependencies.
- `test`: Depends on `build`. Runs in parallel where possible. Vitest for frontend, `go test` for backend.
- `lint`: No dependencies. Runs ESLint, golangci-lint, and Vale in parallel.
- `deploy`: Depends on `build` and `test`. Only runs on `main` branch.

## Remote Caching

Turborepo Remote Cache configured with Vercel (included in Pro plan). Cache metrics over the first 3 weeks: 73% hit rate, average CI time reduced from 4.2 minutes to 1.1 minutes (74% improvement). The `web` app benefits most — shared `ui` and `config` packages are rebuilt only when they change, not when every app builds. Cache misses typically caused by dependency updates (new `node_modules`) or changes to `turbo.json` itself.

## Dependency Graph

```
web ────────────► ui
web ────────────► config
api ────────────► config
docs ───────────► ui
docs ───────────► config
orc-cli (no internal dependencies)
```

Affected-based CI: a PR changing only `apps/docs/` builds and tests `docs`, `ui`, and `config` — skipping `web`, `api`, and `orc-cli`. A PR changing `packages/config/` rebuilds everything. This is managed by Turborepo's `--filter=[...since=origin/main]` flag in CI.

## Migration Approach — Incremental (7 Weeks)

One repository per week, preserving full git history:

- **Week 1**: `orchestra-docs` → `apps/docs/`. Lowest risk, no shared dependencies. Validates the Turborepo setup.
- **Week 2**: `packages/ui`, `packages/config`, `packages/tsconfig`, `packages/eslint-config`. Extracted as new packages from shared code already in `orchestra-web`.
- **Week 3**: `orchestra-web` → `apps/web/`. Integrates with shared packages. Tests: all 247 unit tests must pass, E2E Playwright suite unchanged.
- **Week 4**: `orchestra-api` → `apps/api/`. Go module path updated from `github.com/orchestra-platform/api` to `github.com/orchestra-platform/orchestra-platform/apps/api`.
- **Week 5**: `orchestra-catalog-service` → `apps/api/internal/catalog/`. Merged into the API gateway as an internal package (simplifies deployment — one binary instead of separate services).
- **Week 6**: `orchestra-template-service` and `orchestra-plugin-service` → added to `apps/api/internal/`.
- **Week 7**: `orc-cli` → `tools/orc-cli/`. Homebrew formula updated to point to the new repo.

Each migration uses `git subtree add --prefix=apps/web https://github.com/orchestra-platform/orchestra-web main` to preserve the full commit history. After migration, the original repo is archived (read-only, with a note pointing to the monorepo). Rollback: if a week's migration fails, revert the monorepo commit and continue operating from the standalone repo while debugging.
