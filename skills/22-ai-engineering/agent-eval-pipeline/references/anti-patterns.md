# Anti-Patterns — Agent Evaluation Pipeline

## 1. The Single-Run Oracle
**What it looks like:** Running eval once and declaring the agent "passes" or "fails."
**Why it fails:** Agent behavior is a distribution. A single run has sampling error of ±5-10%.
**Fix:** Run eval 30+ times, compute bootstrap CIs. Only declare pass/fail when CIs don't overlap.

## 2. The Vanishing Baseline
**What it looks like:** Changing the eval scenarios, judge prompt, or scoring rubric without preserving the old baseline.
**Why it fails:** Without a stable baseline, you cannot detect regression — you can only measure absolute scores.
**Fix:** Version baselines with the agent version. Never overwrite. Compare against the baseline from the last known-good agent version.

## 3. The Metric Monoculture
**What it looks like:** Optimizing for one metric (e.g., tool-call accuracy) to the exclusion of all others.
**Why it fails:** Goodhart's Law — when a metric becomes a target, it ceases to be a good metric. Agents optimize for the measured dimension at the expense of unmeasured ones.
**Fix:** Track 5+ dimensions: correctness, efficiency, safety, robustness, faithfulness. Weight them in the final score.

## 4. The Judge-Jury-Executioner
**What it looks like:** Using the same LLM as judge that powers the agent under test.
**Why it fails:** Self-enhancement bias — models prefer their own outputs. GPT-4 scores GPT-4 outputs higher than Claude outputs.
**Fix:** Use a different model family for the judge than the agent. Multi-judge ensemble: median of 3 judges from different providers.

## 5. The Completeness Delusion
**What it looks like:** Believing 200 test cases cover all agent behavior.
**Why it fails:** Agent behavior space is combinatorial. 200 cases cover <1% of the input distribution.
**Fix:** Use embedding-based coverage analysis. Stratified sampling across the input distribution. Rotate 30% of cases monthly from a held-out pool.

## 6. The Gatekeeper's Fallacy
**What it looks like:** Setting eval gates so strict that they block 20% of legitimate PRs.
**Why it fails:** Developers bypass the gate. Within 3 months, 40%+ of PRs are force-merged.
**Fix:** Track false-positive rate. If >2%, loosen thresholds. Require 3 consecutive failures to block. Auto-recover.

## 7. The Cost Blindspot
**What it looks like:** Running GPT-4o as judge on every PR without tracking cost.
**Why it fails:** Eval costs $22,500/month while catching only 5% of regressions that a cheaper model would also catch.
**Fix:** Tier eval by cost. Track eval spend as a metric. Set budget alerts. Use expensive judges only for release gates.
