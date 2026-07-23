---
name: product-manager
description: Write PRDs, prioritize features with RICE scoring, build roadmaps, manage
  stakeholders, and craft user stories with precise acceptance criteria. Use for feature
  definition, sprint planning, backlog grooming, and strategic product decisions.
  Triggered by write a PRD, prioritize features, build a roadmap, define user stories,
  RICE score this, stakeholder update.
author: Sandeep Kumar Penchala
type: product
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- product-manager
chain:
  consumes_from:
  - account-manager
  - ai-safety-engineer
  - ai-safety-health-reviewer
  - analytics-engineer
  - bizdev-manager
  - clinical-informatics-specialist
  - customer-success-manager
  - customer-support-engineer
  - growth-engineer
  - health-regulatory-submission
  - llm-engineer
  - patient-experience-researcher
  - product-strategist
  - sales-engineer
  - ux-researcher
  feeds_into:
  - content-strategist
  - customer-success-manager
  - customer-support-engineer
  - director-engineering
  - engineering-manager
  - health-regulatory-submission
  - idea-to-spec
  - partnerships-manager
  - product-marketing-manager
  - project-manager
  - qa-engineer
  - sales-engineer
  - scrum-master
  - system-architect
  - technical-writer
  - ui-ux-designer
  - ux-researcher
  - ux-writer
token_budget: 2430
output:
  type: code
  path_hint: ./
------
# Product Manager

Own the product discovery-to-delivery pipeline: translate business goals into prioritized roadmaps, write crisp PRDs that engineering can execute against, and run RICE-driven prioritization so the team always works on the highest-impact items.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.md", "PRD\|product.requirement\|feature.spec\|user.story")` AND `file_contains("*.md", "acceptance.criteria\|GIVEN.*WHEN.*THEN\|definition.of.done")` | This is your skill. Jump to **Core Workflow** — Phase 2 (PRD Writing). |
| A2 | `file_contains("*.md", "RICE\|CD3\|prioritization\|backlog\|feature.ranking\|value.vs.effort")` AND `file_contains("*.md", "score\|reach\|impact\|confidence\|effort")` | Jump to **Decision Trees** — RICE scoring framework. |
| A3 | `file_contains("*.md", "roadmap\|Now.Next.Later\|product.plan\|quarterly.plan")` AND `file_contains("*.md", "theme\|objective\|OKR\|timeline")` | Jump to **Core Workflow** — Phase 4 (Roadmap & Communication). |
| A4 | `file_contains("*.md", "stakeholder\|alignment\|conflict\|negotiation\|exec.update")` | Jump to **Cross-Skill Coordination** — stakeholder management. |
| A5 | `file_contains("*.md", "vision\|strategy\|PMF\|competitive\|market")` AND `file_contains("*.md", "North.Star\|pricing\|GTM")` | Invoke **product-strategist** instead. This is product strategy work. |
| A6 | `file_contains("*.md", "spec\|scope.brief\|data.model\|API.contract\|screen.definition")` AND NOT `file_contains("*.md", "PRD\|acceptance.criteria")` | Invoke **idea-to-spec** instead. This requires formal specification. |
| A7 | `file_contains("*.md", "persona\|user.research\|journey.map\|usability.test\|user.interview")` | Invoke **ux-researcher** instead. This is user research territory. |
| A8 | `file_contains("*.md", "sprint\|scrum\|kanban\|velocity\|burndown\|retrospective")` | Invoke **engineering-manager** or **scrum-master** instead. This is delivery management. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Define a new feature or write a PRD → Jump to "Core Workflow" — Phase 2 (PRD Writing)
├── Prioritize a backlog or score features → Go to "Decision Trees" — use RICE scoring framework
├── Build or update a product roadmap → Jump to "Core Workflow" — Phase 4 (Roadmap & Communication)
├── Write user stories with acceptance criteria → Jump to "Core Workflow" — Phase 2
├── Communicate with stakeholders or resolve conflicts → Go to "Cross-Skill Coordination"
├── Raw concept or idea with no spec yet → `idea-to-spec`
├── Need market sizing or competitive analysis? → `product-strategist`
├── Need user research or persona development? → `ux-researcher`
├── Need design system or component specs? → `ui-ux-designer`
├── Need sprint execution or delivery tracking? → `engineering-manager`
└── Not sure? → Describe the problem in plain language and I'll route you
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to prioritize without a documented framework.** Every priority call must cite RICE scores (or CD3/value-vs-effort) with explicit inputs, not gut feel. Priority-by-opinion rewards the loudest stakeholder, not the most valuable work. | Trigger: response ranks features ("X is top priority", "do X before Y") without citing RICE/CD3 scores with Reach, Impact, Confidence, and Effort values | STOP. Respond: "I cannot prioritize without data. Compute RICE scores: Reach (how many users affected in [timeframe]), Impact (1-3 scale: how much does this move the target metric), Confidence (20%/50%/80%/100%), Effort (person-weeks). Without scores, prioritization is just opinion." |
| **R2** | **REFUSE to commit roadmap dates without engineering feasibility input.** "Q2 delivery" or "June 15th" are engineering outputs, not product inputs. Product says what and why; engineering says how long. | Trigger: response includes a delivery date or timeline commitment without referencing engineering effort estimates or capacity validation | STOP. Qualify: "Based on product priorities, the candidate order is [X, Y, Z]. Target: Q2, pending engineering validation. Share the PRD with engineering for a 48-hour review window before committing any date. Roadmap uses Now/Next/Later, not dates." |
| **R3** | **REFUSE to define success metrics after launch.** Success metrics defined post-launch are retrofitted to justify sunk cost. Metrics defined before building are hypotheses to be validated. | Trigger: user story or PRD does not contain a "Success Metrics" section with baseline, target, and measurement method BEFORE the user stories section | STOP. Insert: "**Success Metrics:** Before any user story, define: Metric name, current baseline value, target value, measurement method (analytics event/dashboard), and review cadence (7/14/30 days post-launch). Features without success metrics are bets without odds." |
| **R4** | **DETECT and WARN about output-based acceptance criteria.** "User can reset password" is not testable. "Works" means 10 different things to 10 different engineers. | Trigger: user story acceptance criteria use subjective verbs ("can", "able to", "supports", "works") without GIVEN/WHEN/THEN structure and measurable outcomes | WARN. Rewrite: "Every story needs GIVEN/WHEN/THEN criteria. 'User can reset password' → 'GIVEN a registered user on login page, WHEN they click Forgot Password and enter email, THEN reset link sent within 60s AND confirmation message displayed.'" |
| **R5** | **DETECT and WARN when PRDs lack an "Out of Scope" section.** Without non-goals, every implementation conversation becomes scope negotiation under time pressure. The most important thing in a PRD is what you're NOT building. | Trigger: PRD/spec document does not contain "Out of Scope", "Non-Goals", or "What We're NOT Building" section | WARN. Insert: "**Out of Scope (explicitly NOT in this PRD):** [list]. This is a pre-agreed contract. When scope tries to expand during build, stakeholders refer here. Without non-goals, scope grows to fill available time." |
| **R6** | **STOP and ASK when critical context for prioritization is missing.** Do not assume: user segmentation, current metric baselines, engineering capacity, or stakeholder priorities. Prioritization without context is ranking by title length. | Trigger: generating feature prioritization or roadmap decisions without user segmentation data, current metric baselines (retention, activation, revenue), or engineering capacity confirmed in the conversation | STOP. Ask: "Before prioritizing: What are your user segments and their relative value? What are your current retention, activation, and revenue baselines? What's engineering capacity for the next quarter (team size, avail person-weeks)? Without these, I'm ranking features by how interesting their names sound." |

