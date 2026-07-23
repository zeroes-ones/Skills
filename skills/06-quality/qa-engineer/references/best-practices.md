# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
> **War story:** An engineer spent 2 days debugging a production incident where a background job processed 50K duplicate payments. Root cause: the idempotency key was generated from a request body field that the frontend sometimes omitted, defaulting to `None`. The idempotency check passed because `None` matched `None` across all 50K requests. **Fix:** Idempotency keys must be generated from fields that cannot be empty — use a server-assigned request ID from the first hop, not a client-supplied value.

- **Tests as documentation**: A good test suite explains what the system does. Test names should read like specifications.
- **Deterministic tests**: No `Date.now()`, `Math.random()`, or network calls in unit tests. Use seeded faker/falso for test data.
- **Test isolation**: Tests must not share state. Each test sets up and tears down its own context.
- **Fast feedback**: Unit tests < 5s for the full suite. Integration < 60s. E2E smoke < 5 min. Optimize aggressively.
- **Shift-left testing**: Catch bugs as early as possible. Test at the lowest pyramid level that can verify the behavior.
- **Tagging**: Tag tests by type (`@smoke`, `@regression`, `@slow`, `@flaky`) for selective execution in CI.
