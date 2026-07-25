## Production Checklist

<!-- Pre-production validation before committing to a tool -->

| # | Checklist Item | Verification Method |
|---|---------------|---------------------|
| P1 | Tool is actively maintained (commits within last 3 months) | `gh api repos/owner/repo/commits --jq '.[0].commit.author.date'` |
| P2 | Latest release is within 6 months | `gh api repos/owner/repo/releases/latest --jq '.published_at'` |
| P3 | Repository is NOT archived | `gh api repos/owner/repo --jq '.archived'` → must be `false` |
| P4 | Zero unresolved CVEs rated HIGH or CRITICAL | `gh api repos/owner/repo/security-advisories --jq '.[].severity'` or npm audit / osv.dev |
| P5 | License is compatible with project (MIT/Apache 2.0/BSD/ISC preferred) | `npx license-checker --production --summary` or `pip-licenses` |
| P6 | Full dependency tree audited for license and security (not just top-level) | `npx license-checker --production` or `fossa analyze` or `snyk test --all-projects` |
| P7 | Bundle size measured and documented (frontend libraries) | bundlephobia.com or `npx package-size [package]` |
| P8 | Free tier limits documented and understood | Vendor pricing page — screenshot for records. Set billing alerts at 50% of limits. |
| P9 | Cost projections calculated: 1-year TCO at current scale and 3-year TCO at 10x scale | Spreadsheet with: subscription + hosting + scaling + support + migration costs |
| P10 | Integration test passed: tool works in your CI environment (not just localhost) | GitHub Actions test job that installs and runs the tool |
| P11 | Team skill assessment: the team can be productive with this tool within 1 week | POC built using only docs. Time-to-first-working-feature measured. |
| P12 | Exit strategy documented: migration path to at least one alternative | ADR-style document: "How to migrate from [tool] to [alternative]" with estimated cost and timeline |
| P13 | Vendor lock-in assessed: data is portable (standard formats, export APIs) | Export test: can you export ALL your data in a standard format (JSON, CSV, SQL dump) without vendor assistance? |
| P14 | SLA/SLOs reviewed (for paid services): uptime guarantee, support response time, incident notification | Vendor SLA page — documented in internal wiki. Test support responsiveness with a pre-sales question. |
| P15 | Community health verified: active discussions, responsive maintainers, healthy issue resolution | Check GitHub issues: open vs. closed ratio, median response time, stale PR count |
