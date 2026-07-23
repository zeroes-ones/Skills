---
name: tdd-guide
description: Test-Driven Development guide — red-green-refactor cycle with explicit refactoring recognition triggers, coverage analysis, property-based and mutation testing, and outside-in TDD patterns. Use when adopting TDD, writing tests-first, improving test quality, or introducing TDD practices to a team.
author: Sandeep Kumar Penchala
type: quality
status: stable
version: 1.0.0
updated: 2026-07-22
tags:
- tdd-guide
- tdd
- test-driven-development
- testing
- code-quality
chain:
  consumes_from:
  - backend-developer
  - code-reviewer
  - frontend-developer
  - fullstack-developer
  - idea-to-spec
  - qa-engineer
  feeds_into:
  - accessibility-testing
  - backend-developer
  - code-reviewer
  - frontend-developer
  - fullstack-developer
  - mobile-developer
  - qa-engineer
token_budget: 3800
output:
  type: code
  path_hint: tests/
---
# TDD Guide

Rigorous Test-Driven Development with explicit red-green-refactor cycle recognition, property-based testing, mutation testing, and outside-in workflow. Knows when to refactor, when to delete tests, and what to measure.

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

```
Request: "Help me with TDD..."
├── ...for a new feature? → Jump to Core Workflow (Red-Green-Refactor)
├── ...but I'm new to TDD? → Start at Best Practices (1-5)
├── ...for an existing codebase with no tests? → Jump to Error Decoder (Legacy Codebase)
├── ...for a bug fix? → Jump to Decision Trees (Bug Fix TDD Pattern)
├── ...and I want to evaluate test quality? → Jump to Mutation Testing section
└── Not sure?
    → Run: tell me what you're building. I'll guide you through the first cycle.
```

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

1. **Red first. Always.** Write a failing test before writing a single line of implementation. If you didn't see it fail red, you don't know if the test actually tests anything.
2. **The smallest possible green.** Once red, write only enough code to make the test pass — no abstraction, no "I'll need this later." Premature abstraction is the #1 TDD anti-pattern.
3. **Refactor only when duplication exists.** Refactoring is not "making the code prettier." It has a specific trigger: you see duplication (once and only once rule broken) OR the code doesn't express intent clearly.
4. **Tests are executable specifications.** A test name should describe behavior: `"returns 0 balance for new accounts"` not `"test getBalance"`. Anyone reading the test file should understand what the system does.
5. **Delete tests that don't earn their keep.** Tests that never fail, test implementation details, or duplicate other tests should be removed. Test maintenance cost is real.

## The Expert's Mindset

TDD is not about testing — it's about **using tests as a design tool to produce loosely coupled, highly cohesive code with a safety net that enables fearless refactoring**. The tests are a side effect; the real product of TDD is better design.

### Mental Models

| Model | Description |
|---|---|
| **Tests as specification, not verification** | A test describes what the code should do, in executable form. The test suite IS the spec. If you want to know what the system does, read the tests, not the documentation. |
| **Red-Green-Refactor is a design loop, not a testing loop** | Red: define the interface. Green: make it work (simplest possible). Refactor: make it clean. The design emerges during refactoring, not during green. |
| **The tests drive the design, not follow it** | If a class is hard to test, the design is wrong — the class does too much, has hidden dependencies, or couples concerns. TDD surfaces design problems before they're baked in. |
| **Fast feedback is the point** | The value of TDD is not catching bugs (though it does). It's getting feedback on your design in seconds instead of waiting for integration testing or production. |

### Cognitive Biases in TDD

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Premature abstraction** | Writing "flexible, reusable" code during the green phase instead of the simplest thing | Strict red-green-refactor: no abstraction in green. Duplication must exist before you eliminate it. |
| **Testing implementation, not behavior** | Tests that verify internal method calls, private state, or exact sequence of operations | Test only public behavior: given input X, expect output Y. If you change the implementation without changing behavior, tests should still pass. |
| **Coverage theater** | Writing tests to hit coverage metrics, not to verify behavior | Never add a test "for coverage." Only add tests that describe behavior you care about. |
| **Test-last rationalization** | Writing the code first, then retrofitting tests that "prove" it works | If you didn't see the test fail, you don't know if it's testing the right thing. Red first, always. |

### What Masters Know That Others Don't

