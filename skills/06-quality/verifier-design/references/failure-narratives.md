# Failure Narratives — the checks that shipped broken

> Every narrative below is a real gate failure from the source corpus. Each one ends with the rule it
> justifies, so the rule set is traceable to an event rather than to a preference.

---

## 1. The gate that reported clean while two compilers failed

**The gate:** a stability check over generated models. It collected referenced type names and
declared model names, and compared them.

**What it did wrong:** it used the **raw** names on both sides — before the naming transform that the
generator applies. Two spellings of one type (`PaginatedResponse_BleedLogResponse_` from the raw
reference, `PaginatedResponseBleedLogResponse` from the pascal-case conversion) were therefore
compared to each other consistently, and the mismatch was validated as agreement.

**The signal that was missing:** the Swift and Kotlin compilers were failing on the same code the
gate had just approved. The gate ran first in the pipeline and reported green; the failure surfaced
two steps later, in a language the gate's output had already excused.

**Why it survived:** reading the gate confirms what the gate says. Both sides of the comparison were
"the names", and that is what the code did. Nothing in the gate's source looks wrong, because the
bug is in the *level* at which the comparison happens, not in the comparison.

**The rule it justifies — R3:** refuse to let a check compare identifiers a transform has not
applied yet. Anchor on final emitted identifiers.

```
Wrong:  raw_ref_name       ==  raw_declared_name
Right:  to_pascal(ref_name) == to_pascal(declared_name)
        ^ or, better, on the identifier the consumer actually resolves
```

---

## 2. The gate's first run: 28 findings, every one false

**The gate:** a type-stability check over generated TypeScript.

**What it reported:** 28 "unknown type" findings.

**Why every one was false:** the whitelist omitted `Record`, a TypeScript builtin that the type map
legitimately emits. The gate was right in form and wrong in data.

**Why this matters more than a normal bug:** a gate that cries wolf gets ignored, and an ignored
gate is worse than no gate — it manufactures confidence. A first run of 28 false positives teaches
the team, on day one, that the gate's output is noise. That lesson generalises to every gate.

**The rule it justifies — R6:** refuse to ship a rule whose severity was not calibrated against
measured true and false positives.

**The procedure it produced:** triage the first run *before* the check is relied on. Count findings,
classify each as real or spurious, and choose severity from the pair. A whitelist missing a builtin
is a five-minute fix; a team that learned to ignore the gate is a multi-month fix.

---

## 3. The gate that matched only the rarer spelling

**The gate:** a motion check that flagged hand-rolled slide transitions.

**What it matched:** `slideInHorizontally(` — the call-with-parenthesis form.

**What it missed:** `slideInHorizontally { width -> width }` — Kotlin's trailing-lambda form, which
is the *more likely* way to hand-roll the same slide.

**How it was found:** by writing a probe in the common form and watching the gate stay silent. Not
by reading the gate, and not by any failure — the gate had no coverage of the common case, so it had
no failures to report.

**The rule it justifies — R1's silent-case discipline, and the probe method:** a probe is input
constructed for the purpose of being caught, written the way a developer would actually write the
violation rather than the way the rule's author would.

```
Write the probe the way the VIOLATION appears in the wild.
If the probe passes through, the gate covers a spelling, not a class.
```

---

## 4. The rule set with no legal spelling

**The declaration:** a module scope in a multi-platform tree.

**The rules:** one required scope modifiers to be explicit; another required scope declarations not
to be redundant. Both are defensible. Both applied to the same declaration.

**The result:** `ios/DeeplyDomain` + `internal` failed the redundancy rule; `ios/DeeplyDomain` alone
failed the explicitness rule. The declaration had no legal spelling in that tree.

**How it surfaced:** as a build error in a file whose author had done nothing wrong, with a message
naming neither rule.

**The rule it justifies — R5:** refuse to add a rule without a contradiction check against every
existing rule on the same space. Encode the invariant as a test:

> Every scope must have a legal spelling in every tree.

**Why this is the most generalisable narrative in the set:** every rule in the set was locally
correct. The defect existed only in their intersection, and nothing in the review process looks at
intersections, because rules are reviewed one at a time.

---

## 5. The design gate that flagged 80 legitimate inputs

**The gate:** a rule policing every raw colour literal.

**What it reported:** 80 violations, mostly legitimate scrims.

**Why the rule was correct and the output was still useless:** the rule's *intent* was "colours that
must adapt to the appearance setting must use an adaptive role". Scrims are legitimately absolute.
The single rule conflated two different defects that share one syntax.

