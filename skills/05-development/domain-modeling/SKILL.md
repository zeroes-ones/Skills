---
name: domain-modeling
description: >
  Use when building or refining a project's shared vocabulary (ubiquitous language); when onboarding new team members who need to understand domain concepts; when code uses inconsistent terminology for the same concept; when domain rules are scattered across code without centralized documentation; or when making architectural decisions that need domain context. Handles ubiquitous language building through term challenging, edge-case scenario stress testing, CONTEXT.md maintenance as shared domain glossary, Architecture Decision Record (ADR) creation with three-part trigger test, code-vs-domain-rules cross-referencing, vague term detection and disambiguation, domain boundary mapping, and bounded context identification. Do NOT use for code implementation (route to appropriate developer skill), database schema design (route to database-designer), API contract design (route to api-designer), or system architecture diagrams (route to system-architect).
license: MIT
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - domain-modeling
  - ubiquitous-language
  - ddd
  - bounded-context
  - glossary
  - adr
  - domain-driven-design
  - context-mapping
token_budget: 4000
chain:
  consumes_from:
    - system-architect
    - product-manager
  feeds_into:
    - backend-developer
    - frontend-developer
    - api-designer
    - database-designer
    - qa-engineer
  alternatives: []
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---
# Domain Modeling
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "Everyone knows what 'Customer' means — we don't need a glossary for obvious terms." | Run a "define Customer in 30 seconds" exercise across your team. You'll get 5 different answers — and you've been building against 5 incompatible definitions for months. Vague terms are invisible bugs that manifest as wrong features, duplicate work, and integration failures. A precise definition costs 10 minutes. Ambiguity costs weeks. |
| "CONTEXT.md is just another doc to maintain — the code is self-documenting." | Code documents how, not why. A domain rule enforced in code is invisible to product managers, QA, and new hires. When the rule changes, nobody knows which code to update. CONTEXT.md is the bridge between domain experts who can't read code and developers who can't read minds. Without it, domain knowledge walks out the door with every departing engineer. |
| "We'll document the domain rules after this sprint — we need to ship first." | Every sprint you defer domain documentation, you're accruing knowledge debt at compound interest. The next hire spends 3 months learning what "should be obvious." The refactor hits rules nobody remembers exist. Domain documentation is not documentation — it's the executable specification your team already uses but can't name. |
| "An ADR for every decision is overkill — we'll write them for the big ones." | The three-part trigger test is your filter: hard-to-reverse, surprising-without-context, AND result-of-a-real-tradeoff. If a decision fails any test, skip the ADR. But if someone asks "why did we choose X?" six months from now and nobody remembers, that silence costs you a week of re-litigating the same decision. An ADR is a decision you never have to make twice. |
| "Bounded contexts are DDD academic jargon — our system isn't that complex." | If two teams call the same thing by different names, or different things by the same name, you have implicit bounded contexts whether you document them or not. Undocumented boundaries cause integration bugs that look like "miscommunication" but are actually conflicting domain models fighting in the same codebase. Name the boundaries or the boundaries will name themselves — usually in production incidents. |

Active domain modeling discipline — not just a glossary but a living practice of challenging vague terms, stress-testing with edge-case scenarios, maintaining CONTEXT.md inline, and cross-referencing code against stated domain rules. ADRs are created only when a decision is hard-to-reverse, surprising-without-context, AND the result of a real tradeoff.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable. The agent MUST follow every rule on every invocation.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| R1 | REFUSE to accept vague terms without challenging them | Any term used in a request or codebase that lacks a precise, testable definition in CONTEXT.md | Halt and ask: "What exactly does '{term}' mean here? Give me a definition I could encode as a validation rule." |
| R2 | DETECT when the same term means different things in different contexts | A term appears in multiple bounded contexts or modules with divergent behavior or constraints | Flag the term, document both meanings in CONTEXT.md with context qualifiers, and propose disambiguation (rename or namespace) |
| R3 | REFUSE to create ADRs without passing the three-part trigger test | User or workflow requests an ADR | Run the trigger test: (1) hard-to-reverse? (2) surprising-without-context? (3) result-of-real-tradeoff? If any answer is NO, explain why an ADR is not warranted and suggest a lightweight alternative |
| R4 | DETECT code that contradicts documented domain rules | Code scan reveals logic that violates a constraint, invariant, or state transition documented in CONTEXT.md | Flag the contradiction with file path, line number, the documented rule, and the violating code. Escalate to the owning team via the appropriate channel |
| R5 | REFUSE to let CONTEXT.md go stale | CONTEXT.md's `Last updated` date is older than 30 days OR code references in CONTEXT.md point to files that no longer exist | Trigger a CONTEXT.md refresh: re-scan the codebase, update stale references, archive deprecated terms, and log the refresh in the term drift log |
| R6 | DETECT implicit bounded contexts that lack explicit boundaries | Two teams or modules operate on the same concept with different rules, but no bounded context boundary is documented | Propose a boundary, name both contexts, define their ubiquitous languages separately, and add an Anti-Corruption Layer (ACL) if integration is needed |
| R7 | REFUSE to let domain rules live only in code | A business rule (invariant, constraint, state machine) exists in code but has no corresponding entry in CONTEXT.md | Extract the rule from code, write it in plain language in CONTEXT.md, and link back to the code location. The rule must be understandable by a domain expert who cannot read code |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Domain modeling masters think differently. They don't just document — they interrogate. Every term is a hypothesis until tested against edge cases. Every boundary is a bet about where complexity lives. Every ADR is a signal that the team faced a genuine fork in the road.

