## Decision Trees

<!-- QUICK: 60s -- flowchart-style logic for fork-in-the-road decisions -->

### Self-Serve vs Curated Dashboards
<!-- Decision tree for choosing between governed self-serve exploration and curated, locked-down dashboards -->

```
START: Stakeholder requests new dashboard or data access
  │
  ├─ Is the audience the board of directors, investors, or external partners?
  │    ├─ YES → CURATED. Locked dashboard with approved metric definitions. No self-serve.
  │    └─ NO → Continue
  │
  ├─ Does the data contain PHI, individually identifiable financial data, or material non-public information?
  │    ├─ YES → CURATED. Row-level security, audit trail, export restrictions.
  │    └─ NO → Continue
  │
  ├─ Is the metric definition stable, well-documented, and governed in the semantic layer?
  │    ├─ NO → CURATED. Do not expose ungoverned metrics in self-serve. Define first, then expose.
  │    └─ YES → Continue
  │
  ├─ Does the stakeholder have data literacy to interpret metrics correctly (understands rate vs count, MoM vs YoY, statistical significance)?
  │    ├─ NO → CURATED with narrative. Provide interpreted report rather than raw exploration.
  │    └─ YES → Continue
  │
  ├─ Is the stakeholder a power analyst who needs ad-hoc drill-down, cohort building, or cross-domain joins?
  │    ├─ YES → SELF-SERVE (exploratory tier). Label as "exploratory — not board-reviewed." Creator attribution visible.
  │    └─ NO → SELF-SERVE (governed tier). Curated dataset. Locked metric tiles. Pre-built drill paths.
  │
  └─ FINAL GATE: Will a wrong number from this dashboard reach investors, regulators, or patients?
       ├─ YES → Require peer review and stakeholder sign-off before self-serve access.
       └─ NO → SELF-SERVE with freshness SLA label and "last reviewed" timestamp.
```

### When to Build a Semantic Layer vs Direct Queries
<!-- Decision tree for choosing between a governed semantic layer and direct database queries -->

```
START: Need to expose data for reporting or analysis
  │
  ├─ Will this metric be used by more than one person, team, or dashboard?
  │    ├─ YES → SEMANTIC LAYER. Define once, use everywhere.
  │    └─ NO → Continue
  │
  ├─ Is the metric business-critical (ARR, NRR, churn, gross margin, patient outcomes)?
  │    ├─ YES → SEMANTIC LAYER. Must have single authoritative definition with governance.
  │    └─ NO → Continue
  │
  ├─ Does the metric require calculation logic beyond simple aggregations (e.g., LTV/CAC, magic number, risk-adjusted outcomes)?
  │    ├─ YES → SEMANTIC LAYER. Complex logic should be versioned, tested, and governed.
  │    └─ NO → Continue
  │
  ├─ Is this a one-off analysis with a shelf life of <1 week (ad-hoc board question, urgent investor request)?
  │    ├─ YES → DIRECT QUERY with documentation. Promote to semantic layer if the question recurs.
  │    └─ NO → Continue
  │
  ├─ Are you exploring a new data source where metric definitions are still being iterated?
  │    ├─ YES → DIRECT QUERY in exploratory tier. Formalize when definitions stabilize.
  │    └─ NO → SEMANTIC LAYER.
  │
  └─ Does the query need to join across domains that have separate semantic layers?
       ├─ YES → SEMANTIC LAYER federation or cross-domain model. Do not bypass governance for cross-domain joins.
       └─ NO → SEMANTIC LAYER.
```
