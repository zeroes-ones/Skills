---
name: code-simplification
description: >
  Use when reducing code complexity while preserving exact behavior, refactoring
  legacy code, eliminating dead code, flattening deep nesting, simplifying
  conditionals, removing premature abstractions, or applying Chesterton's Fence
  before removing any code. Handles complexity scoring (cyclomatic, cognitive),
  language-specific anti-pattern removal (TypeScript, Python, React), dead code
  elimination, nested logic flattening, and the Rule of 500 (files exceeding 500
  lines require explicit justification). Do NOT use for greenfield feature
  development (route to backend-developer or frontend-developer), performance
  optimization without behavior preservation (route to performance-engineer),
  security hardening (route to security-reviewer), or API redesign (route to
  api-designer).
author: Sandeep Kumar Penchala
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
license: MIT
allowed-tools: Read Grep Glob Bash
type: quality
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - code-simplification
  - refactoring
  - complexity
  - dead-code
  - cyclomatic-complexity
  - chestertons-fence
  - rule-of-500
token_budget: 4000
chain:
  consumes_from:
    - backend-developer
    - frontend-developer
    - code-reviewer
    - fullstack-developer
    - staff-engineer
  feeds_into:
    - code-reviewer
    - qa-engineer
    - backend-developer
    - frontend-developer
---
# Code Simplification
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Reduce code complexity while preserving exact behavior — the hardest discipline in software engineering. This skill applies five principles: **Preserve Behavior Exactly** (every simplification must pass existing tests unchanged), **Follow Project Conventions** (don't impose new patterns mid-refactor), **Prefer Clarity Over Cleverness** (the best code reads like prose, not a puzzle), **Maintain Balance** (not everything needs golfing — some verbosity is intentional), and **Scope to What Changed** (simplify only the diff surface; don't cascade into unrelated modules).

Chesterton's Fence is your first principle: **understand why code exists before removing it.** Every line that looks useless may be a load-bearing wall for an edge case discovered through production fire. The Rule of 500 states that any file exceeding 500 lines needs explicit justification or a decomposition plan — no exceptions.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect simplification mistakes before they ship. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to remove code without understanding its purpose (Chesterton's Fence) | Trigger: `git log -S "<removed_function_or_constant>" --all` returns commits by multiple authors OR references bug IDs, edge cases, or production incidents — AND you cannot articulate in one paragraph why it was there and why it's safe to remove | STOP. Respond: "CHESTERTON'S FENCE at [file:line]. This code was introduced in commit [SHA] fixing [issue/bug]. I cannot confirm the original problem no longer applies. Before removing: (1) reproduce the original bug with a test, (2) verify current code fixes it, (3) refactor, (4) confirm test still passes. Do not tear down a fence you don't understand." |
| R2 | DETECT behavior change disguised as simplification | Trigger: `diff` between original and simplified code changes any output, return type, exception class, or error message string — grep for `return`/`throw`/`raise`/`console.log` differences | STOP. Respond: "BEHAVIOR CHANGE at [file:line]. The simplification altered [specific output/exception/return]. The five principles REQUIRE Preserve Behavior Exactly. Either: (1) revert the behavioral change and find a behavior-preserving simplification, or (2) if the behavior change is intentional, split into a separate PR — this is a refactor, not a simplification." |
| R3 | DETECT simplification that increases cognitive load despite fewer lines | Trigger: Simplified code uses ternary chains (3+ nested), regex without comments, curried composition without named intermediates, or bitwise operations replacing readable conditionals — grep for `\?.*\?.*:` (double ternary), `/[^/]{30,}[^/]/` (long regex), `.compose\(\)`, `>>|<<|\||\^|&` | STOP. Respond: "CLARITY REGRESSION at [file:line]. Fewer lines ≠ simpler code. The simplification reduced line count but increased time-to-understand. Measure: show original to a colleague — if they ask 'what does this do?', it's not simpler. Name intermediates, add one comment line per regex, and prefer explicit conditionals when logic branches." |
| R4 | DETECT premature abstraction during simplification | Trigger: Simplified code extracts a function/class used exactly once AND the extraction adds 3+ lines of boilerplate (function signature, export, import, JSDoc) — grep for `export function\|export const.*=` that appears only in the calling file | STOP. Respond: "PREMATURE ABSTRACTION at [file:line]. Function `[name]` is called exactly once and the extraction cost exceeds inlining. Rule: inline until you need it in 3+ places. File sizes under 200 lines rarely benefit from single-use extraction. Inline and add a TODO comment for when a second caller appears." |
| R5 | DETECT removed code that test coverage depends on | Trigger: `npm test -- --coverage` or `pytest --cov` after simplification shows coverage decrease > 1% — simplified code removed lines that tests were hitting | STOP. Respond: "COVERAGE REGRESSION: Simplification dropped coverage from [X]% to [Y]%. Removed code was exercising tests that may now be dead. Either: (1) the removed code was genuinely dead — delete the corresponding tests too, or (2) the behavior is still needed — the simplification went too far. Run `git diff --unified=0` to identify coverage gaps." |
| R6 | DETECT simplification that breaks type safety or contracts | Trigger: Simplified code removes type guards, loosens parameter types (e.g., `string` → `any`), removes `assert`/`invariant` calls, or deletes `if (x == null) return` guards without replacement — grep diff for removed `:`, `as`, `assert`, null checks, or widened types | STOP. Respond: "TYPE SAFETY LOSS at [file:line]. Removed guard `[guard]` was preventing a class of runtime errors. Simplification must not weaken the type contract. Either: (1) prove the guard is unreachable (add `// unreachable: [reason]`), or (2) restore it. Loose types cost more debugging hours than they save in keystrokes." |
| R7 | REFUSE to simplify code under active incident or hotfix | Trigger: `git log --oneline -5` in the target file shows commits tagged `hotfix`, `incident`, `#incident-`, `P0`, or `SEV` within 7 days | STOP. Respond: "ACTIVE INCIDENT WINDOW: This file was hotfixed [N] days ago for [issue]. Simplifying code under recent incident response risks: (1) reintroducing the bug, (2) confusing root-cause analysis if the issue recurs, (3) adding noise to blame logs. Wait [X] days post-incident or until the postmortem is closed. Simplify only after stabilization." |

