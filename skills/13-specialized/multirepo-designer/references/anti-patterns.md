# Anti-Patterns Catalog: Multirepo Edition

Common pitfalls in multirepo design that degrade velocity, increase cognitive load, and create operational risk. Each anti-pattern includes the symptom, root cause, and remediation.

## 1. The Distributed Monolith
**Symptom:** Every deployment requires coordinating changes across 5+ repos in a specific order.
**Root Cause:** Services share databases, synchronous RPC chains, or deployment ordering.
**Fix:** Loosen coupling via async messaging, event-driven architectures, and independent data ownership.

## 2. The Orphan Repo
**Symptom:** A repo hasn't had a commit in 18 months. No one volunteers to own it.
**Root Cause:** Repo was created for a project that ended, or the owning team was reorged.
**Fix:** Archive immediately. If needed later, fork from archive. Run quarterly repo health audits.

## 3. The Frankenrepo
**Symptom:** A single repo contains an API server, a CLI tool, a web frontend, and database migrations — none related.
**Root Cause:** "Let's just put it here for now" repeated 50 times.
**Fix:** Split by bounded context. Each repo should do one thing well.

## 4. Configuration Drift
**Symptom:** 12 repos use `eslint-config`, but 4 different versions. CI behaves differently in each.
**Root Cause:** No shared CI templates or automated version bumping.
**Fix:** Publish `@org/ci-templates` and `@org/eslint-config`. Use Renovate to keep consumers updated.

## 5. The Fork-and-Forget
**Symptom:** Team forks `toolkit`, patches it, never upstreams. Now maintains a private fork forever.
**Root Cause:** Upstream review is too slow, or team lacks confidence to contribute.
**Fix:** InnerSource model with clear contribution guidelines. SLAs for PR reviews from platform teams.

## 6. The Mega-Private Package
**Symptom:** `@org/common-utils` has 87 dependencies and every team imports it — but nobody knows everything it does.
**Root Cause:** Shared library grew organically without governance.
**Fix:** Split into scoped packages: `@org/http-utils`, `@org/date-utils`, `@org/testing-utils`. Deprecate mega-package.

## 7. Version Pinning Paralysis
**Symptom:** Teams pin to exact versions of internal packages, never upgrade, creating dependency drift.
**Root Cause:** Fear of breaking changes; no automated migration tooling.
**Fix:** Use `^` ranges for minor/patch. Invest in codemods + automated PRs for major upgrades. Trust but verify via CI.

## 8. The Documentation Black Hole
**Symptom:** Each repo has a README, but finding which repo does what requires tribal knowledge.
**Root Cause:** No central service catalog or repo discovery mechanism.
**Fix:** Maintain a `service-catalog` repo with Backstage/Port/ServiceNow entries. Auto-generate from repo metadata.

## 9. The CI Copy-Paste
**Symptom:** Every repo has a slightly different `.github/workflows/ci.yml`, all copy-pasted from different eras.
**Root Cause:** No shared CI workflow templates.
**Fix:** Publish reusable workflows in `toolkit/.github/workflows/`. All repos call `org/toolkit/.github/workflows/ci.yml@v3`.

## 10. The Auth Free-for-All
**Symptom:** 8 repos each implement their own JWT validation, with subtle differences.
**Root Cause:** No shared auth middleware library.
**Fix:** Publish `@org/auth-middleware` that all services import. One implementation, one security audit.
