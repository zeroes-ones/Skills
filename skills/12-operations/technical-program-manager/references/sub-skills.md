# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **Program Scoping** | New program initiation. Ambiguous problem space. Multiple stakeholders with conflicting priorities. | Define problem statement, success criteria, scope boundaries, stakeholder map, program charter. |
| **Dependency Management** | Cross-team initiative with 5+ inter-team dependencies. External vendor/API dependencies. | Map dependencies by type (technical, resource, external). Track owners, committed dates, buffers. Weekly dependency review. |
| **Technical Design Review Facilitation** | Solution architecture is ambiguous. Multiple valid approaches exist. Teams disagree on technical direction. | Schedule TDR, invite senior engineers from all affected teams, facilitate option generation and trade-off analysis, drive to ADR. |
| **ADR & RFC Process** | Architecture decision cross-cuts teams. Public API or contract change. Build-vs-buy decision. | Write ADR (context, decision, alternatives, consequences). RFC for public contracts. Circulate 1-2 weeks. Decide and communicate. |
| **Roadmap & Milestone Planning** | Program spans >2 months. Multiple teams with sequenced deliverables. External commitments with dates. | Create milestone timeline (5-8 milestones). Define entry/exit criteria per milestone. Track progress weekly. |
| **Stakeholder Communication** | >3 stakeholder groups with different information needs. C-level sponsor. External stakeholders. | RACI for decisions. Weekly 1-page exec summary. Monthly program review. Self-serve dashboard for status. |
| **Risk & Change Management** | High-uncertainty program. Fixed external deadline. Novel technology. Resource-constrained. | Risk register with T-shirt sizing (L/M/S), probability, impact, mitigation. Change control: impact analysis → options → decision. |
| **API Contract Negotiation** | Teams need to agree on API contracts. Migration from one API version to another. Event schema changes spanning teams. | Contract-first approach. OpenAPI/gRPC/AsyncAPI specs. Versioning strategy. Deprecation policy. Contract testing. |
| **Migration Program Management** | System deprecation. Platform migration. Data migration. Dual-run transition. | Define: cutover criteria, rollback plan, data verification, sunset date. Track: % traffic on new system. Sunset old system only after 100% migration. |
| **Program Health & Metrics** | Sponsor asks "are we on track?" Need objective program health data. | Metrics: milestone progress (on-track/at-risk/blocked), risk score, burndown/velocity, dependency health, team satisfaction. Dashboard auto-updated weekly. |
