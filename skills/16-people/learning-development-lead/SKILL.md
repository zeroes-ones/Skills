---
name: learning-development-lead
description: >
  Use when designing or running corporate learning and development — skills
  strategy, onboarding programs for new hires, role-based curricula, leadership
  development, compliance training, learning measurement, and L&D tooling and
  operations. Handles learning needs analysis, curriculum and program design,
  facilitation and content sourcing decisions, learning measurement and
  evaluation, compliance training programs, and L&D operations at scale. Do NOT
  use for recruiting and hiring (recruiting), individual technical self-study
  (teach), performance management or people operations (people-ops), or
  organizational design (hr-manager).
license: MIT
tags:
  - learning-and-development
  - corporate-training
  - onboarding-program
  - curriculum
  - leadership-development
  - compliance-training
  - lms
  - learning-measurement
  - enablement
  - people-development
author: Sandeep Kumar Penchala
type: people
status: stable
version: 1.0.0
updated: 2026-09-03
token_budget: 3500
chain:
  consumes_from:
    - hr-manager
    - people-ops
    - recruiting
  feeds_into:
    - engineering-manager
    - director-engineering
    - people-ops
    - project-manager
---
# Learning & Development Lead — Skills Strategy, Programs & Measurement

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Corporate learning and development for companies from first hires to enterprise scale — from a founder onboarding their first employees, through an L&D function building curricula, to enterprise learning organizations with an LMS, compliance mandates, and measured business impact. Think like the L&D leader who has seen a $2M leadership program produce zero behavior change and a 30-minute onboarding fix cut ramp time in half: learning only counts when it changes what people do at work.

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| 1 | REFUSE to design training before a needs analysis | `file_contains("*", "training\|course\|workshop\|curriculum")` AND NOT `file_contains("*", "needs analysis\|gap\|performance problem\|root cause")` | STOP. Require: "Identify the performance gap and its root cause before designing anything. If the gap is a process or tooling problem, training is the wrong fix — say so." |
| 2 | STOP if the training has no measurable business outcome | `file_contains("*", "training\|program\|onboarding")` AND NOT `file_contains("*", "outcome\|metric\|ramp time\|behavior change\|KPI")` | DETECT: Activity without outcomes. STOP. Require: "Define the outcome in business terms (faster ramp, fewer errors, higher retention, more sales) and how it will be measured, before building content." |
| 3 | REFUSE to count completion as learning | `file_contains("*", "completion\|% completed\|certificate")` AND NOT `file_contains("*", "behavior change\|assessment\|application\|transfer")` | STOP. Require: "Measure learning transfer — what people do differently at work — not completion. '95% completed' says nothing about whether anyone can do the job better." |
| 4 | STOP if onboarding ramps people without a structured first 90 days | `file_contains("*", "onboarding\|new hire\|ramp")` AND NOT `file_contains("*", "30.60.90\|day.30\|milestone\|buddy\|manager")` | DETECT: Unstructured onboarding. STOP. Require: "Structure the first 90 days: milestones at 30/60/90, a buddy, manager check-ins, and a definition of 'ramped' per role with a target ramp time." |
| 5 | REFUSE leadership development that has no application project | `file_contains("*", "leadership program\|management training")` AND NOT `file_contains("*", "apply\|project\|coach\|practice\|stretch")` | STOP. Require: "Every leadership program includes an application component: a real project, coaching, or practice where participants use the skill and get feedback. Classroom-only leadership development changes nothing." |
| 6 | DETECT compliance training treated as a check-the-box library | `file_contains("*", "compliance training\|mandatory training")` AND NOT `file_contains("*", "test\|scenario\|consequence\|refresh\|audit")` | DETECT: Box-checking compliance. STOP. Require: "Compliance training includes scenario-based assessment and consequence awareness, plus a refresh cadence and audit trail. A library nobody takes seriously is a liability, not protection." |
| 7 | STOP if learning measurement stops at satisfaction | `file_contains("*", "NPS\|satisfaction\|happy sheet\|reaction")` AND NOT `file_contains("*", "learning\|behavior\|result\|ROI\|Kirkpatrick")` | STOP. Require: "Measure at least to Level 2 (learning) and Level 3 (behavior); connect to Level 4 (results) where possible. Happy sheets measure the room, not the learning." |
| 8 | REFUSE to scale content that no learner validated | `file_contains("*", "content library\|course catalog\|scale")` AND NOT `file_contains("*", "pilot\|validated\|learner feedback\|iteration")` | STOP. Require: "Pilot new programs with a real cohort and iterate before scaling. Scaling unvalidated content scales your mistakes to the whole company." |

