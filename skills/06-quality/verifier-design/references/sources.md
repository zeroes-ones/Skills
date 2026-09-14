# Sources — provenance for the claims in this skill

> Every claim in SKILL.md and these reference files traces to a source below, tagged by strength.
> The mechanisms (fire cases, negative controls, contradiction matrices, severity tiering) are
> established engineering practice. The specific defect counts and narratives are `[VERIFIED]`
> against one production repository's own records, and are cited as that repository's observations —
> they are evidence for the pattern, not a measurement of your codebase.

---

## Sources

| Claim | Source | Strength |
|-------|--------|----------|
| 8 defects found by compilers, 2 by decoding real data, 1 by reading (of 22) | `Deeply-Health/docs/native-learnings.md`, Part 2 header and Part 4 | **[VERIFIED]** — the repository's own defect ledger, with a "found by" column per defect |
| The second batch (entry-flow defects 23–44) was found entirely by compilers, tests, and gates; none by reading | `native-learnings.md`, Part 2b header | **[VERIFIED]** — same ledger, stated explicitly |
| A stability gate reported clean while two compilers failed, because it compared pre-transform names on both sides | `native-learnings.md`, defect 22 | **[VERIFIED]** — recorded with the root cause |
| The same gate's first run produced 28 false positives, all caused by a whitelist omitting `Record` | `native-learnings.md`, defect 22 | **[VERIFIED]** |
| A rule set had no legal spelling: `ios/DeeplyDomain` + `internal` failed a rule requiring explicitness *and* a rule banning redundancy | `docs/deeply-health-mining.md`, F12 | **[VERIFIED]** — stated with the encoded invariant |
| A design gate reported 80 violations, mostly legitimate scrims, and was fixed by two tiers rather than one rule | `docs/deeply-health-mining.md`, F12 | **[VERIFIED]** |
| A rule requiring the rarer spelling (`slideInHorizontally(`) missed Kotlin's more idiomatic trailing-lambda form; found by writing a probe | `native-learnings.md`, rule 52 | **[VERIFIED]** |
| A configured plist key never reached the built bundle; `INFOPLIST_KEY_<custom>` injects only keys the toolchain knows | `native-learnings.md`, defect 16 | **[VERIFIED]** |
| A localisation directory was declared but never a target source, so translations shipped nowhere and the app rendered raw keys with no warning | `native-learnings.md`, defect 11 | **[VERIFIED]** |
| Entitlements were correct in file and setting while the signature carried an empty dict; the simulator does not enforce entitlements | `native-learnings.md`, defect 39 / rule 26 | **[VERIFIED]** |
| A merged manifest is cached, and reported the old package name until the intermediates directory was cleared | `native-learnings.md`, defect 38 / rule 23 | **[VERIFIED]** |
| An installed APK predated the source edits; the discriminator was a resource count (24 shipped vs 25 in source) | `native-learnings.md`, rule 43 | **[VERIFIED]** |
| A generator emitted unparseable TypeScript that survived because it was untracked, imported by nothing, and its codegen target had never run | `native-learnings.md`, defect 33 | **[VERIFIED]** |
| A testability check derived the expected test file name from the production file's stem, so singular vs plural decided pass/fail | `native-learnings.md`, rule 14 | **[VERIFIED]** |
| A `--check` gate was verified both idempotent and detecting, by injecting `// deliberate drift` and confirming a non-zero exit | `native-learnings.md`, Part 4 "Why rung 4 must be proven to fire" | **[VERIFIED]** |
| A compiler run must be preceded by a negative control when the result is "0 errors" | `native-learnings.md`, Part 4 | **[VERIFIED]** |
| A spec-gap checker's reverse direction was a deliberate no-op, and the spec silently fell to 41 documented paths while the API served 114 | `native-learnings.md`, defect 1; `docs/deeply-health-mining.md`, F11 | **[VERIFIED]** |
| A `SessionStore` port declared `hasSession` and `clear` but no `save`; 214 tests agreed with the bug because the fakes mirrored the omission | `native-learnings.md`, defect 44 / rules 35–37 | **[VERIFIED]** |
| The verification ladder is written → compiles → decodes real data → `--check` in CI, and a hand-written fixture encodes the same assumptions as the generator | `native-learnings.md`, Part 4 | **[VERIFIED]** — the ladder and its stated rationale |
| Warnings from an existing gate became build failures within the same session | `native-learnings.md`, "The pattern behind 23, 24 and 25-26" | **[VERIFIED]** |
| A coverage percentage can be satisfied by assertion-free tests; a named test for a named behaviour cannot | `docs/deeply-health-mining.md`, F9 | **[VERIFIED]** — stated as the checker's own rationale |
| A flaky test's fix is an explicit precondition, not a retry | `native-learnings.md`, rule 48 | **[VERIFIED]** |
| The dollar ranges quoted in SKILL.md's Gotchas and Error Decoder | Synthesised from the defect narratives above, scaled by typical remediation cost for the described class | **[ESTIMATED]** — order-of-magnitude, never to be quoted as measured |
| The remediation multipliers behind the Gotchas table (`escaped class` ≈ 4–10× the cost of catching it at gate time) | General engineering-economics reasoning, not a specific study | **[ESTIMATED]** |
| The specific linter, analyzer, and CI-provider syntax in the recipes | General practice; vendor syntax changes between versions | **Must be confirmed against the installed version** — see Anti-Hallucination in SKILL.md |

---

## Why the source is cited this way

The narratives come from **one** production repository's own defect ledger. That makes them strong
evidence *for the mechanism* — the gate compared pre-transform names and therefore validated a
mismatch as agreement is a mechanical fact about that code, not an opinion — and weak evidence about
*frequency* in any other codebase.

The defect counts are therefore quoted as that repository observed them, and the ratios are used as a
**budget argument** (where to spend) rather than as a prediction (what you will find). A different
codebase will produce a different ratio; the method for measuring its own is the eight recipes in
`verification-recipes.md`, and the ledger format in `failure-narratives.md` is the artefact that
makes the ratio computable.

---

## Explicitly not claimed

* That mechanical checks can replace review. Five classes of defect in the source corpus were
  unreachable by any gate (see `discovery-ratio.md`), and all five live in seams between two
  individually-correct things.
* That a specific false-positive rate is "acceptable". The threshold is a function of the team's
  triage capacity and the cost of the escape, not of the rule.
* That a gate proven to fire is a correct gate. Firing proves wiring and coverage of the probe's
  spelling; correctness of the rule is a separate assertion, answered by the silent case and by
  calibration.
* That any listed technique is tool-specific. Every recipe is expressed as an observable
  (input → exit code → finding text) so it transfers across languages, CI systems, and linters.
