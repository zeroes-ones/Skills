# Resolution Documentation

Template and best practices for the resolution log: what to record, format conventions, and long-term maintenance.

## Resolution Log Template

```markdown
# Merge Conflict Resolution Log
**Date:** YYYY-MM-DD
**Operation:** merge | rebase
**Source branch:** feature/xyz
**Target branch:** main

## Hunk 1: path/to/file.ts (lines 45-72)

**Strategy:** manual-merge
**OURS intent:** (from commit abc123, PR #1842) Adds TOTP 2FA flow
**THEIRS intent:** (from commit def456, PR #1901) Refactors auth to provider pattern
**Resolution:** Merged TOTP challenge into the new provider interface.
Both intents preserved: 2FA works through the pluggable provider system.
**Verification:** build ✓, unit tests ✓, integration tests ✓
```

## Format Conventions

- One entry per hunk
- Record the strategy used, both intents with source references, the resolution rationale, and verification results
- Commit the log alongside the merge: `.merge-conflict-resolution-log.md`

## Long-Term Maintenance

The resolution log serves as institutional memory. When the same files conflict again in future merges, the log explains the previous resolution and why it was chosen.
