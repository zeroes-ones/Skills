# Progress Ledger

## The Pattern

The progress ledger is the single source of truth for multi-session work. It lives in `.handoff/ledger.md`, is git-ignored, and persists across session compaction. The ledger captures every decision, blocker, and completed task so a fresh agent can resume without reading conversation history.

## Core Principle

**Trust the ledger and git log over your own recollection.** Context windows are ephemeral — the ledger is not.

## Ledger Format

```markdown
# Session Ledger: [task-name]

## Context
- Branch: [branch name]
- Commit: [commit hash at session start]
- CWD: [working directory]
- Task: [one-sentence description]

## Completed
- DONE: [task description] | [file path] | Verified: [verification evidence]
- DONE: ...

## In Progress
- DOING: [current focus] | [file:line] | State: [mental state, what to do next]

## Remaining
1. TODO: [concrete next action with file path]
2. TODO: ...

## Decisions
- DECIDED: [decision] | Options: [a, b, c] | Chose: [x] | Rationale: [why] | Tradeoff: [what we gave up]

## Blockers
- BLOCKED: [description] | RESOLUTION: [verifiable command] | ETA: [date] | ESCALATION: [trigger + contact]

## Next Steps
1. [concrete step] — expected: [outcome]
2. ...
```

## Machine-Parseable Prefixes

- `DONE:` — completed tasks with verification
- `DOING:` — current in-progress work with exact line and state
- `TODO:` — remaining work, concrete and ordered
- `DECIDED:` — decisions with options, rationale, and tradeoffs
- `BLOCKED:` — blockers with resolution condition, ETA, escalation

## Anti-Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll remember what to do next" | Context windows are ephemeral; you won't |
| "The git log tells the story" | Git shows what changed, not why or what's left |
| "It's only a short break" | Short breaks become long breaks; the ledger costs 2 minutes |
| "The code documents itself" | Code documents what is, not what was decided and why |
