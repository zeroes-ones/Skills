---
name: code-reviewer
description: 'Six-dimension code review covering security, performance, quality, error
  handling, testing, and documentation with severity grading and actionable, specific
  feedback. Trigger: code review, review code, CR, pull request review, review this.'
author: Sandeep Kumar Penchala
type: quality
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- code-reviewer
token_budget: 3000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - api-test-suite-builder
  - backend-developer
  - frontend-developer
  - qa-engineer
  - security-reviewer
  - staff-engineer
  - tdd-guide
  feeds_into:
  - backend-developer
  - frontend-developer
  - qa-engineer
  - tdd-guide
---
# Code Reviewer

Perform rigorous, structured code reviews across six dimensions: security, performance, code quality, error handling, testing, and documentation. Each finding is graded by severity (Critical, High, Medium, Low, Info) with specific, actionable recommendations. This skill goes beyond linting — it identifies logic errors, architectural concerns, security vulnerabilities, performance bottlenecks, and test gaps that automated tools miss.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Review a pull request (PR) → Start at "Core Workflow > Phase 1"
│   ├── Quick sanity check (<200 lines, low risk) → Jump to "Core Workflow > Phase 2", then approve or flag
│   ├── Standard review (feature/bug fix) → Full 6-dimension review: "Core Workflow > Phase 2 → Phase 3 → Phase 5"
│   └── Critical change (auth, payments, data) → "Core Workflow > Phase 3" — all 6 dimensions, multi-reviewer
├── Security-focused review (auth, crypto, PII) → Go to "Sub-Skills > security-review" then "Six-Dimension Review Framework > Security"
├── Performance review (queries, memory, latency) → Go to "Sub-Skills > performance-review" then "Six-Dimension Review Framework > Performance"
├── Architecture review (new module, refactor, >200 lines) → Start at "Core Workflow > Phase 2", then "Decision Trees > Review Depth Decision"
├── Accessibility review → Go to "Six-Dimension Review Framework > Code Quality" and check for ARIA, keyboard, semantic HTML
├── Need deep security audit → Invoke security-reviewer skill instead
├── Need backend implementation review → Invoke backend-developer skill instead
├── Need frontend implementation review → Invoke frontend-developer skill instead
├── Need QA test strategy → Invoke qa-engineer skill instead
└── Not sure where to start? → "Core Workflow > Phase 1" (Context Gathering) — understand intent first
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never approve without understanding the change.** If you can't explain why a change is correct, ask for clarification — do not assume.
- **Flag severity clearly (blocker vs. nit).** Every finding gets a grade (Critical/High/Medium/Low/Info) with specific line references and fix suggestions.
- **Every finding needs a specific line reference.** No vague "this function is problematic" — point to the exact file, line, and why it matters.
- **Don't review style — use automated tools for that.** Linting, formatting, and type checking are CI's job. Your job is logic, design, security, and correctness.
- **Always explain the "why."** A finding without rationale is a complaint, not a review. Show the impact: "This N+1 query adds 500ms per item — on a page with 50 items, that's 25 seconds."
- **Admit what you don't know.** If a change touches a domain outside your expertise (e.g., cryptography implementation details), flag it for a specialist and don't pretend confidence.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Reviewing pull requests before merge
- Performing pre-commit self-review on your own code
- Auditing a codebase for quality, security, or performance issues
- Establishing code review standards and checklists for a team
- Mentoring developers through constructive code review feedback

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Review Depth Decision

```
Change type and risk?
├── Trivial (typo, comment, formatting) → Light review: correctness only. Approve in <1 hour.
├── Standard (feature, bug fix, <200 lines) → Full 6-dimension review. <4 hour SLA.
├── Complex (new module, refactor, >200 lines) → Full review + architectural check. <24 hour SLA.
└── Critical (auth, payments, data migrations, security) → Multi-reviewer: Peer + Security Specialist.
      All dimensions mandatory. Critical/High findings block merge.

PR > 400 lines? → Request author to split into smaller PRs. If not possible, schedule live review session.
```


**What good looks like:** Review covers all 6 dimensions (correctness, security, performance, maintainability, style, testing). Every finding has a severity, rationale, and suggested fix. Author can address all changes in under 2 hours. No critical or high findings remain.

### When Automated Tools Suffice