- **The best TDD practitioners delete more tests than they write.** Every test has a maintenance cost. A test that duplicates another test, tests a trivial getter, or couples to implementation details should be deleted. The goal is a lean, meaningful test suite.
- **TDD is not always the right tool.** Exploratory code, throwaway prototypes, and UI layout don't benefit from TDD. Know when TDD adds value and when it adds ceremony. The master knows when NOT to TDD.
- **The refactor step is where skill shows.** Anyone can make tests pass. The difference between competent and master is what the code looks like after refactoring. The refactor step is where patterns, principles, and taste are applied.
- **Tests are the first consumer of your API.** If the test is awkward to write, the API is awkward to use. This is the single most valuable design insight TDD provides.

## Operating at Different Levels

TDD skill manifests in the sophistication of test design — from writing tests for individual functions to designing testability into system architecture.

| Level | TDD Output Characteristics |
|---|---|
| **L1 — Apprentice** | Follows red-green-refactor cycle for simple functions. Writes unit tests before implementation. |
| **L2 — Practitioner** | TDDs features independently. Test doubles, test organization, and test naming conventions. Writes tests that document behavior. |
| **L3 — Senior** | Designs testable architecture. Identifies test boundaries and seam points. "This design is hard to test because..." Mentors on TDD craft. |
| **L4 — Staff/Principal** | Sets TDD standards for the org. Test strategy, testing pyramid design, test infrastructure. "This is how we test here." |
| **L5 — Industry-level** | Creates testing methodologies and TDD approaches adopted across the industry. |

**Usage**: Say "as an L2 practitioner, TDD this feature" or "as an L3 senior, help me design this for testability." Default: **L2** (independent TDD execution).

## When to Use
<!-- QUICK: 30s — scan the bullet list to decide -->

- Adding a new feature — let the tests define the API before you implement it
- Fixing a bug — reproduce the bug as a failing test first (proves the fix works)
- Refactoring legacy code — add characterization tests before touching anything
- Onboarding a team to TDD — use the structured cycle as a teaching tool
- Evaluating test quality — mutation testing reveals weak assertions
- Complex business logic — property-based testing catches edge cases manual testing misses
- API or library design — outside-in TDD produces usable APIs by design

## Decision Trees
<!-- STANDARD: 3min -->

### TDD Approach Selection

```
What best describes the situation?
├── New feature from spec → Outside-In TDD (start at acceptance test, work inward)
├── New utility function → Classic TDD (unit test → implementation → refactor)
├── Bug fix → Bug Reproduction TDD (failing test reproducing bug → fix → test stays)
├── Legacy code (no tests) → Characterization TDD (write tests for current behavior → refactor safely)
├── API endpoint → Outside-In TDD (integration test → controller test → service test → model)
└── Complex algorithm → Property-Based TDD (invariants, not examples)
```

### Refactoring Recognition

```
Do you see these signals?
├── Duplication (same logic in 2+ places) → Extract shared method
├── Test name doesn't match what the code does → Rename test, verify it still passes
├── Test setup is >10 lines → Extract factory or fixture
├── Magic numbers in tests → Replace with named constants
├── Long method (>15 lines) → Extract smaller methods, verify tests still pass
├── Multiple assertions testing different behaviors → Split into separate test cases
└── None of the above → Don't refactor. Move to next test.
```

## Core Workflow
<!-- STANDARD: 5min -->

### The TDD Cycle

```
┌──────────────────────────────────────────────────────┐
│                     RED (1-5 min)                     │
│  Write exactly ONE failing test.                     │
│  Run it. Watch it fail.                              │
│  If it doesn't fail → the test is wrong. Fix it.     │
└───────────────────┬──────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│                   GREEN (1-5 min)                     │
│  Write the MINIMUM code to make the test pass.       │
│  No abstraction. No "I'll need this later."          │
│  Run the test. All tests green? Move on.             │
└───────────────────┬──────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│                 REFACTOR (2-10 min)                   │
│  TRIGGER CHECK: Is there duplication?                │
│  TRIGGER CHECK: Does code express intent poorly?     │
│  If NO to both → SKIP REFACTOR. Start next test.     │
│  If YES → Refactor. Run ALL tests after each change. │
└───────────────────┬──────────────────────────────────┘
                    │
                    ▼
              Start next test
```

### Phase 1: Red — Write a Failing Test

```python
# Example: Building a BankAccount.transfer() method
# RED phase — write the test first

def test_transfer_moves_money_between_accounts():
    # Arrange
    alice = BankAccount(balance=100)
    bob = BankAccount(balance=0)

    # Act — this method doesn't exist yet!
    alice.transfer(to=bob, amount=50)

    # Assert
    assert alice.balance == 50
    assert bob.balance == 50

# Run: pytest → FAILS because BankAccount has no transfer() method
```

