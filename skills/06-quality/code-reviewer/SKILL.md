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

## The Expert's Mindset

Code review is not gatekeeping — it's **the highest-leverage quality practice in software engineering**. A review that catches a bug saves 10x the cost of fixing it in QA and 100x in production. But the real value is not bug catching: it's **shared understanding, knowledge transfer, and collective ownership**.

### Mental Models

| Model | Description |
|---|---|
| **Review is teaching, not policing** | Every comment is a chance to level up the author. If your review doesn't make the author a better developer, you're optimizing for the wrong outcome. |
| **Speed matters as much as thoroughness** | A perfect review delivered after 3 days is worse than a good review delivered in 4 hours. Review latency is the #1 predictor of team velocity. |
| **The code, not the coder** | Critique the artifact, never the person. "This function has a race condition" not "You wrote a race condition." Distinguish between objective issues and style preferences. |
| **Every bug caught in review is 10x cheaper than in QA** | But reviews that block for 2 days over naming preferences cost more than they save. Calibrate your rigor to the risk. |

### Cognitive Biases That Weaken Reviews

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Anchoring on first solution** | Accepting suboptimal code because it matches the first approach that came to mind | Ask: "What alternative approaches did you consider?" before evaluating the implementation. |
| **Familiarity bias** | Preferring code that looks like code you would write | Separate style (use a linter) from substance. Ask: "Does this work correctly?" not "Does this look like my code?" |
| **Diffusion of responsibility** | Assuming other reviewers will catch the hard issues | If you're the second reviewer, review as if you're the only reviewer. |
| **Authority bias** | Going easy on senior developers, hard on juniors | Apply the same standards regardless of author. Review the code blind to the name. |

### What Masters Know That Others Don't

- **The best reviewers ask questions before making assertions.** "What happens if this query returns 10,000 rows?" teaches more than "This query doesn't have pagination" and arrives at the same fix.
- **Positive feedback is as important as criticism.** Pointing out elegant solutions reinforces good practices. A review with only negatives is demoralizing; a review with praise + constructive feedback is motivating.
- **Review your own code first.** Before assigning reviewers, do a self-review pass. You'll catch 50% of issues and save reviewer time. Add comments explaining non-obvious choices.
- **A "LGTM" review is worse than no review.** It creates a false sense of security. Either do a real review or decline.
- **Flag dead code in every review.** If a PR adds new code that makes old code unreachable — unused functions, dead CSS classes, orphaned API endpoints — flag it. The PR author should remove the dead code in the same PR or file a follow-up ticket. Dead code accumulates one PR at a time; your review is the last line of defense.

### When to Break Your Own Rules

- **Waive the checklist for hotfixes.** In a P0 incident, review for "does this fix the issue without making things worse?" and defer thoroughness to a post-incident follow-up. Ship, then review properly.
- **Approve with nits when the author is more expert in the domain than you.** Flag style and clarity issues (nits) but don't block on correctness you can't fully evaluate.

## Operating at Different Levels

Code review quality scales with the reviewer's ability to spot patterns — from local bugs to systemic risks.

| Level | Code Review Output Characteristics |
|---|---|
| **L1 — Apprentice** | Learns to review. Catches obvious bugs and style issues. Follows a checklist. |
| **L2 — Practitioner** | Catches logic errors, missing edge cases, and test gaps. Reviews for maintainability. Provides actionable feedback. |
| **L3 — Senior** | Spots architectural issues, coupling problems, and security risks. Reviews the design, not just the code. "This approach will cause problems when we scale to X." |
| **L4 — Staff/Principal** | Identifies systemic patterns across reviews. "I'm seeing this same anti-pattern across three teams — let's fix the template." Sets org-wide review standards. |
| **L5 — Industry-level** | Creates review methodologies adopted across the industry. "Here's a new dimension for evaluating code quality." |

**Usage**: Say "as an L3 reviewer, review this PR." Default: **L3** (architectural and security review, pattern recognition).

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

