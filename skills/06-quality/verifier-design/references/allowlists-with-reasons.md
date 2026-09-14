# Allowlists With Reasons — property, not circumstance

> An allowlist entry is a rule being switched off for one input. That is a decision, and a decision
> without a stated reason is indistinguishable from an accident.

---

## The two kinds of exemption

Every exemption entry either names a **property of the input** or a **circumstance of the moment**.
Only the first is an exemption. The second is a deletion that has not been cleaned up.

| Entry | Kind | Verdict |
|-------|------|---------|
| `severity1..4` — a bleed severity is a clinical scale, identical in every appearance, so it is not an appearance-dependent role | Property | ✅ Legitimate. The property makes the input genuinely outside the rule's scope, and it will still be true in five years. |
| `Record` — a TypeScript builtin the type map legitimately emits | Property | ✅ Legitimate, and it fixed a first run of 28 false positives |
| `auth/*` — legacy, revisit later | Circumstance | ❌ Not an exemption. Nothing about `auth/` makes raw literals correct there. |
| `# noqa: E501 — ticket ENG-4471` | Circumstance | ❌ A ticket number is not a reason. It names who asked, not why the rule does not apply. |
| `added 2024-03` | Circumstance | ❌ A date records when, not why. It reads as a decision and functions as a reminder nobody set. |
| `# nolint — third-party shim, we do not control the file` | Property | ✅ Legitimate. Ownership is a property of the input. |

### The test to apply

> **Would this entry need to change if the input's *content* changed, but its *nature* stayed the
> same?**

A clinical severity scale stays a clinical severity scale whatever values it contains. A third-party
file stays third-party when it is regenerated. Both pass. An entry that says "legacy" fails, because
nothing about the input's nature is being claimed — only a story about its history.

---

## The shape of a good entry

An exemption entry needs three fields, and the third is the one everyone omits:

```
1. WHAT      — the exact match (path, symbol, pattern, key)
2. WHY       — the property of the input that puts it outside the rule's scope
3. BOUND     — what would have to change for this exemption to be wrong
```

The bound is what makes the exemption auditable. Without it, the entry has no expiry condition and
nobody can tell whether it still applies. With it, the next reader can check the condition in
seconds.

### Worked examples

```
# ✅ Property + bound
[severity1..4]
reason  = A bleed severity is a clinical scale (1-4). It is identical in every
          appearance mode, so it is not an appearance-dependent colour role.
bound   = If severities ever become appearance-dependent (a dark-mode clinical
          variant), this exemption is wrong and must be removed.

# ✅ Ownership + bound
[auth/sso/shim/*.ts]
reason  = Third-party generated shim. We do not author or maintain this file;
          the vendor's generator rewrites it on every upgrade.
bound   = If we fork the shim and begin editing it, the ownership reason fails
          and the file must be brought into scope.

# ❌ Nothing here is testable
[auth/*]
reason  = legacy
```

---

## The allowlist as a set

Individual entries can each look reasonable while the **set** is the real problem. Review the
allowlist as a whole, on a schedule, with three questions:

| Question | What a bad answer looks like |
|----------|------------------------------|
| Is the list longer than the rule's pattern? | A rule with a 6-line pattern and a 40-line allowlist is a list of exceptions with a rule attached |
| Does every entry name a property? | Any entry that names only a circumstance is a candidate for deletion or for the input being fixed |
| Do the entries share a pattern? | Ten entries matching `*.generated.*` mean the rule should exclude generated paths as a category, not as ten exceptions |

The third question is the productive one. A cluster of exemptions is the rule telling you it needs a
**scope**, not ten exceptions. Ten exceptions encode a category badly; one scope rule encodes it
correctly and keeps the count honest.

---

## Allowlists that carry reasons, mechanically

Three techniques make reasons structural rather than aspirational:

### 1. Reason-in-line, required by the parser

If the checker parses its own allowlist and refuses to run when an entry has no reason field, the
reason cannot be omitted. This is the strongest option, because it makes the discipline mechanical
rather than cultural.

```
entries:
  - match: "severity[1-4]"
    reason: "clinical severity scale; identical in every appearance"
    bound:  "remove if severities become appearance-dependent"
  - match: "auth/sso/shim/*.ts"
    reason: "third-party generated; we do not author it"
    bound:  "remove if we fork and edit it"
```

### 2. Count-per-entry in the output

Report, alongside each exemption, how many findings it suppressed on the last run:

```
exemption             suppressed   reason
severity[1-4]                 0     clinical severity scale
auth/sso/shim/*.ts            7     third-party generated
legacy-overrides.css         41     legacy
```

The third row is self-indicting: an exemption suppressing 41 findings is a rule being switched off.
The count turns an invisible decision into a visible one.

### 3. Exemption with an owner and a review trigger

Attach the person or team and the event that should reopen the decision:

```
auth/sso/shim/*.ts  owner: platform-team  review: on next vendor upgrade
```

"On next vendor upgrade" is a trigger an event can fire. "Next sprint" is a trigger nothing fires.

---

## What an exemption is not

**It is not a way to ship a defect.** An input that violates the rule's intent is a defect, exempted
or not. The exemption changes who has to fix it and when, never whether it is correct.

**It is not a severity change.** Downgrading a rule to advisory is a different mechanism with a
different cost (see `severity-calibration.md`): the finding still appears, in a place the team reads
as noise.

**It is not permanent.** A property-based exemption may last years, but it lasts because the
property holds, not because the entry was written carefully. The bound is what makes that
checkable.

**It is not a substitute for narrowing a pattern.** If the rule flags 80 legitimate inputs and the
team writes 80 exemptions, the effort has produced a rule that catches nothing plus a list nobody
maintains. Narrow the pattern first; the exemptions should then be few and boring.

---

## Procedure

```
An exemption is proposed.

  Does it name a property of the INPUT (not of the moment, the ticket, or the date)?
  ├── No → REFUSE. Either narrow the rule's pattern or fix the input.
  └── Yes ↓
      Does the property put the input outside the rule's SCOPE, or inside it but tolerated?
      ├── Outside the scope → ALLOW, and record what would invalidate the property.
      └── Inside the scope, tolerated ↓
          This is a debt exemption. It needs an owner AND a trigger event AND a count.
          └── If any of the three is missing, keep the rule advisory instead and publish
              the finding count. Do not create a silent exemption.

  Then, as a set: is the allowlist longer than the rule's pattern?
  ├── No  → done.
  └── Yes → the rule is wrong. Cluster the entries by shared pattern and express the
            cluster as a scope exclusion, not as N exceptions.
```
