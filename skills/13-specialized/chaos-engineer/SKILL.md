---
name: chaos-engineer
description: >
  Use when designing chaos experiments, planning GameDays, validating system resilience
  through controlled fault injection, or building organizational confidence in failure handling.
  Handles chaos experiment design, fault injection (network latency, pod kills, resource
  exhaustion, AZ failure), blast radius control, steady state hypotheses, GameDay facilitation,
  and resilience pattern validation (circuit breaker, retry, bulkhead). Do NOT use for general
  monitoring setup, standard incident response, capacity planning, or routine performance testing.
license: MIT
tags:
  - chaos-engineer
  - resilience
  - fault-injection
  - gameday
  - reliability
  - sre
  - observability
  - chaos
author: Sandeep Kumar Penchala
type: specialized
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from: ["devops-engineer", "site-reliability-engineer", "observability-engineer"]
  feeds_into: ["site-reliability-engineer", "incident-responder", "devops-engineer"]
---
# Chaos Engineer

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Systematic resilience verification framework based on Chaos Engineering principles. Covers experiment design, fault injection, blast radius management, GameDay facilitation, resilience pattern validation, and building organizational confidence in system behavior under failure.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | site-reliability-engineer | SLO definitions, error budgets, monitoring dashboards, alert configurations |
| **This** | chaos-engineer | Chaos experiment designs, fault injection runbooks, GameDay reports, resilience validation |
| **After** | observability-engineer | Enhanced dashboards, alert tuning, anomaly detection patterns validated by chaos |

Common chains:
- **Chain**: site-reliability-engineer → chaos-engineer → observability-engineer — SRE defines what "reliable" means; chaos engineer proves (or disproves) it; observability engineer tunes detection.
- **Chain**: devops-engineer → chaos-engineer → incident-responder — DevOps provisions the testing environment; chaos engineer injects faults; incident responder validates detection and response playbooks.

## Sub-Skills
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

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.yaml", "kind: ChaosEngine\|kind: NetworkChaos\|kind: PodChaos\|kind: StressChaos")` OR `file_contains("*.json", "\"gremlin\"\|\"chaos-mesh\"\|\"litmus\"")` OR `file_exists("gremlin.yaml\|chaos-experiment.yaml")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.yaml", "apiVersion: litmuschaos.io\|chaos-mesh.org")` AND `file_contains("*.yaml", "steadyState\|hypothesis")` | Jump to **Decision Trees** — Steady State Hypothesis Design. |
| A3 | `file_contains("docker-compose.yml\|*.yaml", "prometheus\|grafana\|datadog")` AND `file_contains("*", "alert\|dashboard\|SLO\|error.budget")` | Invoke **observability-engineer** instead. Observability must be in place before chaos. |
| A4 | `file_contains("*.yaml", "deployment\|statefulset\|daemonset")` AND NOT `file_contains("*.yaml", "readinessProbe\|livenessProbe")` | STOP. Jump to **Ground Rules** R1 — no chaos without health checks. |
| A5 | `file_exists("PagerDuty.yaml\|opsgenie.yaml\|incident-response")` AND `file_contains("*", "runbook\|on-call\|escalation")` | Invoke **incident-responder** instead. This is incident response playbook work. |
| A6 | `file_contains("*.tf\|*.tfvars", "aws_\|azurerm_\|google_")` AND `file_contains("*", "VPC\|subnet\|multi-region\|failover")` | Invoke **devops-engineer** instead. This is infrastructure provisioning. |
| A7 | `file_contains("*", "SLO:\|error_budget:\|burn_rate:")` AND `file_contains("*", "99.9\|99.95\|99.99")` | Invoke **site-reliability-engineer** instead. SLO definitions are SRE domain. |
| A8 | `file_contains("gremlin.yaml", "\"attacks\"")` OR `file_contains("*_experiment.yaml", "spec:\|action:\|selector:")` | Jump to **Core Workflow** — Phase 2 (Fault Injection). |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Design a chaos experiment with steady-state hypothesis → Jump to "Decision Trees" — Steady State Hypothesis
├── Run fault injection (network, pod kills, resource exhaustion) → Jump to "Core Workflow" — Phase 2
├── Plan and run a GameDay → Jump to "Core Workflow" — Phase 3 then "references/game-day-playbook.md"
├── Control blast radius and set up abort conditions → Jump to "Decision Trees" — Blast Radius Engineering
├── Validate resilience patterns (circuit breakers, retries, bulkheads) → Jump to "Sub-Skills" — Resilience Pattern Validation
├── Need SLOs or error budgets defined first → Invoke site-reliability-engineer skill instead
├── Need observability dashboards before experimenting → Invoke observability-engineer skill instead
└── Not sure? → Describe the system and I'll design a starting experiment for staging
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to design chaos experiments for services without health checks and readiness probes.** Chaos without observability is just breaking things — the blast radius is unbounded. | Trigger: `grep -rn "readinessProbe\|livenessProbe" --include="*.yaml" --include="*.yml"` returns 0 results for target deployment | STOP. Respond: "This service has no health checks. I won't design a chaos experiment until liveness and readiness probes are in place. Without them, the orchestrator can't detect failure and the experiment has no abort signal." |
| **R2** | **REFUSE to run production chaos without a verified kill switch.** Every experiment must have an abort mechanism tested in staging within the last 7 days. | Trigger: experiment plan lacks `grep -rn "abort\|kill.switch\|terminate\|rollback"` in experiment YAML/config AND no shell command provided to stop all active experiments (`kubectl delete chaosengine` or `gremlin halt`) | STOP. Respond: "Define the kill switch first. Add an abort command and test it in staging. Without an instant-stop mechanism, I won't authorize the experiment." |
| **R3** | **STOP and ASK when blast radius is undefined or unbounded.** The blast radius must be explicitly scoped: namespace, label selector, traffic percentage, or user segment — never `*` or `all`. | Trigger: experiment config contains `namespace: "*"` OR `selector: {}` OR `percent: 100` OR `blastRadius: null` OR no label selector on the fault injection | STOP. Ask: "What is the blast radius? Specify namespace, label selector, percentage of traffic, or user segment. I need explicit scope before proceeding." |
| **R4** | **DETECT and WARN when steady-state hypothesis is unfalsifiable.** "The system is resilient" is not a hypothesis. Every hypothesis must have measurable thresholds. | Trigger: hypothesis text matches `grep -i "resilient\|works fine\|handles failure\|stays up"` without numeric thresholds (P50/P95/P99, error rate %, throughput) | WARN: "This hypothesis is unfalsifiable. Rewrite with numeric thresholds, e.g.: 'P99 latency < 500ms AND error rate < 1% AND throughput > 1000 req/s during 30% packet loss for 120s.'" |
| **R5** | **DETECT and WARN when abort conditions lack numeric thresholds.** "If things look bad" is not an abort condition. Every abort trigger must be numeric and measurable. | Trigger: abort section contains `grep -iv "[0-9]\+%"\|"[0-9]\+ms"\|"[0-9]\+s"` — no numeric values found in abort criteria | WARN: "Add numeric abort thresholds: error rate > X%, P99 latency > Yms, duration > Zs. Without numbers, 'abort when it looks bad' means 'abort after the outage.'" |
| **R6** | **STOP and ASK when the target environment is ambiguous.** Production, staging, canary, or dev? The environment determines every safety parameter. | Trigger: experiment plan does not mention `staging` OR `production` OR `canary` OR `dev` OR `namespace:` explicitly | STOP. Ask: "Which environment? Staging, production, or canary? If production: what time window? Is on-call notified? Is the abort command tested?" |
| **R7** | **REFUSE to inject faults without first verifying observability coverage.** You must confirm the injected fault is visible on dashboards within 2 minutes before proceeding to production. | Trigger: no pre-experiment observability check: `grep -rn "prometheus\|grafana\|datadog\|metrics" --include="*.yaml" --include="*.json" experiment-config/` returns 0 AND no mention of dashboard/alerts in experiment plan | STOP. Respond: "Inject the fault in staging for 30 seconds first. If it's not visible on dashboards within 2 minutes, fix observability. Chaos without visibility is vandalism." |
## The Expert's Mindset

Masters of chaos engineer don't just build — they build **the right thing, at the right time, with the right trade-offs**. They think in systems, not tasks.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Shiny object syndrome** — chasing new tools without evaluating fit | Before adopting any new tool, write the "why this over the incumbent" justification |
| **Over-engineering** — building for hypothetical scale | Default to simplest solution; add complexity only when the current solution actually breaks |
| **Not-invented-here** — preferring to build rather than compose | Always evaluate 2 existing solutions before building custom |
| **Sunk cost fallacy** — sticking with a technology because you already invested in it | Re-evaluate tech choices every quarter; migration cost vs. staying cost |

### What Masters Know That Others Don't
- The **failure modes** of every component in their stack — not just the happy path
- When **not** to use their favorite tool (every tool has a misuse zone)
- That **data/model quality decays over time** — monitoring is not optional, it's foundational

