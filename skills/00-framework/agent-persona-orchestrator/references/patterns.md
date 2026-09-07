# Orchestration Patterns

- Router: one task, best-fit persona (classify then dispatch).
- Pipeline: serial handoffs where each persona consumes the previous output.
- Committee: parallel reviewers on the same artifact, joined by a decision gate.
- Swarm: many small parallel tasks fanned out and aggregated.
- Hybrid: router -> pipeline with committee gates at decision points.
