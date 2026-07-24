# Monorepo vs Polyrepo vs Hybrid Decision Matrix

Systematic scoring framework for choosing repository architecture. Score each dimension 1-5 (1 = strongly favors polyrepo, 5 = strongly favors monorepo).

## Scoring Dimensions

| Dimension | Weight | Description | 1 (Polyrepo) | 3 (Neutral) | 5 (Monorepo) |
|-----------|--------|-------------|--------------|-------------|--------------|
| Team Autonomy | High | Do teams operate independently? | Completely independent roadmaps | Some shared milestones | Always coordinated releases |
| Code Sharing Frequency | High | How often is shared code modified? | Rarely (<monthly) | Weekly | Daily |
| Release Coupling | High | Must repos version together? | Never | Some shared release trains | Always ship together |
| Security Boundaries | Medium | Different classification levels? | Many boundaries (PCI, HIPAA, SOX) | 1-2 boundaries | Single classification |
| Build Times | Medium | Would monorepo CI be acceptable? | Unacceptable (>30min) | Borderline (10-15min) | Fast (<5min) |
| Tooling Maturity | Medium | Do you have monorepo tooling? | No tooling investment | Partial (some caching) | Dedicated team + tooling |
| Team Size | Low | Total number of developers | 500+ (polyrepo natural) | 50-200 | <20 (monorepo natural) |

## Interpretation

- **< 2.5:** Polyrepo. Teams are autonomous, code sharing is rare, releases are independent.
- **2.5-3.5:** Hybrid. Shared libraries in a monorepo, services in individual repos.
- **> 3.5:** Monorepo. Teams coordinate frequently, shared code changes together, atomic cross-cutting changes needed.

## Usage Notes

Score with the current state, not the desired state. Re-score every 12-18 months as team topology evolves. If scores are split (some 1, some 5), hybrid is almost always the right answer.