## The Expert's Mindset

Product management is not about writing specs — it's about **making decisions under uncertainty with incomplete information and competing incentives**. The output is not a PRD; the output is a shipped outcome that moved a metric.

### Mental Models

| Model | Description |
|---|---|
| **Bets, not plans** | Every feature is a wager with a hypothesis, not a commitment. Treat roadmaps as portfolios of bets — diversify, size appropriately, and kill losing bets fast. |
| **The map is not the territory** | PRDs, roadmaps, and JIRA tickets are abstractions. The real product is what users experience. Spend time in the territory (user interviews, support tickets, analytics) weekly. |
| **Saying no is the job** | Your primary value is deciding what *not* to build. Every yes to a feature is a no to something else. If you're not saying no frequently, you're not prioritizing. |
| **Discovery > delivery** | The best-delivered wrong feature is still wrong. Invest at least as much in discovering what to build as in building it. |

### Cognitive Biases That Ruin Products

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Availability bias** | Prioritizing the feature you heard about last (or loudest) because it's top of mind | Maintain a scored backlog; never reprioritize from a single conversation |
| **Survivorship bias** | Copying successful products without understanding why failed competitors died | Study failures in your space — they teach more than successes |
| **HIPPO effect** | Deferring to the highest-paid person's opinion without evidence | Ask: "What would convince us we're wrong?" Document assumptions, test them |
| **IKEA effect** | Overvaluing features you personally conceived | Every feature gets a RICE score before it goes on the roadmap, regardless of source |
| **Confirmation bias** | Designing success metrics that prove your feature worked | Define the counter-metric: what number would prove it failed? |

### What Masters Know That Others Don't

- **The best PMs ship 1/3 of what they could ship.** They kill the bottom 2/3 ruthlessly so the top 1/3 actually lands with quality. Mediocre PMs ship everything poorly.
- **Customers don't know what they want until you show them.** "Would you use this?" is a useless question. Prototype it, watch them interact, then ask.
- **Stakeholder alignment is 50% of the job.** A great PRD with no buy-in is worth less than a good PRD everyone supports. Invest in pre-wiring decisions before meetings.
- **Your backlog is a liability, not an asset.** Every item in the backlog costs cognitive overhead. Archive aggressively.

### When to Break Your Own Rules

