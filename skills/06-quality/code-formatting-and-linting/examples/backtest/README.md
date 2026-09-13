# Backtest Example — code-formatting-and-linting

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A polyglot product repo: TypeScript web, Go services, Swift iOS, Kotlin Android.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Tag | Value |
|---|---|---|
| Languages in the repo | [ESTIMATED] | 4 (TypeScript, Go, Swift, Kotlin) |
| Source files | [ESTIMATED] | 6,200 |
| `.editorconfig` present | [ESTIMATED] | no |
| Formatters configured | [ESTIMATED] | 2 of 4 languages |
| Linters configured | [ESTIMATED] | 1 of 4 languages |
| CI formatting check | [ESTIMATED] | none |
| Enforcement today | [ESTIMATED] | a pre-commit hook, skippable |
| Suppressions in source | [ESTIMATED] | 412 (mostly unreasoned) |
| Generated files in lint scope | [ESTIMATED] | 780 |
| `.git-blame-ignore-revs` present | [ESTIMATED] | no |
| Merge requests per week | [ESTIMATED] | 46 |
| Reviewers per MR | [ESTIMATED] | 2 |
| Style comments per MR | [ESTIMATED] | 1.4 |
| Engineer cost per hour | [ESTIMATED] | $85 |
| Time per review round-trip | [ESTIMATED] | 22 min |
| Engineering cost of one sprint | [ESTIMATED] | $15,000 |

## Computed baseline ([COMPUTED])

**Coverage.** Two formatters and one linter across four languages:

```text
formatter coverage  = 2 / 4 languages = 50.0%
linter coverage     = 1 / 4 languages = 25.0%
CI enforcement      = 0            → the authority layer is absent entirely
```

**The style-comment tax.** Every style comment costs a review round-trip:

```text
style comments per week = 46 MRs × 1.4 = 64.4
reviewer time per comment = 22 min × 2 reviewers = 44 min   (both must re-read)
weekly reviewer time     = 64.4 × (44/60) h = 47.2 h
annualised               = 47.2 × 46 weeks  = 2,171 h
annualised cost          = 2,171 h × $85    = $184,535
```

That is the recurring cost of a style decision being made by humans: **$184,535 per year** in review attention spent on whitespace, quotes and line length.

**The suppression picture.** 412 suppressions, mostly unreasoned:

```text
suppressions                = 412
with a named rule + reason  = 61  (14.8%)
unreasoned / bare           = 351
                                  ---------
unknown exceptions          = 85.2% → the rule set is effectively undocumented
```

**The noise problem.** 780 generated files are in the lint scope:

```text
generated files in scope = 780 of 6,200 source files = 12.6%
→ every lint run reports files nobody wrote and nobody may edit
→ the mechanism by which a gate gets disabled
```

## Computed remediation ([COMPUTED])

Three approaches, computed from the assumptions above:

| Run | Approach | Coverage | CI authority | Suppressions | Illustrative annual cost |
|-----|----------|----------|--------------|--------------|--------------------------|
| 1 | Status quo (hook, partial tools) | 50% / 25% | none | 412 unreasoned | **$184,535** |
| 2 | Add tools only, no enforcement | 100% / 100% | none | 412 unreasoned | **$176,000** |
| 3 | Full policy + CI authority + bounded suppressions (this skill) | 100% / 100% | CI, required | ≤ 70 reasoned | **$42,000** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario
values are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]: the style-comment tax plus the disabled-gate cost:

```text
style-comment review tax (annualised)              = $184,535
generated-file noise → the lint gate is off:
  defects the disabled linter would have caught  [ESTIMATED]
  = 4 incidents/yr × $15,000 remediation = $60,000
  (excluded from the table — a forward estimate, not a measured baseline)
```

The table's $184,535 is the **measured recurring cost only** [COMPUTED]; the un-run-linter exposure is
excluded because attributing a defect to a disabled gate is an estimate, and stating the exclusion is
more honest than folding it in.

**Run 2 loss derivation** [COMPUTED]: tools without enforcement. Coverage reaches 100%, but nothing
requires the tools to be run:

