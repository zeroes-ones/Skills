# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
- **One process per container**: use sidecar containers for log shippers, proxies, or metrics exporters.
- **Images are immutable**: tag with git SHA, never use `:latest` in production manifests.
- **Secrets at rest**: enable encryption at rest in etcd; use External Secrets Operator or Sealed Secrets for git-safe storage.
- **Resource limits are mandatory**: without limits, a memory leak in one pod can OOM the entire node.
- **Use `kubectl diff` before applying**: preview changes and catch unintended mutations.
- **Scan images**: integrate Trivy, Grype, or Snyk into CI; block deployment on HIGH/CRITICAL CVEs.