## The Expert's Mindset

Simplification is not about making code shorter — it is about making code **understandable faster.** A master simplifier knows that the person reading code tomorrow (who might be you at 3 AM during an incident) is the customer. Every keystroke saved today that costs 30 seconds of confusion tomorrow is a net loss.

### Mental Models

| Model | Description |
|---|---|
| **Chess, not checkers** | Simplification is adversarial: you versus complexity that accumulates daily. Every merge adds entropy. Your job is to be the entropy-reducer — the second law of thermodynamics applies to codebases. |
| **The reader is always in a hurry** | They are debugging a production issue, not leisurely studying your code. They will skim, not read. Make the happy path obvious within 5 seconds of scanning. |
| **Complexity is a loan with compound interest** | Every unnecessary abstraction, every clever one-liner, every deeply nested conditional compounds over time. A 10-line function that's "a bit tricky" becomes a 100-line monster after 6 months of incremental changes. Fix it at 10 lines, not 100. |
| **The best diff is a deletion diff** | Green (-) lines outweigh red (+) lines 3:1 in truly great simplifications. If your simplification adds more code than it removes, question whether you're really simplifying. |

### Cognitive Biases That Block Simplification

| Bias | How It Shows Up | Defense |
|---|---|---|
| **IKEA effect** | Overvaluing code you wrote yourself — "I spent 3 days on this, it must be good" | Ask: "Would I merge this if a junior engineer submitted it?" |
| **Sunk cost fallacy** | "We already built the abstraction layer, might as well use it" even when it no longer fits | If the abstraction costs more to maintain than to inline, kill it. Past investment is irrelevant. |
| **Cleverness addiction** | Using advanced language features (proxies, decorators, metaprogramming) when a plain function works | Rule: use the simplest language feature that solves the problem. If you need to explain it, it's too clever. |
| **Scope insensitivity** | "While I'm here, I'll also refactor this module..." — feature creep in simplification | Strict rule: simplify ONLY what the PR touches. Open a follow-up ticket for the rest. |

### What Masters Know That Others Don't