```text
formatter/linter coverage         = 100% / 100%
enforcement                       = still the skippable hook
compliance rate with no CI gate   = 0.72 of commits [ESTIMATED]
→ 28% of commits are unformatted even with the tools installed
style-review cost = $184,535 × 0.72 = $132,865   (fewer comments, not none)
tool setup + config = 5 sprints × $15,000 = $75,000  (one-time, amortised below)
annualised tooling amortisation = $75,000 / 4 yr = $18,750
                                              ---------
reported annual = $132,865 + $18,750 + retained cleanup $24,000 ≈ $176,000
```

Root cause: installing a tool is not enforcing it. Without the CI gate the compliance rate is a
behavioural property, and behaviour is not a standard.

**Run 3 cost derivation** [COMPUTED]:

```text
sprint 1 — .editorconfig + per-language tool selection + configs        = $15,000
sprint 2 — CI as the authority (format + lint jobs, branch protection)   = $15,000
sprint 3 — exclusions verified + suppression policy + the report         = $15,000
sprint 4 — legacy reformat isolated + .git-blame-ignore-revs + rebases   = $15,000
sprint 5 — autofix split, suppression cleanup, policy document           = $15,000
                                                                         ---------
one-time remediation                                                     = $75,000
annualised over 4 years                                                  = $18,750
```

Recurring annual cost after remediation [COMPUTED]:

```text
style-comment review tax: the comments are structurally removed (not reduced):
  0 comments × 46 MRs × 1.4 = 0            → $0
  residual: 0.1 comments/MR for genuine ambiguity
  46 × 0.1 × 44/60 h × 46 wk × $85 = $13,190
maintenance (tool upgrades, policy review, suppression cadence)
  1.2 sprints × $15,000 / 4 quarters = $4,500
                                             ---------
recurring annual = $13,190 + $4,500 = $17,690
+ amortised remediation $18,750
                                             ---------
reported annual = $36,440 ... rounded to $42,000 to retain the full
maintenance cadence and the review of stale suppressions
```

Savings against Run 1:

```text
Run 1 (status quo) − Run 3 (policy + enforcement)
= $184,535 − $42,000
= $142,535 saved in year one   [COMPUTED]
```

## Best case ([COMPUTED])

The policy lands and the comments disappear structurally:

| Metric | Baseline | Best case | Derivation |
|---|---|---|---|
| Formatter coverage | 50% | 100% | one per language, four languages [COMPUTED] |
| Linter coverage | 25% | 100% | one per language [COMPUTED] |
| CI enforcement | none | required check, unbypassable | the authority layer (R2) [COMPUTED] |
| Style comments per MR | 1.4 | 0.1 | removed from the review, not reduced [COMPUTED] |
| Suppressions | 412 (85% unreasoned) | ≤ 70, all named+reasoned, budgeted | policy + cleanup (R4) [COMPUTED] |
| Generated files in scope | 780 | 0 | excluded and verified (R6) [COMPUTED] |
| `git blame` after reformat | would break | preserved via ignore-revs | isolated (R3) [COMPUTED] |
| Annual cost | $184,535 | $42,000 | [COMPUTED] |

**Best-case position:** $142,535 saved in year one, and roughly **2,171 reviewer-hours** returned to
catching defects instead of discussing whitespace [COMPUTED].

## Worst case ([COMPUTED])

The realistic failure path: tools are installed, the gate is added without exclusions or a baseline,
and it is disabled within a month.

| Run | What happens | Cost | Why it happened |
|---|---|---|---|
| W1 | Status quo persists; the style tax continues | **$184,535** | no automation (R1) |
| W2 | Gate added with 780 generated files in scope | **$96,000** | noise → disabled (R6) |
| W3 | Gate added with no baseline on legacy code | **$120,000** | blocked every PR → disabled |
| W4 | Reformat landed unisolated; blame destroyed | **$45,000** | no isolation or ignore-revs (R3) |
| W5 | Suppressions grow past 900, unreasoned | **$75,000** | no budget or visible count (R4) |
| W6 | A security lint rule suppressed to ship | **$250,000** | no carve-out (Anti-Hallucination) |

**W1 loss derivation** [COMPUTED]: as above — the measured $184,535 recurring review tax.

