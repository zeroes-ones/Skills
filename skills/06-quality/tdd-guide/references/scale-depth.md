# Scale Depth: Solo → Small → Medium → Enterprise

<!-- STANDARD: 3min -->

### Solo (1 developer, greenfield)
**Description:** Building an MVP. No existing tests. Fast iteration speed.
**Approach:** Classic TDD for business logic. Skip TDD for UI layout (visually driven). Time-box cycles strictly. Don't chase 100% coverage — test the behavior that matters. Property-based tests for core algorithms.
**Time investment:** 15-20% overhead initially. Pays off in reduced debugging time within 2 weeks.

### Small Team (2-10 developers, growing codebase)
**Description:** Active development. Some tests exist. Starting to feel the cost of manual testing.
**Approach:** Outside-in TDD for new features. Bug reproduction TDD for all fixes. Introduce mutation testing for P0 modules. Establish coverage gates (≥80%) in CI. Pair programming for TDD adoption. Weekly TDD kata sessions.
**Time investment:** Initial 2-4 week adoption period. After that, development speed is net faster.

### Medium Team (10-50 developers, multiple services)
**Description:** Multiple teams. CI/CD pipeline. Dedicated QA. Microservices or modular monolith.
**Approach:** Contract TDD between services. Test data factories as shared libraries. Property-based testing for shared utilities. Mutation testing in CI for all P0/P1 services. Outside-in TDD with acceptance tests driving service boundaries. TDD metrics tracked per team (cycle time, defect escape rate).
**Time investment:** Ongoing culture. Expect 10-15% of sprint time allocated to test quality improvement.

### Enterprise (50+ developers, compliance, high reliability)
**Description:** 500K+ lines of code. Regulatory requirements. Zero-downtime deployments.
**Approach:** Formal TDD policy. Characterization tests mandatory before any legacy refactor. Mutation testing gates block merges. Property-based testing for all business-critical pure functions. Automated test generation from specs for boilerplate. TDD training program for new hires. Test architecture decisions documented as ADRs. Annual TDD maturity assessment.
**Time investment:** Permanent investment. Dedicated test enablement team (2-3 people).
