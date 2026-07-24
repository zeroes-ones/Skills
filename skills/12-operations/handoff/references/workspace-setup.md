# Workspace Setup

## Directory Structure

```
.handoff/
├── ledger.md              # Active session ledger (single source of truth)
├── index.md               # Chronological index of all handoffs
├── handoff-YYYYMMDD-HHMM.md  # Individual handoff snapshots
├── archive/               # Completed or abandoned session ledgers
│   ├── 2026-07-15-auth-refactor.md
│   └── 2026-07-18-rate-limiter.md
└── templates/             # Reusable handoff templates
    └── stakeholder.md
```

## Initialization

```bash
# One-time setup per repository
mkdir -p .handoff/archive .handoff/templates
echo ".handoff/" >> .gitignore
touch .handoff/index.md
```

## Gitignore

The `.handoff/` directory MUST be git-ignored. Ledger files contain session-specific context (mental state, half-finished edits, speculative decisions) that should not be versioned.

## Index Maintenance

`.handoff/index.md` tracks all handoffs chronologically:

```markdown
# Handoff Index
- [2026-07-23 14:30] Rate limiter implementation — Session 3 of 5 — ACTIVE
- [2026-07-22 18:00] Rate limiter implementation — Session 2 of 5 — COMPLETED
- [2026-07-21 10:00] Auth refactor — Session 1 of 1 — ARCHIVED
```

## Archival Policy

* Archive a ledger when: work is completed, work is abandoned, or ledger is >30 days stale
* Archive command: `mv .handoff/ledger.md .handoff/archive/YYYY-MM-DD-task-name.md`
* Update index.md to reflect archived status
* Create fresh ledger if resuming archived work (reference old ledger, don't reuse)

## Workspace Health Command

```bash
# Check workspace health
ls .handoff/ledger.md 2>/dev/null && echo "Ledger: EXISTS" || echo "Ledger: MISSING"
grep -q ".handoff/" .gitignore 2>/dev/null && echo "Gitignore: OK" || echo "Gitignore: MISSING"
wc -l .handoff/ledger.md 2>/dev/null | awk '{print "Ledger lines:", $1}'
```