**Rules for the Red phase:**
- Exactly ONE failing test at a time. No batch test writing.
- The test must fail for the RIGHT reason (missing method, not a typo).
- If the test passes without writing code → your test is wrong. It's not testing anything new.
- Write the assertion first, then work backward to the arrange/act.

### Phase 2: Green — Minimum Code to Pass

```python
# GREEN phase — minimal implementation

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def transfer(self, to, amount):
        self.balance -= amount   # Simplest possible thing
        to.balance += amount     # No error handling yet

# Run: pytest → PASSES
```

**Rules for the Green phase:**
- Write the absolute minimum code. Copy-paste is fine at this stage.
- Don't add validation, error handling, or abstraction. That comes from tests that demand it.
- If you're tempted to "just add this one thing" → write a test for it instead.
- Run all tests (not just the new one). Green phase isn't done if you broke something else.

### Phase 3: Refactor — Only When Triggered

```python
# REFACTOR phase — triggered by next test that says "insufficient funds"
# After adding test_transfer_fails_when_insufficient_funds():

def transfer(self, to, amount):
    if self.balance < amount:             # Duplication trigger —
        raise InsufficientFundsError()    # this validation appears
    self.balance -= amount               # in multiple places
    to.balance += amount

# Now refactor: extract validation, add type hints, clean up
```

**Refactoring triggers (AND NOTHING ELSE):**
1. **Duplication** → Same logic appears in 2+ places. Extract it.
2. **Poor expressiveness** → Code doesn't clearly say what it does. Rename, restructure.
3. **Test structure smell** → Setup is too long, magic numbers, test name unclear.

### Outside-In TDD (for API/feature development)

```
Acceptance Test (RED)
    ↓
Controller Test (RED)
    ↓
Service Test (RED)
    ↓
Model Test (RED)
    ↓
Model Implementation (GREEN)
    ↓
Service Implementation (GREEN)
    ↓
Controller Implementation (GREEN)
    ↓
Acceptance Test (GREEN)
    ↓
Refactor (if triggered)
```

Start at the outermost layer (what the user sees) and work inward. Each failing test drives the design of the next layer down. This ensures you build only what the outer layer actually needs — no speculative inner-layer features.

### Bug Fix TDD Pattern

```
1. Reproduce the bug as a failing test
   → This proves you understand the bug
2. Run the test → RED (test reproduces the bug)
3. Fix the bug → GREEN
4. Add 2-3 edge-case tests around the fix area
   → What if the input is negative? What if it's zero? What if it's the max value?
5. Refactor if triggered
6. Leave the bug-reproduction test in the suite
   → This is now a regression test. It prevents this bug from ever returning.
```

### Property-Based Testing (for complex logic)

Instead of writing individual examples, define **invariants** that must always hold true:

```python
from hypothesis import given, strategies as st

@given(
    amount=st.integers(min_value=1, max_value=10000),
    initial_balance=st.integers(min_value=0, max_value=100000),
)
def test_transfer_preserves_total_money(amount, initial_balance):
    """Invariant: Total money in the system is constant after any transfer."""
    alice = BankAccount(balance=initial_balance)
    bob = BankAccount(balance=0)
    total_before = alice.balance + bob.balance

    alice.transfer(to=bob, amount=min(amount, initial_balance))
    total_after = alice.balance + bob.balance

    assert total_before == total_after
```

This single test explores thousands of random input combinations. Use for: financial calculations, data transformations, parsers, serializers, any pure function with clear invariants.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What to Expect | Communication Trigger |
|---------------|----------------|---------------------|
| `backend-developer` | Backend implementation patterns, API design, database schemas to test against | When new endpoint or service is added — define tests before implementation |
| `code-reviewer` | Test quality feedback, assertion strength review | During code review — reviewer checks that tests were written first |
| `frontend-developer` | Component patterns, UI behavior specs to drive component tests | When new component is designed — write behavior tests first |
| `fullstack-developer` | End-to-end feature requirements spanning FE and BE | When full-stack feature begins — outside-in TDD from acceptance test |
| `idea-to-spec` | Feature specifications, acceptance criteria, user stories | When spec changes — update acceptance tests first |
| `qa-engineer` | Test pyramid strategy, coverage thresholds, quality gates | When QA defines quality standards — align TDD practices |