## Footguns
<!-- DEEP: 10+min — war stories from production code review -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| "LGTM" approved a PR that contained a SQL injection in an ORM raw query — the query was `User.where("email = '#{params[:email]}'")` buried in a 400-line diff | A senior developer submitted a PR at 4:55 PM on a Friday. The `User.where` call was on line 287 of a 400-line diff. The reviewer spent 8 minutes on the review — they skimmed the controller logic, verified the test coverage badge was green, and typed "LGTM 🚀". The SQL injection went to production. Six weeks later, a security researcher found it and reported it through the bug bounty program. The query had been exploited 3 times before discovery. | The PR was too large to review effectively. Research shows reviewers find fewer defects after 400 lines of code — fatigue sets in. The raw SQL was invisible because ORMs create a false sense of safety. The test coverage badge was green but the tests used parameterized queries in the test setup, not the actual code path. | **PRs over 400 lines must be split or receive mandatory pair review.** Enforce this in CI (danger.js or similar): `if diff.lines > 400: require_second_reviewer = true`. For ORM-heavy codebases, add a linter rule that flags any raw SQL string interpolation (e.g., `where("... #{...}"`) as a blocking violation. Reviewers: search the diff for "sql", "execute", "where(", and `#{` before looking at anything else. |
| Reviewer left 47 comments, 43 were about variable naming, indentation, and comment grammar — zero about security, correctness, or performance. The PR had a race condition that caused double-charges. | A staff engineer reviewed a payment processing PR with meticulous attention to code style: "rename `amt` to `amount_cents`", "add a blank line before return", "this comment has a typo." The PR had a `check-and-act` race condition in the payment deduplication logic: it checked if a transaction existed, then created one — without a database-level unique constraint or lock. The reviewer's 43 style comments buried the signal. The author fixed all 43 and the race condition shipped. Customers were double-charged 17 times before the bug was found. | The reviewer applied a "find everything" approach instead of a "find what matters" approach. Style issues are easy to spot, giving a false sense of thoroughness. Critical issues (race conditions, missing constraints) require deep reasoning about concurrency — which the reviewer didn't do. | **Review in priority order: Security → Correctness → Performance → Error Handling → Testing → Style.** If you catch yourself writing a style comment, finish the review first and only add style comments if you've already covered all higher-priority dimensions. Use a checklist: "Did I check for race conditions? Did I verify database constraints? Did I trace every error path?" The most damaging bugs are NOT in variable names. |
| Code review turnaround averaged 72 hours for 6 months — the engineering team of 14 had become a bottleneck because only 2 senior engineers were "allowed" to approve | After a high-severity incident traced to a junior engineer's PR, the CTO mandated that all PRs required approval from one of two senior engineers. With 14 developers shipping daily, each senior engineer received 7 review requests per day. Reviews piled up. Developers started working on 2-3 branches simultaneously to stay productive while waiting for reviews. Context switching increased. A critical hotfix sat unreviewed for 18 hours because both seniors were in all-day planning meetings. | The review bottleneck was organizational, not technical. The "only seniors can approve" policy was a reaction to one incident, not a data-driven decision. It created a single point of failure and demoralized mid-level engineers who were capable reviewers. | **Build a reviewer ladder: every engineer reviews code from day 1, but sensitivity gates control who approves what.** Junior engineers review non-critical paths (UI components, documentation, tests) — this is training, not rubber-stamping. Mid-level review business logic. Senior review security/performance. Set SLA: PRs under 200 lines must be reviewed within 4 business hours. Use CODEOWNERS to auto-assign and rotate reviewer load. Track review latency per team and make it a sprint metric. |
| "Approved with comments" became the default — 23 Medium-severity security findings accumulated across 6 months because "approved" didn't mean "fixed" | The team used GitHub's "approve with comments" workflow: the reviewer found 3 Medium-severity issues (missing CSRF token on a logout endpoint, session not invalidated on password change, error message leaking stack traces), left comments, and approved. The author merged without addressing the Medium findings because "Medium isn't blocking." Over 6 months, 23 Medium findings accumulated across 11 PRs. When a security audit flagged 4 of them as "actually High when combined together," the team had to halt feature work for 3 weeks to remediate. | "Approve with comments" severed the connection between review feedback and merge requirements. Medium severity was defined as "fix in next sprint" but there was no tracking mechanism to ensure fixes happened. | **"Request changes" for anything above Low severity.** If it's not safe to ship with the issue, block the merge. Track all review findings in the same ticketing system as bugs — if it's not tracked, it won't be fixed. Run a monthly "open review finding" audit: every unresolved Medium+ from reviews older than 30 days becomes a P2 bug. Combine severity: two Mediums on the same attack surface = one High. |
| Review focused on the code but nobody tested the change — a UI refactor broke the checkout flow on Safari 15 because CI only ran E2E on Chrome | A PR refactored the checkout page to use CSS Grid instead of Flexbox. The reviewer checked the diff, verified tests passed, and approved. The CI pipeline ran Playwright E2E tests on Chromium only. The CSS Grid syntax used `gap` which Safari 15 required a `-webkit-` prefix for. The checkout page rendered with zero spacing between elements — buttons overlapped, the "Place Order" button was unclickable. Revenue dropped 12% over a weekend before a customer screenshot surfaced on Twitter. | The reviewer trusted automated tests to validate behavior, but the test matrix didn't match the browser usage data. 8% of customers used Safari 15. The reviewer didn't pull the branch locally to test — they relied entirely on the CI green checkmark. | **Reviewer must manually verify UI changes.** Pull the branch. Test on at least one non-Chromium browser (Safari, Firefox). Check browser usage data: if any browser has >5% share, it must be in the CI test matrix. Add a PR template checkbox: "I tested this on [Chrome / Safari / Firefox / Mobile]." If you can't build locally, that's an infrastructure problem — fix it before it causes a revenue incident. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| Your review comments are 80% style and formatting — you notice indentation errors faster than race conditions | Your reviews follow a consistent priority order (Security → Correctness → Performance → Error Handling → Testing → Style) and you can name the most dangerous line in any PR under 400 lines | You can predict which PRs will cause a production incident within 6 months — and your prediction accuracy is >50% when tracked over a year |
| You rubber-stamp PRs from senior developers because "they know what they're doing" | You find meaningful issues in PRs from developers at ALL levels — your review quality doesn't depend on the author's seniority | Engineering managers cite your reviews in promotion packets because your feedback demonstrably improved the quality of 10+ engineers |
| You leave "can we do this better?" feedback without suggesting HOW | Every review comment includes: what's wrong, why it matters, and a concrete fix — the author never has to ask "what should I do instead?" | You've designed a review process adopted by 3+ teams that reduced cycle time by 30% while reducing escaped defects by 40% — and you have the DORA metrics to prove it |