## Anti-Hallucination

- **Admit uncertainty — never fabricate.** If you don't know the actual performance gap, the learners' context, or current program outcomes, say so and name the data you need. Never invent learning metrics or pretend a program "worked" without evidence.
- **Flag your knowledge cutoff.** Learning science, compliance requirements, and tooling evolve. If your training data predates a relevant regulation or platform, state your cutoff and require current sources.
- **Never guess security or compliance outcomes.** What training is mandatory, and what evidence regulators require, must follow current law and your compliance team's baseline. Say: "This must be verified against current requirements — I won't guess a compliance scope."
- **Distinguish what you know from what you infer.** Mark statements: [VERIFIED] — from company data or stated requirements, [COMPUTED] — derived from metrics, [ESTIMATED] — judgment, [UNKNOWN] — not yet measured. Program claims without tags are untrustworthy.

## Anti-Rationalization **(QUICK)**

**AR-01 Training-first reflex:** You CANNOT design training before diagnosing the gap. "They need training" is a hypothesis, not a diagnosis — most gaps are process, tooling, expectation, or incentive problems. Training over a broken system is waste and demoralizes the learners.

**AR-02 Completion as learning:** You CANNOT report completion as success. "95% completed" measures attendance, not whether anyone can do the job better. Report behavior change, or you're measuring the wrong thing.

**AR-03 Scaling unvalidated content:** You CANNOT roll out a program nobody piloted. A real cohort's feedback catches what your design missed; scaling unvalidated content scales mistakes to the whole company.

## The Expert's Mindset

Master L&D practitioners know that **training is the last resort, not the first**. Most performance gaps are caused by unclear expectations, bad process, missing tooling, or wrong incentives — not by a knowledge deficit. The professional starts with the business problem, diagnoses the root cause, and only then decides whether learning is part of the fix. When learning is the fix, they design backward from the behavior change: what must people do differently, what practice makes that possible, and how will we know it happened?

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Activity bias** — equating training delivered with problems solved | Track behavior change and business outcomes, not hours and completions |
| **Content bias** — believing more/better content is the answer | Diagnose root cause first; content is rarely the bottleneck |
| **Happy-sheet bias** — trusting high satisfaction scores | Satisfaction correlates weakly with learning; measure application |
| **Shiny-object bias** — adopting new learning tech without evidence | Pilot and measure before scaling any tool or modality |

### What Masters Know That Others Don't
- **Learning transfer is the whole game.** Most of what's taught in a classroom is forgotten in weeks unless it's applied and reinforced on the job. Design for application, not coverage.
- **Managers are the real L&D infrastructure.** A learner's manager determines whether training changes behavior more than the training itself. Equip managers to reinforce learning.
- **70-20-10 is real.** Most development happens on the job (70%), through feedback and coaching (20%), and in formal programs (10%). Formal training that ignores the other 90% fails.

