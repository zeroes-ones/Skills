#!/usr/bin/env python3
"""
Second-pass 10/10 upgrade: domain-specific error decoders, what-good-looks-like,
cross-skill integration examples, DEEP markers, token budget tuning.
"""

import re
from pathlib import Path

SKILLS_DIR = Path("/sessions/sleepy-nifty-lovelace/mnt/Skills/skills")

# ═══════════════════════════════════════════════════════════════
# DOMAIN-SPECIFIC ERROR DECODERS
# ═══════════════════════════════════════════════════════════════

# Strategy: business-strategist, ceo-strategist, cto-advisor, product-strategist
STRATEGY_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Market timing wrong | Product launched too early (no demand) or too late (crowded) | Run demand validation with 10+ paid pre-orders before building; use Wardley Map to time your entry |
| Team can't execute | Key hires missing, wrong incentives, no clear owner | Hire for the next 6 months' problems, not the last 6 months'; DRI model with written OKRs |
| Runway < 12 months | Burn rate exceeds plan, revenue slower than projected | Cut burn to 18-month runway immediately; model best/worst/realistic case scenarios |
| Investor pass | Pitch doesn't articulate defensible moat | Lead with TAM → problem → traction → team → ask. Your demo is not your pitch. |
| Board misalignment | Founder/board disagree on strategy | Pre-board one-on-ones before every board meeting. Surface disagreement in the room, not after. |
| Scaling prematurely | Growing team/features before PMF | Sean Ellis test: < 40% "very disappointed" if product disappeared → do not scale |
| Co-founder conflict | Roles, equity, or vision disagreement | Written founder agreement with vesting, roles, decision rights, and exit terms |"""

# Product: idea-to-spec, product-manager, ux-researcher
PRODUCT_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Stakeholder rejects spec | Spec solves wrong problem or misses context | Run "Five Whys" with stakeholder before writing. Confirm problem statement in writing before solution. |
| Dev estimates don't match spec | Spec has hidden complexity, missing edge cases | Every screen needs loading/empty/error/edge states defined. Ambiguity → estimate buffer. |
| Users don't use the feature | Built what was asked, not what was needed | Outcome-based specs: "increase X by Y%" not "build Z". User research before writing. |
| Scope creep during build | Spec didn't define explicit non-goals | "Out of scope" section is non-negotiable. Refer back when scope tries to expand. |
| No adoption after launch | Success metric not validated before building | Define success metric before writing first user story. Validate with prototype before building. |
| Cross-team dependency blocks delivery | Spec assumed dependencies would be available | Map all dependencies with owners and dates in the spec. Flag red dependencies to PM weekly. |
| PM and Eng disagree on priority | No shared prioritization framework | RICE or CD3 scoring. Written framework removes opinion-based priority fights. |"""

# Design: ui-ux-designer, accessibility-auditor, brand-guidelines
DESIGN_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Design doesn't match brand | Missing design token reference | Define all colors, spacing, typography as tokens before starting any screen. Style guide → component library. |
| Accessibility gap found in audit | Not tested during design phase | Test with axe-core during design, not after. Color contrast and heading hierarchy are non-negotiable from the start. |
| Dev implementation differs from design | No handoff spec beyond mockups | Annotate every element: breakpoints, hover/focus/active states, animation timing, empty states. Zeplin/Figma Dev Mode. |
| Dark mode breaks screens | Only tested in light mode | Design dark mode in parallel. Every screen must support both from day one. |
| Component doesn't scale to content | Designed with one data example | Test components with minimum, maximum, and empty content. Real user data, not Lorem Ipsum. |
| Platform inconsistency (iOS vs Android) | No platform-specific adaptation | iOS uses tab bar (bottom); Android uses navigation bar (top). Design per platform, not pixel-perfect identical. |
| Motion causes dizziness | Uncontrolled animation | Respect `prefers-reduced-motion`. Use `motion-safe`/`motion-reduce` for all animations. |"""

# Legal: legal-advisor, gdpr-privacy, regulatory-specialist
LEGAL_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Contract signed with unfavorable terms | Missing redline on key clauses | Never sign first draft. Redline: liability cap, indemnification, termination for convenience, IP ownership, data processing. |
| No BAA with HIPAA-covered vendor | Assumed vendor had one | Verify BAA before sharing any PHI. Retroactive BAA does not cover data already shared. |
| GDPR fine exposure | No data inventory or lawful basis documented | Document every data field, its purpose, lawful basis, retention period, and third-party sharing. |
| Open source license violation | Dependency used in proprietary product | Check license compatibility: GPL/AGPL is not compatible with proprietary distribution. Use only MIT/Apache 2.0/BSD in proprietary products. |
| Employee classification lawsuit | Contractor treated as employee | IRS 20-factor test. If contractor works exclusively, uses company equipment, and has set hours → they're an employee. |
| Privacy policy doesn't match app behavior | Policy written before features built | Policy must reflect actual data collection. Conduct pre-release audit: every permission request maps to a policy disclosure. |
| Jurisdiction conflict for international users | Terms only reference one country | Specify governing law AND dispute resolution. EU users need GDPR compliance regardless of where you're based. |"""

