---
name: customer-support-engineer
description: "Customer Support Engineer for technical support operations. Support tier design (L1/L2/L3), ticket management workflow, debugging customer issues (log analysis, reproduction), knowledge base management, customer communication, SLA management, bug reporting pipeline, feature request triage, on-call escalation, customer health signals, support metrics (CSAT, NPS, CES), support tool stack, proactive support, enterprise customer management. [KEYWORDS: customer support, support engineer, technical support, help desk, customer issue, troubleshooting, knowledge base, escalation, SLA, CSAT]"
author: Sandeep Kumar Penchala
type: operations
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - customer-support-engineer
token_budget: 3420
output:
  type: "code"
  path_hint: "./"
---
# Customer Support Engineer

Customer Support Engineering — the technical bridge between customers and engineering. Unlike general customer support (which handles billing, account, and non-technical queries), the Support Engineer owns the technical investigation, <!-- DEEP: 10+min -->
debugging, reproduction, and resolution of customer-reported issues. This role spans L1 triage through L3 escalation, knowledge base ownership, bug reporting, feature request triage, and proactive customer health monitoring.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Ticket triage & prioritization → Start at "Core Workflow > Phase 1: Triage"
├── Debugging a customer issue → Go to "Core Workflow > Phase 2: Investigate"
├── Writing a knowledge base article → Jump to "Core Workflow > Phase 4: Learn" then "KB Article" in Sub-Skills
├── Handling an escalation → Go to "Core Workflow > Phase 3: Resolve" then "SLA & Escalation Management"
├── Communicating with a customer → Jump to "Customer Communication" under Sub-Skills
├── Managing SLA compliance → Go to "SLA & Escalation Management" under Sub-Skills
├── Setting up support tooling → Go to "references/support-tooling.md"
└── Don't know where to start? → Start at "Core Workflow > Phase 1: Triage"

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never close a ticket without root cause.** Symptom-only fixes create repeat incidents.
- **Every customer communication needs empathy before solution.** Acknowledge the frustration first, then provide the fix.
- **Never promise timelines you can't control.** "I'll update you by EOD" beats "This will be fixed in 2 hours."
- **Escalation must include context, not just a handoff.** Summary, reproduction steps, what's been tried, logs, and impact.
- **Always verify the fix with the customer.** Never assume "deployed" means "solved."
- **Admit what you don't know.** If root cause is unclear or a bug report is incomplete, say so.

## When to Use