- **You can't simplify what you can't measure.** Always start by computing cyclomatic complexity and cognitive complexity scores. If you don't have a baseline, you're guessing.
- **The best simplifications are invisible.** After a great simplification, the code looks obvious — "of course it should be this way." That's the goal. If people say "wow, clever!", you failed.
- **Test coverage is your safety net.** Never simplify code with <80% test coverage on the target module. Write tests first, then simplify. The tests prove you didn't break anything.
- **Deletion is a skill.** Most engineers are afraid to delete code. Practice: find a 500-line file and see if you can reduce it to 300 lines without losing behavior. You will discover that 40% of most codebases is dead or redundant.

## Operating at Different Levels

- **Quick scan (30s):** Run complexity lint on changed files. Flag any function with cyclomatic complexity > 10, any file > 500 lines, and any file where comment-to-code ratio exceeds 30% (overtly commented code is often compensating for bad structure). Identify the top 3 complexity hotspots.
- **Standard engagement (10min):** Apply simplification to one function or module. Compute baseline complexity, identify the primary anti-pattern (deep nesting, god function, shotgun surgery), apply the language-specific refactoring pattern, verify tests pass unchanged, confirm complexity score decreased.
- **Deep dive (full session):** Simplify an entire file or module group. Start with dead code elimination (grep for unused exports, unreachable branches), then structural simplifications (extract-to-named, flatten nesting, unify duplicate logic), then rename for clarity. Run full test suite between each step. Commit after each logical simplification unit.
- **Legacy code rescue (multi-session):** For files with 0% test coverage and unknown behavior: (1) characterize with characterization tests, (2) identify seams, (3) simplify one seam at a time, (4) never mix simplification with feature work.

## When to Use

Use code-simplification when working with existing code that is harder to understand than it needs to be — the focus is on reducing cognitive load, not adding features.

- Reducing cyclomatic complexity: functions with > 10 independent paths need restructuring
- Eliminating dead code: unreachable branches, unused exports, deprecated codepaths
- Flattening deep nesting: arrow code with 4+ indentation levels, callback pyramids
- Simplifying conditionals: long if-else chains that can become lookup tables or polymorphism
- Removing premature abstractions: single-use functions, over-engineered factories, unnecessary indirection
- Applying the Rule of 500: files exceeding 500 lines that need decomposition plans
- Consolidating duplicate logic: copy-pasted blocks that differ by only 1-2 parameters
- Renaming for clarity: variables/functions whose names mislead or obscure intent
- Reducing comment density: code where comments exceed 30% of lines (code should be self-documenting)
- Inverting conditionals: early returns replacing deep if-else nesting (guard clause pattern)

Do NOT use code-simplification for greenfield development (route to backend-developer or frontend-developer). Do NOT use for performance optimization that changes behavior (route to performance-engineer). Do NOT use for security hardening (route to security-reviewer). Do NOT use for API contract changes (route to api-designer). Do NOT use for adding features while refactoring — separate PRs.

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("SKILL.md", "code-simplification")` — this is your skill | Redirect: "I am Code Simplification. Route by intent matching below." |
| A2 | `file_lines > 500` AND `file_extension in [.ts, .tsx, .js, .jsx, .py, .go, .java]` | **RULE OF 500** — File violates Rule of 500. Go to **Decision Trees: Rule of 500 Violation**. Compute decomposition plan before any simplification. |
| A3 | `grep "TODO\|FIXME\|HACK\|XXX" file` count > 10 | **TECH DEBT HOTSPOT** — File has >10 debt markers. Start with **Core Workflow: Phase 1 (Dead Code)** then structural simplification. |
| A4 | `git log --oneline -20 file` shows 5+ authors in last 20 commits | **HIGH CHURN** — File has many hands. Run Chesterton's Fence check on every function before modifying. |
| A5 | `cloc file` shows comment ratio > 0.30 | **OVER-COMMENTED** — Code is compensating for unclear structure. Focus on **Core Workflow: Phase 3 (Rename & Restructure)** before touching comments. |
| A6 | `grep "catch\|except\|try" file` count > 15 | **ERROR HANDLING COMPLEXITY** — Consolidate error handling. Jump to **Decision Trees: Error Handling Simplification**. |
| A7 | `grep "if.*if.*if\|for.*for\|switch.*if.*for" file` count > 0 | **DEEP NESTING** — Arrow code detected. Go to **Core Workflow: Phase 2 (Structural Simplification)**. |
| A8 | No specific triggers — general simplification request | **STANDARD** — Full workflow: Phase 1 → Phase 2 → Phase 3. |

### Intent Route (Ask the User)

```
What are you trying to simplify?
├── A specific function that's too complex → Start at "Core Workflow > Phase 2", then "Decision Trees > Cyclomatic Complexity"
├── A file that's too long (>500 lines) → Jump to "Decision Trees > Rule of 500 Violation"
├── Code with too many nested if/for/while → Go to "Decision Trees > Deep Nesting"
├── Dead or unreachable code I want to remove → Start at "Core Workflow > Phase 1"
│   ├── I'm sure it's dead → Verify with coverage + grep, then delete
│   └── I'm not sure → Full Chesterton's Fence investigation before touching anything
├── Duplicate logic across multiple files → Jump to "Decision Trees > Duplicate Consolidation"
├── I want to rename things for clarity → Go to "Core Workflow > Phase 3"
├── Legacy code with no tests → Jump to "Decision Trees > Legacy Code Simplification"
├── I need a complexity score / baseline → "Core Workflow > Phase 0" — measure first
└── Not sure where to start → "Core Workflow > Phase 0" — run complexity analysis on the whole file
```

## Core Workflow

### Phase 0: Measure Baseline

Before touching a single line, compute your baseline. You cannot claim you simplified anything without numbers.

```
npx complexity-report src/target.ts --format json > baseline.json
# or
radon cc src/target.py -j > baseline.json
# or
gocyclo src/target.go > baseline.txt
```

Record: cyclomatic complexity per function, cognitive complexity score, lines of code, comment ratio, and test coverage.

### Phase 1: Dead Code Elimination

Dead code is the only 100% safe simplification — if code is unreachable, removing it cannot change behavior.

```
Step 1: Find unused exports
  npx ts-prune --skip index.ts    # TypeScript
  vulture src/ --min-confidence 90  # Python

