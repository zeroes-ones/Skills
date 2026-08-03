---
name: critical-thinker
description: "Use when you must evaluate claims, arguments, and evidence rapidly and reliably. Handles argument mapping, fallacy detection, Socratic questioning, steel-manning, and media literacy. Do NOT use for formal debate coaching or legal advocacy."
license: MIT
author: Sandeep Kumar Penchala
type: philosophy-wisdom
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [critical-thinking, argumentation, media-literacy, skepticism, cognitive-bias]
token_budget: 4000
chain: |
  - step: map claim
  - step: test evidence
  - step: rebut and refine
---

# Critical Thinking Toolkit — portability: individual, classroom, newsroom

<!-- QUICK: 30s --> A pragmatic system for mapping arguments, spotting bias, and testing claims with a Socratic bank and fallacy catalogue tied to exercises.

## RESEARCH_PREREQUISITE

| RP | Description |
|----|-------------|
| RP1 | Claim to evaluate stated clearly |
| RP2 | Source list and provenance |
| RP3 | Available evidence and datasets |
| RP4 | Stakeholder motives |
| RP5 | Time horizon for decision |
| RP6 | Relevant domain expertise available |
| RP7 | Known biases or conflicts of interest |
| RP8 | Tolerance for false positives/negatives |

## Iterative Research Loop

| Loop | Activity | Output |
|------|----------|--------|
| Loop 0 | Clarify claim and success criteria | Clear hypothesis + what evidence would change mind |
| Loop 1 | Map the argument structure | Premises -> inference -> conclusion map |
| Loop 2 | Test evidence & sources | Evidence table with credibility scores |
| Loop 3 | Steel-man and counter-argue | Revised claim or rejection decision |

## Quickstart (30s outputs)

1) Write the claim as a sentence and identify the conclusion.
2) Ask 3 Socratic questions from the bank focusing on evidence and assumptions.
3) State whether you would provisionally accept, reject, or suspend judgment.

<!-- STANDARD: 3min --> Ground Rules

- Mechanical triggers:
  - If claim impacts >100 people, require source-verification and two independent corroborations.
  - If claim uses statistics, always check sample size and base rates first.
  - If emotional language is present, suspect motivated reasoning and ask for raw data.
- Negative constraints:
  - Do not conflate rhetoric with evidence.
  - Avoid ad hominem rebuttals; target arguments, not people.
  - Do not accept conclusions based on single unreplicated studies.

## Decision Tree: How to evaluate a claim

Start
├─ Is the claim empirical?
│  ├─ Yes -> Check data, methods, sample size
│  │   ├─ n >= 30? -> Yes -> Evaluate effect sizes
│  │   └─ No -> Look for replication or triangulation
│  └─ No -> Philosophical/axiomatic -> Map underlying assumptions
├─ Is the source primary or secondary?
│  ├─ Primary -> Assess methodology
│  └─ Secondary -> Trace to primary for verification
├─ Is there clear motive/conflict of interest?
│  ├─ Yes -> Downgrade credibility and seek independent sources
│  └─ No -> Proceed with standard checks
└─ Apply SIFT/CRAAP for media claims

## Core Workflow

STANDARD: (10–30 minutes)
1. Map premises and conclusion (5–10 min).
2. Evaluate each premise: evidence strength, source credibility (10–15 min).
3. Steel-man best opposing argument (5 min).
4. Decide: accept/provisionally accept/reject/suspend, with next evidence triggers.

DEEP: (30–120 minutes)
1. Recreate key analyses (if data available) or request replication materials.
2. Run simple robustness checks (sensitivity to sample, alternative specs).
3. Build a public transparency note with steps to replicate your evaluation.

<!-- DEEP: 10+min --> Fallacy Catalog & Socratic Bank

Top fallacies to watch (real-world examples and detection cues)
- Straw man: check if opposition actually claims what's being criticized.
- Ad hominem: separate critique of person from claims.
- Post hoc ergo propter hoc: check temporal precedence vs causation.
- Survivorship bias: look for missing negative cases.
- Base-rate neglect: compute base rates and update priors.
- Cherry-picking: search for omitted contradictory evidence.