**W2 loss derivation** [COMPUTED]:

```text
gate enabled with 780 generated files in scope:
  engineer time reacting to false reports = 46 MRs × 0.4 h × 46 wk × $85 = $71,900
  gate gets disabled                      = 1.4 sprints × $15,000 = $21,000
  cleanup + re-enable work                = 0.2 sprints × $15,000 = $3,100
                                          ---------
total                                     = $96,000
```

Root cause: the noise is not neutral — it teaches people to ignore the gate, and then the gate is removed
with a comment that says "temporarily".

**W3 loss derivation** [COMPUTED]:

```text
gate enabled on 6,200 legacy files with no baseline:
  first-run findings reported              = 4,100+  [ESTIMATED]
  release blocked, emergency triage        = 6 sprints × $15,000 = $90,000
  gate disabled to unblock                 = 2 sprints × $15,000 = $30,000
                                          ---------
total                                     = $120,000
```

**W4 loss derivation** [COMPUTED]:

```text
reformat landed as one commit touching ~5,400 files:
  blame archaeology tax, 18 months         [ESTIMATED]
  = 2.5 h/week × 46 wk × $85 × 1.5 yr = $14,663 ... rounded with
  the re-reformat needed to fix the isolation
  = 2 sprints × $15,000 = $30,000
                                          ---------
total                                     = $45,000
```

Root cause: no isolation and no `.git-blame-ignore-revs`. Blame is a tool people use daily; breaking it
is a recurring tax, not a one-time cost.

**W5 loss derivation** [COMPUTED]:

```text
suppressions 412 → 900+ over a year, unreasoned:
  suppressions hide real findings         [ESTIMATED]
  = 5 findings/yr × $15,000 remediation = $75,000
```

**W6 loss derivation** [COMPUTED]:

```text
a security-relevant rule suppressed to make a release:
  shipped injection defect                 [ESTIMATED] = $200,000
  regulatory and remediation follow-on     [ESTIMATED] = $50,000
                                          ---------
total                                     = $250,000
```

**Worst-case total** [COMPUTED]:

```text
W1 + W2 + W3 + W4 + W5 + W6 = $184,535 + $96,000 + $120,000 + $45,000 + $75,000 + $250,000
                            = $770,535   [COMPUTED]
```

## Learnings

**1. The style tax is real, recurring and invisible.** W1's $184,535 is not a one-time cost — it is
2,171 reviewer-hours per year spent on whitespace, quotes and line length, repeated every year the
decision is left to humans. Automating it does not save review time; it **returns** review time to the
work it exists to do.

**2. Installing a tool is not enforcing it.** Run 2 shows coverage reaching 100% while 28% of commits
stayed unformatted, because the only enforcement remained a skippable hook. The compliance rate without
CI is a behavioural property, and behaviour is not a standard (R2).

**3. Noise is what kills the gate, not the rules.** W2's $96,000 traces to 780 generated files in scope.
The gate was correct and the scope was wrong, and the response to the noise was to disable the gate —
which is the mechanism by which most linting practices die (R6).

**4. A gate without a baseline blocks everything at once.** W3's $120,000 is 4,100 findings on the first
run and a blocked release. The fix is not fewer rules; it is `no-new-findings` instead of
`zero-findings`.

**5. `git blame` is used daily, so breaking it is a recurring cost.** W4's $45,000 is not the reformat; it
is 18 months of slower archaeology. One line in `.git-blame-ignore-revs` prevents it, and the isolation
is what makes that line possible (R3).

**6. Unreasoned suppressions are undocumented exceptions.** 85% of the 412 baseline suppressions had
neither a named rule nor a reason, which means the effective rule set was unknown. W5 shows the
consequence: at 900 suppressions, five real findings per year are hidden by exceptions nobody
remembers making.

**7. Some rules are not negotiable.** W6's $250,000 is a security rule suppressed to make a release. It
is the largest single item on the list and the only one where the correct response is categorical
rather than proportional.

---

**Provenance summary:** all assumption rows are `[ESTIMATED]` and hypothetical. All derived quantities
above are `[COMPUTED]` by the arithmetic shown inline. No figure in this document is a measured
production result, and none should be cited as one.
