# Footguns — Agent Evaluation Pipeline

## 1. The "One More Scenario" Trap
Adding scenarios indefinitely without removing stale ones. Eval suite grows from 200 to 2,000 scenarios. Runtime balloons from 5 min to 90 min. Developers start skipping eval.
**Avoidance:** Cap scenario count per tier. Rotate 30% monthly. Archive scenarios that haven't caught a regression in 6 months.

## 2. The "Judge Knows Best" Fallacy
Trusting LLM judge scores without human validation. Judge develops systematic biases (e.g., preferring passive voice, penalizing direct answers). Scores drift without anyone noticing.
**Avoidance:** Monthly human spot-check: 20 random scenarios, human re-scores. If human-judge divergence >0.1, recalibrate.

## 3. The "More Runs = Better" Myth
Running 10,000 eval runs because "more data is better." Each run costs money. At some point, additional runs reduce CI width by <0.001 — meaningless for decisions.
**Avoidance:** Compute CI width vs N. Stop when additional 100 runs reduce CI by <0.005. Usually N=100-500 is sufficient.

## 4. The "Baseline Is Sacred" Error
Never updating the baseline because "the old scores are the standard." Agent capabilities improve over time. A 6-month-old baseline represents an agent that's objectively worse than today's.
**Avoidance:** Update baseline quarterly. Old baseline becomes a historical reference, not the gate threshold.

## 5. The "All Dimensions Equal" Assumption
Weighting correctness, efficiency, safety, robustness, and faithfulness equally. For a medical agent, safety weight = 0.50. For a code-gen agent, correctness weight = 0.40.
**Avoidance:** Define per-agent dimension weights based on use-case risk. Document the rationale. Review weights quarterly.

## 6. The "Eval Is QA's Job" Mindset
Developers write agent code; a separate QA team writes eval. Eval scenarios lag 2-4 weeks behind agent changes. Regressions reach production before eval catches them.
**Avoidance:** Eval scenarios live in the same repo as agent code. PRs that change agent behavior MUST include eval scenario updates. No separate eval team — embedded eval engineer per agent team.

## 7. The "We'll Automate Calibration Later" Deferral
Using uncalibrated judge scores "temporarily" while planning to calibrate. Temporary becomes permanent. Six months later, all shipping decisions are based on uncalibrated noise.
**Avoidance:** Calibration is a launch blocker, not a nice-to-have. No agent ships to production without calibrated eval. If calibration data isn't ready, the agent isn't ready.
