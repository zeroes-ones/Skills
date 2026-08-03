---
name: "decision-engineer"
description: "Use when structuring important personal decisions. Handles bias mitigation, decision matrices, expected value, pre-mortems, reversibility analysis, decision journaling, Bayesian updating, and speed frameworks. Do NOT use for formal organizational governance or legal rulings."
license: MIT
author: Sandeep Kumar Penchala
type: personal-growth
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [decision-making, bias, bayesian, premortem, matrix, ev, calibration]
token_budget: 4000
chain:
  consumes_from: []
  feeds_into: [master-negotiator, life-architect, productivity-master]
  alternatives: []
---
# Decision Engineer
Portability: personal-growth / decision workflows

<!-- QUICK: 30s -->
One-line: A structured toolkit to reduce cognitive bias, model expected value, and produce auditable decisions with clear reversibility rules.

## RESEARCH_PREREQUISITE
| Code | Requirement |
|------|-------------|
| RP1  | Clearly stated decision question |
| RP2  | Time horizon and stakes defined |
| RP3  | Access to relevant data or estimates |
| RP4  | Willingness to write down probabilities |
| RP5  | A decision journal or note space |
| RP6  | 30–60 minute block for structured analysis |
| RP7  | Optional: peer reviewer for calibration |
| RP8  | Commitment to post-outcome audit |

## Iterative Research Loop
| Loop | Purpose | Input | Output |
|------|---------|-------|--------|
| 0 | Problem framing | Decision question | Constraints & objectives |
| 1 | Bias sweep | List of common biases | Debias strategies applied |
| 2 | Modeling | Inputs and priors | EV calculation and sensitivity |
| 3 | Audit | Outcome & logs | Calibration updates |

## Quickstart (30s)
1. Write the decision question in one line.
2. State the time horizon and stakes.
3. Pick one key uncertainty and estimate probabilities now.
4. Decide on a pilot or reversible step to test.

<!-- STANDARD: 3min -->
## Ground Rules
- Mechanical triggers: always run a 5-minute pre-mortem when decision impact > medium.
- Negative constraints: avoid overfitting to recent anecdotal evidence.
- Documentation: record priors and update after outcomes.
- Stop rule: define an explicit decision stop-rule (time, information threshold) before analysis begins.

## Decision Tree (expanded)
Start
|
+- Is decision reversible? -> Yes -> Design rapid experiments -> Collect data -> Update priors
|                         -> No -> Run full EV model & pre-mortem
|
+- Sufficient data? -> Yes -> Build model, run sensitivity, pick option with highest EV
|                   -> No -> Design pilot to reduce uncertainty or choose option-value approach
|
+- High stakes & uncertain -> Use staged commitments and fallback options
|
## Core Workflow
STANDARD: Framing & Objectives
1. Define the decision question and objective function with success criteria.
2. List constraints, stakeholders, and non-negotiables.

STANDARD: Bias Mitigation
1. Run a bias checklist: confirmation, anchoring, availability, sunk cost, overconfidence, survivorship.
2. Apply mitigation tactics: outside view, reference class forecasting, devil's advocate, anonymized estimates.

STANDARD: Modeling & EV
1. Build a simple EV table: outcomes, probabilities, utilities (monetary or utility points).
2. Run sensitivity and scenario analysis on top 3 assumptions.
3. If distributions are unknown, use conservative priors and widen confidence intervals.

DEEP: Pre-Mortem & Red-Teaming <!-- DEEP: 10+min -->
1. Convene a 20–40 minute pre-mortem: imagine failure in 12 months and list all causes.
2. Prioritize top causes and design monitoring signals and contingency actions.
3. War story: a startup skipped a pre-mortem and later ran into predictable supply-chain failure; the pre-mortem would have surfaced vendor concentration risk.
4. Edge case: decisions with emotional stakes require a neutral facilitator to avoid escalation.
5. Exercise: conduct a 20-minute pre-mortem for one current decision and produce three monitoring metrics.

DEEP: Decision Journal & Bayesian Updating <!-- DEEP: 10+min -->
1. Record priors (probability estimates) for key uncertainties before acting and the rationale for each.
2. As evidence arrives, update probabilities and log adjustments and reasons.
3. War story: an investor tracked priors and discovered calibration drift, refining models and improving forecast accuracy over two years.
4. Edge case: when evidence is ambiguous, note signal strength and plan a small experiment to resolve it.
5. Exercise: record priors for a pending decision; schedule updates at 1, 3, and 6 months.

