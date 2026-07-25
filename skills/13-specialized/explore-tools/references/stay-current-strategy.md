## Stay-Current Strategy

<!-- Actionable weekly/monthly routines for maintaining tool knowledge -->

### Daily (Passive)
- **GitHub Stars:** Check your starred repos for new releases. GitHub's "releases" tab in your stars feed surfaces updates from tools you're watching.
- **Dependabot/Renovate PRs:** Open and merge dependency update PRs within 24 hours. Each merged PR is a signal that the tool is maintained and you're current.

### Weekly (~30 min)
- **GitHub Trending:** Review trending repositories in your primary languages (github.com/trending/javascript?since=weekly). This surfaces newly popular tools before they appear in curated lists.
- **npm/PyPI release watch:** Run `npm outdated` or `pip list --outdated` on active projects. Any package >2 major versions behind? Investigate whether the upgrade path offers meaningful improvements.
- **Hacker News scan:** Visit hn.algolia.com and search for "[your stack] alternative" or "Ask HN: best [tool type]" from the past week. The practitioner discussions on HN are more valuable than curated lists.
- **Reddit pulse check:** Skim r/programming and your language-specific subreddit (r/javascript, r/python, r/rust). Filter by "top this week" for the most signal.

### Monthly (~2 hours)
- **Tool audit checklist:**
  1. List every third-party dependency in production (run `npx license-checker --production` or `pip freeze`)
  2. For each dependency, check: (a) last commit date → <3 months? (b) new releases since last audit? (c) new CVEs? (d) community sentiment (any "migrating away from X" posts?)
  3. Flag any dependency that scores RED on the Adoption Risk Assessment for replacement evaluation
  4. Update the cost analysis for paid tools: any pricing changes? New free tier limits? New competitors?
- **libraries.io sweep:** Upload your dependency manifest to libraries.io to check for outdated and vulnerable packages across all ecosystems.
- **Socket.dev health check:** Run `socket diff` (if using Socket CLI) to see if any newly published versions introduce security risks.
- **Best of JS / LibHunt review:** Scan bestofjs.org or libhunt.com for your language to discover rising tools that haven't hit GitHub Trending yet.

### Quarterly (~4 hours)
- **Stack Composition Review:**
  1. Document your current tech stack (every tool, service, and library)
  2. For each: is it still the best choice? What's changed in the ecosystem?
  3. Run a mini Tool Discovery Protocol on 2-3 categories (e.g., "Are we still using the best CI/CD tool?")
  4. Update your "future-proof option" list: which tools would you adopt if starting today?
- **Cost Review:** Pull the last 3 months of bills for all SaaS tools and cloud services. Look for: (a) cost growth >20% quarter-over-quarter (investigate why), (b) tools you're paying for but barely using (cancel), (c) OSS alternatives to paid tools that have matured.
- **Security Posture Refresh:** Run a full dependency security audit: `npm audit --audit-level=high`, `pip-audit`, `cargo audit`, `trivy fs .`. Document and track remediation of any findings.
- **Conference Talk Review:** Watch 2-3 recent conference talks (PyCon, RustConf, JSConf, KubeCon, re:Invent) about tool comparisons or ecosystem trends. Conference talks often preview tools 6-12 months before mainstream adoption.

### Annually (~1 day)
- **Full Stack Retrospective:**
  1. Run the complete Tool Discovery Protocol on your ENTIRE tech stack — as if you were building from scratch today.
  2. Compare the "build today" stack with your current stack. The gap IS your technical debt in tooling choices.
  3. Prioritize migrations: which gaps cause the most pain (cost, velocity, reliability)? Which are cheapest to close?
  4. Create a "Next 12 Months Tooling Roadmap" with estimated migration costs and timelines.
- **Vendor Negotiation:** For any paid tool where you're approaching renewal, research competitors and get competing quotes. Use this leverage to negotiate 20-40% discount on annual commitments.