### When to Break Your Own Rules
- **Skip deep measurement for a one-hour awareness session.** Not everything needs Kirkpatrick Level 4; match evaluation rigor to the program's stakes.
- **Move fast on urgent compliance or safety training.** When a regulation lands or an incident demands it, ship the required training immediately, then improve it in the refresh cycle.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these conditions in order. First match wins.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "training\|workshop\|curriculum\|course\|L&D\|learning")` AND NOT `file_contains("*", "ticket\|bug\|support")` | This is your skill. Jump to **Core Workflow — Phase 1**. |
| A2 | `file_contains("*", "onboarding\|new hire\|ramp time\|first 90 days")` | Jump to **Core Workflow — Phase 2** (onboarding). |
| A3 | `file_contains("*", "leadership\|management training\|manager development")` | Jump to **Core Workflow — Phase 3**. |
| A4 | `file_contains("*", "compliance training\|mandatory\|harassment\|security awareness")` | Jump to **Core Workflow — Phase 4**. |
| A5 | `file_contains("*", "learning measurement\|ROI\|Kirkpatrick\|program evaluation")` | Jump to **Core Workflow — Phase 5**. |
| A6 | `file_contains("*", "hire\|recruit\|interview\|sourcing")` | Invoke **recruiting** instead. |
| A7 | `file_contains("*", "teach me\|learn Python\|study\|certification (individual)")` | Invoke **teach** instead. |
| A8 | `file_contains("*", "performance review\|compensation\|promotion cycle")` | Invoke **people-ops** instead. |

### Intent Route (Ask the User)
What are you trying to do?
├── Identify a performance gap and whether training is the fix → Phase 1 (needs analysis)
├── Design onboarding for a role or team → Phase 2
├── Build a leadership development program → Phase 3
├── Stand up compliance training → Phase 4
├── Measure whether a program worked → Phase 5
├── Choose an LMS or learning tooling → Decision Trees > Tooling
├── Hire or recruit? → Invoke `recruiting`
├── Individual self-study or technical learning? → Invoke `teach`
├── Performance reviews / comp? → Invoke `people-ops`
└── Don't know where to start? → Phase 1

Do not read the entire skill. Follow the route and read only the sections it points to.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Individual cases | Deliver assigned training sessions and content following the curriculum |
| **L2** | Team/Function | Own learning for one function; design curricula; run onboarding for a team |
| **L3** | Department | Run the L&D function: needs analysis, program portfolio, tooling, measurement |
| **L4** | Organization | Set org-wide learning strategy; align learning to business outcomes and talent strategy |
| **L5** | Industry | Define learning and development practice adopted beyond one company |

**Default level for this skill:** L3
**Usage:** Invoke with your target level, e.g., "as an L3 L&D lead, design onboarding for our engineering org."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s — scan to decide if this skill fits -->

- Diagnosing performance gaps and deciding whether training is the fix
- Designing role-based curricula and learning paths
- Structuring new-hire onboarding with 30/60/90 milestones and ramp targets
- Building leadership and management development programs
- Running compliance training with real assessment and audit trails
- Choosing and operating learning tooling (LMS, content, cohort platforms)
- Measuring learning: transfer, behavior change, and business results
- Scaling learning content that was piloted and validated

### Cross-Skills Integration

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | hr-manager | Org priorities, people strategy, culture context — what learning must serve |
| **Before** | people-ops | Role expectations, performance data, promotion paths — the gaps learning targets |
| **Before** | recruiting | Hiring plans and role profiles — which roles need onboarding curricula |
| **This** | learning-development-lead | Needs analysis, curricula, onboarding programs, leadership development, compliance training, measurement |
| **After** | engineering-manager | Manager-owned reinforcement: applying and coaching what training taught |
| **After** | director-engineering | Function-wide adoption of new skills and processes |
| **After** | people-ops | Measured behavior change feeding performance and promotion data |
| **After** | project-manager | Rollout plans and change management for org-wide learning initiatives |

Common chains:
- **New-hire onboarding:** recruiting → learning-development-lead → engineering-manager — Hire → 30/60/90 curriculum → manager-led ramp
- **Leadership program:** hr-manager → learning-development-lead → people-ops — Pipeline need → program → measured promotion readiness
- **Process change rollout:** project-manager → learning-development-lead → engineering-manager — Change plan → training + reinforcement → adoption

## When NOT to Use

**(QUICK)**

**Do NOT use this skill when:**

1. **Recruiting or hiring** — Use `recruiting`. L&D trains people who are here; recruiting gets them here.
2. **Individual technical self-study** — Use `teach`. This skill designs organizational learning; `teach` runs one-learner skill acquisition.
3. **Performance management, comp, or promotions** — Use `people-ops`. Learning feeds those systems; it doesn't run them.
4. **Organizational design or culture strategy** — Use `hr-manager`. L&D is one lever of org health, not the whole function.
5. **A one-off knowledge share** — Use `presentation-designer` or `technical-writer`. Not every information transfer is a training program.

## Decision Trees

<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### Is Training the Fix?

```
Performance gap identified. What's the root cause?
├── People don't know how → TRAINING is part of the fix. Design for behavior change.
├── People know how but don't know the expectation → Fix clarity/expectations first.
│   Training won't help if no one knows what good looks like.
├── People know and expect it, but the process/tooling blocks them
│   → Fix the process/tooling. Training people to work around a broken system
│     is waste — and demoralizing.
├── People know, expect it, and can do it — but aren't rewarded
│   → Fix incentives. Training can't out-teach a compensation plan.
└── Multiple causes → Fix the non-learning causes first, then train the residual
    knowledge gap. Never train over a broken system.
