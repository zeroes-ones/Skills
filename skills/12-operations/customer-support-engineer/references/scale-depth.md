# Scale Depth

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
