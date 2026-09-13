# Autofix Boundaries

<!-- STANDARD: 3min -- which findings may be fixed automatically and which need judgement -->

## Why the boundary exists

An autofix that changes behaviour is not a fix; it is an unreviewed change. Separating deterministic fixes from judgment findings is what makes an autofix safe to run in CI.

| Category | Safe to autofix | Where it runs |
|---|---|---|
| Formatting | **always** — one correct output | editor, hook, **CI** |
| Lint rules with a provably safe fix | yes, if the set is reviewed and version-pinned | hook, optionally CI |
| Lint rules that change behaviour or types | no | reported, never applied |
| Security-relevant rules | **never** | reported, never applied, never suppressed |

## Classifying a rule's fix

```text
Does applying the fix change anything other than presentation?
├── No (whitespace, quotes, ordering of independent declarations)
│   → SAFE AUTOFIX
│   └── Examples: formatting, import ordering, redundant parentheses,
│       consistent type-import syntax, trailing-comma normalisation
└── Yes ↓
    Can the fix change runtime behaviour?
    ├── Yes → NEVER autofix in CI
    │   └── Examples: removing an "unused" variable with a side-effecting
    │       initialiser, rewriting a loop, replacing an API call,
    │       simplifying a condition, adding an optional chaining operator
    └── No, but it changes types or public API
        → NOT autofix-safe; require review
        └── Examples: adding explicit type annotations, extracting a constant,
            changing a signature
    Finally, regardless:
    ├── Is the rule security-relevant?
    │   └── Yes → NEVER autofix (and never suppress)
    └── Does the fix touch more than the reported line?
        └── If it spans files or modules → require review
```

## The classic unsafe "safe" fixes

These look mechanical and are not. Knowing them prevents a real class of incident.

| Fix | Why it is unsafe |
|---|---|
| Remove an "unused" variable | the initialiser may have a side effect (an I/O call, a registration) |
| Remove an "unused" import | it may carry a side effect (a polyfill, a registration module) |
| Simplify a redundant condition | the "redundant" branch may be load-bearing for a corner case, or documentation |
| Replace `==` with `===` | changes semantics for `null`/`undefined` and for coerced values |
| Add optional chaining to silence a null warning | it converts a crash into silent `undefined` propagation |
| Reorder imports | may break side-effect ordering, or a polyfill that must run first |
| Rewrite an async callback to `await` | changes error-handling semantics and execution order |
| Convert a loop to a functional form | changes `this` binding and early-exit behaviour |
| Auto-add explicit types | can narrow or widen a type in a way the author did not intend |
| Remove `await` on a "redundant" call | changes the guarantee the author was relying on |

**The pattern:** any fix that removes or rewrites *code*, rather than reformatting it, may change behaviour. Only the *fixers* a linter explicitly marks as safe for that rule should be auto-applied.

## The reviewed autofix set

Define the set once, review it, then let CI apply it:

```jsonc
// Applied automatically (deterministic, presentation-only)
{
  "autofix-rules": [
    "prettier/prettier",              // formatting
    "import/order",                   // ordering (only if no side-effect modules)
    "no-var",                         // var → let (behaviour-preserving in practice)
    "prefer-const",                   // only where re-assignment is provably absent
    "@typescript-eslint/consistent-type-imports"
  ]
}
```

Two requirements make it trustworthy:

1. **It is version-pinned.** A linter upgrade can add a new fix to a rule you marked safe.
2. **It is reviewed as a set.** Adding a rule to the autofix list is a change to what CI may do unreviewed, so it gets the same scrutiny as a CI permission change.

## How to apply it

```bash
# Local / hook: fix what is fixable, so the developer sees only real findings
eslint --fix .
ruff check --fix .
rubocop -a .

# CI: fix, then verify nothing functional moved
eslint --fix .
git diff --quiet || { echo "fixable findings were committed"; exit 1; }
```

**The CI pattern that is safest:** fix, then *fail* if anything changed, so a human decides whether to accept the fix into the branch. Autofixing and silently pushing creates an unreviewed commit — acceptable only on a single-writer branch.

## Reporting the residual

The findings that remain after autofix are the ones that need a person, and they should be reported as such:

```text
Lint summary:
  autofixable (applied)    12
  requires review           3   ← these are the gate
    - src/api/client.ts:44   no-floating-promises
    - src/db/query.ts:88     security/detect-sql-injection
    - src/ui/panel.ts:120    @typescript-eslint/no-unsafe-assignment
```

Separating the counts matters: it tells the reader that 12 findings were mechanical and 3 need thought. A single count of 15 is unactionable.

## The drift risk

An autofix set that nobody reviews drifts:

| Risk | Mitigation |
|---|---|
| A rule upgrade adds a behavioural fix to a "safe" rule | pin the linter version; re-review the set on upgrade |
| A rule is removed upstream and the entry becomes dead | the set is linted for validity, or reviewed on upgrade |
| A new language is added and inherits no autofix policy | extend the policy with the language |
| The autofix set diverges between local and CI | one config, resolved from the repo root |

## Checklist

- [ ] Formatting is autofixed everywhere, including CI
- [ ] The lint autofix set is explicit, reviewed and version-pinned
- [ ] Behaviour-changing rules are never autofixed in CI
- [ ] Security-relevant rules are never autofixed and never suppressed
- [ ] Local and CI apply the same autofix set from the same config
- [ ] CI either fails on a change or commits it deliberately (never silently, on a shared branch)
- [ ] The report separates autofixed findings from those requiring review
- [ ] The autofix set is re-reviewed on every linter upgrade
