# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

Use this to diagnose where you actually are, not where you want to be.

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| Your spec documents are feature wishlists — a list of "the app should do X" without error states, data constraints, or dependency order | Your spec includes: entity state machines with every lifecycle transition, API contracts with error schemas for every endpoint, and screen definitions with loading/empty/error/edge states — and engineering can build from it without asking "what if this fails?" | An engineering manager hands your spec to a new hire who's never seen the product, and 2 weeks later the implementation matches what you described — no clarifying questions asked |
| You define APIs by describing the happy path response and assume errors are "the backend team's problem" | Every API endpoint in your spec has a response catalog: 200, 400, 401, 403, 404, 409, 422, 429, 500 — each with a real-world example payload | You define a spec for a system spanning 3 services and 2 teams, and 6 months later the integration tests pass on the first run because the contracts were unambiguous |
| You treat non-goals as an afterthought — a quick list at the bottom of the PRD | Your non-goals each have a documented rationale, a decision date, and a trigger for revisiting — and you've successfully defended a non-goal against a VP because the rationale was bulletproof | You're the person other PMs send their specs to with the message "can you find the holes in this?" — and you find at least 3 things they missed, every time |

**The Litmus Test:** Can you take a 30-minute product idea conversation, produce a complete spec (scope brief, domain model, API contract, screen inventory, prioritized story map, and non-goals with rationale) in 4 hours, and have an engineering lead say "I can estimate this without a follow-up meeting"? If the spec requires a meeting to explain it, the spec isn't done.