Socratic question bank (20+ by category)
- Evidence: What evidence would change your mind? How was this evidence collected?
- Assumptions: Which assumptions underlie this claim? Are they stated?
- Alternative explanations: What else could produce the observed effect?
- Stakes: Who benefits if this claim spreads? Who loses?

## Error Decoder

| Error / Pitfall | Root Cause | Fix | Lesson |
|-----------------|------------|-----|--------|
| Accepting clickbait | Emotional salience | Delay judgment; trace to primary source | Prioritize primary sources |
| Confirmation bias | Motivated reasoning | Steel-man opposing view | Seek disconfirming evidence |
| Statistical misinterpretation | Numeracy gaps | Recalculate effect sizes and CIs | Numbers require context |
| Conflating correlation with causation | Lack of counterfactuals | Demand experimental or quasi-experimental evidence | Causation needs intervention logic |
| Source ambiguity | Secondary reporting | Trace to original study/report | Originals beat summaries |

## Best Practices

1. Always map argument structure before critiquing; it reveals hidden premises.
2. Use the SIFT method for online claims: Stop, Investigate, Find better coverage, Trace to source.
3. Insist on base rates for probabilistic claims; adjust priors before accepting small studies.
4. Steel-man and document the strongest counterargument before rejecting a claim.
5. Keep a fallacy cheat-sheet visible when moderating debates.
6. Use short replication checks for important claims (recompute simple stats).
7. Maintain a public log of significant evaluations for transparency.
8. Adopt a low threshold for suspension; better to be uncertain than wrong with impact.
9. Use multiple independent sources when stakes exceed your tolerance for error.
10. Train using real-case drills weekly.

## Production Checklist

- [ ] Claim clearly written
- [ ] Premises mapped
- [ ] Sources traced to primary
- [ ] Evidence table created
- [ ] Fallacies checked
- [ ] Steel-man drafted
- [ ] Decision and triggers recorded
- [ ] Replication steps outlined if applicable
- [ ] Transparency note prepared
- [ ] Review scheduled (30 days)

## Exercises (5–15 minutes)

Exercise A: Fallacy spotting (10 min)
1. Pick a news article and extract the main argument.
2. Map premises and conclusion.
3. Identify at least 2 possible fallacies or weak premises.

Exercise B: Steel-manning (15 min)
1. Choose an opposing view you disagree with.
2. Write the strongest possible version of it in 5 bullet points.
3. Note what would convince you to shift your view.

## Verification: measure calibration and quality

- Track accept/reject decisions and whether future evidence changed decision within 90 days.
- Track time-to-verification for high-stakes claims.
- Measure false-accept rate on a sample of 100 past claims.
- Use peer review on critical evaluations.

## Cross-Skill Coordination

| Skill | Role in workflow |
|-------|------------------|
| mental-models | Provide models to explain causation and systems |
| decision-engineer | Formal decision thresholds and cost models |
| media-literacy | Source evaluation and provenance checks |

## What Good Looks Like

- Transparency note replicable by a peer in <= 2 hours.
- Decisions maintained with confidence intervals and explicit triggers for revision.
- Low false-accept rate on retrospective checks.
- Team adoption of argument-mapping as meeting norm.

## References

- Paul, Richard & Linda Elder, Critical Thinking: Tools for Taking Charge of Your Learning and Your Life
- Kahneman, Daniel, 2011, Thinking, Fast and Slow
- Silver, Nate, 2012, The Signal and the Noise
- Lewandowsky, S., 2012, The Debunking Handbook
- Prinz, Jesse, 2017, SIFT: A Practical Framework for Source Evaluation (essay)

## Scale Depth

- Solo: Daily learning and fallacy drills (tools: flashcards, Obsidian)
- Classroom: Argument-mapping exercises and peer review (tools: Hypothesis, Miro)
- Newsroom: Rapid verification playbooks and replication checks (tools: Slack, Google Sheets)
- Research org: Integrate into methods review and preregistration checks (tools: OSF, GitHub)

## Anti-Hallucination

[VERIFIED] SIFT and CRAAP are established source-evaluation heuristics.
[COMMON-PRACTICE] Steel-manning and Socratic questioning are used across skepticism communities.
[INFERRED] Specific time budgets are practitioner heuristics.
[UNKNOWN] Exact error rates depend on domain and reviewer expertise.