```
Change type?
├── Dependency update (patch)? → CI passes + changelog reviewed. Auto-merge if safe.
├── Configuration change? → Lint + validate config schema. Human review only for production values.
├── Documentation only? → Spell check + link check. Human review for accuracy and tone.
└── Generated code? → Review the generator/template, not the generated output.
```

## Six-Dimension Review Framework

### 1. Security
- **Injection risks**: SQL injection (raw queries, string interpolation), NoSQL injection, command injection (`exec`, `subprocess` without sanitization), LDAP/XML injection.
- **Authentication & authorization**: Missing auth checks on endpoints, JWT validation gaps (`algorithm: none`, missing signature verification), broken access control (IDOR — user can access other users' resources), privilege escalation paths.
- **Data exposure**: Secrets in code (API keys, tokens, passwords), sensitive data in logs/error messages, PII not encrypted at rest, excessive data exposure in API responses.
- **Dependency security**: Outdated packages with known CVEs, unpinned versions, supply chain risks (typosquatting, compromised packages).
- **Input validation**: Missing server-side validation, unbounded inputs, regex DoS patterns, unsafe deserialization.
- **CSRF/XSS**: Missing CSRF tokens on state-changing operations, unsanitized user-generated content rendered in HTML, `dangerouslySetInnerHTML` without sanitization.

### 2. Performance
- **Database queries**: N+1 queries, missing indexes for filtered/sorted columns, `SELECT *` on large tables, unbounded queries (no LIMIT), cartesian products from missing JOIN conditions, inefficient subqueries.
- **Memory**: Memory leaks (unclosed connections, uncleaned intervals/listeners, growing caches), large object allocations in hot paths, unbounded memory growth.
- **Network**: Chatty client-server communication (batch requests), unoptimized assets (uncompressed images, missing lazy loading), no CDN for static assets, missing HTTP caching headers.
- **Algorithmic complexity**: O(n²) or worse in critical paths, unnecessary nested loops, repeated computations without memoization, blocking the event loop (Node.js), synchronous I/O in async contexts.
- **Bundle size**: Unused dependencies, missing tree shaking, large imported libraries for single functions, unminified production code.

### 3. Code Quality
- **Readability**: Meaningful variable/function names, consistent naming conventions, shallow nesting (max 3 levels), short functions (ideally < 50 lines), no commented-out code. When refactoring, enforce the Boy Scout Rule — clean up dead paths, unused imports, and legacy artifacts in every file touched. See `references/dead-code-cleanup-checklist.md` for the full reviewer checklist.
- **Design**: Single Responsibility Principle, DRY violations (copy-pasted code), god objects/classes, feature envy, inappropriate intimacy between modules.
- **Error-prone patterns**: Mutable global state, implicit type coercion, truthy/falsy checks that miss edge cases (`''`, `0`, `false`), floating point for money, `==` instead of `===`, missing `await`.
- **TypeScript usage**: `any` types (should be `unknown` or properly typed), missing strict null checks, overuse of type assertions (`as`, `!`), type holes that bypass safety.
- **Complexity**: High cyclomatic complexity (if-else chains → use lookup tables or strategy pattern), boolean flag parameters (split into separate functions).

### 4. Error Handling
- **Error propagation**: Errors swallowed silently (empty catch blocks), generic catch without context, error messages leaked to users (stack traces in responses).
- **Graceful degradation**: Missing fallbacks for optional services, entire app crashes on non-critical error, no retry logic for transient failures.
- **Edge cases**: Null/undefined not handled, empty arrays/strings not considered, boundary values (0, -1, MAX_INT, empty string), race conditions, timeout handling.
- **Validation**: Business rule violations not caught, data integrity checks missing, inconsistent state after partial failure (no transactions).

### 5. Testing
- **Coverage gaps**: Critical paths untested, edge cases not covered, error paths not tested, integration points not verified.
- **Test quality**: Tests testing implementation details (brittle) rather than behavior, missing assertions (tests that never fail), flaky tests (race conditions, time dependencies, random data), slow tests without clear value.
- **Test data**: Hard-coded magic values without meaning, test data that doesn't reflect production patterns, tests that pass only with specific data.
- **Isolation**: Tests depending on execution order, shared mutable state between tests, tests making real network calls.

### 6. Documentation
- **Code comments**: Comments explaining "what" (should be obvious) not "why", missing JSDoc/docstrings on public APIs, outdated comments that contradict code, TODO comments without ticket references.
- **API documentation**: Missing or outdated API docs, undocumented error responses, auth requirements not specified, request/response examples missing.
- **Architecture**: Complex systems without README/architecture docs, onboarding friction for new team members, tribal knowledge not codified.

## Severity Grading
| Grade | Criteria | Response Required |
|-------|----------|-------------------|
| **Critical** | Security vulnerability, data loss/corruption risk, production outage risk | Must fix before merge |
| **High** | Significant bug, performance degradation, architectural concern | Must fix before merge |
| **Medium** | Code smell, missing test, unclear logic | Should fix; can be deferred with ticket |
| **Low** | Style nit, minor improvement, naming suggestion | Optional; author discretion |
| **Info** | Educational note, alternative approach suggestion | No action required |

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~5 min): Context Gathering
1. Read PR description, linked issue/ticket, and any design docs.
2. Understand what the change is trying to accomplish and why.
3. Verify the PR description explains the problem, not just the solution.
**Output:** Clear understanding of intent and expected behavior.

