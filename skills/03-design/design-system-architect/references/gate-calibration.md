# Gate Calibration

<!-- DEEP: 10+min — severity tiers, vocabulary from generated artifacts, and proving a gate fires -->

## What only a gate can catch

A design-system rule has a specific shape: breaking it produces code that **compiles, renders
plausibly, and looks correct on the machine that wrote it**. A rule with that shape cannot be
enforced by care, because care is what produced it.

The four rules of this shape in this domain:

| Rule | Why review cannot hold it |
|---|---|
| a screen must read a role, not a primitive | the primitive renders correctly in the author's appearance setting |
| a component dimension must not use a spacing step | the numbers are real design values and the result looks right |
| a platform must read a role, not a raw scale member | the raw member is a valid value in that language |
| the type mapping must be monotonic | both platforms compile; only a side-by-side reading reveals the inversion |

Each needs a **signal**, not a reminder.

## Gate design, in order

### 1. Can a developer act on the finding without triage?

If not, the gate is not ready. The failure mode is well documented in this domain: a design gate
policed every raw colour and produced 80 violations, most of them legitimate overlays and scrims. A
list that needs triage before action gets switched off — and an ignored gate is worse than no gate,
because it manufactures confidence.

### 2. Where does the vocabulary come from?

**From the generated artifact, never from a literal in the script.** A guard carrying its own copy of
the palette keys, role names, or scale members disagrees with the real tokens the moment either
changes — and then it reports correct code as broken.

```
# wrong
PALETTE = ["cream", "gold", "charcoal", ...]     # a copy. Drifts. Then lies.

# right
PALETTE = read_keys_from(generated_tokens_artifact)
if not PALETTE: fail_loudly()                    # unreadable is a finding, not a silent skip
```

The "fail loudly if unreadable" clause matters as much as the read: a gate that silently finds no
vocabulary reports clean on everything.

### 3. One severity or two?

| Rule character | Severity model |
|---|---|
| always wrong wherever it appears (a raw palette value on a screen) | single error severity |
| correct inside the design system, usually wrong outside it | strict inside, advisory outside |
| usually wrong, occasionally legitimate (a bare dimension) | error inside the design system, warning at call sites |

The tiering detail that makes this work: **a bare dimension is an error inside the design system and
a warning at a call site.** A screen may legitimately need a size no shared control uses; a
design-system primitive may not, because that is where the scale is defined. One rule, two severities,
each chosen for the place it applies.

### 4. Has it been shown firing?

This is the step that is skipped and the one that matters most. The pattern:

```bash
# inject a real violation of the class the gate exists for
sed -i '' 's/roleBackground/rawCharcoal/' <screen>.swift
python3 scripts/check-theme-compliance.py       # MUST exit 1 and name file:line
git checkout <screen>.swift
python3 scripts/check-theme-compliance.py       # MUST exit 0
```

Both runs are the evidence. The firing run proves the check is connected to the thing it claims to
check; the silent run is the control that proves it does not fire on clean input.

### 5. Accept every spelling the platform allows

A gate keyed on the rarer spelling of a call covers the wrong thing. A motion gate matched the
explicit call form and let the **trailing-lambda form** — the more likely way to hand-roll the same
thing — pass straight through. It was found only by writing a probe and watching the gate stay silent.

For design tokens this generalises directly: a role is spelled differently in each platform's idiom,
and a role-use detector keyed on the long form alone false-positives on every migrated call site.

### 6. Exempt by name, with the reason

An exemption is legitimate when the excluded members genuinely sit outside the rule's intent. Two
requirements:

* **by name**, listing them, not a wildcard over a class;
* **with the reason written where the rule lives**, because an allow-list entry with no reason
  outlives the decision that justified it.

An exemption without a reason is worse than the literal it permits.

## The three defect classes a gate must survive

| Gate defect | Symptom | Cause |
|---|---|---|
| Silent on the defect class | reports clean while the codebase visibly violates the rule | compares values against a list it carries internally, or matches the rarer spelling |
| Fires on everything | 80 findings, mostly legitimate | one severity for a rule that only holds in one scope |
| Reports the truth as a violation | names correct code as broken | its vocabulary disagrees with the generated source |

All three are cured by the same two habits: **read the vocabulary from the generated artifact**, and
**show the gate failing on an injected violation before trusting its clean report**.

## A note on `--delta` grandfathering

Where a gate is added to a codebase that already carries debt, the standard approach is a
delta mode: block only on violations the change introduces, report pre-existing ones without
blocking. That is sound, provided the delta baseline is real. A delta mode whose baseline is
"everything currently present" quietly becomes "no violations block" — which is the same
manufactured-confidence failure as a gate that never fires.
