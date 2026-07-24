# Handoff Template

## Quick Handoff (Same Agent, Same Day)

```markdown
# Quick Resume: [task]
- Branch: [name]
- File: [path]:[line]
- State: [one sentence]
- Next: [exact edit to make]
```

## Session Handoff (End of Day / Compaction)

```markdown
# Handoff: [task-name] — [YYYY-MM-DD HH:MM]

## Summary
[One paragraph: what we're doing, approach, current status]

## Completed
- DONE: [task] | [file] | Verified: [evidence]
...

## In Progress
- DOING: [task] | [file:line] | State: [mental state]

## Remaining
1. TODO: [concrete step]
2. TODO: [concrete step]
3. TODO: [concrete step]

## Decisions
- DECIDED: [decision] | Why: [rationale] | Cost: [tradeoff]

## Blockers
- BLOCKED: [description] | RESOLUTION: [cmd] | ETA: [date]

## Resume Command
[exact command to resume work]

## File Manifest
- [path] — [create/edit/delete] — [purpose]
```

## Cross-Agent Handoff (Different Agent/Team)

Adds to Session Handoff:

```markdown
## Project Context
[3-5 sentences: what this project is, key architecture decisions, tech stack]

## Architecture Summary
[Component diagram or dependency list]

## Testing Strategy
[How to run tests, what coverage means, where tests live]

## Orientation (5-Minute)
1. Read: [key file paths]
2. Understand: [core concepts]
3. Action: [first task to execute]
```

## Stakeholder Handoff (PM / Tech Lead)

```markdown
# Status Update: [project] — [YYYY-MM-DD]

## Progress
- [milestone]: [% complete] — [key accomplishment]
- [milestone]: [% complete] — [key accomplishment]

## Risks
| Risk | Severity | Mitigation | Owner |
|------|----------|------------|-------|
| ... | ... | ... | ... |

## Blockers
- [blocker] — needs: [what] from: [who] by: [when]

## Next Week
1. [goal]
2. [goal]
```
