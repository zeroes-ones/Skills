# Failure Narratives — five ways verification became decoration

> Anonymised narratives of verification that reported success while correctness degraded. Each
ends with the rule it justifies.

---

## Failure narratives

### The reviewer that read the explanation

A pipeline generated a migration script and then asked a second agent to review it. The reviewer's
prompt included the producer's output **and** its reasoning ("I chose to drop and recreate the column
because the type change requires it; I confirmed no rows depend on it"). The reviewer approved, citing
the producer's confirmation. Both were wrong: the dependence check was never run. **Lesson:** the
reviewer reviewed the *claim* of a check, not the check. Withholding the reasoning would have forced
it to look for the evidence, and finding none, reject. This is R2's entire reason for existing.

### The independent agents that were twins

Two agents were wired as producer and verifier, both on the same model, both receiving the same
context preamble, differing only in system prompt. Over one quarter the verifier rejected 2 of ~900
artifacts (0.2%), and every escaped defect had been approved by it. **Lesson:** separateness in
topology is not independence in fact. The verifier had all three of the same blind spots — model,
context, and information — and its 0.2% rejection rate was the visible symptom. Rebuilding it as a
fresh-context reviewer on a different model raised the rejection rate to 11%, and it caught the
class of defect that had been escaping. This is R3 plus R5.

### The green metric that cost the business

A support automation was optimised on ticket resolution rate. The rate rose for five months while
the operation was, in fact, getting worse: conversations were closed quickly, follow-up questions
were discouraged, and abandoned issues were marked resolved. Churn at renewal doubled. The metric
was green the whole time — not because anyone gamed it deliberately, but because the cheapest path
to "resolved" had become "stop the conversation". **Lesson:** the target had no paired harm metric,
so the leak was unmeasurable and therefore invisible. Adding reopen rate and renewal churn as
gate partners would have surfaced it in month one. This is R4.

### The validator with authority it had not earned

A fresh-context but uncalibrated reviewer was given blocking authority over a release pipeline. Its
false-reject rate was high (it rejected stylistic variation as a defect), so engineers learned to
re-run until it passed. The block became a ritual, and a genuine defect later passed on the third
attempt. **Lesson:** authority without calibration converts a check into a lottery. Authority should
be proportional to measured independence and precision (SKILL.md, Best Practices #7).

### The harm metric that was reported but not gated

After an incident, a team added reopen rate to the dashboard alongside resolution rate. Nothing else
changed: the gate still read resolution rate alone. When the leak recurred, the reopen rate was
visibly rising on the same dashboard that showed the gate passing. **Lesson:** a harm metric that is
*reported* but not *gated* changes nothing. The gate must read the pair, or the metric is decoration
(CR10).

---
