# Related Reading

## Where this skill sits

```
codebase-design ─┐
api-designer ────┤
domain-modeling ─┼─→ contract-completeness-review ─┬─→ code-reviewer
mobile-arch ─────┤                                 ├─→ tdd-guide
verifier-design ─┘                                 ├─→ qa-engineer
                                                   ├─→ verification-before-completion
                                                   └─→ implementation-planner
```

This skill sits **between design and review**. Upstream, the contract is designed; downstream, a
change is reviewed against it. This skill answers the question neither side owns: can the contract
express the work at all?

## The boundary with `verifier-design`

The two skills are adjacent and are easy to confuse. The split:

| | `contract-completeness-review` | `verifier-design` |
|---|---|---|
| Question | Can this contract express every operation the system performs? | Does this check actually fire, and is it calibrated? |
| Finds | The missing operation, the bypass, the mirroring fake | The gate that reports clean while the build is broken, the validator that never rejects |
| Artefact | Operation inventory, bypass grid, round-trip assertion | Fire-case and silent-case tests, negative controls, calibration set |
| Escalation | Hand the defect class to `verifier-design` when no existing check can see it | Hand the contract finding here when the check is sound and the contract is not |

The handoff in practice: this skill finds a defect class, notes in the ledger that it was found by
asking rather than by a tool, and states that no existing check can see it. `verifier-design` then
answers the next question — what would a check that sees this look like, and has it been proven to
fire?

## The boundary with `code-reviewer`

`code-reviewer` reviews a change. This skill reviews a contract. They meet when a change adds a
member to a shared interface:

1. This skill establishes that the operation set is complete, so the reviewer knows what the diff is
   supposed to accomplish.
2. `code-reviewer` reviews the implementing diff for its own defects — error handling, performance,
   security, test coverage.

Reviewing a diff against an incomplete contract is how a correct implementation of the wrong
contract ships.

## The boundary with `qa-engineer` and `tdd-guide`

Both work downstream of the operation inventory:

| Skill | What it needs from here |
|---|---|
| `qa-engineer` | The bypass map, so coverage is placed where the seam is actually exercised rather than where the interface claims it is |
| `tdd-guide` | The required operation set, so tests are written from behaviour rather than from the interface's member list |

The round-trip assertion is the shared artefact: this skill specifies which operation it must
depend on, `tdd-guide` writes it, `qa-engineer` places it where every implementation runs it.

## The boundary with `codebase-design`

`codebase-design` decides where a seam goes and how deep an interface should be. A shallow module —
large interface, little behaviour — is the design failure that produces contract-completeness
defects, because a shallow interface is one that cannot express the operations the behaviour needs.
Read `codebase-design` for the decision; use this skill to verify the decision held.

## Reading order

| If you are… | Read |
|---|---|
| New to this skill | This file, then `completeness-vs-consistency.md`, then `writer-reader-audit.md` |
| Auditing a live contract | `writer-reader-audit.md` (phase 3), `bypass-detection.md` (phase 4), then the recipes |
| Fixing a specific finding | `round-trip-assertions.md`, then `mirroring-fakes.md` |
| Building the mechanical check | `discovery-ledger.md`, then hand the class to `verifier-design` |
| Deciding whether the exemption is legitimate | Decision Tree 4 in the skill, then `completeness-vs-consistency.md` |

## The one-sentence version

Completeness asks whether a contract can say the thing the system must do; consistency asks whether
its implementations say it the same way — and every check a team usually has answers only the second.
