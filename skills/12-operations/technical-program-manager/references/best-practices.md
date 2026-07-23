# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **TPM ≠ PM + technical knowledge**: A TPM manages technical *alignment* across teams, not project tasks within a team. If you're updating Jira tickets, you're doing PM work, not TPM work.
- **Contract first, implement second**: Before Team A builds an integration with Team B, agree on the API contract (OpenAPI spec, event schema, gRPC proto). Version it. Both teams build against the contract. This is the single highest-leverage TPM practice.
- **ADR before implementation, not after**: Architecture Decision Records capture *why* a decision was made. Without them, 6 months later no one remembers why Redis was chosen over Memcached and the program pays for it again.
- **Dependency map is your program's skeleton**: If you can't draw the dependency graph, you don't understand the program. Every dependency must have: owner team, blocking team, committed date, buffer. If a dependency has no owner, it WILL slip.
- **Bad news ages like milk**: If a critical path dependency slips, escalate within 24 hours. A 3-day slip caught early is a scope negotiation. A 3-week slip caught late is a crisis.
- **One decision-maker per decision**: RACI is not optional at scale. Every decision in the decision log must have exactly one "A" (Accountable). "Everyone agrees" without a named decider = no one decides.
- **Program health is a lagging indicator of dependency health**: If all dependencies are on track, the program is on track. Track dependency health obsessively. Program health dashboards that don't include dependency status are lying to you.
- **Dual-run everything for migrations**: Never cut over in one big-bang. Old system and new system run in parallel. Ramp traffic gradually. Verify data consistency. Have a rollback path. Sunset only when new system reaches 100% for 1 full cycle.
- **Estimate with uncertainty, communicate with confidence intervals**: "Q3" is not a date. "Q3 with 80% confidence" is. Use PERT: (optimistic + 4×most-likely + pessimistic) ÷ 6. Share the range, not a single date.
- **The TPM's output is decisions, not documents**: Every artifact (charter, ADR, status report, risk register) exists to drive a decision. If no decision is being made, stop producing the artifact.
