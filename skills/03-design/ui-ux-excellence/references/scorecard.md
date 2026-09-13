# Scorecard and Severity Model

<!-- STANDARD: 3min -- the scorecard template and severity model -->

## Two numbers, not one

A heuristic evaluation produces two things, and conflating them is the most common reporting
error:

- **Score (0–4):** how well the interface honours a heuristic.
- **Severity:** how much harm a specific finding does to a specific user.

A product can score well overall and still have a severity-1 defect that loses money. Conversely
a low score on "flexibility and efficiency" may be a deliberate trade with no user impact at all.
Report both; prioritise by severity, not by score.

## The scorecard

```markdown
## Heuristic Scorecard — <product> — <date> — <evaluator>

**Tasks evaluated:** 7   **Screens observed:** 23   **Baseline:** task success 62% [VERIFIED]
**Interface version:** <build/commit>   **Device/profile:** <device>, <network>

| # | Heuristic | Score | Blocking findings | Evidence rows |
|---|-----------|-------|-------------------|---------------|
| 1 | Visibility of system status | 2 | 3 | state-coverage.md |
| 2 | Match to the real world | 3 | 0 | |
| 3 | User control and freedom | 2 | 1 | |
| 4 | Consistency and standards | 3 | 0 | |
| 5 | Error prevention | 1 | 4 | |
| 6 | Recognition over recall | 2 | 2 | |
| 7 | Flexibility and efficiency | 3 | 0 | (trade recorded) |
| 8 | Aesthetic and minimalist design | 3 | 1 | |
| 9 | Error recognition and recovery | 1 | 5 | |
| 10 | Help and documentation | 3 | 0 | |
| **Mean** | | **2.3** | **16** | |

**Verdict:** below the ship bar (every heuristic ≥ 3). 16 blocking findings, 5 severity-1.
```

Record the interface version and the device profile. An evaluation without them cannot be
reproduced, and an irreproducible evaluation is an opinion.

## Severity model

Rate each finding on two axes, then read the class.

**Impact** — what the user loses:

| Impact | Meaning |
|---|---|
| 4 | Loses money, data, or access to a critical capability |
| 3 | Cannot complete the task |
| 2 | Completes the task with a workaround or delay |
| 1 | Notices friction; task completes normally |

**Frequency** — how many users hit it, and how often:

| Frequency | Meaning |
|---|---|
| 4 | Most users, most sessions |
| 3 | Most users, occasionally — or some users, often |
| 2 | Some users, occasionally |
| 1 | Rare path |

**Severity = Impact × Frequency**, mapped to four classes:

| Product | Class | Response |
|---|---|---|
| 12–16 | **S1 — Critical** | Fix before the next release; blocks the ship gate |
| 6–11 | **S2 — Major** | Fix in the next release cycle; scheduled with an owner |
| 3–5 | **S3 — Minor** | Backlog with a review date; may be batched |
| 1–2 | **S4 — Cosmetic** | Record; fix opportunistically or when touching the area |

## Applying the model

```text
Finding: "Error after failed save names the system, not the situation"
Impact    = 3  (the user cannot complete the task — they must retype or abandon)
Frequency = 3  (most users hit it whenever a session expires mid-task)
            ---
Severity  = 9  →  S2 — Major
```

```text
Finding: "Three equally-weighted actions compete at the primary task step"
Impact    = 2  (the task completes, with hesitation and misclicks)
Frequency = 4  (every user, every visit)
            ---
Severity  = 8  →  S2 — Major
```

```text
Finding: "No keyboard accelerator for the repeat-purchase flow"
Impact    = 1  (experienced users complete it, more slowly)
Frequency = 2  (a subset of users, sometimes)
            ---
Severity  = 2  →  S4 — Cosmetic (and possibly a recorded trade)
```

The three examples show why the axes matter: the aesthetic-adjacent finding (competing actions)
outranks what sounds like a mere convenience, because it affects everyone. Severity is about
reach and consequence, not about how sophisticated the defect sounds.

## Ship gate

A defensible ship bar, stated numerically so it is not re-negotiated per release:

```text
1. No S1 findings open.
2. Every heuristic scores >= 3, OR every score < 3 has a recorded, dated trade.
3. Every async screen has its required states (R2) — not a score, a gate.
4. Every error names the problem and offers a remedy.
5. Every proposed fix has a metric, an owner and a review date (R5).
```

Rule 3 and rule 4 are gates rather than scores deliberately: state coverage and error recoverability
are binary properties of *specific screens*, and averaging them away is how they ship broken.

## Trend, not snapshot

A single scorecard is a photograph. The useful artefact is the series:

| Release | Mean score | S1 | S2 | S3 | Task success | SUS |
|---|---|---|---|---|---|---|
| 2.4 | 2.1 | 7 | 12 | 9 | 58% | 61 |
| 2.5 | 2.3 | 5 | 11 | 8 | 62% | 64 |
| 2.6 | 2.6 | 2 | 9 | 7 | 68% | 69 |
| 2.7 | 3.0 | 0 | 6 | 5 | 74% | 74 |

The trend is what shows whether the practice works. A backlog that shrinks while the score rises
means the causes are being removed; a backlog that is merely re-prioritised each cycle means the
findings are being managed rather than fixed.

## Scorecard anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Scores with no evidence column | Not disputable, not fixable (R6) |
| Reporting the mean only | Hides the S1 finding that matters |
| Prioritising by ease instead of severity | Ships the wrong things; the S1 persists |
| Re-scoring without the version recorded | Comparisons are meaningless |
| Treating the score as the goal | The score is a proxy; task success is the outcome |
| No trend series | Improvement cannot be demonstrated, so the practice loses funding |
| Averaging state coverage into a score | States are per-screen gates, not an average |
