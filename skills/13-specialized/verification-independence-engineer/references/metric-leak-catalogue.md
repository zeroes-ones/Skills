# Metric-Leak Catalogue — the cheapest path that betrays an intent

> Every optimised metric is a proxy. This catalogue names, for common metrics, the intent they
stand for, the cheapest path that satisfies the number while betraying it, and the harm metric
that guards it.

---

## The metric-leak catalogue

A metric is a proxy for an intent. Optimising the proxy without guarding the intent is the failure
the article this skill derives from calls *goal blindness* — the loop can only see the metric it was
given, so it satisfies the metric by whatever path the environment permits. This is not a model
being deceptive; it is a number being maximised exactly as specified.

| Target metric | Stated intent | The leak (cheapest satisfying path) | Harm metric that guards the intent |
|---------------|---------------|-------------------------------------|-----------------------------------|
| Ticket resolution rate | Support resolves real problems | Close conversations fast; mark abandoned issues resolved; discourage follow-up | **Reopen rate**, **churn at renewal**, time-to-second-contact |
| Tickets closed per hour | Throughput of support | Close low-value tickets quickly; split tickets to inflate the count | **Customer effort score**, escalation rate |
| Deploys per day | Ship value faster | Deploy trivial changes; split one change into many | **Change failure rate**, mean time to restore |
| Test coverage % | Code is exercised | Test getters and trivial branches; assert nothing meaningful | **Mutation score**, escaped-defect count |
| Lines added / story points | Work is progressing | Inflate estimates; add unused code | **Cycle time to production**, rework rate |
| Cache hit rate | Reduce origin load | Cache almost everything, including wrong things | **Origin QPS during flush**, stale-read incidents |
| Agent task completion % | Agent does useful work | Declare success on partial results; skip verification | **Human re-do rate**, downstream defect escapes |
| Cost per call | Efficiency | Skip the verifier; truncate context; use a weaker model everywhere | **Cost per successful outcome**, re-run rate |
| Latency p50 | System feels fast | Serve stale data; skip validation | **p99**, **error rate**, **staleness violations** |
| Model accuracy on eval | The model is better | Overfit the eval set; leak test data | **Held-out set accuracy**, **live-outcome delta** |

### The rule, stated once

```
Gate on:  target improves   AND   harm metric does not degrade
Never on: target improves (alone)
```

A target with no measurable harm path is not evidence that the target is safe — it is evidence that
the search for the leak was too shallow. Every proxy has one; finding it is the work (Decision
Tree 4).

### Why the leak is invisible without the pair

Aggregate quality can rise while the thing the quality metric stood for falls, for as long as the
lag between them exceeds the measurement window. Resolution rate improved for five months before
churn doubled at renewal, in the classic telling — the metric was green the entire time because the
lag had not yet resolved. **The pair only works if both are read on the same cadence.**

---
