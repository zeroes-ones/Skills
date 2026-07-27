# /test — Write and run tests following TDD methodology

Implement test-driven development: write failing tests first, then implement, then refactor. Follow the test pyramid (80% unit, 15% integration, 5% E2E).

**When to use**: Before implementing logic, after discovering a bug, or before refactoring.

**Workflow**:
1. Invoke `tdd-guide` skill for Red-Green-Refactor workflow
2. Write failing tests that define expected behavior
3. Implement minimal code to pass tests
4. Refactor while keeping tests green
5. Invoke `qa-engineer` for test quality review
6. Output: Passing test suite with coverage report

**What it produces**: Test files covering happy path, edge cases, error states, and concurrency. DAMP over DRY in test descriptions.