#

## Cognitive Biases to Guard Against

| Bias | How It Corrupts Domain Modeling | Countermeasure |
|---|---|---|
| **Curse of Knowledge** | Assuming terms are "obvious" because you've lived with the domain for years | Explain every term to someone outside the team; if they squint, the term needs work |
| **False Consensus** | Believing the team agrees on definitions when they actually don't | Run a "define X in 30 seconds" exercise — compare answers across the team |
| **Anchoring** | Locking onto the first definition of a term and dismissing later refinements | Maintain a term drift log; treat definitions as evolving, not fixed |
| **Overgeneralization** | Using one term to cover multiple distinct concepts to avoid "over-engineering" | If a term needs "usually" or "typically" in its definition, it's too broad |
| **Sunk Cost** | Refusing to rename a core concept because "we've always called it that" | Price the cost of confusion over the next 12 months vs. the cost of the rename |

## Operating at Different Levels

Domain modeling operates at four levels of granularity. Ascend when the current level can't resolve the problem.

| Level | Scope | Artifacts | When to Use |
|---|---|---|---|
| **L1 — Term Definition** | A single domain term and its precise meaning | CONTEXT.md term entry, validation rules | Clarifying "what is a Customer?" during a code review |
| **L2 — Aggregate Design** | A cluster of entities treated as a single unit with an aggregate root | Aggregate diagram, invariant list, transactional boundary | Designing the Order aggregate: Order, LineItem, Payment, Shipment |
| **L3 — Bounded Context** | A boundary within which a specific domain model applies | Context map, ubiquitous language glossary per context | Separating "Billing Account" from "Identity Account" |
| **L4 — Enterprise Context Map** | The full map of bounded contexts and their integration patterns | Context map diagram, integration contracts, ACL specs | Planning how Ordering, Billing, Shipping, and Inventory contexts interact |

**Escalation rule**: If L1 term disputes can't be resolved without discussing aggregates, move to L2. If L2 aggregate conflicts stem from different assumptions about what "the system" means, move to L3.

### Scale Depth
**(STANDARD)**

| Depth | Time | Scope | Artifacts |
|---|---|---|---|
| **QUICK** | 10-20 min | Single term definition, ambiguity resolution | CONTEXT.md term entry with negative space and validation rule |
| **STANDARD** | 1-3 hr | Aggregate design, bounded context identification, context mapping | Aggregate diagram, context map, ubiquitous language glossary per context |
| **DEEP** | 1-3 days | Enterprise context map, event storming workshop, core domain identification | Full context map, domain event catalog, aggregate inventory, strategic DDD decision record |

## When to Use

- Onboarding new team members who need a mental model of the domain
- Refactoring when code uses inconsistent terminology for the same concept
- Sprint planning when acceptance criteria hinge on domain rule interpretation
- Architecture discussions where domain boundaries are unclear
- Code review when you spot a domain rule enforced differently in two places
- Pre-migration planning (monolith decomposition, service extraction)
- Auditing an existing codebase for undocumented business rules
- Preparing for a domain event storming session

#

## Do NOT Use

- **Code implementation** — route to [backend-developer], [frontend-developer], or [fullstack-developer]
- **Database schema design** — route to [database-designer]
- **API contract design** — route to [api-designer]
- **System architecture diagrams** — route to [system-architect]
- **Product roadmap decisions** — route to [product-manager] or [product-strategist]
- **UI/UX wireframes** — route to [ui-ux-designer]

## Route the Request

#

## Auto-Route by Artifacts

When the request context includes these files, auto-activate domain-modeling:

| Artifact Detected | Action |
|---|---|
| `CONTEXT.md` exists in repo root | Load it as the current domain glossary; challenge any stale entries |
| `**/*.glossary.md` or `**/glossary/` directory | Load all glossary files; check for cross-context term conflicts |
| `**/adr/` or `**/doc/adr/` directory | Load the ADR index; check each ADR against the three-part trigger test |
| `**/domain/` directory in code | Scan for aggregates, entities, value objects; cross-reference with CONTEXT.md |
| `**/bounded-contexts.md` or context map diagrams | Validate boundaries against current code organization |

#

## Intent Route

```
User request
  │
  ├─ "What does X mean?" / "Define X" / "Glossary" / "Ubiquitous language"
  │    └─ TRIGGER: L1 Term Definition — challenge, define, record
  │
  ├─ "ADR" / "Architecture Decision" / "Decision record"
  │    └─ TRIGGER: Run three-part test → create ADR or refuse
  │
  ├─ "Boundary" / "Bounded context" / "Context map" / "Where does X belong?"
  │    └─ TRIGGER: L3 Boundary analysis — identify, name, document
  │
  ├─ "Edge case" / "What happens when" / "Scenario"
  │    └─ TRIGGER: Phase 3 edge-case stress testing
  │
  ├─ "Cross-reference" / "Code vs docs" / "Is this rule enforced?"
  │    └─ TRIGGER: Phase 5 code cross-reference audit
  │
  ├─ "Onboarding" / "New team member" / "Explain the domain"
  │    └─ TRIGGER: Load CONTEXT.md → generate domain narrative
  │
  └─ "Term drift" / "Inconsistent" / "Two meanings"
       └─ TRIGGER: R2 term disambiguation protocol
```

