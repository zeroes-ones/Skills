## What Good Looks Like

> When tool evaluation is embedded in the development lifecycle, every significant dependency choice is backed by evidence, cost analysis, and an exit strategy. Developers don't default to familiar tools — they evaluate alternatives and choose deliberately. Quarterly audits catch abandoned dependencies before they become emergencies. Cost ladders make budget conversations data-driven instead of vendor-pitch-driven.

### Signs of Excellence

- **Every ADR cites at least 3 evaluated alternatives** with specific trade-offs, not just "we chose X because everyone uses it."
- **Dependency manifests pass automated health checks** on every CI run: `npm audit` returns zero HIGH/CRITICAL, `license-checker` returns only approved licenses, Socket.dev scan passes.
- **Billing alerts fire BEFORE free tier limits are hit**, not after. The team knows when they'll need to upgrade and has budget approved in advance.
- **Migration paths are documented for every critical dependency.** When a tool is deprecated, the team executes the existing migration plan rather than scrambling.
- **Quarterly tool audits are a recurring calendar event**, not an afterthought. 15 minutes per week scanning trends catches shifts before they're emergencies.
- **The team can articulate WHY each tool was chosen**, not just WHAT was chosen. Junior developers learn the evaluation framework by watching senior developers apply it.
- **Vendor negotiations start with competing quotes.** The team knows the alternatives and uses them as leverage. "We're considering switching to X" is backed by a completed evaluation matrix.
- **"When NOT to use" is documented for every tool.** Developers know which tools are right for which problems and — critically — which tools are WRONG for which problems.

### Signs of Dysfunction

- Tool choices are made by "what I know" or "what's popular" without evaluation. | **Fix:** Force evaluation of 2 alternatives before any adoption decision.
- Dependency versions are 2+ major releases behind without a documented reason. | **Fix:** Run `npm outdated` or `pip list --outdated` and triage each outdated package.
- The team discovers a tool is abandoned only when it breaks in production. | **Fix:** Monthly dependency health check. Set up Dependabot/Renovate and GHAS (GitHub Advanced Security) alerts.
- Cloud bills are 3x what was projected and nobody knows why. | **Fix:** Implement per-service cost tracking. Set billing alerts at $5 increments. Review bills weekly.
- The same evaluation is repeated by different teams for the same tool category. | **Fix:** Centralize tool evaluations in an ADR repository. New teams start from existing evaluations, not from scratch.
- "We can't migrate because we're too deeply integrated." | **Fix:** This is the exit cost you failed to plan for. For all future tool choices, document the migration path BEFORE adopting.
