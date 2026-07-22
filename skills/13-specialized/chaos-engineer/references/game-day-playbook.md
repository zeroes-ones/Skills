# GameDay Playbook

> Battle-tested facilitation guide for planning, executing, and following up on Chaos Engineering GameDays.

---

## Table of Contents

1. [Pre-Game (2 Weeks Before)](#pre-game-2-weeks-before)
2. [GameDay Day (Day Of)](#gameday-day-day-of)
3. [Post-Game (Within 1 Week)](#post-game-within-1-week)
4. [Appendix](#appendix)

---

## Pre-Game (2 Weeks Before)

### Experiment Selection

Prioritize experiments based on a weighted scoring system:

| Criterion | Weight | Scoring (1-5) |
|-----------|--------|----------------|
| Recent incident in this failure mode | 5 | 5 = incident last month, 1 = never happened |
| Service criticality (revenue/user impact) | 4 | 5 = customer-facing checkout/payments, 1 = internal tool |
| Untested failure mode | 3 | 5 = never tested, 1 = tested and passed in last GameDay |
| New resilience feature deployed | 3 | 5 = new circuit breaker shipped this sprint, 1 = no changes |
| Cross-team dependency | 2 | 5 = involves 3+ teams, 1 = single team |

**Selection process:**
1. List all candidate experiments from the experiment catalog.
2. Score each using the table above.
3. Select top 3–5 experiments for the GameDay.
4. Ensure at least one experiment targets a recent incident failure mode.
5. Ensure at least one experiment tests a new resilience feature.
6. Ensure no more than one experiment involves the same service (avoid overloading one team).

### Team Assembly

Minimum 3 people. Scale up based on number of services involved.

| Role | Count | Required Skills |
|------|-------|-----------------|
| **Commander** | 1 | Strong incident command skills, calm under pressure, decision-maker |
| **Operator** | 1–2 | Hands-on with chaos tooling (kubectl, Chaos Mesh, Gremlin, AWS FIS), can execute experiments |
| **Observer** | 1–2 | Monitoring/observability expert, knows dashboards and alerting, can diagnose in real time |
| **Scribe** | 1 | Documentarian, takes timestamped notes, compiles findings |

**Note:** The Commander and Operator cannot be the same person. The Commander must be decision-free — not executing commands — so they can focus on abort decisions, timeline management, and communication.

### Observability Check

For each experiment, verify the following BEFORE GameDay:

1. **Dashboards**: Open the latency, error rate, throughput, and saturation dashboards for each service in scope. Confirm they show live data.
2. **Alerts**: Confirm alerts for the expected impact exist and are configured correctly. Test: what alert will fire when this fault is injected?
3. **Logging**: Verify logs are flowing with correlation IDs. Run a test request and trace it end-to-end.
4. **Tracing**: Verify distributed traces capture the service-to-service calls that will be affected.
5. **Health endpoints**: Confirm `/health`, `/ready`, and `/metrics` endpoints return 200 for all services in scope.

**Pre-flight test**: Run each experiment in staging at least 24 hours before GameDay. If observability gaps are found during the pre-flight, fix them before GameDay or remove the experiment from the agenda.

### Stakeholder Communication

**Email template — Leadership:**

```
Subject: Chaos GameDay — [Date] — [Service(s)] Resilience Verification

Team,

We will be conducting a Chaos Engineering GameDay on [Date] from [Start]
to [End] PT. The objective is to verify the resilience of [service names]
under controlled failure conditions.

Scope:
- Services: [list services]
- Experiments: [list experiments, e.g., pod termination, network latency]
- Blast radius: [scope limitations]
- Environment: [staging / production with canary / production]

Safety:
- All experiments have auto-abort conditions based on error rate and latency
  thresholds
- Manual kill switch available and tested
- Blast radius limited to [scope]

Expected impact: [none / minimal latency increase / no customer impact]

Point of contact: [Commander name] during the exercise.

We will share findings within 1 week.

- [Your name]
```

**Email template — Adjacent Teams:**

```
Subject: Heads up — Chaos GameDay affecting [service names]

Hi team,

On [Date] we're running a Chaos Engineering GameDay that will affect
[service names]. Your service may experience [latency increase / errors /
degraded responses] from these services during [time window].

What you need to do:
- Nothing. Your service should handle this gracefully.
- If you see alerts from [service names], do NOT page — they're expected.
- If you see alerts from YOUR OWN services, page immediately.

We'll post updates in #chaos-gameday Slack channel.

Questions? Ping [name].
```

### Schedule

- Pick a low-traffic window (typically 9 AM–1 PM PT Tuesday–Thursday avoids both morning peak and Friday deploys).
- Block 3–4 hours. Do NOT schedule during known campaign/event periods (Black Friday, Prime Day, product launches).
- Send calendar invites with the title format: `[GameDay] [Services] — [Date]`
- Include in the invite: link to this playbook, link to experiment catalog, Slack channel for communications.

### Rollback Prep

For each experiment, verify:
1. The abort mechanism works (auto-termination trigger, manual kill switch).
2. Rollback steps are documented and tested.
3. The team knows who has authority to call an abort (Commander and any engineer).
4. Rollback is time-bounded: can you stop ALL experiments within 30 seconds?

**Rollback verification checklist:**
- [ ] Chaos Mesh: `kubectl delete chaosnetworkchaos <name>` works immediately
- [ ] Gremlin: Halt attack stops within 5 seconds
- [ ] AWS FIS: `aws fis stop-experiment` works
- [ ] LitmusChaos: `kubectl delete chaosengine <name>` stops immediately
- [ ] Custom scripts: kill process / restore config within 5 seconds

### Dry Run

Run through each experiment in staging at least once before GameDay. Fix everything that breaks. If an experiment fails in staging, either fix the underlying issue or remove it from the GameDay agenda.

**Dry run checklist:**
- [ ] Experiment injects correctly
- [ ] Observability detects the injection
- [ ] Alerts fire as expected
- [ ] Abort mechanism works
- [ ] Rollback works and system returns to baseline
- [ ] No unexpected side effects
- [ ] Scribe can observe and document effectively
- [ ] Estimated timing is accurate (adjust GameDay schedule)

---

## GameDay Day (Day Of)

### Timeline

| Time | Activity | Duration | Owner |
|------|----------|----------|-------|
| 9:00 | Briefing | 15 min | Commander |
| 9:15 | Experiment 1 | 45 min | Operator + Observer |
| 10:00 | Break + Huddle | 15 min | All |
| 10:15 | Experiment 2 | 45 min | Operator + Observer |
| 11:00 | Break | 15 min | All |
| 11:15 | Experiment 3 | 45 min | Operator + Observer |
| 12:00 | Debrief | 30 min | Commander |
| 12:30 | Done | — | — |

### Briefing (15 Minutes)

Agenda:
1. **Introductions** — everyone states name, role (Commander/Operator/Observer/Scribe).
2. **Review experiments** — Commander walks through each experiment: name, hypothesis, fault, blast radius, abort conditions.
3. **Review abort conditions** — Commander reads aloud the abort conditions for each experiment. Everyone must agree they understand when to abort.
4. **Communication channel** — All communications in `#chaos-gameday` Slack channel. No DMs during experiments.
5. **Emergency protocol** — If the kill switch is activated, all experiments stop. Everyone post: "ACK" in the channel. If you don't ACK in 2 minutes, Commander pages you.
6. **Code word** — Establish a code word for abort if needed over voice/video. Example: "RESET" or "ABORT NOW."

### Experiment Execution Flow

Each experiment follows this protocol:

```
Commander:  "Starting Experiment 1: [name]. Hypothesis: [hypothesis]."
Operator:   "Injecting fault now." [runs command]
Observer:   [watches dashboards — reports what they see]
            "I see latency increase from 50ms to 200ms on the checkout dashboard."
            "Error rate is 0.0% — no errors."
            [continues reporting at 1-minute intervals or on significant changes]
Scribe:     [records start time, injection time, every observation, every decision]
Commander:  "Continue monitoring." or "Abort — error rate exceeded threshold."
            If abort: "Experiment [name] is ABORTED. Operator, stop fault injection."
Operator:   "Fault stopped. [confirms rollback complete]"
Observer:   "Metrics returning to baseline. [confirms recovery]"
Scribe:     [records end time, recovery time, verdict]
```

### Communication Templates

**Pre-GameDay Slack message:**
```
@channel Chaos GameDay begins at 9:00 AM PT.
We're testing: checkout-service (pod termination, network latency) and
orders-service (dependency failure).
Blast radius: 1–2 pods, us-east-1a only, internal traffic only.
Abort if: error rate > 1% on ANY service, P99 latency > 2s, or any P0 alert.
Watch #chaos-gameday for live updates.
```

**Experiment start:**
```
:rocket: Experiment 1 START: check-out-pod-kill-single
Hypothesis: When 1 checkout pod is terminated, remaining pods handle traffic
with P99 < 500ms and 0 errors.
Injecting fault now.
```

**Mid-experiment update:**
```
:bar_chart: Experiment 1 — 2 min in.
Latency P99: 320ms (baseline: 250ms) — within hypothesis.
Error rate: 0.0% — no errors.
Pods: 2/3 healthy, 1 terminating. ReplicaSet creating replacement.
```

**Abort:**
```
:rotating_light: ABORT — Experiment 1 ABORTED.
Error rate on checkout-service exceeded 2% threshold.
Operator, stop all fault injection.
```

**Experiment success:**
```
:white_check_mark: Experiment 1 COMPLETE — Hypothesis CONFIRMED.
Latency P99 stayed below 500ms (observed max: 420ms).
Error rate: 0.0% throughout.
Recovery time: 12 seconds to baseline.
```

**Experiment failure:**
```
:x: Experiment 1 COMPLETE — Hypothesis REFUTED.
Latency P99 reached 2.1s (threshold: 500ms).
Circuit breaker did not open within expected 30s window.
Action item: investigate circuit breaker configuration.
```

**Break announcement:**
```
:coffee: 15-minute break. Next experiment at 10:15.
[optional: quick findings from experiment 1]
```

**Debrief announcement:**
```
:memo: All experiments complete. Debrief starting now in [room/link].
Findings report by end of week.
Thanks everyone! :tada:
```

### Role Cheat Sheets (In-Experiment)

#### Commander
- **Your job**: Lead. Decide abort/continue. Communicate.
- **Do NOT**: Run tooling, look at dashboards, troubleshoot.
- **Say**: "Start experiment X." "Continue monitoring." "Abort." "Good, next experiment."
- **When to abort**: Error rate > threshold. Latency > threshold. Alert fires. Team member calls abort. Gut feeling (trust it).
- **Remember**: Aborting early is always OK. An abort is a successful abort — proving you can stop is a finding.

#### Operator
- **Your job**: Run experiment commands. Stop experiments. Verify rollback.
- **Do NOT**: Make abort decisions. Diagnose issues. Communicate findings.
- **Say**: "Injecting fault now." "Fault injected." "Fault stopped." "Rollback confirmed."
- **Key skill**: Speed. If Commander says "Abort," you stop the fault within 5 seconds. Practice your abort commands.

#### Observer
- **Your job**: Watch dashboards. Report findings. Diagnose.
- **Do NOT**: Run commands. Make abort decisions (but DO call out threshold breaches).
- **Say**: "Latency is [value]." "Error rate is [value]." "I see an alert firing." "Circuit breaker just opened." "The dashboard shows [pattern]."
- **Key skill**: Context. Report metrics RELATIVE TO BASELINE. Don't just say "latency is 500ms" — say "latency increased from baseline 250ms to 500ms."

#### Scribe
- **Your job**: Every. Single. Thing. Gets. Recorded.
- **Must record**: Experiment name, hypothesis, start time, injection time, every observation from Observer, every decision from Commander, abort time, recovery time, rollback time, verdict.
- **Do NOT**: Participate in discussion. Your job is to type.
- **Template to follow:**

```
[09:15:00] Experiment 1: check-out-pod-kill-single
[09:15:00] Hypothesis: When 1 checkout pod is terminated...
[09:15:10] Operator: Injecting fault
[09:15:12] Observer: Pod terminating. Other 2 pods healthy.
[09:15:30] Observer: Latency P99 320ms (baseline 250ms). No errors.
[09:15:45] Observer: New pod starting. 3/3 pods expected.
[09:16:00] Observer: All 3 pods healthy. Latency returned to 260ms.
[09:16:30] Commander: Experiment complete. Hypothesis confirmed.
[09:16:30] Verdict: CONFIRMED
```

---

## Post-Game (Within 1 Week)

### Findings Report Template

```
# GameDay Findings Report — [Date]

## Overview
- **Date**: [date]
- **Services tested**: [list]
- **Participants**: [roles + names]
- **Environment**: [staging / production]
- **Number of experiments**: [N]
- **Hypotheses confirmed**: [N]
- **Hypotheses refuted**: [N]

## Experiment Results

### Experiment 1: [name]
- **Hypothesis**: [hypothesis]
- **Verdict**: [CONFIRMED / REFUTED / INCONCLUSIVE]
- **Observed max latency**: [value] (threshold: [value])
- **Observed error rate**: [value] (threshold: [value])
- **Recovery time**: [value]
- **What worked**: [summary]
- **What broke**: [summary]

### Experiment 2: [name]
...

## Key Findings
1. [Finding 1 — e.g., "Circuit breaker on orders-service does not open within expected threshold"]
2. [Finding 2 — e.g., "Connection pool exhaustion caused cascading failure to upstream services"]
3. [Finding 3 — e.g., "Observability detected all injected faults within 2 minutes"]

## Action Items
| # | Action | Severity | Owner | Ticket | Due |
|---|--------|----------|-------|--------|-----|
| 1 | Fix circuit breaker threshold on orders-service | P0 | [name] | [link] | [date] |
| 2 | Add connection pool timeout to payment-service client | P1 | [name] | [link] | [date] |
| 3 | No action needed | — | — | — | — |

## Lessons Learned (GameDay Process)
- What went well: [list]
- What to improve: [list]
- Next GameDay date: [proposed date]
```

### Action Item Tracking

Create tickets in your issue tracker within 48 hours of the GameDay. Each action item must have:

| Field | Required | Example |
|-------|----------|---------|
| Severity | Yes | P0 (critical — fix within 1 week), P1 (high — next sprint), P2 (medium — next quarter) |
| Owner | Yes | Full name or team |
| Ticket link | Yes | Link to Jira/GitHub/Asana |
| Due date | Yes | Specific date |
| Description | Yes | Clear statement of what to fix and why |
| Experiment reference | Yes | Which experiment revealed this issue |
| Verification plan | Yes | How will we verify the fix works? |

**P0 definition**: Direct customer impact, SLO violation risk, security vulnerability.
**P1 definition**: Indirect customer impact, significant observability gap, failure mode not handled.
**P2 definition**: Nice-to-have hardening, documentation gap, minor observability improvement.

### Leadership Summary

1-page executive summary. Keep it to 1 page — leadership reads bullet points, not paragraphs.

```
# Chaos GameDay Executive Summary — [Date]

## Objective
Verify the resilience of [service names] under [pod failure, network latency,
dependency failure] scenarios. All experiments run in [environment] with
blast radius limited to [scope].

## Results
- [N] of [N] experiments confirmed system resilience
- [N] experiments revealed gaps requiring remediation
- Zero customer impact during testing

## Key Findings
1. [Positive finding]: Checkout-service handled 50% pod termination without
   customer-visible impact. Circuit breaker operated correctly.
2. [Gap]: Orders-service connection pool lacks timeout configuration —
   dependency timeouts cause pool exhaustion. P0 fix required.
3. [Positive finding]: Observability detected all injected faults within
   90 seconds. Dashboards, alerts, and logging all performed as expected.

## Action Items
- 1 P0 fix (connection pool timeout) — owner: [name], due: [date]
- 2 P1 improvements — scheduled for next sprint
- 3 experiments added to automated CI/CD pipeline

## Next Steps
- Next GameDay scheduled: [date]
- Target: migrate 2 experiments from manual GameDay to automated CI/CD
- Focus areas for next quarter: [areas based on findings]

## Recommendation
Continue monthly GameDays. The team demonstrated strong incident response
capabilities and the system is resilient in most failure modes tested.
Priority hardening for [area] needed before next GameDay.
```

### Retro (GameDay Process Improvement)

After the GameDay, run a 30-minute retro focused on the GameDay process itself (not the findings — those go in the report).

**Retro format:**

| What went well | What was meh | What to improve |
|----------------|-------------|-----------------|
| [Good thing 1] | [Meh thing 1] | [Improvement 1] |
| [Good thing 2] | [Meh thing 2] | [Improvement 2] |
| [Good thing 3] | | [Improvement 3] |

**Sample retro questions:**
- Was the timeline realistic? Did we rush? Did we have too much idle time?
- Was the communication clear? Did people know what to say and when?
- Did the roles work? Were people clear on their responsibilities?
- Was the tooling easy to use? Any friction?
- Was the abort mechanism fast enough?
- Did the dry run prevent surprises? Were there any staging → prod gaps?
- What should we do differently next time?

### Experiment Catalog Update

Update the experiment catalog within 1 week of GameDay:

- [ ] Mark each experiment as `tested-in-staging` or `tested-in-production`.
- [ ] Add findings summary next to each experiment.
- [ ] Add "passed" or "failed" with the date.
- [ ] Add suggested improvements to experiment if needed.
- [ ] Create new experiments inspired by GameDay insights.
- [ ] Update experiment priority scores based on findings.

---

## Appendix

### A. Communication Templates

#### Email — Leadership Announcement (Pre-GameDay)

```
Subject: Chaos GameDay — [Date] — Resilience Verification

Team,

We will run a Chaos Engineering GameDay on [Date] from [Time] to [Time].
Scope: [services]. Blast radius: [scope]. Environment: [env].

We will inject controlled failures to verify our resilience patterns work.
Abort conditions are configured — the experiment automatically stops if
error rates or latency exceed thresholds.

Contact [Name] during the event. We'll share findings within 1 week.
```

#### Email — Findings Report (Post-GameDay)

```
Subject: GameDay Findings — [Date]

Hi team,

Our Chaos GameDay on [Date] is complete. [N] of [N] experiments confirmed
resilience. [N] experiments revealed gaps.

Summary:
[2-3 bullet points of key findings]

Action items:
[1-2 key action items with owners]

Full report: [link to report]

Next GameDay: [date]
```

#### Email — Leadership Summary (Post-GameDay)

```
Subject: Executive Summary — Chaos GameDay [Date]

[Attach or inline the 1-page executive summary]
```

#### Slack — Emergency Announcement

```
:rotating_light: ALL EXPERIMENTS STOPPED
All fault injection halted. System returning to baseline.
[If applicable: Explain what happened briefly, acknowledge, and confirm recovery.]
```

### B. Role Cheat Sheets

#### Commander Cheat Sheet

```
COMMANDER CHEAT SHEET
=====================

BEFORE GAMEDAY:
  [ ] Review experiment catalog for selected experiments
  [ ] Confirm abort conditions with team
  [ ] Set up Slack channel #chaos-gameday
  [ ] Brief stakeholders
  [ ] Verify dry run was completed

DURING GAMEDAY:
  ┌─────────────────────────────────────────────┐
  │ 1. Kick off each experiment                 │
  │    "Start Experiment X: [name]"             │
  │                                             │
  │ 2. Observe from system-level view           │
  │    (not detailed dashboards)                │
  │                                             │
  │ 3. Decide: Continue or Abort                │
  │    Trust the abort conditions.              │
  │    If in doubt, abort.                      │
  │                                             │
  │ 4. Manage timeline                         │
  │    Keep experiments on schedule.            │
  │    Skip or shorten if needed.               │
  │                                             │
  │ 5. Communicate                              │
  │    Public channel for everything.           │
  │    No side conversations.                   │
  └─────────────────────────────────────────────┘

ABORT CONDITIONS TO READ ALOUD:
  - Error rate > [threshold]
  - P99 latency > [threshold]
  - P0 alert fires
  - Anyone on the team calls "abort"
  - Gut feeling

ABORT SCRIPT:
  "ABORT — Experiment [name] is ABORTED."
  "Operator, stop all fault injection NOW."
  "Observer, confirm all metrics returning to baseline."
  [wait for confirmations]
  "Abort complete. Moving to next experiment or debrief."
```

#### Operator Cheat Sheet

```
OPERATOR CHEAT SHEET
=====================

YOUR COMMANDS — Know these by heart:

KUBERNETES (Pod Kill):
  kubectl delete pod -l app=<service> --now=true

CHAOS MESH (Network Latency):
  kubectl apply -f chaos/network-latency-200ms.yaml
  kubectl delete chaosnetworkchaos <name>

CHAOS MESH (Pod Kill):
  kubectl apply -f chaos/pod-kill.yaml
  kubectl delete chaosnetworkchaos <name>

GREMLIN:
  gremlin attack <attack-type> <target>
  gremlin halt

AWS FIS:
  aws fis start-experiment --experiment-template-id <id>
  aws fis stop-experiment --id <id>

LITMUS:
  kubectl apply -f chaosengine.yaml
  kubectl delete chaosengine <name>

ABORT = STOP EVERYTHING:
  Chaos Mesh: kubectl delete chaos --all -n <namespace>
  Gremlin: gremlin halt
  AWS FIS: aws fis stop-experiment --id <id>
  All: kubectl delete pods/networkchaos/stresschaos --all-namespaces
```

#### Observer Cheat Sheet

```
OBSERVER CHEAT SHEET
=====================

DASHBOARDS TO WATCH:
  1. Service latency (P50, P95, P99) — per endpoint
  2. Error rate (5xx, 4xx) — per service
  3. Throughput (RPS) — per service
  4. CPU/Memory — per pod
  5. Connection pool utilization
  6. Circuit breaker state
  7. Queue depth / consumer lag

WHAT TO REPORT:
  - "Latency P99 is [value], baseline was [value]."
  - "Error rate is [value]%, threshold is [threshold]%."
  - "Circuit breaker is [OPEN/CLOSED/HALF_OPEN]."
  - "I see [specific observation on dashboard]."
  - "Alert just fired: [alert name and severity]."

CADENCE:
  Report every 30-60 seconds during the fault.
  Report immediately on any threshold breach.
  Report when metrics return to baseline after recovery.

DON'T REPORT:
  "Looks OK." (Too vague — use numbers.)
  "I think..." (Say what you see, not what you think.)
  Nothing — silence is failure.
```

#### Scribe Cheat Sheet

```
SCRIBE CHEAT SHEET
==================

TIMESTAMPS ARE YOUR JOB. Every entry starts with [HH:MM:SS].

TEMPLATE — Each experiment:

=== Experiment N: [name] ===
[HH:MM] Commander: "Starting Experiment N. Hypothesis: [hyp]"
[HH:MM] Operator: "Injecting fault: [command]"
[HH:MM] Observer: "[first observation]"
[HH:MM] Observer: "[next observation]"
[...]
[HH:MM] Commander: "Continue / Abort"
[HH:MM] Operator: "Fault stopped. Rollback: [command]"
[HH:MM] Observer: "Metrics returning to baseline"
[HH:MM] Verdict: CONFIRMED / REFUTED / INCONCLUSIVE
=== End Experiment N ===

RECORD EVERYTHING:
  - Experiment name, hypothesis, verdict
  - Every metric reported (value AND threshold)
  - Every decision and who made it
  - Commands executed (what and by whom)
  - Time to inject, time to detect, time to recover
  - Any unexpected events or behaviors

AFTER GAMEDAY:
  - Compile into findings report within 48 hours
  - Highlight P0/P1 action items immediately
```

### C. Debrief Template

```
# GameDay Debrief — [Date]

## Attendance
- Commander: [name]
- Operator(s): [name(s)]
- Observer(s): [name(s)]
- Scribe: [name]
- Other attendees: [names]

## Experiment Summary

| # | Name | Verdict | Key Observation |
|---|------|---------|-----------------|
| 1 | [name] | [C/R/I] | [key observation] |
| 2 | [name] | [C/R/I] | [key observation] |
| 3 | [name] | [C/R/I] | [key observation] |

## What Worked
- [List resilience patterns that performed correctly]
- [List observability wins]
- [List team communication wins]
- [List tooling wins]

## What Broke
- [List resilience gaps found]
- [List observability gaps]
- [List unexpected behaviors]

## What We Learned
- [List insights and surprises]
- [List new failure modes discovered]

## Action Items

| # | Action | Sev | Owner | Ticket | Due |
|---|--------|-----|-------|--------|-----|
| 1 | [action] | P0 | [name] | [link] | [date] |
| 2 | [action] | P1 | [name] | [link] | [date] |
| 3 | [action] | P2 | [name] | [link] | [date] |

## Next GameDay
- Proposed date: [date]
- Proposed focus: [areas]
```

### D. Action Item Tracker Template

```
# GameDay Action Item Tracker

GameDay Date: ________________
Prepared by: ________________

| # | Experiment | Finding | Action | Severity | Owner | Ticket | Due | Status |
|---|------------|---------|--------|----------|-------|--------|-----|--------|
|   |            |         |        |          |       |        |     |        |
|   |            |         |        |          |       |        |     |        |
|   |            |         |        |          |       |        |     |        |

Severity Key:
  P0 = Critical — fix within 1 week (customer impact, SLO risk, security)
  P1 = High — next sprint (significant gap, failure not handled)
  P2 = Medium — next quarter (hardening, documentation, minor improvement)
  P3 = Low — no deadline (nice to have, aspirational)

Status Key:
  Not Started / In Progress / Done / Won't Do / Blocked
```
