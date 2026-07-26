## Core Workflow

### Phase 1 (~15 min): Coupling Analysis & Team Topology Mapping
1. Map all teams to their repos. Draw Conway alignment: does each repo have one clear owner?
2. Analyze cross-repo PR frequency over last 6 months: `git log --oneline --all | grep -i "#[0-9]" | sort | uniq -c`
3. Identify hotspots: repos with >30% cross-repo PRs are candidates for merging. Repos with <5% are correctly isolated.
4. Measure shared code surface area: count duplicate function signatures, shared configuration files, copy-pasted CI templates.
5. Calculate the coordination tax: (cross-repo PRs per sprint) x (average minutes per cross-repo PR) x (engineer hourly rate).

### Phase 2 (~20 min): Repo Boundary Design
1. For each bounded context (from system-architect), define: one deployable repo per independently deployable unit.
2. Identify shared code: extract shared types, configs, and utilities into `@org/shared-lib` repos.
3. Define dependency direction: shared libs at the bottom (no upstream deps), domain services in the middle, application repos at the top.
4. Prevent circular dependencies: use dependency-cruiser or madge to validate no cycles across repo boundaries.
5. Document boundaries in an architecture decision record: rationale, coupling metrics, ownership assignment.

### Phase 3 (~25 min): Cross-Repo CI/CD Orchestration
1. For each cross-repo dependency, define the CI trigger: library publish -> Renovate PR; API change -> contract test; config change -> repository_dispatch.
2. Set up shared CI templates: GitHub reusable workflows, GitLab CI templates, or custom CI generators. One canonical pipeline per language.
3. Implement contract testing: Pact for HTTP APIs, OpenAPI diff for REST, gRPC reflection for protobuf, schema compatibility checks for databases.
4. Configure Renovate/Dependabot for cross-repo dependency updates with grouped PRs and auto-merge for patch versions.
5. Add a CI gate: any PR that changes a shared library exported API must trigger downstream CI and get green results BEFORE merge.

### Phase 4 (~20 min): Shared Library Publishing & Versioning
1. Choose versioning: independent semver for all shared libraries. Lockstep only if repos always deploy together.
2. Set up automated publishing: CI publishes to internal registry on merge to main. Version bump via Changesets or conventional commits.
3. Generate changelogs: categorize changes (breaking, feature, fix), link to PRs, notify consuming teams.
4. Enforce API stability: use `exports` field in package.json, TypeScript `isolatedModules`, or Go internal packages to prevent accidental public API exposure.
5. Set up deprecation tooling: runtime deprecation warnings with migration instructions, automated codemods for consumers.

### Phase 5 (~25 min): Breaking Change Rollout
1. Ship new API alongside old as non-breaking minor release.
2. Deprecate old API: @deprecated annotations, runtime warnings, migration guide with before/after examples.
3. Build automated migration: codemod tool (jscodeshift, comby, ast-grep) tested against all consumer repos.
4. Open automated PRs: batch-apply migration, verify CI passes, assign to CODEOWNERS for review.
5. Monitor adoption: dashboard tracking % consumers migrated, escalate laggards to team leads.
6. Remove old API only after 100% migration + 1 release buffer.

### Phase 6 (~20 min): Cross-Repo Testing Strategy
1. Unit tests: each repo tests its own code in isolation. No cross-repo dependencies in unit tests.
2. Contract tests: define explicit contracts between repos. Repo A publishes contracts, Repo B verifies them in CI.
3. Integration tests: spin up dependent services (Docker Compose, Testcontainers) for cross-repo integration testing.
4. End-to-end tests: test the full cross-repo flow in a staging environment. Run on every PR to shared libraries.
5. Test impact analysis: only run integration/e2e tests for repos affected by the change. Use dependency graph to determine affected repos.
