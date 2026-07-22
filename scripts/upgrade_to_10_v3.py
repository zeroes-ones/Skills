#!/usr/bin/env python3
"""
v3 upgrade: Push all 13 domains from 9.0/9.5 to 10/10.
Addresses every specific gap from the domain-by-domain rating.
"""
import re
from pathlib import Path

SKILLS = Path("/sessions/sleepy-nifty-lovelace/mnt/Skills/skills")

# ═══════════════════════════════════════════════════════════════
# 1. STRATEGY — Outcome-oriented What Good Looks Like
# ═══════════════════════════════════════════════════════════════

STRATEGY_GOOD_LOOKS = {
    "ceo-strategist": "**What good looks like:** An investor or new hire reads the strategy document and can explain the company's core thesis, target market, and 12-month priorities in under 60 seconds. Cap table is clean with 18-month runway across 3 funding scenarios. Every key role has a named owner and the next 2 hires are budgeted. Board meeting produces decisions, not debate.",
    "business-strategist": "**What good looks like:** Business model canvas with 10+ customer interviews validating each assumption — you know which bets are confirmed and which are still risky. Unit economics show LTV/CAC > 3 at scale with a clear path to get there. Beachhead segment identified where you can own 30%+ of a $20M+ TAM within 18 months. The strategy document is 3 pages, not 30.",
    "cto-advisor": "**What good looks like:** Technology radar document published and reviewed with the engineering team — every major dependency has a clear Adopt/Trial/Assess/Hold rating with written rationale. The last 3 build-vs-buy decisions are documented with 5-year TCO, alternatives considered, and accepted tradeoffs. A new CTO can read the radar and understand why every technology choice was made within an afternoon.",
    "product-strategist": "**What good looks like:** Product vision document that the entire leadership team can state in one sentence — no ambiguity, no 5-paragraph preamble. Sean Ellis survey shows >40% 'very disappointed' score with statistical significance. Competitive analysis identifies exactly 3 defensible advantages with evidence. OKRs cascade cleanly from product strategy to quarterly engineering goals with measurable targets.",
}

# ═══════════════════════════════════════════════════════════════
# 2. DESIGN — Figma→Code handoff in cross-skill coordination
# ═══════════════════════════════════════════════════════════════

DESIGN_HANDOFF = """

### Design-to-Code Handoff Chain
```bash
# Figma → Design tokens → Component → Implementation → Verify
/ui-ux-designer && /frontend-developer && /qa-engineer
# Every Figma frame has: spacing token, color token, typography token, breakpoint annotation.
# Frontend devs should never guess measurements — if it's not in the handoff, it doesn't exist.

# Brand → Design system → Component library → App
/brand-guidelines && /ui-ux-designer && /frontend-developer
# Brand tokens feed into the design system. Design system tokens are the single source of truth.
# No hardcoded colors or spacing values — every pixel comes from a named token.

# Accessibility → Design → Development → Audit
/accessibility-auditor && /ui-ux-designer && /frontend-developer
# Accessibility requirements are annotated on every Figma frame before handoff.
# Color contrast, heading hierarchy, focus management, and touch targets are non-negotiable.
# Auditor verifies post-implementation — not post-launch.
```
"""

DESIGN_GOOD_LOOKS = {
    "ui-ux-designer": "**What good looks like:** Figma file with every screen annotated with design tokens (spacing, color, typography tokens, not hardcoded values), responsive breakpoints for mobile/tablet/desktop, dark mode variants, and developer notes for every interactive state (hover, focus, active, pressed, disabled, loading, error, empty). A frontend developer can open the file and start coding without asking a single clarifying question.",
    "brand-guidelines": "**What good looks like:** Brand guidelines document that a designer outside your company can pick up and produce an on-brand screen within an hour. Design token file (JSON/TS/CSS custom properties) matches the guidelines byte-for-byte — they're the same truth, not two documents that contradict each other. Every component pattern has examples of correct use, incorrect use, and edge cases.",
    "accessibility-auditor": "**What good looks like:** Audit report with WCAG 2.2 AA violations ranked by severity (Critical/High/Medium/Low). Each finding contains: the failing element, the exact WCAG criteria violated, a code-level fix (not a principle — a specific change), and a screenshot showing the problem. Zero critical or high violations at launch. Screen reader navigation test passes on iOS VoiceOver and Android TalkBack.",
}

