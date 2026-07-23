# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
- **Immutable infrastructure** — Replace, never patch. New AMI/container image for every change. Baking config into golden AMIs defeats the purpose — inject at deploy time.
- **Drift detection on schedule** — `terraform plan` every 6 hours. Alert on non-empty plan. Classify drift: benign (tag mismatch), suspicious (security group opened), critical (unauthorized IAM change → page on-call).
- **Least-privilege pipelines** — OIDC federation, no static credentials. Separate IAM roles for plan (read-only) vs apply (write). Short-lived tokens with audience restriction.
- **Secrets: zero-trust model** — Assume compromise. Dynamic credentials with TTL, just-in-time access, automatic rotation. Audit log on every secret access.
- **GitOps single source of truth** — No `kubectl apply` from laptops. Git repo defines desired state; Argo CD/Flux reconciles. Manual changes auto-reverted within 5 seconds (`selfHeal: true`).
- **Cost-awareness from day one** — Tag every resource. Set budget alerts at 50%, 80%, 100% of monthly forecast. Weekly cost reviews; monthly FinOps meeting with service owners.
- **DR is a continuous practice, not a document** — Run DR tests on schedule. Measure recovery time, not just "it worked." Automate the failover — manual runbooks fail under pressure.