### When to Break Your Own Rules
- **Move fast on reversible decisions.** Data format? Hard to change. Dashboard layout? Easy. Know the difference.
- **Skip the abstraction until the third use case.** Two is coincidence, three is a pattern.
## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single component/module | Implement a well-defined piece following established patterns |
| **L2** | Feature or service | Design and build a complete feature; make tech choices within team conventions |
| **L3** | System or product area | Define architecture for a product area; set team tech standards; mentor L1-L2 |
| **L4** | Multiple systems / platform | Define org-wide architecture patterns; make build-vs-buy decisions; influence industry practice |
| **L5** | Industry / ecosystem | Create new architectural patterns adopted across the industry; redefine what's possible |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 chaos engineer, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Establishing a Chaos Engineering practice from scratch — tooling, methodology, cultural buy-in.
- Designing and executing chaos experiments to verify system resilience hypotheses.
- Running a GameDay — a planned event where the team responds to injected failures under controlled conditions.
- Implementing circuit breakers, retries, timeouts, and bulkheads — and verifying they actually work under real faults.
- Testing auto-scaling behavior: does the system scale up correctly when nodes are killed?
- Validating observability: during a chaos experiment, can you detect, diagnose, and resolve the issue before it affects users?
- Building resilience scoring for services to prioritize hardening efforts.
- Preparing for AWS/Azure/GCP regional failures — testing multi-region failover.

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### 1. What to Chaos First
```
                     ┌─────────────────────┐
                     │ START: Pick a service│
                     └──────────┬──────────┘
                                │
                    ┌───────────▼───────────┐
                    │ Ran 3+ incidents in   │
                    │ last 6 months?        │
                    └────┬──────────────┬───┘
                         │ YES          │ NO
                    ┌────▼────────┐ ┌──▼──────────────────┐
                    │ Test failure│ │ Does the service have │
                    │ modes from  │ │ health checks, retries│
                    │ real post-  │ │ and circuit breakers? │
                    │ mortems     │ └──┬──────────────┬────┘
                    └─────────────┘    │ YES          │ NO
                              ┌────────▼─────┐  ┌─────▼────────┐
                              │ Start with a │  │ Implement     │
                              │ staging pod- │  │ resilience    │
                              │ kill test    │  │ patterns FIRST│
                              └──────────────┘  └──────────────┘
```
**Pick services with incident history** — test the failures you've already experienced before hypothetical ones.  
**If no resilience patterns exist** — chaos engineering without circuit breakers just proves you're fragile. Build resilience first.

### 2. Experiment Type Selection
```
                ┌──────────────────────────────┐
                │ START: What are you testing?  │
                └──────────────┬───────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
    ┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼────────┐
    │ Infrastructure│  │  Dependency  │  │  System-Wide   │
    │  resilience?  │  │   behavior?  │  │   confidence?  │
    └───────┬──────┘  └───────┬──────┘  └───────┬────────┘
            │                 │                  │
    ┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼────────┐
    │ Pod kill →   │  │ Network      │  │ AZ failure →   │
    │ Node drain → │  │ latency →    │  │ Region failover│
    │ CPU stress   │  │ Packet loss  │  │ → GameDay event│
    └──────────────┘  └──────────────┘  └────────────────┘
```
**Infrastructure tests** verify auto-scaling and self-healing. Start here — they're the safest.  
**Dependency tests** verify circuit breakers, retries, and timeouts. Run after infra tests pass.  
**System-wide tests** verify multi-AZ/region failover. Run as GameDays with full team participation.

### 3. Observability Gate
```
                  ┌────────────────────────────┐
                  │ START: Before any experiment│
                  └─────────────┬──────────────┘
                                │
                    ┌───────────▼───────────┐
                    │ Inject fault in staging│
                    │ for 30 seconds         │
                    └────────────┬──────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │ YES             │                  │ NO
     ┌─────────▼────────┐       │        ┌─────────▼──────────┐
     │ Can you see it   │       │        │ Fix observability  │
     │ on the dashboard │       │        │ gap. Document it.  │
     │ within 2 minutes?│       │        │ Re-test before     │
     └────────┬─────────┘       │        │ running experiment.│
              │                 │        └────────────────────┘
     ┌────────▼────────┐       │
     │ Does alert fire │       │
     │ within expected │       │
     │ time window?    │       │
     └────┬───────┬────┘       │
          │YES    │NO          │
     ┌────▼──┐ ┌──▼──────────┐│
     │Proceed│ │Tune alert   ││
     │to prod│ │thresholds   ││
     └───────┘ └─────────────┘│
```
**No observability = no experiment.** If you can't detect the fault, you can't learn from it.  
**Fix dashboards and alerts before anything else** — running chaos without observability is just breaking things.

### 4. Production Readiness Gate
```
                     ┌──────────────────────┐
                     │ START: Ready for prod?│
                     └──────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │ Staging GameDay       │
                    │ completed with clear  │
                    │ learnings?            │
                    └────┬──────────────┬───┘
                         │ YES          │ NO
                    ┌────▼────────┐ ┌──▼──────────────┐
                    │ Multi-AZ or │ │ Stay in staging. │
                    │ multi-region│ │ Never run first  │
                    │ deployment? │ │ experiment in    │
                    └──┬───────┬──┘ │ production.      │
                       │YES    │NO  └──────────────────┘
               ┌───────▼──┐ ┌──▼──────────┐
               │ Test AZ  │ │ Single-AZ is │
               │ failover │ │ your bottle- │
               │ first    │ │ neck. Fix it.│
               └──────────┘ └──────────────┘
```
**Staging GameDay first** — never your first experiment in production.  
**Multi-AZ/region failover is the highest-value production experiment** — test what protects you from real outages.

### 5. Tool Selection
```
                     ┌─────────────────┐
                     │ START: Pick tool│
                     └────────┬────────┘
                              │
                    ┌─────────▼──────────┐
                    │ Infrastructure is   │
                    │ 100% Kubernetes?    │
                    └────┬────────────┬───┘
                         │ YES        │ NO
                    ┌────▼──────┐ ┌──▼──────────────┐
                    │ Budget >$0?│ │ Multi-cloud or  │
                    └──┬─────┬───┘ │ VMs+bare metal? │
                       │YES  │NO   └──┬──────────┬───┘
               ┌───────▼──┐ ┌─▼────┐  │YES       │NO
               │ Gremlin  │ │Chaos │ ┌▼────────┐┌▼──────┐
               │ (managed)│ │Mesh  │ │ Gremlin ││AWS FIS│
               └──────────┘ │(free)│ │(paid)   ││(AWS)  │
                            └──────┘ └─────────┘└───────┘
```
**K8s-only + free → Chaos Mesh or LitmusChaos.**  
**Multi-platform → Gremlin.**  
**AWS-only → AWS FIS** (IAM integration, pay-per-action).

## Principles (Netflix's Original + Modern Evolution)

1. **Build a Hypothesis Around Steady-State Behavior**: define what "normal" looks like in measurable terms. Example: "The checkout service processes 95% of requests within 500ms P99 under normal load." Quantify everything — if you can't measure it, you can't defend it.

2. **Vary Real-World Events**: inject failures that mirror things that actually happen — server crashes, network partitions, disk failures, dependency latency spikes, certificate expirations, resource exhaustion. Run experiments based on postmortems and incident data. The best failure modes to test are the ones you've already experienced.

3. **Run Experiments in Production**: the only environment that truly reflects production is production. Staging lacks production-scale traffic, data cardinality, configuration quirks, and real-world request patterns. Staging is a stepping stone; production is the goal.

4. **Automate Experiments Continuously**: manual chaos experiments are valuable but episodic. Evolution path: manual GameDays → scheduled experiments → triggered-by-incident experiments → CI/CD chaos gates. Automated experiments catch regressions between releases.

5. **Minimize Blast Radius**: start tiny, expand only when confidence increases. If an experiment could hurt customers, you've failed to control the blast radius. Blood rule: if the experiment escapes containment, you abort before anyone paged.

## Experiment Types (Expanded Catalog)

### Infrastructure
- **Node/Instance Failure**: random node termination, targeted node (runs critical service), 50% of nodes in an ASG, spot instance preemption simulation.
- **AZ Failure Simulation**: block all traffic to/from an AZ, terminate all instances in an AZ, simulate a load balancer losing an AZ.
- **Region Failure**: simulated region outage via DNS blackhole or route table manipulation, test multi-region failover and DNS-based global load balancing.
- **Network Partition**: split services into groups that cannot communicate, isolate a service from its database, simulate a split-brain scenario.

### Network
- **Latency Injection**: add 10ms, 50ms, 100ms, 500ms, or 2000ms to specific service-to-service calls. Test timeout configuration, retry behavior, circuit breaker thresholds.
- **Packet Loss**: 1%, 5%, 10%, 25% packet loss on specific interfaces. How does TCP congestion control handle it? How do long-lived connections fare?
- **Bandwidth Throttling**: limit bandwidth to 1 Mbps, 100 Kbps. Test streaming, large payload transfers, log shipping.
- **DNS Failure**: drop all DNS queries (simulate DNS server down), introduce 5s DNS resolution delay (simulate slow DNS provider), return NXDOMAIN for specific services.

### Application
- **Dependency Failure**: downstream returns 500s, times out, returns malformed response (corrupt JSON, truncated body, infinite stream). Verify circuit breakers, fallbacks, retry policies.
- **Resource Exhaustion**: CPU spike to 100% on specific pod/container, memory fill to 90%/95% (OOM risk), disk fill to 85%/95%, file descriptor exhaustion (ulimit -n).
- **Connection Pool Exhaustion**: saturate database connection pool, saturate HTTP connection pool, saturate gRPC stream pool.

### Security
- **Credential/Secret Rotation**: rotate credentials while system is running — does the application pick up the new secret without restart? Does it handle auth failures gracefully during rotation?
- **Certificate Expiry Simulation**: present an expired or self-signed TLS certificate. Do health checks catch it? Do clients reject the connection? Does monitoring fire?
- **IAM Permission Revocation**: revoke a service's IAM permissions to access S3, DynamoDB, or KMS. Does the application fail gracefully? Does the error message leak information?