# ═══════════════════════════════════════════════════════════════
# 3. ARCHITECTURE — Review-specific What Good Looks Like
# ═══════════════════════════════════════════════════════════════

ARCH_GOOD_LOOKS = {
    "system-architect": "**What good looks like:** Architecture Review Board signs off with zero unresolved critical findings. C4 diagrams (Context → Container → Component → Code) are accurate and up-to-date — a new team member traces the system's data flow from ingress to persistence in under 10 minutes. ADRs for the last 5 major decisions are written, reviewed, and merged. The architecture sketch passes the 'explain to a new hire in 5 minutes' test.",
    "api-designer": "**What good looks like:** OpenAPI 3.1 spec renders cleanly in Swagger UI with no validation warnings. Every endpoint has at least one request example, one response example, and all error schemas documented. A frontend developer can generate a type-safe client from the spec and start integrating without asking a single question about pagination, filtering, sorting, or error handling.",
    "database-designer": "**What good looks like:** ERD covers all entities with named relationships and cardinalities. The 10 most expensive query patterns each have an EXPLAIN plan showing sequential scans eliminated by the chosen index strategy. Migration scripts have both up and down paths tested in CI. The schema survives a production load test at 2x peak QPS without connection pool exhaustion or lock contention.",
    "networking-engineer": "**What good looks like:** Network topology diagram with VPCs, subnets, route tables, security groups, and load balancers — anyone on-call can find the ingress path from CDN to database in under 2 minutes. Zero-trust segmentation is documented and verified: no service can reach another service without explicit policy. p99 latency between colocated services < 5ms. DNS resolution < 50ms p99 from any region.",
}

# ═══════════════════════════════════════════════════════════════
# 4. DEVELOPMENT — Fix generic What Good Looks Like
# ═══════════════════════════════════════════════════════════════

DEV_GOOD_LOOKS = {
    "frontend-developer": "**What good looks like:** Storybook runs with every component rendering in light mode, dark mode, and all interactive states (hover, focus, active, disabled, loading, error). Lighthouse score ≥ 95 across Performance, Accessibility, Best Practices, and SEO. No console errors in production. The bundle ships under 200KB gzipped for initial load, and every page has a measured Core Web Vitals score from lab data before merge.",
    "localization-engineer": "**What good looks like:** The app renders correctly in all 10+ target locales including RTL languages (Arabic, Hebrew) without a single text truncation or layout break. String extraction covers 100% of user-facing text — verified by automated scan that compares source strings to translation files. Date, number, currency, and pluralization formatting matches every locale's expectations (d/m/y vs m/d/y, 1.000 vs 1,000). Translation files are complete, reviewed, and shipped in the same deploy as the code — no lag, no missing strings.",
    "mobile-developer": "**What good looks like:** App builds and runs on both iOS and Android from a single codebase commit. All screens render correctly on the smallest and largest supported device sizes (iPhone SE to Pro Max, Pixel to Galaxy Ultra). No red boxes, crash logs, or ANR reports in the last 100 test sessions. App store review passes on first submission — no guideline violations. Launch-to-interaction time < 2s on a mid-range device (Pixel 6 / iPhone 12).",
}

# ═══════════════════════════════════════════════════════════════
# 5. QUALITY — War stories inline
# ═══════════════════════════════════════════════════════════════

QA_WAR_STORY = """
<!-- DEEP: 10+min -->
> **War story:** An engineer spent 2 days debugging a production incident where a background job processed 50K duplicate payments. Root cause: the idempotency key was generated from a request body field that the frontend sometimes omitted, defaulting to `None`. The idempotency check passed because `None` matched `None` across all 50K requests. **Fix:** Idempotency keys must be generated from fields that cannot be empty — use a server-assigned request ID from the first hop, not a client-supplied value.
"""