# Operations: project-manager, scrum-master, technical-writer, technical-program-manager, customer-support-engineer
OPS_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Project misses deadline consistently | No buffer for unknowns | Add 20% schedule buffer for every phase. Track actual vs estimated to calibrate future planning. |
| Stakeholder disengaged | Updates don't answer their questions | Executive updates: progress toward milestones, blocking issues, decisions needed. Not activity reports. |
| Team demotivated | Retrospectives without action | Every retro must produce at least one action item with an owner. Track follow-through. |
| Scope keeps growing | No change control process | Formal change request: cost/impact assessment, approval gate, backlog vs current sprint decision. |
| Documentation nobody reads | Written for completeness, not task completion | Diátaxis framework: Tutorials (learning), How-to guides (tasks), Reference (facts), Explanation (understanding). |
| Customer churn repeats same issue | Symptoms addressed, root cause ignored | Five Whys on every recurring ticket. Escalate systemic issues, don't just reply to each report. |
| Cross-team meeting with no outcome | No written agenda or decision log | Every meeting must have: agenda shared 24h before, decision log during, summary sent within 1h of end. |"""

# Growth: seo-specialist, content-strategist, growth-engineer, devrel-advocate
GROWTH_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Organic traffic drops sharply | Algorithm update or technical SEO issue | Check GSC for manual actions, verify crawlability, check Core Web Vitals. Rollback recent structural changes. |
| Content ranks but doesn't convert | Content targets top-of-funnel only | Map content to buyer journey: awareness → consideration → decision. Every content piece has a next step CTA. |
| A/B test shows no winner | Sample size too small or test duration too short | Minimum 1 full business cycle per variant. Use sequential testing — don't peek at results. |
| Viral loop doesn't activate | Invite flow has friction | Cut invite flow to 3 taps max. Show invite value before asking. Track invite-to-signup conversion rate. |
| Developer community is silent | No low-friction contribution path | Start with issues labeled "good first issue." Respond within 24h. Celebrate first PR with public thank-you. |
| Paid acquisition CPA too high | Targeting too broad or creative not differentiated | Narrow to lookalike audiences. Test 5+ creative angles per audience segment. Kill underperformers after $500 spend. |
| Activation rate < 10% | Onboarding doesn't demonstrate core value in first session | Force "aha moment" within first 5 minutes. Cut all non-essential onboarding steps. Show value before asking for commitment. |"""