### State
- **Clock Skew**: advance system clock by 30 minutes or 24 hours. Do JWT tokens validate correctly? Do TTL-based caches expire prematurely? Do scheduled jobs fire at unexpected times?
- **Event Ordering Violation**: send messages out-of-order to a queue consumer, send duplicate messages (at-least-once semantics test), send delayed messages exceeding SLA.
- **Data Corruption**: simulate bit flips in cached data, simulate corrupted message payload, simulate partial writes to persistent storage.

## Steady State Hypothesis Deep Dive

A steady state hypothesis is your experiment's null hypothesis. It states: "Under this specific fault, the system will continue to exhibit normal behavior within defined boundaries."

### Metrics to Measure
- **Latency**: P50 (typical user experience), P95 (tail latency), P99 (worst-case user experience). Track the delta from baseline — a 50ms increase at P99 is worth investigating even if absolute values are fine.
- **Error Rate**: total errors / total requests as percentage. Distinguish between client errors (4xx) and server errors (5xx). Monitor by endpoint, by downstream dependency, by status code.
- **Throughput**: requests per second (RPS). Does the system compensate for degraded capacity by shedding load or does it accumulate backlog?
- **Saturation Indicators**: CPU utilization, memory usage, disk I/O, network I/O, connection pool utilization, request queue depth. These leading indicators predict failures before latency or errors spike.

### Control vs Experiment
- Establish steady state baseline by measuring the system WITHOUT fault injection for at least 5 minutes.
- Run experiment WITH fault injection for the planned duration.
- Compare metrics during fault vs baseline. The hypothesis is refuted if any metric exceeds its defined threshold for more than N consecutive seconds.
- Recovery observation: after fault stops, measure how long it takes for all metrics to return to baseline. This is your Mean Time to Recover (MTTR) from that specific failure.

### Writing Good Hypotheses
A good hypothesis is falsifiable, measurable, and bounded:

| Component | Requirement | Example |
|-----------|-------------|---------|
| Fault trigger | Specific | "When 50% of checkout-service pods are terminated..." |
| Measured metric | Quantified | "...checkout latency P99 remains below 500ms..." |
| Threshold | Bounded | "...and checkout error rate stays below 0.5%..." |
| Duration | Time-bound | "...for the entire 5-minute experiment duration." |

### Example Hypotheses
- **Pod termination**: "When 50% of checkout-service pods are terminated, checkout latency P99 remains below 500ms and checkout error rate stays below 0.5%."
- **Network latency**: "When 200ms latency is added to calls from orders-service to payment-service, orders-service latency P95 stays below 1s and no orders are lost."
- **CPU stress**: "When CPU is stressed to 90% on inventory-service pods, inventory lookup latency P99 stays below 2s and throughput drops by no more than 20%."
- **AZ failure**: "When us-east-1a is isolated, all traffic routes to the remaining AZs within 60 seconds, P99 latency stays below 1s during failover, and zero complete request failures occur."

## Blast Radius (Military-Grade Controls)

### Scope Containment Dimensions
- **Traffic percentage**: canary traffic only (1% of users), internal-only traffic, synthetic traffic.
- **Infrastructure scope**: single pod, single node, single AZ, single region.
- **Service scope**: single endpoint, single service, non-critical service only.
- **User segment**: internal users, beta testers, free-tier customers (never enterprise customers if avoidable).
- **Time window**: low-traffic hours only (1–4 AM), weekend windows, never during known campaign/event periods.

### Abort Conditions
Auto-termination triggers (any one fires → experiment stops immediately):
- Error rate exceeds threshold (e.g., 5% increase from baseline over 30 seconds).
- P99 latency > 2x baseline for 60 seconds.
- Production alert fires and is acknowledged.
- Customer-facing impact detected by synthetic monitoring.
- Manual kill switch activated by Commander, Operator, or on-call engineer.

### Progressive Expansion Model
```
Staging (all experiments required to pass)
  → Canary (single instance, internal traffic, 15 min)
    → 1% production traffic (30 min, daytime)
      → 10% production traffic (30 min, daytime)
        → 50% production traffic (60 min, low-traffic window)
          → 100% production traffic (automated, continuous)
```
Each level requires N successful runs at the current level before advancing. N = 3 for infra/network faults, N = 5 for stateful faults.

### Time-Bounded Execution
- Every experiment has a `maxDuration` parameter. Hard stop enforced by tool.
- Auto-terminate if the responsible engineer does not acknowledge a "pre-go" prompt within 2 minutes.
- Default durations: prod experiments 5–15 minutes, staging experiments 10–30 minutes.
- Experiments that exceed their window without explicit extension are forcibly terminated.

## Tooling Deep Dive

### Chaos Mesh
- **Type**: Kubernetes-native, open source (CNCF).
- **Architecture**: Custom Resource Definitions (CRDs) for each fault type. Controller-manager + dashboard + chaos-daemon (runs on each node).
- **Fault Types**: PodChaos (pod kill, container kill), NetworkChaos (latency, loss, partition, bandwidth), StressChaos (CPU, memory), IOChaos (delay, fault), DNSChaos (error, random), TimeChaos (clock skew), HTTPChaos (abort, delay, replace).
- **Strengths**: deep K8s integration, declarative YAML, active community, scheduler (cron-based), web UI, multi-namespace support.
- **Limitations**: K8s-only, learning curve for advanced scenarios, no built-in multi-experiment orchestration.

### Gremlin
- **Type**: SaaS, commercial.
- **Platform**: Kubernetes, VMs, bare metal, containers, AWS, Azure, GCP.
- **Fault Types**: CPU, memory, disk (fill, IO), network (latency, loss, blackhole, DNS), state (time travel, process kill, shutdown).
- **Strengths**: multi-platform, scenario orchestration (run sequential/parallel attacks), web UI, teams/RBAC, halt mechanism, no infrastructure to manage.
- **Limitations**: cost (per-host licensing), vendor lock-in, custom fault types require Gremlin SDK.

### AWS Fault Injection Service (FIS)
- **Type**: AWS-native, pay-per-action.
- **Platform**: EC2, ECS, EKS, RDS, DynamoDB, CloudWatch.
- **Fault Types**: instance termination (EC2, ECS tasks), CPU/network stress, RDS failover, DynamoDB throttle, AZ power loss.
- **Strengths**: IAM integration (blast radius via IAM policies), CloudWatch integration (stop conditions), experiment templates, no infrastructure to manage (within AWS).
- **Limitations**: AWS-only, fewer fault types than Chaos Mesh or Gremlin, no built-in scenario orchestration.

### LitmusChaos
- **Type**: Open source, CNCF project.
- **Platform**: Kubernetes.
- **Fault Types**: pod-kill, container-kill, cpu-hog, memory-hog, network-latency, network-loss, disk-fill, DNS-chaos, node-drain, node-cordon, and 50+ more via ChaosHub.
- **Strengths**: declarative (ChaosEngine CRDs), ChaosHub with community experiments, GitOps-friendly, CI/CD integration (Argo, Jenkins), Litmus Portal for management.
- **Limitations**: K8s-only, less mature than Chaos Mesh in some areas, complex troubleshooting.

### Steadybit
- **Type**: SaaS, modern, commercial.
- **Platform**: Kubernetes, hosts, containers.
- **Fault Types**: network, resource, state, HTTP, K8s, cloud API attacks.
- **Strengths**: application-level fault injection (discovers service dependencies automatically), nice UX, attack scenarios with pre/post conditions, dashboards.
- **Limitations**: cost, smaller community, fewer fault types than Gremlin/Chaos Mesh.

### Comparison Table

| Feature | Chaos Mesh | Gremlin | AWS FIS | LitmusChaos | Steadybit |
|---------|-----------|---------|---------|-------------|-----------|
| Open source | Yes | No | No | Yes | No |
| Kubernetes native | Yes | Yes | Yes | Yes | Yes |
| Multi-platform | No | Yes | AWS only | No | Limited |
| Self-hosted | Yes | No | No | Yes | No |
| SaaS option | No | Yes | Yes | Yes (Portal) | Yes |
| Learning curve | Medium | Low | Medium | Medium | Low |
| Cost | Free | Per host | Per action | Free | Per host |
| Fault types | 8+ categories | 6 categories | 5 categories | 50+ experiments | ~20 types |
| Web UI | Yes | Yes | Yes | Yes | Yes |
| RBAC/Teams | Namespace | Yes | IAM | Yes | Yes |

## Game Days

### Planning (2 Weeks Before)
- **Scope**: define which services, which experiments, what NOT to touch.
- **Experiment selection**: prioritize based on recent incidents, service criticality, untested failure modes, new resilience features deployed.
- **Team assembly**: minimum 3 people — more if multiple services are being tested.
- **Observability setup**: verify dashboards, alerts, logging, and tracing for every service in scope.
- **Stakeholder communication**: notify leadership, support team, adjacent service owners.
- **Schedule**: pick low-traffic window, block 3–4 hours, send calendar invites with explicit "do not schedule over" request.
- **Rollback prep**: verify all abort mechanisms work end-to-end. Document rollback steps for each experiment.
- **Dry run**: run through each experiment in staging at least once. Fix everything that breaks before GameDay.

