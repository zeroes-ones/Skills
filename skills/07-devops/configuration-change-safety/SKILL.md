---
name: configuration-change-safety
description: >
  Use when designing or reviewing how configuration and change reach production — config as
  code, config schemas and validation, staged rollout of config, drift detection, blast-radius
  limits, change rollback, or change-freeze windows — or when a config change has caused an
  incident. Handles change classification (what can be rolled back and what cannot), config
  validation gates, progressive rollout, drift detection, and the safety properties a change
  must hold before it is applied. Do NOT use for pipeline construction and build automation
  (ci-cd-builder, automation-engineer), release trains and versioning (release-manager),
  runtime resilience patterns (resilience-pattern-engineer), or live incident command
  (incident-responder).
author: Sandeep Kumar Penchala
license: MIT
type: devops
status: stable
version: 1.0.0
updated: 2026-09-11
tags:
  - configuration
  - config-as-code
  - change-management
  - drift-detection
  - progressive-delivery
  - rollback
  - blast-radius
  - feature-flags
  - validation
  - release-safety
token_budget: 3500
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
chain:
  examples:
    - skills/07-devops/configuration-change-safety/examples/backtest
  consumes_from:
    - devops-engineer
    - cloud-architect
    - automation-engineer
    - observability-engineer
    - system-architect
    - dependency-governance
  feeds_into:
    - ci-cd-builder
    - release-manager
    - site-reliability-engineer
    - incident-responder
    - resilience-pattern-engineer
workflow:
  artifacts:
    inputs: [change-set, environment-topology]
    outputs: [change-safety-plan]
  completion:
    criteria:
      - Every change is classified as reversible or irreversible before it is applied
      - Every config value has a schema and is validated before apply, not after failure
      - Every change reaches production progressively, never to all targets at once
      - Drift between declared and observed configuration is detectable and alerted
    evidence: required
  escalate_to: [human-gate]
---

# Configuration & Change Safety

> **Portability target:** Spec-level. This skill encodes domain expertise, not tool-specific commands.

Treat configuration like code, and treat every change as a hypothesis that can be wrong.

## Route the Request **(QUICK)**

### Auto-Route (No User Input Required)

| ID | Signal | Route to |
|----|--------|----------|
| A1 | `file_contains("*.tf", "resource\|module")` or Helm/Kustomize/Ansible manifests present | **Config-as-Code Audit** — is config declared or hand-edited? |
| A2 | Recent incident or postmortem referencing config, deploy, flag, or certificate | **Change-Safety Review** from Decision Tree 1 |
| A3 | `file_contains("*.yaml", "featureFlag\|feature_flag\|rollout")` | **Progressive Rollout Design** |
| A4 | No config validation or schema found, but config files exist | **Validation Gap** — Decision Tree 2 |
| A5 | Config present in a running environment with no declaration in version control | **Drift Detection** — Decision Tree 3 |

### Intent Route (Ask the User)

```
├── "a config change took us down"                    → Change-Safety Review → Decision Tree 1
├── "how do we roll this out safely?"                 → Decision Tree 1 then rollout design
├── "should this be a flag, a config value, or code?" → Change Classification
├── "our environments have drifted"                   → Drift Detection (Decision Tree 3)
├── "we need config validation before apply"          → Decision Tree 2 (schema + gates)
└── "review whether our change process is safe"       → Full workflow, all three trees
```

## Anti-Rationalization **(QUICK)**

| Rationalization | Why it is wrong | Required response |
|-----------------|-----------------|-------------------|
| "It's only a config change." | Config changes are *disproportionately* linked to high-severity incidents — the Azure outage was an "inadvertent configuration change". | Classify and stage it exactly like code. |
| "We'll validate it in staging." | Staging does not reproduce production config, load, or topology. Validation must also happen *before* apply, on the real target. | Schema in CI + pre-apply validation on the target. |
| "Rollback is easy, we'll just revert." | Some changes are irreversible: data migrations, certificate revocations, contract removals, flag-state loss. | Classify reversibility *before* applying (R1). |
| "We tested it, so it's safe." | A change safe for one target may be catastrophic for another — a label selector matching 100% instead of 2%. | Test the selector and the blast radius, not just the change (R3). |
| "Drift is inevitable, we accept it." | Accepted drift is an undocumented change nobody reviewed and nobody can roll back. | Detect and alert on drift; treat it as an unmanaged change (R4). |
| "The flag is temporary." | Flags left at 100% become permanent code paths nobody owns, and their removal is its own risky change. | Every flag has an owner and a removal date at creation (R5). |

