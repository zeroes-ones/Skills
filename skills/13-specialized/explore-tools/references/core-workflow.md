## Core Workflow

<!-- QUICK: 30s — scan phase titles -->
<!-- DEEP: 30+ min — full evaluation -->

### Phase 1: Requirement Analysis (~5 min)

**Input:** User's request for tool discovery (natural language query)

**Steps:**
1. **Extract the core problem** — What exactly needs to be solved? (e.g., "I need to add authentication to a Next.js app" not "What's the best auth library?")
2. **Identify constraints** — Budget ($0? $500/mo? enterprise?), team skills (JS? Python? Go?), timeline (MVPs vs. production-grade), scale (100 users? 1M?), compliance (SOC2? HIPAA? GDPR?)
3. **Categorize the need** — Library (npm/PyPI/cargo), framework (full-stack/backend/frontend), service (SaaS/API), platform (PaaS/IaaS), or tool (CLI/IDE/SDK)
4. **Prioritize features** — Must-have vs. nice-to-have. What's the dealbreaker? What's negotiable?
5. **Define success criteria** — How will we know the right tool was chosen? (time-to-integrate, cost/month, bundle size, team productivity)

**Output:** Requirements brief with constraints, priorities, and success criteria.

### Phase 2: Candidate Discovery (~10 min)

**Input:** Requirements brief from Phase 1

**Search Strategies by Ecosystem:**

| Ecosystem | Primary Sources | Secondary Sources | Search Query Examples |
|-----------|----------------|-------------------|----------------------|
| **JavaScript/TypeScript** | npm trends, bundlephobia, bestofjs.org | GitHub topics, Reddit r/javascript, Dev.to | `npm search [keyword]`, npmtrends.com compare |
| **Python** | pypistats.org, libraries.io | awesome-python, Reddit r/python, PyCon talks | `pip index versions [package]`, pypi.org search |
| **Rust** | crates.io stats, lib.rs, blessed.rs | awesome-rust, Rust forums, r/rust | `cargo search [keyword]`, lib.rs categories |
| **Go** | pkg.go.dev, awesome-go | Go subreddit, GopherCon talks, go.dev/blog | Google search: `golang [purpose] library` |
| **Containers** | Docker Hub pull counts, GitHub Container Registry | awesome-docker, r/docker | `docker search [keyword]`, hub.docker.com |
| **CLI/System** | Homebrew analytics, Chocolatey, apt/snap stats | awesome-cli, r/commandline | `brew search [keyword]`, `brew info --analytics [formula]` |
| **Cross-cutting** | GitHub Trending, GitHub Awesome Lists, Stack Overflow Tags | Hacker News, Reddit, Dev.to, Medium, slant.co, stackshare.io | `site:github.com/topics [keyword]`, `site:news.ycombinator.com "best [tool type]"` |

**Candidate gathering checklist:**
- [ ] Search package registries for top 5 candidates by downloads/stars
- [ ] Check GitHub Awesome lists for curated recommendations
- [ ] Search Stack Overflow for [topic] + "recommendation" or "vs"
- [ ] Search Hacker News: "Ask HN: best [tool type]" (last 2 years)
- [ ] Check bundlephobia for frontend candidates (install size, tree-shaking)
- [ ] Identify at least 5 candidates before filtering

**Output:** Longlist of 5-10 candidate tools with basic stats (stars, downloads, last update).

### Phase 3: Multi-Dimensional Evaluation (~15 min)

**Input:** Longlist of 5-10 candidates from Phase 2

**Evaluation Framework — Score each candidate across 8 dimensions:**

| # | Dimension | Weight | How to Measure | Data Source |
|---|-----------|--------|---------------|-------------|
| 1 | **Active Maintenance** | 25% | Last commit date, release frequency (releases/year), contributor count, issue response time | GitHub Insights, npm release history, PyPI release history |
| 2 | **Bundle Size / Cost** | 20% | Install size (minified + gzipped), dependency count, tree-shaking support. For services: free tier limits, paid tier pricing, scaling cost | bundlephobia.com, npm-stat, vendor pricing pages, AWS/GCP pricing calculator |
| 3 | **Community Size** | 15% | GitHub stars, npm/PyPI weekly downloads, Stack Overflow questions (tag count), Discord/Slack member count | GitHub, npm trends, Stack Overflow tags, community platforms |
| 4 | **Documentation Quality** | 15% | Docs completeness (API reference, guides, tutorials, examples), TypeScript types (DefinitelyTyped or bundled), changelog quality, migration guides | Official docs, tsdocs.dev, DefinitelyTyped, GitHub wiki |
| 5 | **Security Posture** | 15% | CVE count (resolved vs. unresolved), security policy (SECURITY.md), dependency health (Snyk/Socket.dev), audit history, bug bounty program | GitHub Security Advisory, Snyk Advisor, Socket.dev, npm audit, osv.dev |
| 6 | **License Compatibility** | 5% | License type (MIT, Apache 2.0, BSD, GPL, AGPL, BUSL, SSPL), license of dependencies | GitHub license field, `license-checker`, FOSSA, SPDX license list |
| 7 | **Performance** | 5% | Benchmark data, runtime overhead, memory footprint, cold start time (serverless), throughput | Published benchmarks, independent comparisons, bundlephobia size-impact |
| 8 | **Learning Curve** | Extra (tiebreaker) | Time-to-first-feature, quality of getting-started guide, API surface complexity, team familiarity | Personal assessment based on team skill level |