### Roles
- **Commander** (leads, decides abort/continue): owns the timeline, makes abort decisions, manages communications. Not hands-on with tooling.
- **Operator** (runs experiments, executes commands): runs fault injection, monitors execution, stops experiments on command.
- **Observer** (monitors, analyzes, diagnoses): watches dashboards, metrics, logs. Analyzes impact in real time. The person who says "I see something."
- **Scribe** (documents everything, time-stamps): records experiment start, fault injection, observed impact, recovery, and every decision. Writes the after-action report.

### Execution Timeline (3.5 Hour Example)
| Time | Activity | Duration |
|------|----------|----------|
| 9:00–9:15 | Briefing — review experiments, roles, abort conditions, communication channel | 15 min |
| 9:15–10:00 | Experiment 1 (pod termination) — inject, observe, record, abort if needed | 45 min |
| 10:00–10:15 | Break + quick huddle — share findings from experiment 1 | 15 min |
| 10:15–11:00 | Experiment 2 (network latency) — inject, observe, record | 45 min |
| 11:00–11:15 | Break | 15 min |
| 11:15–12:00 | Experiment 3 (dependency failure) — inject, observe, record | 45 min |
| 12:00–12:30 | Debrief — what we found, what worked, what broke, action items | 30 min |

### Communication During GameDay
- **Pre-GameDay Slack message**: "@channel Chaos GameDay begins at 9:00 AM PT. We'll be running experiments in [services] with blast radius limited to [scope]. Abort conditions: [thresholds]. Watch #chaos-gameday for updates."
- **Experiment start**: "Starting Experiment 1: pod termination on checkout-service. Blast radius: 2 pods in us-east-1a. Expected impact: none."
- **Experiment abort**: "ABORTING Experiment 2. Error rate on orders-service exceeded 5%. Returning to normal. All faults stopped."
- **Experiment success**: "Experiment 3 complete. Hypothesis confirmed. P99 latency stayed below 400ms, error rate 0.0%. 5 min recovery time to baseline."
- **Debrief follow-up**: "GameDay complete. Full report by EOD Friday. Action items tracked in [link to tickets]. Thanks team!"

### Debrief Format
1. **Experiment summary**: name, hypothesis, verdict (confirmed / refuted / inconclusive).
2. **What worked**: resilience patterns that performed as expected, observability that caught the fault, team communication.
3. **What broke**: failures we didn't expect, resilience patterns that didn't engage, observability gaps.
4. **What we learned**: surprising behaviors, new failure modes discovered, insights for architecture.
5. **Action items**: owner, ticket number, severity, due date. Each item is concrete and trackable.

### Post-GameDay (Within 1 Week)
- **Findings report**: compiled from Scribe's notes, Observer's analysis, Commander's debrief.
- **Action item tracking**: create tickets with severity (P0 = critical, fix immediately), owner, and due date.
- **Leadership summary**: 1-page executive summary covering objectives, key findings, action items, go-forward plan.
- **Retro** on the GameDay itself: what went well, what to improve for next time (tooling, communication, timing, scope).
- **Experiment catalog update**: mark experiments as tested, update findings, add new experiments inspired by GameDay insights.

## CI/CD Integration for Chaos

### Pipeline Integration
Run chaos experiments in staging on every merge to main — catch resilience regressions like we catch functional bugs.

```yaml
# Example GitHub Actions + LitmusChaos integration
chaos-tests:
  runs-on: ubuntu-latest
  steps:
    - name: Install LitmusChaos
      run: kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator.yaml
    - name: Run chaos experiments
      run: |
        kubectl apply -f experiments/pod-kill.yaml
        kubectl wait --for=condition=Completed chaosengine/pod-kill --timeout=300s
    - name: Check experiment result
      run: kubectl get chaosresult pod-kill -o jsonpath='{.status.experimentStatus.verdict}'
```


**What good looks like:** Chaos experiment catalog with 10+ experiments covering different fault types. GameDay completed in the last 30 days with documented findings. Blast radius controls tested and verified. Resilience score for each service tracked over time.

### SLO-Based Experiment Gating
Only run chaos experiments if error budget is healthy:
- Check SLO burn rate. If error budget burn rate > 2 for the current window, skip chaos experiments.
- Only run experiments on services with sufficient error budget (>50% remaining).
- If an experiment consumes error budget, account for it: chaos experiments consume error budget.

### Error Budget Integration
- Chaos experiments are not free — they consume error budget (artificially by injecting failures).
- Define a chaos budget as a fraction of total error budget (e.g., 5% of error budget reserved for chaos).
- If chaos budget is depleted, pause ALL experiments until next window.
- Automate: link chaos experiment results to SLO dashboards. If an experiment causes an SLO violation, that's data, not failure — but track it.

## Organization Maturity Model

| Level | Name | Characteristics |
|-------|------|----------------|
| 1 | Crawl | GameDays in staging only. No automation. Quarterly cadence. Experiments are manual. No blast radius controls beyond manual stop. |
| 2 | Walk | GameDays in production (limited blast radius, canary only). Some automated experiments in staging. Observability validated before each experiment. Monthly cadence. |
| 3 | Run | Automated chaos in staging CI (every merge). Scheduled production experiments (weekly). Resilience scoring per service. Blast radius controls automated (auto-abort). |
| 4 | Fly | Continuous chaos in production (low-intensity). Experiments gated by error budgets. SLO-based experimentation (experiments auto-stop when SLO risk detected). Self-healing verification. Resilience score as a release gate. |

## Observability for Chaos

### Golden Rule
Before running ANY experiment, verify: you can detect the failure you're about to inject. If you can't see it in your dashboards, your alerts, and your logs — **fix observability first**.

### Pre-Experiment Observability Check
1. Inject the fault in staging (1 pod, 30 seconds).
2. Check: does your latency dashboard show the spike?
3. Check: does your error rate dashboard show the increase?
4. Check: does your saturation dashboard show the resource constraint?
5. Check: do your logs contain the error (with correlation ID)?
6. Check: does your alert fire within the expected time window?
7. If ANY of these fail → STOP. Fix the observability gap. Document it. Re-test.

### Running Chaos Without Observability Is Just Breaking Things
- Without observability, you cannot confirm the hypothesis.
- Without observability, you cannot detect blast radius escape.
- Without observability, you cannot learn from the experiment.
- Without observability, you cannot prove the value of chaos engineering to leadership.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Chaos engineering is inherently cross-team — you break things that other teams built and own. Without coordination, chaos experiments are indistinguishable from attacks or accidents.

### Decision Gates & Artifacts

- **Gate 1 — Observability Verified:** Chaos experiments require existing dashboards and alerts from `observability-engineer`. Without them, experiments are just breaking things. Artifact: observability health check report.
- **Gate 2 — SLOs Defined:** Steady state hypotheses depend on SLO definitions and error budgets established by `site-reliability-engineer`. Artifact: SLO threshold document per service.
- **Gate 3 — Infrastructure Ready:** Experiment execution environments and blast radius controls depend on infrastructure provisioned by `devops-engineer`. Artifact: environment readiness checklist.
- **Gate 4 — Runbook Validated:** Incident response playbooks validated in coordination with `incident-responder` before production experiments. Artifact: signed-off runbook validation report.
- **Artifact:** GameDay report (findings, action items, owners), resilience score per service, blast radius containment verification.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **DevOps / SRE** | Experiment execution, blast radius control, monitoring during experiments | Experiment schedule, injection method, abort conditions, observability dashboard |
| **Backend Developers (Service Owners)** | Service-level experiments, fault injection in specific services | Service architecture, known failure modes, recovery time expectations |
| **Security Reviewer** | Security-relevant experiments (network segmentation, auth failures) | Experiment boundaries, security control bypass risks, incident response awareness |
| **System Architect** | Cross-service experiments, cascade failure testing, resilience patterns | Service dependency graph, circuit breaker locations, bulkhead boundaries |
| **Incident Responder / On-Call** | ALL experiment windows — must know experiments are running | Experiment schedule, expected symptoms, abort command, contact for false alarm |
| **QA Engineer** | Pre-production chaos experiments, resilience test integration | Test environment setup, experiment scenarios, expected recovery behavior |
| **Project Manager** | Experiment scheduling, GameDay planning, stakeholder communication | Experiment calendar, production freeze windows, team availability |
| **CTO Advisor** | First-time production chaos experiments, high-risk experiments | Risk acceptance, blast radius approval, executive awareness |
| **Product Strategist** | User-impacting experiments, degraded mode UX testing | Expected user experience during failure, graceful degradation expectations |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Chaos experiment scheduled in production (>24 hours notice minimum) | On-Call, DevOps, Service Owners, Project Manager | All stakeholders aware; avoid confusion with real incidents |
| Experiment about to begin (5-minute warning) | On-Call, DevOps, Service Owners | Final confirmation; abort if any stakeholder objects |
| Experiment exceeds blast radius (affects unexpected services) | On-Call, DevOps, Service Owners | Abort immediately; blast radius containment failed |
| Real incident occurs during experiment | On-Call, Incident Commander, All Stakeholders | Abort experiment NOW; real incident takes priority |
| Experiment reveals critical vulnerability (system did not recover) | System Architect, Service Owners, CTO Advisor | Resilience gap discovered; remediation prioritization required |
| GameDay scheduled (cross-team resilience exercise) | All Engineering Teams, Project Manager, CTO Advisor | Full organization awareness; schedule around releases and PTO |
| Experiment results published (post-experiment report) | All Stakeholders, CTO Advisor | Learnings shared; resilience improvements prioritized |
| Circuit breaker or timeout configuration found inadequate during experiment | System Architect, Service Owners | Configuration change needed; deployment required |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Chaos experiment causes production incident (real user impact) | **Incident Commander** + CTO Advisor + VP Engineering | Abort experiment; SEV-level incident response; postmortem required |
| Experiment reveals systemic failure pattern (multiple services fail same way) | **System Architect** + CTO Advisor | Architecture resilience gap; may require significant re-architecture |
| Service owner refuses to participate in chaos experiments for >2 quarters | **CTO Advisor** + VP Engineering | Resilience culture gap; executive sponsorship needed |
| Blast radius control mechanism itself fails (experiment cannot be aborted) | **CTO Advisor** + DevOps Lead | Safety mechanism failure; halt all experiments until fixed |
| Production chaos experiment proposed for first time | **CTO Advisor** + VP Engineering | Organizational risk decision; executive approval required |


## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `Error: admission webhook.*denied\|chaos-mesh.*forbidden` + `kubectl auth can-i create chaosengine --as=system:serviceaccount:chaos-testing:chaos-operator -n chaos-testing` returns `no` | Chaos experiment stuck in `Pending` — never starts injecting faults | RBAC misconfiguration: the chaos operator service account lacks permissions to create/mutate pods, network policies, or stress processes in the target namespace | Grant RBAC: `kubectl create clusterrole chaos-operator --verb=create,delete,get,list,patch,update,watch --resource=pods,networkpolicies,stresschaos`. Bind to service account. Verify: `kubectl auth can-i create podchaos --as=system:serviceaccount:chaos-testing:chaos-operator` | 1. Check experiment status: `kubectl get chaosengine -n chaos-testing -o yaml \| grep -A5 "status:"` 2. Audit RBAC: `kubectl auth can-i --list --as=system:serviceaccount:chaos-testing:chaos-operator` 3. Apply missing permissions from chaos-mesh RBAC template: `kubectl apply -f https://raw.githubusercontent.com/chaos-mesh/chaos-mesh/master/helm/chaos-mesh/templates/rbac.yaml` 4. Re-run: `kubectl apply -f experiment.yaml && kubectl wait --for=condition=Completed chaosengine/experiment --timeout=120s` |
| `Error: chaos-daemon.*connection refused\|chaos-daemon.*dial unix.*connect: no such file` + `kubectl get pods -n chaos-testing -l app.kubernetes.io/component=chaos-daemon` shows 0/1 Ready | Fault injection targets available but daemon can't communicate with chaos-daemon sidecar on target node | Chaos daemon pod not running on target node — daemonset not scheduled or crashlooping. Chaos-mesh uses per-node daemon for fault injection; without it, no faults can be injected | Check daemonset: `kubectl get ds -n chaos-testing chaos-daemon`. Check tolerations match node taints. Verify host PID namespace: `kubectl get pod <chaos-daemon> -o yaml \| grep hostPID`. Restart daemonset if stuck: `kubectl rollout restart ds/chaos-daemon -n chaos-testing` | 1. Verify daemonset coverage: `kubectl get pods -n chaos-testing -l app.kubernetes.io/component=chaos-daemon -o wide \| grep <target-node>` 2. Check daemon logs: `kubectl logs -n chaos-testing ds/chaos-daemon --tail=50` 3. Verify hostPID=true: `kubectl get ds chaos-daemon -n chaos-testing -o yaml \| grep -A1 hostPID` 4. If missing, patch: `kubectl patch ds chaos-daemon -n chaos-testing -p '{"spec":{"template":{"spec":{"hostPID":true}}}}'` |
| `Error: cannot delete pod.*statefulset\|pod terminated but rebuilt instantly\|replicaset rescaled` + `grep -rn "replicas:" deployment/ -A2` shows replicas=3 | Pod kill experiment runs but service doesn't degrade — StatefulSet controller or HPA immediately recreates pods faster than fault can cause impact | Chaos experiment targeting the wrong layer — killing Pods in a StatefulSet/ReplicaSet with 3+ replicas is absorbed by the controller before any user impact is felt. The experiment proves controller resilience, not service resilience | Reduce replica count during experiment OR target the service endpoint directly. Better: inject latency/errors at the application layer instead of killing infrastructure. Use `NetworkChaos` (latency injection) or `HTTPChaos` (error injection) for realistic failure simulation | 1. Verify target is correct: `kubectl get deployment <svc> -o yaml \| grep replicas` 2. If replicas > 1, switch to application-layer fault: `kind: HTTPChaos` with `abort: true` or `delay: 5000ms` 3. If must use PodChaos, set `mode: all` OR temporarily scale down: `kubectl scale deployment <svc> --replicas=1` before experiment 4. Re-verify: `kubectl get chaosengine -o yaml \| grep -A10 "status:"` — must show `injection-affected` > 0 |
| `Error: experiment duration exceeded\|chaos-engine timeout\|context deadline exceeded` + `grep -rn "duration:" experiment.yaml` shows duration: 600s | Experiment ran for 10 minutes but never completed — steady-state check failed to detect recovery; experiment timed out waiting for system to return to baseline | The steady-state hypothesis was too strict — requiring P99 < 50ms when baseline was 45ms. Natural variance caused the check to fail repeatedly, keeping the experiment running until timeout | Relax hypothesis thresholds: use P95 instead of P99, allow ±10% variance from baseline. Set `duration` to be the minimum needed to observe behavior (60-120s for infra faults, 300s for stateful). Always include a hard `deadline` in experiment spec | 1. Check why experiment didn't complete: `kubectl describe chaosengine <name> -n chaos-testing \| grep -A20 "Events:"` 2. Review hypothesis: `grep -A10 "steadyState\|hypothesis" experiment.yaml` 3. Adjust thresholds: widen from baseline ±5% to ±15%, use P95 instead of P99 4. Set deadline: `duration: 120s` with `spec.scheduler.cron: ""` (one-shot) 5. Re-run with shorter duration: `kubectl apply -f experiment.yaml && kubectl wait --for=condition=Completed --timeout=180s chaosengine/<name>` |
| `Error: cannot list resource.*nodes.*cluster scope\|nodes is forbidden` + `kubectl get nodes` succeeds but chaos operator can't access node-level resources | AZ failure or node-level chaos experiment fails — chaos operator has namespace-scoped RBAC but target is cluster-scoped (nodes, persistentvolumes) | Chaos operator was granted namespace-scoped Role instead of ClusterRole. Node-level faults (kernel panic, disk failure, AZ partition) require cluster-scoped permissions | Grant ClusterRole: `kubectl create clusterrole chaos-node-access --verb=get,list,watch,update,patch --resource=nodes`. Bind: `kubectl create clusterrolebinding chaos-node --clusterrole=chaos-node-access --serviceaccount=chaos-testing:chaos-operator` | 1. Verify permission scope: `kubectl auth can-i get nodes --as=system:serviceaccount:chaos-testing:chaos-operator` 2. If `no`, check current bindings: `kubectl get clusterrolebinding -o yaml \| grep chaos-operator` 3. Apply cluster-scoped RBAC from chaos-mesh docs 4. Test with dry-run: `kubectl apply -f node-chaos.yaml --dry-run=client` 5. Apply and verify: `kubectl apply -f node-chaos.yaml && kubectl get chaosengine -o yaml \| grep "status:.*Running"` |
| `Error: failed to apply tc rules\|tc: command not found\|network chaos daemon not ready` + `kubectl logs -n chaos-testing ds/chaos-daemon \| grep -i "tc\|traffic.control\|iptables"` | NetworkChaos (latency/loss) experiment runs but has no observable effect — `curl` from test pod still shows <1ms latency when 500ms was injected | Target pod is not in the same network namespace as the chaos-daemon. The daemon uses `tc` (traffic control) on the pod's network interface, but if the pod uses `hostNetwork: true` or a CNI plugin that bypasses tc, no traffic is affected | Verify pod network mode: `kubectl get pod <target> -o yaml \| grep hostNetwork`. If `hostNetwork: true`, target the node instead of the pod. For CNI issues, switch to `kind: HTTPChaos` or `kind: DNSChaos` which work at application layer. Use `iptables`-based injection as fallback | 1. Check network mode: `kubectl get pod <target> -o yaml \| grep -E "hostNetwork\|hostPID"` 2. Test network chaos from sidecar: `kubectl exec -n chaos-testing <chaos-daemon> -- tc qdisc show dev eth0` 3. From target pod: `kubectl exec <target> -- ping -c5 <other-pod>` — baseline latency 4. Inject latency: `kubectl apply -f network-delay.yaml` 5. Re-ping: `kubectl exec <target> -- ping -c5 <other-pod>` — must show increased latency 6. If no effect, switch to DNS chaos: `kind: DNSChaos` with `patterns: [{name: "svc.cluster.local", type: "error"}]`