## Ground Rules — Read Before Anything Else **(QUICK)**

| # | Rule | Mechanical Trigger | Violation Response |
|---|------|-------------------|-------------------|
| **R1** | **REFUSE to apply a change whose reversibility has not been classified.** "Can we undo this?" must be answered before, not during, an incident. | Change set has no reversibility classification, or an irreversible change has no rollback/forward-fix plan | STOP. Respond: "State whether this change is reversible, and how. Data migrations, certificate revocations, contract removals and flag-state loss are irreversible — they need a forward-fix plan, not a rollback claim. I will not proceed until each change is classified." |
| **R2** | **REFUSE to apply configuration that has no schema.** Unvalidated config fails at runtime, in production, at the worst time. | Config value with no type, range, or allowed-set constraint | STOP. Respond: "What type and range is this value? An unvalidated config value is a production surprise. Define the schema — type, bounds, allowed values — and validate before apply." |
| **R3** | **REFUSE to apply a change to all targets at once.** Every change reaches production progressively, and the selector must be verified to match what you intend. | Change applies to 100% of targets, or blast radius is a percentage without a verified selector | STOP. Respond: "Show me the selector and what it matches. '1% of instances' once took down 100% of traffic because that instance held a sole leader. Blast radius is measured on the dependency graph, not on the count." |
| **R4** | **REFUSE to leave drift undetected.** Configuration that differs from its declaration is an unreviewed change. | Observed config differs from declared config with no detection or alert | STOP. Respond: "This environment differs from its declaration and nothing detects it. That is an unmanaged change — nobody reviewed it and nobody can roll it back. Add drift detection and alert on divergence." |
| **R5** | **REFUSE to create a feature flag without an owner and a removal date.** Flags accumulate into permanent, untested code paths. | Flag created with no owner or no removal date | STOP. Respond: "Every flag needs an owner and a removal date at creation. A flag at 100% for 60 days with no removal ticket is technical debt with a blast radius." |
| **R6** | **REFUSE to treat a config change as lower-risk than a code change.** The evidence says the opposite. | Change review applies less scrutiny to config than to code | STOP. Respond: "Config changes correlate with *higher* severity than code changes in incident data. Apply the same review, the same staged rollout, and the same rollback plan." |

## Anti-Hallucination

- **Admit uncertainty.** If you do not know whether a change is reversible, say so and treat it as irreversible until proven otherwise. Never claim reversibility you have not verified.
- **Flag your knowledge cutoff.** Config tooling (Terraform state semantics, Helm hooks, Kubernetes rollout behaviour, feature-flag SDK evaluation order) changes between versions. State that specific behaviours must be confirmed against the installed version rather than recalled.
- **Never guess security.** A config change that widens IAM scope, disables a check, or relaxes TLS is a security change. Route it through `iam-architect` or `appsec-engineer`; do not approve it here.
- **[VERIFIED] provenance.** Tag every claim as `[VERIFIED]` (observed in the environment, with the command), `[COMPUTED]` (derived, with the formula), or `[ESTIMATED]` (assumed, with the assumption written down).

## The Expert's Mindset **(QUICK)**

The evidence is counter-intuitive and worth internalising: **change is the dominant trigger of production incidents, and configuration changes are disproportionately linked to high severity.** Teams that treat config as "just a setting" and code as "the real work" have the risk backwards. The Azure outage was an inadvertent configuration change; CrowdStrike was a config artifact, not a driver.

The second shift is that **reversibility is the property that matters, not correctness.** You cannot know a change is correct before applying it — that is what production is for. You *can* know whether you can undo it. So classification comes first: reversible changes can be staged and rolled back freely; irreversible ones need a forward-fix plan and a human gate, because "roll back" is unavailable exactly when it matters.

Third: **blast radius is a property of the dependency graph, not of a count.** "1% of instances" is a comforting number that can be a 100% outage if that instance holds a sole leader. The safe question is never "how many did I change?" but "what depends on what I changed?"

