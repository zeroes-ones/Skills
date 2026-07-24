# CONTEXT.md Template

`CONTEXT.md` is the living, inline domain glossary stored at the project root. It evolves with every domain discovery.

## Template Structure

```markdown
# CONTEXT.md — [Project Name] Domain Glossary
Last updated: YYYY-MM-DD

## Bounded Contexts
| Context | Owner Team | Description |
|---------|------------|-------------|

## Core Terms
| Term | Definition | Context | Examples/Constraints |
|------|-----------|---------|---------------------|

## Edge Cases
| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|

## Domain Rules (cross-referenced to code)
| Rule ID | Rule | Code Location | Validated |
|---------|------|---------------|-----------|

## Term Drift Log
| Date | Term | Old Meaning | New Meaning | Reason |
|------|------|-------------|-------------|--------|
```