## Proactive Triggers
<!-- QUICK: 30s — when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| GameDay exercise completed with severity findings | CTO Advisor, VP Engineering, All Service Owners | Resilience gaps discovered; prioritization needed for remediation tickets |
| Chaos experiment reveals circuit breaker misconfiguration | System Architect, Service Owners | Circuit breaker not activating; configuration fix needed before next incident |
| Blast radius containment breach during automated experiment | DevOps Lead, On-Call, Security Reviewer | Containment mechanism failure; halt all automated experiments until root cause fixed |
| Experiment results show MTTR exceeds SLO by >2x | Service Owners, SRE, CTO Advisor | Recovery time unacceptable; architectural or procedural changes needed |
| New service onboarded without chaos experiment coverage | Service Owner, DevOps | Resilience blind spot; experiment design and scheduling needed |
| Chaos tooling license exceeds quarterly budget by >20% | CTO Advisor, Finance | Budget reallocation or tooling evaluation needed |
| Steady state hypothesis invalidated by infrastructure change | Service Owners, DevOps | Baseline metrics shifted; hypothesis rewrite and experiment revalidation required |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Chaos tooling deployed and operator running — Chaos Mesh, Litmus, or Gremlin agent active on all target nodes | `kubectl get pods -n chaos-testing -l app.kubernetes.io/component=chaos-daemon -o json \| jq '.items \| length'` → must equal `kubectl get nodes --no-headers \| wc -l` | Helm: `helm upgrade --install chaos-mesh chaos-mesh/chaos-mesh -n chaos-testing --create-namespace --set chaosDaemon.runtime=containerd` |
| **[S2]** | RBAC scoped correctly — chaos operator has namespace-limited permissions, not cluster-admin | `kubectl auth can-i --list --as=system:serviceaccount:chaos-testing:chaos-operator \| grep -E "\[\*\]" \| wc -l` → must be 0 (no wildcard permissions) | Apply scoped RBAC: `kubectl create role chaos-operator -n chaos-testing --verb=get,list,create,delete,patch --resource=pods,networkpolicies,stresschaos` |
| **[S3]** | Kill switch tested: abort all active experiments within 30 seconds | `time kubectl delete chaosengine --all -n chaos-testing && kubectl wait --for=delete chaosengine --all -n chaos-testing --timeout=30s` → must complete < 30s | Shell alias: `alias chaos-stop='kubectl delete chaosengine --all -n chaos-testing --grace-period=0 --force'` |
| **[S4]** | Steady-state hypothesis defined for target service with measurable numeric thresholds | `grep -c "P99\|P95\|error_rate\|throughput\|latency" experiment.yaml` → must be ≥ 3 (three distinct metrics) | Template: copy `templates/steady-state-hypothesis.yaml` into experiment spec with P50/P95/P99, error rate %, throughput req/s |
| **[S5]** | Abort conditions defined with numeric thresholds (error rate > X%, latency > Yms, duration > Zs) | `grep -E "[0-9]+%\|[0-9]+ms\|[0-9]+[sm]" experiment.yaml \| wc -l` → must be ≥ 2 | Insert abort block: `spec.abortConditions: [{metric: "error_rate", threshold: "5%", duration: "30s"}]` |
| **[S6]** | Blast radius scoped explicitly — namespace, label selector, percentage, NOT wildcard | `grep -E "namespace:.*\*\|selector:.*\{\}\|percent:.*100\|mode:.*all" experiment.yaml` → must return 0 matches | Set label selector: `selector: {namespaces: ["chaos-testing"], labelSelectors: {app: "target-svc"}}` and `mode: "one"` or `mode: "fixed-percent", value: "10"` |
| **[S7]** | Pre-experiment observability verified — dashboards show service metrics, alerts configured | `curl -s http://prometheus:9090/api/v1/query?query=up{job="target-svc"} \| jq '.data.result[0].value[1]'` → must return `"1"` | Run pre-flight: `scripts/chaos-preflight.sh <service> <namespace>` — checks dashboard, alerts, metrics endpoint, logs |
| **[S8]** | GameDay playbook documented with roles, timeline, communication plan, and abort procedure | `grep -c "role:\|timeline:\|communication:\|abort:" game-day-playbook.md` → must be ≥ 4 | Copy and customize: `templates/game-day-playbook.md` with specific service names, on-call contacts, dashboard URLs |
| **[S9]** | At least one chaos experiment passes in staging CI on every merge to main | `kubectl get chaosengine -n staging -o json \| jq '[.items[] \| select(.status.conditions[0].type=="Completed")] \| length'` → must be > 0 for last 24h | GitHub Actions: `.github/workflows/chaos-staging.yml` — runs `kubectl apply -f experiments/ && scripts/wait-for-completion.sh` |
| **[S10]** | Experiment rollback tested in staging — fault injected, then aborted within 60s, system returns to baseline | `scripts/chaos-rollback-test.sh <experiment>.yaml staging` → exit code 0 and all metrics within baseline ±10% | Script: inject fault → wait 30s → abort → wait 30s → query Prometheus for P95 comparison → pass/fail |
| **[S11]** | Chaos experiment catalog maintained with status per experiment (designed → tested-staging → tested-prod → automated) | `grep -c "status:.*tested-prod" experiments/catalog.yaml` → must be ≥ 1 (at least one prod-verified experiment) | Catalog script: `scripts/catalog-status.sh` — reads `experiments/catalog.yaml`, outputs JSON with status counts |
| **[S12]** | Experiment results tracked — MTTR per failure mode measured, resilience score computed per service | `curl -s http://chaos-dashboard:8080/api/resilience-scores \| jq '.[] \| select(.score < 70)'` → must return 0 services below 70% | Dashboard: deploy `chaos-dashboard` with Prometheus metrics → compute score = (1 - MTTR/SLO) × 100 per service |

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person) → Small (2-10) → Medium (10-50) → Enterprise (50+)

| Phase | Team Size | Priority | Chaos Engineering Approach |
|-------|-----------|----------|---------------------------|
| **Solo/MVP** | 1-3 devs | Ship. Don't break what ships. | No chaos engineering. Manual: kill a pod in staging, see what happens. Fix obvious failures (no health checks, no retries). "Resilience awareness," not chaos engineering. |
| **Small/Growth** | 3-15 devs, 1 infra/SRE | Don't lose customers to preventable failures | First GameDay in staging (half-day). Test: pod kill, DB failure, disk exhaustion. Implement circuit breakers, retries, health checks. Quarterly GameDays. |
| **Medium** | 15-50 devs, dedicated SRE | Resilience as measurable KPI | Automated chaos in staging CI (every merge). Monthly production GameDays. Resilience scoring per service. Full fault injection catalog. Blast radius auto-controls. |
| **Enterprise** | 50+ devs, chaos/SRE team | Continuous confidence | Continuous production chaos (low-intensity). SLO-gated experiments. Multi-region failover testing. Self-healing verification. Resilience score as release gate. Chaos budget integrated into error budgets. |

### Transition Triggers

| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | First paying customer or first production incident | Add health checks + retries. Run one staging GameDay. Document 3 known failure modes. |
| Small → Medium | >3 production incidents in 6 months OR >10 services | Automate chaos in CI. Add resilience scoring. Run monthly production GameDays. Hire/assign dedicated SRE. |
| Medium → Enterprise | Multi-region deployment OR compliance requires DR testing | Continuous production chaos. SLO-gated experiments. Multi-region failover drills. Full-time chaos engineering team. |