### Phase 2 (~10 min): High-Level Review
1. Check architectural alignment — does this change fit existing patterns?
2. Identify simpler approaches. Is the solution proportionate to the problem?
3. Verify the change doesn't duplicate existing functionality.
4. Flag any module boundary violations or unexpected coupling.
**Output:** Go/no-go on architectural fit; list of concerns to probe deeper.

### Phase 3 (~15 min): Six-Dimension Deep Review
1. **Security**: Injection, auth, data exposure, dependency CVEs, input validation.
2. **Performance**: N+1 queries, memory leaks, bundle size, algorithmic complexity.
3. **Code Quality**: Readability, design principles, TypeScript strictness, error-prone patterns.
4. **Error Handling**: Propagation, graceful degradation, edge cases, transaction safety.
5. **Testing**: Coverage gaps, test quality, isolation, flaky tests.
6. **Documentation**: Comment intent, API docs, architecture decisions.
**Output:** Findings grouped by severity (Critical/High/Medium/Low/Info), each with line references and concrete fix suggestions.

### Phase 4 (~5 min): Test Verification
1. Run the test suite. Do tests pass on this branch?
2. Review new tests for meaningfulness — do they test behavior or implementation?
3. Check coverage on changed paths. Is coverage gap acceptable given risk?
4. Manually verify UI/UX or complex interaction changes if applicable.
**Output:** Confirmation tests pass; flag any coverage gaps or test quality issues.

### Phase 5 (~5 min): Write Review
1. Group feedback by file/section for readability.
2. Apply severity grading table consistently.
3. Balance constructive criticism with positive feedback.
4. Use `nit:` and `suggestion:` prefixes for non-critical items.
5. Request specific changes on Critical/High items.
**Output:** Published review — actionable, specific, respectful, and timely.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
> **War story:** A team reviewed a PR adding a new API endpoint. All 6 dimensions passed — correct logic, clean code, good tests, proper error handling. The reviewer skipped the dependency diff because "only one new import." That import was `pyjwt` (a third-party JWT library with a known CVE) instead of `PyJWT` (the maintained fork). The dependency was in production for 3 months before the security audit caught it. **Fix:** Never skip dependency review — verify every new import against the organization's approved list and SCA scan results.

- **Be specific and actionable**: "This query could cause an N+1 problem" → "Use `.include('author')` on the Prisma query at line 47 to eager-load authors in one query."
- **Explain the "why"**: Don't just say "use `useMemo`" — explain that the derived value recomputes on every render, causing downstream re-renders.
- **Suggest, don't demand**: Use "Consider...", "What do you think about...", "Could we..." for non-critical items.
- **Separate nitpicks from substance**: Use `nit:` or `suggestion:` prefixes so authors can filter.
- **Review in a timely manner**: < 4 hours for small PRs (< 200 lines), < 24 hours for large PRs. Code review is the #1 bottleneck in development velocity.
- **Automate what can be automated**: Linting, formatting, type checking, security scanning — leave human review for logic, design, and architecture.

## Anti-Patterns

