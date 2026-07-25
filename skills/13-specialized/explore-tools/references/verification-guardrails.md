## Verification Guardrails

<!-- Run before delivering ANY tool recommendation -->

| # | Guardrail | Check |
|---|-----------|-------|
| V1 | At least 3 alternatives evaluated | Count distinct tools in evaluation matrix. If <3, go back to Phase 2. |
| V2 | GitHub last commit date verified (within 3 months for "active" status) | `gh api repos/owner/repo/commits --jq '.[0].commit.author.date'`. If >3 months, flag as yellow. |
| V3 | License verified as compatible with project requirements | Run `npx license-checker --production` or `pip-licenses`. Flag GPL/AGPL/BUSL/SSPL. |
| V4 | Bundle size/cost verified (not guessed from memory) | Open bundlephobia.com for each npm candidate. Check vendor pricing page for services. Do not estimate from memory. |
| V5 | Security advisories checked | `npm audit --package=[name]`, GitHub Security Advisory tab, osv.dev query. Document all HIGH/CRITICAL CVEs. |
| V6 | Cost breakdown includes hidden costs | Hosting + scaling + support + migration costs documented. If any are "N/A" or blank, fill them in. |
| V7 | Free tier limitations explicitly stated | List the exact free tier limits (requests/month, storage, users, features unavailable). |
| V8 | Migration path from current tool documented | If replacing an existing tool, provide: shadow mode setup → gradual rollout → cutover plan with estimated timeline. |
| V9 | Recommendation includes "when NOT to use" guidance | Every recommendation must specify at least 2 scenarios where the tool is a bad fit. |
| V10 | All pricing tagged with verification date | Add "Pricing verified: [date]" to every cost figure. Prices change. |
| V11 | Alternatives sorted by budget tier | Group recommendations into tiers: $0 (OSS/free), $0-50 (startup), $50-500 (growth), $500+ (enterprise). |
| V12 | Adoption Risk Assessment completed for top 3 candidates | Run the full risk matrix (maintenance, stars, bus factor, issues, security, breaking changes, funding, deps, docs, ecosystem). |
| V13 | Confirmation that tools are NOT deprecated/archived | Check if the GitHub repo is archived: `gh api repos/owner/repo --jq '.archived'`. If `true`, flag as RED. |
| V14 | Dependency tree checked for known-vulnerable sub-dependencies | Run `npm audit` or `snyk test` or `socket.dev` scan. Check beyond the top-level package. |
| V15 | Recommendation caveated with training data cutoff | Add: "⚠️ Verified against my training data (cutoff: [date]). Verify current status on [registry URL] before adopting." |

### Pre-Delivery Checklist
Run through this before finalizing any tool recommendation:

```
[ ] Phase 1 complete: Requirements extracted (problem, budget, constraints, team, timeline)
[ ] Phase 2 complete: 5-10 candidates identified from registries + community sources
[ ] Phase 3 complete: Top 3-5 candidates scored across 8 dimensions with weighted matrix
[ ] Phase 4 complete: Cost analysis with 1-year and 3-year TCO for top 3 candidates
[ ] Phase 5 complete: 4-option recommendation (top, runner-up, budget, future-proof)
[ ] Adoption Risk Assessment: All 10 dimensions checked for top 3 candidates
[ ] License compatibility: Full dependency tree scanned for GPL/AGPL/BUSL contamination
[ ] Security: CVE database checked, unresolved HIGH/CRITICAL CVEs documented
[ ] Bundle size: bundlephobia.com verified for all frontend candidates
[ ] Pricing: All figures tagged with verification date, free tier limits documented
[ ] Migration path: Documented from current tool (if replacing) or from "nothing" (if new)
[ ] Anti-recommendations: 2+ scenarios where each tool is a bad fit
[ ] Training data disclaimer: Verification date + registry URL provided
```
