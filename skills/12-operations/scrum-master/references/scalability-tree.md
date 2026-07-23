# Scalability Decision Tree

```
Is your team size >7 people?
├── YES → Split into 2 teams. Optimal size: 5-7. Don't scale one team to 12.
└── NO → Single team is fine.

Are sprints consistently finishing with >30% carryover?
├── YES → <!-- DEEP: 10+min -->
Root cause: overcommitment? scope creep? unplanned work? Fix the cause.
└── NO → Carryover <20% is healthy.

Is velocity variance >30% sprint-over-sprint?
├── YES → Inconsistent sizing, team changes, scope changes. Stabilize.
└── NO → Stable enough for forecasting. Use 3-sprint rolling average.

Is cycle time >5 days for "ready to done" on average?
├── YES → Bottleneck. Check CFD. Apply WIP limits at constraint.
└── NO → Cycle time is healthy.

Are retro action items being completed?
├── YES → Improvement loop working.
└── NO → Reduce to 1 action item. Track visibly. Build the habit.

Do you have >3 teams on the SAME product?
├── YES → Cross-team coordination needed. Nexus or LeSS. Single Product Backlog.
└── NO → No scaling framework needed.
```


**What good looks like:** Team velocity tracked for 5+ sprints with predictable range. Sprint goal achieved in 8 of 10 sprints. Retro produces action items tracked to completion. Impediments removed within 24 hours. Team health score > 4/5 in retro survey.
