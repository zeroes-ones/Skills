# Restart Protocol

## Goal

A fresh agent reading a handoff document should resume productive work in under 5 minutes.

## Protocol

### Minute 1: Orient
1. Read the handoff summary paragraph
2. Note: branch, commit, working directory
3. Run the resume command
4. Verify: `git branch --show-current` matches handoff

### Minute 2: Understand State
1. Read the "In Progress" section — what was being edited?
2. Read the "Decisions" section — what was chosen and why?
3. Read the "Blockers" section — are any still active?

### Minute 3: Verify Environment
1. Run tests to confirm current state: `npm test` or equivalent
2. Check git status: `git status --short`
3. Verify dependencies: `npm install` or equivalent

### Minute 4: First Action
1. Execute "Next Steps" item #1
2. Verify expected outcome matches

### Minute 5: Update Ledger
1. Mark previous DOING: item as DONE: or update state
2. Set new DOING: item
3. Continue working

## Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Resume command fails | Branch deleted, file moved, tool unavailable | Check git log for branch name, locate file with `find`, install missing tool |
| Tests fail on fresh checkout | Missing env vars, uncommitted config | Check for `.env.example`, ask team for config |
| "In Progress" doesn't make sense | Too much time elapsed, code refactored | Git diff from ledger commit to HEAD, identify what changed |
| Blocker still active beyond ETA | Escalation didn't happen | Follow escalation path now, cc original requester |

## Restartability Score

After resuming, grade the handoff:
- **A:** Resumed in <2 minutes, first edit within 5 minutes
- **B:** Resumed in <5 minutes, minor clarification needed
- **C:** Resumed in <10 minutes, significant context missing
- **F:** Could not resume, had to start fresh
