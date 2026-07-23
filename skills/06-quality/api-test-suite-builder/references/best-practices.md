# Best Practices

<!-- STANDARD: 3min -->

1. **One describe block per endpoint** — failures are instantly diagnosable. No scrolling.
2. **Seed minimal data** — create only what the test needs in `beforeAll`. Don't load the entire database.
3. **Assert response shape, not just status code** — a 200 with a missing field is a bug. Validate the full response schema.
4. **Use parametrized tests for validation matrices** — `it.each` (Vitest) or `@pytest.mark.parametrize` reduces 11 validation tests to 5 lines.
5. **Test that sensitive fields are ABSENT** — `expect(res.body).not.toHaveProperty('password_hash')` is as important as asserting presence.
6. **Always test the "missing header" case separately from "invalid token"** — they trigger different code paths and return different errors.
7. **Name tests descriptively** — `"returns 401 when token is expired"` not `"auth test 3"`. Test names are documentation.
8. **Use factories for test entities** — `createTestUser({ role: 'admin' })` not `{ id: 1, name: 'Admin' }`. Factories survive schema changes.