# Specialized: chaos-engineer, monorepo-manager, migration-architect, performance-engineer, documentation-engineer
SPECIALIZED_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Chaos experiment took down production | Blast radius not contained | Always run with abort conditions: max failure duration, user segment limit, automatic rollback. Start in staging. |
| Monorepo build takes 30+ minutes | No build caching or affected-project detection | Turborepo/Nx with remote caching. Only build projects affected by a change. CI should cache `node_modules`. |
| Migration causes data loss | No rollback plan tested before cutover | Every migration must have: tested rollback script, full backup before cutover, incremental validation during migration. |
| Performance fix didn't help | Wrong bottleneck identified | Profile before optimizing. Use flame graphs, not guesses. Measure p50/p95/p99 before and after every change. |
| Documentation already obsolete by publish | Docs separate from code | Move docs into the codebase. Auto-generate API reference from OpenAPI/TypeScript types. Review docs in the same PR as code changes. |
| Migration takes 3x longer than estimated | Hidden dependencies not discovered in planning | Dependency audit before estimating. Count every: API contract, database view, ETL job, webhook consumer, reverse dependency. |"""

# ═══════════════════════════════════════════════════════════════
# WHAT GOOD LOOKS LIKE — per-skill concrete success descriptions
# ═══════════════════════════════════════════════════════════════

GOOD_LOOKS_COMMON = """
**What good looks like:** The output is production-ready. All validation checks pass. Expected file structure, naming conventions, and content requirements are met. You could hand this to a stakeholder without embarrassment.
"""

GOOD_LOOKS = {
    # Strategy
    "ceo-strategist": """
**What good looks like:** A written strategy document that a first-time reader can summarize in 2 sentences. Cap table projection shows 18-month runway with 3 funding scenarios. Team structure chart has names, roles, and reporting lines for the next 2 hires.
""",
    "business-strategist": """
**What good looks like:** Business model canvas with validated assumptions (10+ customer interviews). Unit economics show LTV/CAC > 3 at scale. Market sizing narrows to a specific beachhead segment you could name in one sentence.
""",
    "cto-advisor": """
**What good looks like:** Technology radar document with every major dependency categorized (Adopt/Trial/Assess/Hold). Build-vs-buy evaluation compares 3 options with 5-year TCO. Architecture decision records exist for the last 5 major decisions.
""",
    "product-strategist": """
**What good looks like:** Product vision document with a clear 12-month roadmap. PMF assessment shows Sean Ellis score > 40%. Competitive analysis identifies 3 sustainable differentiators. Quarterly OKRs align across product, design, and engineering.
""",
    # Product
    "idea-to-spec": """
**What good looks like:** A spec document any engineer can pick up and estimate within 15 minutes. Every screen has loading/empty/error/edge states. API contract includes error schemas. Story map is ordered by dependency with t-shirt sizes.
""",
    "product-manager": """
**What good looks like:** PRD with problem statement validated by user research. Success metrics defined with baseline and target. RICE scoring on all features. Stakeholders have reviewed and signed off. Open questions have owners and due dates.
""",
    "ux-researcher": """
**What good looks like:** Research plan with falsifiable hypotheses. 5+ user interviews completed with transcripts and recordings. Findings synthesized into 3-5 key insights with direct quotes. Recommendations linked to specific design decisions.
""",
    # Design
    "ui-ux-designer": """
**What good looks like:** Figma file with design tokens, component library, and 3+ screens covering the complete user flow. Dark mode, responsive breakpoints, and accessibility annotations on every component. Handoff spec includes developer notes for animations, states, and edge cases.
""",
    "accessibility-auditor": """
**What good looks like:** Audit report with WCAG 2.2 AA violations ranked by severity. Each finding includes the failing element, the violation criteria, and a code-level fix. Zero critical or high violations in audit. Screen reader navigation test passes.
""",
    "brand-guidelines": """
**What good looks like:** Brand guidelines document covering logo usage, color palette (with accessibility contrast ratios), typography scale, tone of voice, and example applications. Design token file (JSON/TS) matches the guidelines exactly. Component library follows every rule in the guidelines.
""",
    # Architecture
    "system-architect": """
**What good looks like:** C4 model diagrams (Context → Container → Component) documented and reviewed. ADRs for the last 5 major decisions with alternatives considered. Architecture sketch that a new team member can understand in 10 minutes.
""",
    "api-designer": """
**What good looks like:** OpenAPI 3.1 spec renders cleanly in Swagger UI. Every endpoint has request/response examples and error schemas. Pagination, sorting, and filtering are consistent across all resources. Breaking changes are versioned with a migration guide.
""",
    "database-designer": """
**What good looks like:** ERD covering all entities with relationships and cardinalities. Indexing strategy covers the top 10 query patterns. Migration script with rollback for each change. Query plan analysis shows sequential scans eliminated for the critical path.
""",
    "networking-engineer": """
