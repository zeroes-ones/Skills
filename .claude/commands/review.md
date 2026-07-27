# /review — Review code for bugs, security, architecture, and maintainability

Run a comprehensive code review covering correctness, readability, architecture, security, and performance. Uses the `code-reviewer` persona for read-only analysis.

**When to use**: Before merging PRs, after significant changes, or during architecture reviews.

**Workflow**:
1. Invoke `code-reviewer` persona (read-only) with `code-reviewer` skill
2. Five-axis review: Correctness, Readability, Architecture, Security, Performance
3. Report findings with severity: CRITICAL (must fix), REQUIRED (should fix), NIT (nice to have)
4. Invoke `security-reviewer` for security-specific deep dive
5. Output: Review report with file paths, line numbers, and suggested fixes

**What it produces**: A structured review with actionable findings. No code modifications — findings only.