**Scoring methodology:** Score each dimension 1-5 (5 = excellent). Multiply by weight. Sum for total score.

**Example scoring for a frontend state management library comparison:**

| Candidate | Maint. (25%) | Size/Cost (20%) | Community (15%) | Docs (15%) | Security (15%) | License (5%) | Perf. (5%) | **Total** |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Zustand | 5 (1.25) | 5 (1.00) | 4 (0.60) | 4 (0.60) | 5 (0.75) | 5 (0.25) | 5 (0.25) | **4.70** |
| Jotai | 4 (1.00) | 5 (1.00) | 4 (0.60) | 3 (0.45) | 5 (0.75) | 5 (0.25) | 4 (0.20) | **4.25** |
| Redux Toolkit | 5 (1.25) | 3 (0.60) | 5 (0.75) | 5 (0.75) | 5 (0.75) | 5 (0.25) | 3 (0.15) | **4.50** |
| MobX | 4 (1.00) | 3 (0.60) | 4 (0.60) | 3 (0.45) | 4 (0.60) | 5 (0.25) | 4 (0.20) | **3.70** |
| Valtio | 3 (0.75) | 5 (1.00) | 3 (0.45) | 3 (0.45) | 4 (0.60) | 5 (0.25) | 5 (0.25) | **3.75** |

**Output:** Scored shortlist of 3-5 candidates with dimension-by-dimension comparison matrix.


### Phase 4: Cost Analysis (~10 min)

**Input:** Shortlisted candidates from Phase 3

**Build a cost comparison for at least 3 options:**

| Cost Factor | Tool A | Tool B | Tool C |
|-------------|--------|--------|--------|
| Free tier: what's included | [limits] | [limits] | [limits] |
| Free tier: what's NOT included | [missing features] | [missing features] | [missing features] |
| First paid tier | [price/mo] | [price/mo] | [price/mo] |
| Break-even point (when does free → paid?) | [users/requests/data] | [users/requests/data] | [users/requests/data] |
| Hidden costs: hosting | [cost estimate] | [cost estimate] | [cost estimate] |
| Hidden costs: scaling | [cost at 10x/100x] | [cost at 10x/100x] | [cost at 10x/100x] |
| Hidden costs: support/enterprise | [cost] | [cost] | [cost] |
| Hidden costs: migration (exit cost) | [cost estimate] | [cost estimate] | [cost estimate] |
| 1-year TCO (10K users) | [total] | [total] | [total] |
| 3-year TCO (100K users) | [total] | [total] | [total] |
| Vendor lock-in risk | [Low/Med/High] | [Low/Med/High] | [Low/Med/High] |

**Cost Analysis Principles:**
- **Always calculate TCO, not just subscription price.** A $0/month OSS tool that requires 20 hours/month of maintenance costs $1,000-$3,000/month in engineer time.
- **Free tier limits are real constraints.** "Unlimited" in free tier marketing means "unlimited until our fair use policy kicks in." Read the fine print.
- **Scaling costs are nonlinear.** A tool that costs $0 at 1K users may cost $5,000/month at 100K users. Graph the cost curve at 1x, 10x, and 100x current scale.
- **Exit costs are adoption costs in reverse.** If migrating away costs $80,000, factor that into your decision. Prefer tools with standard protocols and open data formats.
- **Self-hosting is not free.** Self-hosting saves subscription fees but costs: server ($20-200/mo), maintenance (5-20 hrs/mo), security patches, backups, monitoring, on-call burden.

**Output:** Cost comparison matrix with 1-year and 3-year TCO for each candidate.


### Phase 5: Recommendation (~5 min)

**Input:** Scored shortlist with cost analysis from Phases 3-4

**Deliver a structured recommendation with 4 options:**

**1. Top Recommendation** — The overall winner with justification:
- Why it wins across the weighted dimensions
- What trade-offs it makes (no tool is perfect)
- Best-fit scenario ("ideal for teams that...")

**2. Runner-Up** — The strong alternative:
- Where it beats the top pick (specific dimensions)
- Why it lost (the specific trade-off that cost it the top spot)
- When to choose this instead ("better if you need...")

**3. Budget Option** — The cost-optimized pick:
- Free tier or OSS with self-hosting
- What you sacrifice (features, support, scale)
- Break-even point where you should upgrade to paid

**4. Future-Proof Option** — The scalability pick:
- What to migrate to when you outgrow the top recommendation
- Trigger criteria ("when you hit X users or Y requests/month")
- Migration complexity and estimated cost

**Migration Path (if replacing an existing tool):**
- Step-by-step migration plan (shadow mode → gradual rollout → cutover)
- Estimated migration timeline and cost
- Risk mitigation (rollback plan, data export, backward compatibility window)

**"When NOT to Use" Section** — Critical for honest evaluation:
- Scenarios where this tool is a bad fit
- Anti-patterns that cause failure with this tool
- Constraints that should disqualify this tool (minimum scale, required expertise, platform lock-in)

**Output:** Final recommendation document with all 4 options, migration path, and disqualifying criteria.