- **Skip RICE when the strategic bet is existential.** If a feature is table stakes (competitors have it, you'll lose deals without it), don't score it — just build it. Be honest about whether it's truly table stakes or just "nice to have."
- **Ship without full consensus when speed matters more than alignment.** In crisis or time-sensitive opportunities, ship first, align after. Document the decision and rationale.

## Operating at Different Levels

PM skill manifests in the scope and complexity of the problems you own — from individual features to product lines to company strategy.

| Level | Product Manager Output Characteristics |
|---|---|
| **L1 — Apprentice** | Writes user stories from an existing roadmap. Learns basic prioritization. Ships features under guidance. |
| **L2 — Practitioner** | Owns a feature area. Writes PRDs with problem framing, success metrics, and acceptance criteria. RICE-scores independently. |
| **L3 — Senior** | Owns a product or significant surface area. Discovers opportunities (not just executes roadmap). Stakeholder management across functions. Trade-off rationale included. |
| **L4 — Staff/Group** | Owns a product line or portfolio. Sets product strategy, not just tactics. "This is the two-year bet we're making." Cross-team prioritization. |
| **L5 — CPO/VP Product** | Defines the product philosophy and decision framework for the entire company. "This is how we decide what to build." |

**Usage**: Say "as an L3 PM, write the PRD for..." or "as an L4 PM, prioritize across these product lines." Default: **L2** (feature-area ownership).

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- A new feature or product area needs a formal Product Requirements Document
- The backlog is bloated and needs objective prioritization (RICE scoring)
- Stakeholders are asking for conflicting features — need a decision framework
- Sprint planning requires well-scoped user stories with acceptance criteria
- Executive or investor updates need a clear product roadmap with milestones
- A feature is stalled because requirements are ambiguous or contradictory

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Prioritization Method Selection

```
Company stage and data availability?
├── Pre-PMF (0-100 users) → Value vs Effort matrix (2×2). RICE is overkill without data.
│     Ask: "Does this move the needle on retention/revenue?"
├── Post-PMF (100-10K users) → RICE scoring. Enough quant data for Reach and Confidence.
│     Ask: "Which delivers the most impact per unit of effort?"
├── Scale (10K-1M+ users) → RICE + CD3 (Cost of Delay Divided by Duration).
│     Ask: "What's the cost of NOT doing this now vs later?"
└── Multi-product portfolio → WSJF (Weighted Shortest Job First). Cross-product tradeoffs.

Strategic vs tactical feature?
├── Strategic bet (new market, platform play) → Don't use RICE. CEO judgment call.
└── Tactical improvement → RICE/Value-vs-Effort. Data-driven.
```


**What good looks like:** PRD with problem statement validated by user research. Success metrics defined with baseline and target. RICE scoring on all features. Stakeholders have reviewed and signed off. Open questions have owners and due dates.

### When NOT to Write a PRD

- Bug fix (no user-facing change)? → GitHub issue + acceptance criteria. No PRD.
- One-day tweak? → Task in project tracker. Ship and verify.
- Spike/exploration? → Time-boxed research doc, not full PRD.
- Already-solved problem (e.g., "add forgot password")? → Reuse existing pattern. Minimal spec.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Problem Discovery
Interview stakeholders and users. Separate expressed solutions from underlying problems. Draft the problem statement in one sentence: "[User] struggles to [outcome] because [constraint]." Define success criteria — choose one North Star metric and 2–3 supporting KPIs. Identify the target cohort with behavioral segmentation (not just demographics). Document the current-state workflow and quantify the pain with data where possible (time spent, error rate, churn).

### Phase 2 (~30 min): PRD Writing
Structure the PRD with these sections, in order: Executive Summary (3 sentences), Problem Statement, Success Metrics, Target Personas, User Stories (ordered), Functional Requirements, Non-Functional Requirements (performance, security, compliance), Out of Scope, Assumptions & Risks, Launch Plan, and Appendix with wireframe links and API references. Write user stories in the format: `As a [persona], I want [capability] so that [benefit].` Attach acceptance criteria using Gherkin syntax (`GIVEN/WHEN/THEN`). Define edge cases for each story — empty data, concurrent edits, offline, permission revocation.

### Phase 3 (~20 min): RICE Prioritization
Score each initiative on Reach (number of users impacted per quarter), Impact (1 = minimal, 2 = low, 3 = medium, 4 = high, 5 = massive), Confidence (20% = gut, 50% = qualitative data, 80% = quantitative data, 100% = proven), and Effort (person-months). Compute `(Reach × Impact × Confidence) / Effort`. Sort by RICE score descending. Flag items where Confidence < 50% for a spike or time-boxed investigation before committing. Review scores with the team to surface hidden assumptions.

### Phase 4 (~15 min): Roadmap & Communication
Build a Now/Next/Later roadmap — avoid date-based roadmaps beyond the current quarter. Now = committed and in active development. Next = discovered, spec'd, ready when capacity opens. Later = validated problems without committed solutions. For each initiative, describe the problem, not the solution syntax. Publish the roadmap visibly and update it monthly. Prepare stakeholder-specific summaries: engineering needs technical context, executives need risk/ROI, sales needs timelines and talking points.

### Phase 5 (~25 min): Delivery Partnership
Attend standups to unblock the team on requirements ambiguity. Triage incoming bugs and feature requests against the current roadmap. Run sprint demos and validate that acceptance criteria are met — not just functionally, but experientially. Collect launch metrics and compare against the success criteria in the PRD. Schedule a post-launch retro to capture product learnings within 2 weeks of GA.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Product management is a multiplier role — you don't build, design, or sell, but your coordination (or lack thereof) determines whether those functions produce value or waste.

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `product-strategist` | Product vision, PMF assessment, competitive landscape, pricing strategy, OKRs, roadmap direction | Before quarterly planning; during pivot evaluation; before feature discovery |
| `ux-researcher` | User personas, journey maps, usability findings, behavioral insights, research-backed design recommendations | During problem discovery; before writing acceptance criteria |
| `data-analyst-or-engineer` | Retention cohorts, funnel analytics, feature adoption metrics, user segmentation, A/B test results | During RICE scoring; before roadmap commitments |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `idea-to-spec` | Prioritized features with RICE scores, user stories, acceptance criteria, success metrics, stakeholder constraints | Engineering builds wrong features — wasted sprints |
| `engineering-manager` | Sprint-ready backlog, technical constraints, timeline expectations, cross-team dependencies | Team velocity drops, deadlines slip, capacity sits idle |
| `qa-engineer` | Acceptance criteria in GIVEN/WHEN/THEN, edge cases, severity definitions, expected behavior | Bugs missed in QA — regressions reach production |
| `scrum-master` | Prioritized backlog, sprint goals, capacity context, blocker identification | Sprints start without clear goals — wasted planning cycles |
| `ui-ux-designer` | User stories with context, design constraints, accessibility requirements, success metrics | Designs don't reflect user needs — redesign cycles |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Major scope change mid-sprint | `engineering-manager`, `qa-engineer`, `scrum-master` | Sprint replanning, capacity reallocation, timeline communication |
| Pivot signal from PMF data | `ceo-strategist`, `cto-advisor`, `ux-researcher` | Strategic replanning, research deep-dive, roadmap overhaul |
| Competitive launch with >50% feature parity | `ceo-strategist`, `cto-advisor`, `product-strategist` | Competitive response, roadmap reprioritization, positioning update |
| Customer churn spike (>10% monthly) | `ceo-strategist`, `product-strategist` | Churn root cause, feature gap analysis, retention intervention |
| OKR at risk (red status at mid-quarter) | `ceo-strategist`, `cto-advisor`, `scrum-master` | Expectation management, resource reallocation, scope negotiation |
| Critical production bug discovered | `engineering-manager`, `qa-engineer` | Impact assessment, hotfix prioritization, customer communication |

### Escalation Path

```
Strategic product conflict (CEO wants X, CTO says impossible, customer demands Y)
  └── `ceo-strategist` + `cto-advisor` + `product-manager`. ADR or decision memo within 1 week.

Delivery risk (team velocity drop >40%, key engineer departure, critical blocker)
  └── `engineering-manager` + `cto-advisor` + `product-manager`. Replan or descope within 48 hours.

Customer escalation (enterprise customer threatening churn over missing feature)
  └── `product-manager` + `ceo-strategist` if >10% revenue at risk.
```

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Stakeholder asks "can we just add this one small thing?" mid-sprint | Check RICE score against current sprint items. If unprioritized, add to "Next" column with score — never swap in-progress work without a tradeoff conversation | Scope creep mid-sprint is the #1 cause of missed deadlines; every "small thing" carries hidden complexity and context-switching cost |
| Engineering lead reports velocity drop >30% for two consecutive sprints | Run a retrospective on the last 3 completed stories. Check if acceptance criteria are ambiguous, dependencies unmapped, or stories too large (>5 story points). Loop in scrum-master | Sustained velocity drops signal systemic issues (unclear specs, technical debt, or morale), not just "a slow sprint" — early diagnosis prevents quarter-level misses |
| User research reveals a feature you prioritized has low desirability in Kano survey results | Reclassify the feature (attractive → indifferent) and re-score RICE with updated Reach and Confidence. Move to "Later" if Confidence drops below 50% | Building features users don't want wastes engineering capacity; the Kano model distinguishes "must-have" from "nice-to-have" with data, not opinion |
| Competitor launches feature with >70% parity to your Q2 roadmap item | Run competitive teardown within 48 hours: what problem do they solve better/worse? Decide: accelerate to differentiate, deprioritize and own a different problem, or match with a better UX. Notify product-strategist | Parity features lose — if you ship the same thing 3 months later, you're competing on execution speed, not differentiation, and the competitor already has the data |
| PRD has been in async review for >5 business days with zero stakeholder feedback | Schedule a 15-minute sync with each silent stakeholder. Ask directly: "What would make you reject this spec?" Silence in review = misalignment that surfaces during implementation | Delayed feedback means stakeholders haven't read the PRD or disagree but won't say so; both scenarios produce rework after engineering has already started building |
| Post-launch metrics show adoption <20% of target after 30 days | Audit the success metric baseline: was the Reach estimate inflated? Run 5 user interviews with non-adopters within 1 week. Decide: iterate on UX, pivot the use case, or kill the feature | Low adoption after launch means either the problem wasn't real, the solution missed the mark, or the rollout was flawed — each requires a different fix, and waiting depletes team trust |
| Engineering estimates 3x what you expected for a P0 feature | Walk through the spec together with engineering: identify hidden complexity, missing edge cases, or integration points you didn't account for. Adjust scope or timeline — never pressure estimates down | Estimation gaps reveal spec ambiguity; engineers see complexity PMs miss. Pressuring estimates down produces missed deadlines, technical debt, and burned-out teams |
| Backlog contains items older than 2 quarters with no updates or grooming activity | Archive or delete stale items. If the problem was genuinely important, it would have been reprioritized by now. Send a summary of archived items to stakeholders before deletion with a 1-week veto window | Stale backlogs create the illusion of progress ("look at all these ideas!") while hiding the real work that needs doing. A lean backlog is a trusted backlog |
| Feature has no RICE score or prioritization framework applied — it's in the backlog "because someone asked for it" | Run RICE scoring: Reach (how many users affected?), Impact (how much does it move the needle?), Confidence (how sure are we?), Effort (engineering weeks). Every unscored feature in the backlog is a bet without odds. Score before sprint planning, not after | Prioritization without a framework is politics. RICE depersonalizes the decision — it's not "the PM said no," it's "the score says there are 5 things more valuable than this right now" |
| Stakeholder hasn't been consulted on a feature that affects their team — they'll find out during the sprint review | Flag immediately: map all affected stakeholders before the feature enters sprint planning. Required sign-off from any team whose workflow, metrics, or resources are impacted. Proactively schedule 15-minute sync with each silent stakeholder before the PRD goes to review | Silent stakeholders become loud blockers during implementation. Surprise at sprint review = rework after engineering has already started. The cost of a 15-minute sync is $0; the cost of stakeholder rework is a sprint |
| No success metrics defined — the feature will be judged "successful" based on vibes | Propose North Star metric decomposition: which input metric does this feature move? Define baseline value, target threshold, and measurement window before the first user story is written. If you can't define success numerically, you're building on hope | Success metrics are the difference between a feature that ships and a feature that works. Defining metrics before building forces the question: what user behavior change are we buying with this effort? Vague answers = vague outcomes |
| Product-manager → fullstack-developer: feature breakdown into technical tasks | Walk through the PRD with engineering before sprint planning. Identify: API contract dependencies (contract-first or implementation-first?), database migration requirements, frontend component inventory, state management needs. Break features into tasks the fullstack developer can estimate independently | Fullstack developers need the complete picture — frontend, backend, and database. A PRD that only describes UI behavior without API contracts or data models forces developers to guess at integration points. The PM doesn't need to write the API spec, but they must flag when one is needed |
| No coordination with `cto-advisor` for technical feasibility — feature requires architecture change nobody approved | Before committing to a feature with architectural implications, run a technical feasibility review with `cto-advisor` and `system-architect`. Document in an ADR. Business commitments without engineering validation are not commitments — they're wishes dressed as promises | Architecture decisions made under sprint pressure are the most expensive kind. A feature that requires a new service or data pipeline must be validated at the architecture level before it enters the backlog. CTO review is not a bottleneck — it's insurance against 2-quarter rewrites |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- Write the PRD before writing the first line of code — and share it asynchronously for 48-hour comment period.
- Use the RICE framework consistently; subjectivity is inevitable but consistency surfaces the right conversations.
- Separate outcome roadmaps from output roadmaps — track what users do, not what the team ships.
- Accept that the "Next" column is a buffer, not a promise — reprioritize quarterly without guilt.
- Every user story must have a measurable completion criterion — "works" is not a criterion.
- Keep PRDs under 10 pages; appendices carry supplementary detail so the core remains skimmable.
- When stakeholders disagree, escalate the decision criteria, not the decision.
- Run a pre-mortem: "It's 6 months from now and this feature failed. What happened?"

## Anti-Patterns
<!-- QUICK: 90s -- 4-column machine-checkable format. Every anti-pattern has a grep to find it and a lint/prevention config. -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Writing PRDs in isolation and sharing them as "final" — engineering sees the spec for the first time when sprint planning starts | Share PRDs as drafts with a 48-hour async comment period. Engineering, design, and QA review before a single user story is written. PRDs are collaboration tools, not approval artifacts | `grep -Lz 'review.window\|async.comment\|draft.review\|48.hour\|stakeholder.review' *.md` — PRD files missing review process language | PRD template: Add `## Review Process: 48-hour async review period after draft. **DO NOT SHIP until all reviewers approve.**` header. Template path: `templates/prd-draft-review.md` |
| Computing RICE scores solo without team validation — Reach = "all logged-in users will see this" and Confidence = "80% because we have analytics" | Compute RICE as a team exercise. Require evidence for each input: Reach from analytics, Impact from user research, Confidence tiered (20%/50%/80%/100%) | `grep -P 'RICE.*score.*\d+|Reach.*=.*\d+|Impact.*=.*\d+' *.md \| grep -v 'team.review\|validated\|confidence.tier'` — RICE scores without validation evidence | RICE template: Add `| Input | Value | Evidence Source | Reviewed By |` column. Every score needs an evidence link and reviewer initial. Template: `templates/rice-with-evidence.md` |
| Committing launch dates before engineering has seen the full spec — CEO announces "Q2 launch" based on the PM's rough estimate | Roadmap uses Now/Next/Later, not dates. When dates are required, get engineering's estimate AFTER spec review with edge cases and NFRs included | `grep -iP '(launch|ship).*(date|deadline|Q[1-4]|month|week of)\b' *.md \| grep -v 'engineering.estimate\|pending.validation\|feasibility'` — date commitments without engineering validation | Roadmap template: Replace date columns with `Now/Next/Later` + `Engineering Estimate Status: [ ] Not Reviewed / [ ] Reviewed / [ ] Committed`. |
| Defining success metrics after launch when adoption is low — retrofitting metrics to make the feature look successful | Define success metrics before writing the first user story. Establish baseline values and target thresholds numerically | `grep -L 'Success.Metrics\|success.metrics\|Metric.*baseline\|Metric.*target' *.md` — PRD/spec files with no success metrics section | PRD template: Add `## Success Metrics` as the FIRST section after Problem Statement. Include `Baseline`, `Target`, and `Measurement Method` columns. If section is empty, REFUSE to proceed. |
| Accepting "works" as a user story completion criterion — "user can reset password" with no measurable definition of done | Every user story must have acceptance criteria in GIVEN/WHEN/THEN format with measurable outcomes | `grep -P '(can|able to|supports|works|should)\b' *.md \| grep -v 'GIVEN.*WHEN.*THEN\|acceptance.criteria'` — subjective verbs without GIVEN/WHEN/THEN | Acceptance criteria linter: `scripts/check-acceptance-criteria.sh` checks every story in PRD for GIVEN/WHEN/THEN structure and objective verbs |
| Skipping the non-goals section — "everything is in scope until someone explicitly says it's not" | Every PRD includes an explicit "Out of Scope" section. When scope tries to expand during build, point to the non-goals as a pre-agreed contract | `grep -L 'Out.of.Scope\|Non.Goals\|What.We.*NOT.*Building\|out.of.scope' *.md` — PRD files without non-goals section | PRD template: Add `## Out of Scope (explicitly NOT in this PRD)` as mandatory section. Template validator: `scripts/prd-template-check.sh` — fails if non-goals section is missing or empty |
| Treating the "Next" column as a promise — committing to stakeholders that features will ship next quarter | Explicitly communicate that "Next" is a buffer, not a promise. Reprioritization happens quarterly with stakeholder buy-in | `grep -iP '(next.*quarter|Q[1-4].*next|committed.*next|promise.*next|guarantee)' *.md` — language that treats roadmap as fixed commitment | Roadmap communication template: `## Release Cadence: Now = committed (this quarter), Next = plan (subject to quarterly reprioritization), Later = direction (no commitment)` |

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: PM = you talking to users and writing todos. No PRDs. No roadmap beyond "what's next." Success metric = revenue or active users. Prioritization = whatever keeps the lights on.
- **What to skip**: PRDs. OKRs. RICE. NPS. Roadmap presentations. Stakeholder management (you're the only stakeholder).
- **Coordination**: Talk to users. Ship. Repeat.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Lightweight PRDs (<5 pages). Simple roadmap (Now/Next/Later). North Star metric identified. Basic OKRs. Customer interviews structured (not ad-hoc). Prioritization = value vs effort. Feature flags for safer launches.
- **What to skip**: Full RICE/CD3. Competitive analysis program. Product ops. Beta programs. Post-launch metrics dashboards.
- **Coordination**: Weekly product sync with eng lead. Monthly roadmap review with CEO. Bi-weekly customer interview debriefs.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Full PRD template. RICE prioritization. OKRs cascading. Dedicated PM per product area. Launch plans with rollout and rollback. Beta program management. Post-launch metrics dashboard. Stakeholder communication cadence. Competitive win/loss analysis.
- **What to skip**: Product portfolio management (unless multi-product). Product ops as dedicated function. Formal product council.
- **Coordination**: Bi-weekly product review. Monthly roadmap review with stakeholders. Quarterly OKR review. Pre-launch go/no-go meetings.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-product portfolio with P&L. Product ops team. Product council with formal gates. Advanced analytics team. Pricing science. PLG team. M&A product integration. International product strategy. Accessibility and compliance built into PRD template.
- **What's full production**: Quarterly business review (QBR). Product portfolio review monthly. Product council bi-weekly. Launch governance with stage gates. Product analytics embedded in every team.
- **Coordination**: QBR with exec team. Monthly portfolio review. Bi-weekly product council. Weekly PLG + growth review.

### Transition Triggers
- **Solo → Small**: Second PM needed because you can't cover all features + users. >500 active users.
- **Small → Medium**: 3+ PMs with overlapping stakeholder groups. >10K users or second product line.
- **Medium → Enterprise**: Multi-product with independent P&L. IPO preparation. >100K users.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | idea-to-spec | Structured PRD, API contracts, screen inventory |
| **This** | product-manager | Prioritized backlog, RICE scores, roadmap, stakeholder alignment |
| **After** | scrum-master | Sprint-ready user stories, capacity planning, delivery tracking |

Common chains:
- **New product**: idea-to-spec → product-manager → scrum-master — from spec to sprint-ready backlog
- **Feature work**: business-strategist → product-manager → ux-researcher — from strategic context to evidence-based prioritization

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `problem-discovery` | Stakeholder/user interviews, problem framing | Phase 1 — problem statement, success metrics, cohort segmentation |
| `prd-writing` | Feature definition, requirements documentation | Phase 2 — executive summary, user stories, NFRs, edge cases |
| `rice-prioritization` | Backlog grooming, roadmap decisions | Phase 3 — Reach × Impact × Confidence / Effort scoring |
| `roadmap-communication` | Stakeholder updates, executive reviews | Phase 4 — Now/Next/Later, problem-focused, stakeholder summaries |
| `delivery-partnership` | Sprint execution, unblocking, launch validation | Phase 5 — standups, demos, launch metrics, post-launch retro |
| `okr-setting` | Goal cascading, measurable outcomes | `ceo-strategist` — North Star alignment, KPI definition |
| `competitive-analysis` | Market positioning, feature gap analysis | `business-strategist` — win/loss, feature comparison |


### War Story 1 — The 50-Page PRD Nobody Read
**Symptom:** A PM spent 3 weeks writing a 50-page PRD for a new onboarding flow. Engineering spent 2 days reading it, asked 30 clarifying questions, and built something different from what the PM intended. The feature took 2x longer than estimated.
**Root cause:** The PRD was written in isolation, shared as a "final" document, and assumed the reader would fill in the gaps. No early review cycles, no async comment period, no acceptance criteria in a testable format.
**Fix:** Adopted the "Minimum Viable PRD" approach: 5-page maximum, executive summary first, GIVEN/WHEN/THEN acceptance criteria for every story, async review mandatory before any sync meeting. PRDs became collaboration tools instead of approval artifacts.
**Lesson:** PRD quality isn't measured by page count — it's measured by how few questions engineers need to ask after reading it.

### War Story 2 — The RICE Score That Lied
**Symptom:** A team used RICE scoring religiously. The highest-scored feature had a RICE of 320 — 3x the next candidate. They built it over 2 quarters. It got 50 users in the first month, not the 5,000 they modeled.
**Root cause:** The Reach estimate was based on "all logged-in users will see this" (50K/month) rather than "users who need and will act on this" (200/month). Confidence was set at 80% because "we have analytics" — but the analytics didn't measure intent.
**Fix:** Introduced confidence tiering: 20% (gut), 50% (qualitative data), 80% (quantitative proxy), 100% (proven in market). Any feature with Confidence < 80% required a validation sprint before full build. Punted 60% of the backlog.
**Lesson:** RICE is only as good as its inputs. A feature with RICE 100 at 80% confidence beats RICE 300 at 20% confidence every time. Invest in confidence accuracy.

### War Story 3 — The Ship Date That Was Set Before Engineering Saw the Spec
**Symptom:** The CEO committed a "Q2 launch" date to the board based on the PM's estimate. Engineering saw the PRD in April, estimated 6 months. The PM was blamed for the miss. The launch slipped by 2 quarters.
**Root cause:** The PM estimated without engineering input. The spec was incomplete (no edge cases, no error states, no non-functional requirements). Engineering's real estimate was 4x the PM's guess.
**Fix:** Established a "no dates without engineering review" policy. Roadmap uses Now/Next/Later. PMs can say "we're targeting Q2, pending engineering validation." Built a spec review step: engineering estimates after they've read the full spec, not after a 5-minute pitch.
**Lesson:** Dates set without engineering input are not estimates — they're wishes. Always get engineering's estimate after they've read the full spec.


## Error Decoder
<!-- DEEP: 10+min -- 5-column format with grep matches and auto-recovery loops -->

| 🖥️ Console Match (grep) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|--------------------------|---------|-----------|-----|----------------------|
| `grep -iP '(stakeholder.*reject\|spec.*wrong\|doesn.t.*need\|solution.*mismatch)' logs/pm-issues.log` | Stakeholder rejects spec after seeing it for the first time | Spec solves the wrong problem or misses stakeholder context. PM wrote in isolation without validating the problem statement | Run "Five Whys" with stakeholder before writing. Confirm problem statement in writing BEFORE solution. Send draft for async review, not final approval | 1. Stop writing. 2. Schedule 30-min whiteboard session with stakeholder — no screens, just problem definition. 3. Write problem statement (< 3 sentences). 4. Send for confirmation: "Is this the problem?" 5. Only after confirmation: write solution. 6. Share draft with "Comments welcome in 48 hours" |
| `grep -iP '(dev.*estimate.*higher\|estimate.*blow.*up\|hidden.*complexity\|edge.case.*miss)' logs/pm-issues.log` | Engineering estimates 3×-10× higher than PM expected | Spec has hidden complexity, missing edge cases, or undefined NFRs. Ambiguity → estimate buffer | Every screen needs loading, empty, error, and edge states defined. Add NFRs (latency, throughput, security). Ambiguity is the single largest driver of estimate inflation | 1. Do NOT push back on the estimate. 2. Walk through the spec with engineering lead. 3. For each screen: "What happens if empty? Error? Concurrent use?" 4. Add missing states to spec. 5. Re-estimate with states defined. 6. Accept the revised estimate — it reflects real complexity |
| `grep -iP '(no.*adoption\|no.one.*using\|feature.*ignored\|launched.*but.*zero)' logs/pm-issues.log` | Users don't adopt the feature after launch | Built what was asked, not what was needed. Feature request treated as requirement without outcome validation | Define success metrics before building. Validate with prototype or concept test before full build. Outcome-based: "increase X by Y%" not "build Z" | 1. Do NOT build more features. 2. Interview 5 target users: "What problem were you solving when you tried this?" 3. Map answers against original problem statement. 4. If mismatch found: rewrite problem statement, prototype lightweight solution, retest with 5 users. 5. If confirmed: enhance existing feature, don't build adjacent features to compensate |
| `grep -iP '(scope.creep\|scope.*expand\|requirement.*added\|stakeholder.*requested.*also)' logs/pm-issues.log` | Scope expands continuously during build — "just one more thing" | Spec didn't define explicit non-goals. Every request during build feels urgent and reasonable in isolation | Add "Out of Scope" section as a non-negotiable contract. When scope tries to expand, point to non-goals. New requests go into backlog, not current sprint | 1. Stop accepting in-sprint additions. 2. Add every new request to a "Considered but Deferred" section in the PRD. 3. Schedule scope review 1 week after launch. 4. If truly critical (P0 bug, legal requirement): swap with equal-scope item from current sprint — NEVER add to scope without removing equivalent scope |
| `grep -iP '(cross.team.*block\|dependency.*not.ready\|waiting.*on.*team\|blocked.*by)' logs/pm-issues.log` | Cross-team dependency blocks delivery — feature ships 6 weeks late | Spec assumed dependencies would be magically available. No named owner, no date, no escalation path | Map ALL dependencies with owner name, committed date, and fallback plan in the spec. Flag red (at risk) to PM weekly. Review dependencies as first item in every standup | 1. Create dependency tracker: `\| Dependency \| Owner \| Committed Date \| Status \| Escalation \|`. 2. Review weekly with owning PM. 3. If status = Red (date missed OR no response in 5 business days): escalate to common manager. 4. Define fallback: "If dependency not available by [date], we will [mock/decouple/repurpose X]" |
| `grep -iP '(priority.*disagree\|eng.*vs.*pm\|what.*should.*we.*build\|which.*first\|priority.*fight)' logs/pm-issues.log` | PM and Engineering disagree on what to build first | No shared prioritization framework. Priority based on opinion — loudest voice wins, not most valuable work | Adopt RICE or CD3 scoring. Run scoring as a team exercise. Written scores depersonalize decisions and speed up alignment | 1. Stop arguing. All disagreements pause. 2. Pull up the RICE template. 3. Together: score the disputed features. 4. If scores are close (< 20% difference): flip a coin, ship one, measure, learn. 5. If scores diverge: investigate the input that differs (usually Confidence or Effort). 6. Agree: "RICE says X. We ship X. We review in 30 days and adjust." |


## What Good Looks Like

> You've just completed the product management exercise. Your PRD fits under 10 pages and the executive summary tells a VP everything they need in three sentences. Every user story has measurable acceptance criteria — nobody in engineering has to ask "how do I know when this is done." RICE scores are computed with documented inputs, and the team reviewed them together, surfacing hidden assumptions before they became implementation dead ends. Your roadmap uses Now/Next/Later and describes problems, not solutions — engineering owns the how. The launch plan includes a rollout strategy with feature flags and rollback criteria, and the post-launch dashboard is live before the first user sees the feature.


## Production Checklist
<!-- QUICK: 30s -- all items are machine-verifiable. Every item gets a validation command and auto-fix path. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **S1** | PRD approved by engineering lead, design lead, and primary stakeholder | `grep -c '## Review Status\|Approved by\|Reviewed by' PRD.md` — must return >= 3 approvals | Add `## Review Status` section: `\| Role \| Name \| Status \| Date \|`. Require 3 checkmarks before moving to build |
| **S2** | Success metrics defined with baseline values and target values | `grep -cP '(Metric.*Baseline.*Target\|# Metric\|Success.Metric)' PRD.md` — must match | PRD template: Add `## Success Metrics` table with columns `Metric Name \| Baseline \| Target \| Measurement Method`. Template: `templates/prd-success-metrics.md` |
| **S3** | Every user story has acceptance criteria in GIVEN/WHEN/THEN format | `grep -cP 'GIVEN.*\n.*WHEN.*\n.*THEN' PRD.md` — count must match number of user stories | Run `scripts/check-gwt.sh PRD.md` to report stories missing GIVEN/WHEN/THEN. Rewrite stories without GWT |
| **S4** | RICE scores computed and reviewed with the team | `npx rice-validator PRD.md --min-confidence 50` or `grep -cP 'Reach.*\d+.*Impact.*\d+.*Confidence.*\d+.*Effort.*\d+' PRD.md` — must match feature count | RICE template: Run `templates/rice-scoring.md` and fill all columns. Schedule 30-min team review for every scoring session |
| **S5** | Edge cases documented for top-5 user stories (empty, error, concurrency, permissions) | `grep -cP '(Empty.*State\|Error.*State\|Edge.*Case\|Concurrency\|Permission.*Case)' PRD.md` — must be >= 5 | Edge case checklist: For each screen, fill: `\| State \| Behavior \| Recovery \|`. Template: `templates/edge-case-checklist.md` |
| **S6** | Non-functional requirements specified (latency, throughput, availability, security) | `grep -cP '(Latency\|Throughput\|Availability\|Security\|Compliance\|Scalability)' PRD.md` — must be >= 4 | NFR template: Add `## Non-Functional Requirements` with at minimum: P95 latency target, request throughput, availability SLO (e.g., 99.9%), and security requirements |
| **S7** | Roadmap published and communicated to all stakeholders | `curl -s -o /dev/null -w '%{http_code}' <roadmap-url>` must return 200; OR `grep -l 'Now\|Next\|Later' roadmap.md > /dev/null && echo "found"` | Publish roadmap to shared wiki/Notion/Confluence. Send stakeholder email with link and 5-minute async walkthrough video |
| **S8** | Launch plan includes rollout strategy (feature flags, canary, % ramp) and rollback criteria | `grep -cP '(feature.flag\|canary\|ramp.*%\|rollback.*criteria\|kill.switch)' launch-plan.md` — must be >= 2 | Launch plan template: Add `## Rollout: % ramp: 5→25→50→100`. `## Rollback: if error rate > X% or P95 latency > Yms for Z minutes` |
| **S9** | Post-launch metrics dashboard set up before GA | `curl -s -o /dev/null -w '%{http_code}' <dashboard-url>` must return 200 | Create dashboard with: adoption rate, error rate, P95 latency, and core success metric. Template link: `dashboards/launch-metrics-template.json` |
| **S10** | Backlog groomed and free of stale items older than 2 quarters | `grep -cP '(created\|updated).*(202[3-4])' backlog.md` — items older than 6 months must return 0 after purge | Run `scripts/backlog-health.sh` — auto-closes items with no activity in 180 days. Stale backlog = stale thinking |

## Footguns
<!-- DEEP: 10+min — war stories from product management execution -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Shipped a major feature with no success metrics defined — 8 months later, the CEO asked "was that worth it?" and nobody could answer | A PM launched a dashboard redesign after 14 sprints of work across 3 teams. The launch post celebrated "cleaner UI, faster load times, 4.8 stars on the app store." Eight months later, the CEO asked whether the redesign had moved any business metric. The PM checked: activation rate was flat, retention unchanged, NPS within margin of error. $620K of engineering time had produced a prettier product that changed nothing. No baseline was captured before the redesign, so "nothing changed" could mean "it would have been worse" or "it was wasted effort." | Shipping without a measurement plan. The PM defined "success" as "launch on time" — a process metric, not an outcome metric. The business goal was framed as "modernize the UI" rather than "increase trial-to-paid conversion by 15%." | **Define success metrics before the first line of code.** Every feature needs: (1) a baseline measurement from the 30 days before launch, (2) a target (+X% by Y weeks post-launch), (3) a counter-metric to watch for harm (e.g., "conversion goes up but support tickets double"). Write these in the PRD. If you can't define a business metric the feature will move, ask whether the feature is worth building. |
| RICE "Reach" score used total registered users (280,000) instead of monthly active users (6,200). A feature "for everyone" was actually relevant to 2.2% of the user base — and the prioritization had it as #1 | A PM scored a "social sharing" feature at Reach: 280,000 (all registered users × 100%). It ranked #1 in RICE, above "offline mode" which scored Reach: 6,200 (MAU). But social sharing required users to be actively using the app (MAU), and offline mode was actually relevant to 280,000 registered users who traveled. After launch: 1,400 shares in 3 months (0.5% of registered users). Offline mode was delayed by 2 quarters and had 4,100 DAU within 30 days of launch. | RICE inputs were gamed by picking the denominator that made a pet feature look good. "All users" for the feature you want to build, "daily users" for the one you don't. The PM didn't define a consistent reach metric before scoring. | **Standardize Reach to a single definition: users who will encounter this feature in a typical week.** Not registered users (most are dormant), not "target market" (most won't see it). Publish the reach definition before scoring begins. If two PMs score the same feature with different reach numbers, stop and reconcile — the disagreement means the definition isn't clear enough. |
| Backlog had 430 items, 340 created over 18 months ago. "Priority" was a field everyone ignored. The team pulled the top 5 items from the backlog and 3 of them were obsolete. | A PM inherited a backlog that had grown without pruning for 2 years. Items were added by support ("customer wants dark mode"), sales ("prospect asked for SSO"), and execs ("we should do AI"). No one ever subtracted. When the new PM asked "which of these are still relevant?", the answer was silence. The team spent a sprint researching 15 backlog items and killed 11 of them. The other 4 had been "P1" for 18 months — if they were truly P1, they would have been built by now. | Backlog accumulation without curation. Adding is easy (2 minutes to write a ticket), pruning is hard (requires stakeholder conversations to say "we're never building this"). The backlog became a graveyard of ideas that everyone assumed someone else would prioritize. | **Prune the backlog quarterly.** Rule: any item older than 6 months without a status update gets closed. If it's important, someone will reopen it. Every item needs a "last reviewed" date and a "decision" field (build/defer/kill). If an item has been deferred 3 times, it's a kill — you're never building it and admitting that is kinder than pretending. Target: backlog under 100 items for a 2-pizza team. |
| Stakeholder update email said "on track" for 7 consecutive weeks — the feature was actually 4 weeks behind because PM reported engineering estimates as commitments | A PM sent weekly status to the VP of Product: "Authentication migration: on track. Target: June 15." Engineering had said "probably 8 weeks" in the planning meeting. The PM translated that to "committed to June 15." When the team hit an unexpected PostgreSQL migration issue in week 3, the PM kept reporting "on track" hoping they'd catch up. By week 6, the gap was 4 weeks and the VP found out from an engineer in the hallway. The trust damage took 6 months to repair. | Reporting estimates as commitments. "Probably 8 weeks" means "my 50th percentile guess is 8 weeks, my 90th percentile is 12 weeks." Treating it as deterministic hides real uncertainty. The PM valued presenting good news over sharing accurate information. | **Report as a range with confidence, not a single date.** "Best case: June 15 (30% confidence). Likely: June 29 (70% confidence). Worst case: July 13 (95% confidence)." Update the range weekly — if the worst case moves right, say so immediately. Never use the word "on track" — say "as of this week, the 70% confidence date is still June 29" or "the 70% confidence date moved to July 6 because of [specific reason]." |
| Feature flag was meant to be temporary — it controlled the checkout flow for 14 months until removing it broke the payments system for 22 minutes | A PM launched a new checkout with a feature flag so they could roll back quickly. The flag worked perfectly. The old checkout was never removed — "just in case." Fourteen months and 37 deploys later, a new engineer saw the flag and thought "this is dead code" and removed it. The flag's removal triggered a code path that hadn't been tested in 11 months — the payments service received `null` for the tax calculation field and returned `500` for every transaction. 22 minutes of downtime, $8,400 in lost transactions. | Feature flags with no kill date become permanent complexity. The flag was added with a rollout plan but no removal plan. "Just in case" became "forever" because removing a flag that works feels riskier than leaving it. | **Every feature flag needs a removal ticket filed on the day it's created.** The ticket has: (1) a target removal date (30 days post-full-rollout), (2) an owner, (3) a checklist (remove flag, remove old code path, update tests, verify in staging). If the removal date passes without action, the flag turns into a P2 bug — it's now tech debt with a known risk. Track active flags on a dashboard visible to the whole team — if you have more than 10 active flags, you have a flag hygiene problem. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

Use this to diagnose where you actually are, not where you want to be.

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You write user stories as "As a user, I want X" without acceptance criteria — engineering fills in the blanks from their own assumptions | Every user story in your backlog has 3+ GIVEN/WHEN/THEN acceptance criteria, edge cases are enumerated, and a developer who's never attended a planning meeting can implement it correctly | A feature you defined and shipped 12 months ago has the exact adoption curve you predicted in the PRD — within 10% on both timeline and magnitude |
| You prioritize by "what the loudest stakeholder asked for most recently" | You compute RICE scores with documented inputs for every feature, the team reviews scores together, and you can explain to any stakeholder exactly why their request is #14, not #3 | You inherit a backlog with 400 items and within 1 week you close 250 of them — and nobody complains because you've articulated the strategy that justifies every kill |
| You see your job as "write tickets and run standups" | Your launch plan includes a rollout strategy with feature flags, canary percentages, rollback criteria, and a post-launch dashboard that's live before the first user sees the feature | An engineer tells you "I thought this feature was a bad idea but the data proved me wrong" — because you designed the measurement plan that made the evidence undeniable |

**The Litmus Test:** Can you kill a feature that your CEO personally requested, with data, in a way that makes the CEO say "you're right, thanks for saving us from that"? If you can only say no to peers but not to power, you're not L3 yet. Masters advocate for the product, not for their career.

## Deliberate Practice

Product management is learned in the arena — through shipped products, failed experiments, and retrospectives. The improvement loop is the lean startup loop applied to yourself.

### The PM Improvement Loop

```
SHIP → MEASURE → LEARN → (adjust process) → repeat
```

After every launch: what did you predict would happen? What actually happened? Where was the gap? Close one gap per cycle.

### Practice Routines by Skill Level

| Level | Practice | Frequency |
|---|---|---|
| **Novice** | Write 10 user stories in GIVEN/WHEN/THEN from real feature requests. Have an engineer review them for clarity and testability. | Weekly |
| **Competent** | RICE-score 20 items from your backlog independently, then compare scores with another PM. Discuss every gap >2x. | Biweekly |
| **Expert** | Run a customer interview following The Mom Test (talk about their life, not your product). Write up the 3 most surprising insights. | Weekly |
| **Master** | Reverse-engineer a successful product: write the PRD they must have written, then write the PRD they *probably actually* wrote. Compare the difference — that gap is where the craft lives. | Monthly |

### The One Highest-Leverage Activity

**Watch a user use your product in silence.** Don't guide. Don't explain. Just watch. One hour of silent observation reveals more than 50 survey responses. Do this before writing any PRD.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **idea-to-spec** — for bootstrapping the spec artifact from a raw concept
- **ux-researcher** — for persona validation and usability testing before PRD finalization
- **ui-ux-designer** — for design system and interaction pattern alignment
- _Inspired_ by Marty Cagan — for product discovery habits
- _Escaping the Build Trap_ by Melissa Perri — for outcome-driven product management
- RICE Scoring by Intercom (Sean McBride) — for the original prioritization framework
