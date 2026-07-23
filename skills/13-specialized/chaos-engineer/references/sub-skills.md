# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
When the agent identifies a specific chaos engineering need, drill into the relevant sub-skill. Each sub-skill has dedicated references — the experiment catalog (42 ready-to-use experiments) and the GameDay playbook (complete facilitation guide).

| Sub-Skill | What It Covers | Reference |
|-----------|---------------|-----------|
| **Fault Injection** | Pod kills, network latency/partition, resource exhaustion (CPU, memory, disk, file descriptors), DNS failures, clock skew — implementation via Chaos Mesh, LitmusChaos, Gremlin, AWS FIS, or custom scripts | `references/chaos-experiment-catalog.md` (42 experiments) |
| **Steady State Hypothesis Design** | Defining measurable "normal" behavior, selecting latency/error/throughput indicators, writing falsifiable hypotheses, control vs experiment comparison | Section below: "Steady State Hypothesis Deep Dive" |
| **Blast Radius Engineering** | Scope containment (traffic %, user segment, infrastructure scope), abort conditions (auto-termination triggers), progressive expansion (staging → canary → 1% → 10% → prod) | Section below: "Blast Radius (Military-Grade Controls)" |
| **GameDay Facilitation** | Pre-game planning (2 weeks), day-of execution timeline (briefing → experiments → debrief), roles (Commander/Operator/Observer/Scribe), post-game action items — full playbook | `references/game-day-playbook.md` (complete guide with templates) |
| **Resilience Pattern Validation** | Verifying circuit breakers (closed→open→half_open→closed), retry with backoff + jitter, bulkhead isolation, timeouts, rate limiters — chaos experiments that prove they work | Section below: "Tooling Deep Dive" + experiment catalog |
| **Chaos in CI/CD** | Automated experiments in staging CI, SLO-based gating, error budget integration, scheduled production experiments | Section below: "CI/CD Integration for Chaos" |

> **Token-saving rule:** Planning a GameDay? Load the GameDay playbook (731 lines) and only the experiment catalog entries for the experiments you're running. Don't load tooling deep dives for tools you aren't using. The experiment catalog alone would consume massive tokens if loaded entirely — pick specific experiments.
