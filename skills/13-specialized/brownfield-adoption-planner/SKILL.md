---
name: brownfield-adoption-planner
description: >
  Use when planning the phased rollout of agent skills into an existing, brownfield
  codebase with production traffic, where safety and team trust are paramount. Handles
  four-phase adoption (read-only safety net → context + characterization tests →
  development for new features → devops/observability), risk assessment per phase,
  team buy-in strategies, rollback planning, and gradual skill enablement. Do NOT use
  for greenfield projects (route to PROJECT-BOOTSTRAP.md), emergency hotfixes (route
  to incident-responder), or regulatory compliance (route to compliance-officer).
license: MIT
tags:
  - brownfield-adoption
  - phased-rollout
  - team-change-management
  - legacy-modernization
  - risk-management
  - skill-adoption
author: Sandeep Kumar Penchala
type: specialized
status: stable
version: 1.0.0
updated: 2026-07-27
token_budget: 3000
chain:
  consumes_from:
    - system-architect
    - security-reviewer
    - compliance-officer
    - codebase-design
    - business-strategist
  feeds_into:
    - code-reviewer
    - qa-engineer
    - incremental-implementation
    - ci-cd-builder
    - observability-engineer
    - code-simplification
    - teach
---

# Brownfield Adoption Planner

> **Portability target:** Works in Claude Code, Copilot CLI, Cursor, Codex, and Gemini CLI. No agent-specific features required.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Anti-Hallucination
<!-- STANDARD: 3min -->

* Admit uncertainty. If you cannot identify all integration points in the legacy codebase, state which paths remain unverified.
* Flag assumptions. If you assume a certain service boundary without reading the code, mark it as assumed.
* Flag your knowledge cutoff. If the codebase uses frameworks or patterns you have not seen, pause and ask the team before recommending changes.
* Never recommend unsafe changes. If a codebase lacks tests, the first phase must add tests — never suggest refactoring without a safety net.
* Never guess security. If a phase touches authentication, payments, or compliance, route to security-reviewer and compliance-officer before proceeding.
* [VERIFIED] before any migration: Legacy tests pass. New tests cover the extraction boundary. Backward compatibility contract is signed off.

## When to Use
<!-- STANDARD: 3min -->

* Introducing agent skills into an existing project with more than ten thousand lines of code
* Migrating from no automation to full skill coverage without disrupting delivery
* The team is skeptical of AI tooling and needs a low-risk on-ramp
* The codebase has no tests and adding tests is a prerequisite to skill adoption
* A brownfield system needs modernization but cannot be rewritten
* Regulatory or compliance constraints prevent greenfield approaches

> If you catch yourself rationalizing, stop. The rationalizations below are traps.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

| # | Rule | Mechanical Trigger | Violation Response |
|---|------|-------------------|-------------------|
| 1 | Every adoption phase adds one safety skill before any mutation skill | Phase plan lists skills; grep shows mutation skills before safety skills | Reject the plan. Reorder phases |
| 2 | No mutation skill is used on code without passing tests | Attempt to use edit/create on file not in covered_files list | Block operation. Route to phase safety gate |
| 3 | Each phase has an acceptance gate that blocks the next phase | Phase completion checklist not fully checked | Halt. Retire outstanding checks |
| 4 | Read-only skills ship in Phase 0, same day as install | install.sh runs; no read-only skill config found | Fail install. Add read-only skill config |
| 5 | Phase rollback is a documented one-line command | Phase N gate fails and no documented rollback step | Block phase. Document rollback first |

## Route the Request
<!-- STANDARD: 3min -->

This is a map, not a recipe. Start at the top and follow the matching branch.

~~~
INCOMING: Team wants to adopt agent skills in an existing project
|
+-- What type of project?
|   +-- GREENFIELD (less than 1000 LOC, no production traffic)
|   |   -> Route to PROJECT-BOOTSTRAP.md (greenfield path)
|   |   -> No need for brownfield adoption plan
|   |
|   +-- BROWNFIELD (more than 10000 LOC, active production traffic)
|       |
|       +-- Does the project have a test suite?
|       |   +-- YES -> Test coverage above 60 percent?
|       |   |   +-- YES -> Start at Phase 1: Read-Only + Context
|       |   |   +-- NO  -> Start at Phase 0: Safety Net
|       |   +-- NO  -> Start at Phase 0: Safety Net (non-negotiable)
|       |
|       +-- Team is AI-SKEPTIC?
|       |   +-- YES -> Phase 0 sends read-only artifacts for manual review
|       |   +-- NO  -> Phase 0 runs automatically in CI
|       |
|       +-- Regulatory constraints?
|           +-- YES -> Add compliance-officer to Phase 0 safety net
|           +-- NO  -> Proceed with standard phases
~~~

