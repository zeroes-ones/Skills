# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. Mid-flow abandonment

**Symptom:** analytics show a large drop at one step of a multi-step flow. Support hears "it kept
asking for things".
**Mechanism:** a step demands information the user does not have at that moment (a document, an
account number, a decision), or the flow hides how much remains. Both are preventable.
**Diagnosis:** instrument per-step completion and abandonment with the last step recorded. The
step with the drop is the finding.

**Fix:** show progress and total steps; move hard-information requests later; allow save-and-resume.
**Recurrence guard:** the step-completion funnel is instrumented, so a regression is visible in the
next cycle (measurement.md).

## 2. Blank screen, then content pops in

**Symptom:** the screen shows nothing for a second or more, then the content appears at once.
**Mechanism:** no loading state, so the region renders empty while fetching (R2, Decision Tree 2).
**Diagnosis:** throttle the network and load the screen.

**Fix:** a skeleton matching the final layout; keep the page chrome stable.
**Recurrence guard:** every async screen's loading state is part of the state enumeration gate.

## 3. "Unhelpful" errors in support tickets

**Symptom:** users contact support rather than recovering; tickets describe messages as confusing.
**Mechanism:** the message names the system's condition in the system's vocabulary and offers no
action (Heuristic 9).
**Diagnosis:** collect every error string and check the three obligations — name, remedy,
preservation.

**Fix:** rewrite in the user's terms, with the correct next action and an explicit preservation
statement.
**Recurrence guard:** new error strings are reviewed against the three obligations before merge.

## 4. The designer's-machine illusion

**Symptom:** the interface is comfortable in review and slow for users.
**Mechanism:** verification on a fast device with a warm cache and a good connection.
**Diagnosis:** re-run the review on a throttled representative device.

**Fix:** measure on the median device and network; apply the correct perceived-performance
technique for the measured band (R4).
**Recurrence guard:** the review protocol names the device and network profile.

## 5. Accidental irreversible action

**Symptom:** users delete or submit something they did not intend to.
**Mechanism:** the destructive control sits adjacent to a frequent one, with no separation,
confirmation or undo (Decision Tree 1).
**Diagnosis:** measure the distance and visual weight between destructive and routine controls in
the same region.

**Fix:** separate spatially; confirm naming the specific consequence; or offer undo.
**Recurrence guard:** destructive-action adjacency is a review item.

## 6. "Cluttered" with no cause identified

**Symptom:** the interface is repeatedly described as cluttered, and the description never
translates into a change.
**Mechanism:** an aesthetic finding with no evidence attached (R1).
**Diagnosis:** count the equally-weighted options competing at each step, and the information that
carries no task relevance at that step.

**Fix:** reduce the count; verify by re-counting and by task success against the baseline.
**Recurrence guard:** findings are accepted only with a count or a reproduction step.

## 7. Sluggish feel and double-taps

**Symptom:** users tap controls twice, or describe the product as slow despite fast operations.
**Mechanism:** a transition longer than the interaction it accompanies, or feedback that arrives
after the input rather than with it (R3).
**Diagnosis:** time each transition against the action it accompanies; inspect whether input is
accepted during the transition.

**Fix:** shorten to below the interaction; keep compositor-friendly properties; never block input
on a transition.
**Recurrence guard:** motion durations come from tokens and are reviewed against their
interactions.

## 8. Quality regression after a redesign

**Symptom:** a redesign ships and the experience is worse on the measures that mattered.
**Mechanism:** no baseline and no metric, so the redesign optimised against different implicit
criteria (R5).
**Diagnosis:** was the metric captured before the change? If not, the regression cannot be
attributed — capture it now and treat this window as the baseline.

**Fix:** capture the baseline before the change; name the metric and the owner.
**Recurrence guard:** a redesign requires a pre-change baseline as an entry condition.

## 9. Dead first-run experience

**Symptom:** new users see an empty or uninformative surface and do not activate.
**Mechanism:** the empty state was never designed as onboarding (R2, empty-states.md).
**Diagnosis:** create a new account and visit every surface.

**Fix:** name the concrete noun, describe the purpose, offer one primary action.
**Recurrence guard:** first-run states are part of the state gate.

## 10. Filtered-empty indistinguishable from empty

**Symptom:** users believe there is no data when a filter is hiding it.
**Mechanism:** one empty state serves both conditions.
**Diagnosis:** apply a filter that matches nothing and compare the message to the true-empty case.

**Fix:** echo the query, state the filter count, offer a clear action.
**Recurrence guard:** the empty-state taxonomy distinguishes the cases (state-coverage.md).

## 11. Form rejected at the end

**Symptom:** users complete a long form and are rejected; frustration is high.
**Mechanism:** validation only on submit (forms-and-feedback.md).
**Diagnosis:** leave a field with a format error — does anything happen before submit?

**Fix:** validate on blur; keep submit-time errors live-updating once shown.
**Recurrence guard:** validation timing is a review item per form.

## 12. Double submission

**Symptom:** duplicate records, duplicate charges, duplicate messages.
**Mechanism:** no in-flight state and no idempotency; the submit button was disabled as the only
protection, and a slow response let both taps through.
**Diagnosis:** throttle the network and tap the submit control twice.

**Fix:** an in-flight state that does not move the button, plus idempotency at the API.
**Recurrence guard:** every mutating submit has an in-flight state and an idempotency key.

## 13. Screen-reader users re-submit the same failing form

**Symptom:** a screen-reader user cannot tell why the form failed, so they submit again.
**Mechanism:** the error was shown visually (often by colour) and never announced, and not
associated with its field.
**Diagnosis:** complete the form with a screen reader after deliberately triggering an error.

**Fix:** associate the message with the field, mark the field invalid, and announce the error.
**Recurrence guard:** error association and announcement are part of the forms checklist.

## 14. The same findings every quarter

**Symptom:** the quality backlog is re-prioritised each cycle and never shrinks.
**Mechanism:** findings without metrics, owners or review dates (R5).
**Diagnosis:** compare the current finding list to the previous two cycles'.

**Fix:** every fix gets a metric, an owner and a review date; report a trend series.
**Recurrence guard:** the trend series is the artefact reviewed, not the snapshot.

## 15. "Feels slow" with healthy server metrics

**Symptom:** users report slowness; dashboards show fast responses.
**Mechanism:** the server is fast, but the *perceived* experience is not — no acknowledgement, no
skeleton, or the first paint is delayed behind data.
**Diagnosis:** measure time-to-first-meaningful-feedback, not just response duration.

**Fix:** acknowledge immediately; render structure before data; apply the technique for the band
(Decision Tree 4).
**Recurrence guard:** the perceived metric is tracked alongside the server metric.

## The triage rule

Four of these symptoms — blank-then-pop, unhelpful errors, dead first-run, and mid-flow
abandonment — account for most reported experience defects, and all four are detectable in
minutes: throttle the network, disconnect it, use the product as a new user, and walk the flow.
Run the state coverage pass and the error pass before any deeper diagnosis.