Fourth: **drift is an unmanaged change.** A hand-edited value in production is a change nobody reviewed, nobody staged, and nobody can roll back — the change-management failure that hides in plain sight.

## What Change Masters Know **(STANDARD)**

- The most dangerous changes are those with **no rollback path and no gate**: a certificate revoked early, a migration that dropped a column, a contract removed before consumers migrated.
- **Flags are the safest mechanism and the most abused.** They decouple deploy from release — but an unowned flag at 100% is a permanent code path with no off-state tests.
- **Validation belongs before apply, on the target.** Validating in CI catches typos; validating on the target catches the environment difference that actually causes outages.
- **A selector is code.** The blast radius of a change is determined by what the selector matches, and selectors are rarely tested as carefully as the change itself.
- **Freeze windows exist because change causes incidents.** A freeze during peak trading, a major event, or a compliance period is blast-radius control by time.

### When to Break Your Own Rules **(DEEP)**

- **An emergency security fix may bypass staged rollout** — apply immediately, with an explicit written reversal time and a named human owner. Log it as an exception, not a precedent.
- **A single-instance internal service may legitimately apply to 100%** — there is no progressive path. Say so explicitly rather than leaving the rule silently violated.
- **A short-lived environment may skip drift detection** — its lifetime is shorter than the drift window. State the assumption.
- **A flag may ship without a removal date during an active incident** — a flag is the correct emergency tool. Record the debt explicitly and schedule removal.

## Deliberate Practice **(STANDARD)**

| Level | Routine | Time | Success Metric |
|-------|---------|------|---------------|
| Novice | Classify five past changes as reversible or irreversible and write the rollback path for each | 30 min | Every irreversible change identified with a forward-fix plan |
| Intermediate | Add a schema and pre-apply validation to one config file, then prove an invalid value is rejected before apply | 45 min | Invalid config fails the gate, not the service |
| Advanced | Design a staged rollout for a config change across 200 instances with verified selectors and abort thresholds | 2 h | Selector matches exactly the intended targets; abort fires on a threshold |
| Expert | Introduce drift detection for an environment and find a real divergence within a week | 1 week | A drift alert fires naming the declaring file and the observed value |

## Operating at Different Levels **(STANDARD)**

### L1: Apprentice
- **Scope:** Hand-edited config with no validation
- **Autonomy:** Applies changes as instructed
- **Impact:** Config errors reach production directly
- **Craft:** Knows config should live in version control

### L2: Practitioner
- **Scope:** Config as code, some validation, manual rollout
- **Autonomy:** Prepares and applies changes
- **Impact:** Config is reviewable and mostly reproducible
- **Craft:** Classifies reversibility; writes a rollback step

### L3: Senior
- **Scope:** Schemas, pre-apply validation, staged rollout, drift detection
- **Autonomy:** Owns the change process for a service
- **Impact:** Config changes become as safe as code changes
- **Craft:** Verifies selectors; sets abort thresholds; detects drift

### L4: Staff / Principal
- **Scope:** Change safety as a platform property across services
- **Autonomy:** Sets the organisation's change standards
- **Impact:** Blast radius is designed, not discovered
- **Craft:** Classifies change classes organisation-wide; automates gates

### L5: Transformative
- **Scope:** Change velocity and safety co-designed; every change reversible by construction
- **Autonomy:** Owns the organisation's change posture
- **Impact:** Deploy frequency rises while change-induced incidents fall
- **Craft:** Designs systems where the risky change is impossible to express

## When to Use **(QUICK)**

| Use this skill | Use a neighbour instead |
|----------------|------------------------|
| Designing how config reaches production safely | `ci-cd-builder` — pipeline construction and build automation |
| Classifying a change's reversibility and blast radius | `release-manager` — release trains, versioning, release notes |
| Adding schema and pre-apply validation to config | `automation-engineer` — infrastructure-as-code and tooling |
| Detecting drift between declared and observed config | `cloud-architect` — environment topology and IaC structure |
| A config change has already broken production | `incident-responder` — the incident is live |
| Designing the runtime defence for a newly fragile dependency | `resilience-pattern-engineer` — timeouts, breakers, bulkheads |

## When NOT to Use **(QUICK)**