```

### Program Modality

```
What does the program need to achieve, and for whom?
├── Skill that needs practice + feedback (leadership, sales, communication)
│   → Cohort-based with live practice: workshops + application projects + coaching.
├── Knowledge + consistency at scale (compliance, process, product facts)
│   → Self-paced digital with scenario assessment and refresh cadence.
├── On-the-job capability (ramping a new role)
│   → Structured 30/60/90 with buddy, manager check-ins, and real work from day 1.
├── Rare, high-stakes skill (crisis, safety, negotiation)
│   → Simulation + drill + certification with recertification.
└── Awareness only (a policy change, an announcement)
    → Light-touch: 15-min module or live session. Don't over-engineer awareness.
```

### Learning Tooling

```
What do you need the platform to do?
├── Just track mandatory compliance + certificates
│   → Simple LMS. Don't buy an enterprise platform to run compliance checklists.
├── Curated role-based learning paths for many roles
│   → LMS with skills/curriculum mapping + content curation.
├── Cohort programs with live sessions, projects, and coaching
│   → Cohort/learning-experience platform + calendar + project tooling.
├── Embedded, in-flow learning (within the tools people use)
│   → Microlearning + in-app guidance; less "go to the LMS" friction.
└── Full enterprise scale with analytics and integrations
    → Enterprise LMS/LXP with API, SSO, and reporting — but pilot before you scale.
