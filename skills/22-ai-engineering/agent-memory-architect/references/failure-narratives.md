# Failure Narratives

Five ways memory systems fail in practice, and the rule each justifies.

## 1. The store nobody reads

A team builds an append-only run log with a clean schema, per-run provenance, and a manage job. Six months later the store holds thousands of entries and no code path reads any of them. Cost is real; benefit is zero.
**Rule:** R1 — write-manage-read, or it is a log.

## 2. The confident wrong answer

A run concludes that an API returns a list; it actually returns a paginated object. The conclusion is stored. A later run retrieves it, treats it as fact, and builds on it. The original error is now a premise.
**Rule:** R6 — store the outcome, retrieve as prior.

## 3. The summary that drifted

A consolidation job summarises old entries weekly. After a year the summary describes a workflow that was never run, because each summarisation distorted slightly and the distortions compounded.
**Rule:** R4 — count, never re-summarise.

## 4. The injection path

An agent ingests a web page containing text shaped like a system instruction. The run stores a conclusion that echoes it. A later run retrieves the entry inside its instruction block and follows it.
**Rule:** R2 — context-only label at the injection boundary.

## 5. The archive that ate the task

Memory grows uncapped. Eventually injection consumes most of the window, and answer quality degrades *as memory improves*, because there is less room for the actual task.
**Rule:** R3 + retrieval budget — bound the store and cap its share.
