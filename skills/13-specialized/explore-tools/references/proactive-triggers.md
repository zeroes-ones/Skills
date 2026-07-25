# Proactive Triggers

These are signals that should trigger the explore-tools specialist to investigate — no one needs to tag you; you should be watching for these.

| Trigger | Immediate Action |
|---------|-----------------|
| "Tool stack costs have doubled in 3 months" | Run cost audit across all tools: check utilization vs idle, verify license tier correct for actual usage, audit per-seat vs consumption pricing, check if any free-tier alternatives have closed the gap. A single wrong-tier SaaS subscription can quietly burn $2K-$10K/month |
| "Team spending 40% of sprint on tool configuration, not building" | Re-evaluate tool complexity vs team throughput. If configuration overhead exceeds build time, the tool is a net negative regardless of feature set. Consider lower-friction alternatives even if they're "less capable" on paper |
| "New open-source tool released replaces 3 tools in stack" | Immediately evaluate: does it actually consolidate use cases or is it "80% solution"? If real consolidation, calculate migration cost vs ongoing maintenance of 3 separate tools. One tool replacing three at 80% capability each is often better than three at 95% each |
| "Security vulnerability discovered in core tool" | Check if actively exploited, if patch exists, whether usage pattern affected. If no patch: evaluate alternatives within 48 hours. Do not wait for vendor response on critical CVEs — have migration plan ready |
| "Free tier of a paid tool you recommended has expanded to cover client's needs" | Notify immediately. Free tier expansions change cost equations dramatically. Log in tools register, update recommendation matrix, flag as trigger for re-evaluation at next checkpoint |
| "Tool deprecated or acquired and EOL announced" | Begin migration planning within 1 week. Acquisitions = certain feature stagnation. EOL announcements have fixed timelines — start migration before customers ask |

## Escalation Path

```
Cost over-run exceeding 50% of budget? → CFO/Finance → CEO Strategist
Critical vulnerability in production tool? → Security Engineer → Incident Responder
Tool EOL with no clear alternative? → System Architect → CTO Advisor
Build vs buy analysis shows build wins? → Engineering Manager → VP Engineering
```
