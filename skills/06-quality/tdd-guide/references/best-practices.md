# Best Practices

<!-- STANDARD: 3min -->

1. **Time-box the cycle.** Red: 1-5 min. Green: 1-5 min. Refactor: 2-10 min. If any phase takes longer, the test is too big — split it.
2. **Test behavior, not implementation.** `expect(component.queryByText('Welcome'))` not `expect(component.state.isLoggedIn).toBe(true)`. Tests survive refactors when they assert what the user sees.
3. **One assertion per test (typically).** When a test has 5 assertions and fails on the 2nd one, you don't know if #3-5 would have failed. Multiple assertions for the same logical behavior are fine (e.g., checking multiple fields of a response).
4. **Tests should be DAMP (Descriptive And Meaningful Phrases), not DRY.** Some duplication in tests is good — each test should tell a complete story without jumping to helper functions.
5. **Don't test the framework.** If you're using Django REST, testing that `ModelSerializer` serializes fields correctly is testing Django, not your code. Test your business logic.
6. **Use the Given-When-Then structure.** Arrange (Given), Act (When), Assert (Then). Separate them with blank lines. Consistency makes tests scannable.
7. **Run tests on every save.** Use `pytest-watch` or `vitest --watch`. The feedback loop must be under 2 seconds for TDD to work.
8. **Mutation testing reveals weak tests.** If you can change the implementation logic and tests still pass, your assertions are too weak. Run mutation testing monthly on P0 code.