Step 2: Find unreachable branches
  grep -n "return.*\n.*return\|throw.*\n.*return" src/target.ts
  # A return/throw followed by code in the same block = dead code

Step 3: Check git blame before deleting
  git log -S "<code_snippet>" --all --oneline
  # If the snippet was introduced with a bug fix, it's Chesterton's Fence — investigate

Step 4: Verify with coverage
  npm test -- --coverage --collectCoverageFrom=src/target.ts
  # Lines with 0% coverage AND unreachable = safe to delete
  # Lines with 0% coverage BUT reachable = NEED tests before simplification
```

ASCII diagram:

```
┌──────────────────────┐
│  Phase 1: Dead Code  │
├──────────────────────┤
│ 1. Find unused       │
│ 2. Find unreachable  │
│ 3. Git blame check   │
│ 4. Coverage verify   │
│ 5. Delete            │
│ 6. Run tests         │──── PASS ──► Phase 2
│         │                        │
│         └── FAIL ──► REVERT      │
└──────────────────────────────────┘
```

### Phase 2: Structural Simplification

Now attack the living code. Priority order:

**2a. Flatten nesting (guard clauses)**

Before:
```typescript
function getDiscount(user: User): number {
  if (user) {
    if (user.isActive) {
      if (user.orders > 10) {
        return 0.15;
      } else {
        return 0.05;
      }
    } else {
      return 0;
    }
  } else {
    return 0;
  }
}
```

After:
```typescript
function getDiscount(user: User): number {
  if (!user || !user.isActive) return 0;
  return user.orders > 10 ? 0.15 : 0.05;
}
```

**2b. Simplify conditionals (lookup table)**

Before:
```typescript
function getStatusColor(status: string): string {
  if (status === 'active') return 'green';
  else if (status === 'pending') return 'yellow';
  else if (status === 'error') return 'red';
  else if (status === 'disabled') return 'gray';
  else if (status === 'warning') return 'orange';
  return 'black';
}
```

After:
```typescript
const STATUS_COLORS: Record<string, string> = {
  active: 'green', pending: 'yellow', error: 'red',
  disabled: 'gray', warning: 'orange',
};
const getStatusColor = (status: string) => STATUS_COLORS[status] ?? 'black';
```

**2c. Extract to named variable (no new functions!)**

Before:
```python
total = sum(order.price * order.quantity * (1 - 0.1 if customer.is_member else 1) * (1 + TAX_RATES[order.state]) for order in orders if order.status != 'cancelled')
```

After:
```python
def order_net_price(order, customer):
    discount = 0.1 if customer.is_member else 0.0
    tax = TAX_RATES[order.state]
    return order.price * order.quantity * (1 - discount) * (1 + tax)