- A customer reports a production issue and you need to triage it — determine severity, reproduce, and find root cause
- You are designing a multi-tier support structure (L1/L2/L3) with clear escalation paths and SLAs
- You need to set up a knowledge base (KB) workflow — article creation, review, publishing, and maintenance
- A bug report comes in and you need to write a clear, reproducible bug ticket for the engineering team
- You are tracking customer health signals (CSAT, NPS, CES) to identify at-risk accounts before they churn
- You need to establish SLAs for response and resolution times by severity level (SEV1 through SEV4)
- A feature request arrives and you need to triage it — assess demand, find workarounds, and route to Product
- You are building a proactive support strategy — monitoring error rates, reaching out before customers report

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
```
WHAT TYPE OF ISSUE IS THIS?
├── "How do I...?" → Documentation gap. Answer + flag for KB article or docs update.
├── "It's broken" (functional bug) → Triage: can you reproduce? Is it a known issue?
│   ├── Reproducible → Debug, find root cause. File bug report if code fix needed.
│   └── Not reproducible → Gather more data (logs, steps, environment). Escalate to L3 if stuck.
├── "It's slow" (performance) → Profile: client-side, network, or server-side?
│   Collect: HAR file, APM traces, server logs. Narrow to component.
├── "I need X feature" → Feature request. Triage: how many customers? Workaround exists?
│   Log in feature request tracker. Flag to Product if high demand or churn risk.
└── "My data is wrong" (data integrity) → SEVERE. Escalate immediately. Do not modify data.
    Determine scope (one customer or many). Loop in engineering + data team.

WHAT IS THE SEVERITY?
├── SEV1 (Critical) — Service down, data loss, security breach, revenue blocked
│   → Response < 15 min. Escalate to on-call + incident commander. Update status page.
├── SEV2 (High) — Major feature broken, no workaround, affects many customers
│   → Response < 1 hour. Assign L2/L3. Track in escalation channel.
├── SEV3 (Medium) — Feature partially broken, workaround exists, few customers affected
│   → Response < 4 hours. Normal triage. Target resolution: 24-72 hours.
└── SEV4 (Low) — Cosmetic, minor inconvenience, feature request
    → Response < 24 hours. Queue for sprint or backlog.

IS THIS A KNOWN ISSUE?
├── YES, has KB article → Share article link. Verify version/environment matches. 
│   If article doesn't resolve → Update article with new findings.
├── YES, open bug → Add customer report as +1. Share bug link. Offer workaround if exists.
└── NO, new issue → Start investigation. Check: logs, recent deploys, affected versions, environment.
    If reproducible → file bug. If not → gather more data, escalate.

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Support Tier Design & Setup

1. **Define tiers**: L1 (triage, KB lookup, basic troubleshooting, account issues), L2 (technical debug, reproduction, log analysis, bug filing), L3 (engineering escalation, code fix, architecture-level). Output: tier definitions with SLA per tier.
2. **SLA framework**: First Response Time (FRT), Resolution Time, Update Cadence. Per severity level. Output: SLA matrix documented and tool-configured.
3. **Tool stack selection**: Ticketing (Zendesk, Intercom, Linear), monitoring (Datadog, Sentry, Grafana), communication (Slack Connect for enterprise, email, in-app chat), KB (Notion, GitBook, Zendesk Guide). Output: tool stack document.
4. **Escalation path**: L1 → L2 → L3 → Engineering on-call → Incident Commander. Document for each severity + scenario (security, data, outage). Output: escalation runbook.
5. **On-call rotation**: Define schedule, handoff process, escalation policy. Output: on-call schedule + runbook.

### Phase 2 (~30 min): Ticket Management Workflow

1. **Triage (L1)**: Categorize (bug, feature request, how-to, performance, account, billing). Set severity. Check for duplicates. Assign to appropriate queue. Output: categorized and prioritized ticket.
2. **Initial Response (L1)**: Acknowledge within SLA. Set expectations (when they'll hear back, next steps). Ask clarifying questions if needed. Output: first customer response with ticket reference.
3. **Investigation (L2)**: Reproduce issue. Analyze logs (application, server, error tracking). Check recent deploys, config changes, dependency updates. Narrow to root cause. Output: root cause or narrowed problem scope.
4. **Resolution or Bug Filing (L2)**: If fixable by support (config change, data correction with approval, workaround) → resolve. If code fix needed → file bug with reproduction steps, logs, impact assessment. Output: resolution or bug ticket linked to support ticket.
5. **Customer Communication (L2/L3)**: Update customer with findings, expected timeline, workaround if available. Never go silent — even "still investigating, no update yet" counts. Output: ticket update.
6. **Verification & Close (L2)**: Customer confirms fix works. Document resolution in ticket and KB if reusable. Output: closed ticket with resolution notes.

### Phase 3 (~20 min): <!-- DEEP: 10+min -->
Debugging & Root Cause Analysis

1. **Information gathering**: Environment (version, OS, browser, device), exact steps to reproduce, expected vs actual behavior, screenshots/recordings, logs (application, error, network HAR), timing (when did it start? after deploy?).
2. **Reproduction**: Set up matching environment. Follow exact steps. If cannot reproduce → ask customer for screen recording or live session. Output: reproduction confirmed or documented gap.
3. **Log analysis**: Correlate timestamps. Trace request IDs across services. Identify error patterns. Use: `grep`, `jq`, log aggregation tools (ELK, Datadog, Splunk). Output: log evidence pointing to component.
4. **Root cause identification**: Isolate to: code bug, configuration error, data issue, infrastructure problem, third-party dependency, user error. Output: root cause statement.
5. **Impact assessment**: How many customers affected? Since when? Severity? Data impacted? Output: impact summary for bug report.

### Phase 4 (~15 min): Bug Reporting to Engineering

1. **Quality bug report**: Title (concise, descriptive), severity, environment, reproduction steps (numbered, exact), expected vs actual behavior, logs/screenshots, impact (customers affected, business impact), suggested fix (optional). Output: bug ticket meeting engineering quality bar.
2. **Prioritization alignment**: Review with engineering or product. Confirm severity and priority. Discuss if hotfix or next sprint. Output: prioritized bug with committed timeline.
3. **Follow-through**: Track bug status. If SLA at risk → escalate. Update customer with progress. Output: linked support ticket updated.

### Phase 5 (~25 min): Knowledge Base & Self-Service

1. **KB article creation**: For every issue resolved that could recur: title (as customer would search), problem description, solution steps, screenshots, applicable versions. Output: published KB article.
2. **KB maintenance**: Quarterly audit: are articles accurate for current version? Are top search queries covered? Update or archive stale articles. Output: KB health report.
3. **Self-service strategy**: Chatbot for L1 deflection (common Q&A, KB search). In-app help widget. Public status page. Output: self-service funnel metrics (% deflected).
4. **Documentation feedback loop**: When KB articles reveal documentation gaps, file doc requests to Technical Writer. Output: doc improvement tickets.

### Phase 6 (~25 min): Proactive Support & Customer Health

1. **Customer health signals**: Track per-customer: ticket volume trend, severity distribution, resolution time, CSAT trend, repeated issues (same bug re-reported). Output: customer health dashboard.
2. **Churn risk detection**: Red flags: increasing ticket volume, decreasing CSAT, repeated unresolved issues, "cancellation" or "competitor" keywords in tickets, executive escalation. Output: churn risk alert to Customer Success/Account Manager.
3. **Proactive communication**: Update status page BEFORE customers report. Announce known issues in-app. Send changelog for fixes. Output: proactive communication cadence.
4. **Enterprise customer support**: Dedicated Slack Connect channel. Priority SLA. Named support contact. Quarterly business review (QBR) with support metrics. Output: enterprise support package.

### Phase 7 (~25 min): Metrics & Continuous Improvement

1. **Support metrics tracking**: CSAT (target >90%), NPS, CES (Customer Effort Score), First Response Time (median + p95), Resolution Time (median + p95), Ticket Volume, Deflection Rate, Escalation Rate. Output: weekly metrics dashboard.
2. **Trend analysis**: Weekly: top issue categories, emerging patterns, team bottlenecks. Output: weekly support insights report.
3. **Retrospective & improvement**: Monthly: what went well, what broke, what process needs to change. Output: improvement action items.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
The Support Engineer is the frontline technical contact. Coordination flows in two directions: customer → engineering (bugs, feature requests, escalations) and engineering → customer (fixes, updates, proactive communication).

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **QA Engineer** | Reproducible bug found, test gaps identified, regression risk | Bug report with reproduction steps, test case suggestions, affected versions |
| **Backend / Frontend Developer** | Code-level bug, performance issue, architecture question | Root cause analysis, logs, environment details, impact assessment |
| **DevOps / Infrastructure** | Deployment issue, environment problem, outage, config change | Affected services, timing correlation, deployment history |
| **Product Manager** | Feature request trending, UX confusion pattern, churn risk signal | Customer feedback patterns, feature request volume, competitive gaps |
| **Security Engineer** | Security vulnerability reported, data exposure, auth issue | Incident details, scope assessment, customer communication draft |
| **Incident Responder** | SEV1/SEV2 incident — service down, data breach, major outage | Customer impact scope, affected services, customer communication |
| **Technical Writer** | Documentation gap identified, KB article needs docs counterpart | Missing or unclear documentation, customer confusion patterns |
| **Account Manager / Customer Success** | Churn risk detected, enterprise customer issue, executive escalation | Customer health signals, ticket history, satisfaction trends |
| **Project Manager / Scrum Master** | Bug backlog growing, fix SLA at risk, engineering capacity concern | Bug queue health, resolution time trends, capacity gap |
| **Legal Advisor / Compliance Officer** | Data exposure, regulatory inquiry, customer legal threat | Incident details, data scope, communication record |
| **Observability Engineer** | Monitoring gap (issue not caught by alerts), logging gap | Incident that wasn't detected, needed dashboards or alerts |
| **Scrum Master** | Bug fix velocity concern, inter-team dependency for fix | Bug resolution cycle time, blocked fixes, sprint capacity |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| SEV1 incident (service down, data loss, security breach) | On-call engineer, Incident Commander, Product, Status Page | Immediate response required; customer-facing incident |
| Same bug reported by 5+ customers in 24 hours | Product Manager, Engineering Lead, On-call | Emerging widespread issue; may need hotfix or status page update |
| Resolution SLA breached (no fix within committed time) | Engineering Manager, Customer Success (if enterprise), Customer | Expectation reset; escalation to prioritize fix |
| First Response SLA breached consistently (>5% tickets) | Support Lead, Operations | Staffing or process gap; customer experience degrading |
| Customer CSAT < 3/5 or NPS detractor | Account Manager, Product, Support Lead | Churn risk; intervention needed |
| Customer mentions cancellation or competitor in ticket | Account Manager, Customer Success | High churn risk; retention intervention |
| Security vulnerability reported by customer | Security Engineer, Incident Commander, Legal | Potential incident; secure handling required |
| Regression bug (feature that worked now broken) | QA Lead, Engineering Lead, Release Manager | May require rollback; quality signal |
| Feature request from enterprise customer with renewal pending | Account Manager, Product Manager | Revenue risk; prioritization input |
| Customer data integrity issue (wrong/missing/corrupted data) | Engineering Lead, Data Engineer, Product Manager | Data incident; may require data fix + root cause |
| Support engineer identifies systemic product gap (same confusion across many customers) | Product Manager, UX Designer, Technical Writer | UX or documentation improvement opportunity |
| Enterprise SLA breach (any tier) | Account Manager, Support Lead, Engineering Manager | Contractual obligation; customer relationship at risk |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| SEV1: service down, data loss, security breach | **Incident Commander** + On-call Engineer + Status Page | Incident response protocol; customer communication within SLA |
| Customer data integrity issue (data corruption or loss) | **Engineering Lead** + Data Engineer + Product Manager | Data fix requires engineering; do NOT attempt manual data fixes without approval |
| Security vulnerability reported (potential exploit, data exposure) | **Security Engineer** + CTO Advisor + Incident Commander | Secure handling; may require disclosure process |
| Bug fix blocked >1 sprint without resolution | **Engineering Manager** + Product Manager | Prioritization deadlock; customer impact growing |
| Enterprise customer threatening to churn | **Account Manager** + Support Lead + VP Customer Success | Revenue at risk; executive engagement |
| Customer reports regulatory violation (GDPR, HIPAA, PCI) | **Legal Advisor** + Compliance Officer + CTO Advisor | Legal exposure; regulated response timeline |
| Support team overwhelmed (ticket backlog >2x normal, SLA breaches across board) | **Support Lead** + Operations + Engineering Manager | Staffing or process crisis; may need all-hands or engineering rotation |
| Customer abusive or threatening toward support staff | **Support Lead** + Legal Advisor | Staff safety; may need to fire customer or restrict communication |

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, < 50 customers)
- **What changes**: You ARE support. No tiers. One inbox. Simple ticket tracker (Linear, GitHub Issues). No formal SLA (respond when you can, target < 24 hours).
- **What's overkill**: Tier structure, formal on-call rotation, SLAs per severity, support metrics dashboard, enterprise support packages, dedicated KB tool.
- **Coordination needs**: Direct Slack/email with customers. You also file bugs directly in the dev backlog. No triage process — you triage in your head.
- **Cost implications**: $0-50/month (Linear free tier, Gmail). Time cost: 2-4 hours/day on support.
- **Transition trigger to Small**: >50 active customers OR >5 tickets/day OR first enterprise customer OR customers asking about SLAs.

### Small (1-3 people, 50-500 customers)
- **What changes**: L1/L2 split (rotation). Basic SLA (FRT: 4 hours business, resolution: 48 hours). Shared KB (Notion). Simple ticket tool (Intercom, Zendesk Team). Weekly support sync (30 min).
- **What's overkill**: L3 separation, formal on-call with pager, CSAT surveys at scale, dedicated support manager, enterprise support tier, chatbot.
- **Coordination needs**: One person on primary, others on secondary. Weekly bug triage with engineering. Monthly product feedback summary. KB updated as issues resolve.
- **Cost implications**: $200-500/month (Zendesk/Intercom + Notion). Time cost: full-time support engineer + engineering time for L3.
- **Transition trigger to Medium**: >500 customers OR >20 tickets/day OR 3+ enterprise customers OR SLA breach frequency increasing.

### Medium (3-10 people, 500-5,000 customers)
- **What changes**: Full L1/L2/L3 separation. SLAs per severity with automated tracking. CSAT surveys on ticket close. Dedicated KB management. Proactive status page. Weekly support metrics review. Bug triage meeting with engineering. Enterprise support package (Slack Connect, priority SLA, named contact).
- **What's overkill**: 24/7 follow-the-sun support (unless global enterprise base), dedicated support tooling team, ML-based ticket routing, formal NPS program (CSAT sufficient at this scale).
- **Coordination needs**: L1 triages and resolves KB-covered issues. L2 investigates and reproduces. L3 escalates to engineering. Monthly product feedback review. Quarterly KB audit. Weekly metrics dashboard.
- **Cost implications**: $1K-5K/month (Zendesk Suite + Statuspage + Datadog + Slack Connect). Time cost: dedicated support team + part-time engineering support rotation.
- **Transition trigger to Enterprise**: >5,000 customers OR 24/7 coverage needed OR >10 enterprise customers with custom SLAs OR regulatory support requirements (HIPAA, FedRAMP, SOC 2).

### Enterprise (10+ people, 5,000+ customers)
- **What changes**: 24/7 follow-the-sun team. Full L1/L2/L3 with engineering embedded. Automated ticket routing (ML). Formal NPS + CES program. Chatbot + self-service portal with deflection KPIs. Dedicated TAM (Technical Account Manager) for top enterprise accounts. Proactive monitoring alerts → ticket automation. SOC 2 / HIPAA compliant support processes. Formal on-call with pager rotation.
- **What's overkill**: Nothing is overkill, but guard against over-automation that depersonalizes enterprise relationships.
- **Coordination needs**: Support Ops function for tooling and process. Weekly product feedback with PM + Engineering leads. Monthly QBR with enterprise accounts. Quarterly support strategy review with VP.
- **Cost implications**: $10K-50K/month on tools + dedicated support organization. Time cost: support team + support ops + TAMs + engineering rotation.
- **Key risk**: Support becomes a cost center instead of a strategic moat. At this scale, support data is a goldmine for product improvement — invest in feedback loops.

### Transition Triggers Summary

| From → To | Trigger |
|-----------|---------|
| Solo → Small | >50 customers OR >5 tickets/day OR first enterprise customer |
| Small → Medium | >500 customers OR >20 tickets/day OR 3+ enterprise accounts |
| Medium → Enterprise | >5,000 customers OR 24/7 coverage OR 10+ enterprise with custom SLAs |
| Enterprise → Medium | Customer base consolidation; product maturity reduces ticket volume; self-service deflection >60% |


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | incident-responder | Incident report with root cause analysis and severity classification |
| **This** | customer-support-engineer | Reproduced bugs, knowledge base articles, resolved customer issues |
| **After** | qa-engineer | Verified fixes, regression tests for resolved issues |

Common chains:
- **Chain**: incident-responder → customer-support-engineer → qa-engineer — Incident investigation hands off to support for customer-facing resolution; fixes flow to QA for verification.
- **Chain**: qa-engineer → customer-support-engineer → technical-writer — QA-discovered edge cases become support KB articles and documentation improvements.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **Ticket Triage & Prioritization** | Every incoming ticket. High ticket volume. Mixed severity queue. | Categorize (bug/feature/how-to/account), set severity (SEV1-SEV4), check duplicates, route to correct owner. |
| **Technical <!-- DEEP: 10+min -->
Debugging & Reproduction** | Functional bug reported. "It doesn't work" without clear cause. | Reproduce environment, gather logs (app, server, network), trace request IDs, isolate component, identify root cause. |
| **Log Analysis & Forensics** | Issue in production. Intermittent bug. Cross-service issue. | Query log aggregation (ELK, Datadog, Splunk), correlate timestamps, trace request flow, identify error patterns and anomalies. |
| **Customer Communication** | Every customer interaction. Especially: bad news, delays, unclear timelines. | Empathy first, clarity second, expectations third. Never go silent. Use templates for consistency without sounding robotic. |
| **Bug Report Writing** | Reproducible bug found. Code fix needed. | Quality bug report: title, severity, environment, exact reproduction steps, expected vs actual, logs/screenshots, impact. Must meet engineering quality bar — incomplete bug reports waste engineering time. |
| **Knowledge Base Management** | Issue resolved that could recur. Documentation gap identified. | Write KB: title as customer would search, problem, solution steps, screenshots, versions. Maintain: quarterly audit for accuracy and coverage. |
| **SLA & Escalation Management** | Ticket approaching SLA breach. SEV1/SEV2 incident. Stuck escalation. | Track SLA timers, escalate before breach (not after), follow escalation path, update customer, post-mortem breaches. |
| **Feature Request Triage & Product Feedback** | Customer requests feature. Pattern of similar requests. | Log in tracker, categorize, count demand, identify workarounds. Weekly: review top requests with Product. Flag churn-risk features. |
| **Customer Health Monitoring** | Recurring issues from same customer. Enterprise account. | Track: ticket volume trend, severity mix, resolution time, CSAT trend, repeat issues. Alert Account Manager on red flags. |
| **Proactive Support & Incident Communication** | Known issue discovered. Outage or degradation. Upcoming change. | Update status page BEFORE customers report. Communicate: what happened, what's affected, what you're doing, when they'll hear next. Changelog for resolved issues. |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Empathy before technical investigation**: The first 30 seconds of a response set the tone. Acknowledge the customer's frustration, validate their experience, then move to technical problem-solving. "I understand how frustrating that must be — let me help figure this out" before "What version are you on?"
- **Never go silent**: "Still investigating" is infinitely better than radio silence. Set a timer for SLA update cadence and never miss it. Silence destroys trust faster than any technical issue.
- **Reproduce before you escalate**: L2's highest-value work is reproduction. An issue that L3 can reproduce takes 10x less engineering time than one that's "sometimes it fails, idk." If you can't reproduce, say so and share what you tried.
- **Bug reports are your product**: A support engineer's most important engineering-facing output is the bug report. Include: environment, exact steps (numbered), actual vs expected, logs, screenshots, impact. A great bug report is resolved in hours. A bad one takes weeks of back-and-forth.
- **KB is your leverage**: Every hour spent writing a KB article saves 10+ hours of future support. Write for the customer's search query, not for the engineer's mental model. "Why can't I export my data?" not "Export Functionality Error Resolution."
- **SLAs are promises, not targets**: If you consistently hit FRT at minute 58 of a 60-minute SLA, you're one incident away from breach. Build 20% buffer into your workflow. Aim to respond before the SLA midpoint.
- **Customer health is a leading indicator of churn**: A customer with 10 tickets in a month, declining CSAT, and repeated issues is about to leave. Flag to Account Manager BEFORE they send the cancellation email.
- **Proactive > Reactive**: Update the status page when you discover an issue, not when customers discover it. A status page update at minute 1 is a minor inconvenience. A status page update after 100 customer complaints is a crisis.
- **Feature requests are product signals, not noise**: Track them. Categorize them. Report patterns weekly. The support team sees product gaps before anyone else. One request is noise. Ten identical requests from different customers in a month is a roadmap item.
- **Protect your team from abuse**: Have a policy for abusive customers. One warning, then restricted to email-only communication, then fired as a customer if it continues. Support engineers are not emotional punching bags.


### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Project misses deadline consistently | No buffer for unknowns | Add 20% schedule buffer for every phase. Track actual vs estimated to calibrate future planning. |
| Stakeholder disengaged | Updates don't answer their questions | Executive updates: progress toward milestones, blocking issues, decisions needed. Not activity reports. |
| Team demotivated | Retrospectives without action | Every retro must produce at least one action item with an owner. Track follow-through. |
| Scope keeps growing | No change control process | Formal change request: cost/impact assessment, approval gate, backlog vs current sprint decision. |
| Documentation nobody reads | Written for completeness, not task completion | Diátaxis framework: Tutorials (learning), How-to guides (tasks), Reference (facts), Explanation (understanding). |
| Customer churn repeats same issue | Symptoms addressed, root cause ignored | Five Whys on every recurring ticket. Escalate systemic issues, don't just reply to each report. |
| Cross-team meeting with no outcome | No written agenda or decision log | Every meeting must have: agenda shared 24h before, decision log during, summary sent within 1h of end. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Support tier structure defined: L1 (triage/KB), L2 (debug/reproduce/bug file), L3 (engineering escalation)
- [ ] **[S2]**  SLA framework implemented: FRT, Resolution Time, Update Cadence per severity level (SEV1-SEV4)
- [ ] **[S3]**  Support tool stack deployed: ticketing (Zendesk/Intercom/Linear), monitoring (Datadog/Sentry), KB (Notion/GitBook), comms (Slack Connect/email/in-app)
- [ ] **[S4]**  Escalation runbook documented for each severity and scenario (security, data, outage)
- [ ] **[S5]**  On-call rotation established with handoff process and escalation policy
- [ ] **[S6]**  Ticket triage workflow: categorize, prioritize, assign — with automation rules
- [ ] **[S7]**  Bug report template standardized with required fields: reproduction steps, environment, logs, impact
- [ ] **[S8]**  Knowledge base live with ≥20 articles covering top customer questions
- [ ] **[S9]**  Self-service funnel: chatbot, KB search, in-app help — with deflection rate measured
- [ ] **[S10]**  Customer communication templates: initial response, status update, resolution, delay notification, escalation
- [ ] **[S11]**  CSAT survey triggered on ticket close; NPS for enterprise accounts
- [ ] **[S12]**  Support metrics dashboard: CSAT, FRT (median + p95), Resolution Time (median + p95), Ticket Volume, Deflection Rate, Escalation Rate — reviewed weekly
- [ ] **[S13]**  Customer health dashboard: per-customer ticket trends, severity distribution, CSAT trend, repeat issues — reviewed weekly
- [ ] **[S14]**  Feature request tracker with categorization and weekly product feedback loop
- [ ] **[S15]**  Churn risk detection: automated flagging for customers with high ticket volume + low CSAT + repeat issues
- [ ] **[S16]**  Proactive communication setup: status page, changelog, in-app announcements, email for enterprise
- [ ] **[S17]**  Enterprise support package defined: Slack Connect, priority SLA, named contact, QBR cadence
- [ ] **[S18]**  Documentation feedback loop: KB gaps → doc requests → Technical Writer
- [ ] **[S19]**  Security incident handling procedure: secure ticket handling, escalation path, customer communication template, legal notification if required
- [ ] **[S20]**  Postmortem process for SLA breaches and SEV1 incidents: root cause, process improvement, action items

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **Internal**: `references/ticket-triage-template.md` — Ticket triage checklist: categorization, severity assessment, duplicate check, assignment, initial response template.
- **Internal**: `references/bug-report-template.md` — Engineering-quality bug report template: title, severity, environment, reproduction steps, logs, impact, suggested fix.
- **Internal**: `references/kb-article-template.md` — Knowledge base article template: customer-facing title, problem, solution, steps, screenshots, applicable versions, related articles.
- **Internal**: `references/customer-communication-templates.md` — Response templates for: initial acknowledgment, investigation update, resolution, delay notification, escalation, security incident.
- **Internal**: `references/sla-matrix-template.md` — SLA definition template: severity levels, FRT, resolution time, update cadence, business hours vs 24/7.
- **External**: [Zendesk Support Best Practices](https://www.zendesk.com/blog/customer-service-best-practices/) — Ticketing, automation, and customer experience best practices
- **External**: [Intercom Customer Support Handbook](https://www.intercom.com/blog/customer-support-handbook/) — Modern support operations and customer communication
- **External**: [Google SRE Handbook — On-Call](https://sre.google/sre-book/being-on-call/) — On-call best practices, alert fatigue, escalation
- **External**: [CSAT vs NPS vs CES](https://www.qualtrics.com/experience-management/customer/csat-vs-nps-vs-ces/) — Customer experience metrics: when to use each
- **External**: [Linear Method — Customer Feedback](https://linear.app/method/customer-feedback) — Triage and feedback loop with engineering