## The Expert's Mindset
<!-- STANDARD: 3min -->

1. **Safety before speed.** A brownfield project has years of hard-won stability. Disrupting that with aggressive automation erodes trust and endangers the business. Phase 0 installs guardrails, not bulldozers.
2. **Read-only first, mutation later.** The people who built this system have battle scars you do not know about. Read-only skills surface their knowledge; mutation skills apply yours.
3. **Gates are not optional.** Every phase has a measurable acceptance gate. If the gate does not pass, the next phase does not start. This is the fundamental difference between adoption and chaos.
4. **Every phase is independently valuable.** The team should see benefit after Phase 0 finishes, even if they stop there. No phase should feel like a prerequisite tax.

## Operating at Different Levels
<!-- STANDARD: 3min -->

### Level 1: Quick (Basic Assessment)
* Run the adoption readiness checklist
* Identify the first codebase target: smallest service or module with git activity in the past thirty days
* Output Phase 0 plan: install code-reviewer and security-reviewer skills
* Measure: coverage_report.md, security_findings.md in the first week
* **Complete when:** Phase 0 skills running, first read-only artifact delivered

### Level 2: Standard (Team Rollout)
* Full four-phase plan for one codebase with timeline and ownership
* Phase 0: Read-only safety skills with manual review workflow
* Phase 1: Context skills plus test harness addition
* Phase 2: Development skills for new features only — existing code is protected
* Phase 3: DevOps and observability for technical debt pay-down
* **Complete when:** All four phases complete, team self-sufficient with skills

### Level 3: Deep (Organization Rollout)
* Multi-codebase adoption with codebase-specific risk assessment
* Brownfield adoption playbook customized to team topology
* Integration with existing CI/CD and code review workflows
* Metrics dashboard: adoption rate, error rate, team satisfaction, time saved
* Run business-strategist to model ROI of full adoption
* **Complete when:** Three or more codebases at Phase 2 or higher, dashboard operational

### Level 4: Exploration (Strangler Fig Migration)
* Run system-architect to identify extraction candidates
* Each extracted service becomes greenfield for skill adoption
* Old monolith receives Phase 0 and Phase 1 only
* Migration roadmapped over quarters, not sprints
* **Complete when:** First extracted service running independently with full skill coverage

## Core Workflow
<!-- STANDARD: 3min -->

### Phase 0: Safety Net (Week 0-1)

**Objective:** Prove skills add value without risking the codebase.

| Step | Action | Skill | Artifact |
|------|--------|-------|----------|
| 1 | Install the skills repo | — | .claude/skills/ or equivalent |
| 2 | Run code-reviewer on PR #N | code-reviewer | review_report.md |
| 3 | Run security-reviewer on auth and payment paths | security-reviewer | security_findings.md |
| 4 | Run accessibility-auditor on main user flows | accessibility-auditor | a11y_audit.md |
| 5 | Deliver findings to team for manual review | — | Consolidated report |
| 6 | **Gate:** Team agrees findings are useful | — | Signed acceptance email |

**Complete when:** All four artifacts produced and reviewed. Zero code changes made by skills.

### Phase 1: Read-Only + Context (Week 1-3)

**Objective:** System understanding without modification. Add safety tests where needed.

| Step | Action | Skill | Artifact |
|------|--------|-------|----------|
| 1 | Run system-architect on one module | system-architect | architecture_doc.md |
| 2 | Run codebase-design on dependency graph | codebase-design | dependency_map.md |
| 3 | Add characterization tests to most-changed module | qa-engineer | characterization_tests/ |
| 4 | Run technical-writer on onboarding docs | technical-writer | onboarding_guide.md |
| 5 | **Gate:** Characterization tests pass in CI | — | CI status: green |
| 6 | **Gate:** Team reviews and approves architecture doc | — | Signed review |

**Complete when:** Architecture understood, characterization tests green, onboarding docs updated.

### Phase 2: Development for New Features (Week 3-8)

**Objective:** Skills participate in new feature delivery. Existing code is off-limits for mutation.

