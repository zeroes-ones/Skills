# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Pipeline stages defined: lint → test → build → scan → deploy → verify | `gh workflow list --json name \| jq '.[].name' \| grep -cE "lint\|test\|build\|scan\|deploy\|verify"` → ≥ 5 | Generate pipeline template with all 6 stages |
| **[S2]** | Fan-in/fan-out used for parallel execution where beneficial | `grep -rn "needs:" .github/workflows/ \| wc -l` → ≥ 3 AND `grep -rn "strategy.*matrix" .github/workflows/ \| wc -l` → ≥ 1 | Convert sequential jobs to parallel dependency graph |
| **[S3]** | Path filters skip irrelevant workflows in monorepo | `grep -rn "paths:" .github/workflows/ \| wc -l` → ≥ 1 OR project is not a monorepo | Add `paths:` filters to each workflow |
| **[S4]** | Concurrency groups cancel redundant PR runs | `grep -rn "concurrency:" .github/workflows/ \| wc -l` → ≥ 1 | Add `concurrency: ci-${{ github.ref }}` to workflows |
| **[S5]** | All third-party actions pinned to full-length commit SHA | `grep -rnE "uses:\s+[^@]+@v[0-9]" .github/workflows/ \| wc -l` → 0 | Use `actionlint` to auto-pin actions to SHA |
| **[S6]** | OIDC federation for cloud authentication | `grep -rn "id-token:\s*write" .github/workflows/ \| wc -l` → ≥ 1 OR no cloud deploy in pipeline | Add OIDC permissions + configure cloud provider trust |
| **[S7]** | Environment protection rules on production | `gh api repos/:owner/:repo/environments/production --jq '.protection_rules'` → non-empty | Add required reviewers + branch restriction via `gh api` |
| **[S8]** | Secrets scoped per environment; never shared across environments | `gh secret list --env production \| wc -l` → ≥ 1 AND no plaintext secrets in workflow files | Move shared secrets to environment-scoped secrets |
| **[S9]** | SLSA provenance generated for all releases | `grep -rn "slsa-github-generator\|SLSA" .github/workflows/ \| wc -l` → ≥ 1 | Add `slsa-github-generator/.github/workflows/generator_generic_slsa3.yml` |
| **[S10]** | SBOM (SPDX/CycloneDX) generated and attached to releases | `grep -rn "spdx\|cyclonedx\|sbom" .github/workflows/ \| wc -l` → ≥ 1 | Add `anchore/sbom-action` to release workflow |
| **[S11]** | Signed commits enforced via branch protection | `gh api repos/:owner/:repo/branches/main/protection/required_signatures --jq '.enabled'` → `true` | Enable via `gh api --method POST` |
| **[S12]** | Dependency caching with lockfile-hash keys | `grep -rn "actions/cache\|cache-" .github/workflows/ \| wc -l` → ≥ 1 | Add `actions/cache@<sha>` with `restore-keys` fallback |
| **[S13]** | Docker BuildKit with registry cache backend | `grep -rn "cache-from\|cache-to.*type=registry" .github/workflows/ \| wc -l` → ≥ 1 | Add `cache-from: type=gha` and `cache-to: type=gha,mode=max` |
| **[S14]** | Test sharding for suites > 5 minutes | `grep -rn "matrix\|shard\|split" .github/workflows/ \| wc -l` → ≥ 1 | Add `strategy.matrix.shard` with `jest --shard` |
| **[S15]** | Automated rollback tested: health check failure → revert to previous | `grep -rn "rollback\|revert\|rollback" .github/workflows/ \| wc -l` → ≥ 1 | Add rollback step using previous deployment tag/commit |
