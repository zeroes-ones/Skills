# Additional Resources — Configuration & Change Safety

> Deep knowledge loaded on demand. The SKILL.md holds the decisions and rules; this file holds the
> extended material: the change-class taxonomy, validation gate patterns, worked rollout arithmetic,
> failure narratives, and the sources behind the claims.

---

## 1. Change-class taxonomy

Every change falls into one of these classes. The class determines the application strategy, so the
classification is the first act, not a documentation step.

| Class | Examples | Reversible? | Required controls |
|-------|----------|-------------|-------------------|
| **Pure config value** | Timeouts, pool sizes, feature-flag defaults, rate limits | Yes, if the previous value is recorded | Schema + target validation; staged rollout; recorded previous value |
| **Structural config** | Topology, routing rules, IAM policies, network policies | Usually yes, but blast radius is large | Human gate + staged rollout + security review if scope changes |
| **Schema change (additive)** | New optional field, new index | Yes | Compatible-by-default; validate consumers tolerate it |
| **Schema change (destructive)** | Drop column, narrow type, tighten constraint | **No** | Human gate + forward-fix plan + consumer inventory |
| **Data migration** | Backfill, re-encode, deduplicate | **No** (once applied) | Human gate + idempotent script + rollback-by-restore plan |
| **Certificate / credential** | Rotation, revocation, CA change | **No** (revocation is one-way) | Overlap window + inventory + automated renewal |
| **API contract** | Removing a field, changing an error shape | **No** for consumers already shipped | Deprecation window + consumer-driven contract tests |
| **Flag state** | Turning a flag on/off, changing rollout % | Yes | Owner + removal date; off-state tested |

**The rule that follows:** irreversibility, not size, determines whether a human gate is required.
A one-line destructive schema change is more dangerous than a 100-line config refactor.

---

## 2. Validation gate patterns

Validation belongs in two places, catching different error classes.

### 2.1 CI validation (schema)

```yaml
# config.schema.json (illustrative)
type: object
properties:
  connection_pool_size:
    type: integer
    minimum: 1
    maximum: 200        # schema bound
    default: 20
  request_timeout_ms:
    type: integer
    minimum: 50
    maximum: 30000
required: [connection_pool_size, request_timeout_ms]
```

Catches: typos, type errors, out-of-range values, missing required keys.
Misses: target state, quota limits, version incompatibility, drift.

### 2.2 Target validation (state)

Runs against the real environment before apply. Illustrative checks:

```bash
# Does the proposed value conflict with the target's actual limits?
current_connections=$(psql -tAc "SELECT count(*) FROM pg_stat_activity")
max_connections=$(psql -tAc "SHOW max_connections")
# proposed_pool_size * instance_count must not exceed max_connections
```

Catches: resource conflicts, quota exhaustion, version incompatibility, existing drift.
This is the gate that catches the class of error CI cannot see.

### 2.3 The gate ordering

```
1. CI schema validation        → fails the build
2. Security review (if relevant) → routes to appsec-engineer / iam-architect
3. Target state validation     → fails the apply
4. Apply, staged               → canary → % → all
5. Observation gate            → abort at the numeric threshold
```

Steps 3–5 are the ones teams most often skip, and they are the ones that prevent the outage.

---

## 3. Worked rollout arithmetic

### 3.1 Blast radius by count vs. by dependency graph

```
200 instances, 60,000 rpm, 300 rpm per instance

By count:        1% of instances  = 2 instances  = 600 rpm  (looks like 1% of traffic)
By graph:        if those 2 instances hold the sole leader-election lock
                 → 100% of write operations fail
                 → effective blast radius = 100%, not 1%
```

**The arithmetic to do before every scoped change:** for each selected target, what depends on it?
The count is an input to the selector; the dependency graph is the actual blast radius.

### 3.2 Staged rollout with abort thresholds

```
Stage 1  canary        1 instance     observe 15 min   abort if error_rate > 0.5%
Stage 2  small         1% (2)         observe 30 min   abort if error_rate > 0.5% or p99 > 1.5x baseline
Stage 3  large         10% (20)       observe 30 min   abort if error_rate > 1% or p99 > 2x baseline
Stage 4  full          100% (200)     observe 60 min   (no further stage)
```

Two properties matter: the thresholds are **numeric and set before apply**, and each stage's
observation window is long enough for the signal to appear. "Watch it closely" is not a threshold.

### 3.3 Observation window sizing

```
window >= time_for_signal_to_manifest
```

For a request-path change, that is minutes (error rates move immediately). For a cache-related
change, it may be hours (the effect appears as the cache turns over). Sizing the window shorter than
the signal's latency is how a staged rollout passes while being wrong.

### 3.4 Drift window cost

```
drift introduced at t=0, detected at t=6h
mean time to attribute the cause      ≈ 2h   (which change? which actor?)
```

Undetected drift converts a five-minute fix into a multi-hour investigation, because the change was
never recorded and so has no review trail to consult.

---

## 4. Failure narratives

### 4.1 The 1% change that took down everything

A team rolled a config change to "1% of instances" — two of two hundred — believing the blast radius
was 1% of traffic. Both selected instances happened to hold the application's sole leader-election
lock. Every write in the system routed through those two instances, so a 1% change produced a 100%
write outage for fourteen minutes while the team watched a dashboard that said one percent.

**Fix:** verify the selector against the dependency graph, not the instance count. Ask "what depends
on these targets?" before asking "how many are they?"