| Step | Action | Skill | Artifact |
|------|--------|-------|----------|
| 1 | Select a new feature with well-defined scope | — | Feature spec |
| 2 | Run incremental-implementation with feature flags | incremental-implementation | VS-0 through VS-N PRs |
| 3 | Run code-reviewer on each PR | code-reviewer | Review comments |
| 4 | Run qa-engineer for integration tests | qa-engineer | Integration suite |
| 5 | **Gate:** Feature ships with zero production incidents | — | Monitoring report |
| 6 | **Gate:** Team independently runs development skills | — | Team survey |

**Complete when:** One feature delivered end-to-end with skills. Team comfortable with workflow.

### Phase 3: DevOps + Observability (Week 8+)

**Objective:** Pay down technical debt. Add monitoring and alerting skill coverage.

| Step | Action | Skill | Artifact |
|------|--------|-------|----------|
| 1 | Run ci-cd-builder to review pipeline | ci-cd-builder | Pipeline audit |
| 2 | Run observability-engineer on one service | observability-engineer | Dashboard spec |
| 3 | Run dependency-governance on package.json | dependency-governance | Dependency report |
| 4 | Run code-simplification on most complex module | code-simplification | Refactor plan |
| 5 | **Gate:** Monitoring dashboards operational | — | Screenshot or URL |
| 6 | **Gate:** Dependency vulnerabilities addressed | — | Zero critical CVEs |

**Complete when:** CI/CD improved, dashboards live, dependencies audited, refactor plan approved.

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: Phase Sequencing

~~~
Codebase assessment complete
|
+-- Test coverage below 40 percent?
|   +-- YES -> Phase 0: Add characterization tests FIRST
|   +-- NO  -> Is team AI-skeptical?
|              +-- YES -> Phase 0: Read-only with manual review
|              +-- NO  -> Can team dedicate one engineer to skill enablement?
|                         +-- YES -> Start Phase 1: Read-only + Context
|                         +-- NO  -> Phase 0 only until capacity exists
~~~

### Decision Tree 2: Safety Gate

~~~
Phase N gate checklist presented
|
+-- All gates pass?
|   +-- YES -> Proceed to Phase N + 1
|   +-- NO  -> Which gate failed?
|              +-- Test failure -> Fix tests. Re-run gate
|              +-- Team rejection -> Gather feedback. Adjust plan
|              +-- Production incident -> Rollback phase. Post-mortem. Retry
~~~

### Decision Tree 3: When to Stop

~~~
Phase 2 complete
|
+-- Is the team self-sufficient with skills?
|   +-- YES -> Consider Phase 3 optional. Focus on sustaining adoption
|   +-- NO  -> Add coaching phase. Run teach skill
|
+-- Is the codebase fully modernized?
    +-- YES -> Transition to greenfield steady state (PROJECT-BOOTSTRAP.md)
    +-- NO  -> Continue Phase 3 for debt pay-down
~~~

## Production Checklist
<!-- STANDARD: 3min -->

Before deploying or delivering work from this skill, verify:

| # | Check | Verify |
|---|-------|--------|
| ☐ | Phase 0 read-only artifacts delivered: architecture map, dependency graph, risk hotspots, and code health report all present | All artifacts exist in `adoption_artifacts/` directory; tech lead has reviewed and signed off on findings |
| ☐ | Characterization tests cover top-5 most-changed files with ≥80% line coverage | Run coverage report on test suite; verify `coverage.json` shows ≥80% line coverage on the identified high-churn files |
| ☐ | Safety skills deployed before any mutation skill: linter, security scanner, and code-reviewer active and configured | Verify Phase 1 skill configuration precedes Phase 2 configuration; mutation skills blocked at gate until safety skills pass |
| ☐ | Team sign-off documented per phase: acceptance confirmation (email, Slack thread, or PR approval) for each completed phase gate | Acceptance trail exists for current phase and all prior phases; no phase advanced without documented sign-off |
| ☐ | Feature flag or kill switch present for every skill-introduced code change: every mutation has a disable path | Audit recent skill-authored changes: every diff has corresponding feature flag toggle or documented revert path |
| ☐ | Phase rollback tested: one-line rollback command reverts to pre-phase state with zero manual intervention | Execute documented rollback command in staging environment; verify system returns to prior operational state without errors or data loss |
| ☐ | CI/CD pipeline stability maintained: pipeline reliability (success rate) and duration (P95) within 10% of pre-adoption baseline | Compare pipeline metrics before and after each phase adoption; alert if metrics regress beyond 10% threshold |
| ☐ | Rollback plan is documented and tested | Per-phase rollback runbook exists in adoption artifacts; tested in non-production environment within last 30 days; rollback time <15 minutes |