active_orders = [o for o in orders if o.status != 'cancelled']
total = sum(order_net_price(o, customer) for o in active_orders)
```

### Phase 3: Rename & Clarify

Naming is the highest-leverage simplification. A good name eliminates the need for a comment.

- **Rename misleading variables:** `data` → `customerOrders`, `tmp` → `intermediateTotal`, `val` → `shippingCost`
- **Replace magic numbers:** `if (days > 30)` → `if (days > ACCOUNT_INACTIVITY_THRESHOLD)`
- **Remove redundant comments:** If the code says `// iterate over users` above `for user in users:`, delete the comment
- **Add one critical comment:** One comment explaining WHY (not what) if the logic is genuinely non-obvious

## Decision Trees

### Decision Tree 1: Cyclomatic Complexity Reduction

```
Phase 1: Measure
├── CC ≤ 5 → No action needed. Move on.
├── CC 6-10 → Flag for future refactor. Document in code review.
├── CC 11-20 → MUST simplify in this session.
└── CC > 20 → CRITICAL. Function is likely untestable. Full decomposition required.

Phase 2: Identify Primary Driver
├── Deep nesting (3+ levels) → Apply guard clause pattern (early return)
├── Long if-else chain (5+ branches) → Convert to lookup table or strategy pattern
├── Boolean flag explosion (3+ boolean params) → Replace with options object or enum
├── Mixed concerns (validation + transformation + I/O) → Split into pure functions
└── Loop + conditional combo → Extract loop body to named function
```

### Decision Tree 2: Rule of 500 Violation

```
Phase 1: Determine Decomposition Candidates
├── File has natural seams (clear sections, comment dividers) → Extract along seams
├── File has heterogeneous concerns (data, UI, logic mixed) → Separate by concern
├── File is a "god class" (one class does everything) → Split by responsibility
└── File is a long data file (constants, config, enums) → Split by domain

Phase 2: Execute Decomposition
├── Can extract module without circular dependency → Immediate extraction
├── Extraction would create circular dependency → Extract interfaces first (DIP)
├── File is test file → Split by describe/test grouping (max 200 lines per describe)
└── File is configuration → Split by environment or feature flag group
```

### Decision Tree 3: Chesterton's Fence Investigation

```
Phase 1: Discover Purpose
├── git log -S "<code>" --all → Found bug-fix commit → INVESTIGATE before removing
├── git log -S "<code>" --all → Found feature commit by departed engineer → Ask team
├── git log -S "<code>" --all → Found only formatting/linting commits → Likely dead
└── git log -S "<code>" --all → No results → Code was never changed = high risk

Phase 2: Decision
├── Code handles an edge case → Write test for edge case, then simplify around it
│   └── Cannot reproduce edge case → Add characterization test documenting current behavior
├── Code was for a removed feature → Safe to delete after confirming all callers removed
├── Code is defensive (null check, bounds check) → Verify with type system first
└── Cannot determine purpose → LEAVE IT. File a ticket for investigation.
```

### Decision Tree 4: Duplicate Consolidation

```
Phase 1: Find Duplicates
├── Exact copy-paste (differ only in whitespace/comments) → Extract shared function immediately
├── Near-duplicate (differ by 1-2 parameter values) → Parameterize and extract
├── Structural duplicate (same shape, different types) → Consider generic/template
└── Semantic duplicate (different code, same intent) → Pick the better one, delete the other

Phase 2: Extraction Safety
├── Duplicate is in same file → Extract to module-level function
├── Duplicate spans 2 files → Extract to shared utility module
├── Duplicate spans 3+ files → Extract to library/package (consider publishing)
├── Duplicate is in test files → Extract to test helper/fixture factory
└── One duplicate has diverged (extra logic) → Unify the common part, keep divergence as parameter or strategy
```

### Decision Tree 5: Legacy Code Simplification (0% Test Coverage)

```
Phase 1: Characterize
├── File has any tests at all → Run them. Record pass/fail.
├── File has 0 tests → Write characterization tests for every public function.
│   ├── Happy path for each function
│   ├── Null/undefined input handling
│   └── Error path (what exceptions does it throw?)
└── Cannot write characterization test → File is too coupled. Extract seams first.

Phase 2: Simplify One Seam at a Time
├── Identify the smallest independent unit (single function, < 20 lines)
├── Write characterization test for that unit
├── Simplify the unit
├── Run all characterization tests
└── Commit. Repeat.
```

