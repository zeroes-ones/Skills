# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You run the test generator, see green, and merge — you don't read any of the generated tests | You audit every generated test suite: you identify which scenarios the generator missed, add manual tests for those gaps, and verify the assertions are testing behavior, not just status codes | You've built custom generators that encode your organization's specific threat model — auth roles, sensitive fields, business rules — and the generated suites catch bugs before human review |
| You configure coverage thresholds but never look at WHAT is covered — "85% lines" is your only metric | You run mutation testing on every PR and can explain why each surviving mutant escaped: "This mutant survived because we don't test what happens when the payment service returns a 504 after 3 retries" | You've reduced the escape rate of P0 bugs from your API by >50% — and you can prove it with 12 months of production incident data correlated to test suite changes |
| Your test data is a single JSON fixture with 3 users named "test1", "test2", "test3" | Your test factories generate realistic, varied data — different roles, edge-case values (null, empty, Unicode, 10MB payloads) — and every test creates its own isolated data | Developers add new endpoints and the tests are generated, reviewed, and passing within 10 minutes — and your framework is adopted by 3+ teams in the org |

**The Litmus Test:** Given an OpenAPI spec with 50+ endpoints, can you identify 3 categories of bugs that schema-based test generation will ALWAYS miss — and describe the manual tests you'd write to catch them? If your answer is only "business logic errors," you're not thinking deep enough. (Hint: race conditions, behavioral contracts, and resource lifecycle bugs.)
