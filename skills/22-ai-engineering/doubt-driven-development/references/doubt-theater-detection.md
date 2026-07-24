# Doubt Theater Detection

## Taxonomy of Performative Doubt

Doubt theater is any doubt statement that satisfies the PROCESS of adversarial review
without providing the SUBSTANCE. It creates the appearance of rigor while contributing
zero defect-discovery value.

## The 15 Patterns of Doubt Theater

### Category 1: The Vacuum Statements

**DT-1: The Generic Edge Case**
"Have we considered edge cases?" — Names zero edge cases. No test condition.
**Reformulate:** "Claim would be wrong if input contains Unicode homoglyphs in the username
field. Example: 'admin' vs 'аdmin' (Cyrillic 'а'). Test: register both; verify they're distinct."

**DT-2: The Performance Ghost**
"What about performance at scale?" — No load estimate, no bottleneck hypothesis.
**Reformulate:** "Claim that this endpoint responds in <200ms would be wrong if the N+1 query
on line 47 executes 100 times under 100 concurrent users. Test: load test with 100 VUs."

**DT-3: The Security Blanket**
"Is this secure?" — No threat model, no attack vector, no OWASP category.
**Reformulate:** "Claim that user input is safe would be wrong if the sanitizer doesn't handle
double-encoded input. Test: send %253Cscript%253E (double-encoded <script>)."

### Category 2: The Authority Appeals

**DT-4: The Best Practice Appeal**
"This doesn't follow best practices." — No practice cited, no explanation of what breaks.
**Reformulate:** "Claim that this retry logic is safe would be wrong without exponential
backoff — rapid retries can cause thundering herd. Test: simulate 1000 concurrent failures."

**DT-5: The Documentation Dodge**
"This should be documented." — Documentation doesn't prevent defects; tests do.
**Reformulate:** "Claim that callers know about this side effect would be wrong if a caller
doesn't handle the exception. Test: grep for all call sites; verify exception handling."

**DT-6: The "Someone Should" Deferral**
"Someone should look at this later." — Vague ownership, no deadline.
**Reformulate:** "Claim that the timeout value is correct would be wrong if the downstream
service p95 latency is 3s and timeout is 2s. Test: query downstream latency metrics."

### Category 3: The Anxiety Projections

**DT-7: The Future Anxiety**
"What if requirements change?" — No scenario, no fragility assessment.
**Reformulate:** "Claim that this hardcoded threshold handles all cases would be wrong if the
business rule changes from 5 to 10 items. Test: change the constant; count affected lines."

**DT-8: The Scope Creep**
"While we're here, we should also..." — Unrelated concern, derails focus.
**Response:** "That's a separate claim. File it as a new doubt cycle after this one completes."

**DT-9: The Gut Feeling**
"I have a bad feeling about this." — No falsifiable condition.
**Reformulate:** "Identify the specific condition that would make your feeling true.
What test would convert 'bad feeling' into 'confirmed defect'?"

### Category 4: The Process Games

**DT-10: The Checkbox Doubt**
"Let me just raise one doubt so it looks like I reviewed this." — Low-effort performative doubt.
**Detection:** Doubt that takes < 30 seconds to formulate is almost always theater.

**DT-11: The Echo Doubt**
Repeating someone else's doubt in different words without adding new evidence.
**Detection:** Compare doubt text against prior doubts on same claim. > 80% semantic similarity = echo.

**DT-12: The Volume Play**
Raising 20 low-quality doubts to appear thorough — overwhelming the review with noise.
**Detection:** Doubt count per claim > 5 with no CRITICAL or HIGH severities = volume play.

### Category 5: The Metric Masks

**DT-13: The Coverage Citation**
"We have 95% test coverage so this is fine." — Coverage measures execution, not correctness.
**Reformulate:** "Claim that tests verify behavior would be wrong if coverage includes tests
without assertions. Test: grep for test functions with zero expect/assert calls."

**DT-14: The "Works on My Machine"**
"It passed locally." — Local success doesn't prove anything about production conditions.
**Reformulate:** "Claim that this behaves correctly in production would be wrong if the
production database has 1000x more rows than local. Test: run against production-scale data."

**DT-15: The Linter Defense**
"The linter didn't flag this so it's fine." — Linters catch syntax, not logic.
**Reformulate:** "Linters don't verify correctness. Claim would be wrong if [specific logic
condition]. Test: [specific behavior test]."

## Detection Heuristics (Mechanical)

```bash
# DT-1 through DT-3: Generic question patterns
grep -in "have we considered\|what about\|is this secure\|edge cases" doubt_log.md

# DT-4 through DT-6: Authority/deflection patterns
grep -in "best practice\|should be documented\|someone should" doubt_log.md

# DT-7 through DT-9: Anxiety patterns
grep -in "what if\|while we're here\|bad feeling\|I'm not sure" doubt_log.md

# DT-12: Volume play detection
# Count doubts per claim; flag claims with > 5 LOW-severity doubts and 0 CRITICAL

# DT-15: Linter defense
grep -in "linter\|eslint\|pylint\|rubocop" doubt_log.md
```

## Reformulation Protocol

When doubt theater is detected, do NOT shame the reviewer. Use this protocol:

```
FLAGGED: Doubt Theater — [DT-#] [Pattern Name]
Original: "[reviewer's original statement]"
Missing:  [✗ failure condition] [✗ concrete example] [✗ testable check]

Reformulation: "Claim [X] would be WRONG if [specific condition].
                Example: [concrete scenario].
                Test: [grep/curl/run command]."

Would you like to reformulate, or dismiss this doubt?
```

## Doubt Theater Metrics

Track these metrics over time to measure team improvement:
- **Theater Rate:** (doubts flagged as theater) / (total doubts raised) — target < 15%
- **Reformulation Rate:** (theater doubts successfully reformulated) / (theater doubts flagged) — target > 80%
- **Time-to-Substantive:** Average time from initial doubt statement to reformulation — target < 2 min