**The Litmus Test:** Can you review a 500-line PR in under 15 minutes and identify the 3 most dangerous lines — the ones most likely to cause a security breach, data loss, or outage? If you need more than 20 minutes or you find more style issues than substance, you're practicing reading, not reviewing.

## Deliberate Practice

Reviewing is a skill separate from coding — it requires different mental muscles (pattern matching for bugs, empathy for the author, calibration of severity). The best reviewers practice deliberately.

### The Review Improvement Loop

```
REVIEW → RECEIVE FEEDBACK ON YOUR REVIEW → CALIBRATE → repeat
```

After every review cycle: ask the author which comments were most and least valuable. Did you catch the important bugs? Did you waste time on nits? Adjust your focus.

### Practice Routines by Skill Level

| Level | Practice | Frequency |
|---|---|---|
| **Novice** | Review 10 PRs using a structured checklist. For each PR, write your findings. Then read the senior reviewer's comments on the same PR. Identify 3 things they caught that you missed and why. | Weekly |
| **Competent** | Time-box reviews to 60 minutes. Track your false positive rate (comments marked "won't fix" or dismissed). Target <20% false positives. | Every review |
| **Expert** | Review a PR in a codebase or language outside your primary expertise monthly. Focus on logic, error handling, and edge cases — the universal patterns. | Monthly |
| **Master** | Pair-review with a junior engineer. Let them lead. After each file, discuss: what did you see? What did they see? Calibrate your teaching to their level. | Biweekly |

### The One Highest-Leverage Activity

**Do a self-review before assigning reviewers.** Comment on your own PR explaining non-obvious choices, flagging areas you're unsure about, and noting what you'd change if you had more time. This catches 50% of issues and makes you a better reviewer of others.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Google Engineering Practices — Code Review](https://google.github.io/eng-practices/review/)
- [Conventional Comments](https://conventionalcomments.org/)
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)
- [Best Kept Secrets of Peer Code Review](https://www.amazon.com/Best-Kept-Secrets-Peer-Review/dp/1599160676) — Jason Cohen
- [Code Review Best Practices — Palantir](https://blog.palantir.com/code-review-best-practices-19e02780015f)
