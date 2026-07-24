# Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) |
|---|---|---|
| Signing artifacts from non-hermetic builds | Isolate build environment — no network access, pre-resolved dependencies | `grep -rn 'network_mode.*host\|--network host' Dockerfile* .github/` |
| Trusting SBOMs from vendors without independent verification | Generate your own SBOM from the vendor's artifact and diff against their claimed SBOM | Compare `syft` output against vendor-provided SBOM; flag discrepancies |
| Auto-merging dependency updates without integration tests | Require full CI suite on all dependency update PRs before merge | `grep -rn 'auto-merge.*true\|automerge.*true' .github/dependabot.yml renovate.json` |
| Using long-lived CI credentials instead of OIDC | Federate CI identity via OIDC — generate per-job, short-lived tokens | `grep -rn 'GITHUB_TOKEN\|NPM_TOKEN\|PYPI_TOKEN\|DOCKER_PASSWORD' .github/workflows/*.yml` |
| Maintaining lockfiles without integrity hash verification | Pin with content hashes (npm: integrity, pip: --require-hashes) | `npm ls --json` for missing integrity fields |
