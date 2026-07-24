# Dependency Inventory Framework

Systematic approach to graphing and analyzing all dependencies across a multi-repo organization.

## Inventory Process

1. **Per-repo extraction:** Use language-specific tools to extract the full dependency tree (direct + transitive).
2. **Centralized aggregation:** Combine all repo trees into a single graph database.
3. **Visualization:** Dependency graph showing which packages connect which repos.

## Tools by Language

| Language | Direct Dependencies | Transitive Tree | License Info |
|----------|-------------------|-----------------|--------------|
| JavaScript/TypeScript | `npm ls --depth=0` / `yarn list --depth=0` | `npm ls --all` / `npx depcruise` | `license-checker --json` |
| Python | `pip list` / `poetry show` | `pipdeptree --json` | `pip-licenses` |
| Java (Maven) | `mvn dependency:list` | `mvn dependency:tree` | `mvn license:download-licenses` |
| Java (Gradle) | `gradle dependencies` | `gradle dependencies --configuration runtimeClasspath` | Gradle License Report plugin |
| Rust | `cargo tree --depth 1` | `cargo tree` | `cargo license` |
| Go | `go list -m all` | `go mod graph` | `go-licenses` |

## Key Metrics

- **Total unique packages across org.** Baseline for governance scope.
- **Top-20 most-used packages.** These drive version alignment policy.
- **Packages used in exactly 1 repo.** Candidates for removal or consolidation.
- **Average dependency depth.** Deeper trees = more transitive risk.
- **Orphan packages:** no longer maintained upstream but still in use.

## Output Artifacts

- Dependency graph (JSON/CSV): repo -> package -> version -> license -> CVE status
- SBOM per repo (SPDX or CycloneDX format)
- Dashboard: version sprawl heatmap, CVE exposure map, license risk matrix