### Decision Tree 6: Error Handling Simplification

```
Phase 1: Audit Error Patterns
├── Same error wrapped 3+ times → Remove intermediate wrapping, keep outermost
├── Swallowed errors (catch {} with empty body) → Add logging + rethrow or handle
├── Generic catch-all (catch (e: any) in TS) → Narrow the error type
└── Mixed error strategies (some throw, some return null, some return Result) → Unify

Phase 2: Unify Strategy
├── Library/utility code → Use Result<T, E> pattern (never throw from utilities)
├── Application code → Use structured error classes with error codes
├── API handlers → Use error middleware (Express, FastAPI exception handlers)
└── Async code → Use Promise.catch or try/catch consistently (pick one pattern per file)
```

## Cross-Skill Coordination

| Scenario | Skill to Invoke |
|---|---|
| Simplification changes public API surface | `api-designer` — verify backward compatibility |
| Simplification touches database queries | `database-designer` — verify query plans unchanged |
| Simplification is pre-requisite for feature work | `backend-developer` or `frontend-developer` — coordinate refactor + feature |
| Want to verify simplification didn't introduce bugs | `code-reviewer` — 6-dimension review of the diff |
| Need tests before simplifying legacy code | `qa-engineer` or `tdd-guide` — characterization tests |
| Simplification touches performance-critical path | `performance-engineer` — benchmark before and after |
| Simplification is part of broader tech debt initiative | `staff-engineer` or `engineering-manager` — align with roadmap |

## Proactive Triggers

These conditions automatically activate code-simplification scrutiny even when not explicitly invoked:

- **Trigger: `git diff --stat` shows +200 lines or file exceeds 500 lines.** Auto-check: Rule of 500 violation. If yes, require decomposition plan.
- **Trigger: cyclomatic complexity of any changed function > 10.** Flag in PR review: "This function's complexity exceeds threshold. Consider simplification before merge."
- **Trigger: new PR adds a file with >30% comment ratio.** Auto-comment: "High comment-to-code ratio detected. Consider renaming for clarity instead of commenting."
- **Trigger: git blame shows a line was last touched > 2 years ago AND you're modifying it.** Auto-activate Chesterton's Fence check.
- **Trigger: `npm ls` or `pip freeze` shows a dependency used by exactly one file.** Flag: "Single-use dependency — consider inlining or removing."

## What Good Looks Like

**Before — Complex nested conditional (CC=12):**
```typescript
function calculateShipping(order: Order, user: User, warehouse: Warehouse): number {
  let cost = 0;
  if (order.items.length > 0) {
    if (user.isPremium) {
      if (order.total > 100) {
        cost = 0;
      } else {
        if (warehouse.isNearby(user.address)) {
          cost = 5;
        } else {
          cost = 10;
        }
      }
    } else {
      if (order.total > 50) {
        if (warehouse.isNearby(user.address)) {
          cost = 7;
        } else {
          cost = 12;
        }
      } else {
        cost = warehouse.isNearby(user.address) ? 10 : 15;
      }
    }
  }
  return cost;
}
```

**After — Guard clauses + lookup (CC=3):**
```typescript
const SHIPPING_RATES = {
  premium:  { nearby: 0, far: 0, freeThreshold: 100,  base: 0 },
  standard: { nearby: 7, far: 12, freeThreshold: 50,   base: 15 },
} as const;

function calculateShipping(order: Order, user: User, warehouse: Warehouse): number {
  if (order.items.length === 0) return 0;

  const tier = user.isPremium ? 'premium' : 'standard';
  const rates = SHIPPING_RATES[tier];

  if (order.total > rates.freeThreshold) return 0;

  return warehouse.isNearby(user.address) ? rates.far : rates.base;
}
```

## Deliberate Practice