1. **The task is building or debugging the pipeline itself** — use `ci-cd-builder`; this skill governs the *safety properties of a change*, not the pipeline carrying it.
2. **The change is a code change with no config component** — `code-reviewer` owns it; classification still applies, but the design work does not.
3. **An incident is live** — use `incident-responder` first. Classify later.
4. **The change widens security scope** — route through `iam-architect` / `appsec-engineer`. Approving a security-relevant config change here is out of scope.
5. **The environment is ephemeral and short-lived** — drift detection and staged rollout may be disproportionate. State the assumption rather than skipping silently.

## Decision Trees **(STANDARD)**

### Decision Tree 1: How must this change be applied?

```
Is the change reversible (can you restore the previous state exactly)?
├── Yes ↓
│   └── How many targets does it affect?
│       ├── One target → apply directly, with a recorded rollback step
│       └── Many targets ↓
│           Is the selector verified to match exactly the intended targets?
│           ├── No → STOP. Verify the selector first (R3).
│           └── Yes → PROGRESSIVE: canary → small % → large % → all, with abort thresholds
└── No (irreversible) ↓
    Is there a forward-fix path if it goes wrong?
    ├── No → STOP. Do not apply. Redesign for reversibility, or get a named human gate (R1).
    └── Yes → HUMAN GATE + forward-fix plan + extended observation window
              (data migration, cert revocation, contract removal, flag-state loss)
```

### Decision Tree 2: Where does validation belong?

```
Is the config value constrained by a type, range, or allowed set?
├── No → STOP. Define the constraint first (R2). Unconstrained config is a runtime surprise.
└── Yes ↓
    Validate in CI against the schema
    ├── Catches: typos, type errors, missing required keys
    └── Does NOT catch: environment differences, target state conflicts
    Then validate ON THE TARGET before apply
    ├── Catches: resource conflicts, quota limits, version incompatibility, drift
    └── Gate: apply proceeds only if target validation passes
    Finally: is the value security-relevant (IAM, TLS, network policy)?
    ├── Yes → route to iam-architect / appsec-engineer before apply
    └── No → proceed
```

### Decision Tree 3: Drift detected — what now?

```
Is the drift intentional and documented?
├── Yes → declare it in the config source, then reconcile. Undeclared intent is still drift.
└── No ↓
    Is the drifted value security-relevant?
    ├── Yes → treat as a security event: escalate to appsec-engineer, preserve evidence
    └── No ↓
        Can the observed value be safely reverted to the declared value?
        ├── Yes → reconcile (revert), then find how it drifted (which actor, which path)
        └── No (the observed value is load-bearing) ↓
            Adopt-then-declare: codify the observed value, review it, then manage it normally
            └── REQUIRED: record who changed it and why. Drift with no known cause is a process gap.
```

## Core Workflow **(STANDARD)**

| Phase | Time | What you do | Complete when |
|-------|------|-------------|---------------|
| **1. Inventory** | 15 min | List every config surface in the change and where it is declared | Complete when every config value has a declaring file or is marked undeclared |
| **2. Classify** | 20 min | Run Decision Tree 1 per change; mark reversible vs. irreversible | Complete when every change has a reversibility classification and a rollback or forward-fix path |
| **3. Schema** | 20 min | Run Decision Tree 2; define constraints; place the validation gates | Complete when every value has a type, range or allowed set, and a pre-apply gate exists |
| **4. Blast radius** | 20 min | Verify the selector; map what depends on the targets | Complete when the selector is proven to match exactly the intended targets |
| **5. Rollout** | 20 min | Design canary → % → all with abort thresholds | Complete when abort thresholds are numeric and the abort path is tested |
| **6. Rehearse** | 30 min | Apply in a non-production environment; execute the rollback or forward-fix | Complete when the rollback has actually been executed once, not just documented |
| **7. Apply** | 15 min | Progressive apply with observation gates | Complete when each stage passed its threshold before the next began |
| **8. Observe** | 30 min | Watch the change-specific signals through the observation window | Complete when the window elapsed with no threshold breach |
| **9. Drift** | 20 min | Run Decision Tree 3; confirm declared equals observed | Complete when declared and observed configuration match, or drift is documented |
| **10. Record** | 10 min | Log the change, its classification, and its outcome in the State Log | Complete when the *why* is recorded, not just the *what* |