- **Style-only reviews**: Focusing exclusively on formatting, naming, and code style while ignoring logic correctness, security, and performance. Code reviews that never catch bugs are performative. Automate style (Prettier, gofmt, black) so human review targets substance.
- **Rubber-stamp approvals**: Approving PRs without reading the diff — "LGTM" with zero comments. Every rubber stamp is a production incident waiting to happen. Track review comment-to-approval ratio; zero-comment approvals should be rare.
- **Gatekeeper mentality**: Blocking merges for subjective preferences ("I would have used a for-loop instead of map"). Code review is a conversation, not a veto. Use `nit:` or `suggestion:` prefixes for non-blocking style opinions.
- **Scope creep in review**: Requesting changes that go beyond the PR's intent — refactoring unrelated files, introducing new patterns, or expanding the feature. Open a separate ticket or tech-debt item instead.
- **Inconsistent severity application**: Flagging a missing semicolon with the same urgency as an auth bypass. Use a consistent severity grading framework (Critical/High/Medium/Low) so authors can triage.
- **Reviewing without context**: Reading the diff in isolation without understanding the PR description, linked issue, or architectural constraints. Always start with the PR description and linked ticket to understand intent before reviewing implementation.
- **Delayed reviews**: Allowing PRs to sit unreviewed for days while the author context-switches. Review latency is the #1 bottleneck in development velocity. Set SLA: <4 hours for small PRs, <24 hours for large PRs.
- **Skipping dependency review**: Approving PRs without checking new or updated dependencies for known CVEs, license conflicts, or supply chain risks. Every `package-lock.json` or `requirements.txt` change must be verified against SCA scan results.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `backend-developer` | PR with API changes, data access logic, auth implementation, query changes | When PR is submitted; code review is the last line of defense |
| `frontend-developer` | PR with UI components, client-side state, accessibility, bundle impact | When PR is submitted; ensures UI quality, accessibility, and performance |
| `security-reviewer` | Security findings for joint severity assessment, patterns to add to code review checklist | When PR touches auth/payment/data paths; delegate deep security review |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `backend-developer` | Actionable feedback with line references, architectural concerns, test coverage gaps, design pattern suggestions | PR stuck in review — #1 bottleneck in development velocity |
| `frontend-developer` | Same review feedback with accessibility, performance, and bundle size focus | Frontend PRs merge with regressions — UX degradation |
| `qa-engineer` | Flagged test coverage gaps, edge cases found during review, security-sensitive code areas | QA can't target testing effectively — gaps in test coverage |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| Critical security vulnerability found | Security Engineer, PR author | Immediate fix; may block deploy |
| Architectural deviation detected | System Architect | Decide: approve exception or redesign |
| Repeated pattern of same issue across PRs | Engineering Manager | Systemic problem — needs tooling, lint rule, or training |
| PR too large for effective review (>400 lines) | PR author, Engineering Manager | Request PR decomposition |
| CI consistently failing/flaky on PRs | DevOps Engineer, CI/CD Builder | Pipeline health investigation |

### Escalation Path

```
Security finding (Critical/High)? → Security Engineer → Compliance Officer
Architecture dispute? → System Architect → CTO Advisor
Repeated quality issues from same author? → Engineering Manager
CI infrastructure issues? → DevOps Engineer
```

## Proactive Triggers

| Trigger | Action | Rationale |
|---|---|---|
| PR changes affect 2+ services or API boundaries | Flag integration test gaps; verify contract tests exist for cross-service communication | Multi-service changes have multiplicative failure modes — the integration surface is where bugs hide |
| New dependency added (any manifest change) | Check license compatibility, known CVEs in SCA scan, maintainer reputation, and supply chain posture | A single compromised dependency grants attacker access to the entire build pipeline |
| Auth/authorization code modified | Auto-assign security reviewer; flag for mandatory security review gate | Auth changes are the highest-leverage attack surface — even a one-line change can create an auth bypass |
| Database migration present (schema change or data migration) | Verify rollback plan exists; check for locking/blocking operations; ensure migration is reversible | A bad migration with no rollback plan can cause hours of downtime with no undo path |
| PR exceeds 400 lines | Request decomposition into smaller, reviewable units | Review quality is inversely proportional to PR size — a 1000-line PR gets a fraction of the scrutiny per line |
| CI review gate configured | Verify required status checks include: lint, type-check, unit tests, SAST scan, and dependency audit | CI gates enforce consistency; missing gates allow unreviewed code to merge silently |
| Concurrency-sensitive code (goroutines, threads, async shared state) | Check for race conditions, missing locks/synchronization, and non-atomic operations on shared mutable state | Concurrency bugs are deterministic in hindsight but invisible in code review without deliberate attention |

**Service Interaction Designs:**