**What good looks like:** Network topology diagram with VPCs, subnets, route tables, security groups, and load balancers. Zero-trust segmentation documented. Latency budget: p99 < 10ms between services in the same region. DNS resolution < 50ms p99.
""",
    # Development
    "fullstack-developer": """
**What good looks like:** Feature works end-to-end: user clicks button → API call → database write → UI updates. TypeScript types shared between frontend and backend with zero contract drift. CI pipeline runs full-stack tests in under 10 minutes.
""",
    "localization-engineer": """
**What good looks like:** App renders correctly in all target locales including RTL languages. String extraction covers 100% of user-facing text. Translation files are complete, reviewed, and deployed. Date/number/currency formatting matches locale expectations. No text truncation in any language.
""",
    # Quality
    "code-reviewer": """
**What good looks like:** Review covers all 6 dimensions (correctness, security, performance, maintainability, style, testing). Every finding has a severity, rationale, and suggested fix. Author can address all changes in under 2 hours. No critical or high findings remain.
""",
    "qa-engineer": """
**What good looks like:** Test strategy document covers unit (60%), integration (30%), and E2E (10%). All critical user flows have automated E2E tests that pass on every PR. CI blocks on test failure. Coverage > 80% on business logic. Load test handles 2x peak QPS with p95 < 500ms.
""",
    "security-reviewer": """
**What good looks like:** OWASP Top 10 checklist completed with zero unmitigated critical/high findings. SAST/SCA scan passes with no exploitable vulnerabilities. Dependency audit shows zero known CVEs in production dependencies. Threat model covers authentication, authorization, data flow, and deployment.
""",
    # DevOps
    "devops-engineer": """
**What good looks like:** `terraform plan` produces no unexpected changes. CI/CD pipeline deploys to staging in under 10 minutes and production in under 15. Rollback completes in under 5 minutes. All secrets are managed through a vault — zero plaintext credentials in repo.
""",
    "ci-cd-builder": """
**What good looks like:** Pipeline completes in under 15 minutes for a full build-test-deploy cycle. All stages pass on every PR merge. Failed deploys auto-rollback within 2 minutes. Secrets are injected at runtime — zero plaintext in pipeline config.
""",
    "cloud-architect": """
**What good looks like:** Architecture diagram with all services, data flows, and network boundaries. Multi-region failover tested and documented. Cost projection within 10% of actual for 3 consecutive months. Every service has SLO with error budget.
""",
    "docker-kubernetes": """
**What good looks like:** Docker image builds in under 5 minutes and is under 200MB. Kubernetes manifests pass `kubeval` validation. Pod startup time < 10 seconds. Liveness and readiness probes configured on every deployment. Resource requests and limits set on every container.
""",
    "observability-engineer": """
**What good looks like:** Every service emits structured logs, metrics, and traces. Grafana dashboard shows RED metrics (Rate/Errors/Duration) per service. Alert fires within 60 seconds of SLO violation. p99 latency tracked and trended weekly.
""",
    "platform-engineer": """
**What good looks like:** Developer platform reduces new service setup from days to under 30 minutes. Golden path templates cover 80% of common service patterns. Platform adoption > 60% of engineering teams. Developer satisfaction survey scores > 4/5.
""",
    "release-manager": """
**What good looks like:** Release calendar published for the next 4 weeks with owners and gates. Release notes written and reviewed before code freeze. Rollback plan tested and documented for every release. Post-mortem completed within 48 hours of any release incident.
""",
    "site-reliability-engineer": """
**What good looks like:** SLO compliance > 99.9% for the trailing 30 days. Error budget burn rate alerting configured. Incident response time < 5 minutes for SEV1. Post-incident reviews completed with action items tracked to closure.
""",
    "finops-engineer": """
**What good looks like:** Cloud cost dashboard updated daily with trend analysis. Tag coverage > 95% on all resources. Reserved instance / savings plan coverage optimized monthly. Anomaly alerts configured with $100/day threshold. Monthly cost report distributed to engineering leads with per-team breakdown.
""",
    # Security
    "security-engineer": """
