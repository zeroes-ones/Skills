# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
> **War story:** A team reviewed a PR adding a new API endpoint. All 6 dimensions passed — correct logic, clean code, good tests, proper error handling. The reviewer skipped the dependency diff because "only one new import." That import was `pyjwt` (a third-party JWT library with a known CVE) instead of `PyJWT` (the maintained fork). The dependency was in production for 3 months before the security audit caught it. **Fix:** Never skip dependency review — verify every new import against the organization's approved list and SCA scan results.

- **Be specific and actionable**: "This query could cause an N+1 problem" → "Use `.include('author')` on the Prisma query at line 47 to eager-load authors in one query."
- **Explain the "why"**: Don't just say "use `useMemo`" — explain that the derived value recomputes on every render, causing downstream re-renders.
- **Suggest, don't demand**: Use "Consider...", "What do you think about...", "Could we..." for non-critical items.
- **Separate nitpicks from substance**: Use `nit:` or `suggestion:` prefixes so authors can filter.
- **Review in a timely manner**: < 4 hours for small PRs (< 200 lines), < 24 hours for large PRs. Code review is the #1 bottleneck in development velocity.
- **Automate what can be automated**: Linting, formatting, type checking, security scanning — leave human review for logic, design, and architecture.