## Verification
<!-- STANDARD: 3min -->

| Complete When | Evidence |
|---|---|
| Complete when Phase 0 read-only artifacts delivered | Markdown files in adoption_artifacts/ directory |
| Complete when team signed off on Phase 0 findings | Signed acceptance email or Slack thread |
| Complete when characterization tests cover top-5 most-changed files | Test files with coverage_report.json |
| Complete when architecture doc reviewed by two engineers | Review comments resolved |
| Complete when feature shipped with feature flags, zero incidents | Monitoring dashboard showing zero errors |
| Complete when team independently uses three or more skills | Survey response or usage metrics |
| Complete when CI/CD pipeline audit completed | Pipeline audit report |
| Complete when dashboards operational with alerts configured | Screenshot or URL to dashboard |
| Complete when phase rollback tested successfully | Rollback run log showing phase reversal |
| Complete when adoption milestones document updated | milestones.md with dates and metrics |

## Best Practices
<!-- STANDARD: 3min -->

1. **Phase 0 is non-negotiable.** Read-only skills must prove value before any mutation skills are introduced.
2. **One codebase at a time.** Do not roll out across multiple codebases simultaneously until one is at Phase 3.
3. **Team buy-in per phase.** Each phase gate includes team sign-off. Skipping this creates resistance that compounds.
4. **Rollback per phase.** Document the exact command sequence to undo each phase before starting it.
5. **Metrics from day one.** Track: time saved, bugs caught, team sentiment, adoption percentage.
6. **Brownfield greenfield boundary.** New features built from scratch within the brownfield codebase should follow greenfield skill patterns.
7. **Characterization tests before refactoring.** Tests that capture current behavior, not ideal behavior.
8. **Skill enablement engineer.** Designate one team member as the skill champion for each phase.
9. **Migration dashboard visibility.** Everyone sees adoption progress — builds momentum and accountability.
10. **Celebrate phase completions.** Each phase is a milestone. Recognize the team.

## Anti-Patterns
<!-- STANDARD: 3min -->

| Pattern | Correction |
|---|---|
| Skipping Phase 0 because we already trust skills | Trust is earned per-codebase, not assumed |
| Running mutation skills on untested code | Add characterization tests first. Always |
| Adopting all skills at once | Four phases, gated. Each phase is at most four skills |
| Treating brownfield as greenfield | Brownfield has production users. Risk profile is entirely different |
| No rollback plan per phase | Every phase must have a documented one-step rollback |
| Ignoring team resistance | Resistance is a signal. Adjust the plan, not the message |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

1. **Testing the untestable:** Twenty-year-old codebase with zero tests. Cost: $20,000 to $80,000 if you skip characterization tests and refactor blind. **Fix:** Characterization tests capture current behavior before any refactoring.
2. **Silent integration breaks:** Changing an internal API consumed by five teams. Cost: $15,000 to $50,000 in cascading incidents. **Fix:** Run dependency-governance before any API change.
3. **CI/CD pipeline brittleness:** Pipeline fails intermittently on old code. Cost: $5,000 to $15,000 per week in lost velocity. **Fix:** Phase 0 freezes pipeline changes. Phase 3 audits and stabilizes.
4. **Team trust collapse:** One bad skill-generated PR erodes team confidence. Cost: $50,000 to $200,000 — the entire adoption initiative fails. **Fix:** Phase 0 produces only read-only artifacts. Phase 2 starts with feature flags and safe defaults.
5. **Regulatory breach:** Skill-generated code violates PCI or HIPAA. Cost: $100,000 to $2,000,000 in fines plus remediation. **Fix:** Add compliance-officer to Phase 0 if regulated. Never skip compliance gates.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

### Upstream (call before planning)

| Upstream Skill | When to Call |
|---|---|
| system-architect | Understanding legacy architecture before planning adoption |
| security-reviewer | Codebase handles auth, payments, or PII |
| compliance-officer | Regulated industry: HIPAA, PCI, SOC2, FedRAMP |
| codebase-design | Mapping dependency graph for Phase 1 targeting |
| business-strategist | Modeling ROI of brownfield adoption |

### Downstream (call during execution)

| Downstream Skill | When to Call |
|---|---|
| code-reviewer | Phase 0 and Phase 2 — review PRs |
| qa-engineer | Adding characterization tests in Phase 1 |
| incremental-implementation | New feature delivery in Phase 2 |
| ci-cd-builder | Pipeline audit in Phase 3 |
| observability-engineer | Dashboard setup in Phase 3 |
| code-simplification | Technical debt pay-down in Phase 3 |
| teach | Team training after each phase |