| Interaction | Design Detail |
|---|---|
| Code Review ↔ CI/CD | Automated review gates enforce required status checks (lint, test, SAST, dependency audit) before merge. CI must block PRs that fail any gate. Review comment resolution verified via GitHub Checks API — unresolved threads block merge. |
| Code Review ↔ Security | SAST results (Semgrep/CodeQL) posted as inline PR annotations. Dependency scanning (Dependabot/Snyk) runs on every manifest change. Security reviewer auto-assigned when diff touches `auth/`, `crypto/`, `payment/`, or `admin/` paths. |
| Code Review ↔ QA | Review findings with severity grading feed into QA's test plan. Flagged coverage gaps become targeted test cases. Flaky test patterns identified during review shared with QA for quarantine. |
| Code Review ↔ Frontend | Accessibility and bundle-size checks run as part of review gates. Semantic HTML and ARIA patterns validated via automated checks before human review. Visual regression diffs included in PR for UI changes. |
| Code Review ↔ DevOps | IaC changes (Dockerfile, Terraform, K8s manifests) get specialized review path. Container image scanning results posted to PR. Secret detection (truffleHog/gitleaks) blocks PRs containing credentials. |

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Code review = self-review checklist before merging. Review dimensions: correctness + security (just check for obvious issues). No PR process. No automated checks.
- **What to skip**: Multi-reviewer PR process. Automated CI checks (lint, type-check, tests). Security specialist review. Review SLAs. Severity grading.
- **Coordination**: Self-review. Ship fast, fix forward.

### Small Team (2-10 people, 100-10K users)
- **What changes**: PR required for all merges. One reviewer (peer). Automated checks: lint, type-check, tests. Review dimensions: all 6 but lighter on architecture/performance. Severity grading used. Review SLA: <24 hours. Security-sensitive changes get extra scrutiny.
- **What to skip**: Multiple reviewers per PR. Formal review board. Review metrics tracking. Security specialist for every PR.
- **Coordination**: PR assigned via GitHub. Async review within 24 hours. Quick sync for complex changes.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Two reviewers for critical paths (auth, payments, data). Full 6-dimension review enforced. Automated checks: lint + type-check + tests + security scan + coverage. Severity-based merge gates (Critical/High block merge). Review metrics tracked (turnaround time, review depth). Security reviewer for sensitive changes.
- **What to skip**: Formal review board (peer review is enough). Mandatory architecture review for every PR. Review metrics as performance evaluation.
- **Coordination**: CODEOWNERS for domain expertise. Weekly code review quality sync. Monthly review metrics review.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multiple reviewer tiers (peer → domain expert → security → architecture for critical changes). Automated review bots (linter, type-checker, security scanner, dependency checker). Formal review checklist per change type. Review board for cross-cutting changes. Compliance review gates (SOC 2, HIPAA, PCI DSS). Review metrics as quality KPIs. Reviewer training program.
- **What's full production**: Automated pre-review (AI-assisted review). Change-risk-based review depth. Reviewer workload balancing. Review quality auditing. Cross-team review coordination.
- **Coordination**: Weekly review quality audit. Monthly review board for cross-cutting changes. Quarterly reviewer calibration.

### Transition Triggers
- **Solo → Small**: Second developer joins. Need shared understanding of code changes.
- **Small → Medium**: 5+ developers. Critical production incidents traced to merged code. >10K users.
- **Medium → Enterprise**: Compliance requirements. Multiple teams with shared code ownership. >50 developers.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | backend-developer | Feature implementation with tests |
| **This** | code-reviewer | Six-dimension review with severity-graded findings |
| **After** | qa-engineer | Test coverage for flagged risk areas |

Common chains:
- **Chain**: backend-developer → code-reviewer → qa-engineer — Code is reviewed for quality/security, then QA targets findings with additional tests
- **Chain**: frontend-developer → code-reviewer → release-manager — UI changes reviewed for accessibility and performance, then queued for release

## What Good Looks Like

