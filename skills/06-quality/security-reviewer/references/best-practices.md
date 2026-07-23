# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
> **War story:** A startup passed SOC 2 Type I with a clean audit. Three months later, a researcher found an unauthenticated GraphQL introspection endpoint that exposed the entire schema, including internal mutation names like `adminResetUserPassword`. The endpoint had no rate limiting and no auth check — it was added in a 'minor refactor' that didn't trigger a security review because the PR title said 'clean up resolver naming.' **Fix:** Security review gates must trigger on file patterns, not PR labels. Any PR touching `graphql/`, `resolver/`, or `mutation/` paths gets an automatic security reviewer assignment regardless of how minor it looks.

- **Defense in depth**: Validate at every layer. A WAF does NOT excuse missing input validation in application code.
- **Assume breach**: Design for containment. Segment networks. Implement anomaly detection. A single vulnerability shouldn't compromise everything.
- **Shift-left**: Catch vulnerabilities in code review, not penetration testing. SAST in CI on every PR. DAST on every staging deploy.
- **Context is everything**: A theoretical XSS in an internal admin tool differs from XSS on a public e-commerce checkout. Adjust severity based on exposure, data sensitivity, and user population.
- **Fix root cause, not symptom**: Don't add WAF rules for SQL injection -- use parameterized queries. Don't sanitize output for XSS -- use context-aware encoding and CSP.
- **Positive reinforcement**: Highlight secure patterns. "Good use of parameterized queries here" and "Nice job validating with Zod at the boundary" reinforce good habits.
- **Security is quality**: Frame findings as bugs. Don't appeal to fear -- appeal to correctness and engineering excellence.
- **Know thy threat model**: A startup MVP has a different threat model than a bank. Calibrate review depth and severity to the actual risk.
