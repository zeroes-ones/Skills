# Error Decoder: Common Multirepo Error Patterns

Quick-reference decoder for error messages and symptoms you'll encounter in multirepo environments. Match the symptom to the diagnosis and fix.

## Build & Dependency Errors

### `Cannot find module '@org/toolkit' or its corresponding type declarations`
**Likely Cause:** Consumer hasn't installed the package, or the version in `package.json` doesn't exist in the registry.
**Fix:** Check `npm view @org/toolkit versions`. Verify the consumer's version exists. If not, the publisher may have unpublish or the version tag is wrong.

### `error TS2307: Cannot find module '@org/contracts/generated'`
**Likely Cause:** Contracts repo changed the generated output path. Consumer's import is stale.
**Fix:** Regenerate client SDK from the latest contracts. Pin the contracts version in consumer to ensure stable imports.

### `BUILD FAILED: no such package '@org//toolkit/auth': The repository could not be resolved`
**Likely Cause (Bazel):** The `MODULE.bazel` or `WORKSPACE` file references a repo that doesn't exist at the specified commit/version.
**Fix:** Verify the repo exists and the tag/commit is correct. Check that the repo is not archived or private without access.

## API & Contract Errors

### `400 Bad Request: Unknown field 'emailAddress'`
**Likely Cause:** Provider deployed a new field that isn't in the consumer's client version. Or consumer is sending a field the provider removed.
**Fix:** Update contracts, regenerate clients. Ensure providers practice additive-only changes for minor versions.

### `gRPC UNIMPLEMENTED: Method /user.v2.UserService/GetProfile not found`
**Likely Cause:** Consumer is calling a method that was removed or renamed.
**Fix:** Check the contracts changelog. The method may have been deprecated and removed. Migrate to the replacement method.

## CI/CD Errors

### `Error: This workflow is not supported because it references 'org/toolkit/.github/workflows/ci.yml@v1' which has been removed`
**Likely Cause:** The shared CI workflow was deleted or the major version tag was removed.
**Fix:** Check toolkit releases. Update consumer to reference the current major version.

### `fatal: unable to access 'https://github.com/org/internal-lib.git/': The requested URL returned error: 403`
**Likely Cause:** Repo is private. Consumer's CI doesn't have access. Or the repo was archived/transferred.
**Fix:** Grant CI token access. If archived, migrate to replacement repo.

## Governance Errors

### `remote: error: GH006: Protected branch update failed - required status check "build (14.x)" is missing`
**Likely Cause:** CI configuration changed. The required check name no longer matches what CI produces.
**Fix:** Update branch protection rules to match current CI job names. Use wildcard patterns (`build (*)`) to avoid this.

### `! [remote rejected] main -> main (cannot modify refs/heads/main: at least 1 approving review is required by reviewers with write access)`
**Likely Cause:** Branch protection requires code review. No CODEOWNER has approved.
**Fix:** Request review from a CODEOWNER. If emergency, use admin override with justification in the audit log.

## Runtime Errors

### `connect ECONNREFUSED 127.0.0.1:5432`
**Likely Cause:** Service is trying to connect to a database that doesn't exist in this environment. Each service should own its database — but in local dev, you may need multiple DBs.
**Fix:** Use docker-compose or Tilt to spin up the full dependency graph locally. Or mock external services in dev.

### `JWT verification failed: issuer mismatch. Expected 'auth.internal.company.com', got 'auth-legacy.internal.company.com'`
**Likely Cause:** Two services are using different auth providers or different issuer configurations.
**Fix:** Standardize on one auth provider. Use `@org/auth-middleware` that centralizes JWT validation config.