## Best Practices **(STANDARD)**

1. **Classify reversibility before anything else.** It determines the entire application strategy, and discovering it mid-incident is too late.
2. **Give every config value a schema.** Type, bounds, allowed values, required-ness. Unconstrained config is a runtime surprise with no early warning.
3. **Validate twice: in CI for typos, on the target for environment truth.** Neither catches what the other does.
4. **Verify the selector before the change.** A selector is code, and its blast radius is often more consequential than the change itself.
5. **Express blast radius on the dependency graph, not on a count.** "1% of instances" can be 100% of a shared dependency.
6. **Set abort thresholds numerically, before apply.** "Watch it closely" is not a threshold. `error_rate > 1%` is.
7. **Actually execute the rollback once outside production.** An untested rollback is a plan, not a capability.
8. **Alert on drift, not just detect it.** Detection without alerting is a report nobody reads.
9. **Give every flag an owner and a removal date at creation.** Otherwise it becomes a permanent path with no off-state tests.
10. **Treat a config change as at least as risky as a code change.** The incident evidence says more risky, not less.

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Total outage from a change scoped to a small percentage | Blast radius measured by count, not dependency graph — the target held a sole leader | Map downstream dependencies before scoping; verify the selector | Blast radius is a graph property |
| Config applied successfully but service fails at runtime | No schema; the value was syntactically valid but semantically wrong | Define type/range/allowed values; validate on the target before apply | Unvalidated config fails in production |
| Rollback attempted during an incident and failed | The change was irreversible (migration, cert revocation, contract removal) and unclassified | Classify reversibility first; irreversible changes need a forward-fix plan and a human gate. Recovery typically costs **$50,000–$500,000** | "We'll roll back" is not a plan for irreversible changes |
| Environment behaves differently from its declaration | Drift — a hand-edited value nobody reviewed | Detect and alert on drift; reconcile or adopt-then-declare. Undetected drift commonly costs **$10,000–$100,000** in debugging time | Drift is an unmanaged change |
| Feature behaves inconsistently across users | A flag left at partial rollout with no owner | Flag inventory with owners and removal dates; audit rollout percentages | Unowned flags create permanent, untested paths |
| Change passed CI but failed on the target | CI validated against the schema, not the target's actual state | Add pre-apply validation on the target (quota, conflicts, version compatibility) | Two validations, two classes of error |
| Certificate expired and took down a service | No expiry inventory or renewal automation | Inventory every expiry; automate renewal; alert well before | Time-related failures recur (see `time-and-clock-correctness`) |
| "We tested this exact change in staging" yet it broke production | Staging did not reproduce production topology, load, or config | Test the selector and blast radius; use progressive rollout as the real test | Production is the only faithful test — so stage it |

## Error Recovery **(QUICK)**

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|--------------|------------|
| Change is breaking production | Abort the rollout at the current stage; hold at the last good state | Execute the pre-rehearsed rollback | Escalate to `incident-responder`; the rollback path is exhausted |
| Rollback fails | Determine whether the change is actually reversible (re-classify) | Apply the forward-fix plan | Human gate: named owner decides accept-degraded vs. extended outage |
| Config invalid at apply time | Read the validation error; it names the constraint | Correct the value and re-run the pre-apply gate | If the schema is wrong, fix the schema — never bypass the gate |
| Drift found in production | Determine intent and security relevance (Decision Tree 3) | Reconcile to declared, or adopt-then-declare | Escalate to `appsec-engineer` if security-relevant |
| Selector matched more than intended | Abort immediately; the blast radius is already exceeded | Roll back the affected targets | Escalate; treat as an incident regardless of observed impact |
| Flag at 100% with no owner | Assign an owner and a removal date now | Remove the flag if its off-state is tested | Freeze new flag creation until the inventory is clean |

**Hard failure boundary:** After 3 failed recovery attempts, escalate to a human. Do not loop.

## Cross-Skill Coordination **(STANDARD)**

### Upstream (What This Skill Needs)

