# Sub-Skills — Agent Evaluation Pipeline

## When to Involve Specialized Skills

### `qa-engineer`
**Involve when:** Designing the agent testing pyramid structure, managing flaky-test patterns, or integrating eval into existing CI infrastructure.
**What they provide:** Test pyramid methodology adapted for agent non-determinism. Flaky-test management patterns. Test case generation automation.

### `ci-cd-builder`
**Involve when:** Configuring GitHub Actions/GitLab CI eval workflows, designing matrix builds for parallel eval, or setting up artifact management for eval results.
**What they provide:** CI pipeline design with caching, parallelization, and artifact storage. Quality gate configuration.

### `llm-engineer`
**Involve when:** Designing judge prompts, selecting judge models, optimizing judge cost/quality tradeoffs, or debugging judge bias.
**What they provide:** Prompt engineering for evaluation consistency. Model selection guidance. Token optimization strategies.

### `devops-engineer`
**Involve when:** Containerizing eval harness, setting up eval infrastructure (Kubernetes, Docker Registry), or configuring monitoring for eval pipeline health.
**What they provide:** Container orchestration. Infrastructure as Code for eval environments. Monitoring and alerting.

### `platform-engineer`
**Involve when:** Building eval-as-a-service, designing self-service scenario authoring, or creating eval dashboards for multiple teams.
**What they provide:** Internal developer platform patterns. API design for eval service. Multi-tenant architecture.

### `performance-engineer`
**Involve when:** Eval runtime exceeds CI timeout, eval cost exceeds budget, or eval throughput can't keep up with PR volume.
**What they provide:** Performance profiling of eval pipeline. Bottleneck identification. Cost optimization strategies.

### `security-reviewer`
**Involve when:** Gotcha scenarios include security-sensitive attacks, eval harness has access to production systems, or eval results contain sensitive data.
**What they provide:** Security review of eval infrastructure. Adversarial scenario design. Data protection for eval artifacts.