## Proactive Triggers
<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---|---|---|
| Phase gate fails twice | Pause adoption. Retrospective. Adjust plan | Repeating failure pattern needs root-cause analysis |
| Team satisfaction drops below neutral | Stop. Survey. Address concerns before proceeding | Adoption without buy-in is sabotage |
| Production incident attributed to skill output | Rollback phase immediately. Post-mortem | Trust is the foundation of adoption |
| Skill usage drops for two weeks | Check in with team. Identify friction | Silent abandonment is worse than rejection |
| Phase 0 artifacts receiving no reviews | Escalate. Find champion | Unused output means adoption is stalled |

## What Good Looks Like
<!-- STANDARD: 3min -->

**Correct:**

~~~
Phase 0 complete: billing-service
* code-reviewer: 12 findings over 3 PRs (8 accepted, 2 rejected, 2 discussion)
* security-reviewer: 3 findings (1 high-severity SQL injection, fixed)
* Team sign-off: ✅ (Sarah, Engineering Lead)
* Phase 1 gate: ✅ (characterization tests green, architecture doc approved)
* Phase 1 start: Tuesday
* Rollback: rm -rf adoption_artifacts/phase0 && git restore .

~~~

**Counter-example (reject):**

~~~
"We installed skills and started refactoring. Four bugs in production.
Team is upset. Rollback took two days because we didn't plan it."

~~~

## Deliberate Practice
<!-- STANDARD: 3min -->

1. **Risk assessment drill:** Assess a codebase you know well using the adoption readiness checklist. Identify three risk points.
2. **Characterization test exercise:** Pick a function without tests. Write three characterization tests that capture observed behavior.
3. **Phase gate design:** Design gates for a hypothetical Phase 4 that your organization might need.
4. **Rollback drill:** Document the rollback steps for your current development environment. Verify it works.
5. **Stakeholder map:** List everyone who could block skill adoption. Plan a one-on-one with each.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

1. **Phase gate failed, team wants to proceed anyway:** Escalate to engineering manager. Gates are not optional. Cost of skipping: erosion of the entire adoption framework.
2. **Skill-generated code caused a production incident:** Rollback the phase. Post-mortem with security-reviewer present. The skill is not to blame — the phase gate was insufficient. Strengthen the gate. Cost: one to three days.
3. **Team champion left the organization:** Pause adoption. Identify new champion. Run teach skill with new champion. Restart from current phase. Cost: one to two weeks.
4. **Characterization tests reveal undocumented behavior:** This is expected and GOOD. Document the behavior. Consult product-manager if behavior contradicts spec. Cost: one to two days per finding.
5. **Legacy dependency blocks Phase 3:** Dependency cannot be upgraded. Escalate to system-architect for containment strategy. Phase 3 may be deferred for that module. Cost: ongoing but contained.

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

* [ ] Phase 0: Read-only skills installed and producing artifacts
* [ ] Phase 0: Team sign-off received
* [ ] Phase 1: Architecture documented
* [ ] Phase 1: Characterization tests green in CI
* [ ] Phase 1: Gate passed, Phase 2 authorized
* [ ] Phase 2: First feature shipped with skills, zero incidents
* [ ] Phase 2: Team self-sufficient with development skills
* [ ] Phase 3: CI/CD audit complete
* [ ] Phase 3: Dashboards operational
* [ ] Adoption metrics dashboard live

## References
<!-- STANDARD: 3min -->

* [PROJECT-BOOTSTRAP.md](../../../PROJECT-BOOTSTRAP.md) — Greenfield adoption path
* [code-reviewer](../../../personas/code-reviewer.md) — Read-only review persona
* [security-reviewer](../../06-quality/security-reviewer/SKILL.md) — Security audit skill
* [incremental-implementation](../../05-development/incremental-implementation/SKILL.md) — Safe feature delivery
* [system-architect](../../04-architecture/system-architect/SKILL.md) — Architecture understanding
* [qa-engineer](../../06-quality/qa-engineer/SKILL.md) — Test suite creation
* [teach](../../12-people/teach/SKILL.md) — Team training
* [Strangler Fig Application (Martin Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html)
* [Characterization Tests (Michael Feathers)](https://michaelfeathers.silvrback.com/characterization-testing)