| Downstream Skill | What to Deliver | Communication Trigger |
|-----------------|-----------------|---------------------|
| `accessibility-testing` | TDD patterns for accessibility — test a11y behavior before implementation | When building UI components — a11y assertions as part of red-green-refactor |
| `backend-developer` | TDD workflow, test-first patterns, property-based test templates | When starting a new feature — establish tests before implementation |
| `code-reviewer` | Mutation testing reports, test quality metrics for review | During code review — provide test assertion strength data |
| `frontend-developer` | Component TDD patterns, React Testing Library workflows | When building new components — define behavior via tests first |
| `fullstack-developer` | Outside-in TDD across FE/BE boundary, integration test patterns | When building end-to-end features — acceptance test drives both sides |
| `mobile-developer` | TDD patterns for mobile (unit + widget + integration tests) | When adding new screens or business logic — test-first |
| `qa-engineer` | Mutation testing results, property-based test suites, quality reports | When test suite is built — hand off for quality evaluation |

## Proactive Triggers
<!-- STANDARD: 2min — surface these WITHOUT being asked -->

- **New feature without tests** → A spec or user story exists but no test file has been created. Offer to write the first failing acceptance test. 🔴
- **Bug reported without reproduction test** → A bug was found but there's no test proving it exists. Write a reproduction test before touching the fix. 🔴
- **Refactoring without test safety net** → Code is being refactored but coverage is below 70%. Suggest characterization tests first. 🟡
- **Test never failed red** → A test was committed that passed on first run. It may not actually test anything. Offer mutation testing to verify. 🟡
- **Test coverage dropping** → New code is being added without corresponding tests. Flag the coverage delta in PR. 🟡
- **Long-running test suite (>5 min)** → Slow tests discourage TDD. Identify slow tests and suggest optimization or isolation. 🟠
- **Property-based testing opportunity** → A pure function with clear invariants (serialization, math, parsing) is being tested with individual examples. Suggest property-based approach. 🟠
- **Outside-in opportunity** → A feature spans FE and BE. Suggest starting with an acceptance test that drives both sides. 🟠

## Best Practices
<!-- STANDARD: 3min -->

1. **Time-box the cycle.** Red: 1-5 min. Green: 1-5 min. Refactor: 2-10 min. If any phase takes longer, the test is too big — split it.
2. **Test behavior, not implementation.** `expect(component.queryByText('Welcome'))` not `expect(component.state.isLoggedIn).toBe(true)`. Tests survive refactors when they assert what the user sees.
3. **One assertion per test (typically).** When a test has 5 assertions and fails on the 2nd one, you don't know if #3-5 would have failed. Multiple assertions for the same logical behavior are fine (e.g., checking multiple fields of a response).
4. **Tests should be DAMP (Descriptive And Meaningful Phrases), not DRY.** Some duplication in tests is good — each test should tell a complete story without jumping to helper functions.
5. **Don't test the framework.** If you're using Django REST, testing that `ModelSerializer` serializes fields correctly is testing Django, not your code. Test your business logic.
6. **Use the Given-When-Then structure.** Arrange (Given), Act (When), Assert (Then). Separate them with blank lines. Consistency makes tests scannable.
7. **Run tests on every save.** Use `pytest-watch` or `vitest --watch`. The feedback loop must be under 2 seconds for TDD to work.
8. **Mutation testing reveals weak tests.** If you can change the implementation logic and tests still pass, your assertions are too weak. Run mutation testing monthly on P0 code.

## Anti-Patterns
<!-- STANDARD: 2min -->

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| Writing implementation first, then tests | Write the failing test first. If you didn't see it fail, you don't know if it tests anything. |
| Writing 5 tests at once | Write ONE test. Make it pass. Refactor. Then the next test. Batch testing is not TDD. |
| Refactoring without duplication trigger | Refactoring requires a trigger: duplication OR poor expressiveness. "Making it nicer" without a trigger adds complexity without value. |
| Tests that test mocks: `expect(mockFn).toHaveBeenCalled()` | Test behavior: `expect(result).toEqual(expectedOutput)`. Mock verification tests break on any refactor. |
| Skipping the refactor phase because "it's already clean" | Run all tests one more time. Duplication often hides in the test file itself — check for repeated setup or assertions. |
| Tests with no assertions (verification by not-throwing) | Every test must have at least one explicit assertion. "It doesn't crash" is not a behavior spec. |
| Over-mocking — every dependency is mocked | Only mock I/O boundaries (database, network, filesystem). Mocking your own code creates tests that pass despite broken logic. |
| Commenting out failing tests instead of fixing them | A commented-out test is technical debt. Either fix it, update the expectation if the behavior changed, or delete it if the requirement is gone. |

