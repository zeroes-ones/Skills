# Production Checklist — Agent Evaluation Pipeline

## Pre-Development
- [ ] Agent behavior specification written (what should the agent do?)
- [ ] 5 evaluation dimensions defined with behavioral rubric anchors
- [ ] 20+ initial eval scenarios drafted (happy-path + edge-case)
- [ ] Eval harness directory scaffolded (`eval/` with `Dockerfile`, `run.py`)

## Development
- [ ] Test pyramid populated: 200+ unit cases, 50+ integration scenarios, 20+ E2E scenarios
- [ ] Continuous scoring (0.0-1.0) implemented for all dimensions
- [ ] LLM-as-judge prompt written with rubric anchors inline
- [ ] Judge calibrated against 3+ human raters, kappa ≥ 0.7
- [ ] Position bias measured and mitigated (symmetric evaluation)
- [ ] SPRT configured: α=0.05, β=0.20, δ=0.05
- [ ] Eval Dockerfile written and tested locally

## Pre-Merge (Tier 1)
- [ ] 50 stratified scenarios selected for fast pre-merge eval
- [ ] GPT-4o-mini (or equivalent) configured as Tier-1 judge
- [ ] CI workflow triggers on PR to main
- [ ] PR comment template with per-dimension scores vs baseline
- [ ] WARN threshold: baseline - 1.5σ, BLOCK threshold: baseline - 2.5σ
- [ ] 3 consecutive failures required to block (flaky-gate protection)

## Nightly (Tier 2)
- [ ] Full scenario suite (200-500) runs nightly
- [ ] GPT-4o configured as Tier-2 judge
- [ ] Gotcha suite (50+ scenarios) included
- [ ] Bootstrap CIs computed for all dimensions
- [ ] Drift detection: embedding cosine similarity, token budget, latency
- [ ] Dashboard with 30-day trends and alert thresholds

## Release (Tier 3)
- [ ] Full suite + 20% rotation set + adversarial set
- [ ] Highest-quality judge model (GPT-4o/Opus)
- [ ] All dimensions must pass at p < 0.01
- [ ] Safety gate: any unsafe action → absolute block
- [ ] Manual review triggered for any safety failure

## Ongoing
- [ ] Monthly recalibration: check judge-human kappa
- [ ] Monthly scenario rotation: 30% new from held-out pool
- [ ] Monthly false-positive rate report: target <2%
- [ ] Monthly eval cost report: target <10% of production inference cost
- [ ] Quarterly silent regression fire drill
- [ ] Quarterly review: are evaluation dimensions still the right ones?
