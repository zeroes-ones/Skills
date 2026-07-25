---
name: seo-specialist
description: >
  Use when performing technical SEO audits, deploying structured data (JSON-LD/schema), optimizing Core Web
  Vitals, managing crawl budgets, defining E-E-A-T content strategy, configuring international SEO (hreflang),
  diagnosing JavaScript SEO issues, or responding to algorithm updates. Handles site architecture, indexing
  strategy, link building, rank tracking, and search visibility optimization. Do NOT use for paid search (SEM),
  social media strategy, email marketing, or conversion rate optimization.
license: MIT
tags:
- seo
- technical-seo
- structured-data
- core-web-vitals
- crawl-budget
- javascript-seo
- json-ld
- hreflang
author: Sandeep Kumar Penchala
type: growth
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
  - content-strategist
  - frontend-developer
  - analytics-engineer
  feeds_into:
  - content-strategist
  - growth-engineer
  - marketing-manager
---
# SEO Specialist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Expert field manual for technical SEO strategy, audit execution, and search visibility optimization.
Covers the full lifecycle: crawl budget management, structured data deployment, Core Web Vitals
remediation, content SEO (E-E-A-T, topic clusters, semantic search), international SEO (hreflang,
localization), JavaScript SEO (SSR/SSG, dynamic rendering), link building strategy, rank tracking,
and algorithm update response.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("robots.txt", "Disallow:")` OR `file_exists("sitemap.xml")` OR `file_contains("*", "<link rel=\"canonical\"")` | This is your skill. Jump to **Core Workflow** — Phase 1 (Technical SEO Audit). |
| A2 | `file_contains("*", "application/ld+json")` OR `file_contains("*", "json-ld")` OR `file_exists("schema.json")` | Jump to **Core Workflow** — Phase 4 (Structured Data / JSON-LD). |
| A3 | `file_contains("*", "lighthouse")` OR `file_contains("*", "web-vitals")` OR `file_contains("package.json", "\"web-vitals\"")` | Jump to **Core Workflow** — Phase 2 (Core Web Vitals Optimization). |
| A4 | `file_contains("*", "hreflang")` OR `file_contains("*", "x-default")` OR `file_contains("*", "lang=\"")` | Jump to **Core Workflow** — Phase 5 (International SEO / Hreflang). |
| A5 | `file_contains("*", "getServerSideProps\|SSR\|server-side")` AND `file_contains("*", "<div id=\"root\">")` | Jump to **Core Workflow** — Phase 6 (JavaScript SEO / SPA Rendering). |
| A6 | `file_exists("sitemap_index.xml")` OR `file_contains("*", "crawl-budget\|crawl budget")` | Jump to **Decision Trees** — Crawl Budget Optimization. |
| A7 | `file_contains("*", "disavow\|backlink\|link-building")` OR `file_exists("disavow.txt")` | Jump to **Core Workflow** — Phase 7 (Link Building & Authority). |
| A8 | `file_contains("*", "canonical\|rel=\"canonical\"")` AND `file_contains("*", "noindex\|<meta.*robots")` | Jump to **Decision Trees** — Indexing & Canonical Strategy. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Technical SEO audit (site migration, traffic drop, or health check) → Start at "Core Workflow > Phase 1"
├── Structured data / JSON-LD / schema markup → Go to "Core Workflow > Phase 4"
├── Core Web Vitals optimization (LCP/INP/CLS) → Jump to "Core Workflow > Phase 2"
├── Crawl budget & indexing issues → Go to "Decision Trees > Crawl Budget Optimization"
├── E-E-A-T content strategy & topical authority → Go to "Core Workflow > Phase 3"
├── International SEO (hreflang, multi-language) → Jump to "Core Workflow > Phase 5"
├── JavaScript SEO (SPA, JS-rendered content) → Go to "Core Workflow > Phase 6"
├── Link building & authority gap analysis → Jump to "Core Workflow > Phase 7"
├── Rank tracking & monitoring setup → Go to "Core Workflow > Phase 8"
├── Cross-skill: keyword strategy → Invoke content-strategist skill
├── Cross-skill: structured data implementation → Invoke frontend-developer skill
├── Cross-skill: SEO-safe experiment rules → Invoke growth-engineer skill
├── Cross-skill: campaign page SEO → Invoke marketing-manager skill
└── Not sure? → Start at "Core Workflow > Phase 1"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to promise ranking improvements with specific timelines.** SEO outcomes depend on competitors, algorithm updates, and indexation speed — none of which you control. | Trigger: generated output contains "will rank #1" OR "will increase traffic by X%" OR a date range like "within 3 months" coupled with ranking claims | STOP. Respond: "I cannot promise specific ranking outcomes or timelines. SEO depends on competitors, algorithm updates, and indexation speed. Instead, here are the data-driven changes recommended based on your crawl logs, CrUX data, and GSC trends — and the observable signals to watch for improvement." |
| **R2** | **REFUSE to make recommendations without data evidence.** Every SEO recommendation must be backed by crawl logs, CrUX data, GSC trends, or SERP analysis — never gut feel. | Trigger: generated output contains "should","consider","might help","try" without a preceding data reference (GSC, CrUX, Screaming Frog, Ahrefs, SERP) | STOP. Respond: "I need data before making this recommendation. Share your GSC coverage report, CrUX field data, crawl export, or SERP analysis so I can ground every recommendation in evidence. I won't prescribe without diagnosing first." |
| **R3** | **REFUSE to present algorithm behavior as fact unless Google has documented it.** Qualify all Google behavior with "based on observed patterns" unless citing official documentation. | Trigger: generated output contains "Google does" OR "Google will" OR "the algorithm" without "based on observed" OR a link to developers.google.com/search | STOP. Insert qualifier: "Based on observed patterns (and unless Google has documented this, it's an observation, not a fact)..." |
| **R4** | **REFUSE to recommend technical fixes without content strategy.** A perfectly crawled site with thin content still won't rank. Bundle technical and content recommendations together. | Trigger: generated output contains only technical fixes (sitemap, robots.txt, canonical, CWVs, schema) with zero content recommendations (keyword targeting, content gaps, E-E-A-T, topic clusters) | STOP. Append: "These technical fixes address crawlability — but without content strategy, crawlable is not rankable. Let me also assess your content: keyword targeting, topic clusters, E-E-A-T signals, and content gaps against the SERP." |
| **R5** | **STOP and refuse to theorize without verification data.** Do not speculate about what might be wrong. Test with Screaming Frog, PageSpeed Insights, Rich Results Test, or GSC URL Inspection before recommending. | Trigger: generated output says "might be caused by" OR "could be" OR "possibly" without referencing an actual tool output or test result | STOP. Respond: "I won't theorize about root causes. Let me verify: run Screaming Frog on the affected pages, PageSpeed Insights for CWVs, Rich Results Test for schema, and GSC URL Inspection for rendering. Share the results and I'll give you evidence-based recommendations." |
| **R6** | **DETECT and WARN when crawler access is unavailable.** If you can't access GSC, crawl data, or analytics, do not guess at root causes — admit the limitation. | Trigger: user asks for diagnosis AND conversation has no reference to GSC data, crawl exports, CrUX reports, or analytics dashboards | WARN. Respond: "I cannot diagnose root causes without data. I need at minimum: GSC coverage report export, a Screaming Frog crawl, or CrUX field data. Without these, I'd be guessing — and guessing wastes your time. Share what you can access." |
| **R7** | **DETECT and WARN about algorithm update panic reactions.** Core updates roll out over 2 weeks. Do not recommend changes during the rollout based on real-time fluctuations. | Trigger: user reports traffic drop AND mentions a core/algorithm update AND asks for immediate fixes before the update has fully rolled out (< 14 days since announcement) | WARN. Respond: "Core updates take ~2 weeks to fully roll out. Changes made during the rollout are noise — you're reacting to incomplete signals. Wait for the rollout to complete, then analyze: which pages lost traffic? which queries? is the drop proportional to pre-update quality? Diagnose before you prescribe." |

### Anti-Hallucination Ground Rules
- **Admit uncertainty**: If you are unsure about any API, version, configuration, or domain-specific fact, state "I am not certain about X — consult [authoritative source]" rather than guessing.
- **Flag your knowledge cutoff**: State "My training data ends in [date]. Verify current documentation for any version-specific details or newly released features."
- **Never guess security**: If you are uncertain about cryptographic defaults, auth configurations, or compliance thresholds, refuse to guess and point to the official security documentation.
- **VERIFIED**: Mark all definitive claims with **[VERIFIED]** when confirmed by documentation. Mark uncertain claims with **[BEST-KNOWN]** and provide the citation path to verify.

## 
## The Expert's Mindset

Master seo specialists understand that strategy is not about predicting the future — it's about **being less wrong than the competition, faster**.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Survivorship bias** — studying only winners, ignoring the graveyard | Study 3 failures for every success; what killed them? |
| **Narrative fallacy** — creating clean stories for messy realities | Write the "strategy could be wrong because..." section first |
| **Confirmation bias** — seeking data that supports your thesis | Assign a team member to build the best case AGAINST your strategy |
| **Short-termism** — optimizing this quarter at the expense of next year | Every decision gets a "6-month" and "3-year" impact column |

### What Masters Know That Others Don't
- **The bottleneck is always one thing.** Find it. Fix it. Then find the next one.
- **Strategy = what you say NO to.** If your strategy doesn't exclude anything, it's not a strategy.
- **Timing beats brilliance.** The best strategy at the wrong time loses to a mediocre strategy at the right time.

### When to Break Your Own Rules
- **Bet the company when the asymmetry is right.** If downside = $1M and upside = $1B, the math doesn't care about your process.
- **Ignore the data when you're creating a new category.** By definition, there's no data for something that doesn't exist yet.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Initiative | Execute a defined strategic initiative with clear metrics |
| **L2** | Product line / function | Define strategy for a product line; own outcomes |
| **L3** | Business unit | Set multi-year strategy for a business unit; allocate resources across competing priorities |
| **L4** | Company | Define company-wide strategy; make existential trade-off decisions |
| **L5** | Industry | Shape industry dynamics; create new market categories |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 seo specialist, develop..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Launching a new domain or executing a site migration — pre-launch SEO audit and post-launch verification
- Organic traffic decline: root cause diagnosis — manual actions, algorithm update, technical regression, competitor moves
- Implementing structured data (JSON-LD): Article, Product, FAQ, HowTo, LocalBusiness, Organization, BreadcrumbList, Sitelinks Searchbox
- Core Web Vitals below thresholds: LCP > 2.5s, INP > 200ms, CLS > 0.1 — with per-metric optimization playbooks
- Crawl budget wasted on low-value URLs (facets, pagination, query params, duplicate content)
- Multi-language/multi-region site: hreflang architecture, ccTLD vs subdirectory vs subdomain decision
- JavaScript-heavy site: SSR/SSG strategy, dynamic rendering, hydration impact on indexing
- Competitor outranking on high-intent keywords — content gap analysis and SERP feature targeting
- Building a link acquisition strategy: digital PR, broken link building, HARO, link reclamation
- Setting up SEO monitoring: GSC API dashboards, rank tracking, algorithm update alerts

## Decision Trees
**(QUICK)**

> See [references/decision-trees.md](references/decision-trees.md) for the full SEO decision trees covering technical SEO audits, content optimization flows, keyword research frameworks, and crawl budget diagnostics.

## Core Workflow
**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Technical SEO Audit & Crawl Optimization

1. **Crawl Budget Management** — Define what percentage of crawl budget reaches valuable pages:
   ```
   Crawl Budget Formula:
   Crawl Rate Limit (Googlebot requests/sec from Search Console) ×
   Crawl Demand (URL popularity + freshness signals) =
   Effective crawl budget

   Budget Killers (wasting crawl capacity):
   ❌ Faceted navigation: /?color=red&size=large&sort=price — exponential URL space
   ❌ Session IDs in URL: /product?sessionid=abc123
   ❌ Infinite scroll without History API pushState
   ❌ Poorly configured pagination: ?page=1 through ?page=5000
   ❌ Duplicate content with different URL slugs
   ❌ Staging/dev environments accidentally open to crawlers

   Budget Reclamation Strategy:
   1. robots.txt: Disallow: /*?sort=*, Disallow: /*?filter=*, Disallow: /search/*
   2. Canonical tags on faceted pages → point to clean URL
   3. noindex + nofollow on thin/utility pages (login, cart, account settings)
   4. Redirect chains: audit all redirects → flatten to single 301 hop
   5. Remove stale URLs from sitemaps (404, redirected, noindex)
   ```

**What good looks like:** Lighthouse SEO score ≥ 90. Core Web Vitals pass on 75th percentile of real users. XML sitemap submitted and indexed. robots.txt allows all public content, blocks all private. Every page has unique title, meta description, and canonical URL.

2. **XML Sitemaps — Production Patterns**:
   ```xml
   <!-- Sitemap index for sites > 50K URLs — split by content type -->
   <?xml version="1.0" encoding="UTF-8"?>
   <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     <sitemap><loc>https://example.com/sitemap-products.xml</loc><lastmod>2026-07-15</lastmod></sitemap>
     <sitemap><loc>https://example.com/sitemap-articles.xml</loc><lastmod>2026-07-15</lastmod></sitemap>
     <sitemap><loc>https://example.com/sitemap-categories.xml</loc><lastmod>2026-07-15</lastmod></sitemap>
   </sitemapindex>
   ```

   **Sitemap Rules**:
   - Only canonical URLs. No URLs with `noindex`. No redirects. No 404s.
   - `<lastmod>` must reflect actual content changes (don't set to today's date for all URLs)
   - `<priority>` is largely ignored by Google — invest time in `<lastmod>` and URL selection instead
   - For news: separate Google News sitemap with `news:news` namespace — URLs published in last 48 hours
   - For video: video sitemap or `VideoObject` schema — use schema for richer results
   - Compress with gzip: `sitemap.xml.gz` — submit compressed URL to GSC

3. **robots.txt Precision**:
   ```
   # Pattern: allow crawling, block only problematic paths
   User-agent: *
   Allow: /
   Disallow: /api/
   Disallow: /*?sort=
   Disallow: /*?filter=
   Disallow: /*?color=
   Disallow: /search
   Disallow: /checkout
   Disallow: /account
   Sitemap: https://example.com/sitemap-index.xml

   User-agent: Googlebot-News
   Allow: /

   User-agent: GPTBot
   Disallow: /
   ```

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.


## Error Recovery
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->
SEO touches content, engineering, marketing, and design. Rankings degrade when any of these operate in isolation.

### Decision Gates & Artifacts

| Gate | Condition | Action |
|------|-----------|--------|
| SEO ↔ Content | Keyword targeting strategy or content gap analysis | Coordinate with `content-strategist`; share keyword research and SERP intent data |
| SEO ↔ Frontend | Core Web Vitals regression, structured data, or JS rendering | Involve `frontend-developer`; share CWVs scores, schema specs, and rendering audit results |
| SEO ↔ Growth | A/B test SEO safety review or landing page experiment | Sync with `growth-engineer`; agree on canonical rules and noindex directives for test pages |
| SEO ↔ Marketing | Campaign landing pages or paid/organic cannibalization risk | Coordinate with `marketing-manager`; review keyword overlap and landing page SEO requirements |
| SEO ↔ Analytics | GSC data integration or organic traffic anomaly detection | Involve `analytics-engineer`; share API access and anomaly thresholds |

**Artifacts shared across skills:**
- Keyword research document (shared with `content-strategist`, `marketing-manager`)
- Technical SEO audit report (shared with `frontend-developer`, `growth-engineer`)
- Structured data specification (shared with `frontend-developer`)
- Ranking and traffic dashboard (shared with `content-strategist`, `marketing-manager`, `analytics-engineer`)

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Content Strategist** | Content planning, keyword strategy | Keyword targets, content gaps, SERP intent analysis |
| **Frontend Developer** | Core Web Vitals, structured data, rendering | CWVs scores, JS rendering audit, `<head>` markup requirements |
| **Backend Developer** | Sitemaps, redirects, URL structure, canonicals | Dynamic sitemap spec, redirect map, server-side rendering decisions |
| **Growth Engineer** | A/B testing SEO-safe parameters, landing pages | Canonical URL rules, noindex on test pages, traffic impact of experiments |
| **UX Designer** | Navigation, IA, mobile UX | Crawl depth analysis, mobile usability issues, internal linking structure |
| **System Architect** | CDN, page speed, SSR vs CSR | LCP/INP targets, caching strategy, rendering architecture impact on crawl budget |
| **Marketing/Demand Gen** | Campaign landing pages, paid search | Keyword cannibalization risks, landing page SEO requirements |
| **Data/Analytics** | GA4, Search Console, rank tracking | Event tracking for SEO metrics, GSC data integration, attribution modeling |
| **Technical Writer** | Documentation site, blog platform | Docs site crawlability, content hierarchy, schema markup for docs |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Site redesign or URL structure change | Content Strategist, Frontend Dev, Marketing | Redirect planning, content migration, traffic preservation |
| Core Web Vitals regression below threshold | Frontend Dev, System Architect, Project Manager | Performance blocks indexing; needs immediate fix |
| New JavaScript framework adoption (SPA → CSR) | System Architect, Frontend Dev, Content Strategist | JS rendering breaks crawlability; needs SSR/hydration review |
| Organic traffic drop >20% week-over-week | Marketing, Content Strategist, Growth Engineer | Algorithm update or technical regression; triage immediately |
| New subdomain or international site launch | System Architect, Content Strategist, Backend Dev | Domain authority split, hreflang, geo-targeting |
| Structured data errors in GSC | Frontend Dev, Backend Dev | Rich results eligibility lost; fix within 48 hours |
| Crawl budget exhaustion (log analysis shows) | System Architect, Backend Dev | Pages not indexed; prune or optimize crawl efficiency |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Manual action (penalty) in GSC | **Legal Advisor** + VP Engineering | Legal risk if algorithmic; needs formal response plan |
| Competitor outranking on primary keyword after algorithm update | **Content Strategist** + Growth Engineer | Content quality + technical gap analysis required |
| Site migration (domain change) with traffic at risk | **CTO Advisor** + Project Manager | Cross-team coordination; executive visibility needed |
| SEO recommendations blocked by engineering for >2 sprints | **CTO Advisor** or VP Product | SEO debt compounds; needs prioritization authority |
| Paid and organic cannibalizing >30% overlap | **Marketing Lead** + Growth Engineer | Budget waste; needs channel alignment |

### Route to Other Skills

- **`content-strategist`** — When keyword research, topic clusters, or content gap analysis needs to feed into content planning
- **`frontend-developer`** — When Core Web Vitals fixes, structured data markup, or JS rendering changes are needed
- **`growth-engineer`** — When A/B tests need SEO safety review, canonical rules, or noindex coordination
- **`marketing-manager`** — When paid and organic search strategies need alignment or campaign landing page SEO


| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `product-strategist` | Target audience, growth model (PLG vs SLG), product positioning | Before designing growth experiments or content strategy |


## Proactive Triggers

<!-- QUICK: 30s -- trigger-action table for autonomous SEO workflow -->

The SEO specialist detects ranking and crawl health signals before they become traffic losses. Every trigger is tied to an observable signal in GSC, CrUX, or crawl data.

| Trigger | Action | Why |
|---------|--------|-----|
| GSC reports a sudden spike in "Discovered - currently not indexed" for 10+ pages that were previously indexed | Check the affected pages: (a) are they new pages with thin content? (b) did a recent deploy change the rendering behavior? (c) is the crawl budget exhausted (check server logs for crawl rate)? Fix the root cause within 48 hours — pages in limbo for >2 weeks rarely get indexed | Google's "discovered but not indexed" is a quiet emergency — pages that sit in this state are invisible to search. The cause is almost always content quality, rendering failure, or crawl budget exhaustion. Each day of inaction entrenches the exclusion |
| `frontend-developer` deploys a new page template without structured data — 3 weeks later, rich results eligibility is lost for 50+ pages | Add structured data validation to the CI/CD pipeline: any PR that adds or modifies page templates must pass Rich Results Test for the relevant schema types. Block the deploy if schema is missing or invalid. Add a GSC Enhancements monitor that alerts on new errors within 1 hour | Schema errors compound silently — one template change can strip rich results from hundreds of pages. CI/CD schema validation is the only reliable defense. The cost of a schema CI check is milliseconds; the cost of lost rich results is months of recovery |
| Core Web Vitals CrUX report shows LCP degraded from 2.1s to 3.8s (p75) for the last 28-day collection period | Don't wait for the next CrUX update. Immediately: (a) check the CrUX API for daily trends — is it a spike or a drift? (b) audit the last deploy that touched images, fonts, or above-the-fold rendering, (c) run WebPageTest on the affected pages from a slow 4G connection, (d) revert the offending change if identified | CrUX is a 28-day rolling average — a 3.8s reading means users have been suffering for weeks. By the time it shows in the dashboard, the damage is done. Monitor daily via the CrUX API, not monthly via the dashboard |
| Organic traffic to 5+ pages targeting the same topic cluster drops simultaneously but rankings haven't changed — Google is showing a featured snippet or "People Also Ask" that's stealing clicks | Check SERP features for the affected queries: is a featured snippet answering the query directly? Is a knowledge panel occupying above-the-fold real estate? Optimize for the snippet: structure content to directly answer the query in 40-60 words. Claim the snippet instead of competing against it | Zero-click searches are the silent traffic killer — rankings stay the same, traffic evaporates. The only defense is to own the SERP feature that's stealing your clicks. If Google is going to answer the query on the SERP, make sure it's your content they quote |
| Crawl log analysis shows Googlebot spending 60%+ of crawl budget on faceted navigation URLs (e.g., `?sort=price&color=red&size=large`) and ignoring new product pages | Add `Disallow: /*?sort=*` and `Disallow: /*?color=*` to robots.txt for non-essential facet combinations. Use `rel=canonical` on filtered pages pointing to the main category. Implement `<a href>` with `rel=nofollow` on low-value facet links. Monitor crawl budget allocation weekly for 30 days post-change | Faceted navigation is crawl budget cancer — it generates infinite URL combinations that Googlebot dutifully crawls, starving your real content. Robots.txt is your scalpel: disallow what wastes budget, allow what needs indexing. Audit crawl budget quarterly |
| Competitor outranks you on a primary keyword after a core update — their page has similar content length but 3x more backlinks from authoritative domains in your industry | Don't try to out-write them — you can't content-quality your way past a backlink gap this large. Instead: (a) identify the specific domains linking to them, (b) create a data study, original research, or interactive tool that those domains would want to cite, (c) pitch it to the top 10 linking domains | Content quality closes small gaps; backlink authority closes large ones. A page with 3x the domain authority will outrank you even with worse content. The SEO specialist's job is to diagnose the GAP, not just the symptom — and prescribe the right lever: content for quality gaps, digital PR for authority gaps |
| `growth-engineer` launches an A/B test that changes page content without implementing canonical tags — duplicate content appearing in Google index within 48 hours | Halt the experiment. Implement SEO-safe A/B testing: (a) all variant pages must include `<link rel="canonical" href="[CONTROL_URL]">`, (b) add `<meta name="robots" content="noindex, nofollow">` on variant pages if content differs substantially, (c) use `Vary: User-Agent` server header, (d) maintain URL structure — use query params or cookies, not separate URLs. Audit all active experiments for SEO safety | A/B tests are the #1 source of accidental duplicate content. The growth team optimizes for conversion; the SEO team must be the gatekeeper. Every experiment launch checklist must include an SEO review step — no exceptions |
| GSC manual action notification: "Site violates Google Webmaster Guidelines" — this is an SEO SEV1, equivalent to a production outage | Immediately: (a) read the full manual action description, (b) audit the site for the specific violation type, (c) fix ALL instances of the violation (not just the obvious ones), (d) document the fix with before/after evidence, (e) submit a reconsideration request with a detailed explanation of what was fixed and why it won't recur. Do NOT submit a reconsideration request until the fix is complete — a rejected request doubles the penalty duration | A manual action is Google's nuclear option — it means a human reviewer found your site in violation. Reconsideration requests are reviewed by humans who look for thoroughness and sincerity. A rushed, incomplete fix submitted with a generic apology will be rejected. Fix everything, document everything, then submit once |

### Service Interaction: SEO Specialist → Frontend Developer

The SEO-Specialist-to-Frontend-Developer partnership is where search visibility meets web performance and markup. The SEO specialist defines what Google needs to see; the frontend developer implements how it renders.

| Interaction Point | What SEO Specialist Provides | What Frontend Developer Needs |
|-------------------|---------------------------|-------------------------------|
| **Core Web Vitals optimization** | CrUX field data showing which pages fail LCP/INP/CLS thresholds, prioritized by traffic impact; specific element-level diagnosis (which image is LCP? which layout shift is CLS?) | Performance budget constraints, image optimization pipeline (WebP/AVIF, srcset, lazy loading strategy), font loading strategy (font-display, subsetting), bundle splitting plan |
| **Structured data implementation** | JSON-LD schema specification per page type (Article, Product, FAQ, BreadcrumbList, Organization), Rich Results Test validation criteria, monitoring requirements | Schema generation approach (statically in HTML, dynamically via JS injection, or via GTM?), integration with CMS data models, schema update workflow when content changes |
| **JavaScript rendering audit** | List of critical SEO elements that MUST be in server-rendered HTML (title, meta description, canonical, hreflang, H1, body text, internal nav), GSC URL Inspection screenshots showing rendering gaps | SSR/SSG architecture assessment, hydration strategy, dynamic rendering fallback (Prerender.io or Rendertron) if full SSR is infeasible, `<head>` management approach (React Helmet, Next.js Head) |
| **Sitemap generation** | Sitemap specification: which URLs to include/exclude, priority and changefreq values, pagination strategy for large sitemaps, sitemap index structure | Sitemap generation approach: build-time static generation, server-side dynamic generation, or CI/CD pipeline; compression and submission automation to GSC |
| **Internal linking & URL structure** | Crawl depth analysis showing pages >3 clicks from homepage, recommended internal link additions, URL structure guidelines (trailing slash policy, lowercase, hyphens vs underscores) | Navigation component architecture, breadcrumb component, URL routing patterns, redirect implementation strategy (server-side vs client-side) |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "seo-specialist",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like

> Organic traffic compounds predictably because every new page targets a validated keyword gap in a mapped topic cluster, and pillar pages earn backlinks without outreach because they are the definitive

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

### Cross-skills Integration

```mermaid
graph LR
    A[content-strategist] --> B[seo-specialist]
    B --> C[frontend-developer]
    D[growth-engineer] --> B
    B --> E[analytics-engineer]
```
Run skills in the order shown:
```bash
# Chain A: content-strategist → seo-specialist → frontend-developer
# Chain B: growth-engineer → seo-specialist → analytics-engineer

```

## Deliberate Practice

```mermaid
graph LR
    A[Formulate<br/>thesis] --> B[Test in<br/>market] --> C[Study<br/>outcome] --> D[Refine<br/>mental model] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Write a strategy memo for a past business event; compare your reasoning to what actually happened | Monthly |
| **Competent** | Write 3 strategies for the same goal with different constraints; debate which wins | Quarterly |
| **Expert** | Reverse-engineer a competitor's strategy from public information; validate against their next move | Quarterly |
| **Master** | Board-level strategy for a company in a different industry; present to a peer CEO for feedback | Semi-annually |

**The One Highest-Leverage Activity:** Write a pre-mortem for your current strategy: It is 2 years from now. Our strategy failed. Why?

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "SEO is just keywords — stuff them and rank" | Thin content without E-E-A-T triggers helpful content updates that erase 40-90% of traffic overnight — $10K-$500K/month in lost revenue during 3-12 month recovery. |
| "We'll buy 500 backlinks for $2K — fast ranking boost" | Purchased backlinks trigger spam detection — recovery costs $10K-$100K in consultant fees plus 3-12 months of lost rankings and revenue. |
| "Page speed is an engineering problem — not SEO's concern" | Every 100ms delay costs $2.5K/month per $100K revenue — $25K-$210K/year in recoverable revenue from deferred speed optimization. |
| "Googlebot can render JavaScript — it's fine" | JS-rendered content indexes 2-4 weeks after HTML — you lose ranking windows for every content change and fall behind faster competitors. |
| "More pages targeting the same keyword means more coverage" | Keyword cannibalization splits ranking signals across pages — $5K-$20K/month per cannibalized cluster in lost traffic that one authoritative page would capture. |

## Best Practices
**(STANDARD)**

1. **Fix technical SEO fundamentals before investing in content.** Crawl budget waste, broken internal links, missing canonical tags, slow server response times, and poor mobile usability undermine every piece of content you publish. Run a full technical audit (Screaming Frog, Sitebulb, or Google Search Console) and fix crawlability, indexability, and performance issues first. Content built on a broken foundation gets 30-50% less organic traffic.

2. **Target search intent, not keywords.** A keyword tells you what people type. Search intent tells you what they want: informational (learn something), navigational (find a specific site), commercial (research before buying), transactional (buy now). Map every page to ONE intent type. A page that tries to serve informational and transactional intent simultaneously serves neither well.

3. **Build a topical authority map, not a keyword list.** Google's algorithms evaluate whether your site demonstrates comprehensive expertise on a topic, not whether you rank for isolated keywords. For each core topic, create a pillar page (comprehensive guide) surrounded by cluster content (specific subtopics), all interlinked. A site with 50 articles on related subtopics outperforms a site with 50 unrelated articles targeting high-volume keywords.

4. **Monitor Core Web Vitals as ranking signals and user experience metrics.** LCP (Largest Contentful Paint) should be under 2.5s, FID (First Input Delay) under 100ms, CLS (Cumulative Layout Shift) under 0.1. These aren't just SEO metrics — they correlate with bounce rate, conversion rate, and revenue. Fix performance before chasing backlinks.

5. **Implement structured data (Schema.org) for rich results eligibility.** FAQ schema, HowTo schema, Article schema, Product schema, Review schema, and BreadcrumbList schema all enable rich results in SERPs that increase CTR by 5-30%. Validate with Google's Rich Results Test. Structured data is one of the highest-ROI SEO investments: hours to implement, years of benefit.

6. **Build backlinks through value creation, not outreach volume.** The most effective link-building strategies: original research/ data studies (journalists cite data), free tools/calculators (users embed), comprehensive guides (referenced as "the definitive resource"), and expert roundups (contributors share). One data study that earns 50 organic backlinks is worth more than 500 cold outreach emails that earn 5.

7. **Audit and consolidate thin or duplicate content regularly.** Pages with < 300 words of unique content, pages targeting near-identical keywords, and pages with zero organic traffic after 12 months dilute your site's quality signals. Consolidate thin pages into comprehensive resources (301 redirect), delete truly valueless pages (410 or 404), or improve content to meet quality thresholds. Pruning 20% of low-quality pages often increases traffic to the remaining 80%.

8. **Use log file analysis to understand actual crawl behavior.** Google Search Console shows what Google indexed, not what it crawled and discarded. Log file analysis reveals: which pages Google crawls most, which important pages are crawled rarely, and where crawl budget is wasted on low-value URLs (filter pages, faceted navigation, parameter URLs). Optimize crawl budget allocation before it becomes a bottleneck.

9. **Track SEO performance by segment, not aggregate traffic.** "Organic traffic up 15%" hides that your blog traffic is up 40% while your product pages are down 10%. Segment by: page type (blog, product, category, landing), intent (informational, commercial, transactional), and conversion value. A 5% increase in commercial-intent traffic often drives more revenue than a 20% increase in informational traffic.

10. **Run SEO as a continuous process, not a project.** SEO is not "we did an audit and fixed everything." Algorithm updates (3,000+/year), competitor content (published daily), and changing user behavior mean SEO requires ongoing investment. Establish a monthly audit cadence: technical health check, content performance review, backlink profile monitoring, and competitor movement tracking.

## Anti-Patterns
**(STANDARD)**

- **A Google algorithm update can erase 40-90% of your organic traffic overnight.** Core updates, helpful content updates, and spam updates hit sites with thin content, aggressive monetization, or poor UX disproportionately. An ecommerce site doing $200K/month from organic traffic can drop to $20K-$120K/month after one update — and recovery takes 3-12 months. **Total cost: $10K-$500K/month in lost revenue during ranking recovery.** Diversify traffic sources (email, paid, social) so no single channel exceeds 50% of revenue, and maintain content quality above Google's E-E-A-T bar continuously — not just after a penalty.
- **Keyword cannibalization silently bleeds $5K-$20K/month in lost rankings.** When 3 blog posts target the same keyword ("best project management software"), they split authority and all rank worse than one authoritative page would. A page ranking #4 instead of #1 captures ~8% of clicks vs. ~28% — losing 20% of potential traffic on a $25K/month keyword. **Total cost: $5K-$20K/month per cannibalized keyword cluster.** Audit with Search Console's query report — if multiple URLs rank for the same high-value query, consolidate into one comprehensive page and 301-redirect the others.
- **Every 100ms of page load delay costs an ecommerce site ~$2.5K/month in lost conversions per $100K/month revenue.** At 2.5s load time vs. 1.5s, conversion rates drop ~7%. For a $1M/month ecommerce operation, that's $17.5K/month — $210K/year — in recoverable revenue. **Total cost: $2.5K per 100ms delay per $100K/month revenue; $25K-$210K/year for typical ecommerce.** Run Lighthouse CI in your pipeline with a Performance score ≥ 90 gate; treat page speed as an ongoing engineering investment, not a one-time optimization.
- **A bad backlink profile penalty costs $10K-$100K in recovery and 3-12 months of lost traffic.** Buying 500 backlinks for $2K sounds cheap — until Google's spam detection flags your domain. Disavowing, removing, or replacing toxic links costs $10K-$50K in SEO consultant fees, and rebuilding lost rankings takes months. **Total cost: $10K-$100K recovery cost + 3-12 months lost revenue.** Never buy links; earn them through content worth linking to. Audit your backlink profile quarterly with Ahrefs or Semrush and proactively disavow toxic domains before Google penalizes you.
- **JavaScript-rendered content** that Googlebot CAN render is still indexed ~2-4 weeks after HTML content. If critical content (H1, body text, internal links) only exists in the JS bundle, you lose 2-4 weeks of ranking every time it changes. SSR or prerendering is non-negotiable for SEO-critical content.
- **`rel="canonical"` across domains** only works as a HINT, not a directive. Cross-domain canonicals are treated as suggestions; Google may choose a different canonical version. For true de-duplication, use `noindex` on duplicates, not cross-domain canonicals.
- **Core Web Vitals data** in Search Console is the 75th percentile of real-user Chrome UX Report data, NOT lab data from Lighthouse. Lighthouse says your LCP is 1.2s, but real users on 3G in rural areas experience 4.5s. Only the 4.5s matters.
- **Redirect chains** (A → B → C) lose ~10% of link equity per hop AND add 200-600ms latency per redirect. A chain of 5 redirects costs 1-3 seconds of load time and ~40% link equity loss. Fix intermediate redirects to point directly to the final destination.
- **Hreflang tags** with incorrect language+country codes silently fail. `en-uk` is invalid (correct: `en-gb`). `pt-br` is valid. Missing reciprocal tags (page A points to B, but B doesn't point back to A) causes Google to ignore all hreflang annotations on both pages.
- **Site migration or rebrand without a comprehensive 301 redirect map.** An ecommerce business migrates from `oldsite.com` to `newsite.com` — 15,000 product URLs, 2,000 category pages, and 500 blog posts change structure. The dev team sets up a wildcard redirect and calls it done, but Google treats wildcard redirects as soft 404s when the destination doesn't match the original content's intent. Rankings collapse within 4-6 weeks, organic traffic drops 60-85%, and recovery requires a URL-by-URL redirect audit plus a reconsideration timeline of 6-18 months. **Total cost: $50K-$500K in lost revenue during the ranking recovery window, plus $20K-$100K in SEO consultant remediation fees.** Map every indexed URL to its new destination with a 1:1 301 redirect BEFORE migration, verify with Screaming Frog post-launch, and monitor Search Console coverage reports daily for the first 90 days.

- **What:** Chasing algorithm updates with "SEO hacks" instead of building sustainable quality. **Why:** Google runs 3,000+ algorithm updates per year. Each "hack" works for 3-6 months before the next update neutralizes it. Meanwhile, you've accumulated technical debt (spammy backlinks, keyword-stuffed content, doorway pages) that takes 6-12 months to clean up. The cycle of hack → penalty → recovery costs more than doing it right from the start. **Instead:** Invest in E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness): author bios with credentials, cited sources, original research, and transparent about pages. Quality survives algorithm updates; hacks don't.

- **What:** Building backlinks at any cost — buying links, PBNs, comment spam, article directories. **Why:** Google's Penguin algorithm and manual actions team actively detect and penalize link schemes. A manual action can remove your entire domain from search results for 3-12 months. Recovery requires disavowing every toxic link (months of work) and filing a reconsideration request that may or may not be approved. **Instead:** Earn links through linkable assets: original research (data studies, surveys, industry benchmarks), free tools, definitive guides, and expert contributions to reputable publications. One earned link from a .edu or major publication is worth 10,000 spam links and carries zero penalty risk.

## Production Checklist
**(STANDARD)**

Before any SEO deliverable leaves this skill, verify:

- [ ] Technical SEO audit completed: crawlability, indexability, site speed, mobile friendliness, structured data
- [ ] robots.txt, XML sitemap, and canonical tags verified and functioning correctly
- [ ] Core Web Vitals measured and within thresholds: LCP < 2.5s, FID < 100ms, CLS < 0.1
- [ ] Search intent mapped for all target pages — each page serves exactly one intent type
- [ ] Topical authority map created: pillar pages + cluster content with internal linking structure
- [ ] Structured data (Schema.org) implemented for eligible page types and validated via Rich Results Test
- [ ] Content audit completed: thin/duplicate content identified, consolidation plan documented
- [ ] Backlink profile audited: toxic links identified for disavowal, link-building opportunities prioritized
- [ ] Log file analysis (if access available) performed: crawl budget allocation optimized
- [ ] Keyword cannibalization checked — no two pages targeting the same primary keyword
- [ ] Internal linking structure reviewed: important pages within 3 clicks of homepage, orphan pages identified
- [ ] SEO performance segmented by page type, intent, and conversion value — not aggregate traffic
- [ ] Monthly monitoring cadence established: rank tracking, traffic analysis, competitor monitoring, algorithm update review
- [ ] Local SEO (if applicable): Google Business Profile optimized, NAP consistency verified, local citations built

## Verification

- [ ] Run Lighthouse: Performance ≥ 90, SEO = 100, Best Practices ≥ 90
- [ ] Crawl test: `screamingfrog` or `sitebulb` crawl — zero broken links, zero orphan pages, canonical tags correct
- [ ] Structured data: Google Rich Results Test — all pages have valid structured data, zero errors
- [ ] Robots.txt: `googlebot` can access all SEO-critical pages, blocked from admin/login/checkout-success
- [ ] Sitemap: `sitemap.xml` contains all indexable pages, `lastmod` dates are correct
- [ ] Mobile-friendly: Google Mobile-Friendly Test — all pages pass
- [ ] Hreflang: for each locale pair, reciprocal tags exist and point to correct URLs

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## Scale Depth

### Solo/Small Site (< 100 pages, < 10K monthly visits)
- Technical: Google Search Console + free tools (Lighthouse, PageSpeed Insights). Fix critical errors only
- Content: Target 10-20 long-tail keywords with low competition. One pillar page + 5-10 cluster articles
- Backlinks: Earn 5-10 quality backlinks through HARO, guest posts on relevant blogs, and industry directories
- Tools: Google Search Console, Google Analytics, free Ahrefs Webmaster Tools, Screaming Frog (free for < 500 URLs)
- Cadence: Monthly technical health check. Quarterly content audit and refresh
- Deliverable: 1-page SEO plan + monthly traffic report

### Medium (100-1,000 pages, 10K-100K monthly visits)
- Technical: Weekly crawl audits. Core Web Vitals optimization. Structured data at scale. Log file analysis
- Content: 50-200 articles with topical clusters. Content refresh cadence (quarterly for top pages). Programmatic SEO for templates
- Backlinks: Digital PR campaigns. Original research/data studies. Broken link building at scale
- Tools: Ahrefs/Semrush, Screaming Frog, Schema App, SEO testing platform (SearchPilot), rank tracking (AccuRanker)
- Cadence: Weekly rank tracking. Monthly content performance review. Quarterly backlink audit and strategy refresh
- Deliverable: Monthly SEO dashboard + quarterly strategy document + content calendar

### Large (1,000-10,000 pages, 100K-1M monthly visits)
- Technical: Automated crawl monitoring. Edge SEO (CDN-level changes). JavaScript SEO audit. International SEO (hreflang)
- Content: Content operations team. Editorial calendar with 20-50 articles/month. AI-assisted content optimization. Dynamic internal linking
- Backlinks: Dedicated digital PR team. Industry partnerships. Newsjacking. Brand mention reclamation at scale
- Tools: Enterprise SEO platform (Botify, Conductor, BrightEdge), custom dashboards, A/B testing for SEO, AI content tools
- Cadence: Daily rank monitoring. Weekly content performance. Monthly strategy review. Quarterly board presentation
- Deliverable: Monthly SEO business review + quarterly strategy + annual SEO roadmap

### Enterprise (10,000+ pages, 1M+ monthly visits)
- Technical: Custom crawl infrastructure. Automated issue detection and remediation. Multi-region, multi-language SEO. Faceted navigation optimization
- Content: Multi-team content operations. Content strategy by business unit. AI-generated content with human editorial review
- Backlinks: Brand-level digital PR. Industry-defining research. Strategic partnerships. M&A SEO due diligence
- Tools: Custom SEO platform, data warehouse integration, ML-powered insights, enterprise CDN with edge SEO
- Cadence: Real-time monitoring. Weekly cross-functional sync. Monthly executive review. Quarterly board strategy
- Deliverable: Real-time SEO dashboard + monthly executive summary + quarterly board presentation + annual strategy + M&A SEO playbook

## Error Decoder
**(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Organic traffic dropped 60% overnight; no recovery after 3 months | Google manual action for unnatural backlinks. Site was buying links from PBNs for 18 months. Manual action page in Search Console confirmed the penalty. | Disavow all toxic backlinks (use Ahrefs/Semrush backlink audit). File reconsideration request with detailed documentation of link removal efforts. Expect 2-6 months for recovery after approval. | Bought backlinks have a 100% eventual penalty rate. |
| 500 product pages indexed but only 50 get organic traffic | Crawl budget wasted on faceted navigation URLs, parameterized URLs, and filter combinations (e.g., /products?color=red&size=large&sort=price). Google crawled 450 noise pages and missed 50 valuable pages. | Implement canonical tags on faceted URLs pointing to the main product page. Use robots.txt to block crawl of parameter combinations. Add noindex to thin filter pages. Consolidate crawl budget toward valuable pages. | Google doesn't index what you want; it indexes what you let it crawl. |
| Competitor outranked you for your primary keyword despite having worse content | Competitor has stronger domain authority (DR 70 vs. your DR 30) because they've been building quality backlinks for 5 years. Content quality alone doesn't overcome a 40-point authority gap. | Build topical authority through cluster content. Earn backlinks through original research and industry partnerships. Internal linking from high-authority pages to target pages. Expect 12-18 months to close a significant authority gap. | Domain authority is cumulative — you can't sprint past someone who's been running for 5 years. |
| Traffic flat for 12 months despite publishing 100 new articles | Content published without search intent mapping. Articles target keywords with no search volume, or target the wrong intent (informational article targeting a transactional keyword). Google doesn't rank content that doesn't match what searchers want. | For each article, search the target keyword and analyze the top 3 results: what intent do they serve? What format (list, guide, comparison, tool)? What comprehensiveness level? Match or exceed the dominant format and intent. | Google doesn't rank your content; it ranks the best answer to the searcher's question. |
| Site migration (HTTP → HTTPS) caused 40% traffic loss | Missing 301 redirects from HTTP to HTTPS. Google indexed both versions as separate sites, splitting link equity. Canonical tags missing or pointing to HTTP on HTTPS pages. | Audit all redirects: every HTTP URL must 301 to its HTTPS equivalent. Verify canonical tags all point to HTTPS. Update XML sitemap to HTTPS only. Submit change of address in Search Console. | Site migrations without redirect mapping are self-inflicted SEO disasters. |
| Core Web Vitals "passed" in lab tests but failing in field data (CrUX) | Lab tests (Lighthouse, PageSpeed Insights "lab data") run on powerful dev machines with fast connections. Field data (Chrome User Experience Report) represents real users on slow mobile connections with CPU-constrained devices. | Optimize for the 75th percentile of real users, not your MacBook Pro. Use CrUX data in Search Console and PageSpeed Insights "field data" tab. Test on emulated Moto G4 with 3G throttling. Fix LCP by optimizing server response time, render-blocking resources, and image loading. | Your users don't have your laptop. |

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
- **When NOT to Use This Skill (Overkill)**: See [when-not-to-use.md](references/when-not-to-use.md)

