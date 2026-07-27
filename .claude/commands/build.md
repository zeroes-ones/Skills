# /build — Implement tasks from the plan using thin vertical slices

Execute the plan with incremental implementation. Each task is a thin vertical slice — no horizontal layer development. Feature flags wrap new code. Every slice is independently committable.

**When to use**: After `/plan` produces an ordered task list. For new feature implementation.

**Workflow**:
1. Load the plan from `/plan`
2. Invoke `incremental-implementation` skill
3. Invoke `fullstack-developer` or domain-specific developer skill
4. Each slice: implement → test → commit → next
5. Invoke `code-reviewer` after each significant slice
6. Output: Working, tested, committed code

**What it produces**: Implemented features in independently-reviewable commits. Each commit is revertible. Feature flags default to OFF.
