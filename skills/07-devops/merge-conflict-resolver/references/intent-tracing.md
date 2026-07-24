# Intent Tracing Guide

Step-by-step guide to tracing each side of a conflict back to its commit, PR, and issue with source hierarchy prioritization.

## Source Hierarchy (most → least authoritative)

1. **Linked issue** — problem statement, requirements, acceptance criteria (the "why")
2. **PR description** — approach, trade-offs, design decisions
3. **Commit message body** — implementation rationale, detailed context
4. **Commit message subject** — summary, but may lack nuance
5. **Code comments** in conflicting region — developer notes (may be stale)
6. **Diff context** — changed lines only (the "what", not "why")

## Tracing Commands

```bash
git log --oneline --no-merges <side-ref>..<base-ref> -- <file>
git log -1 --format="%B" <commit-hash>
git log -1 --format="%B" <commit-hash> | grep -oP 'Merge pull request #\K\d+'
```

## Intent Summary Template

For each hunk, build a summary: side identifier, what it changes, the commit hash, PR number, issue number, and what the change intends to accomplish.