**Solo rule:** Chaos engineering for a startup with 10 users on a single EC2 instance is theater. Before injecting faults, ensure: (a) health checks, (b) process monitoring, (c) tested backups. That's 90% of resilience for 10% of the effort.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Never run your first chaos experiment in production:** Always staging first. Production readiness requires staging GameDay with clear learnings and proven abort mechanisms.
2. **Verify observability before every experiment:** Inject the fault in staging for 30 seconds. If you can't see it on dashboards within 2 minutes, fix observability before proceeding — running chaos without observability is just breaking things.
3. **Start with the smallest possible blast radius:** Single pod, 1% traffic, 5-minute window. Expand only after N successful runs (N=3 for infra faults, N=5 for stateful faults).
4. **Define abort conditions with specific numeric thresholds:** "Error rate > 5% for 30 seconds" not "if things look bad." Auto-termination must be tool-enforced, not human-dependent.
5. **Test failures you've actually experienced first:** Prioritize experiments based on real postmortems, not hypothetical scenarios. The best failure mode to test is the one that already caused an incident.
6. **Run experiments during low-traffic windows with on-call aware:** Schedule experiments 1-4 AM or weekends. Notify on-call 24+ hours in advance with expected symptoms and abort command.
7. **Every experiment needs a documented rollback:** One command, one feature flag flip, one script — tested in staging before production. If rollback fails, you have a production incident.
8. **Track MTTR per failure mode:** Recovery time is as important as resilience. If the system recovers in 30 seconds vs 5 minutes, that difference matters to users.
9. **Integrate chaos into CI/CD:** Run automated experiments on every merge to main in staging. Catch resilience regressions like functional bugs — before they reach production.
10. **GameDay debrief must produce tracked action items:** Every finding gets an owner, severity, ticket number, and due date. Learning without action is wasted effort.

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Running chaos experiments only before big launches — panic-driven chaos produces rushed experiments with no rollback plan | Schedule experiments continuously on a calendar. Decouple experiments from release anxiety. Run weekly low-intensity chaos in staging CI. | `grep -rn "chaos\|gameday\|experiment" .github/workflows/ --include="*.yml" \| wc -l` → if 0, no CI-integrated chaos | GitHub Actions schedule trigger: `.github/workflows/chaos-weekly.yml` with `schedule: [{cron: "0 4 * * 3"}]` (Wed 4 AM) running baseline chaos in staging |
| Injecting all faults at once ("kitchen sink") — cannot isolate which fault caused the failure | Inject exactly one fault per experiment. Understand single-fault behavior before combining. Run 3+ successful single-fault experiments before multi-fault. | `grep -c "kind:" experiment.yaml` → if > 1, multiple fault types in one experiment | Pre-commit hook: `scripts/validate-experiment.sh` — fails if `grep -c "kind:" $1` returns > 1 |
| Disabling monitoring during experiments to avoid alert fatigue | Tag experiments for alert deduplication. Fix gaps in observability. Never silence alerts — route them to the experiment channel instead. | `grep -rn "silence\|mute\|suppress\|maintenance.mode" --include="*.yaml" --include="*.yml" experiment-config/` → finds alert-suppression configs | AlertManager rule: route chaos-tagged alerts to `#chaos-experiments` Slack channel with `severity: warning` label, not `severity: critical` |
| Skipping the GameDay retrospective because "we learned enough during the exercise" | Require a written retro with owner, severity, and ticket number for every finding within 48 hours. Template: `templates/gameday-retro.md`. | `grep -rn "retro\|postmortem\|post-game" gameday/ --include="*.md" \| wc -l` → if 0, retro not written | GitHub Actions: 48h after GameDay, check for retro PR; if none, auto-create issue: `gh issue create --title "GameDay retro missing" --body "48h post-GameDay, no retro found"` |
| Running experiments without notifying on-call — on-call declares SEV-1 for a chaos experiment | Notify on-call 24+ hours in advance with expected symptoms, dashboard links, and abort command. Send reminder 1h before experiment. | `grep -rn "on-call\|oncall\|notify\|escalation" experiment.yaml game-day-playbook.md \| wc -l` → if 0, no on-call notification plan | Pre-experiment script: `scripts/notify-oncall.sh` — queries PagerDuty/Opsgenie for current on-call, sends Slack/email with experiment details and abort command |
| Testing only infrastructure faults (pod kill, network) — application-level failures cause more incidents | Expand catalog to include application faults: latency injection, malformed responses, config rollbacks, error injection at the HTTP/API layer. | `grep -E "kind:\s*(PodChaos\|NetworkChaos\|StressChaos\|IOChaos)" experiments/catalog.yaml \| wc -l` vs `grep -E "kind:\s*(HTTPChaos\|DNSChaos\|JVMChaos)" experiments/catalog.yaml \| wc -l` → ratio of infra:app faults should be < 3:1 | Catalog template: `templates/experiment-catalog.yaml` — pre-populated with 42 experiments split 50/50 between infra and application faults |
| Treating chaos engineering as a one-time certification — resilience decays as code changes | Automate experiments in CI/CD. Rerun on every deploy. Treat resilience as continuous verification, not a checkpoint. | `grep -rn "chaos\|experiment" .github/workflows/ci.yml --include="*.yml" \| wc -l` → if 0, chaos not in CI pipeline. `grep -rn "chaos\|experiment" .github/workflows/deploy.yml` → if 0, not in deploy pipeline | CI integration: add `chaos-staging` job to `.github/workflows/ci.yml` that runs `make chaos-test` after deploy job. Deploy gate: `chaos-approval` environment with required reviewer before production chaos. |
| Gamifying chaos with "who broke production" culture — blame culture suppresses reporting | Frame experiments as learning opportunities. Celebrate findings, not blame. Leaderboards track MTTR improvement, not "who caused incidents." | `grep -rn "blame\|fault\|who.broke\|you.broke" --include="*.md" --include="*.yaml" gameday/ experiment-config/` → must return 0 matches | Dashboard: display "Resilience Improvement" leaderboard — most improved P95 latency during chaos, fastest MTTR, most gameday findings remediated — never "most experiments passed" |

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Chaos tooling | Chaos Mesh (free OSS, K8s) or LitmusChaos (free OSS, CNCF) | Gremlin ($100/mo) or Steadybit ($500/mo) | Non-K8s infrastructure, SaaS preference, or need managed experiment library |
| Fault injection (no K8s) | Custom scripts: `kill`, `tc` (traffic control), `stress-ng` (free) | AWS FIS (pay-per-experiment) or Gremlin | Multi-service coordinated experiments or need blast-radius controls via IAM |
| GameDay facilitation | Miro free (3 boards) + Google Meet + manual tracking | Dedicated GameDay tooling | >2 GameDays/year or need structured experiment tracking and reporting |
| Circuit breaker | Resilience4j (Java, free), Polly (.NET, free), opossum (Node.js, free) | Service mesh (Istio/Linkerd, operational cost) | Already running a service mesh or need language-agnostic circuit breaking |
| Observability for chaos | Prometheus + Grafana (free) + structured logging | Datadog/Honeycomb (paid) | Already have paid APM; use existing observability for chaos experiments |

**Annual chaos tool budget by phase:** MVP: $0 (don't do it). Growth: $0-3K (OSS + GameDay facilitation). Scale: $5K-50K (managed chaos platforms + SRE time).

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Baseline
**Input:** Service name, environment (staging/prod), observability dashboards.  
**Steps:** 1) Collect P50/P95/P99 latency, error rate, throughput for 5+ minutes under normal load. 2) Verify all dashboards, alerts, and logs show the service clearly. 3) Record baseline metrics as JSON artifact.  
**Output:** Baseline metrics file + observability verification checklist passed.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Hypothesis & Experiment Design
**Input:** Baseline metrics, failure mode catalog (42 experiments in references).  
**Steps:** 1) Select one failure mode (e.g., pod kill, network latency). 2) Write falsifiable hypothesis: "When X happens, Y metric stays below Z for T minutes." 3) Define blast radius (traffic %, pods, AZ, time window). 4) Set abort conditions with specific numeric thresholds.  
**Output:** Experiment document with hypothesis, blast radius, abort triggers, rollback steps.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Staging Validation
**Input:** Experiment document, staging environment, chaos tooling access.  
**Steps:** 1) Run experiment in staging at full blast radius. 2) Verify steady state hypothesis holds. 3) Confirm observability detects the fault within 2 minutes. 4) Test abort mechanism — stop experiment, verify recovery. 5) If hypothesis refuted, fix the gap and re-run.  
**Output:** Staging validation report — passed/failed, MTTR measured, gaps documented.

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Progressive Production Rollout
**Input:** Staging validation passed, production access, on-call notified.  
**Steps:** 1) Canary: single pod/internal traffic, 15 minutes. 2) 1% traffic, 30 minutes. 3) 10% traffic, 30 minutes. 4) Full scope (if applicable). At each step: monitor abort triggers, compare metrics to baseline.  
**Output:** Production experiment results — hypothesis verdict, blast radius respected, MTTR measured.

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Analysis & Remediation
**Input:** Experiment results, Scribe notes, Observer analysis.  
**Steps:** 1) Document: what worked, what broke, what surprised us. 2) Create action items with owner + severity + due date. 3) Update experiment catalog status (designed → tested-staging → tested-prod → automated). 4) Share findings with service owners and leadership.  
**Output:** After-action report, tracked action items, updated experiment catalog.

## When NOT to Use This Skill (Overkill)

- **Pre-launch startup with <1K users and single server**: You don't need chaos engineering. You need: a process monitor, automated restarts, and daily backups. Fix that first.
- **No observability in place**: "We're going to inject faults to see what happens, but we have no way to observe the impact." This is not chaos engineering; it's vandalism. Observability first.
- **No resilience patterns implemented**: Injecting a pod kill when you don't have health checks, retries, or circuit breakers just proves you have no resilience. You already know that. Build resilience first, then verify.
- **Your system is 100% serverless (Lambda, Cloud Run, no long-running processes)**: Many chaos experiments assume long-running processes. Serverless platforms handle pod kills natively. Focus on: timeout configs, cold start latency, downstream dependency failures.
- **Non-critical internal tool used by 10 people**: If the tool being down for 1 hour is acceptable, chaos engineering ROI is negative. Invest in other areas.

## Token-Efficient Workflow

```
# Step 1: Resilience baseline
python3 scripts/resilience_check.py --service checkout --output json
# Returns: {"health_checks": true, "retries": true, "circuit_breaker": false,
#           "timeout_ms": 5000, "replicas_min": 2, "chaos_ready": false}

# Step 2: Decision tree
# health_checks == false → ADD FIRST. This is table stakes.
# circuit_breaker == false → Implement for all external dependencies.
# replicas_min < 2 → Single point of failure. Add replica before testing pod kills.

# Step 3: Run a single chaos experiment (staging first)
kubectl apply -f experiments/pod-kill-checkout.yaml
# Experiment: kill 1 pod every 60s for 5 min. Verify: availability, latency, error rate.

# Step 4: Verify steady state
python3 scripts/verify_steady_state.py \
  --service checkout --p95-threshold 500 --error-threshold 0.01 --duration 300
# Exit code 0 = steady state maintained during chaos, 1 = hypothesis refuted
```

**Principle:** `resilience_check.py` inspects K8s/consul config, outputs JSON with binary readiness. Agent follows decision tree to exactly one gap. Experiment runs via `kubectl apply`. Steady state verification is exit-code-based.

## What Good Looks Like

The system fails gracefully. Chaos experiments run in production without customer impact. Every team knows their blast radius and practices recovery regularly. When real incidents happen, they're boring — because the team has already practiced the response.