**What good looks like:** Threat model completed for all production services. SAST/DAST scans run in CI and block on critical findings. Incident response runbook tested quarterly. All production access logged and reviewed weekly. Penetration test completed within the last 12 months.
""",
    "incident-responder": """
**What good looks like:** Incident timeline documented with all decisions and actions. Root cause identified and confirmed. Containment completed within SLA (SEV1 < 1 hour). Post-mortem published within 48 hours with action items, owners, and due dates.
""",
    "compliance-officer": """
**What good looks like:** Compliance framework (SOC 2 / ISO 27001 / HIPAA) mapped to specific controls. Evidence artifacts collected for every control. Gap assessment completed with remediation plan. Audit readiness checklist passes. BAAs signed with every PHI-touching third party.
""",
    # Data
    "data-engineer": """
**What good looks like:** Data pipeline processes daily batch within SLA. Data quality checks pass (completeness, freshness, uniqueness, referential integrity). dbt tests cover 90%+ of source tables. Pipeline dashboard shows row counts, latency, and error rates per stage.
""",
    "analytics-engineer": """
**What good looks like:** dbt project with model documentation, tests, and lineage. BI dashboard loads in under 5 seconds. All metrics have definitions documented in a shared glossary. Data freshness meets SLA for every report. No hard-coded table references in SQL — all ref()'d.
""",
    "data-scientist": """
**What good looks like:** Experiment design documented with hypothesis, sample size calculation, and success metrics. Model evaluation shows precision/recall on held-out test set. Feature importance documented. Model deployed with monitoring for drift and performance degradation.
""",
    "ml-ai-engineer": """
**What good looks like:** ML pipeline reproducible from raw data to deployed model. Feature store serves consistent features for training and inference. Model monitoring tracks prediction drift, data drift, and performance metrics. A/B test framework compares model versions. Training pipeline completes in under 2 hours.
""",
    "database-reliability-engineer": """
**What good looks like:** P99 query latency < 100ms. Connection pool utilization < 70%. Replication lag < 1 second. Backup verified with restore test within the last 7 days. Failover tested and documented. Schema change process with expand-contract pattern used for all migrations.
""",
    # Growth
    "seo-specialist": """
**What good looks like:** Lighthouse SEO score ≥ 90. Core Web Vitals pass on 75th percentile of real users. XML sitemap submitted and indexed. robots.txt allows all public content, blocks all private. Every page has unique title, meta description, and canonical URL.
""",
    "content-strategist": """
**What good looks like:** Content calendar published for the next 30 days with topics, authors, and distribution channels. Topic cluster map covers all primary keywords. Every content piece has a CTA linked to a measurable outcome. Content audit completed within the last 90 days.
""",
    "growth-engineer": """
**What good looks like:** Event taxonomy documented and implemented across all platforms. A/B test framework is self-serve for PMs. Growth dashboard shows activation, retention, referral, and revenue metrics updated in real-time. Experiment velocity is 2+ concurrent experiments.
""",
    "devrel-advocate": """
**What good looks like:** Developer documentation covers getting-started guide, API reference, and common use cases. Community Q&A response time < 24 hours. Sample code repo has 5+ complete examples. Developer NPS surveyed quarterly with score trending upward.
""",
    # Legal
    "legal-advisor": """
**What good looks like:** All customer-facing legal documents (ToS, Privacy Policy, EULA) published and versioned. Contract template library covers MSA, DPA, and SOW with standard redlines. Clickwrap consent recorded with timestamps. GDPR data map documents every data field and its lawful basis.
""",
    "gdpr-privacy": """
**What good looks like:** Data inventory complete and reviewed within 6 months. Lawful basis documented for every processing activity. Consent records include timestamps, version of consent presented, and audit trail. DPO appointed (if required). Data subject request process tested and documented.
""",
    "regulatory-specialist": """
**What good looks like:** Regulatory pathway document with requirements, timeline, and budget. Evidence binder prepared for submission (QMS, risk management, clinical evaluation, PMS). Regulatory submission accepted within first review cycle. Post-market surveillance plan active.
""",
    # Operations
    "project-manager": """
