# Cross-Model Escalation

## When to Escalate

Cross-model escalation sends a doubt to a DIFFERENT model than the one that generated or
reviewed the code. This exploits the fact that different models have different training data,
different reasoning patterns, and different blind spots.

## Mandatory Escalation Triggers

| Trigger | Rule |
|---|---|
| Same model generated AND reviewed the code | Must escalate to different model |
| CRITICAL severity doubt reaches cycle 3 | Must escalate to different model |
| Security claim with no prior security-reviewer pass | Must escalate; prefer Claude for security reasoning |
| LLM-output handling code | Must escalate to a model different from the one generating the output |
| Regulatory compliance claim (FDA, HIPAA, SOC2) | Must escalate; prefer Claude Opus for structured reasoning |

## Model Pairing Guide

| Primary Model | Escalate To | Best For | Weakness of Pair |
|---|---|---|---|
| Claude (generation) | GPT-4o (review) | Code correctness, logic errors, edge cases | Neither catches all concurrency bugs |
| GPT-4o (generation) | Claude (review) | Security, data integrity, architectural reasoning | Claude may miss generation-specific prompt tricks |
| Claude Opus | GPT-4o | Breadth: Claude finds depth issues, GPT-4o finds width issues | Different failure modes on async patterns |
| Gemini | Claude | Gemini generates creative attacks; Claude verifies rigorously | Gemini hallucination rate higher on code review |
| Any model | Claude Opus | Architectural claims, invariant reasoning, regulatory compliance | Opus slower and more expensive; use only for CRITICAL |

## Escalation Protocol

### Step 1: Prepare the Escalation Brief
```markdown
## ESCALATION-[claim_id]

**Claim under review:** [CLAIM-ID]: [one-sentence assertion]
**Code context:** [file:line range, surrounding 50 lines]
**Doubt history:** [cycles 1-3 summary: what was tested, what held, what failed]
**Specific question for escalated model:**
  "Review this code for [specific failure mode]. In particular, check whether
   [condition] could occur under [scenario]. If yes, what is the blast radius?"
**Primary model's finding:** [what the first model concluded]
**Blind spot hypothesis:** [why the primary model might have missed something]
```

### Step 2: Run the Escalated Review
Send the brief to the escalated model with explicit instruction:
"You are a second reviewer with DIFFERENT training data. Your job is to find what
the first reviewer missed. Assume the first reviewer may have confirmation bias."

### Step 3: Diff the Findings
```
Primary model (Claude) findings:     Escalated model (GPT-4o) findings:
  - CLAIM-001: HOLDS                   - CLAIM-001: HOLDS (agreement)
  - CLAIM-002: FAILS (no try/catch)    - CLAIM-002: FAILS (agreement)
  - CLAIM-003: HOLDS                   - CLAIM-003: FAILS — GPT-4o found that
                                         the environment variable fallback
                                         enables debug mode in production
                                       ← UNIQUE FINDING: missed by Claude
```

### Step 4: Reconcile Disagreement
If models disagree on a claim:
1. Both models produce a test that would prove their position
2. Run both tests against the actual code
3. The test that passes determines which model was correct
4. Document the disagreement in RECONCILE.md as a model blind spot

## Cost Model

| Escalation Type | API Cost (approx.) | Engineer Time | Total |
|---|---|---|---|
| Claude → GPT-4o (200 lines) | $2-5 | 10 min | ~$27-30 |
| GPT-4o → Claude (200 lines) | $3-8 | 10 min | ~$28-33 |
| Claude Opus deep review (500 lines) | $15-25 | 20 min | ~$65-75 |
| Full cross-model cycle (3 claims) | $10-25 | 30 min | ~$85-100 |

**ROI threshold:** Escalate if (probability of missed defect × cost of that defect) > $100.
For CRITICAL claims where defect cost > $50K, escalation is always justified.

## Blind Spot Coverage Matrix

| Defect Category | Claude Alone | GPT-4o Alone | Cross-Model |
|---|---|---|---|
| Logic errors | 85% | 80% | 95% |
| Concurrency bugs | 60% | 55% | 75% |
| Security (injection) | 75% | 70% | 90% |
| Security (auth bypass) | 80% | 75% | 92% |
| Data integrity | 78% | 72% | 88% |
| Error handling gaps | 70% | 68% | 82% |
| Performance anti-patterns | 65% | 60% | 78% |
| API contract violations | 82% | 78% | 90% |

Cross-model review improves detection by 10-18 percentage points across all categories.
The largest gains are in concurrency and performance — areas where single-model reasoning
is most vulnerable to blind spots.