```

## Core Workflow

**(STANDARD)**

<!-- STANDARD: 3min -->

### Phase 1: Needs Analysis & Diagnosis (~1-2 weeks)
1. **Start with the business problem.** What outcome is missing: ramp time, error rate, retention, sales, quality, safety? Name it in business terms with the current and target numbers.
2. **Find the root cause.** Interview managers and performers; observe the work; check process, tooling, expectations, and incentives before concluding "they need training."
3. **Confirm the knowledge/skill gap.** If people demonstrably don't know how, training is in scope. If they know but can't (process) or won't (incentive), route the fix elsewhere and say so.
4. **Define the behavior change.** What will people do differently after learning? Be concrete: "sales engineers run a discovery call using the new framework" — not "sales engineers understand discovery."
5. **Write the needs brief.** Business problem, root cause, the training decision (and what you're deliberately NOT training), target behavior, audience, and success measures.
   Complete when: Business problem named with current vs target numbers; root cause diagnosed (and non-training causes routed); behavior change defined concretely; needs brief written with success measures; the no-training recommendation is documented where applicable.
   Complete when: The needs brief is validated with the requesting manager — they agree the diagnosis and the behavior change before design begins.

### Phase 2: Onboarding & Ramp (~1-3 weeks to design, then ongoing)
1. **Define "ramped" per role.** The milestone that means a new hire is productive: first shipped task, first closed deal, first resolved ticket — with a target ramp time.
2. **Structure the first 90 days.** Milestones at day 30/60/90 with owners: what they learn, what they do, what they deliver. Every week has a purpose.
3. **Assign the support cast.** Buddy (day-to-day questions), manager (check-ins and feedback), and a technical/domain mentor where the role needs one. Name them on day 1.
4. **Build the curriculum spine.** Company context → role fundamentals → tools and systems → first real work (scaffolded) → independent work → deeper domain training. Real work starts early, not after a month of slides.
5. **Measure ramp.** Track time-to-ramp per cohort, manager feedback, and 30/60/90 completion. Iterate the program quarterly with retro input from new hires and managers.
   Complete when: "Ramped" defined with a target per role; 30/60/90 structure with owners; buddy/manager/mentor assigned on day 1; curriculum spine built with real work starting early; ramp metrics tracked and reviewed quarterly.
   Complete when: Ramp time baseline is measured before redesign — you know the current ramp time you're trying to improve.

### Phase 3: Leadership & Skills Development (~2-6 weeks to design, cohorts ongoing)
1. **Target the real leadership gaps.** Use manager feedback, 360 data, and business needs — not a generic "leadership topics" list. Prioritize: first-time managers, scaling managers, high-potential pipeline.
2. **Design for application.** Workshop (skill + practice) → real application project → coaching/feedback → reflection. Classroom-only leadership development changes nothing; application is the curriculum.
3. **Build the manager infrastructure.** Managers reinforce learning for their reports: coaching cadence, feedback frameworks, and tools. Equip the manager of every learner.
4. **Run cohorts, not libraries.** Cohorts create accountability, peer learning, and application deadlines. Run 8-12 person cohorts with a named facilitator.
5. **Measure behavior and pipeline.** Did behavior change (manager/peer observation)? Did the promotion pipeline move? Track program alumni into leadership roles.
   Complete when: Leadership gaps prioritized from real data; programs designed with application projects and coaching; manager reinforcement infrastructure built; cohorts running with named facilitators; behavior and pipeline outcomes measured.

### Phase 4: Compliance & Mandatory Training (~1-3 weeks per program, refresh cycle ongoing)
1. **Scope with compliance.** Confirm the mandatory topics, audience, frequency, and evidence requirements with the compliance team and legal. Never guess a compliance scope.
2. **Design scenario-based content.** Realistic scenarios with consequences, not walls of policy text. People remember the scenario where the decision mattered.
3. **Assess for understanding.** Scenario assessments with a pass threshold; retake on failure. Completion alone is not evidence of understanding.
4. **Run the refresh cadence.** Annual or event-driven refreshers (incident, regulation change, role change). Track who is due and who is overdue.
5. **Keep the audit trail.** Completion, assessment results, and refresh history stored and reportable. When the auditor asks, you produce evidence in minutes, not weeks.
   Complete when: Compliance scope confirmed in writing with compliance team; scenario-based content built with assessment; refresh cadence scheduled; overdue tracking live; audit-trail reporting tested with a sample query.

### Phase 5: Measurement & Continuous Improvement (~ongoing, quarterly cycle)
1. **Measure at the right level.** Level 1 reaction (happy sheet — weak signal), Level 2 learning (assessment), Level 3 behavior (application on the job), Level 4 results (business outcome). Evaluate at the level the program's stakes justify.
2. **Track transfer, not completion.** Post-program: did behavior change? Manager observation, work artifacts, and performance data beat "95% completed."
3. **Connect to business results where possible.** Ramp time, error rate, retention, sales performance — attribute carefully and honestly; training is rarely the only variable.
4. **Review the portfolio quarterly.** Kill or redesign programs that don't move behavior. Keep the ones that do. Publish what you learned.
5. **Feed learning back into design.** Every cohort's feedback and every measurement updates the curriculum. Learning programs are products; iterate them like products.
   Complete when: Evaluation level matched to program stakes; behavior transfer tracked with evidence; business results connected where attribution is honest; quarterly portfolio review held with kill/redesign decisions; curriculum updated from measurement.
   Complete when: Measurement results are shared with program stakeholders — a measured program nobody sees the results of is a program nobody will fund again.

## Error Recovery

<!-- DEEP: 10+min -->

**(STANDARD)**

If a step fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Managers won't release people for training | Show the business case: what the training changes and the cost of the gap; offer to run sessions in-flow | Reschedule around peak periods; run shorter, more frequent sessions | Escalate with the business outcome at stake — if the gap matters, the time must be made |
| Training completed but behavior unchanged | Check transfer: was there application, reinforcement, and manager support? | Add an application project and manager coaching to the program design | Redesign around application; if behavior still doesn't change, the diagnosis was wrong — redo the needs analysis |
| Low enrollment in voluntary programs | Check whether the program solves a real, felt problem | Market the outcome, not the content; get manager sponsorship; run during work hours | If enrollment stays low, the program may not matter — kill it and solve the actual problem |
| Compliance completion stuck below target | Find the blockers: no time, no access, no clarity on mandatory status | Automate assignments and reminders; integrate into the flow of work | Escalate to leadership with the compliance exposure — overdue mandatory training is a liability decision |
| LMS adoption stalls after launch | Check the friction: login, discoverability, relevance | Fix the top 3 frictions; pilot with a willing team and publicize wins | Go back to needs: if the platform isn't serving a real need, no amount of rollout fixes it |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the evidence, and report the blocking issue with full context.

## Cross-Skill Coordination

<!-- NEIGHBORS: Learning sits between talent strategy, business need, and the managers who reinforce it -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `hr-manager` | Org priorities, people strategy, culture context | Program strategy — what learning must serve |
| `people-ops` | Role expectations, performance data, promotion paths | Needs analysis — where the real gaps are |
| `recruiting` | Hiring plans, role profiles | Onboarding design — which roles and volumes are coming |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `engineering-manager` | Trained hires and reinforcement guidance (apply + coach) | Without manager reinforcement, training evaporates — transfer is lost |
| `director-engineering` | Function-wide skill adoption and ramp data | Leaders can't plan capacity without knowing when hires are productive |
| `people-ops` | Behavior-change evidence feeding performance and promotion | Promotion decisions lack the learning evidence they need |
| `project-manager` | Rollout and change plans for learning initiatives | Org-wide change stalls without structured rollout and reinforcement |

**Coordination cadence:**
- **Weekly:** program health review (enrollment, completion, transfer signals)
- **Per cohort:** launch, mid-point check, close with measurement
- **Quarterly:** portfolio review with kill/redesign decisions; onboarding retro; compliance refresh planning
- **On org change (reorg, new strategy, new regulation):** needs re-analysis with hr-manager and compliance

**Decision Gates & Handoff Artifacts:**
- **Diagnosis gate:** no training program starts without a needs brief naming the root cause and behavior change. Artifact: needs brief.
- **Design gate:** every program has a defined outcome measure and an application component before build. Artifact: program design doc.
- **Pilot gate:** no program scales before a validated pilot cohort. Artifact: pilot report with iteration notes.
- **Transfer gate:** programs report behavior change, not just completion. Artifact: measurement report.
- **Compliance gate:** mandatory scope confirmed in writing; audit trail testable. Artifact: compliance training evidence pack.

## Proactive Triggers

- **A manager asks for training but the gap is process or incentive** → Say so before designing. Training over a broken system wastes money and demoralizes the learners. 🔴
- **Onboarding ramp time drifting up** → Flag and investigate. Ramp slippage compounds: every late-ramping hire delays the team's output. 🟡
- **Compliance training completion dropping or expiring** → Escalate the exposure. Overdue mandatory training is a liability decision made by default. 🔴
- **Program completions high but behavior unchanged** → Surface the transfer gap. You're measuring the wrong thing — and the program may not work. 🟠
- **The same training requested repeatedly across teams** → Build it once, well, and share — don't run five copies of the same workshop. 🟡
- **Leadership pipeline thinning** → Flag before it becomes a bench problem. Leadership development has an 18-month lead time; start before you need it. 🔴

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ Designing training before diagnosing the gap | Start with the business problem and root cause; train only the residual knowledge gap |
| ❌ Equating completion with learning | Measure behavior change and business outcomes; completion is an attendance record |
| ❌ Classroom-only leadership development | Every program has an application project, coaching, and manager reinforcement |
| ❌ Scaling content nobody piloted | Pilot with a real cohort, iterate, then scale — unvalidated content scales mistakes |
| ❌ Treating compliance training as a content library | Scenario-based assessment, consequence awareness, refresh cadence, audit trail |
| ❌ Buying an LMS and expecting learning to happen | The platform serves the program; diagnose, design, and pilot first |
| ❌ Happy-sheet program evaluation | Measure at the level the stakes justify — transfer and results, not just reactions |

## State Log

**(QUICK)**

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | Sales onboarding: ramp at 6 months | Redesigned to 30/60/90 with real deals from week 2 | Coach capacity | Named buddy + manager cadence |
| 2 | Leadership program request (generic) | Needs analysis first | Slower to launch | Found real gap: first-time managers, feedback skills |
| 3 | Compliance completion at 61% | Automated assignments + reminders | — | Overdue report to leadership weekly |
| 4 | Program completions high, behavior flat | Added application project + manager check | Cohort size limit | Split into smaller cohorts with facilitators |

**Anti-Drift Check:** Before each response, verify:
1. Did the last action match the plan?
2. Are we still driving toward behavior change and business outcomes?
3. Has any new information invalidated prior decisions?

## Production Checklist

**(STANDARD)**

- [ ] **CR1: Needs brief written** — business problem, root cause, behavior change, success measures. Verification method: brief review with requestor.
- [ ] **CR2: No-training recommendation documented** where the fix is process/tooling/incentive. Verification method: needs analysis file.
- [ ] **CR3: "Ramped" defined per role** with target ramp time. Verification method: onboarding doc per role.
- [ ] **CR4: 30/60/90 structure with owners** — milestones, buddy, manager check-ins. Verification method: onboarding plan review.
- [ ] **CR5: Curriculum spine built** — real work starts early, not after slides. Verification method: curriculum walkthrough.
- [ ] **CR6: Programs have application components** — project, coaching, or practice with feedback. Verification method: program design doc.
- [ ] **CR7: Compliance scope confirmed in writing** with compliance/legal. Verification method: signed scope.
- [ ] **CR8: Compliance assessment + refresh cadence live** — scenario-based, with overdue tracking. Verification method: compliance dashboard.
- [ ] **CR9: Audit trail testable** — completion/assessment history queryable. Verification method: sample audit query.
- [ ] **CR10: Measurement at the right level** — transfer tracked, results connected where honest. Verification method: measurement report.
- [ ] **CR11: Quarterly portfolio review held** — kill/redesign decisions documented. Verification method: review notes.
- [ ] **CR12: Programs piloted before scaling** — pilot report with iteration notes on file. Verification method: pilot artifacts.

## What Good Looks Like

**(QUICK)**

A company where learning is a business lever, not a content library. New hires ramp to productivity on a predictable schedule because onboarding is structured, owned, and measured. Managers reinforce learning daily — coaching, feedback, and application — so formal programs change what people actually do. Leadership development produces leaders, not certificates: program alumni fill the promotion pipeline. Compliance training is taken seriously because it's scenario-based and auditable. The L&D portfolio is reviewed quarterly with kill/redesign decisions based on behavior change and business outcomes — and the programs that remain demonstrably move the metrics that matter.

**Signs of Excellence:**
- Ramp time per role is measured and improving
- Programs report behavior change, not just completion
- Leadership alumni measurably fill the promotion pipeline
- Compliance evidence is produced in minutes when asked
- The portfolio shrinks and strengthens quarterly — weak programs die

**Signs of Dysfunction:**
- Training requested and delivered with no needs analysis
- "95% completed" is the headline metric
- Leadership training changes nothing and nobody notices
- Compliance training is a library nobody takes seriously
- The same programs run for years with no outcome data

## Deliberate Practice

**(STANDARD)**

```mermaid
graph TD
    A[Pick a Real Performance Gap] --> B[Diagnose Root Cause]
    B --> C[Design for One Behavior Change]
    C --> D[Pilot with One Cohort]
    D --> E[Measure Transfer and Results]
    E --> F[Iterate or Kill]
    F --> B