**The fix, and why it worked:** two tiers by ownership — strict inside the design system (where a
raw literal means using a value instead of the token), duplication-only everywhere else (where a
repeated literal is the real defect, because it will drift). The finding count collapsed and the
true positives survived.

**The rule it justifies — Decision Tree 2's tiering:** strict inside the boundary that owns the
concept, duplication-only outside it.

**The counterfactual worth recording:** the same defect class, in its subtler form, was invisible to
the gate. A raw palette swatch (`Color.deeplyCharcoal`) compiles, renders correctly on a device set
to dark, and is unreadable in light mode. The literal-detection gate looked for hex literals and
hand-built colour constructors — not for a wrong-but-real token. So the rule was simultaneously too
broad (80 false positives) and too narrow (missing the real instance). That combination is a pattern
defect in both directions at once, and it was fixed by reading the vocabulary from the generated
token file so the check could not drift from what the compiler sees — and by **showing it fail on a
deliberately reintroduced violation** before trusting it.

---

## 6. The testability check with an exact name derivation

**The check:** it derived the expected test file name from the production file's stem, matching
`AuthViewModels.swift` to `AuthViewModelsTests`.

**The report:** `AuthViewModels.swift: view model has no test`.

**The reality:** the test file existed and was named `AuthViewModelTests.swift`. Singular versus
plural decided pass versus fail.

**Why it matters beyond the naming:** a false "untested" report looks *exactly* like a real one.
There is no way to tell from the output which it is; you have to read the checker. Every gate with a
derived expectation has this property, and the derivation rule is the thing to document, not just
the check.

**The rule it justifies — the derivation-rule discipline (Best Practice 1 and Failure Narrative 9 in
the source):** a gate's derived name, path, or threshold is exact, and it belongs in the check's
documented contract, not buried in the implementation.

---

## 7. The generator whose output was never consumed

**The situation:** a token generator had three backends. Two emitted named declarations. The third
emitted its last five blocks as raw JSON concatenated onto a TypeScript preamble — valid JSON,
invalid TypeScript.

**Why it survived three compounding reasons:**

| Reason | Why that is not an excuse |
|--------|--------------------------|
| The file was never committed | A generated artefact outside version control is invisible to review and to CI |
| Nothing imported it | So the type checker never parsed it — the one check that catches it in a second |
| That codegen target had never been run | A backend that has never executed is not "working", it is unexercised |

**The rule it justifies — Best Practice 6's sibling:** a generator is not tested by running it; it is
tested by its output being **consumed**. Writing a file proves nothing. `tsc`/`swiftc`/`kotlinc` over
the generated file proves the shape.

**The generalised rule:** if a generator writes into the repository, that file belongs in the
repository (or is gitignored on purpose). **Untracked-and-unused is the worst of both** — no review,
no type-check, and a surprise the first time somebody regenerates.

---

## 8. The drift check that was proven both ways

This one is the success case, recorded because it is the only one in the corpus where the discipline
was applied in advance.

**The check:** a `--check` mode that regenerates in memory, compares against the committed artefact,
and exits non-zero on any difference.

**What was proven before it was trusted:**

| Proof | Method | Result |
|-------|--------|--------|
| Idempotency | Two consecutive runs | No drift reported on either |
| Detection | `// deliberate drift` injected | Non-zero exit, confirmed |
| Restoration | Drift marker removed | Clean again |

**Why the idempotency proof is separate from the detection proof:** a drift check that always reports
drift is as useless as one that never fires. The first trains the team to ignore the output; the
second gives no coverage. Both are required, and they are different code paths.

**The rule it justifies — Best Practice 5:** give every freshness check an idempotency claim *and* a
detection claim. "Two runs agree" and "an injected change exits non-zero" are different assertions.

---

## Narratives condensed to rules

| Narrative | Rule |
|-----------|------|
| 1. Clean while compilers failed | R3 — anchor on final emitted identifiers |
| 2. 28 false positives on the first run | R6 — measure and triage before shipping severity |
| 3. Matched only the rarer spelling | R1 + probe method — write the probe the way the violation appears |
| 4. No legal spelling | R5 — contradiction matrix before the newer rule ships |
| 5. 80 legitimate findings | Decision Tree 2 — tier by ownership |
| 6. Exact derived name | Best Practice 1 — document the derivation contract |
| 7. Output never consumed | Best Practice 6 — a generator is tested by its output being consumed |
| 8. Drift proven both ways | Best Practice 5 — idempotency and detection are separate assertions |