1. **The 500 → 300 Challenge:** Find a 500+ line file in your codebase. Measure its complexity. Spend exactly 30 minutes simplifying it. Goal: reduce lines by 40% without breaking any tests. Record baseline and final complexity scores.
2. **Guard Clause Conversion:** Find 5 functions with 3+ nesting levels. Convert each to guard clause pattern (early returns). Count how many indentation levels you eliminated. The first one will feel awkward. By the fifth, it will be instinctive.
3. **Chesterton's Fence Hunt:** Find 10 lines of code you think are dead. For each, run `git log -S` and `git blame`. Categorize: truly dead, load-bearing, or indeterminate. How many were actually dead? The ratio will calibrate your deletion instincts.
4. **Conditional Table Refactor:** Find a function with 5+ if-else branches on the same variable. Convert to a lookup table or object literal. Measure: does the refactored version have higher or lower cognitive complexity? (It should always be lower.)
5. **Naming Audit:** Take a 200-line module. For every variable and function name, ask: "Would a new team member understand this without reading the implementation?" Rename anything that fails this test. Run tests. Observe: how many comments became redundant?

## Gotchas

- **Deleting error-handling code because "it never happens."** Production logs show the "impossible" null pointer happens 10,000 times per day at scale. Every `catch` block, null guard, and defensive check exists because someone got paged at 3 AM. **Total cost: $15,000-$50,000 per incident in engineering hours + revenue loss.**
- **Golfing code so aggressively it becomes unreadable.** A 3-line ternary chain with nested destructuring and a spread operator is NOT simpler than a 10-line function with named intermediates. The reader loses 5 minutes decoding the trick every time they encounter it. **Total cost: $2,500-$10,000/year in cumulative engineer confusion across a 10-person team.**
- **Removing a seemingly redundant `Array.isArray()` check.** JavaScript: `typeof [] === 'object'`. That check was guarding against an API that sometimes returns a single object instead of an array. Removing it causes a `[].map is not a function` error in production. **Total cost: $8,000-$25,000 in debugging, hotfix, and postmortem.**
- **Extracting a function used exactly once.** The extraction adds 6 lines (signature, JSDoc, export, import, call) to save 3 lines of inline code. Net +3 lines AND the reader now has to jump to a different location. Premature abstraction is the #1 cause of "enterprise Java" syndrome. **Total cost: $1,000-$5,000/year in navigation friction.**
- **Simplifying code that has an open bug report attached.** The bug report describes specific behavior. Your simplification changes that behavior. The bug is now "fixed" for the wrong reason, masking the root cause. Three months later, the real bug resurfaces in a different form. **Total cost: $10,000-$30,000 in misdiagnosed recurrence.**
- **Applying functional patterns to imperative code without team buy-in.** You convert a simple `for` loop to `reduce` with a composed transducer pipeline. It's elegant. Nobody else on the team understands it. They revert your change in the next sprint. **Total cost: $500-$2,000 in wasted effort + team friction.**
- **Removing a "useless" log statement that was the only monitoring signal.** That `console.log('payment processed')` looked redundant — except it was the only line grep'd by the on-call dashboard. Removing it blinds the ops team to payment failures for 6 hours. **Total cost: $20,000-$100,000 in missed revenue during monitoring blackout.**

## Verification

- [ ] All existing tests pass with zero changes to test files
- [ ] Cyclomatic complexity decreased for every modified function (measure before and after)
- [ ] Test coverage did not decrease (or intentional coverage removal is documented)
- [ ] No behavioral changes (same outputs, same exceptions, same side effects)
- [ ] Chesterton's Fence check completed for every removed line of code
- [ ] Rule of 500: no modified file exceeds 500 lines without documented justification
- [ ] Comment ratio decreased or remained stable (did not increase)
- [ ] `git diff --stat` shows net-negative or neutral line count (more deletions than additions)
- [ ] Code review confirms readability improvement (ask a colleague to read the diff)

## References

- [Core Workflow](../references/core-workflow.md) — Detailed step-by-step with more code examples
- [Anti-Patterns](../references/anti-patterns.md) — Common simplification failures by language
- [Best Practices](../references/best-practices.md) — Proven simplification techniques with benchmarks
- [Calibration](../references/calibration.md) — Complexity score thresholds and when to stop
- [Checklist](../references/checklist.md) — Pre-merge verification checklist
- [Error Decoder](../references/error-decoder.md) — Common simplification error messages and fixes
- [Footguns](../references/footguns.md) — Simplifications that frequently backfire
- [Scale Depth](../references/scale-depth.md) — Simplifying at scale: monorepo, microservices, legacy
