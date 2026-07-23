# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
- **Account/project isolation**: separate production and non-production at the account level; never mix in a single VPC.
- **Infrastructure as Code from day one**: the console is for exploration only; all production changes go through IaC pipelines.
- **Least privilege IAM**: start with no permissions, add only what's needed; use IAM Access Analyzer to validate.
- **Design for failure**: assume any component can fail at any time; use circuit breakers, retries with backoff, and graceful degradation.
- **Region selection**: prioritize latency, data residency, service availability, and cost in that order.
