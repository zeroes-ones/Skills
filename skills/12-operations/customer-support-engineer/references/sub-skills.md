# Sub-Skills

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
