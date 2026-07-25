## What Good Looks Like

Every event has a registered schema with version. Consumers are idempotent and DLQ-backed. Consumer lag <200ms p95. Correlation IDs trace a user action across 10+ services. Replay 6 months of events -> reconstruct any read model in <15 min. Poisoned message lands in DLQ within 3 retries, alert fires, healthy consumers never stop.