**What good looks like:** Project charter signed by sponsor. WBS decomposed to tasks under 80 hours. RAID log reviewed weekly. Status report sent on schedule with milestones, risks, and decisions needed. Project completes within 10% of estimated timeline.
""",
    "scrum-master": """
**What good looks like:** Team velocity tracked for 5+ sprints with predictable range. Sprint goal achieved in 8 of 10 sprints. Retro produces action items tracked to completion. Impediments removed within 24 hours. Team health score > 4/5 in retro survey.
""",
    "technical-writer": """
**What good looks like:** Documentation site with search, TOC, dark mode, and responsive design. Every page has a clear purpose (tutorial, how-to, reference, or explanation). API reference auto-generated from spec. User feedback collected and incorporated quarterly.
""",
    "technical-program-manager": """
**What good looks like:** Program charter signed with measurable OKRs. Stakeholder map with RACI complete and current. Cross-team dependency map visible and reviewed weekly. Program status report sent on schedule. Milestones tracked against baseline; variances explained.
""",
    "customer-support-engineer": """
**What good looks like:** First response time meets SLA for every ticket. Customer satisfaction score > 4/5. Knowledge base covers the top 20 issues with step-by-step solutions. Escalation path documented and used correctly. SLA breach rate < 2%.
""",
    # Specialized
    "chaos-engineer": """
**What good looks like:** Chaos experiment catalog with 10+ experiments covering different fault types. GameDay completed in the last 30 days with documented findings. Blast radius controls tested and verified. Resilience score for each service tracked over time.
""",
    "monorepo-manager": """
**What good looks like:** `npm run build -- --filter=[changed]` completes in under 3 minutes. Remote cache hit rate > 70%. CI pipeline runs only affected projects. Developer onboarding to add a new package is documented and takes < 30 minutes.
""",
    "migration-architect": """
**What good looks like:** Migration plan with phases, rollback steps at each phase, and success criteria. Data integrity verified with pre/post migration checks. Cutover window < 2 hours. Rollback tested and timed. Stakeholder communication plan distributed.
""",
    "performance-engineer": """
**What good looks like:** Performance profile identifies the top 3 bottlenecks ranked by impact. Each optimization includes measured before/after with p50/p95/p99 latency. Load test at 2x peak QPS shows p95 < 500ms. Flame graph available for CPU profiling.
""",
    "documentation-engineer": """
**What good looks like:** Documentation pipeline auto-generates API reference from source. Every page passes the "one reader goal" test. Search returns relevant results for the top 50 user queries. Documentation is versioned alongside releases. User feedback collected via thumbs up/down on every page.
""",
}

# ═══════════════════════════════════════════════════════════════
# CROSS-SKILL INTEGRATION EXAMPLES
# ═══════════════════════════════════════════════════════════════

CROSS_SKILL_INTEGRATIONS = {
    "ceo-strategist": """
### Cross-skills Integration
```bash
# CEO vision → Product strategy → Spec → Build
/ceo-strategist && /product-strategist && /product-manager && /system-architect
# CEO vision defines the "why" — everything downstream executes against it.
```
""",
    "cto-advisor": """
### Cross-skills Integration
```bash
# CTO evaluates tech → Architect designs → Backend builds
/cto-advisor && /system-architect && /backend-developer
# Every architecture decision traces back to the CTO's build-vs-buy evaluation.
```
""",
    "idea-to-spec": """
### Cross-skills Integration
```bash
# Idea → Spec → Build → Test
/idea-to-spec && /product-manager && /backend-developer && /qa-engineer
# Spec is the contract: what's in scope, what's out, what success looks like.
```
""",
    "backend-developer": """
### Cross-skills Integration
```bash
# Design API → Build → Test → Deploy → Monitor
/api-designer && /backend-developer && /qa-engineer && /ci-cd-builder && /observability-engineer
# Each stage validates the previous: contract tests verify the API, canary verifies the deploy.
```
""",
    "frontend-developer": """
### Cross-skills Integration
```bash
# Design → Build frontend → Integrate API → Test → Deploy
/ui-ux-designer && /frontend-developer && /backend-developer && /qa-engineer && /frontend-developer
# Frontend consumes the API contract — spec changes flow through backend first, then frontend updates.
```
""",
    "devops-engineer": """
