# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Support Tier Design & Setup

1. **Define tiers**: L1 (triage, KB lookup, basic troubleshooting, account issues), L2 (technical debug, reproduction, log analysis, bug filing), L3 (engineering escalation, code fix, architecture-level). Output: tier definitions with SLA per tier.
2. **SLA framework**: First Response Time (FRT), Resolution Time, Update Cadence. Per severity level. Output: SLA matrix documented and tool-configured.
3. **Tool stack selection**: Ticketing (Zendesk, Intercom, Linear), monitoring (Datadog, Sentry, Grafana), communication (Slack Connect for enterprise, email, in-app chat), KB (Notion, GitBook, Zendesk Guide). Output: tool stack document.
4. **Escalation path**: L1 → L2 → L3 → Engineering on-call → Incident Commander. Document for each severity + scenario (security, data, outage). Output: escalation runbook.
5. **On-call rotation**: Define schedule, handoff process, escalation policy. Output: on-call schedule + runbook.

<!-- DEEP: 10+min -->
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

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Bug Reporting to Engineering

1. **Quality bug report**: Title (concise, descriptive), severity, environment, reproduction steps (numbered, exact), expected vs actual behavior, logs/screenshots, impact (customers affected, business impact), suggested fix (optional). Output: bug ticket meeting engineering quality bar.
2. **Prioritization alignment**: Review with engineering or product. Confirm severity and priority. Discuss if hotfix or next sprint. Output: prioritized bug with committed timeline.
3. **Follow-through**: Track bug status. If SLA at risk → escalate. Update customer with progress. Output: linked support ticket updated.

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Knowledge Base & Self-Service

1. **KB article creation**: For every issue resolved that could recur: title (as customer would search), problem description, solution steps, screenshots, applicable versions. Output: published KB article.
2. **KB maintenance**: Quarterly audit: are articles accurate for current version? Are top search queries covered? Update or archive stale articles. Output: KB health report.
3. **Self-service strategy**: Chatbot for L1 deflection (common Q&A, KB search). In-app help widget. Public status page. Output: self-service funnel metrics (% deflected).
4. **Documentation feedback loop**: When KB articles reveal documentation gaps, file doc requests to Technical Writer. Output: doc improvement tickets.

<!-- DEEP: 10+min -->
### Phase 6 (~25 min): Proactive Support & Customer Health

1. **Customer health signals**: Track per-customer: ticket volume trend, severity distribution, resolution time, CSAT trend, repeated issues (same bug re-reported). Output: customer health dashboard.
2. **Churn risk detection**: Red flags: increasing ticket volume, decreasing CSAT, repeated unresolved issues, "cancellation" or "competitor" keywords in tickets, executive escalation. Output: churn risk alert to Customer Success/Account Manager.
3. **Proactive communication**: Update status page BEFORE customers report. Announce known issues in-app. Send changelog for fixes. Output: proactive communication cadence.
4. **Enterprise customer support**: Dedicated Slack Connect channel. Priority SLA. Named support contact. Quarterly business review (QBR) with support metrics. Output: enterprise support package.

<!-- DEEP: 10+min -->
### Phase 7 (~25 min): Metrics & Continuous Improvement

1. **Support metrics tracking**: CSAT (target >90%), NPS, CES (Customer Effort Score), First Response Time (median + p95), Resolution Time (median + p95), Ticket Volume, Deflection Rate, Escalation Rate. Output: weekly metrics dashboard.
2. **Trend analysis**: Weekly: top issue categories, emerging patterns, team bottlenecks. Output: weekly support insights report.
3. **Retrospective & improvement**: Monthly: what went well, what broke, what process needs to change. Output: improvement action items.
