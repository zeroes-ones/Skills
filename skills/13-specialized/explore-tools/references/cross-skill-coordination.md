## Cross-Skill Coordination

<!-- This skill can be invoked by ANY other skill when tool selection is needed -->

### Decision Gates & Artifacts

- **Gate 1 — Requirements Defined:** Tool discovery requires clear problem definition, budget constraints, and success criteria from `product-strategist`. Artifact: product requirements brief with budget and timeline.
- **Gate 2 — Architecture Boundaries Set:** Tool selection must respect architecture constraints (language, platform, protocols) from `system-architect`. Artifact: architecture decision records with integration boundaries.
- **Gate 3 — Domain Expertise Available:** Domain-specific evaluation needs input from specialized skills. Artifact: domain-specific requirements and constraints.
- **Artifact:** Structured tool recommendation with evaluation matrix, cost analysis, risk assessment, and migration path.

### Coordinate With — When Tool Selection Is Needed

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Product Strategist** | Defining budget constraints, time-to-market pressure, make-vs-buy decisions | Budget range, timeline urgency, strategic importance (core vs. commodity), vendor risk tolerance |
| **System Architect** | Architecture-level tool decisions (database, framework, cloud provider, message queue) | Architecture constraints, integration requirements, non-functional requirements (latency, throughput, consistency), existing stack compatibility |
| **Backend Developer** | Backend library/framework/ORM/caching/messaging tool selection | Performance requirements, language ecosystem, existing codebase patterns, team familiarity |
| **Frontend Developer** | Frontend library/UI framework/state management/bundling tool selection | Bundle size constraints, browser support matrix, framework compatibility (React/Vue/Svelte/etc.), accessibility requirements |
| **DevOps Engineer** | CI/CD, infrastructure, monitoring, logging, deployment tool selection | Cloud provider, containerization strategy, scale requirements, budget for infrastructure tooling, existing IaC patterns |
| **Security Reviewer** | Security tool evaluation, dependency scanning, CVE assessment | Security requirements, compliance framework (SOC2, HIPAA, GDPR, PCI-DSS), risk tolerance, incident response capabilities |
| **QA Engineer** | Testing framework, test runner, E2E tool, performance testing tool selection | Test strategy (unit/integration/e2e split), CI integration requirements, flakiness tolerance, reporting needs |
| **Database Designer** | Database selection (SQL vs NoSQL, hosted vs self-managed), ORM selection | Data model complexity, query patterns, consistency requirements, scale projections, team SQL expertise |
| **Mobile Developer** | Mobile framework, navigation, state management, push notification, analytics tool selection | Target platforms (iOS/Android/both), performance constraints, offline requirements, app store compliance |
| **Data Engineer** | Data pipeline, ETL/ELT, data warehouse, orchestration tool selection | Data volume/velocity/variety, latency requirements, existing data infrastructure, team data engineering expertise |
| **ML/AI Engineer** | ML framework, model serving, vector database, LLM tooling selection | Model type and size, inference latency requirements, GPU availability, MLOps maturity, budget for API-based vs self-hosted |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Tool evaluation reveals the current tool costs 10x more than alternatives | Product Strategist, CTO Advisor, DevOps Engineer | Significant cost savings opportunity; budget reallocation potential |
| Critical dependency flagged as abandoned (no commits in 6+ months) | System Architect, all consuming teams, Project Manager | Migration emergency on the horizon; risk of security vulnerabilities and breaking dependency conflicts |
| Recommended tool has a CVE disclosed (HIGH/CRITICAL) | Security Reviewer, all consuming teams, Project Manager | Immediate security risk; may require hotfix, workaround, or tool replacement |
| New tool emerges that is objectively better than current choice across all dimensions | System Architect, Tech Lead, Product Strategist | Migration opportunity; evaluate cost/benefit of switching |
| Cost analysis shows free tier will be exceeded within 3 months at current growth rate | Product Strategist, Finance, DevOps Engineer | Budget planning needed; either upgrade to paid tier or implement cost controls |
| Dependency tree audit finds GPL/AGPL license contamination | Legal/Compliance, System Architect, CTO Advisor | Legal risk to proprietary code; immediate remediation required before next release |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Tool evaluation blocked by unclear requirements or conflicting constraints | Product Strategist, CTO Advisor | Need executive alignment on priorities (cost vs. speed vs. quality) |
| All evaluated tools score RED on risk assessment — no safe options exist | System Architect, CTO Advisor | Build-vs-buy decision needed; may need to build custom solution or accept managed risk |
| Tool migration cost exceeds annual tool budget by >3x | CTO Advisor, VP Engineering, Finance | Funding decision; migration may need dedicated budget allocation |
| Security audit of recommended tool reveals compliance-blocking issue | CTO Advisor, Legal/Compliance, Security Reviewer | Compliance risk; may block adoption regardless of technical merit |
| Vendor lock-in risk identified that could block future architecture evolution | System Architect, CTO Advisor | Strategic risk; decision needs explicit risk acceptance at executive level |## Proactive Triggers

| Trigger | Action | Rationale |
|---------|--------|-----------|
| User asks "is there a tool for..." | Run Discovery Protocol (Phase 1) | Tool discovery is the primary use case |
| User mentions budget constraints | Run Cost Optimization Matrix | Cost-aware decisions prevent lock-in |
| User is evaluating 3+ tools | Produce 4-option recommendation grid | Structured comparison prevents analysis paralysis |
| Tool EOL or deprecation announced | Trigger replacement search + migration plan | Proactive migration avoids last-minute scrambles |
| New ecosystem version released | Check tool compatibility + update scoring | Version-aware recommendations stay current |
| User expresses "this feels expensive" | Re-run TCO model with 3-year projection | Cost is the #1 reason tools are abandoned post-adoption |