| Upstream Skill | Artifact Needed | What You'll Use It For |
|---------------|----------------|----------------------|
| `devops-engineer` | Config layout, environment structure | Know where each value is declared |
| `cloud-architect` | Environment topology, region/AZ layout | Determine the real blast radius of a change |
| `automation-engineer` | IaC and tooling inventory | Place validation gates in the existing tooling |
| `observability-engineer` | Change-specific signals and dashboards | Define abort thresholds and observation windows |
| `system-architect` | Service dependency graph | Map what depends on the change targets |
| `dependency-governance` | Change policy, approval requirements | Align classification with policy |

### Downstream (What This Skill Produces)

| Downstream Skill | Deliverable | What They'll Do With It |
|-----------------|------------|------------------------|
| `ci-cd-builder` | Validation gates to implement in the pipeline | Add pre-apply checks to the build/deploy path |
| `release-manager` | Change classification and rollout plan | Sequence releases and write release notes |
| `site-reliability-engineer` | Abort thresholds and observation windows | Wire alerts and error-budget policy |
| `incident-responder` | Reversibility classification and rollback path | Know what recovery options exist during an incident |
| `resilience-pattern-engineer` | Fragile-dependency list from the change | Design runtime defences for newly fragile paths |

## Proactive Triggers **(STANDARD)**

- **A config change is proposed in review** → Apply R1–R3 classification before approval. Config changes correlate with *higher* severity than code changes. 🔴
- **A change applies to 100% of targets** → Require a staged path or a written justification. 🔴
- **A new feature flag is created** → Require an owner and a removal date at creation (R5). 🟡
- **Observed config diverges from declared** → Treat as an unmanaged change; run Decision Tree 3. 🔴
- **A certificate or credential approaches expiry** → Inventory and automate renewal before the window closes. 🟡
- **An irreversible change is proposed** → Require a human gate and a forward-fix plan, not a rollback claim. 🟠

## Anti-Patterns **(STANDARD)**

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ **Hand-editing production config** — a fix applied directly to a running system | ✅ Change the declaration, review it, then apply through the gate |
| ❌ **"It's only config"** — less review than a code change | ✅ Same review, same staged rollout, same rollback plan (R6) |
| ❌ **Rollback as an assumption** — "we can always revert" for an irreversible change | ✅ Classify reversibility first; irreversible changes get a forward-fix plan (R1) |
| ❌ **Blast radius by percentage** — "1% of instances, we're fine" | ✅ Verify the selector and map the dependency graph (R3) |
| ❌ **Validate in staging only** — the change is faithful, the environment is not | ✅ Validate on the target before apply (Decision Tree 2) |
| ❌ **Detection without alerting** — a drift report nobody reads | ✅ Alert on divergence, naming the declaring file and observed value |
| ❌ **Flags without owners** — left at 100% indefinitely | ✅ Owner + removal date at creation (R5) |
| ❌ **Testing the change but not the selector** — the change is safe, the scope is not | ✅ Test the selector as carefully as the change |

## State Log **(QUICK)**

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | Change classified | Reversible; progressive rollout with numeric abort thresholds | Partial rollout leaves mixed state briefly | Observation gate between stages; rollback rehearsed |
| 2 | Drift detected | Reconciled to declared value | Brief divergence during reconcile | Alert on divergence; actor and path identified |

**Anti-Drift Check:** Before each response, verify:
1. Did the last action match the plan?
2. Are we still within scope?
3. Has any new information invalidated prior decisions?
4. Has a change been applied without a reversibility classification? If so, the process has drifted.

## Production Checklist **(STANDARD)**

- [ ] **CR1: Reversibility classified** — Verification: every change marked reversible or irreversible, with a rollback or forward-fix path
- [ ] **CR2: Schema defined** — Verification: every config value has a type, range or allowed set
- [ ] **CR3: CI validation present** — Verification: schema validation runs in CI and rejects invalid values
- [ ] **CR4: Target validation present** — Verification: pre-apply validation runs against the target environment
- [ ] **CR5: Selector verified** — Verification: the selector is proven to match exactly the intended targets
- [ ] **CR6: Blast radius mapped** — Verification: dependencies of the targets are enumerated, not just the count
- [ ] **CR7: Progressive rollout designed** — Verification: canary → % → all, with numeric abort thresholds
- [ ] **CR8: Rollback rehearsed** — Verification: the rollback (or forward-fix) has been executed once outside production
- [ ] **CR9: Observation window defined** — Verification: a duration and the signals to watch are recorded
- [ ] **CR10: Drift detection active** — Verification: divergence between declared and observed raises an alert
- [ ] **CR11: Flag inventory current** — Verification: every flag has an owner and a removal date
- [ ] **CR12: Change recorded with rationale** — Verification: the State Log explains *why*, not just what changed