## Core Workflow
**(STANDARD)**

<!-- Full 128 lines extracted to references/core-workflow.md -->

#

## Phase 1: Term Harvesting — Scan the Codebase
**Goal**: Build an initial glossary of every domain-significant term in the codebase.
for each source in [code, docs, tickets, conversations]:
    extract nouns that appear in:
...
> 📎 **[references/core-workflow.md](references/core-workflow.md)** — 128 lines of detailed guidance

## Best Practices
**(STANDARD)**

1. **Establish a ubiquitous language that lives in a living document.** Maintain a CONTEXT.md at the repository root with every domain-significant term, its precise definition, what it is NOT (negative space), and a validation rule. The document must be < 30 days fresh — stale glossaries cost $30K-$80K per onboarded developer in trial-and-error learning. Use `find . -name "CONTEXT.md" -mtime +30` in CI to flag staleness.

2. **Identify bounded contexts before designing aggregates or databases.** A bounded context is a boundary within which a specific domain model applies. "Account" means different things in Identity (login, MFA, session) vs Billing (payment method, invoice, balance). Failing to separate these contexts early costs $100K-$500K in remediation when schemas inevitably collide. Draw a context map BEFORE any database schema.

3. **Design aggregates around transactional consistency boundaries, not object graphs.** An aggregate is a cluster of entities treated as a single unit with a root entity as the entry point. The Order aggregate (Order, LineItems, Payment) ensures all-or-nothing transactional consistency. Design aggregates by asking: "What invariants must hold after any single transaction?" — not "what objects seem related?"

4. **Use domain events to decouple bounded contexts.** When something significant happens in the domain (OrderPlaced, PaymentFailed, ShipmentDelivered), publish a domain event. Downstream contexts react independently. This avoids the distributed transaction tangle where Ordering directly calls Billing, which sends to Shipping. Events are the seams between contexts — design them before integration code.

5. **Capture domain rules in code as explicit predicates, not implicit if-checks.** Every domain rule should be a named, testable predicate function: `isEligibleForDiscount(customer, order)` rather than `if (customer.age > 65 && order.total > 100)`. Named rules are discoverable (grep for the function name), testable in isolation, and linkable to CONTEXT.md. Encoded-only rules cost $20K-$60K per regulatory audit failure.

6. **Use context mapping to define integration patterns between bounded contexts.** Each relationship between contexts has a pattern: Partnership (both teams cooperate), Customer-Supplier (upstream provides, downstream adapts), Conformist (downstream conforms to upstream model), Anticorruption Layer (ACL — downstream translates upstream model to protect its own). Document the pattern explicitly in a context map diagram.

7. **Run event storming workshops to discover bounded contexts and domain events.** Event storming surfaces domain events, commands, aggregates, and bounded contexts through collaborative modeling with domain experts and engineers. The artifacts are sticky notes on a wall, not UML diagrams. The goal is shared understanding, not perfect notation. Run an event storming session before designing any new bounded context.

