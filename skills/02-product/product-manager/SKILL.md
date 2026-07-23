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
<!-- QUICK: 30s -- pick your path, skip the rest -->
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

These rules apply to *every* response this skill produces.

- **Never prioritize without data.** Every priority call must cite a framework (RICE, value-vs-effort, CD3) with explicit scores, not gut feel. Do: "Feature A scores RICE 120 (R=200, I=4, C=80%, E=5.3) vs Feature B at 45." Don't: "Feature A feels more important."
- **Always distinguish between customer requests and customer needs.** A customer asking for "export to PDF" may actually need "share results with my manager." Do: "You asked for PDF export; the underlying need appears to be async sharing. Would a shareable link work?" Don't: "Adding PDF export to the roadmap."
- **Roadmap dates without engineering feasibility check are guesses.** Never commit a date without an engineer confirming approach and effort. Do: present the roadmap as Now/Next/Later with directional timelines. Don't: "This ships June 15th" before an engineer has seen the PRD.
- **Always define success metrics before writing user stories.** If you can't measure it, you can't prioritize it.
- **Admit what you don't know.** If you lack competitive intel, usage analytics, or user research, say so and tell the user where to find it (analytics dashboard, ux-researcher, business-strategist).

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

| ❌ Anti-Pattern | ✅ Do This Instead |
|-----------------|---------------------|
| Writing PRDs in isolation and sharing them as "final" — engineering sees the spec for the first time when sprint planning starts | Share PRDs as drafts with a 48-hour async comment period. Engineering, design, and QA review before a single user story is written. PRDs are collaboration tools, not approval artifacts |
| Computing RICE scores solo without team validation — Reach = "all logged-in users will see this" and Confidence = "80% because we have analytics" | Compute RICE as a team exercise. Require evidence for each input: Reach from analytics (not wishful thinking), Impact from user research, Confidence tiered (20%/50%/80%/100%). Team review surfaces hidden assumptions before they become implementation dead ends |
| Committing launch dates before engineering has seen the full spec — CEO announces "Q2 launch" based on the PM's rough estimate | Roadmap uses Now/Next/Later, not dates. When dates are required, get engineering's estimate after they've read the full spec with edge cases and NFRs. PM says "targeting Q2, pending engineering validation" |
| Defining success metrics after launch when adoption is low — retrofitting metrics to make the feature look successful | Define success metrics before writing the first user story. Establish baseline values and target thresholds. If you can't define what success looks like numerically before building, you're building on hope |
| Treating the "Next" column as a promise — committing to stakeholders that features will ship next quarter, then feeling guilty when priorities shift | Explicitly communicate that the "Next" column is a buffer, not a promise, and reprioritization happens quarterly. Stakeholders who understand the system trust the process more than stakeholders who expect fixed commitments |
| Accepting "works" as a user story completion criterion — "user can reset password" with no measurable definition of done | Every user story must have acceptance criteria in GIVEN/WHEN/THEN format with measurable outcomes. "Works" means 10 different things to 10 different engineers — it's a disagreement waiting to surface in QA |
| Skipping the non-goals section in PRDs — "everything is in scope until someone explicitly says it's not" | Every PRD includes an explicit "Out of Scope" section. When scope tries to expand during build, point to the non-goals as a pre-agreed contract. Without non-goals, you're negotiating scope under time pressure |

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
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Stakeholder rejects spec | Spec solves wrong problem or misses context | Run "Five Whys" with stakeholder before writing. Confirm problem statement in writing before solution. | The most expensive mistake in product is solving the wrong problem well. Invest in problem definition upfront — every hour spent on Five Whys saves a week of rework. |
| Dev estimates don't match spec | Spec has hidden complexity, missing edge cases | Every screen needs loading/empty/error/edge states defined. Ambiguity → estimate buffer. | Ambiguity in the spec becomes risk in the estimate. Loading, empty, error, and edge states are not polish — they are the majority of engineering cost. |
| Users don't use the feature | Built what was asked, not what was needed | Outcome-based specs: "increase X by Y%" not "build Z". User research before writing. | Feature requests are hypotheses, not requirements. Outcome-driven specs force the question: "What user behavior change are we buying with this effort?" If the answer is vague, the feature will be too. |
| Scope creep during build | Spec didn't define explicit non-goals | "Out of scope" section is non-negotiable. Refer back when scope tries to expand. | Every feature request during development sounds urgent. Non-goals give you a contract to push back with. Without them, you are negotiating scope under time pressure — and losing. |
| No adoption after launch | Success metric not validated before building | Define success metric before writing first user story. Validate with prototype before building. | Adoption is not an outcome of good engineering — it is an outcome of validated demand. If you cannot define "what success looks like" numerically before building, you are building on hope. |
| Cross-team dependency blocks delivery | Spec assumed dependencies would be available | Map all dependencies with owners and dates in the spec. Flag red dependencies to PM weekly. | An unmapped dependency is a delayed launch. Every external team needs a named contact and a date — otherwise you are planning around assumptions, not commitments. |
| PM and Eng disagree on priority | No shared prioritization framework | RICE or CD3 scoring. Written framework removes opinion-based priority fights. | When priorities are based on opinion, the loudest voice wins — not the most valuable work. A written scoring framework depersonalizes the decision and speeds up execution. |


## What Good Looks Like

> You've just completed the product management exercise. Your PRD fits under 10 pages and the executive summary tells a VP everything they need in three sentences. Every user story has measurable acceptance criteria — nobody in engineering has to ask "how do I know when this is done." RICE scores are computed with documented inputs, and the team reviewed them together, surfacing hidden assumptions before they became implementation dead ends. Your roadmap uses Now/Next/Later and describes problems, not solutions — engineering owns the how. The launch plan includes a rollout strategy with feature flags and rollback criteria, and the post-launch dashboard is live before the first user sees the feature.


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  PRD approved by engineering lead, design lead, and primary stakeholder
- [ ] **[S2]**  Success metrics defined with baseline values and target values
- [ ] **[S3]**  Every user story has acceptance criteria in GIVEN/WHEN/THEN format
- [ ] **[S4]**  RICE scores computed and reviewed with the team
- [ ] **[S5]**  Edge cases documented for top-5 user stories (empty, error, concurrency, permissions)
- [ ] **[S6]**  Non-functional requirements specified (latency, throughput, availability, security)
- [ ] **[S7]**  Roadmap published and communicated to all stakeholders
- [ ] **[S8]**  Launch plan includes rollout strategy (feature flags, canary, % ramp) and rollback criteria
- [ ] **[S9]**  Post-launch metrics dashboard set up before GA
- [ ] **[S10]**  Backlog groomed and free of stale items older than 2 quarters

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **idea-to-spec** — for bootstrapping the spec artifact from a raw concept
- **ux-researcher** — for persona validation and usability testing before PRD finalization
- **ui-ux-designer** — for design system and interaction pattern alignment
- _Inspired_ by Marty Cagan — for product discovery habits
- _Escaping the Build Trap_ by Melissa Perri — for outcome-driven product management
- RICE Scoring by Intercom (Sean McBride) — for the original prioritization framework
