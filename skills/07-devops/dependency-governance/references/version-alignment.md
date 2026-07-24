# Version Alignment Policy

Tiered framework for determining when dependency versions must match across repositories and when divergence is acceptable.

## Policy Tiers

### Tier 1: Must Match
- **Scope:** Frameworks (React, Angular, Next.js, Spring Boot), security libraries (auth, crypto, JWT), database drivers.
- **Rule:** All repos on the same MAJOR version. MINOR/PATCH within 2 releases of each other.
- **Enforcement:** CI check that compares version against org baseline. Failing CI blocks merge.
- **Rationale:** Divergent versions create incompatible APIs, different behavior, and security gaps.

### Tier 2: Should Align
- **Scope:** Shared utilities (lodash, date-fns, axios), testing frameworks (Jest, Testing Library).
- **Rule:** All repos within 1 MAJOR version. MINOR/PATCH can vary freely.
- **Enforcement:** Renovate grouping with shared preset. Dashboard tracks drift.
- **Rationale:** Version divergence causes subtle bugs and bundle duplication.

### Tier 3: Free
- **Scope:** Dev tools (eslint, prettier, husky), formatters, linters, type definitions.
- **Rule:** No alignment requirement. Teams choose independently.
- **Enforcement:** Renovate updates with auto-merge. No CI enforcement.
- **Rationale:** Dev tool versions do not affect production behavior or security.

## Exception Process

- Documented exception with reason, approver, and review date.
- Temporary exceptions: "migrating within 2 sprints."
- Permanent exceptions: "legacy system on separate stack."

## Monitoring

- Quarterly alignment audit: % repos compliant per tier.
- Automated drift detection: CI scheduled job compares versions against baseline.
- Escalation: >20% drift triggers engineering leadership review.