8. **Identify core domain vs supporting vs generic subdomains.** Core domain is what makes your business unique — your competitive advantage. Supporting subdomains are custom but not differentiating (e.g., internal reporting). Generic subdomains are solved problems (e.g., authentication, payment processing). Invest engineering effort proportionally: 70% on core, 20% on supporting, 10% on generic (buy, don't build).

9. **Maintain a term drift log to catch semantic evolution.** Document when a term's meaning changes across sprints: "Sprint 6: 'UserStatus' = account active/inactive. Sprint 12: feature treats it as online/offline presence." Term drift costs $10K-$25K per quarter in misdirected development. The drift log catches the second meaning before it becomes a conflicting implementation.

10. **Write ADRs only for decisions that require the three-part test.** An Architecture Decision Record (ADR) is warranted only when: (a) the decision is architecturally significant (impacts structure, non-functional characteristics, or dependencies), (b) multiple viable alternatives exist, and (c) the decision is not easily reversible. Premature ADR creation costs $5K-$15K in decision debt — cluttering the register makes genuinely important ADRs harder to find.

## Decision Trees
**(QUICK)**

#

## Term Ambiguity Detection

```
Term T encountered in request or codebase
  │
  ├─ Is T defined in CONTEXT.md?
  │    ├─ YES → Does the definition include negative space?
  │    │         ├─ YES → Is the definition testable as a validation rule?
  │    │         │         ├─ YES → TERM IS WELL-DEFINED — proceed
  │    │         │         └─ NO  → Refine definition until testable
  │    │         └─ NO  → "What is T NOT?" → add negative space → retest
  │    └─ NO  → Provisional definition from usage → add to CONTEXT.md → challenge
  │
  └─ Does T appear in multiple bounded contexts?
       ├─ YES → Same meaning in all contexts?
       │         ├─ YES → Document as cross-context term
       │         └─ NO  → R2: Disambiguate — namespace or rename
       └─ NO  → Single-context term — no disambiguation needed
```

#

## ADR Trigger Decision

```
ADR requested for decision D
  │
  ├─ TEST 1: Is D hard-to-reverse?
  │    └─ Would undoing D require: major refactoring? data migration? retraining? contract breaking?
  │         ├─ YES → continue to test 2
  │         └─ NO  → REFUSE: "This decision is easily reversible. Use a team wiki page or comment instead."
  │
  ├─ TEST 2: Would D be surprising without context?
  │    └─ Would a new team member ask "why did they do it this way?"
  │         ├─ YES → continue to test 3
  │         └─ NO  → REFUSE: "This decision follows natural defaults. No ADR needed."
  │
  └─ TEST 3: Was D the result of a real tradeoff?
       └─ Were there genuine alternatives with different pros/cons?
            ├─ YES → CREATE ADR with: Title, Status, Context, Decision, Alternatives, Consequences
            └─ NO  → REFUSE: "Only one reasonable approach existed. No tradeoff to document."
```

#

## Bounded Context Boundary Placement

```
Proposed boundary between concepts A and B
  │
  ├─ Do A and B use different ubiquitous languages?
  │    └─ i.e., do domain experts use different terms for A vs B?
  │         ├─ YES → BOUNDARY IS VALID — proceed to integration design
  │         └─ NO  → Check next signal
  │
  ├─ Are A and B owned by different teams with different roadmaps?
  │    ├─ YES → BOUNDARY IS VALID — organizational boundary implies domain boundary
  │    └─ NO  → Check next signal
  │
  ├─ Do A and B have different lifecycles (create/update/delete schedules)?
  │    ├─ YES → BOUNDARY IS VALID — lifecycle independence is a strong signal
  │    └─ NO  → Check next signal
  │
  ├─ Would a single transaction span A and B?
  │    ├─ YES → BOUNDARY IS SUSPECT — reconsider; shared kernel may be appropriate
  │    └─ NO  → BOUNDARY IS VALID — distinct transactional boundaries
  │
  └─ No signals triggered → Likely NOT a bounded context boundary
       → Consider: shared kernel, or same context with sub-modules
```

#

## Edge-Case Generation Strategy

```
Given domain term T with definition D
  │
  ├─ STATE: What unexpected states can T be in?
  │    ├─ Invalid state transitions (e.g., Order goes from SHIPPED back to PENDING)
  │    ├─ Intermediate states that are "impossible" per the model
  │    └─ Legacy data in states not covered by current code
  │
  ├─ CONCURRENCY: What if two actors operate on T simultaneously?
  │    ├─ Two admins approve the same refund
  │    ├─ User updates profile while billing runs
  │    └─ Inventory allocation and order cancellation race
  │
  ├─ ABSENCE: What if a dependency of T is missing?
  │    ├─ Parent entity deleted while child entity is processing
  │    ├─ Required external service returns 404
  │    └─ Referenced data migrated away mid-operation
  │
  ├─ NEGATION: What is the opposite of the happy path?
  │    ├─ Payment fails AFTER order confirmation
  │    ├─ Subscription cancels DURING renewal
  │    └─ User revokes OAuth grant mid-session
  │
  └─ TIME: What if operations happen out of order?
       ├─ Shipment arrives before payment clears
       ├─ Notification sent before transaction commits
       └─ Scheduled job runs during a deployment
```

#

## Glossary Maintenance Cadence

```
CONTEXT.md maintenance trigger
  │
  ├─ PASSIVE: Last updated > 30 days ago?
  │    └─ YES → R5 STALE — full refresh required
  │
  ├─ EVENT-DRIVEN: Domain event occurred?
  │    ├─ New feature added → scan new code for domain terms → add to glossary
  │    ├─ Bug caused by domain rule misinterpretation → strengthen rule definition
  │    ├─ Team discussion revealed terminology confusion → update and disambiguate
  │    └─ Domain expert joined/left → review all definitions for accuracy
  │
  ├─ CODE-DRIVEN: Code change detected?
  │    ├─ New aggregate/entity/value object → extract domain terms → add to glossary
  │    ├─ Validation logic changed → update corresponding domain rule in CONTEXT.md
  │    ├─ State machine modified → update lifecycle documentation
  │    └─ File referenced in CONTEXT.md was deleted/moved → fix broken reference
  │
  └─ REVIEW-DRIVEN: Scheduled review?
       ├─ Sprint boundary → review all terms touched this sprint
       ├─ Pre-release → verify all domain rules have code enforcement
       └─ Quarterly audit → full glossary review with domain expert
```

## Error Recovery
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Error Decoder
**(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Two teams each use "Account" in their API but return completely different objects — Identity returns email + MFA state, Billing returns payment method + balance | Same term, different bounded contexts, no disambiguation. Both teams think the other team's "Account" is the same thing. Integration code silently maps between incompatible schemas — a time bomb | Run the term disambiguation protocol: identify all contexts where "Account" appears, namespace each meaning (Identity.Account, Billing.Account), update CONTEXT.md with negative space ("Identity.Account ≠ Billing.Account"), add validation to integration points | The most expensive bug in domain modeling is not a bug — it's a classification error. Two things that share a name but not a meaning produce correct-looking code that is semantically wrong. The fix is a CONTEXT.md entry, not a code change |
| CONTEXT.md says "Customer: A paying user with an active subscription" — but the codebase has three different `isCustomer()` functions with different rules | CONTEXT.md not enforced as the single source of truth. The definition was written once, never maintained, and developers implemented their own interpretations. The document is dead — code is the de facto model | Audit all `isCustomer()` implementations. Align them to the canonical definition. If the definition is wrong, update CONTEXT.md first, then code. Add a CI check: `grep -r "isCustomer()"` validates against `CONTEXT.md` definition tag | A CONTEXT.md that code doesn't reference is worse than no CONTEXT.md — it creates the illusion of shared understanding where none exists. The document must be code-linked or it's a fiction |
| Aggregate designed as the full object graph: Order → LineItems → Products → Categories → Suppliers. Every Order query pulls 10MB of data from 6 tables | Aggregate boundary too large — transactional consistency is needed only for Order + LineItems + Payment. Products, Categories, and Suppliers are reference data, not part of the transactional boundary | Redesign aggregate: Order aggregate contains only Order, LineItems, and Payment. Products and Suppliers are separate aggregates referenced by ID. Invariant check: "What must be consistent after a single transaction?" — only Order total, LineItem quantities, Payment status | Aggregates are transactional consistency boundaries, not navigation graphs. The test: can you enforce all invariants within a single database transaction for this cluster? If yes, it's an aggregate. If you need cross-aggregate coordination, use domain events |
| CONTEXT.md 90 days stale — new hire spends 4 weeks building mental model through trial-and-error, reading outdated docs, and interrupting senior devs | No staleness enforcement. CONTEXT.md decays because nobody feels ownership. Each sprint touches terms, but updating the glossary is "not my job." The cost compounds with every hire and every sprint | Add CI staleness check: `find . -name "CONTEXT.md" -mtime +30`. Make glossary updates part of the "definition of done" for any story that introduces or changes a domain term. Assign a glossary steward per bounded context | CONTEXT.md maintenance is not documentation work — it's part of domain modeling. Treat it like tests: part of the feature, not an afterthought |
| Domain rule "VIP customers get free shipping on orders over $50" enforced in 3 places: frontend validation, backend API, and checkout microservice — each with slightly different logic | Domain rules encoded only in code, not linked to a canonical source. When the rule changes (threshold from $50 to $75), one implementation is updated, two are missed. Inconsistent enforcement produces charging bugs | Extract domain rule as a named, testable predicate: `isEligibleForFreeShipping(customer, order)`. Document in CONTEXT.md and link to the enforcing function. Add a code audit: `grep -r "free.shipping" --include="*.ts"` to find all rule instances and verify canonical source | Domain rules are data, not code. They change independently of the code structure and must be discoverable across the codebase. If you can't find all instances of a rule with a single grep, it's not modeled — it's scattered |
| Event storming session runs 4 hours, produces 200 sticky notes on a wall — two weeks later nobody can reconstruct the decisions | No artifact synthesis. Event storming produces raw material, not a finished model. Without synthesis into a context map or ubiquitous language glossary, the insights evaporate within days | Synthesize within 48 hours: produce a context map diagram, prioritized domain event catalog, aggregate inventory, and CONEXT.md update from the workshop. Share with all participants for async review. Schedule 1-hour follow-up to validate synthesis | Event storming is discovery, not design. The output of discovery is insight. The output of design is a context map. You need both — the workshop without synthesis is a team-building exercise, not domain modeling |

## Cross-Skill Coordination

Domain modeling feeds domain clarity into every downstream skill while consuming strategic intent from upstream.

| Direction | Skill | What Domain Modeling Provides / Consumes |
|---|---|---|
| **Consumes** | [system-architect] | System decomposition decisions, integration patterns, architectural constraints |
| **Consumes** | [product-manager] | Business requirements, user stories, stakeholder terminology, feature priorities |
| **Feeds** | [backend-developer] | Precise domain definitions, aggregate boundaries, invariant rules, state machines |
| **Feeds** | [frontend-developer] | Ubiquitous language for UI labels, form validation rules, workflow definitions |
| **Feeds** | [api-designer] | Resource naming, bounded context boundaries for API scoping, domain constraints for request validation |
| **Feeds** | [database-designer] | Aggregate boundaries that guide transaction scoping, entity relationships, invariant enforcement points |
| **Feeds** | [qa-engineer] | Domain rules as test cases, edge-case scenarios for test planning, invariant validation checks |

#

## Coordination Protocol

When domain-modeling detects a conflict between a consumed artifact and domain reality:
1. Document the conflict in CONTEXT.md under a "Cross-Skill Conflicts" section
2. Propose resolution with rationale
3. Route back to the upstream skill for re-alignment
4. Do NOT silently accept upstream artifacts that contradict domain understanding

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | Architecture decisions, technology constraints, system boundaries | Before implementing features that cross system boundaries |
| `api-designer` | API contracts, versioning strategy, rate limiting, error handling | Before building API-consuming code |

## Proactive Triggers

The agent watches for these signals and acts without being asked.

| Trigger | Detection Method | Automatic Response |
|---|---|---|
| New PR contains a domain-significant class/entity name not in CONTEXT.md | Scan PR diff for new class/interface/type names matching domain patterns | Comment on PR: "New domain term '{X}' detected. Add to CONTEXT.md?" with provisional definition |
| Two PRs use different terms for the same concept | Compare terminology across recent PRs in the same domain area | Flag the inconsistency, propose canonical term, request alignment |
| CONTEXT.md Last updated > 30 days | Check file metadata on repo load | Trigger R5 stale glossary refresh workflow |
| Bug report mentions "confusion" or "unclear" about business rules | Monitor issue tracker for keywords: confused, unclear, inconsistent, ambiguous | Proactively load CONTEXT.md, check if the relevant rule is defined clearly, propose clarification |
| New microservice or module created without bounded context documentation | Detect new top-level directories in monorepo or new services in deployment config | Ask: "Does this new service represent a new bounded context? Document the boundary." |
| Code comment contains "TODO: clarify business rule" | grep for `TODO.*(business rule\|domain rule\|clarify\|verify)` | Extract the TODO, create a task to define the rule in CONTEXT.md, link back to the code location |

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

#

## How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "domain-modeling",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

#

## State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

#

## Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like

A well-modeled domain has clear boundaries, a shared language, and traceability from business rule to code.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ENTERPRISE CONTEXT MAP                           │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │   Identity   │    │   Billing    │    │     Fulfillment      │  │
│  │   Context    │    │   Context    │    │       Context        │  │
│  │              │    │              │    │                      │  │
│  │  Account     │───▶│  Account     │    │  Order               │  │
│  │  Profile     │    │  Invoice     │◀───│  Shipment            │  │
│  │  Session     │    │  Payment     │    │  Inventory           │  │
│  │              │    │  Plan        │    │                      │  │
│  │  UB: "Account│    │              │    │  UB: "Order =        │  │
│  │  = identity  │    │  UB: "Account│    │  confirmed purchase  │  │
│  │  for login"  │    │  = paying    │    │  with line items"    │  │
│  └──────────────┘    │  entity"     │    └──────────────────────┘  │
│         │            └──────┬───────┘              │                │
│         │                   │                      │                │
│         ▼                   ▼                      ▼                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    CONTEXT.md (Single Source of Truth)         │  │
│  │  • Core Terms: 47 defined, 0 ambiguous                        │  │
│  │  • Domain Rules: 23 documented, 23 code-verified              │  │
│  │  • Edge Cases: 31 catalogued, 12 resolved                     │  │
│  │  • Bounded Contexts: 3 explicit, 0 implicit                   │  │
│  │  • ADRs: 2 created (both passed 3-part test)                  │  │
│  │  • Last updated: 3 days ago                                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Key: UB = Ubiquitous Language   ───▶ = Integration via ACL/Events  │
└─────────────────────────────────────────────────────────────────────┘
```

**Signs of excellence**:
- A new team member can read CONTEXT.md and understand the domain without asking questions
- Every domain rule in CONTEXT.md has a corresponding test that would fail if the rule changed
- Code reviews catch terminology drift before it reaches main
- ADRs exist for the 2-3 truly contentious decisions; everything else is in lightweight documentation
- The term drift log shows active evolution, not neglect

## Deliberate Practice

Five exercises to sharpen domain modeling skills.

#

## Exercise 1: The 30-Second Definition
Pick any domain term from your current project. Define it in 30 seconds to a colleague who knows nothing about the project. If they can't explain it back correctly, your definition isn't precise enough. Repeat until they can.

#

## Exercise 2: The Edge-Case Gauntlet
Take the 5 most important domain rules in your project. For each, write 3 edge cases that would break a naive implementation. Then check if your current code handles them. Document the gaps.

#

## Exercise 3: The Terminology Audit
Pick a bounded context. List every term used in class names, API endpoints, and database tables. Circle any term that appears in more than one bounded context with a different meaning. Propose disambiguation.

#

## Exercise 4: The ADR Litmus Test
Review the last 10 "architecture decisions" your team made informally (Slack threads, PR comments, meeting notes). For each, run the three-part trigger test. How many would have warranted a formal ADR? Write those ADRs.

#

## Exercise 5: The Glossary Time Machine
Open your CONTEXT.md (or create one). For each term, ask: "Would this definition have been correct 6 months ago? Will it be correct 6 months from now?" Terms that fail the time test need the term drift log.

## Anti-Patterns

### Anti-Pattern: Ambiguous terminology across teams — "Account" means everything and nothing
**What it looks like:** The Identity team's "Account" includes email, password hash, MFA state, and session tokens. The Billing team's "Account" includes payment methods, invoice history, credit balance. Both teams call their API `/accounts` and nobody realizes they're different things until the first integration breaks. Every cross-team feature requires a 2-hour discovery meeting to clarify which "Account" we're talking about.
**Why it fails:** Ambiguous terminology costs $50K-$150K/year in wasted engineering time. Over a year with 8 cross-team features, that's ~200 hours of clarification meetings. At $250/hr fully loaded, that's $50K in direct cost — rework from misunderstandings doubles or triples it. The same word cannot serve two bounded contexts without explicit disambiguation.
**Do this instead:** Run the term disambiguation protocol. Namespace terms by context: Identity.Account, Billing.Account. Update CONTEXT.md with negative space: "Identity.Account ≠ Billing.Account." Add validation at integration points. If a term needs "usually" or "typically" in its definition, it's too broad — split it.

### Anti-Pattern: Stale CONTEXT.md — the dead glossary
**What it looks like:** CONTEXT.md was created enthusiastically 6 months ago during onboarding week. It hasn't been updated since. New terms from the last 5 sprints exist only in code and conversation. A new hire reads CONTEXT.md, builds a mental model from stale information, and spends 4 weeks discovering through trial-and-error which definitions are wrong. Senior devs lose 5-10 hours/week answering "what does X actually mean?"
**Why it fails:** A stale glossary costs $30K-$80K per onboarded developer. With a maintained CONTEXT.md, onboarding compresses from 4 weeks to 1 week. At a $150K salary, each week saved is ~$3K. Across 10 hires, that's $30K saved — and senior devs reclaim their time. A CONTEXT.md that code doesn't reference is worse than no CONTEXT.md — it creates the illusion of shared understanding.
**Do this instead:** Add CI staleness check: `find . -name "CONTEXT.md" -mtime +30`. Make glossary updates part of the definition of done for any story introducing or changing a domain term. Assign a glossary steward per bounded context. The document must be code-linked: every term entry references the enforcement code.

### Anti-Pattern: Premature ADR creation — the over-documented decision register
**What it looks like:** Every design discussion ends with "let's write an ADR." The `adr/` directory grows to 47 entries in 8 months. 44 of them document decisions that either (a) have no viable alternatives so the "decision" was obvious, (b) are trivially reversible with no architectural impact, or (c) were never actually decided — the ADR was written to justify a choice already made in code.
**Why it fails:** Each unnecessary ADR clutters the decision register, making it harder to find the 3 decisions that actually matter. A new architect joining the project reads 40 ADRs to understand the architecture — a full week of ramp-up wasted. Worse: important ADRs get skimmed because "they all look the same." Premature ADR creation costs $5K-$15K in decision debt.
**Do this instead:** Apply the three-part test before writing an ADR: (a) Is the decision architecturally significant? (b) Are there multiple viable alternatives? (c) Is the decision not easily reversible? Only if all three are YES do you write an ADR. Otherwise, document as a code comment, a CONTEXT.md entry, or a team decision log — not an ADR.

### Anti-Pattern: Missing bounded context boundary — mixing Identity and Billing in the same model
**What it looks like:** The system has one "Account" table that stores login credentials AND payment methods AND subscription tier AND usage limits. When Billing needs to add a new payment method type, the migration touches the Identity schema. When Identity adds MFA, Billing's invoice queries break. Every schema change is a cross-team negotiation because the boundary was never drawn.
**Why it fails:** Missing bounded context separation costs $100K-$500K in remediation. When you finally separate them (and you will), the migration involves: data separation across tables, API versioning, client-side updates, and coordinated deployments across teams. This is 3-6 months of sustained effort that could have been avoided with a single context mapping session.
**Do this instead:** Draw context maps before designing schemas. Identity and Billing are separate bounded contexts — they communicate through domain events (UserRegistered, PaymentMethodAdded), not shared tables. Each context owns its data exclusively. The ACL (Anticorruption Layer) translates between context models at integration points.

### Anti-Pattern: Domain rules encoded only in code — the invisible business logic
**What it looks like:** "VIP customers with annual plans get 20% off renewals" is implemented as `if (customer.type === 'vip' && plan.billingCycle === 'annual') { discount = 0.2; }` — buried in a 400-line checkout service. When auditors ask "where is your policy for VIP renewal discounts?" the answer is "in the code." When the rule changes, nobody knows all the places it's implemented. Audit: FAIL.
**Why it fails:** Encoded-only rules cost $20K-$60K per regulatory audit failure. The fine for a single compliance gap in regulated industries (finance, healthcare) starts at $20K. Beyond compliance, undocumented rules guarantee divergence — the same rule enforced differently in frontend validation, backend API, and reporting pipeline produces inconsistent behavior that looks like bugs.
**Do this instead:** Extract every domain rule as a named, testable predicate: `isEligibleForVipRenewalDiscount(customer, plan)`. Document in CONTEXT.md with a link to the enforcing function. Audit with `grep -r "vip.*renewal.*discount"` to find all instances. The rule is discoverable, testable, and auditable.

### Anti-Pattern: Term drift over sprints — "UserStatus" means different things in different sprints
**What it looks like:** Sprint 6 adds a `UserStatus` field meaning "account active/inactive." Sprint 12 builds an online presence feature that treats `UserStatus` as "online/offline/away." Nobody notices the conflict. The online presence feature writes "online" to the `UserStatus` field — the account management dashboard now shows "online" instead of "active." The bug takes 3 days to trace because "UserStatus" is used in 47 files with two incompatible meanings.
**Why it fails:** Term drift costs $10K-$25K per quarter in misdirected development. The online presence feature was built on a false assumption — `UserStatus` means account state, not presence state. The rework costs 2-3 sprints. The bug report doesn't say "term drift" — it says "account management broken" and the root cause is a semantic collision invisible to tools.
**Do this instead:** Maintain a term drift log in CONTEXT.md. When sprint 12 introduces a new meaning, log: "Sprint 12: ONLINE_PRESENCE feature uses 'UserStatus' differently than account management. RESOLVED: Renamed to 'PresenceStatus'." Add CI validation: `grep -r "UserStatus"` against CONTEXT.md definition tag to catch conflicting usages.

### Anti-Pattern: Event storming without synthesis — sticky notes on a wall, no model emerges
**What it looks like:** Team runs a 4-hour event storming session. 200 sticky notes on a wall. Lots of insight. Everyone leaves energized. Two weeks later, someone asks "what did we decide about the Order aggregate?" Nobody remembers. The sticky notes are gone — either photographed in a Slack thread nobody reads or physically discarded during office cleanup.
**Why it fails:** Event storming is discovery, not design. The output of discovery is insight. The output of design is a context map + domain event catalog + aggregate inventory. Without synthesis within 48 hours, insights evaporate — participants forget the nuances, edge cases, and trade-off discussions that made the session valuable. The session cost 32 person-hours (8 people × 4 hours) — $8K+ — and produced zero persistent artifacts.
**Do this instead:** Synthesize within 48 hours into: (a) a context map diagram showing bounded contexts and integration patterns, (b) a prioritized domain event catalog, (c) an aggregate inventory with invariants per aggregate, (d) a CONTEXT.md update reflecting new terminology and definitions. Share with all participants for async review. Schedule a 1-hour follow-up to validate the synthesis.

## Production Checklist
**(STANDARD)**

Before declaring a domain model complete or shipping any feature that depends on it, verify every item. Each unchecked item is a future integration failure or audit gap.

- [ ] **CONTEXT.md fresh:** `find . -name "CONTEXT.md" -mtime +30` returns empty. Every domain-significant term has an entry with precise definition, negative space (what it is NOT), a validation rule, and a reference to enforcing code.
- [ ] **Ubiquitous language consistent:** `grep -r "Account" --include="*.ts"` across all bounded contexts reveals no term used with different meanings in different contexts without explicit disambiguation (e.g., Identity.Account vs Billing.Account).
- [ ] **Bounded contexts mapped:** Context map diagram exists showing all identified bounded contexts and their integration patterns: Partnership, Customer-Supplier, Conformist, or Anticorruption Layer (ACL). No two contexts share database tables.
- [ ] **Aggregate boundaries validated:** Each aggregate was tested with: "Can I enforce ALL invariants within a single database transaction for this cluster?" Aggregates reference other aggregates by ID only — no object-level navigation across aggregate boundaries.
- [ ] **Domain events cataloged:** Every significant domain event (OrderPlaced, PaymentFailed, ShipmentDelivered) is cataloged with its triggering aggregate, payload schema, and consuming contexts. Cross-context communication uses events, not direct API calls.
- [ ] **Core domain identified:** Core, supporting, and generic subdomains categorized. Investment follows the 70/20/10 split: 70% engineering effort on core domain, 20% on supporting, 10% on generic (buy, don't build).
- [ ] **Domain rules extracted to named predicates:** Every business rule exists as a named, testable function discoverable via `grep`. Each rule is linked to its CONTEXT.md entry. No domain rule lives only as an inline conditional.
- [ ] **ADR register audited:** Every ADR passes the three-part test (architecturally significant + multiple alternatives + not easily reversible). ADRs failing any test demoted to code comments or team decision log. Register index maintained with status per ADR.
- [ ] **Term drift log active:** CONTEXT.md includes a term drift section. Any term whose meaning has changed across sprints is logged with date, old definition, new definition, and conflict resolution.
- [ ] **Event storming synthesis exists (if applicable):** If event storming was conducted, synthesis artifacts (context map, domain event catalog, aggregate inventory, CONTEXT.md update) completed within 48 hours and shared with participants.
- [ ] **Onboarding ramp validated:** A developer new to the domain can read CONTEXT.md and identify: key bounded contexts, primary aggregates, core domain concepts, and where to find the code that enforces the most important domain rule. Goal: mental model in < 1 week.
- [ ] **CI glossary enforcement active:** CI pipeline checks: CONTEXT.md freshness (< 30 days), no term used in code that isn't defined in CONTEXT.md (advisory), no term used in two incompatible ways across contexts (blocking).
- [ ] **Cross-team integration contracts documented:** Every integration between bounded contexts has a documented contract specifying: the integration pattern (Partnership/Customer-Supplier/Conformist/ACL), the data format, failure modes, and the owning team.
- [ ] **Audit trail exists:** For regulated domains: every domain rule is traceable from CONTEXT.md definition → enforcing code → test coverage → compliance requirement. A single `grep` from the compliance requirement finds the code that enforces it.
- [ ] **Glossary steward assigned:** One person per bounded context is accountable for CONTEXT.md freshness in that context. Steward rotation documented. No glossary section is > 30 days without a designated owner.

## Verification
<!-- Full 40 lines extracted to references/verification.md -->

Run these checks to confirm the domain model is healthy.
# Check CONTEXT.md freshness (should be < 30 days old)
find . -name "CONTEXT.md" -mtime +30 -exec echo "STALE: {}" \;
# Find domain terms used in class names but missing from CONTEXT.md
...
> 📎 **[references/verification.md](references/verification.md)** — 40 lines of detailed guidance

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## References

1. [Ubiquitous Language](references/ubiquitous-language.md) — Core principles and maintenance of shared vocabulary
2. [Term Challenging](references/term-challenging.md) — Protocol for interrogating domain term precision
3. [Edge-Case Scenarios](references/edge-case-scenarios.md) — Adversarial scenario generation to stress-test definitions
4. [CONTEXT.md Template](references/context-md-template.md) — Living domain glossary structure and sections
5. [ADR Trigger Rules](references/adr-trigger-rules.md) — Three-part test for when to create an Architecture Decision Record
6. [Domain Boundaries](references/domain-boundaries.md) — Identifying where one domain ends and another begins
7. [Code Cross-Reference](references/code-cross-reference.md) — Verifying code implements documented domain rules
8. [Bounded Contexts](references/bounded-contexts.md) — Designing explicit boundaries for domain models
