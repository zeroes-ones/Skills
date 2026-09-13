# Suppression Policy

<!-- STANDARD: 3min -- bounded suppressions, reasons, budgets and the visible count -->

## The problem

A lint finding is sometimes wrong. The response determines whether the gate survives.

| Response | Consequence |
|---|---|
| Suppress the specific rule at the specific site, with a reason | the gate keeps working; the exception is visible |
| Disable the rule globally in config | the check is gone for the code that needed it |
| Disable the linter in CI "temporarily" | the gate is gone, and the "temporarily" is permanent |
| Add a bare disable comment | an accident and a decision become indistinguishable |

This is R4: suppressions are bounded, reasoned, and counted.

## The three requirements

Every suppression has all three, or it is a defect:

| Requirement | Detail | Why |
|---|---|---|
| **The rule is named** | `eslint-disable-next-line no-console`, not `eslint-disable` | a file-wide disable hides future findings of every rule |
| **A reason is given** | a short justification or a linked issue | an unexplained suppression cannot be reviewed or retired |
| **The scope is minimal** | one line, or the smallest block that works | a wider scope suppresses findings nobody intended to allow |

## The forms, per language

| Language | Scoped form | Note |
|---|---|---|
| TypeScript/JS | `// eslint-disable-next-line rule-name -- reason` | ESLint supports the `--` reason convention |
| Swift | `// swiftlint:disable:next rule_name` | the `:next` form is the scoped one |
| Kotlin | `@Suppress("RuleName")` | annotation-scoped by nature |
| Rust | `#[allow(clippy::rule_name)]` | attribute-scoped |
| Python | `# noqa: E501  # reason` | rule code required; a bare `# noqa` is a defect |
| C/C++ | `// NOLINT(rule-name)` | clang-tidy reads the parenthesised form |
| Go | `//nolint:rule // reason` | golangci-lint reads the rule and the reason |
| Shell | `# shellcheck disable=SC2086 # reason` | rule code required |

**The pattern across languages:** all of them support a *rule-specific* form, and several support an inline reason. There is no good excuse for the bare form.

## Making the count visible

An invisible count grows. A visible one is noticed.

```bash
# A suppression report, run in CI and printed to the summary
set -euo pipefail
SRC="${1:-.}"

count() { grep -rInE "$1" "$SRC" --include="*" 2>/dev/null | wc -l | tr -d ' '; }

echo "Suppression report"
echo "  eslint-disable : $(count 'eslint-disable')"
echo "  swiftlint      : $(count 'swiftlint:disable')"
echo "  ktlint/detekt  : $(count '@Suppress')"
echo "  clippy allow   : $(count '#\[allow\(clippy')"
echo "  noqa           : $(count '# noqa')"
echo "  nolint         : $(count 'nolint')"
echo
echo "Totals by rule (top 10):"
grep -rhoE '(eslint-disable(-next-line)?|swiftlint:disable(:next)?|# noqa:|nolint:|NOLINT\()[^ ]*' "$SRC" 2>/dev/null \
  | sed 's/.*[ (:]//' | sort | uniq -c | sort -rn | head -10
```

Run it in CI, print it to the build summary, and the growth becomes visible without anyone asking.

**What to do with the number:**

| Observation | Inference |
|---|---|
| Flat or falling | the policy is healthy |
| Rising slowly | normal drift; review at the cadence |
| Rising fast, concentrated on one rule | the rule is probably wrong for this repo — relax it globally with a recorded reason |
| Rising fast, spread across rules | the gate's severity or the baseline is misconfigured |
| A rule appears with hundreds of suppressions | that rule is effectively disabled; decide deliberately |

## The budget

A per-language budget turns growth into a signal:

```yaml
# Suppression budgets — CI fails if exceeded
typescript: 40
swift: 15
kotlin: 25
python: 10
rust: 5
```

**Rules for a budget:**

1. **Set it from the current count**, plus a small allowance — not from an aspiration.
2. **Exceeding it requires a recorded decision**, like a budget increase anywhere else.
3. **Lower it when the count falls**, so the budget is a ratchet rather than a ceiling that drifts upward.
4. **Never raise it silently** to unblock a release — that is the failure the budget exists to prevent.

## Reviewing stale suppressions

Suppressions outlive their reasons. A cadence catches them:

```text
Quarterly:
  1. Run the suppression report.
  2. For each suppression older than a set period, check whether the reason still holds.
     ├── Rule no longer applies (tool upgrade, code refactor) → remove it
     ├── Reason no longer valid → remove it, fix the finding
     └── Reason still valid → keep it, and refresh the date/issue link
  3. Record how many were removed.
```

A suppression whose stated reason is no longer true is a suppression that should be deleted — and deleting it usually reveals a finding that was fixed long ago.

## Global relaxations, done properly

Sometimes the rule is genuinely wrong for the repository. That is legitimate — but it is a *different action* from a suppression, and it must be recorded as such.

| Situation | Action |
|---|---|
| The rule conflicts with the domain (a CLI that must print) | disable the rule globally, with a written reason and an owner |
| The rule is a duplicate of a stronger check | disable it, naming the stronger check |
| The rule is deprecated or superseded | remove it from the config entirely |
| A finding is a false positive in one pattern | **scope the suppression**, not the rule |

**The distinction to keep:** a global relaxation is a *policy decision* reviewed by whoever owns the policy; a suppression is a *site exception* reviewed by the code owner. Conflating them lets site exceptions accumulate as if they were policy.

## The security carve-out

Some rules are not suppressible to ship a release:

| Rule class | Examples |
|---|---|
| Injection sinks | unsanitised query construction, `dangerouslySetInnerHTML`, `exec` with interpolation |
| Unsafe deserialisation | `pickle.loads`, unvalidated `yaml.load` |
| Hardcoded secrets | credential-shaped string literals |
| Cryptographic misuse | disabled certificate verification, weak-hash use |
| Access-control bypass | a suppressed authorization check |

A suppression on one of these means shipping a known defect. Refuse, fix the finding, or escalate to `appsec-engineer` — and record the escalation. This is the Anti-Hallucination rule made concrete.

## Checklist

- [ ] Every suppression names the rule (R4)
- [ ] Every suppression carries a reason (an issue link or a short justification)
- [ ] Every suppression uses the smallest scope that works
- [ ] Bare, file-wide and reason-less suppressions are treated as defects
- [ ] The total is reported per language in CI, with a top-rules breakdown
- [ ] A per-language budget exists, set from the current count, and it ratchets downward
- [ ] Exceeding a budget requires a recorded decision
- [ ] Stale suppressions are reviewed on a stated cadence
- [ ] Global rule relaxations are recorded as policy decisions with an owner
- [ ] Security-relevant rules are excluded from the suppression policy entirely
