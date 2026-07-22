# Code Review Summary — Sprints 4–6

**Review Period**: June 1 – July 18, 2026 (3 sprints, 2-week cadence)  
**Total PRs Reviewed**: 47 (18 in Sprint 4, 15 in Sprint 5, 14 in Sprint 6)  
**Reviewers**: 4 senior engineers rotating primary/secondary roles

## Finding Categories

**Architecture Concerns (3)**
1. **Circular dependency in catalog service** (PR #142): `CatalogService` importing `TemplateService` and vice versa. Resolved by extracting a shared `ServiceIndexer` interface into `packages/shared-interfaces`. Both services now depend on the interface, not each other.
2. **Missing interface for plugin SDK** (PR #187): The plugin loader called concrete implementations directly, preventing mocking in tests. Introduced `PluginExecutor` interface with `Execute(ctx, params) (Result, error)` — 17 existing plugins refactored to implement it.
3. **N+1 database query in template execution loop** (PR #163): Service owner lookup executed inside a `for` loop over 50+ services. Replaced with a single batch query using `WHERE service_id = ANY($1)` with a PostgreSQL array parameter.

**Performance Issues (12)**
- 4 N+1 query patterns across catalog, plugin, and template services — all resolved by introducing eager loading with dataloader-style batching.
- 3 missing database indexes (template_executions.status, plugin_configs.org_id, service_versions.deployed_at) — indexes added with `CREATE INDEX CONCURRENTLY` to avoid locking.
- 2 unbundled dependencies (monaco-editor at 2.1MB and moment.js at 68KB) — replaced monaco-editor with @codemirror/lang-json (187KB) and moment.js with date-fns (tree-shakeable, 12KB used).
- 3 React re-render issues from missing `useMemo` on filter computations — resolved, verified with React DevTools Profiler.

**Security Issues (8)**
- 3 unvalidated input fields (service name allowing HTML injection, template parameter accepting arbitrary JSON, plugin config merging without schema validation) — added zod schemas on both client and server.
- 2 missing CSRF tokens on state-changing API routes — enabled NextAuth.js built-in CSRF protection.
- 1 debug endpoint (`/api/debug/pprof`) accessible in production — gated behind `ENV=development` check.
- 2 secrets in repository history (AWS access keys, expired and rotated within 1 hour of discovery) — removed via `git filter-branch`, added pre-commit hook via `detect-secrets`.

**Resolution**: All 23 findings were resolved before merge. Zero blockers in the review period. Average time-to-resolution: 1.8 days (down from 2.4 days in Sprints 1–3).
