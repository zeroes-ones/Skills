# Backtest Example — document-specialist

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario is a fixed, hypothetical quarterly board-pack production run for a mid-size company.
- Document volume, review cycles, and rates are illustrative inputs, not measured from an
  organisation.
- Outputs are scenario illustrations validating the document-production workflow, not observed
  outcomes.

| Parameter | Value | Tag |
|---|---|---|
| Documents produced per quarter | 12 | [ESTIMATED] |
| Analyst hours per document (manual build) | 6 h | [ESTIMATED] |
| Analyst cost per hour | $110 | [ESTIMATED] |
| Rework hours after a corrupt-on-edit file | 4 h | [ESTIMATED] |
| Rework hours after an unverified PDF conversion | 3 h | [ESTIMATED] |
| Probability of a silent truncation per manual transform | 15% | [ESTIMATED] |
| Cost of one external re-send after a bad artifact | $4,000 | [ESTIMATED] |

## Computed scenario ([COMPUTED])

**Without this skill — hand-built markup, no verify loop.**

- Manual build: 12 × 6 h × $110 = **$7,920** per quarter
- Corrupt-on-edit rework (2 documents in 12): 2 × 4 h × $110 = **$880**
- Unverified conversion rework (3 in 12): 3 × 3 h × $110 = **$990**
- Expected silent-truncation incidents: 12 × 15% = 1.8 → one external re-send = **$4,000**
- Quarterly total: **$13,790**; annualised: **$55,160**

**With this skill — native libraries, template, verify loop, inspected conversions.**

- Templated build: 12 × 2 h × $110 = **$2,640** (appearance lives in the template; code supplies
  content only)
- Corrupt-on-edit: 0 — the format's native library keeps the structure valid
- Conversion rework: 0 — every conversion is inspected (Ground Rule R3) before shipping
- Silent truncation: caught by the count-reconciliation check (Ground Rule R4), so no external
  re-send
- Quarterly total: **$2,640**; annualised: **$10,560**

**Delta:** **$44,600 per year** avoided on 12 documents per quarter.

Cost of the verification itself: the reopen-and-assert loop runs in under a second per document
(`references/verification-recipes.md`), so the check is effectively free against the $4,000
incident it prevents.

## Best case

The first quarter establishes a template and a reusable verify snippet. From then on, appearance
changes once (in the template) and every document inherits it; the code never touches styling
again. Silent truncation becomes structurally impossible rather than merely unlikely, because
reconciliation is in the script rather than in a reviewer's attention.

## Worst case

The workbook is delivered as a static snapshot when the consumer needed it to recalculate —
formulas-versus-values was never confirmed (Ground Rule R5). The file looks correct, opens
correctly, and is quietly wrong for every subsequent reader, because a value was frozen where a
formula belonged. The failure is invisible until someone edits an input and nothing moves. The
mitigation is the explicit confirmation in Phase 1: ask which the consumer needs before writing
either.

## Learnings / key takeaways

1. The largest single saving is not time — it is the avoided external re-send. A silently
   truncated or wrong-font artifact is a trust event, not just a rework event.
2. Hand-building markup is a false economy: it appears to work, then corrupts on the first edit,
   and the discoverer is usually the consumer rather than the author.
3. Templating is what makes the recurring cost collapse: appearance changes in one place, and code
   stops being responsible for styling.
4. Verification must live **in the script**. A check that depends on a human remembering to look
   is a check that fails exactly when someone is busy.

## What this does not show

- No real document corpus, review cycle, or incident history underlies these rates; they are
  stated assumptions for arithmetic, not benchmarks.
- The 15% truncation probability and the $4,000 re-send cost are illustrative; a team with a
  mature template pipeline and mandatory review would see a much smaller delta.
- This skill does not produce the visual design of a deck, the prose of a long document, or the
  metric definitions behind the numbers — those route to `presentation-designer`,
  `technical-writer`, and `business-intelligence-engineer` respectively.
