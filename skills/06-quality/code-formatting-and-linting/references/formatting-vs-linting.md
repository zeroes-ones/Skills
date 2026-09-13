# Formatting versus Linting

<!-- STANDARD: 3min -- why the two are different categories, and why conflating them causes both classic failures -->

## The distinction that prevents most style problems

They look alike — both read source and complain — and they behave oppositely.

| Property | **Formatting** | **Linting** |
|---|---|---|
| Nature | mechanical, total | semantic, contextual |
| Correct output | exactly one per input | sometimes none, sometimes many |
| Autofix | safe and complete | partial; some fixes need judgement |
| Authority | the tool | the team, per rule |
| Failure mode if over-applied | churn and unnecessary diffs | noise that teaches people to ignore the gate |
| Failure mode if under-applied | permanent arguments | real defects shipping |

**The rule that follows:** formatting is automated, non-negotiable and invisible. Linting is a gate with a policy for exceptions.

## The two failures that come from conflating them

### Failure 1 — the formatter treated as a reviewer

```text
"We'll use Prettier, but review should double-check the formatting."
→ Reviewers comment on formatting
→ Comments differ between reviewers
→ The argument recurs
→ Review attention goes to trivia
```

The fix is not "review more carefully". It is to make formatting impossible to get wrong: the tool decides, CI enforces, and no human is asked.

### Failure 2 — the linter treated as a formatter

```text
"The linter has 4,000 findings, so we turned it off in CI and fix them when we touch the file."
→ The gate is gone
→ New violations accumulate at the same rate as old ones
→ The findings that mattered are still there
```

The fix is to separate the *autofixable* set (apply it) from the *judgement* set (gate it), and to establish a baseline rather than disabling the check.

## What belongs in each category

| Concern | Category | Why |
|---|---|---|
| Indentation, tabs vs spaces | Formatting | one correct output |
| Trailing whitespace, final newline | Formatting | one correct output |
| Quote style, semicolons, line wrapping | Formatting | one correct output |
| Import ordering | Formatting | deterministic, though some tools disagree on grouping |
| Unused variable | Linting | often indicates a real defect; sometimes intentional |
| Naming conventions | Linting | a rule with legitimate exceptions |
| Complexity thresholds | Linting | judgement-dependent |
| Security-relevant rules (injection sinks, unsafe deserialisation) | Linting | **never suppressible to ship** |
| Null-safety, exhaustiveness, type strictness | Linting | semantic; a real defect class |

**The bright line:** if the answer is "there is exactly one right way", it is formatting. If the answer is "it depends", it is linting.

## Why the boundary matters operationally

| Aspect | Formatting | Linting |
|---|---|---|
| Where it runs | on save, on commit, in CI | in CI (and optionally in the editor) |
| Whether CI may autofix | **yes** — deterministic | only for the designated autofix subset |
| Whether a suppression is acceptable | no — there is nothing to suppress | yes, with a reason and a scope |
| Whether a finding may be deferred | no | yes, against a baseline |
| What a new engineer must learn | nothing; their editor does it | the rules and the suppression policy |

Notice the last row: formatting should require **zero** learning. If a new engineer has to read a style guide, formatting is not automated.

## The naming discipline

Use the words distinctly, in the config, in CI, and in conversation:

```yaml
# CI, named clearly so failures are actionable
- name: Check formatting          # mechanical: must be clean
  run: make fmt-check

- name: Lint                      # semantic: gate with a baseline
  run: make lint
```

Two separate jobs, two separate failure messages, two separate responses. A single "style" job produces a single confusing failure.

## The decision, condensed

```text
Is there exactly one correct output for this concern?
├── Yes → FORMATTING
│   ├── Automate it completely (format on save, then a hook, then CI)
│   ├── Let CI autofix where the fix is deterministic
│   └── Never review it, never discuss it, never suppress it
└── No (it depends) → LINTING
    ├── Is the fix deterministic and safe?
    │   ├── Yes → put it in the autofix set (applied in CI)
    │   └── No  → gate it
    ├── Does it catch a security defect?
    │   └── Yes → never suppress; fix or escalate
    └── Legitimate exceptions?
        └── A scoped suppression with a reason, and a visible count
```

## Checklist

- [ ] Formatting and linting are separate jobs, named separately, in config and in CI
- [ ] No formatting concern appears in a review checklist
- [ ] Every formatting concern is fully automated with one correct output
- [ ] The lint autofix set is separated from the judgement set
- [ ] The lint gate has a baseline on legacy code, not a zero-findings requirement
- [ ] Security-relevant lint rules are excluded from the suppression policy
- [ ] A new engineer needs to learn nothing about formatting