## What Good Looks Like **(QUICK)**

A change process where every change is classified reversible or irreversible before it is applied; every config value has a schema validated both in CI and on the target; blast radius is expressed on the dependency graph with a verified selector; rollout is progressive with numeric abort thresholds and a rehearsed rollback; drift between declared and observed configuration is alerted; and every flag has an owner and a removal date. The team can answer "if this goes wrong, what exactly do we do?" for any change, without improvising.

**Signs of Excellence:**
- Every change has a written rollback or forward-fix path
- Selectors are tested as carefully as the changes they scope
- Drift alerts name the declaring file and the observed value
- Rollbacks have been executed at least once outside production

**Signs of Dysfunction:**
- Production config edited by hand
- "It's only config" in a review comment
- A rollback plan that has never been run
- Flags at 100% with no owner

## Verification

Run this sequence. Do not proceed past a failure.

1. **Reversibility check.** Is every change classified reversible or irreversible, and does each have a rollback or forward-fix path? If any is unclassified, stop and fix R1.
2. **Schema check.** Does every config value have a type, range or allowed set? If any is unconstrained, stop and fix R2.
3. **Validation check.** Does validation run both in CI (schema) and on the target (state)? If only one, stop and complete Decision Tree 2.
4. **Selector check.** Has the selector been proven to match exactly the intended targets? If unverified, stop and fix R3.
5. **Rollout check.** Are abort thresholds numeric and is the rollout progressive? If it applies to all targets at once, stop and fix R3.
6. **Rehearsal check.** Has the rollback or forward-fix been executed once outside production? If only documented, stop — it is unproven.
7. **Drift check.** Does divergence between declared and observed configuration raise an alert? If only detectable, stop and fix R4.

**Pass criteria:** All seven checks pass before applying the change.

## Verification Guardrails **(STANDARD)**

### Pre-Generation
- [ ] The change set and environment topology are available
- [ ] Every config value has a declaring file (or is marked undeclared)
- [ ] The target environment is identified and reachable for pre-apply validation

### Post-Generation
- [ ] No change is unclassified for reversibility
- [ ] No config value is unconstrained
- [ ] No change applies to all targets without a staged path or written justification
- [ ] Drift detection is active and alerts

## References **(QUICK)**

- `references/additional-resources.md` — change-class taxonomy, validation gate patterns, worked rollout arithmetic, and incident narratives
- `scripts/verify-skill.sh` — runnable verification harness for this skill
- Related: `ci-cd-builder`, `release-manager`, `site-reliability-engineer`, `incident-responder`, `resilience-pattern-engineer`

## Gotchas **(STANDARD)**

| Gotcha | Cost if missed | Fix |
|--------|----------------|-----|
| Blast radius by count instead of dependency graph | "1% of instances" takes down 100% of traffic — a **$100,000–$1,000,000** class outage | Verify the selector; map dependencies |
| Irreversible change with a rollback claim | Rollback fails mid-incident; recovery runs **$50,000–$500,000** | Classify reversibility; forward-fix plan + human gate (R1) |
| Unvalidated config | Fails at runtime in production; debugging typically **$10,000–$100,000** | Schema + pre-apply validation on the target (R2) |
| Undetected drift | An unreviewed, unrollbackable change; **$10,000–$100,000** in diagnosis | Alert on divergence between declared and observed (R4) |
| Rollback never rehearsed | Discovered broken during the incident it was meant for | Execute it once outside production |
| Flag at 100% with no owner | Permanent untested code path; removal becomes its own risky change | Owner + removal date at creation (R5) |
| Certificate expiry with no inventory | Time-triggered outage independent of any code change | Inventory expiries; automate renewal; alert early |
| Selector untested | The change is safe; its scope is not | Test the selector as carefully as the change (R3) |
| Config change reviewed less than code | Config changes correlate with *higher* severity | Apply R6: identical review and staging |