> Every code review catches structural bugs, security flaws, and performance regressions before they reach production. Reviews are delivered in under four hours with actionable, priority-ranked feedback. Each finding links to a specific line, explains the risk, and suggests a concrete fix. The team treats reviews as a learning opportunity, and review feedback measurably reduces production incidents sprint over sprint. Reviewers consistently spot issues across all six dimensions, and developers trust the review process enough to never bypass it.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `security-review` | Auth, crypto, PII, payment code | Dimension 1 — injection, auth, data exposure, dependency CVEs |
| `performance-review` | Query-heavy, memory-intensive, latency-sensitive code | Dimension 2 — N+1, memory leaks, complexity, bundle size |
| `code-quality-review` | All PRs — readability, design, error-prone patterns | Dimension 3 — SRP, DRY, TypeScript strictness, cyclomatic complexity |
| `error-handling-review` | Error paths, external integrations, async code | Dimension 4 — propagation, graceful degradation, edge cases, transactions |
| `testing-review` | Test coverage gaps, test quality, flaky tests | Dimension 5 — behavior vs implementation, assertions, isolation |
| `documentation-review` | API docs, READMEs, architecture docs, comments | Dimension 6 — JSDoc, API specs, architecture decisions, TODOs |
| `language-specific` (Python/TS/Go/Rust) | Per-language anti-patterns | `references/language-specific-review-guides.md` |
| `dead-code-cleanup` | Dead code, commented-out code, stale flags, unused deps | `references/dead-code-cleanup-checklist.md` |


## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| PR passed review — race condition in production took down checkout service | Reviewer focused on code style, naming, and test coverage but missed the in-memory cache mutation race between concurrent requests. | Always review for concurrency in shared mutable state. Check for race conditions: is there a mutex/lock around shared cache writes? Are HTTP handlers goroutine-safe? Add `-race` flag to test suite. | Style and correctness are different dimensions. A perfectly formatted PR with a subtle concurrency bug is still a production incident waiting to happen. |
| Security vulnerability in login flow — missed by 3 reviewers | All reviewers focused on business logic correctness (does the token flow work?) and did not review security (can the token flow be bypassed?). | Every PR needs a security-focused pass in addition to the logic pass. At minimum: check auth checks on every endpoint, verify input validation, and review dependency changes for known CVEs. | A PR review that doesn't include a security pass is incomplete. Rotate a "security hat" among reviewers for each PR. |
| PR blocked for 3 days over indentation debate | Team had no automated formatter. Reviewers spent more energy on formatting consistency than on logic errors, test coverage gaps, or edge cases. | Enforce formatting automatically (Prettier, gofmt, black). Config must be in CI and fail the build. Never allow formatting as a human review topic — it costs engineering velocity and distracts from real bugs. | Code review is for logic, design, and correctness — not formatting. Automate everything that can be automated so humans focus on what matters. |
| PR merged — deployment failed because environment variable name was misspelled | Reviewer checked the code in isolation but didn't verify the run-time configuration. The env var `DATABASE_URL` was typed as `DATABSE_URL` in the application code but present correctly in the deployment config. | Include configuration verification in review: check env var names in code match deployment configs. Add schema validation at startup so typos cause immediate crashes, not silent fallbacks. | Code correctness is not deploy correctness. Config drift between code and infrastructure is one of the most common — and hardest to catch — review misses. |
| Developer merged 3 PRs in one review because individual PRs were "too small to bother" | No PR size guidance. Developers avoided the review bottleneck by batching changes into single large PRs. | Set a maximum PR size (400 lines is a common threshold). Large PRs must be split or get a synchronous review session. Track review turnaround time — if it exceeds 24 hours, increase reviewer capacity. | PR size is inversely proportional to review quality. A 1000-line PR gets a fraction of the scrutiny per line that a 100-line PR gets. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Every PR reviewed against all six dimensions before merge
- [ ] **[S2]**  Critical and High severity items resolved before merge
- [ ] **[S3]**  Medium severity items tracked as follow-up tickets
- [ ] **[S4]**  Review comments are specific, actionable, and explain the "why"
- [ ] **[S5]**  Automated checks pass (lint, type-check, tests, security scan) before human review
- [ ] **[S6]**  Reviewer pulled branch and manually tested UI/UX changes
- [ ] **[S7]**  Test coverage for changed code verified (added/modified tests present and meaningful)
- [ ] **[S8]**  Positive feedback given alongside constructive criticism
- [ ] **[S9]**  Review turnaround time tracked and < 24 hours
- [ ] **[S10]**  Security-sensitive changes (auth, payments, PII) reviewed by security specialist

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Google Engineering Practices — Code Review](https://google.github.io/eng-practices/review/)
- [Conventional Comments](https://conventionalcomments.org/)
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)
- [Best Kept Secrets of Peer Code Review](https://www.amazon.com/Best-Kept-Secrets-Peer-Review/dp/1599160676) — Jason Cohen
- [Code Review Best Practices — Palantir](https://blog.palantir.com/code-review-best-practices-19e02780015f)
