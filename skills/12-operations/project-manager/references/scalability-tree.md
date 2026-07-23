# Scalability Decision Tree

```
How long is the project?
├── <2 weeks → TODO list in GitHub Issues. No Gantt, no WBS. Just a checklist with owners.
└── 2 weeks to 2 months → WBS + dependency map + weekly status. Google Sheets sufficient.
    └── >2 months → Full plan with Gantt, RAID, communication plan, phase gates.

How many people involved?
├── 1-3 → Async status updates in Slack. Lightweight planning.
├── 3-10 → Weekly sync (30 min max). RAID log. Written status updates.
└── 10+ → Structured communication plan. Different info for execs vs team vs stakeholders.

Are there external dependencies (other teams, vendors, APIs)?
├── YES → Dependency tracking becomes critical. Flag external deps in RAID with owner + due date.
│   External dependencies are the #1 cause of project delays.
└── NO → Internal alignment is simpler. Focus on sequencing, not negotiation.

Is the budget >$50K or is there a contract with penalties?
├── YES → Formal change control, earned value tracking, regular financial reporting.
└── NO → Lightweight budget tracking. Check monthly not weekly.

Are stakeholders asking for "more visibility"?
├── YES → Create a self-serve dashboard. Don't send more emails. Stakeholders pull, not PM push.
└── NO → Current communication is sufficient. Don't create reports nobody reads.
```


**What good looks like:** Project charter signed by sponsor. WBS decomposed to tasks under 80 hours. RAID log reviewed weekly. Status report sent on schedule with milestones, risks, and decisions needed. Project completes within 10% of estimated timeline.
