# Cross-Repo Coordination Patterns

Mechanisms for coordinating CI/CD, releases, and testing across independent repositories in a polyrepo ecosystem.

## Pattern 1: Repository Dispatch (Event-Driven)

Upstream repo publishes a release event; downstream repos subscribe and rebuild.

- **Mechanism:** `repository_dispatch` (GitHub), webhook triggers (GitLab), custom event bus
- **Use case:** Shared library releases -> downstream service rebuilds
- **Pros:** Decoupled — upstream does not know about consumers. Consumers opt in.
- **Cons:** No contract validation at trigger time. Downstream discovers breakage in CI.

## Pattern 2: Scheduled Cross-Repo Integration Tests

A dedicated workflow runs nightly across all repos, deploying the latest versions and running end-to-end tests.

- **Mechanism:** Cron-scheduled GitHub Actions workflow, GitLab pipeline schedule
- **Use case:** Detecting integration breakage before it reaches production
- **Pros:** Catches issues that individual repo tests miss. No coordination required.
- **Cons:** Slow feedback (24h cycle). Flaky tests erode trust.

## Pattern 3: Contract Testing

Consumer-driven contracts: each consumer defines what it expects from the provider. Provider CI runs against all consumer contracts.

- **Mechanism:** Pact, Spring Cloud Contract, custom contract framework
- **Use case:** Service-to-service API dependencies
- **Pros:** Catches breakage at design time, not test time. Provider knows who depends on what.
- **Cons:** Contract maintenance overhead. Requires consumer teams to write and maintain contracts.

## Pattern 4: Shared CI Templates

All repos use the same CI pipeline structure via reusable workflows or CI templates.

- **Mechanism:** GitHub reusable workflows, GitLab CI `include:project`, CircleCI orbs
- **Use case:** Consistency across repos — every repo runs the same lint, test, build, security scan
- **Pros:** Single source of truth. Updates propagate automatically.
- **Cons:** Template changes can break many repos at once. Requires versioning the templates.

## Anti-Patterns

- **Repo A's CI deploys Repo B's code.** Violates ownership boundaries. Each repo owns its own deployment.
- **Manual cross-repo version bumps.** "Please update to v2.3.1" Slack messages. Automate with Renovate/Dependabot.
