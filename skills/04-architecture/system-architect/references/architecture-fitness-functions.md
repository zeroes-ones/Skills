# Architecture Fitness Functions

Automated tests verifying architecture doesn't degrade — run in CI:

| Category | What to Test | Example Threshold |
|----------|-------------|-------------------|
| **Coupling** | No circular deps between modules | `import-linter` / `madge` |
| **Cohesion** | Module size ≤ 500 lines | Custom script |
| **Performance** | P95 latency ≤ 200ms for critical paths | k6 / Locust |
| **API compatibility** | No breaking OpenAPI changes | `openapi-diff` |
| **Security** | No hardcoded keys, no HIGH CVEs | Trivy / Semgrep |