## Expanded Error Decoder (5-8 rows)
| Error Message / Pitfall | Root Cause | Fix | Lesson |
|-------------------------|------------|-----|--------|
| "We misestimated risk" | Overconfidence, no reference class | Use outside view and priors from similar cases | Systematic priors beat anecdotes |
| "Decision felt rushed" | Lack of stop-rule or reversibility check | Build pilot or phased commitment | Small experiments reduce regret |
| "Analysis paralysis" | Pursuit of more data than useful | Apply stop-rule and choose a pilot | Perfect info is rare and costly |
| "Ignored stakeholder friction" | Not listing stakeholders early | Map stakeholders and run rapid alignment | Operational constraints matter |
| "Bias in forecasts" | Anchoring to recent events | Run a de-biasing checklist and seek outside estimates | Awareness alone is insufficient |
| "Monitoring signals missed" | No pre-defined metrics | Pre-define leading indicators and thresholds | If you can't measure, instrument it before acting |

## Best Practices (8-10)
1. Always write a one-sentence decision question and a one-paragraph objective function.
2. Define a clear stop-rule before analysis (time or information threshold).
3. Use reference-class forecasting for probability estimates where personal experience is limited.
4. Prefer staged commitments with explicit triggers and exit clauses for irreversible choices.
5. Maintain a decision journal and review calibration quarterly.
6. Use pre-mortems for medium+ stakes and red-team critical assumptions.
7. Convert key uncertainties into measurable signals before implementation.
8. When in doubt, design a pilot that limits downside and tests the most critical assumption.
9. Share a short decision memo with a peer reviewer for feedback when possible.
10. Keep models simple; complexity should be justified by significant value improvements.

## Production Checklist (12 items)
- [ ] Decision question written in one sentence
- [ ] Time horizon and stakes documented
- [ ] Stakeholder map created
- [ ] Bias sweep checklist completed
- [ ] EV model or pilot plan created
- [ ] Sensitivity analysis performed on top 3 assumptions
- [ ] Pre-mortem scheduled (if medium+ stakes)
- [ ] Decision journal entry created with priors
- [ ] Stop-rule defined and recorded
- [ ] Monitoring signals and thresholds set
- [ ] Pilot launch plan with metrics ready (if chosen)
- [ ] Post-outcome audit scheduled

## Metrics & Measurement (concrete)
- Calibration error: absolute difference between predicted probabilities and observed frequencies over multiple decisions (target decreases over time).
- Pilot success rate: % of pilots that deliver signal reduction for key uncertainties.
- Decision cycle time: median time from question to decision for small/medium/large decisions.
- Reversibility index: % of decisions classified as reversible within a given time window.

## Exercises & Templates
Exercise 1 — 10-minute decision sketch
1. Write the decision question and horizon in one line.
2. List top 3 possible outcomes and an estimated probability for each.
3. Choose one testable assumption and propose a pilot.
Expected outcome: actionable pilot idea and prioritized uncertainty.

Template: Decision memo (one page)
- Decision question:
- Time horizon & stakes:
- Options considered:
- EV calculation summary:
- Key assumptions & monitoring signals:
- Stop-rule:
- Recommendation & next steps:

## Decision Tree (expanded)
Start
|
+- Can we pilot? -> Yes -> Design pilot -> Run -> Update priors -> Decide
|              -> No -> Build EV model -> Pre-mortem -> Choose best option
|
+- Is reversibility high? -> Yes -> Favor experimentation
|                        -> No -> Increase analysis depth and include contingency plans
|
+- Stakeholders misaligned? -> Yes -> Run rapid alignment workshop -> renegotiate constraints
|                         -> No -> Proceed to chosen option

## Cross-Skill Coordination (expanded)
| Skill | Role | Coordination Pattern |
|-------|------|----------------------|
| life-architect | Prioritization | Use decision models for major life trade-offs and runway planning |
| master-negotiator | Calibration | Use EV to set reservation prices and negotiation levers |
| productivity-master | Execution | Time-box experiments and pilots into calendars |

## What Good Looks Like (concrete)
- Documented decisions with priors and post-mortems for major decisions; calibration error decreases over time.
- Majority of high-impact decisions include staging or pilot approach.
- Monitoring signals triggered appropriately and countermeasures tested within time windows.

## References (5-8)
- Kahneman, D. (2011). Thinking, Fast and Slow.
- Tetlock, P. (2015). Superforecasting: The Art and Science of Prediction.
- Clemen, R. T. (1996). Making Hard Decisions: An Introduction to Decision Analysis.
- Research on reference class forecasting (Flyvbjerg et al.).
- Tools: simple EV spreadsheets, decision journal templates, Monte Carlo plugins for Google Sheets.

## Scale Depth (expanded)
Solo: personal decision journal and memo templates; simple EV spreadsheets.
Small: shared decision templates for partners or small teams with review protocol.
Medium: multi-stakeholder decisions with facilitator, documented assumptions, and external reviewers.
Enterprise: route to governance frameworks and decision protocols with stakeholder maps and legal review.

## Anti-Hallucination
- [VERIFIED] Pre-mortems and outside-view debiasing are validated techniques.
- [COMMON-PRACTICE] Decision journals improve calibration when consistently used.
- [INFERRED] Bayesian updating is powerful but requires systematic logging.
- [UNKNOWN] Predictive accuracy depends on domain and data quality; treat probabilistic forecasts with humility.