CODE_REVIEW_WAR_STORY = """
<!-- DEEP: 10+min -->
> **War story:** A team reviewed a PR adding a new API endpoint. All 6 dimensions passed — correct logic, clean code, good tests, proper error handling. The reviewer skipped the dependency diff because "only one new import." That import was `pyjwt` (a third-party JWT library with a known CVE) instead of `PyJWT` (the maintained fork). The dependency was in production for 3 months before the security audit caught it. **Fix:** Never skip dependency review — verify every new import against the organization's approved list and SCA scan results.
"""

SECURITY_WAR_STORY = """
<!-- DEEP: 10+min -->
> **War story:** A startup passed SOC 2 Type I with a clean audit. Three months later, a researcher found an unauthenticated GraphQL introspection endpoint that exposed the entire schema, including internal mutation names like `adminResetUserPassword`. The endpoint had no rate limiting and no auth check — it was added in a 'minor refactor' that didn't trigger a security review because the PR title said 'clean up resolver naming.' **Fix:** Security review gates must trigger on file patterns, not PR labels. Any PR touching `graphql/`, `resolver/`, or `mutation/` paths gets an automatic security reviewer assignment regardless of how minor it looks.
"""

# ═══════════════════════════════════════════════════════════════
# 6. DEVOPS — Domain-specific decoders for finops & observability
# ═══════════════════════════════════════════════════════════════

