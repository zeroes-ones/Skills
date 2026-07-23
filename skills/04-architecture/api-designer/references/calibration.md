# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You design endpoints by thinking about what your database schema looks like and exposing CRUD operations on each table | You design APIs by writing the consumer code first — the ideal client experience drives the endpoint shape, not the database schema — and you test every endpoint by integrating with it from a real SDK | A new developer integrates with your API in under 2 hours without reading documentation beyond the Quick Start guide — and when they hit an error, the response tells them exactly what to fix |
| Your error responses are `{"error": "something went wrong"}` with no structured format, no error codes, and no remediation hints | Every error response follows RFC 7807 with `type`, `title`, `status`, `detail`, and `instance` — and includes an actionable `hint` extension field telling the consumer what to do next | You deprecate a v1 endpoint used by 500+ active consumers and migrate 98% of them to v2 before the sunset date — with zero Sev1 incidents during the transition |
| You version APIs by slapping `/v2` on the URL and calling it a day — no deprecation policy, no migration guide, no sunset timeline | You maintain a public changelog, a deprecation calendar with 6-month notice periods, and automated emails to consumers whose traffic still hits deprecated endpoints | Your API design guidelines are adopted by 3+ teams outside your org, and an external developer writes a blog post titled "Why [Your Company]'s API is the best-designed I've ever used" |

**The Litmus Test:** Can a developer you've never met integrate with your API — authentication, first request, error handling, pagination — in under 15 minutes, without reading any documentation beyond the OpenAPI reference and the Quick Start guide?