## Error Decoder
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Test passes on first run (never saw red) | Test doesn't actually test anything new. The behavior already exists. | Delete the test or write a stronger assertion. Verify by changing the implementation — the test should fail. | If you didn't see it fail, it's not a TDD test. It's documentation. |
| Refactoring broke 20 tests | Tests are coupled to implementation, not behavior. You changed a method name and the tests mock that exact method. | Rewrite tests to assert behavior (outputs, side effects), not implementation (method calls, internal state). | Fragile tests discourage refactoring. This defeats the purpose of TDD. |
| Test suite takes 10+ minutes | Integration tests dominate the suite. Slow feedback destroys TDD discipline. | Push integration tests to a separate CI stage. Keep the TDD cycle at the unit test level (under 2 seconds). | TDD lives and dies by feedback loop speed. If tests are slow, developers stop running them. |
| 90% coverage but bugs in production | Coverage measures execution, not assertion quality. Error paths are executed but assertions are weak. | Run mutation testing. If mutating the code doesn't break tests, assertions are too weak. Strengthen assertions on error paths. | 100% line coverage with weak assertions is worse than 70% coverage with strong assertions — it creates false confidence. |
| "Can't test this — too coupled" | Code wasn't designed for testability. Direct instantiation, hidden dependencies, static calls. | Apply dependency inversion. Inject dependencies. Use the test as a design tool — if it's hard to test, the API is hard to use. | TDD is a design practice, not a testing practice. Tests that are hard to write are telling you the design is wrong. |

## Production Checklist
<!-- STANDARD: 3min -->

| ID | Item | Status |
|----|------|--------|
| TD1 | Red-green-refactor cycle followed for every new feature and bug fix | ☐ |
| TD2 | Zero tests committed that never saw a red phase | ☐ |
| TD3 | Mutation testing run on P0 code — ≥85% mutation score | ☐ |
| TD4 | Property-based tests for pure functions with clear invariants | ☐ |
| TD5 | Test suite runs in < 5 seconds for unit tests (TDD cycle speed) | ☐ |
| TD6 | Integration tests separated from unit tests (different CI stage) | ☐ |
| TD7 | Bug reproduction tests remain in suite after fixes (regression prevention) | ☐ |
| TD8 | No commented-out tests — either fix, update, or delete | ☐ |
| TD9 | Tests assert behavior, not implementation (survive refactors) | ☐ |
| TD10 | Outside-in TDD used for features spanning frontend and backend | ☐ |
| TD11 | Characterization tests written before legacy code refactoring | ☐ |
| TD12 | Team follows time-boxed cycles (red < 5 min, green < 5 min, refactor < 10 min) | ☐ |

## Scale Depth: Solo → Small → Medium → Enterprise
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

## What Good Looks Like
<!-- STANDARD: 3min -->

Developers write tests first by habit, not by rule. Every bug fix starts with a reproduction test that stays in the suite forever. The test suite runs in under 5 seconds for unit tests — fast enough that nobody hesitates to run it. Coverage is high (85%+) but the real metric is mutation score: 85%+ means assertions are strong. When someone refactors, tests catch behavioral changes instantly. New team members learn the system by reading test descriptions. The codebase is clean because TDD enforces testability — and testable code is decoupled, injected, and modular by nature. Nobody says "this is too hard to test" because that's the first signal of a design problem, not a testing problem.

## Deliberate Practice

TDD is a physical skill disguised as a mental one. The red-green-refactor rhythm must be practiced until it's automatic — like a musician practicing scales until they disappear into the music.

```mermaid
graph LR
    A[Write a failing test] --> B[Write minimum code to pass]
    B --> C[Refactor: improve design without changing behavior]
    C --> D[Review: was the test a good first consumer of the API?]
    D --> A
```

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | TDD a simple kata (FizzBuzz, Roman Numerals, Bowling Game) from scratch | Weekly |
| **Competent** | TDD a real feature at work. Time yourself: red-green-refactor cycles should be < 5 minutes | Daily |
| **Expert** | TDD a feature using only outside-in: acceptance test first, then unit tests, then implementation | Weekly |
| **Master** | Teach TDD to a developer who doesn't use it. Teaching reveals gaps in your own understanding | Monthly |

**The One Highest-Leverage Activity**: Code kata every week. Same kata, different approach. The repetition isn't about the problem — it's about the rhythm. Red. Green. Refactor. Until you don't think about the steps anymore.

## References
<!-- STANDARD: 3min -->

- **qa-engineer** — for test pyramid strategy, coverage goals, and quality metrics
- **code-reviewer** — for test quality assessment during code review
- **idea-to-spec** — for feature specifications that drive acceptance tests
- **api-test-suite-builder** — for automated API test generation that complements manual TDD
- **backend-developer** — for language-specific TDD patterns and test framework setup
- **frontend-developer** — for component-level TDD with React Testing Library or Vue Test Utils
