# Investigation Tickets

## Ticket Format

```markdown
# [TICKET-ID]: [One-line unknown summary]

## Unknown
We don't know [specific unknown statement].

## Classification
- Type: [BLOCKING | ORDERING | INDEPENDENT | NICE_TO_HAVE]
- Depends on: [list of ticket IDs, or "none"]

## Method
How we will investigate: [experiment, research, prototype, analysis, interview]

## Artifact
- Type: [decision doc | benchmark results | prototype | data analysis | landscape survey]
- Path: tickets/artifacts/[filename]
- Contains: [description of what the artifact will contain]

## Completion Criteria
- [ ] [Specific, verifiable condition 1]
- [ ] [Specific, verifiable condition 2]

## Status
- status: [pending | active | done | blocked | unknowable]
- sessions_active: [count]
- started: [YYYY-MM-DD]
- completed: [YYYY-MM-DD]

## Findings
[Populated after investigation — summary of what was learned]
```

## Investigation vs Implementation Ticket

| Dimension | Investigation Ticket | Implementation Ticket |
|-----------|---------------------|----------------------|
| Question | "What don't we know?" | "What do we need to build?" |
| Output | Knowledge artifact (doc, data, prototype result) | Working software |
| Completion | Unknown is resolved (answer known) | Feature is shipped |
| Success metric | Decision quality, knowledge coverage | Code quality, user value |
| Revisitable | Knowledge may be superseded by new info | Code is replaced by refactor |
| Owner | Wayfinder | Project-manager |

## Ticket Anti-Patterns

| Anti-Pattern | Example | Fix |
|-------------|---------|-----|
| Todo masquerading | "Investigate databases" — no method, no artifact | Add method + artifact specification |
| Implementation disguised | "Investigate by building a prototype" → produces production code | Cap prototype at spike/ directory, don't merge |
| Unknown inflation | 50 tickets for a 2-day task | Cluster related unknowns into single tickets |
| Dependency hoarding | Every ticket depends on one ticket → serial investigation | Only add dependencies where genuinely blocked |