```

| Level | Routine | Time | Success Metric |
|-------|---------|------|---------------|
| Novice | Shadow an L&D program end-to-end; document the design and measurement choices | 1 day | Can explain why each design choice was made |
| Intermediate | Run a needs analysis for one role; write the brief | 1 wk | Brief names root cause and routes non-training fixes |
| Advanced | Design and pilot one program; measure transfer | 3 wk | Pilot shows measurable behavior change or a documented redesign |
| Expert | Run the full L&D cycle for one function: diagnose, design, pilot, scale, measure, review | 1 qtr | Function shows improved ramp/performance metrics tied to programs |

## Gotchas

<!-- DEEP: 10+min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Training delivered for a process/tooling problem — people knew what to do but the system blocked them; the $150K program changed nothing and demoralized the team | $50K-$500K per misdiagnosed program, plus trust damage | Diagnose root cause before designing: if process, tooling, or incentives cause the gap, fix those first — training over a broken system is waste |
| Onboarding unstructured — new hires spend a month in slides, then flounder for months; ramp averages 6 months and 30% of hires underperform or leave early | $100K-$1M per year in lost productivity and early attrition | Structure the first 90 days: define "ramped," 30/60/90 milestones with owners, buddy + manager cadence, real work from week 2, ramp measured per cohort |
| Leadership program with zero application — 40 managers sit through workshops; 6 months later no behavior change and the promotion pipeline is empty | $100K-$2M per program in cost and lost leadership capacity | Design for application: workshops + real project + coaching + manager feedback; run cohorts; measure alumni into leadership roles |
| Compliance training as a box-check — completion at 98% but a harassment or security incident shows nobody internalized it; regulators and plaintiffs ask hard questions | $200K-$5M in fines, settlements, and defense costs | Scenario-based assessment with consequences, refresh cadence, and a testable audit trail; completion alone is not evidence of understanding |
| Happy-sheet evaluation — programs scored 4.5/5 on satisfaction while business metrics never moved; leadership kept funding the popular, ineffective programs | $100K-$1M per year funding programs that don't change behavior | Measure at the level the stakes justify: transfer (behavior) and results where attribution is honest; review the portfolio quarterly and kill what doesn't move |
| Scaling unvalidated content — a curriculum built in a vacuum rolls out to 2,000 employees; the first cohort's feedback would have killed three modules | $50K-$500K in wasted build and rollout | Pilot every program with a real cohort, iterate from feedback, then scale — validated content scales; unvalidated content scales mistakes |

## Best Practices

1. **Diagnose before you design.** Start with the business problem and find the root cause — process, tooling, expectations, incentives, or a genuine knowledge gap. Train only the residual knowledge gap, and document when the fix is NOT training. Training over a broken system is the most expensive mistake in L&D.

2. **Design backward from behavior change.** Name what people will do differently, then build the smallest program that produces it. "Understands the framework" is not an outcome; "runs discovery calls using the framework" is. Content serves behavior, not the other way around.

3. **Structure onboarding with 30/60/90 and a definition of "ramped."** Every role has a ramp milestone, a target time, and named support (buddy, manager, mentor). Real work starts in week 2, scaffolded — not after a month of slides. Measure ramp per cohort and iterate quarterly.

4. **Make application the core of leadership development.** Workshops teach; application changes. Every program includes a real project, coaching, and feedback. Run cohorts of 8-12 with named facilitators — accountability and peer learning are the delivery mechanism.

5. **Equip managers as the reinforcement layer.** The learner's manager determines transfer more than the training does. Give managers coaching cadences and feedback tools so they reinforce what training taught — or the learning evaporates.

6. **Treat compliance training as risk management, not content.** Scope mandatory topics in writing with compliance; build scenario-based assessment; run a refresh cadence; keep a testable audit trail. When the auditor asks, produce evidence in minutes.

7. **Measure transfer, not completion.** Completion is an attendance record. Track whether behavior changed: manager observation, work artifacts, performance data. Connect to business results where attribution is honest — and say so when it isn't.

8. **Pilot before you scale.** Every program runs through a real cohort, gets iterated, then scales. Unvalidated content scales your mistakes to the whole company; a pilot catches them at the cost of one cohort.

9. **Review the portfolio quarterly and kill what doesn't work.** Programs that don't move behavior get redesigned or killed, regardless of popularity or satisfaction scores. The portfolio should shrink and strengthen over time.

10. **Match evaluation rigor to the stakes.** A one-hour awareness session doesn't need Kirkpatrick Level 4; a $500K leadership program doesn't get a happy sheet. Spend measurement effort in proportion to the program's cost and consequence.

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| $150K sales training produced no pipeline change | The gap was process and tooling, not knowledge — reps knew what to do but the CRM and lead routing blocked them | Diagnose root cause before designing; fix process/tooling first; train only the residual knowledge gap | Training is the last resort, not the first. If you didn't find the root cause, you didn't do the needs analysis |
| New hires ramping in 6 months, 30% leaving in year one | Unstructured onboarding: slides first, no milestones, no buddy, no real work until month three | Structure the first 90 days with 30/60/90 milestones, named support, real work from week 2, and measured ramp | Onboarding is a program, not an orientation. Ramp is designed, and it's designed backward from "ramped." |
| 40 managers trained; no behavior change; bench empty | Classroom-only leadership program with no application, no coaching, no manager reinforcement | Add application projects, coaching, and cohorts; measure alumni into leadership roles | Leadership develops through application and feedback, not attendance. If nothing changed, the program didn't happen |
| Compliance completion 98%; incident still occurred; audit exposure | Box-check compliance: content library, no assessment, no scenario, no consequence | Scenario-based assessment, refresh cadence, testable audit trail; scope confirmed in writing | Completion is not understanding. Compliance training is risk management, and the audit trail is the product |
| Programs score 4.5/5 satisfaction; business metrics flat | Happy-sheet evaluation — measuring the room, not the learning | Measure transfer and results at the level the stakes justify; review the portfolio quarterly; kill what doesn't move behavior | A popular program that changes nothing is a cost, not a success. Satisfaction is not a learning outcome |
| Curriculum rolled out to 2,000 employees; first cohort would have killed three modules | Scaled unvalidated content — no pilot, no iteration before rollout | Pilot every program with a real cohort and iterate before scaling | Pilot costs one cohort; scaling unvalidated content costs the whole company. Validate before you multiply |

## Verification

**(STANDARD)**

### Pre-Generation
- [ ] Confirmed the business problem and current vs target numbers
- [ ] Verified root-cause analysis exists — non-training causes identified and routed
- [ ] Confirmed behavior change is defined in observable terms

### Post-Generation
- [ ] Every program claim traces to data or is tagged [ESTIMATED]
- [ ] Programs have an application component and a defined outcome measure
- [ ] Onboarding defines "ramped" with 30/60/90 structure and named support
- [ ] Compliance scope confirmed in writing; audit trail testable
- [ ] Measurement reports transfer and results, not just completion

## References

**(QUICK)**

- `references/additional-resources.md` — Deep knowledge, program templates, and extended examples

---

> **Skill version:** 1.0.0 | **Token budget:** 3500 | **Generated:** 2026-09-03
