# Severity Calibration — how a rule stops being ignored

> "A gate that cries wolf gets ignored, and an ignored gate is worse than no gate." That sentence is
> the whole reason this discipline exists. This file is the arithmetic behind it.

---

## The ignored gate is a negative-value asset

A gate that is ignored is not merely useless. It is worse than nothing, for three measurable
reasons:

| Effect | Mechanism |
|--------|-----------|
| **Coverage illusion** | The gate appears in the inventory of controls. Audits, reviews, and onboarding all count it as protection that does not exist. |
| **Signal pollution** | Every legitimate finding is buried in noise, so the real findings that do get through are not read either. |
| **Trust decay** | The team learns that a gate's output is noise, and generalises that lesson to gates that are not noisy. |

The third is the expensive one and the hardest to reverse. A team that has learned to skip gate
output must be re-taught, and the re-teaching happens by demonstration, not by policy.

```
cost of a noisy gate ≈ (findings per run × triage cost + trust damage)
                     + (defects missed while the noise is being triaged) × cost per escape
```

The trust term does not appear on any dashboard. It is the term that decides whether the gate
still exists in a year.

---

## Measure before you choose a severity

Severity is an output of measurement, never an input. The measurement is short:

```
run the rule on the CURRENT corpus (not on the change, not on a sample)
  total_findings      = N
  real_findings       = T      (triage each one; do not estimate)
  spurious_findings   = N - T

precision = T / N
```

Then choose severity from the pair `(N, precision)`:

| N (findings) | precision | Severity | Reasoning |
|--------------|-----------|----------|-----------|
| Small | High | **Blocking** | The gate is telling you something real and rare — exactly what a gate is for |
| Small | Low | **Blocking, after narrowing** | Rare false positives are usually a single pattern to exclude with a reason, not a reason to soften the rule |
| Large | High | **Blocking, but fix the corpus first** | The rule is right and the corpus is wrong. Shipping it blocking before the backlog is cleared will produce a week of ignored output |
| Large | Low | **Advisory until narrowed** | This is the dangerous quadrant. A blocking rule with this profile is how gates get deleted |

**The failure mode this table prevents:** a rule's first run produces 28 findings, every one a false
positive (a whitelist omitted a builtin the type map legitimately emits). The rule is right in form
and wrong in data. Shipping it at blocking severity on that run trains the team to ignore it within
the first day.

---

## Tiering by ownership

The single most effective calibration technique, and the one with a clear principle behind it:

> **Strict inside the boundary that owns the concept. Duplication-only outside it.**

### The case

A design gate policed every raw colour literal and reported **80 violations, mostly legitimate
scrims**. The rule was correct: raw colour literals are a defect inside the design system, because
they bypass the token pipeline. Outside the design system, a raw literal is sometimes the only way
to express an overlay.

Shipping the single loud rule produced a finding set nobody read. The fix was two rules:

| Tier | Scope | What it checks | Severity |
|------|-------|---------------|----------|
| Strict | Inside the design system | Every raw literal — the pipeline is supposed to own this | Blocking |
| Permissive | Everywhere else | **Duplication only** — the same literal repeated, which is the copy-paste defect | Advisory |

The tiering works because it separates two different defects that happen to share a syntax:

* *Inside the boundary*: using a raw value **instead of** the token it should use.
* *Outside the boundary*: **repeating** a value that will drift when the token changes.

The second is the real defect outside the boundary, and it is detectable without flagging the
legitimate one-off.

### Why "ownership" and not "convenience"

A tier boundary drawn at ownership is stable: the design system directory is a fact about the repo,
it exists for a reason, and the rule's strictness follows from that reason. A tier boundary drawn at
"wherever it was noisy" is a snapshot of one day's findings and will be wrong next quarter.

### The three legitimate tiers

```
1. STRICT       inside the boundary that owns the concept   → blocking
2. DUPLICATION  repeated values, anywhere                    → advisory or blocking
3. AUDIT        newly added occurrences in the diff           → blocking on new code only
```

Tier 3 is the `--delta` pattern: block only on violations this change introduces. It is legitimate
**only** when paired with a plan to reduce the pre-existing count, because a rule that is entirely
grandfathered constrains nothing (see `joint-rule-contradiction.md`).

---

## Narrow the pattern before softening the rule

Most "noisy rule" complaints are pattern defects, not threshold defects. The check to run first:
**does the pattern match a family or a defect?**

| Pattern matches | Diagnosis | Fix |
|-----------------|-----------|-----|
| The defect, precisely | The rule is correct; the corpus is wrong | Keep severity, fix the corpus |
| A family containing the defect | Pattern too broad | Narrow the pattern to the defect |
| A rare spelling of the defect | Pattern too narrow | **Widen it**, and add a probe in the common spelling |
| A proxy correlated with the defect | Wrong assertion | Replace the proxy with the property itself |

Row 3 is the counter-intuitive one and the most common silent failure. A motion gate matched
`slideInHorizontally(` — the call-with-parenthesis form. Kotlin's trailing-lambda form,
`slideInHorizontally { width -> width }`, is the more idiomatic way to hand-roll the same slide, and
it passed through untouched. The gate's severity was irrelevant: it had no coverage of the common
case.

**Narrowing and widening are both calibration**, and both are driven by the same measurement — what
the rule actually matched on the real corpus.

---

## The severity decision procedure

```
Run the rule on the current corpus. Count N, triage to T.

T / N is high and there is a boundary that owns the concept?
├── Yes → STRICT inside the boundary, DUPLICATION outside. Blocking on the strict tier.
└── No  → Is the pattern matching the defect or a family?
    ├── A family → NARROW the pattern. Re-measure. Do not change severity yet.
    └── The defect → T / N is genuinely low because the corpus has real debt:
        ├── Is there budget to fix the debt now?
        │   ├── Yes → fix it, then block. Blocking a debt-laden corpus produces noise.
        │   └── No  → ADVISORY with the count published, plus a named owner and a date.
        │             Never silently downgrade: record the decision and its trigger.
        └── Is T / N low because the rule cannot tell the cases apart?
            └── The check needs more information (a path, a symbol, a marker),
                not a lower severity. See the anti-pattern in SKILL.md.
```

---

## Anti-patterns specific to severity

| ❌ | Why it is wrong |
|----|----------------|
| Downgrading to advisory to make CI green | The finding is unchanged; only the visibility is. This is deletion with extra steps. |
| Adding `continue-on-error: true` | The gate runs, fails, and does not affect the pipeline. The most expensive form of a false control, because the log still shows it running. |
| Exempting the noisy files individually | The exemption list becomes the rule's real definition. Review it as a set: if it is longer than the pattern, the pattern is wrong. |
| "We will fix the debt next sprint" with no owner | The rule is grandfathered forever. Attach an owner and a date, or keep it advisory and publish the count. |
| Choosing severity from the change under review | Severity is a property of the rule on the corpus, not of the diff that happened to reveal it. |

---

## The one measurement to keep

Publish, for every rule: **findings on the last full run** and **the count of those that were real**.
Two numbers per rule, in a table, updated when the rule changes.

```
| Rule              | Findings | Real | Precision | Severity | Owner |
|-------------------|----------|------|-----------|----------|-------|
| design-literals   | 2        | 2    | 1.00      | blocking | ds    |
| theme-compliance  | 0        | —    | —         | blocking | ds    |
| raw-colour (all)  | 80       | 11   | 0.14      | retired → tiered | ds |
```

The table is the artefact. It makes the ignored gate visible before the team stops reading it, and
it makes the deletion of a rule a recorded decision rather than a quiet edit.
