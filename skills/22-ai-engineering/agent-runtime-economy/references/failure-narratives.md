# Failure Narratives

Five ways runtime economy fails in practice, and the rule each justifies.

## 1. The optimised body, the untouched floor

A team spends a quarter shrinking skill bodies by 40%. Session cost falls 3%, because the ambient listing — never measured — is 40% of every prompt and the bodies are loaded only sometimes.
**Rule:** R1 — measure the ambient floor first.

## 2. The cheaper wrong answer

Cost per session drops 30% after a context cut. Nobody re-ran the success metric. Task success also dropped, and the team found out from a customer.
**Rule:** R4 — pair every cost with a success metric.

## 3. The cap that was raised

A session cap binds once. The reflex is to raise it. The cap's only signal — that this task class costs more than expected — is discarded, and the real cause is never investigated.
**Rule:** R2 — a budget is a decision, not a constraint.

## 4. The loop that ran to the cap

An agent retries the same failing approach nineteen times. Each retry is a small burn; together they dominate the session. No convergence condition existed, so nothing ended it early.
**Rule:** R3 — the stop rule is the cheapest optimisation available.

## 5. The workflow that cost more than the task

A single classification step is implemented as a three-node workflow with state, checkpoints, and a retry gate. It costs more to run than the task it performs, and was never compared to one call.
**Rule:** R6 — structure must earn its cost against the simplest baseline.