FINOPS_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Cloud bill doubled overnight | Data transfer costs spiked from a new feature that streams large assets without CDN | Route all static/large assets through CDN. Set budget alerts at 80%/100%/120%. Tag every resource and query by tag to find the culprit in under 5 minutes. |
| Reserved instance shows no savings | RI purchased for a workload that stopped running or changed instance family | Reserve only for workloads with predictable, stable usage (24/7 services). Spot for batch jobs. Savings Plans cover instance family changes — prefer them over RIs for heterogeneous fleets. |
| Cost anomaly alert fires weekly, team ignores it | Threshold set too tight (10%) for a variable workload | Set anomaly thresholds at 2 standard deviations from trailing 14-day average, not a flat percentage. Filter out known growth patterns (deployments, user growth). Escalate if alert is acknowledged but not investigated within 72 hours. |
| Engineering team has no idea what their infrastructure costs | No per-team cost allocation or showback | Implement tag-based cost allocation. Every resource must have `Team`, `Environment`, `Service`, and `CostCenter` tags. Generate a weekly per-team cost report. Showback > chargeback — visibility first, accountability second. |
| Cross-region data transfer is 40% of the bill | Services in different regions communicate synchronously without data sovereignty requirements | Colocate dependent services in the same region. Use async messaging (SQS/Kafka) for cross-region communication. If low latency is required, deploy replicas in the consuming region. |
| GPU costs outrunning revenue 3:1 | ML training runs on on-demand GPUs with no spot instance fallback or checkpointing | Use spot instances with checkpointing for training — 70% cost reduction. Set max GPU budget per experiment. Preemptible TPUs for GCP users. Reserve only the minimum guaranteed capacity; burst into spot. |
| Hundreds of 'orphan' storage volumes costing $5K/mo | EBS volumes/block storage never deleted when EC2 terminates | Enable 'Delete on termination' by default. Implement a 'leaked resource' Lambda that snapshots and deletes unattached volumes older than 7 days. Tag volumes with `CreatedBy` and `TTL` for automated cleanup. |
"""

OBSERVABILITY_DECODER = """
### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Dashboard shows no data during incident | Dashboard queries against a different data source or time range than the alert that fired | Dashboard must share the same Prometheus/OTEL data source as the alert. Every dashboard panel should have a link to the alert that would fire if this metric goes bad. Test dashboard with actual incident data in post-mortems. |
| Alert fires every night at 3 AM, no one investigates | Threshold doesn't account for known maintenance windows | Add alert annotations for known maintenance windows (deploy window, batch jobs, backup window). Use mute timings or alert inhibition rules. If a team acknowledges the same alert 3 times without action, escalate to the manager. |
| Distributed trace shows 5-second gap between services | No instrumentation on the message queue consumer — time is 'black holed' between publish and process | Instrument the queue consumer with start/end spans around dequeue → process → acknowledge. Add messaging system span (broker latency, queue depth). The gap is invisible without instrumentation at every async boundary. |
| Memory leak undetected for 3 weeks | Container restarts reset the metric counter — Go/Java heap graphs show 'sawtooth' pattern that looks normal | Track rate of change (derivative) of memory usage per deploy. Alert on container restart frequency — restarts hide leaks. Use GAUGE metrics (current heap usage) not COUNTER (cumulative). p99 latency creep is often the first sign of a memory leak — monitor it. |
| Pager fatigue — team silenced the critical alert channel | Too many low-severity alerts on the same channel as SEV1 alerts | Route alerts by severity: SEV1 (page), SEV2 (Slack notify), SEV3 (dashboard badge), SEV4 (weekly digest). No alert should fire more than once per 30 minutes per service. Maximum 5 pages per on-call per shift — if exceeded, review alert thresholds. |
| 'No data' metric causes false-positive auto-scaling | Missing data is treated as 0 by Prometheus, triggering scale-down during a deployment | Always use `default` or `absent()` handling for scaling metrics. Missing data !== 0. Use `avg_over_time(metric[5m])` to smooth deployment gaps. Alert on 'no metrics received' as a separate data freshness check, not a scaling signal. |
| Canary deploy shows no metric difference between old and new | Metric cardinality too low to distinguish versions — all metrics tagged with `service` but not `version` or `deploy_id` | Tag every metric with `version`, `deploy_id`, `canary_group` (control/treatment). Compare p50/p95/p99 and error rate between control and treatment. Minimum 2 minutes of canary data before comparing statistical significance. |
"""

# ═══════════════════════════════════════════════════════════════
# 7. SECURITY — Boundary clarification
# ═══════════════════════════════════════════════════════════════

SEC_REVIEWER_BOUNDARY = """
- **Use `/security-engineer` instead when:** You need a penetration test, threat model of a new architecture, SAST/SCA tool configuration, or incident response. Security-reviewer is for _reviewing existing work_ — security-engineer is for _building and testing security systems_.
- **Use `/compliance-officer` instead when:** You need SOC 2, ISO 27001, or HIPAA audit evidence collection, control mapping, or gap assessment. Security-reviewer finds vulnerabilities; compliance-officer proves you have processes to find and fix them.
"""

SEC_ENGINEER_BOUNDARY = """
- **Use `/security-reviewer` instead when:** You need a code-level security review of a PR, dependency audit on a specific change, or SAST finding triage. Security-engineer builds the security program; security-reviewer inspects individual changes against it.
- **Use `/incident-responder` instead when:** A security incident is in progress or has just been detected — active containment, eradication, and recovery. Security-engineer builds preventive controls; incident-responder handles active breaches.
"""

PM_BOUNDARY = """
- **Use `/scrum-master` instead when:** The team needs coaching on agile practices, sprint ceremonies are dysfunctional, impediments need removal, or team health needs improvement. Scrum-master is about _how_ the team works — facilitation, coaching, process improvement.
- **Use `/technical-program-manager` instead when:** You need to coordinate across multiple teams, manage cross-team dependencies, drive a program with a fixed timeline and multiple workstreams. TPM handles scope that spans teams; PM handles scope within a single project.
"""

SCRUM_BOUNDARY = """
- **Use `/project-manager` instead when:** You need project planning with WBS, Gantt charts, RAID logs, budget tracking, stakeholder reporting, or a formal project charter. Project-manager handles the _what and when_ — scope, timeline, budget, risks. Scrum-master handles the _how_ — team process, coaching, impediment removal.
- **Use `/technical-program-manager` instead when:** A program spans multiple scrum teams, has cross-team dependencies, and requires a consolidated timeline and risk register. TPM coordinates across teams; scrum-master serves one team.
"""

# ═══════════════════════════════════════════════════════════════
# 8. GROWTH — Content-strategist good-looks
# ═══════════════════════════════════════════════════════════════

CONTENT_GOOD_LOOKS = "**What good looks like:** A 30-day content calendar published with each piece assigned to a writer, a reviewer, and a distribution channel — not just topics, but drafts are due 5 days before publish for editorial review. Topic cluster model maps every primary keyword to a pillar page and 5-8 supporting articles; internal links connect them. Every content piece has a specific CTA tied to a tracked conversion goal (signup, demo request, PDF download). Content audit within the last 90 days shows what's performing, what's stale, and what needs updating — with a timeline for each action."

# ═══════════════════════════════════════════════════════════════
# 9. GDPR — Token budget tune and token-saving rule
# ═══════════════════════════════════════════════════════════════

GDPR_SAVING_RULE = """
> **Token-saving rule:** The full GDPR skill covers 10+ areas (data inventory, consent, DPA, SAR, breach response, etc.). Load only the section relevant to your current task. If you need data inventory, skip consent law. Each section references the relevant GDPR articles — read the article reference, not the full GDPR text. A typical task requires ~1500 tokens, not the full 8000+.
"""

# ═══════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════

def replace_good_looks(text, skill_name, new_content):
    """Replace existing What Good Looks Like entry with new content."""
    # Match "**What good looks like:**" through to the next section or blank line
    pattern = re.compile(
        r'\*\*What good looks like:\*\*.*?(?=\n(?:#|\n\*|$))',
        re.DOTALL
    )
    if pattern.search(text):
        return pattern.sub(new_content, text, count=1)
    return text


def replace_error_decoder(text, new_decoder):
    """Replace the generic 3-row error decoder with domain-specific one."""
    # Match from "### Error Decoder" to the next ## heading or end
    pattern = re.compile(
        r'### Error Decoder.*?(?=\n## )',
        re.DOTALL
    )
    if pattern.search(text):
        return pattern.sub(f"### Error Decoder{new_decoder.strip()}\n\n", text)
    return text


def insert_after_section(text, after_marker, content):
    """Insert content after a specific marker string."""
    pos = text.find(after_marker)
    if pos >= 0:
        end = pos + len(after_marker)
        text = text[:end] + content + text[end:]
    return text


def process(filepath):
    text = filepath.read_text()
    original = text
    skill_name = filepath.parent.name
    domain = filepath.parent.parent.name

    changes = []

    # ── STRATEGY good-looks ──
    if domain == "01-strategy" and skill_name in STRATEGY_GOOD_LOOKS:
        text = replace_good_looks(text, skill_name, STRATEGY_GOOD_LOOKS[skill_name])
        changes.append("outcome-good-looks")

    # ── DESIGN handoff + good-looks ──
    if domain == "03-design":
        if skill_name in DESIGN_GOOD_LOOKS:
            text = replace_good_looks(text, skill_name, DESIGN_GOOD_LOOKS[skill_name])
            changes.append("outcome-good-looks")
        # Add Figma→code handoff if not present
        if "Design-to-Code Handoff Chain" not in text:
            # Insert before ## Sub-Skills or at end of cross-skill section
            if "## Sub-Skills" in text:
                text = text.replace("## Sub-Skills", f"{DESIGN_HANDOFF}\n## Sub-Skills", 1)
                changes.append("figma-handoff")
            elif "## References" in text:
                text = text.replace("## References", f"{DESIGN_HANDOFF}\n## References", 1)
                changes.append("figma-handoff")

    # ── ARCHITECTURE good-looks ──
    if domain == "04-architecture" and skill_name in ARCH_GOOD_LOOKS:
        text = replace_good_looks(text, skill_name, ARCH_GOOD_LOOKS[skill_name])
        changes.append("review-good-looks")

    # ── DEVELOPMENT good-looks ──
    if domain == "05-development" and skill_name in DEV_GOOD_LOOKS:
        text = replace_good_looks(text, skill_name, DEV_GOOD_LOOKS[skill_name])
        changes.append("specific-good-looks")

    # ── QUALITY war stories ──
    if domain == "06-quality":
        if skill_name == "qa-engineer" and "processed 50K duplicate payments" not in text:
            text = insert_after_section(text, "<!-- STANDARD: 3min -- rules extracted from production experience -->", QA_WAR_STORY)
            changes.append("war-story")
        if skill_name == "code-reviewer" and "pyjwt" not in text:
            text = insert_after_section(text, "<!-- STANDARD: 3min -- rules extracted from production experience -->", CODE_REVIEW_WAR_STORY)
            changes.append("war-story")
        if skill_name == "security-reviewer" and "GraphQL introspection" not in text:
            text = insert_after_section(text, "<!-- STANDARD: 3min -- rules extracted from production experience -->", SECURITY_WAR_STORY)
            changes.append("war-story")

    # ── DEVOPS domain-specific decoders ──
    if domain == "07-devops":
        if skill_name == "finops-engineer" and "Cloud bill doubled overnight" not in text:
            text = replace_error_decoder(text, FINOPS_DECODER)
            changes.append("finops-decoder")
        if skill_name == "observability-engineer" and "Dashboard shows no data during incident" not in text:
            text = replace_error_decoder(text, OBSERVABILITY_DECODER)
            changes.append("observability-decoder")

    # ── SECURITY boundary ──
    if skill_name == "security-reviewer" and "Use `/security-engineer` instead" not in text:
        text = insert_after_section(text, "### When to Use", SEC_REVIEWER_BOUNDARY)
        changes.append("boundary-clarification")
    if skill_name == "security-engineer" and "Use `/security-reviewer` instead" not in text:
        text = insert_after_section(text, "### When to Use", SEC_ENGINEER_BOUNDARY)
        changes.append("boundary-clarification")

    # ── DATA token budget tune ──
    if domain == "09-data":
        if skill_name == "ml-ai-engineer":
            text = re.sub(r'token_budget: \d+', 'token_budget: 5000', text)
            changes.append("budget-4000→5000")
        if skill_name == "data-scientist":
            text = re.sub(r'token_budget: \d+', 'token_budget: 4500', text)
            changes.append("budget-3975→4500")

    # ── GROWTH content-strategist good-looks ──
    if skill_name == "content-strategist":
        # Already good but can be stronger on calendar specifics
        # Check current text
        if "drafts are due 5 days before publish" not in text:
            text = replace_good_looks(text, skill_name, CONTENT_GOOD_LOOKS)
            changes.append("stronger-good-looks")

    # ── LEGAL GDPR token budget ──
    if skill_name == "gdpr-privacy":
        text = re.sub(r'token_budget: \d+', 'token_budget: 8000', text)
        if "Token-saving rule" not in text:
            text = insert_after_section(text, "## When to Use", GDPR_SAVING_RULE)
            changes.append("budget-4000→8000 + saving-rule")

    # ── OPERATIONS boundary ──
    if skill_name == "project-manager" and "Use `/scrum-master` instead" not in text:
        text = insert_after_section(text, "### When to Use", PM_BOUNDARY)
        changes.append("boundary-clarification")
    if skill_name == "scrum-master" and "Use `/project-manager` instead" not in text:
        text = insert_after_section(text, "### When to Use", SCRUM_BOUNDARY)
        changes.append("boundary-clarification")

    if text != original and changes:
        filepath.write_text(text)
        print(f"  ✓ {skill_name} ({', '.join(changes)})")
        return True
    elif text != original:
        filepath.write_text(text)
        print(f"  ✓ {skill_name} (changes applied)")
        return True
    else:
        print(f"  - {skill_name} (no changes needed)")
        return False


def main():
    print("=" * 65)
    print("10/10 v3 — Closing all domain-specific gaps")
    print("=" * 65)

    skill_files = sorted(SKILLS.glob("*/**/SKILL.md"))
    print(f"\nProcessing {len(skill_files)} skills...\n")

    upgraded = 0
    total = 0
    for sf in skill_files:
        try:
            total += 1
            if process(sf):
                upgraded += 1
        except Exception as e:
            print(f"  ✗ ERROR: {sf.relative_to(SKILLS)} — {e}")

    print(f"\n{'=' * 65}")
    print(f"Complete: {upgraded} upgraded out of {total}")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
