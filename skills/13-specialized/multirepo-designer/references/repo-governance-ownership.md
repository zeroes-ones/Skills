# Repo Governance & Ownership Models

Clear ownership prevents the "tragedy of the commons" where every repo belongs to everyone and no one simultaneously. Below are proven governance models for multirepo ecosystems.

## Ownership Models

### 1. Team-Owned (Recommended)
Each repo has exactly one owning team. The team is responsible for reviews, releases, incidents, and roadmap.

```
# .github/CODEOWNERS
* @org/identity-team
/docs/ @org/identity-team @org/tech-writers
/tools/migration/ @org/identity-team @org/platform-tooling
```

### 2. Federated Ownership
Core modules owned by a platform team; extensions owned by domain teams.

```yaml
# repo-metadata.yaml
repo: toolkit
primary_owner: platform-tooling
federated_owners:
  - path: /plugins/auth/
    team: identity-team
  - path: /plugins/billing/
    team: commerce-team
```

### 3. Community-Owned (InnerSource)
Repos open for contributions from any team, with designated maintainers.

```yaml
# MAINTAINERS.md
maintainers:
  - alice (platform-tooling) — LGTM, merge
  - bob (identity-team)   — LGTM, merge
contributors:             # Can review, cannot merge
  - charlie (commerce-team)
  - dana (reporting-team)
```

## Governance Policies

### CODEOWNERS Enforcement
```yaml
# Branch protection rules applied across all repos via toolkit CI template
branch-protection:
  require_codeowner_reviews: true
  required_approving_review_count: 1
  dismiss_stale_reviews: true
  require_linear_history: true
```

### Repo Lifecycle States

| State | Criteria | CI/CD | Support Level |
|-------|----------|-------|---------------|
| **Incubating** | New repo, < 3 months old | Optional | Best-effort |
| **Active** | Owned, documented, tested | Required | Full support |
| **Maintenance** | Stable, low change velocity | Required | Bug fixes only |
| **Deprecated** | Replacement exists | Optional | Critical security only |
| **Archived** | Read-only, no new issues | Disabled | None |

### Archival Checklist

Before archiving a repo:
- [ ] Migrate active consumers to replacement repo
- [ ] Copy relevant docs/history to replacement
- [ ] Update all references in other repos' docs
- [ ] Archive with a README pointing to replacement
- [ ] Announce retirement 90 days before archival
- [ ] Remove from monitoring dashboards

## The "One Repo, One Owner" Rule

Every repo MUST have exactly one PRIMARY owner. Co-ownership ("Team A and Team B both own this") leads to diffusion of responsibility. If a repo genuinely serves two teams, split it or use federated ownership with clear boundaries.
