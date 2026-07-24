---
name: code-reviewer
description: >
  Use when performing structured code reviews on pull requests, reviewing code for
  security vulnerabilities, evaluating performance implications, or assessing error
  handling and test coverage. Handles six-dimension reviews covering security,
  performance, quality, error handling, testing, and documentation with severity-graded
  actionable feedback. Do NOT use for automated linting, CI/CD pipeline configuration,
  security penetration testing, or writing new code.
author: Sandeep Kumar Penchala
license: MIT
allowed-tools: Read Grep Glob
type: quality
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- code-review
- security
- performance
- quality
- static-analysis
- pull-request
token_budget: 3000
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
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Perform rigorous, structured code reviews across six dimensions: security, performance, code quality, error handling, testing, and documentation. Each finding is graded by severity (Critical, High, Medium, Low, Info) with specific, actionable recommendations. This skill goes beyond linting — it identifies logic errors, architectural concerns, security vulnerabilities, performance bottlenecks, and test gaps that automated tools miss.

## Route the Request

<!-- TWO-TIER ROUTING: Auto-Route table (machine) → Intent Route tree (human fallback) -->

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("SKILL.md", "code-reviewer")` — this is your skill | Redirect: "I am Code Reviewer. Route by intent matching below." |
| A2 | `file_contains("diff", "auth/\|crypto/\|payment/\|admin/")` OR `file_contains("commit_message", "auth\|jwt\|oauth\|password")` | **SECURITY** — Full 6-dimension review with security-first pass. Auto-assign security reviewer. Gate: Critical/High block merge. |
| A3 | `file_contains("diff", "package-lock.json\|package.json\|requirements.txt\|Pipfile\|Cargo.toml")` | **DEPENDENCY** — SCA scan first (Dependabot/Snyk). Review license compatibility, CVE status, maintainer reputation. Block if any Critical CVE. |
| A4 | `file_exists("**/migration/**")` OR `file_contains("diff", "CREATE TABLE\|ALTER TABLE\|DROP TABLE")` | **MIGRATION** — Verify rollback plan exists. Check locking/blocking operations. Ensure migration is reversible. Gate: no rollback = block merge. |
| A5 | `diff_line_count > 400` | **SPLIT** — Request PR decomposition. Research shows review quality drops 60% after 400 lines. Require ≤400 lines per PR. |
| A6 | `file_contains("diff", "goroutine\|thread\|async\|concurrent\|mutex\|channel")` | **CONCURRENCY** — Check race conditions, missing synchronization, non-atomic shared state. Require `-race` flag in CI. |
| A7 | `file_contains("diff", ".tsx\|.jsx\|.vue\|<.*>")` | **UI/FRONTEND** — accessibility check (axe-core), bundle-size impact, visual regression diff, semantic HTML validation. |
| A8 | `file_contains("diff", "Dockerfile\|docker-compose\|.tf\|.k8s")` | **INFRA** — Specialized IaC review path. Container scan, secret detection, non-root user verification. |
| A9 | None of the above — general change | **STANDARD** — 6-dimension review (Security → Correctness → Performance → Error Handling → Testing → Documentation). |
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

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "LGTM — it's a small change, what could break?" | A one-line `if user` that looks innocent may bypass a permission check on line 200 you can't see in the diff. "LGTM" reviews are worse than no review — they create false confidence that someone checked. Either do a real review or decline. |
| "I'll review it thoroughly tomorrow — I have meetings all day today." | PR review latency is the #1 predictor of team velocity. 3 days of waiting = context decay for the author, merge conflicts, and rework. A team of 8 shipping 15 PRs/week loses 45-60 developer-days per quarter to review wait time. Cost: $80K-$200K/year. |
| "Style nits are important feedback — consistency matters." | Leave 14 naming comments and the author numbs out, glossing over the one architectural comment about the deprecated library that costs 3x to refactor later. Use a formatter and linter for style. Human review is for correctness, security, and design — not whitespace. |
| "CI is green — ship it." | The author may have changed tests to match broken behavior. CI passing means tests pass — not that the tests are good, coverage is sufficient, or production conditions were simulated. Review modified test assertions as carefully as production code changes. |
| "I trust this developer — they know what they're doing." | Authority bias kills reviews. Senior developers ship bugs too — especially at 11 PM before a deadline, when judgment is compromised. Review the code blind to the name. Every developer, every PR, same standard. Trust is not a review dimension. |

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect code review mistakes before they are given. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE approval without understanding the change | Trigger: Reviewer cannot state in one sentence: (1) what the change does, (2) why this approach over alternatives, and (3) what could go wrong — self-check before issuing approval | STOP. Respond: "Cannot approve. Before approving, complete this statement: 'This change does [X] by [Y]. Alternative [Z] was rejected because [reason]. The risk is [W].' If any field is blank, request clarification from the author — do not LGTM what you don't understand." |
| R2 | DETECT hardcoded credentials, secrets, or tokens in diff | Trigger: Diff adds string literals matching `password`, `secret`, `api_key`, `token`, `private_key`, `-----BEGIN`, or high-entropy base64 strings (≥32 chars of base64) in any file | STOP. Respond: "SECURITY — BLOCKER: Hardcoded credential at [file:line]. Secrets in source are exposed to everyone with repo access and persist forever in git history. Use environment variables, a secrets manager (Vault/AWS Secrets Manager), or CI/CD secret injection. Rotate the credential immediately if it was ever pushed." |
| R3 | DETECT missing error handling for changed or fallible function | Trigger: Function in the diff now performs I/O, network, or parsing (can fail) but neither wraps the call in `try/catch`/`Result` nor propagates the error to callers — grep diff for new `fetch`, `open`, `parse`, `connect` without adjacent error handling | STOP. Respond: "MISSING ERROR HANDLING at [file:line]. `[function]` can now fail but neither handles the error locally nor propagates it. Every fallible operation must either: handle the error and degrade gracefully, OR propagate it in the return type (`Result<T, E>`, `throws`, `Either`). Silent failures cause corrupted state." |
| R4 | DETECT N+1 query or unbounded data retrieval | Trigger: Database query, API call, or data fetch inside a loop (`for`/`map`/`forEach`/`while`) without batching — count: each iteration triggers an independent query with no `IN (...)` clause, no `Promise.all`, no bulk endpoint | STOP. Respond: "PERFORMANCE — HIGH: N+1 pattern at [file:line]. Each iteration fires a separate query — [N] items = [N] round-trips. Impact: 100 items × 50ms latency = 5 seconds. Fix: collect all IDs first, then fetch in one query (`WHERE id IN (...)`), one bulk API call, or use `include`/`eagerLoad`. Always batch." |
| R5 | DETECT changed logic path with no test coverage | Trigger: Diff adds a new conditional branch (`if`/`else`/`switch` case), modifies algorithm logic, or changes a return type — but the diff contains no new or modified test file asserting the new behavior | STOP. Respond: "TESTING — HIGH: Changed logic at [file:line] has zero test coverage in this diff. Minimum requirement: one happy-path test AND one edge-case test per new branch. Blocking unless tagged as a hotfix — file a follow-up ticket with the ticket ID in a comment. Approving untested logic creates regression debt." |
| R6 | DETECT injection vector from user input to dangerous sink | Trigger: Data originating from `req.body`, `req.params`, `req.query`, `$_(GET|POST)`, `request.form`, `event.body` flows into SQL string interpolation, `exec()`/`spawn()`, `.innerHTML`, or `open()` path construction without parameterization or sanitization | STOP. Respond: "SECURITY — BLOCKER: Injection risk at [file:line]. User input `[source]` flows to `[sink]` without sanitization. SQL: use parameterized queries (`$1`, `?`). HTML: use `textContent` or DOMPurify. Shell: use `execFile` with argument array, never string concatenation. File paths: canonicalize and validate against an allowlist." |
| R7 | REFUSE review of formatting, style, or linting issues | Trigger: Reviewer comment describes whitespace, indentation, line length, import ordering, brace style, or naming convention — any issue detectable by a linter, formatter, or type checker | STOP. Respond: "STYLE — DECLINE: This is a linter concern, not a human review finding. If the configured linter didn't catch it, propose a linter rule addition in a separate PR. Human code review focuses on: correctness, security, performance, design, test coverage, and error handling — not formatting."

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

## What Good Looks Like

> Every code review catches structural bugs, security flaws, and performance regressions before they reach production.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

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

## Gotchas

- **Rubber-stamping large PRs (>400 lines).** Reviewer attention quality degrades sharply after ~400 lines of diff. A 1,200-line PR gets a 45-second glance, an "LGTM 👍" comment, and a merge. The buried SQL injection in line 847, the missing authorization check in line 312, and the N+1 query on line 523 all ship to production. Large PRs correlate directly with production incidents — studies show defects increase 40%+ beyond 400 lines. **Total cost: $50,000-$500,000 per year in production bugs that thorough review of smaller changes would have caught.** Fix: Break PRs into logical chunks under 400 lines; enforce a PR size limit in CI (reject >500 lines); require multi-session reviews for unavoidably large changes; review in 45-minute focused sessions with breaks between.
- **Security issues missed in review.** A code reviewer focuses on logic, naming, and patterns — but skips over hardcoded API keys, missing input sanitization, and broken authorization checks because "security review is someone else's job." The average data breach costs $4.45M (IBM 2023), and a significant percentage originate from vulnerabilities that a trained reviewer would have caught. One missed SQL injection or exposed secret is all it takes. **Total cost: $100,000-$1,000,000+ average breach cost from security issues that slip through review.** Fix: Add a security checklist to every code review (OWASP Top 10 quick-scan); use automated SAST tools (semgrep, CodeQL) as a pre-review filter; train reviewers to recognize common vulnerability patterns; flag security findings at BLOCKER severity in review.
- **Review bottleneck becoming the critical path.** All code must be reviewed by a single senior engineer who is also the tech lead, architect, and on-call responder. PRs queue up for 3-4 days while this person is in meetings, putting out fires, or designing the next sprint. A team of 8 engineers shipping ~15 PRs per week loses 45-60 developer-days per quarter to review wait time, during which context decays and merge conflicts accumulate. **Total cost: $80,000-$200,000 per year in blocked developer throughput, rework from stale branches, and delayed feature delivery.** Fix: Distribute review responsibility across the team with a review assignment rotation; establish a review SLA (all PRs reviewed within 4 business hours); use CODEOWNERS to auto-assign reviewers based on code area; pair less experienced reviewers with domain experts for training.
- **Nitpicking variable names while missing architectural flaws.** A reviewer leaves 18 comments on a 300-line PR — 14 are about variable naming (`getUserData` vs `fetchUser`), import ordering, and whitespace preferences, and 4 are substantive. The author spends 2 hours addressing the nits and glosses over the one architectural comment about the service being tightly coupled to a deprecated library because they're numbed by the volume of trivial feedback. Three sprints later, the deprecated library is EOL and the refactor costs 3x what it would have if caught during review. **Total cost: $30,000-$150,000 per year in missed architectural issues, developer frustration, and delayed refactors.** Fix: Use automated formatters (Prettier, Black, gofmt) and linters to eliminate style debates before human review; separate comments into "blocking" (security, correctness, architecture) and "suggestion" (style, naming, clarity); reviewers should explicitly tag each comment's severity.
- **Reviewing without running the code.** A reviewer reads the diff, verifies logic mentally, leaves an "LGTM" — but never checks out the branch, builds it, runs the tests, or clicks through the UI. The PR merges and CI goes red because the author forgot to push a new file that was only in their local directory. The feature works on the author's machine because of an environment variable they set 6 months ago that doesn't exist in CI or production. **Total cost: $25,000-$100,000 per year in broken builds, reverted merges, and production incidents from unverified code that passed review.** Fix: Require reviewers to pull the branch and run tests locally for non-trivial changes; add a CI check that runs the test suite against the merge commit; for UI changes, require a screenshot or screen recording in the PR description as evidence the reviewer interacted with the feature.
- **Reviewing only the diff** misses context. A one-line change that looks innocent (`if user`) may bypass a permission check on line 200 that you can't see in the diff. Always expand context +50 lines before and after critical changes.
- **"LGTM" with no comments** is worse than no review — it signals the code was checked when it wasn't. If you genuinely found nothing, mention at least one specific thing you verified (e.g., "verified auth checks on all new endpoints").
- **Security issues in test files** are still security issues. Hardcoded API keys in `test/setup.ts` get committed and leaked. Review test files with the same severity as production code.
- **CI passing doesn't mean the code works**. The author may have changed tests to match broken behavior. Review modified test assertions as carefully as production code changes.
- **Large PRs (>400 lines)** get rubber-stamped. The reviewer's attention degrades significantly after ~400 lines. Break large PRs or review in multiple sittings with fresh context.

## Verification

- [ ] All identified issues have severity grading (blocker/critical/major/minor/nit) and specific file:line references
- [ ] Every issue has a concrete fix suggestion, not just "this is wrong"
- [ ] Security issues are flagged separately with OWASP category reference
- [ ] Review covers all 6 dimensions: security, performance, quality, error handling, testing, documentation
- [ ] No style-only comments (leave formatting to automated formatters)

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Negative Constraints**: See [negative-constraints.md](references/negative-constraints.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

