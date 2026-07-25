## Adoption Risk Assessment Framework

Score each tool on this risk matrix before recommending adoption:

| Risk Factor | 🟢 Green (Go) | 🟡 Yellow (Caution) | 🔴 Red (Avoid) |
|------------|---------------|---------------------|----------------|
| **Maintenance** | Commits in last week; regular release cadence | Commits in last 3 months; irregular releases | No commits in 6+ months; no releases in 12+ months |
| **GitHub Stars** | >5,000 (active community) | 500-5,000 (growing but small) | <500 stars AND <2 years old (unproven) — except niche/domain-specific tools |
| **Bus Factor** | >10 active contributors from multiple organizations | 3-10 contributors; 1-2 organizations | 1-2 contributors from single organization (single point of failure) |
| **Issue Health** | Issues closed > Issues opened; median response time <1 week | Issues and PRs balanced; response time 1-4 weeks | Issues piling up; response time >1 month; stale PRs accumulating |
| **Security** | Zero CVEs; security policy (SECURITY.md); bug bounty program; regular audits | CVEs resolved within 30 days; basic security policy | Unresolved CVEs rated HIGH or CRITICAL; no security policy; no dependency scanning |
| **Breaking Changes** | Semantic versioning strictly followed; major versions <1/year; migration guides provided | Occasional breaking changes in minor versions; documented workarounds | Frequent major version bumps (>2/year); breaking changes in patch versions; no changelog |
| **Funding Model** | Company-backed (VC-funded or profitable) OR OpenCollective with >$50K/year | Individual sponsorship; small OpenCollective (<$10K/year) | No visible funding; solo maintainer with no sponsorship; history of abandoned projects |
| **Dependency Health** | <10 dependencies; all well-maintained; no deprecated sub-deps | 10-50 dependencies; mostly healthy with some stale deps | >50 dependencies; deprecated sub-dependencies; known-vulnerable transitive deps |
| **Documentation** | Comprehensive API docs + guides + examples + migration docs + changelog | API docs exist but gaps in guides/migration docs | No docs beyond auto-generated API; README-only; outdated docs from previous major version |
| **Ecosystem Integration** | Works with standard ecosystem tooling (TypeScript types, ESLint plugins, testing integrations) | Partial ecosystem support; some manual glue code needed | Doesn't integrate with standard tooling; requires proprietary/adapter layer |

### Traffic Light Rules:
- **All green?** → Adopt with confidence. Monthly health check.
- **1-2 yellows, rest green?** → Adopt with caution. Weekly health monitoring. Have an exit plan.
- **Any red?** → Do not adopt unless you're willing to fork and maintain. Document the risk acceptance.
- **3+ yellows?** → Treat as red. The accumulation of caution signals compounds risk exponentially.

### Quick Health Check Commands:
```bash
# Maintenance check
gh api repos/owner/repo/commits --jq '.[0].commit.author.date'  # Last commit date
gh api repos/owner/repo/releases --jq '.[0].published_at'      # Last release date

# Security check
npm audit --package=package-name           # npm ecosystem
gh api repos/owner/repo/security-advisories --jq '.[].severity'  # GitHub Security Advisories
curl -s https://api.osv.dev/v1/query -d '{"package":{"name":"pkg","ecosystem":"npm"}}'  # OSV.dev

# License check
npx license-checker --summary                # npm dependency tree
pip-licenses --summary                       # Python dependencies
cargo license --summary                      # Rust dependencies

# Bundle size check (frontend)
open "https://bundlephobia.com/result?p=package-name"
npx package-size package-name                # CLI alternative
```