**Lesson:** the comforting number was the dangerous part.

### 4.2 The config change nobody reviewed

A production incident was mitigated by hand-editing a connection pool value on the running service.
The fix worked, the incident closed, and the change was never recorded. Six weeks later the same
service behaved differently in production than in every other environment, and nobody could say why.
The investigation took two days; the answer was a value that existed only in production.

**Fix:** apply the change through the declaration, review it, then reapply. And add drift detection
so the divergence raises an alert rather than being found by accident.

**Lesson:** drift is an unmanaged change — unreviewed and unrollbackable.

### 4.3 The rollback that wasn't

A team shipped a data migration they described as "reversible: we can restore from backup". During an
incident they attempted the rollback and found the backup restore took four hours and lost forty
minutes of subsequent writes — a worse outcome than the fault. The change had been classified as
reversible by assumption, not by execution.

**Fix:** classify reversibility by *executing* the rollback once in a non-production environment, and
record how long it took. If the restore is hours, the change is not reversible within the incident
window, whatever the label says.

**Lesson:** an untested rollback is a plan, not a capability.

### 4.4 The flag that outlived its feature

A feature flag was created for a launch and left at 100%. Over eighteen months the flag became part
of the code's structure — branches referenced it, tests assumed it, and no one tested its off-state.
When a later refactor tried to remove it, the removal was itself a risky change requiring its own
rollout.

**Fix:** every flag gets an owner and a removal date at creation. A flag at 100% for sixty days with
no removal ticket is technical debt with a blast radius.

**Lesson:** flags decouple deploy from release, but an unowned flag is a permanent code path.

### 4.5 The selector that matched everything

A chaos experiment — and, separately, a config rollout — used a label selector intending 2% of pods.
A missing label on the remaining pods meant the selector matched 100%. The experiment designed to
test resilience became the outage; the config change designed to be cautious became total.

**Fix:** test the selector as carefully as the change. Resolve it in dry-run and count the matches
before applying.

**Lesson:** a selector is code, and it is rarely reviewed as carefully as the change it scopes.

---

## 5. Verification recipes

### 5.1 Proving a config value is validated before apply

```bash
# Schema validation in CI
python3 -c "import json,sys; json.load(open('config.json'))" && jsonschema -i config.json config.schema.json

# Target validation before apply (illustrative)
# assert proposed value does not exceed the target's actual limit
```

The test that matters: feed it an invalid value and confirm the **gate** fails, not the service.

### 5.2 Proving a rollback works

```
1. Apply the change in a non-production environment.
2. Execute the recorded rollback.
3. Assert: the previous state is restored exactly.
4. Record the elapsed time.
```

If step 3 cannot be asserted, the change is not reversible in the sense the label claims.

### 5.3 Proving drift detection fires

```
1. Change a value directly in the environment (outside the declaration).
2. Assert: a drift alert fires, naming the declaring file and the observed value.
3. Reconcile, and assert the alert clears.
```

Detection without alerting is a report nobody reads — step 2 is the requirement.

### 5.4 Proving the selector matches what you intend

```
1. Resolve the selector in dry-run.
2. List the matched targets.
3. For each, enumerate what depends on it.
```

This is the exercise that would have caught failure 4.1.

---

## 6. Sources

| Claim | Source | Strength |
|-------|--------|----------|
| **Over half of incidents stem from software changes**; deployments and config updates link disproportionately to high severity and manual remediation | TU Delft analysis of 348 VOID incident reports (2025) | Thesis — directionally strong |
| **~Half of incidents are non-code** (capacity, manual deploy error, expired certificates); >90% mitigated without a code change | Microsoft Teams study, ACM | Peer-reviewed / industrial |
| Azure outage (Oct 2025) triggered by an "inadvertent configuration change" in Azure Front Door, cascading to M365/Entra/Xbox | Public incident reporting | Vendor post-incident report |
| CrowdStrike (Jul 2024) caused by a **config artifact** (channel file), not the driver; lessons include *test config like code*, staged rollouts, automatic rollback | Public incident analysis | Vendor post-mortem + independent analysis |
| AWS outage (Oct 2025) from a race condition in DNS automation, cascading across EC2/Lambda | Public incident reporting | Vendor post-incident report |
| Config-as-PR, canary rollouts and drift detection as standard controls for config-error incidents | Community incident-pattern literature (languages from danluu/post-mortems covering AWS, Google, GitHub, Cloudflare, Meta) | Community-maintained pattern library |
| Time-related failures (cert expiry, leap seconds, NTP) as a distinct recurring category | Same pattern literature; ICT failure taxonomy (Computers & Security, 2025) | Peer-reviewed review + pattern library |

**Explicitly not claimed:** that any change process eliminates change-induced incidents. The controls
reduce blast radius and recovery time. Research consistently finds **most incidents involve multiple
contributing factors** rather than a single root cause, which is why this skill treats classification,
validation, staging and drift as independent controls rather than a single gate.

---

## 7. Related reading in this library

- `ci-cd-builder` — implementing these gates in the pipeline
- `release-manager` — sequencing releases, versioning, release notes
- `site-reliability-engineer` — error budgets, which bound acceptable change risk
- `incident-responder` — what to do when a change has already broken production
- `resilience-pattern-engineer` — runtime defences for dependencies a change made fragile
- `dependency-governance` — change policy and approval requirements
