# Related Reading — where verifier-design plugs into the library

> This skill owns one question: **how do you know a check works?** Several neighbouring skills touch
> verification from different angles, and confusing them is the most common routing error. This file
> is the disambiguation.

---

## The four verification skills, and the line between them

| Skill | Owns | The question it answers |
|-------|------|------------------------|
| **`verifier-design`** (this) | The design of a check | "How do we know this linter/gate/validator actually catches the class it claims?" |
| `verification-independence-engineer` | The information boundary between producer and verifier | "Who should check this, and what may they see while checking?" |
| `verification-before-completion` | Evidence for one completed task | "Is *this* change actually done and correct?" |
| `agent-eval-pipeline` | Probabilistic evaluation of agent output | "How do we score a non-deterministic system against expectations?" |

The cleanest way to hold the distinction:

```
verifier-design                  builds and calibrates the instrument
verification-independence        decides who holds the instrument
verification-before-completion   reads the instrument for one task and decides "done"
agent-eval-pipeline              builds an instrument for a system whose output has a distribution
```

An example that separates all four. A team ships a schema-drift check:

* **verifier-design**: does the check fire on injected drift? Does it stay silent on a legitimate
  schema change? Is it comparing final emitted types or pre-transform names? Was its severity
  calibrated against the real corpus?
* **verification-independence-engineer**: is the check run by the same agent that wrote the schema?
* **verification-before-completion**: for this particular migration, did the check pass *and* was
  everything else done?
* **agent-eval-pipeline**: if a model generates the schema, how do we measure the drift rate over
  many generations?

---

## The distinction that causes the most misrouting

`verification-before-completion` and this skill both use the word "verification". They differ in
what they treat as given:

| | `verification-before-completion` | `verifier-design` |
|---|---|---|
| Assumes | the test suite is trustworthy | nothing; the suite is a claim under audit |
| Output | evidence that one task is done | evidence that a check works, ever |
| Failure it prevents | marking broken work complete | a gate that has never caught anything |
| Time horizon | this change | the rule's remaining lifetime |

If the question contains "this PR", "this fix", or "is it done" — it is
`verification-before-completion`. If it contains "our lint", "the gate", "the CI check", "always
catches", or "0 problems" — it is this skill.

---

## Where this skill's output goes

```
verifier-design produces
  ├── fire cases + silent cases      → tdd-guide, qa-engineer (as fixtures and probes)
  ├── calibrated severity + counts   → ci-cd-builder (where the gate runs, at what severity)
  ├── blind-spot declarations        → shipping-and-launch (what the release gates do NOT cover)
  └── proof the validator works      → verification-independence-engineer (a validator must
                                        itself be calibrated before its independence matters)
```

The last arrow is worth stating explicitly: **independence is worthless if the independent check
cannot fail.** A perfectly separated verifier that shares an assumption with the producer's
intermediate representation (R3) reproduces the producer's blindness with more ceremony.

---

## Adjacent skills and what to borrow from each

| Skill | Borrow this |
|-------|------------|
| `debugging-and-error-recovery` | The layer-elimination move: find the observation that rules out a whole layer rather than fixing the next plausible cause. That is the same discipline as the negative control, applied to a failure instead of a check |
| `qa-engineer` | Test-pyramid placement, and the documented-target versus enforced-floor split: a high absolute coverage target invites assertion-free tests, while a high patch bar plus a low drop tripwire gets the behaviour |
| `tdd-guide` | Behaviour-named tests. Naming a test after the defect it guards is the same act as naming a check after the defect class it catches |
| `ci-cd-builder` | Where a gate executes, whether its failure propagates to the pipeline verdict, and whether the path filter can skip it |
| `code-formatting-and-linting` | Rule configuration, precedence across tools, and the reason a formatter's autofix is a different category from a lint rule's finding |
| `observability-engineer` | Making a check's activation observable. A gate that engages silently is a gate whose false-positive rate cannot be measured |
| `repo-scaffolding` | The repository's standard gate set, so a new check reuses the established convention instead of inventing a fifth |
| `code-reviewer` | What review is genuinely for — novel classes, intent, external-standard mismatches — which is the residual left after the mechanical signals |
| `supply-chain-security` | Provenance and integrity checks, which are the purest example of "verify the artefact, not the declaration" |
| `verification-independence-engineer` | Producer/verifier separation, and the information boundary a validator should be given |

---

## Reading order for someone new to the discipline

1. `proving-a-check-fires.md` — the core, and the one that changes behaviour fastest.
2. `negative-controls.md` — the cheapest habit, and the one most often skipped.
3. `severity-calibration.md` — why a correct rule still gets deleted.
4. `artefact-versus-configuration.md` — the class of defect no existing signal sees.
5. `joint-rule-contradiction.md` — the most generalisable idea in the set.
6. `allowlists-with-reasons.md` — the maintenance discipline that decides whether the gate survives.
7. `discovery-ratio.md` — the budget argument for where to spend next.
8. `failure-narratives.md` — the same content as stories, for recall.
9. `verification-recipes.md` — the runnable form, for use.
