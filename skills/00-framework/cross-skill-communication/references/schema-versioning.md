# Schema Versioning Protocol

## Semver Semantics for Skill Output Schemas

| Bump | Meaning | Example | Consumer Impact |
|------|---------|---------|-----------------|
| MAJOR (1.x→2.x) | Breaking change: field removed, type changed, required field added | `confidence` changed from integer to float | Consumers MUST update to parse new schema |
| MINOR (1.0→1.1) | New optional field added | Added `confidence_breakdown` object | Old consumers ignore new field. New consumers use it |
| PATCH (1.0.0→1.0.1) | Bug fix, no schema change | Fixed rounding in confidence score | No consumer impact |

## Dual-Publish Transition Protocol (MAJOR Bumps)

```

Day 0:  MAJOR bump announced. Deprecation notice on old version.
Day 1:  Skill begins publishing BOTH old and new schema versions.
Day 30: Deadline for all consumers to migrate.
Day 31: Old version retired. Skill publishes new version only.

IF any consumer hasn't migrated by Day 30:
├── Extend transition by 15 days
├── Flag non-migrated consumer
└── After extended deadline: retire old version. Non-migrated consumer will break.

```

## Consumer Migration Checklist

- [ ] Identify all messages consumed from the bumped skill
- [ ] Update message parsing to handle new schema
- [ ] Test with dual-published messages (both old and new formats)
- [ ] Deploy updated consumer
- [ ] Confirm consumer processes new schema correctly in production
- [ ] Report migration complete to producer