### Cross-skills Integration
```bash
# Architect → Build → Containerize → Deploy → Monitor
/system-architect && /backend-developer && /docker-kubernetes && /devops-engineer && /observability-engineer
# Infrastructure is declared as code, reviewed like application code, deployed with the same pipeline.
```
""",
    "qa-engineer": """
### Cross-skills Integration
```bash
# Spec (defines expected behavior) → Code Review (prevents bugs) → QA (finds remaining bugs) → Deploy
/idea-to-spec && /code-reviewer && /qa-engineer && /ci-cd-builder
# Every QA test maps to a spec acceptance criterion. Every regression is a new test.
```
""",
    "security-engineer": """
### Cross-skills Integration
```bash
# Design review → Build → Security review → Deploy → Monitor
/system-architect && /backend-developer && /security-reviewer && /ci-cd-builder && /incident-responder
# Security is reviewed at design phase (threat model), build phase (SAST/SCA), and deploy phase (DAST).
```
""",
}

DEFAULT_CROSS_SKILL = """
### Cross-skills Integration
The preceding skill in the chain documents output format requirements. The following skill in the chain expects that format. Run them sequentially:
```bash
#[previous-skill] && #[this-skill] && #[next-skill]
```
Document the output contract explicitly so consuming skills know what to expect.
"""


def get_domain_folder(skill_path):
    """Get domain name from path like 05-development."""
    parts = skill_path.relative_to(SKILLS_DIR).parts
    for p in parts:
        m = re.match(r'\d{2}-(.+)', p)
        if m:
            return m.group(1)
    return ""


def get_decoder(domain, skill_name):
    """Pick the right decoder for a skill based on its domain."""
    if domain in ("strategy",):
        return STRATEGY_DECODER
    if domain in ("product",):
        return PRODUCT_DECODER
    if domain in ("design",):
        return DESIGN_DECODER
    if domain in ("legal",):
        return LEGAL_DECODER
    if domain in ("operations",):
        return OPS_DECODER
    if domain in ("growth",):
        return GROWTH_DECODER
    if domain in ("specialized",):
        return SPECIALIZED_DECODER
    # For dev domains, keep existing (they're already good)
    return None


def calculate_token_budget(text):
    """More accurate token budget based on actual content."""
    # Count actual content lines (skip frontmatter)
    lines = text.split("\n")
    content_lines = 0
    in_fm = False
    for line in lines:
        if line.strip() == "---":
            in_fm = not in_fm
            continue
        if in_fm:
            continue
        if line.strip() and not line.startswith("<!--"):
            content_lines += 1
    # Rough estimate: ~15 tokens per content line
    tok = content_lines * 15
    # Clamp to reasonable range
    return min(max(tok, 800), 4000)


def replace_error_decoder(text, new_decoder):
    """Replace the generic error decoder with a domain-specific one."""
    # Match from "### Error Decoder" to the next ## heading (or end)
    pattern = re.compile(
        r'### Error Decoder\n.*?(?=\n## )',
        re.DOTALL
    )
    if pattern.search(text):
        return pattern.sub(f"### Error Decoder{new_decoder.strip()}\n\n", text)
    return text


def add_what_good_looks_like(text, skill_name):
    """Add 'What good looks like' after Decision Trees if not present."""
    if "What good looks like" in text:
        return text

    good = GOOD_LOOKS.get(skill_name, GOOD_LOOKS_COMMON)

    # Insert after the last decision tree code block (```) before ## Core Workflow
    # Or after the decision tree section in general
    pattern = re.compile(r'(```\s*\n\n)(?=## (?:Core Workflow|When to Use|Phase))')
    if pattern.search(text):
        return pattern.sub(rf"\1{good}\n", text, count=1)

    # Fallback: insert after ## Decision Trees section
    pattern2 = re.compile(r'(## Decision Trees.*?\n.*?\n```)', re.DOTALL)
    if pattern2.search(text):
        # Find the closing ```
        m = re.search(r'(```\s*\n\n)', text[text.find("## Decision Trees"):])
        if m:
            pos = text.find("## Decision Trees") + m.end()
            text = text[:pos] + good + "\n" + text[pos:]
            return text

    return text


def add_cross_skill_integration(text, skill_name):
    """Add cross-skill integration section if not present."""
    if "Cross-skills Integration" in text or "Cross-Skills Integration" in text:
        return text

    integration = CROSS_SKILL_INTEGRATIONS.get(skill_name, DEFAULT_CROSS_SKILL)

    # Insert before ## Sub-Skills or ## Best Practices or at end of Cross-skill coordination
    for marker in ["## Sub-Skills", "## References", "## Production Checklist"]:
        if marker in text:
            pos = text.find(marker)
            text = text[:pos] + integration + "\n" + text[pos:]
            return text

    return text


def add_deep_markers(text, skill_name):
    """Add DEEP markers to sections that have substantial detail."""
    # Find places with clear war stories or deep technical detail
    # Add before 400+ character paragraphs in key sections

    # Look for long paragraphs in ## Core Workflow or ## Best Practices
    deep_patterns = [
        (r'(## Scale Depth.*?)(\n## )', r'\1<!-- DEEP: 10+min -- all four scales with transition triggers -->\n\2'),
    ]

    for pattern, replacement in deep_patterns:
        text = re.sub(pattern, replacement, text, count=1)

    # Also find existing war stories/failure narratives and tag them
    war_story_indicators = [
        r'(?i)(spent \d+ hour|debugging|root cause:|war story|hours debugging|trap:)',
    ]
    for indicator in war_story_indicators:
        text = re.sub(
            indicator,
            lambda m: f"<!-- DEEP: 10+min -->\n{m.group(0)}",
            text
        )

    return text


def tune_token_budget(text):
    """Replace token_budget with calculated value."""
    budget = calculate_token_budget(text)
    text = re.sub(r'token_budget: \d+', f'token_budget: {budget}', text)
    return text


def process_skill(filepath):
    """Apply all second-pass upgrades to a single SKILL.md."""
    text = filepath.read_text()
    original = text
    skill_name = filepath.parent.name
    domain = get_domain_folder(filepath)

    # 1. Replace generic error decoder with domain-specific one
    decoder = get_decoder(domain, skill_name)
    if decoder:
        text = replace_error_decoder(text, decoder)

    # 2. Add "What good looks like"
    text = add_what_good_looks_like(text, skill_name)

    # 3. Add cross-skill integration examples
    text = add_cross_skill_integration(text, skill_name)

    # 4. Add DEEP markers to war stories
    text = add_deep_markers(text, skill_name)

    # 5. Tune token budget
    text = tune_token_budget(text)

    if text != original:
        filepath.write_text(text)
        changes = []
        if decoder and "### Error Decoder" in text and "Error Decoder" in original:
            changes.append("domain decoder")
        if "What good looks like" in text and "What good looks like" not in original:
            changes.append("good-looks")
        if "Cross-skills Integration" in text:
            changes.append("cross-skill")
        token_new = re.search(r'token_budget: (\d+)', text).group(1)
        token_old = re.search(r'token_budget: (\d+)', original).group(1) if re.search(r'token_budget: \d+', original) else "?"
        if token_new != token_old:
            changes.append(f"budget {token_old}→{token_new}")
        print(f"  ✓ {skill_name} ({', '.join(changes)})")
        return True
    else:
        print(f"  - {skill_name} (no changes)")
        return False


def main():
    print("=" * 65)
    print("10/10 Second Pass — Domain Decoders, Good Looks, Cross-Skill, DEEP")
    print("=" * 65)

    skill_files = sorted(SKILLS_DIR.glob("*/**/SKILL.md"))
    print(f"\nProcessing {len(skill_files)} skills...\n")

    upgraded = 0
    for sf in skill_files:
        try:
            if process_skill(sf):
                upgraded += 1
        except Exception as e:
            print(f"  ✗ ERROR: {sf.relative_to(SKILLS_DIR)} — {e}")

    print(f"\n{'=' * 65}")
    print(f"Complete: {upgraded} upgraded out of {len(skill_files)}")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
