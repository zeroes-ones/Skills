# /copilot-skill plan — Decompose a spec into an ordered task list with dependency graph

Route the current spec through `project-manager` and `scrum-master` skills for vertical slicing into implementable tasks with dependency tracking.

**When to use**: After `/spec` produces a PRD. Before `/build` begins implementation.

**Workflow**:
1. Load the PRD from `/spec`
2. Invoke `project-manager` — feature prioritization with RICE scoring
3. Invoke `scrum-master` — sprint planning, vertical slicing, task decomposition
4. Output: Ordered task list with dependencies, effort estimates, and acceptance criteria

**What it produces**: A dependency-ordered task list. Each task: Objective, Files, Acceptance Criteria, Verification steps.