## Footguns
<!-- DEEP: 10+min — war stories from chaos engineering in production -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| First chaos experiment was a Chaos Monkey run at 2 PM on Black Friday — terminated 30% of checkout service instances, auto-scaling had been disabled during a cost-saving initiative, checkout was down for 22 minutes, $180K revenue lost | An e-commerce platform adopted chaos engineering in November 2023. The new chaos engineer, eager to demonstrate value, ran Chaos Monkey against the checkout service at 2 PM on Black Friday — the highest-traffic hour of the year. They assumed auto-scaling would replace terminated instances within 60 seconds. Unbeknownst to them, the infrastructure team had disabled aggressive auto-scaling on November 1 as a cost-saving measure for the holiday period. 30% of instances were terminated and not replaced for 22 minutes. The incident was escalated to the CEO. Chaos engineering was banned for 18 months. | The engineer ran an experiment without understanding the system's current configuration. The steady state wasn't validated before the experiment. There was no blast radius control, no business-hours-only policy, and no approval process. The "start small" principle was ignored — this was a maximum-impact experiment as a first run. | **Never run a first experiment in production without verifying the safety mechanisms first.** Before any production chaos: (1) validate that auto-scaling, health checks, and circuit breakers actually work in staging, (2) run the experiment with 1% traffic in production first, (3) never run experiments during known high-traffic periods (Black Friday, product launches, marketing campaigns), (4) require a second engineer to review and approve every production experiment. If you can't answer "what's the worst that could happen and how do I stop it in <30 seconds?" you're not ready. |
| Blast radius was configured as 5% of traffic but the feature flag system interpreted the percentage as a decimal fraction (0.05 = 5%) — the chaos tooling interpreted it as percentage (5 = 5%) — 100% of traffic was affected | A streaming platform's chaos engineering team configured a latency injection experiment targeting 5% of traffic. The feature flag system used a 0-1 scale (0.05 = 5%). The chaos tooling (Gremlin) used 0-100 scale (5 = 5%). Someone passed "5" to Gremlin, which interpreted it as 5%. Someone else set the feature flag to "5", which the flag system interpreted as 500% — clamped to 100%. The experiment injected 500ms latency to 100% of traffic. P99 spiked from 200ms to 700ms. Customer complaints flooded in for 12 minutes before the experiment was halted. | Two systems with incompatible percentage representations. No integration test between the feature flag system and the chaos tooling. No validation that the actual blast radius matched the intended blast radius. | **Validate actual blast radius before applying chaos, not after.** Before any experiment: (1) deploy the experiment in "dry run" mode (metrics only, no impact) and verify the affected percentage matches intent, (2) check that your feature flag system and chaos tooling use the same scale — never assume, (3) add a kill-switch that stops the experiment automatically if impact exceeds 2x the intended blast radius. Chaos tooling should have a "max blast radius" hard cap that requires VP approval to exceed. |
| Game Day scheduled with 20 participants across 4 teams — nobody prepared, the scenario was revealed at the start, 4 hours of "the system is broken... now what?" with zero lessons learned | A SaaS company scheduled their first Game Day in March 2024. The chaos engineer prepared a complex scenario (region failure + database corruption + DNS outage). They invited 20 people and revealed the scenario at 9 AM: "us-east-1 just went down, go." For the next 4 hours: engineers argued about what was broken, two teams blamed each other, the on-call engineer wasn't in the room and nobody knew the runbooks, and the SRE team was trying to debug a problem the chaos engineer had designed to be unsolvable. At 1 PM, the chaos engineer revealed the scenario. Attendees were angry — "you wasted our day." No future Game Days were scheduled. | The Game Day was a test of the participants, not a test of the system. No one had access to runbooks, dashboards, or escalation paths because those weren't distributed. The scenario was designed to be a challenge to solve, not an opportunity to learn. The chaos engineer treated it as their moment to shine, not the team's moment to practice. | **Game Days are practice, not tests.** (1) Distribute the scenario and expected runbooks 48 hours in advance — participants should know what systems are affected, (2) the goal is to execute a known recovery process faster each time, not to "figure it out live," (3) debrief immediately: what worked, what didn't, what runbooks were wrong, (4) track recovery time across Game Days — it should decrease. A Game Day where nothing was learned is worse than no Game Day. First Game Day: just fail over a single database — 20 minutes, not 4 hours. |
| Chaos experiments ran weekly for 6 months without a single documented steady-state hypothesis — "we're killing random pods and seeing what happens" — found 0 systemic issues because they measured nothing | A platform team ran chaos experiments every Friday for 6 months (January-June 2024). The weekly ritual: pick a service, kill 20% of pods, watch dashboards for 10 minutes, close the ticket as "no impact detected." In July, a real AZ failure happened. The system didn't recover. Investigation: the chaos experiments were killing pods, but Kubernetes was replacing them before any user traffic was affected. The experiments never tested whether the SERVICE was resilient — only that Kubernetes pod replacement worked. Six months of experiments that validated Kubernetes, not the application. | The team confused "run chaos" with "validate resilience." Without a steady-state hypothesis, chaos experiments are just vandalism. "No impact detected" meant the experiment wasn't aggressive enough, not that the system was resilient. | **Every chaos experiment starts with a steady-state hypothesis.** Format: "We hypothesize that if we [inject fault X], the system will [recover in Y seconds] and customers will experience [Z impact]." Measure the steady state BEFORE the experiment (baseline latency, error rate, throughput). Measure during. Compare. If the hypothesis is "no impact," the fault is too small. A valid experiment should show a measurable deviation that recovers within the expected window. Track: how many hypotheses were validated vs. disproven? A 100% validation rate means your experiments are too safe. |
| Ran a network partition experiment between payment service and database — forgot that the payment service's health check also required database connectivity, so Kubernetes killed ALL payment pods as "unhealthy" — took down payments entirely for 14 minutes | A fintech team ran a chaos experiment in October 2024: inject 500ms network latency between the payment service and its database. Within 30 seconds, Kubernetes liveness probes on the payment service started failing (the health check endpoint queried the database). Kubernetes terminated all 6 payment pods as unhealthy. New pods started and immediately failed their liveness probes because the latency injection was still active. CrashLoopBackOff. The experiment was supposed to test graceful degradation; instead it caused a complete payment outage for 14 minutes until the chaos engineer manually removed the latency injection. | The health check had an implicit dependency on the database — the very dependency being tested. The chaos engineer didn't audit what the liveness probe actually checked. The experiment exposed a design flaw (health check shouldn't fail if the database is slow) but wasn't designed to surface it safely. | **Audit health checks before every chaos experiment.** For any experiment affecting dependency D: (1) check what the liveness and readiness probes of dependent services actually test, (2) ensure liveness probes are independent of external dependencies (liveness = "is my process alive?", readiness = "can I serve traffic?"), (3) if a liveness probe depends on an external service, fix that BEFORE running chaos. The experiment discovered a real bug — but the hard way. A pre-experiment audit would have found it without an outage. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can run `chaos-monkey terminate-random-instance` but you can't explain what steady state you're validating — your experiments are "let's see what happens" | You've designed and run 10+ chaos experiments where you predicted the outcome (recovery time, customer impact, blast radius) before running and were right >80% of the time — and you have the written hypotheses and results to prove it | An SRE team says "we're afraid to run chaos experiments in production" — you design their first 5 experiments, none cause an incident, and within 3 months they're running experiments independently and have discovered 3 real resilience gaps |
| Your Game Days are PowerPoint presentations about what chaos engineering is, not hands-on exercises where teams actually recover from failures | Your Game Days have a defined scenario, prepared runbooks, time-boxed recovery windows, and a debrief that produces specific action items — and recovery time has decreased across 3+ Game Days | A VP asks "prove that chaos engineering is worth the investment" — you produce a report showing 8 resilience gaps found, 6 fixed, and the estimated cost of those gaps becoming production incidents, with the total value >10x the chaos engineering investment |
| You think chaos engineering is about tools — you're certified in Gremlin, Chaos Mesh, and Litmus but never ran an experiment that found a real problem | You think chaos engineering is about hypotheses — every experiment starts with "we believe the system will behave like X if we inject fault Y" and you're comfortable being wrong because disproving a hypothesis is a win | You design an organization's chaos engineering program from scratch — you select tooling, define experiment catalog, train 5+ teams, and establish metrics that prove the program's ROI within 6 months |

**The Litmus Test:** A company has never run a chaos experiment and their CTO says "we're not Netflix, we don't need this." Can you design a single experiment that (a) has zero risk of customer impact, (b) teaches the team something they don't already know, and (c) makes the CTO ask "what else don't we know?" If your first experiment would require production access and could cause an incident, you're L1. Masters start with staging, prove value in 2 weeks, and get invited to production.

## Deliberate Practice

```mermaid
graph LR
    A[Build] --> B[Measure<br/>failure modes] --> C[Study<br/>post-mortems] --> D[Re-build<br/>with constraints] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Rebuild an existing system from scratch, then compare your design with the original | Monthly |
| **Competent** | Add a new constraint (10x data, zero downtime, etc.) to a familiar design and re-architect | Quarterly |
| **Expert** | Design the same system under 3 conflicting constraint sets; write a decision record for each | Quarterly |
| **Master** | Teach a junior to design a system; your role is to ask questions, not give answers | Monthly |

**The One Highest-Leverage Activity:** Every quarter, take a system you built 6+ months ago and redesign it from scratch with what you know now. Write down what changed and why.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Principles of Chaos Engineering](https://principlesofchaos.org/)
- [Netflix — Chaos Engineering (Original Paper)](https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116)
- [Chaos Mesh — Kubernetes Chaos Engineering](https://chaos-mesh.org/)
- [LitmusChaos — CNCF Chaos Engineering](https://litmuschaos.io/)
- [AWS Fault Injection Service (FIS)](https://aws.amazon.com/fis/)
- [Gremlin — Chaos Engineering Platform](https://www.gremlin.com/)
- [Steadybit — Chaos Engineering Platform](https://www.steadybit.com/)
- [Resilience4j — Fault Tolerance Library](https://resilience4j.readme.io/)
- [Martin Fowler — Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
