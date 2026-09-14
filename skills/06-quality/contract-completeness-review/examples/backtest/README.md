# Backtest Example — contract-completeness-review

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below, anchored to the published defect record in
> `references/failure-narratives.md` where a **[$VERIFIED-scope]** tag is shown.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A cross-platform product shares one domain module between an iOS app and an Android app.
- The domain module declares the ports; each platform supplies an implementation.
- The team's existing verification is: two compilers, one UI suite per platform, five repository
  gates. No check derives an operation set from behaviour.
- Blended engineering + release rate: $160/hour, fully loaded.
- Model parameters reflect the stated inputs only; no external data feed.

| Parameter | Value | Tag |
|---|---|---|
| Shared ports in the domain module | 11 | [ESTIMATED] |
| Ports with two implementations | 9 | [ESTIMATED] |
| Platform source files touching those ports | 46 | [ESTIMATED] |
| Existing tests across both platforms | 214 | [VERIFIED-scope] — the defect record's count |
| Existing repository gates | 5 | [VERIFIED-scope] |
| Engineering + release rate | $160/h | [ESTIMATED] |
| Cost of one defect reaching a user | 900 h | [ESTIMATED] |
| Cost of one post-launch contract audit | 40 h | [ESTIMATED] |

## Computed scenario ([COMPUTED])

The question the review answers is not "do both platforms satisfy the ports" — every existing check
answers that, and it is green. It is **"can each port express every operation the system performs
on the state it describes?"**

Operation inventory, derived from call sites and persisted state rather than from the port text:

```
ports with a complete lifecycle (create+read+update+delete)      4
ports with read+delete only                          ← the shape 5
ports with read only                                             1
ports with no reachable member                                   1
                                                       total    11

expressibility diff: 5 ports cannot express their own create/update operation
```

Three designs, computed from the assumptions above:

| Run | Review performed | Defects shipped | Illustrative cost |
|-----|------------------|-----------------|-------------------|
| 1 | None — consistency only ("both compilers pass, 214 tests green") | 5 latent inexpressible operations; 1 reaches users | **$180,000** |
| 2 | Manual read of the 11 port declarations | 2 found by reading; 3 latent; 1 reaches users | **$90,000** |
| 3 | Operation inventory + writer audit + bypass grid + round trips | 5 found at review time; 0 reach users | **$6,400** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario values
are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]: one inexpressible **write** operation ships. The platform whose
implementation satisfies the port exactly never persists the value; its compiler is green and its
suite is green, because its fakes mirror the omission. Cost: 900 h of engineering and release at
$160/h = **$144,000**, plus 225 h of incident triage and stakeholder management = **$36,000**. Total
**$180,000**.

**Run 2 loss derivation** [COMPUTED]: a careful read of the port declarations finds the two ports
whose *names* disagree with their members — a `…Store` with no write is visible to a reader who is
looking for it. It does not find the three ports whose omission is invisible: the write happens
outside the port on one platform (a bypass, not a gap), the two authorities for one fact, and the
generated value with no consumer. One latent defect reaches users: 900 h × 0.5 (smaller blast
radius) × $160 = $72,000, plus 112 h triage = **$18,000**. Total **$90,000**.

**Run 3 loss derivation** [COMPUTED]: the review costs 40 h of a senior engineer across 11 ports
(inventory 6 h, operation set 8 h, writer audit 5 h, bypass grid 5 h, expressibility diff 6 h,
round-trip assertions 10 h) = 40 h × $160 = **$6,400**. Five findings, all fixed before release, at
an average of 1.5 h each — 7.5 h, i.e. **$1,200**, already inside the review budget. Nothing reaches
a user. Total **$6,400**.

## Best case

Run 3 — the operation set is derived from call sites and persisted state, the writer of each piece
of shared state is named along with the seam it uses, every operation × implementation cell is
marked *through the contract* or *bypass*, and the five inexpressible operations are found at review
time. Each fix ships with a round-trip assertion, and the assertion's removal check is run so the
team knows it can fail. Customer impact: $0 beyond the $6,400 review
([COMPUTED] from the table above).

## Worst case

Run 1 — the design most teams ship by default: two green compilers and a thorough suite, offered as
the completeness argument. Three compounding failures ([COMPUTED]):

- **The compilers cannot see it.** An incomplete contract is satisfied by every implementation. The
  build that "proves" the ports are correct is the same build that cannot detect the defect.
- **The suite cannot see it.** The fakes are derived from the ports, so they carry the same omission.
  214 green assertions confirm the world is consistent with a contract that cannot persist a value.
- **The gates cannot see it.** The testability gate asks whether behaviour is *tested*, not whether
  the contract is *complete*. It has no input that would distinguish the two.

The instructive part is that Run 1 looks like the *strongest* verification posture in the three
runs — more tests, more gates, two platforms building green. The failure appeared only at the
boundary the existing checks do not reach, which is the definition of a defect that requires a new
question rather than more care.

## Learnings / key takeaways

- **Lesson learned:** the difference between Run 1 and Run 3 is one question — *"who WRITES this?"* —
  asked of each piece of shared state. It was not found by any of the five gates, both compilers, or
  214 tests in the source record ([VERIFIED-scope]). Adding a sixth gate over the same inputs would
  not have found it either; the review had to ask something the checks do not ask.
- **Actionable lesson:** read the interface is the weakest of the three runs. Run 2 spent the same
  senior engineer's time on the declaration text, where an omission is visible only when the *name*
  contradicts the members — and found 2 of 5 ([COMPUTED]). Deriving the operation set from call
  sites costs 8 hours and found the other 3.
- **Actionable lesson:** the bypass map is what turns "platform A is fine" into a claim with a path
  attached. Run 1's Android failure was attributed to Android for a full session because iOS was
  green — and iOS was green because it never used the port for the write
  ([VERIFIED-scope]).
- **What this validated:** the skill's core workflow (inventory → operation set → writer audit →
  bypass map → expressibility diff → evidence fidelity → reachability → reverse direction →
  round-trip assertion → ledger) distinguished a $180,000 design from a $90,000 design from a $6,400
  design, and named the specific phase responsible for each difference — the writer audit and the
  bypass map, both of which take under six hours.

## What this does not show

- No real production system was measured. Port counts, file counts, and the rate are [ESTIMATED].
- The dollar figures are [COMPUTED] from those estimates, not historical accounting. The source
  project's defect record publishes the mechanism and the ratio, not per-defect costs.
- The skill's *output quality* on a real codebase is not assessed here. The meaningful test is a run
  against a live repository with a searchable call graph, where the agent either produces a complete
  operation inventory or correctly refuses and states what it could not search.
