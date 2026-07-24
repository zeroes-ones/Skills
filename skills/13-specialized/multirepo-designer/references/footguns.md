# Footguns: Multirepo-Specific Pitfalls

These are the sharp edges that catch even experienced teams. Each represents a situation where the multirepo approach creates risks that don't exist (or are smaller) in a monorepo.

## 1. The Phantom Dependency
**Problem:** Repo A imports `@org/toolkit@^3.0.0`. A transitive dependency of toolkit breaks A's build. A never declared that transitive dep, so the breakage is mysterious.
**Fix:** Toolkit should re-export only its public API. Use `depcheck` in CI to flag undeclared usage of transitive deps.

## 2. The Rolling Breaking Change
**Problem:** `contracts` releases a breaking change v4.0.0. `toolkit` updates. `auth` updates toolkit. `gateway` updates auth. Six weeks later, the last downstream repo finally compiles again.
**Fix:** Ship codemods with breaking changes. Automate the upgrade PRs. Never let a breaking change cascade through N layers manually.

## 3. The CI Config Explosion
**Problem:** 50 repos, each with its own `.github/workflows/ci.yml`. A critical security fix needs to be applied to all 50. It takes 2 weeks.
**Fix:** Reusable workflows. One canonical CI definition. All repos reference it by major version.

## 4. The Silent Schema Drift
**Problem:** `auth` changes a field from `email` to `emailAddress` in its API response. `gateway` doesn't notice because it uses `any` types. Prod breaks 3 weeks later when a new field is added that conflicts.
**Fix:** Codegen clients from contracts. Validate responses in CI against the contract. Never use untyped access to API responses.

## 5. The Bootstrap Tax
**Problem:** New hire clones 8 repos to set up their dev environment. Each has different setup steps. Day 1 is wasted on environment hell.
**Fix:** Provide a `dev-env` repo with a single script that clones and sets up all repos. Or use a dev container.

## 6. The Forgotten Repo
**Problem:** A critical vulnerability (Log4Shell-scale) is announced. Security team scans all known repos. The "forgotten" repo from 2019 that nobody touches still runs in production. It's not on the scan list.
**Fix:** Maintain a machine-readable inventory of ALL production repos. Automate dependency scanning. Archive repos that aren't deployed.

## 7. The Circular Dependency Trap
**Problem:** `auth` depends on `toolkit` for logging. `toolkit` depends on `auth` for user context in logs. Neither can be built without the other.
**Fix:** Extract the shared interface into `contracts`. Both depend on contracts. Neither depends on the other directly.

## 8. The Sync-Release Lockstep
**Problem:** To ship Feature X, you need PRs in repos A, B, C, D merged in exact order. Merge conflicts or CI failures in repo C block everyone.
**Fix:** Feature flags. Ship each repo independently, gated behind a flag. Turn on the flag when all repos are ready. Never orchestrate deployments by merge order.

## 9. The Version Hell Spiral
**Problem:** `@org/toolkit` is at v12.7.3 because the team releases a major version for every tiny breaking change instead of deprecating first.
**Fix:** Deprecate before removing. Major versions should happen 1-2 times per year, not per sprint. If you're releasing majors monthly, your API surface is too unstable.
