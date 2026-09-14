# Additional Resources — index and worked walkthrough

> The index to this skill's reference files, plus one end-to-end walkthrough of designing a check
> from scratch. Read SKILL.md first; come here when you need the reasoning behind a rule.

---

## Reference file map

| File | Owns | Rule it serves |
|------|------|----------------|
| `proving-a-check-fires.md` | Fire cases, silent cases, the probe method, why a clean run is low-information | R1, R2 |
| `negative-controls.md` | The three negative controls, the control matrix, controls for probabilistic checks | R2 |
| `joint-rule-contradiction.md` | The scope × modifier matrix, the legal-spelling invariant, bidirectional consistency | R5 |
| `severity-calibration.md` | Measuring true and false positives, tiering by ownership, the ignored-gate arithmetic | R6 |
| `allowlists-with-reasons.md` | The property-versus-circumstance test, entry shape, the allowlist as a set | R4 |
| `discovery-ratio.md` | The found-by evidence, instrument cost/coverage portfolio, classes no gate reaches | Best Practice 1, 10 |
| `artefact-versus-configuration.md` | Declared-but-absent, stale-versus-wrong, the commands that read shipped output | R7 |
| `failure-narratives.md` | Eight real gate failures, each ending in the rule it justifies | All |
| `verification-recipes.md` | The eight checks as runnable procedures, plus a gate specification template | All |
| `sources.md` | Provenance for every claim, tagged by strength | Anti-Hallucination |
| `related-reading.md` | Where this skill plugs into the library, and the four verification skills compared | Routing |

---

## Walkthrough: designing a check end to end

A concrete run through the workflow, using a plausible scenario so the shape of the output is
visible.

### The situation

A team has an API specification generated from a running backend, and code generated from that
specification. Twice this quarter, the specification and the running service disagreed and nothing
failed.

### Phase 1 — Name the class (15 min)

> **The defect class:** a route served by the API that the specification does not document, or a
> route documented that the API does not serve.

Note the two halves and that they are different checks. This is the point where most designs stop
half-done.

### Phase 2 — Locate the signal (20 min)

The specification is a generated artefact; the running API is a live surface. Neither is source, so
the check must compare **two artefacts**:

```
spec paths   ← enumerate from the generated specification file
served paths ← enumerate from the running service's own route table (or OpenAPI output)
```

Locating the second enumeration is the hard half, and it is the half that decays into a no-op
(see `joint-rule-contradiction.md`: this exact check's reverse direction was written as
`if not fuzzy_found: pass  # Don't fail on extras`, and the specification fell to 41 documented
paths while the API served 114).

### Phase 3 — Fire case (30 min)

Inject a divergence in the direction you can construct quickly:

```
1. Add a route to the running service that the specification does not document
2. Run the check
3. OBSERVE: non-zero exit, finding names the undocumented path
4. Keep the served-only route in a fixture, or generate and remove it in the same script
```

Then do the same for the other direction:

```
1. Add a documented path that no route serves
2. Run the check
3. OBSERVE: non-zero exit
```

Two fire cases, because there are two checks wearing one name. A single fire case for this class
proves half of it.

### Phase 4 — Silent case (20 min)

```
1. A route with a deprecated alias — legitimate, must not be flagged
2. A path parameter spelling difference (`{id}` vs `{uuid}`) — decide and encode the tolerance
3. A health/readiness endpoint excluded by design
4. Empty spec, empty route table — must report a scope error, not a clean result
```

Item 4 is the scope negative control in disguise: an empty input must be *visible* as empty.

### Phase 5 — Negative control (15 min)

```
- Point the spec path at a nonexistent file → the check must error, not report clean
- Point the route enumeration at an unreachable service → the check must error
```

Both directions, because either enumeration being empty makes the comparison trivially true.

### Phase 6 — Anchor (20 min)

```
❌ spec.path_string        ==  route.decorator_argument
✅ normalized_path(spec)   ==  normalized_path(served_route)
```

The normalization is where the bug hides. If the check normalizes both sides with the *same*
function, it cannot detect a normalization defect — that is R3, and it is exactly how the stability
gate validated a mismatch as agreement. The mitigation is a fire case built with a path that is
correct before normalization and wrong after.

### Phase 7 — Contradiction matrix (30 min)

```
Dimensions: DIRECTION {documented-only, served-only} × PARAM_STYLE {{id}, {uuid}, :id}
            × METHOD {GET, POST, PUT, DELETE, PATCH}

Fill each cell with the spelling the check must accept.
Every empty cell = a case the check will reject for a legitimate reason.
```

### Phase 8 — Calibrate (30 min)

```
Run on the current tree.
  findings: N
  triage each: real divergence, or a legitimate spelling the check does not yet tolerate?
  precision: T / N
```

If the first run flags 40 deprecated aliases, the check ships as advisory until the alias tolerance
is added — not as blocking with 40 exemptions.

### Phase 9 — Allowlists (20 min)

```
[health endpoints]
reason  = Liveness and readiness probes are infrastructure; they are
          deliberately undocumented in the public specification.
bound   = If a probe becomes publicly routable, this exemption is wrong.
```

### Phase 10 — Wire and prove (25 min)

Re-run both fire cases through the real pipeline. Confirm the exit code propagates. Check the path
filter does not skip the check when only the service file changes — a `changed-files` condition is
the most common reason a check runs and does nothing.

### Phase 11 — Record (10 min)

```
CHECK            spec-api-parity
DEFECT CLASS     a served route not documented, or a documented route not served
ESCAPED INSTANCE Q3: 41 documented paths against 114 served, undetected for a quarter
READS            generated spec artefact + running service route table
FIRE CASES       (a) served-only route → exit 1  (b) documented-only path → exit 1
SILENT CASES     deprecated alias; tolerated param spelling; health endpoints; empty input
NEGATIVE CONTROL spec path pointed at a missing file → error, not clean
ANCHOR           normalized_path applied per side, with a normalization-defect fire case
CONTRADICTIONS   matrix in docs/gates/spec-parity-matrix.md
FINDINGS         0 real, 0 spurious (corpus is currently consistent)
SEVERITY         blocking, both directions
EXEMPTIONS       health endpoints — infrastructure probes, undocumented by design
DOES NOT CATCH   semantic differences (a route that exists but returns the wrong shape);
                 authorization requirements; whether the documented description is accurate
WIRED AT         ci/parity job, fire case re-proved 2026-09-14
```

---

## The three sentences to remember

1. **A check that has never failed is an untested check.** The fire case is not a test of the check; it is the definition of the check existing.
2. **A check that shares an assumption with the code it validates cannot catch a bug in that assumption.** Anchor on final emitted identifiers, always.
3. **An ignored gate is worse than no gate, because it manufactures confidence.** Severity is chosen from measurement, or the rule should not ship.

---

## Cross-domain transfer note

Every technique in this skill is stated as an observable — an input, an exit code, a finding text —
rather than as a tool invocation. The mechanisms (fire case, silent case, negative control,
contradiction matrix, severity tiering) are independent of language, linter, and CI provider. Only
the invocation syntax changes, and that syntax must be confirmed against the installed version
rather than recalled — see Anti-Hallucination in SKILL.md.
