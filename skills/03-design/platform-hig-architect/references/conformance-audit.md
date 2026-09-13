# Conformance Audit

<!-- STANDARD: 3min -- how to audit a surface against its platform guidelines -->

> **Verification note.** An audit scores against a *version* of a platform's guidance. Record the
> version and the date, because guidance changes and an unscored audit cannot be re-verified.

## What this audit is, and is not

It audits **platform-convention conformance**: does the app honour the platform's learned
expectations, form-factor conventions, input models and accessibility contract?

It is *not* a WCAG audit (`accessibility-auditor`), a heuristic/craft evaluation
(`ui-ux-excellence`), or a deep review of one platform's design language
(`apple-hig-expert`, `material-design-expert`).

## Scoring

Score each dimension 0–4. A dimension scoring below 3 is a blocking finding.

| Score | Meaning |
|---|---|
| 0 | Convention violated with no record |
| 1 | Convention violated, recorded as a deviation without justification |
| 2 | Partly honoured; some screens correct, others not |
| 3 | Convention honoured everywhere, deviations recorded and justified |
| 4 | Convention honoured and the platform's newer/forward guidance considered |

## The dimensions

| # | Dimension | What to check |
|---|---|---|
| 1 | Navigation | Model matches the platform; back affordance correct everywhere; depth within budget |
| 2 | Form factor | Each size class designed; multitasking survives; no stretched layouts |
| 3 | Input | Every supported modality completes the primary task; focus model defined |
| 4 | Gestures | Vocabulary matches the platform; non-gesture alternatives exist |
| 5 | Controls | Platform control behaviour preserved; system affordances used |
| 6 | Feedback | Platform-appropriate progress, haptics, notifications, error presentation |
| 7 | Typography | System text styles or reproduced scaling; resize honoured at the maximum |
| 8 | Motion | Platform-appropriate timing; reduced-motion honoured |
| 9 | System integration | Permissions, share, deep links, widgets behave as the platform expects |
| 10 | Accessibility | Platform accessibility tree populated; labels, roles, order, state |
| 11 | Deviation hygiene | Every deviation recorded with what, why and cost |

## Procedure

1. **Inventory the surfaces.** One audit per surface, because conventions differ (R2).
2. **Record the platform version** being audited against, and the date.
3. **Score each dimension** from the evidence below — not from intent.
4. **Collect evidence per dimension.** Screenshots, recordings, and the platform's own inspector
   are evidence; the design file is not.
5. **Report blocking findings first**, then deviations, then improvements.
6. **Feed findings back into the convention matrix** — a finding is usually a cell the product
   resolved wrongly.

## Evidence per dimension

| Dimension | Evidence |
|---|---|
| Navigation | A recording of back behaviour from 3+ depths; peer/detail structure diagram |
| Form factor | Screenshots at each size class and at the smallest split view |
| Input | A recording of the primary task completed by keyboard, pointer, remote or gaze |
| Gestures | A demonstration of each gesture and its non-gesture alternative |
| Controls | A comparison of the app's controls to the platform's own |
| Feedback | Recordings of progress, error, empty and notification states |
| Typography | Screenshots at default and maximum text size |
| Motion | A recording of transitions with reduced-motion enabled and disabled |
| System integration | Triggering permissions, share, deep links, widgets |
| Accessibility | The platform inspector's tree, plus a screen-reader walkthrough |
| Deviation hygiene | The deviation log, checked against the UI |

## Report format

```markdown
## Audit: <surface> — <platform> <version> — <date>

**Surfaces audited:** <list, one per form factor>
**Platform version:** <version> (guidance revision <if known>)
**Verdict:** PASS / PASS WITH DEVIATIONS / BLOCKED

### Blocking findings (score < 3)
| # | Dimension | Score | Finding | Evidence | Required action |
|---|---|---|---|---|---|

### Recorded deviations (score 2-3)
| # | Dimension | Deviation | Rationale | Cost to users | Preserved behaviour |
|---|---|---|---|---|---|

### Improvements (score 3 → 4)
| # | Dimension | Current | Platform-forward alternative |
|---|---|---|---|

### Matrix cells to revisit
| Category | Surface | Current decision | Corrected decision |
|---|---|---|---|
```

## The blocking findings, ranked by frequency

| Finding | Dimension | Why it blocks |
|---|---|---|
| Back affordance wrong on some screens | Navigation | Traps users; it is the most-learned convention there is |
| Tablet layout breaks in split view | Form factor | Multitasking is a platform feature, not an edge case |
| Focus invisible or order undefined | Input | Non-touch users cannot operate the app |
| Gesture-only function with no alternative | Gestures | Conformance failure (WCAG 2.5.1) and an excluded user group |
| Text ignores the platform size setting | Typography | Fails the user's platform-level preference |
| Accessibility tree unpopulated | Accessibility | Screen-reader users get an unusable app |
| Permission or share reimplemented | Controls | Loses system behaviour and usually fails review |
| Unrecorded deviation | Deviation hygiene | Indistinguishable from a defect; unverifiable later |

## Reviewer's audit checklist

- [ ] One audit per surface, platform version recorded
- [ ] Every dimension scored from evidence, not intent
- [ ] Blocking findings (score < 3) reported first with required action
- [ ] Deviations listed with rationale and cost
- [ ] Accessibility verified with the platform's own inspector and screen reader
- [ ] Text resize verified at the platform's maximum
- [ ] Input verified without touch
- [ ] Matrix cells corrected where a finding exposes a wrong convention decision
- [ ] Audit re-runnable: version, date and evidence all recorded
