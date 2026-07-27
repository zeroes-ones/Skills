---
name: product-manager
description: >
  Use when writing PRDs, prioritizing features with RICE scoring, building product
  roadmaps, managing stakeholders, or crafting user stories with precise acceptance
  criteria. Handles feature definition, sprint planning, backlog grooming, stakeholder
  communication, user story mapping, and strategic product decisions. Do NOT use for
  technical architecture decisions, code-level design, or engineering team management.
license: MIT
tags:
- product
- prd
- rice
- roadmap
- user-stories
- backlog
- prioritization
author: Sandeep Kumar Penchala
type: product
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 2430
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
---
# Product Manager
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Own the product discovery-to-delivery pipeline: translate business goals into prioritized roadmaps, write crisp PRDs that engineering can execute against, and run RICE-driven prioritization so the team always works on the highest-impact items.

## Route the Request
<!-- STANDARD: 3min -->

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

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---:|
| "I've been doing this long enough to know what's high priority" | Institutional knowledge is uncalibrated opinion. Without RICE scores, you're prioritizing by recency bias and stakeholder volume. The loudest voice wins — not the highest value. RICE takes 15 minutes per feature and saves months of building the wrong thing. |
| "The team knows the deadline — we'll figure out scope on the way" | Deadlines without engineering feasibility input produce missed dates or cut corners. Neither outcome is "making it work." Engineering owns the estimate; product owns the priority. Skip this separation once and you've trained the team that dates are arbitrary. |
| "We'll define success metrics after we see how the feature performs" | Post-launch metrics are retroactive justification, not measurement. Features without pre-defined success criteria are bets without odds — you cannot learn from them because you never defined what winning looks like. Define the target before you pull the trigger. |
| ""User can reset password" is clear enough — the team knows what 'works' means" | "Works" means 10 different things to 10 different engineers. Ambiguity in acceptance criteria costs $500-$2,000 per story in rework during QA. GIVEN/WHEN/THEN is not ceremony — it's the cheapest bug-prevention tool you have. |
| "Out of scope is obvious — writing it down is bureaucracy" | Unwritten scope boundaries are invisible fences. When the stakeholder asks for "one small addition" during sprint 6, you have no agreed contract to point to. Out of Scope is not bureaucracy — it's the only thing standing between your roadmap and scope creep. |

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

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
| **R7** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- A new feature or product area needs a formal Product Requirements Document
- The backlog is bloated and needs objective prioritization (RICE scoring)
- Stakeholders are asking for conflicting features — need a decision framework
- Sprint planning requires well-scoped user stories with acceptance criteria
- Executive or investor updates need a clear product roadmap with milestones
- A feature is stalled because requirements are ambiguous or contradictory

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: Build vs Buy vs Partner

        ┌── INPUT: New capability needed for roadmap
        │
   ┌────┴────────────────────────┐
   │                             │
   ▼                             ▼
Is this core differentiator    Is this table-stakes
or competitive advantage?      or commodity?
   │                             │
   ▼                             ▼
YES → BUILD internally       ┌── Does a mature
      Invest engineering     │   vendor solution
      time for ownership     │   exist?
                             └──┬──────────────────┘
                                │ YES        │ NO
                                ▼            ▼
                           ┌── Integration   PARTNER
                           │   cost < build  or contract
                           │   cost?         development
                           └──┬──────────┘
                              │ YES   │ NO
                              ▼       ▼
                            BUY     BUILD
                            (SaaS)  (if
                                    strategic
                                    enough)

### Decision Tree 2: Stakeholder Update Format Selection

        ┌── INPUT: Stakeholder needs status update
        │
   ┌────┴────────────────────┐
   │                         │
   ▼                         ▼
Executive / Board          Engineering / Design
   │                         │
   ▼                         ▼
┌── Strategic decision    ┌── Blocked on
│   needed?               │   dependencies?
└──┬──────────────────┐   └──┬──────────────┘
   │ YES       │ NO        │ YES        │ NO
   ▼           ▼            ▼            ▼
Decision     Weekly      Unblock        Async
memo +       exec        meeting        Slack +
options      summary     (15 min)       sprint
- reco       3 bullets                  board
                                       update
   ┌── Customer-facing
   │   launch imminent?
   ▼
YES → Go-to-market
      readiness
      checklist +
      launch comms
      plan
NO  → Standard weekly
      product digest

### Decision Tree 3: User Story Splitting Decision

        ┌── INPUT: Story is too large for one sprint
        │
   ┌────┴────────────────────┐
   │                         │
   ▼                         ▼
Can split by                Can split by
workflow step?              data variation?
   │                         │
   ▼                         ▼
YES → Slice by user      YES → Slice by
      journey: login →        entity type:
      dashboard → action      handle each
                              variant
   ┌── Can split by
   │   acceptance criteria
   │   complexity?
   ▼
YES → Happy path first,
      edge cases and
      error states in
      follow-up stories
NO  → Re-evaluate:
      is this actually
      an epic?

**(QUICK)**

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
<!-- STANDARD: 3min -->

**(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Problem Discovery
Interview stakeholders and users. Separate expressed solutions from underlying problems. Draft the problem statement in one sentence: "[User] struggles to [outcome] because [constraint]." Define success criteria — choose one North Star metric and 2–3 supporting KPIs. Identify the target cohort with behavioral segmentation (not just demographics). Document the current-state workflow and quantify the pain with data where possible (time spent, error rate, churn).

  Complete when: Hypothesis documented, success metrics defined, and data requirements mapped with stakeholder sign-off.

### Phase 2 (~30 min): PRD Writing
Structure the PRD with these sections, in order: Executive Summary (3 sentences), Problem Statement, Success Metrics, Target Personas, User Stories (ordered), Functional Requirements, Non-Functional Requirements (performance, security, compliance), Out of Scope, Assumptions & Risks, Launch Plan, and Appendix with wireframe links and API references. Write user stories in the format: `As a [persona], I want [capability] so that [benefit].` Attach acceptance criteria using Gherkin syntax (`GIVEN/WHEN/THEN`). Define edge cases for each story — empty data, concurrent edits, offline, permission revocation.

  Complete when: Strategy documented, success criteria defined, stakeholders aligned, and next-phase dependencies identified.

### Phase 3 (~20 min): RICE Prioritization
Score each initiative on Reach (number of users impacted per quarter), Impact (1 = minimal, 2 = low, 3 = medium, 4 = high, 5 = massive), Confidence (20% = gut, 50% = qualitative data, 80% = quantitative data, 100% = proven), and Effort (person-months). Compute `(Reach × Impact × Confidence) / Effort`. Sort by RICE score descending. Flag items where Confidence < 50% for a spike or time-boxed investigation before committing. Review scores with the team to surface hidden assumptions.

  Complete when: Prioritized backlog documented, RICE scores calculated, roadmap communicated to stakeholders, and dependencies mapped.

### Phase 4 (~15 min): Roadmap & Communication
Build a Now/Next/Later roadmap — avoid date-based roadmaps beyond the current quarter. Now = committed and in active development. Next = discovered, spec'd, ready when capacity opens. Later = validated problems without committed solutions. For each initiative, describe the problem, not the solution syntax. Publish the roadmap visibly and update it monthly. Prepare stakeholder-specific summaries: engineering needs technical context, executives need risk/ROI, sales needs timelines and talking points.

  Complete when: Evaluation metrics computed, results compared against baseline, and go/no-go recommendation documented.

### Phase 5 (~25 min): Delivery Partnership
Attend standups to unblock the team on requirements ambiguity. Triage incoming bugs and feature requests against the current roadmap. Run sprint demos and validate that acceptance criteria are met — not just functionally, but experientially. Collect launch metrics and compare against the success criteria in the PRD. Schedule a post-launch retro to capture product learnings within 2 weeks of GA.

  Complete when: Evaluation metrics computed, results compared against baseline, and go/no-go recommendation documented.
  Complete when: PRD reviewed by engineering lead and feasibility confirmed within sprint capacity.
  Complete when: Success metrics defined with baseline measurement and target thresholds.
  Complete when: User testing completed with at least 5 participants — findings documented.

## Best Practices
<!-- STANDARD: 3min -->

1. **PRD as a decision document, not a specification.** The PRD captures WHY and WHAT — the problem, success criteria, and user stories. Engineering owns HOW. If your PRD specifies database schemas, it is overreaching.

2. **RICE is a conversation starter, not a calculator.** RICE scores expose assumptions (Is Confidence really 80%? Is Effort really 2 person-months?) The debate that follows the scoring is where prioritization actually happens. Never rank by decimal-point differences.

3. **Stakeholder communication is role-specific.** Engineering needs technical context and acceptance criteria. Executives need risk, ROI, and timeline. Sales needs talking points and launch dates. Marketing needs positioning and customer value. Send the same PRD to all of them and everyone misses what they need.

4. **Roadmaps set outcomes, not timelines beyond the current quarter.** Now = committed and in active development. Next = discovered, spec'd, ready when capacity opens. Later = validated problems without committed solutions. Date-based roadmaps beyond 8 weeks are fiction.

5. **User stories split by persona, not by feature.** "As a user, I want..." creates a false consensus that all users want the same thing. Power users and first-time users of the same feature have diametrically opposed needs. Split personas first, then write stories per persona.

6. **Acceptance criteria must be testable before code freeze.** Use Gherkin syntax (GIVEN/WHEN/THEN) and include edge cases: empty data, concurrent edits, offline mode, permission revocation. If QA cannot write an automated test from your acceptance criteria, the criteria are too vague.

7. **Discovery is continuous, not a phase.** Reserve 20-30% of every cycle for discovery. The spec you wrote 3 months ago was based on what you knew then. Every sprint should include at least one customer conversation that might change what you build next.

8. **Outcome metrics over output metrics.** "Shipped 3 features" is output. "Reduced checkout abandonment from 62% to 54%" is outcome. Define success criteria as outcome metrics before a single line of code is written. If you cannot measure whether the feature worked, do not build it.

9. **Kill criteria ship with every feature.** Define not just the target metric but the kill threshold — the number below which the feature should be removed. Without a kill threshold, every feature becomes a permanent tax on the codebase, compounding maintenance cost forever.

10. **The highest-leverage PM activity is watching users.** One hour of silent user observation reveals more than 50 survey responses. Schedule a user observation session before writing any PRD. The pattern you notice in minute 47 is the one that changes the roadmap.

## Error Decoder
<!-- STANDARD: 3min -->

| Error Message / Situation | Root Cause | Fix | Lesson |
|--------------------------|------------|-----|--------|
| Roadmap is a Gantt chart set 12 months out | Assumption that the world is static. The first customer escalation, competitor launch, or platform change invalidates everything after month 2. | Switch to Now/Next/Later with rolling 6-week certainty windows. Publish outcomes, not dates. Update monthly. | Roadmaps are living documents that describe intent, not contracts that describe certainty. |
| "As a user, I want..." user stories create conflicting requirements | All users are not the same user. Power users and first-time users need different things from the same feature. | Split personas BEFORE writing stories. Write "As a [specific persona], I want [capability] so that [job-to-be-done]." | One-size-fits-all stories produce one-size-fits-nobody features. |
| Stakeholders approved the PRD but engineering built something different | PRD described WHAT without acceptance criteria. Engineering filled in the gaps with their best guess — which was wrong. | Every user story must have Gherkin acceptance criteria. Every functional requirement must have a verifiable condition. | A spec without acceptance criteria is a suggestion, not a spec. |
| RICE score says Feature A (253,750) wins over Feature B (251,000) | False precision. Reach, Impact, and Confidence are estimates. A 1% difference in RICE score is pure noise. | Use RICE to bucket features into tiers (top quartile, middle 50%, bottom quartile). Debated within tiers based on strategic context. Never rank by decimal-point differences. | RICE is ordinal, not cardinal. Adjacent scores are ties. |
| Feature shipped but nobody can answer "did it work?" | No success criteria defined in the PRD. Without a baseline and target, post-launch evaluation is impossible. | Every PRD must include: (1) the metric it moves, (2) baseline before launch, (3) target after 90 days, (4) kill threshold. | Features without success criteria become permanent codebase taxes that nobody can justify keeping or killing. |
| Customer says "I would definitely use this" in interview but never adopts | Social desirability bias. People say yes to avoid conflict. 80% of "would use" responses in interviews result in zero adoption. | Ask "When was the last time you had this problem?" and "How do you solve it today?" The presence of existing workarounds and the recency of the problem predict adoption better than stated intent. | Stated intent and revealed behavior correlate at ~0.3. Observe what users DO, not what they SAY. |

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like
<!-- STANDARD: 3min -->

> Your PRD fits under 10 pages and the executive summary tells a VP everything they need in three sentences.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice
<!-- STANDARD: 3min -->

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

## Anti-Patterns
<!-- STANDARD: 3min -->

- **70% of features go unused or rarely used — that's $100K-$1M in wasted engineering per product.** Standish Group data consistently shows ~70% of features in a typical software product are rarely or never used. If your annual engineering budget is $2M, that's $1.4M/year building things nobody wants. **Total cost: $100K-$1M wasted per product annually.** Before building any feature, require evidence: 5+ customer interviews confirming the problem, usage data from a prototype or competitor feature, or a validated experiment result.
- **HIPPO-driven development costs $50K-$500K per misguided initiative.** When the Highest Paid Person's Opinion ("we need AI features" / "our competitor has dark mode") drives the roadmap without user validation, you build what the boss wants — not what users need. A 3-month engineering sprint triggered by an executive whim costs $50K-$200K. Multiple HIPPO-driven features per year = $500K+ in shelfware. **Total cost: $50K-$500K per HIPPO-driven initiative.** Require the same validation bar for executive ideas as any other feature request: user evidence or experiment data.
- **Features shipped without success metrics are impossible to justify or kill.** When you can't answer "did this feature work?", every feature becomes a permanent tax on the codebase — no one can prove it should be removed. The cost isn't just the $20K-$100K build; it's the compounding maintenance, onboarding complexity, and support burden forever. **Total cost: $20K-$100K build + indefinite maintenance tax.** Every feature spec must define: (1) the metric it moves, (2) the baseline before launch, (3) the target after 90 days, and (4) the kill threshold.
- **Skipping user research before building costs $50K-$300K in building the wrong solution.** User research costs $5K-$15K for a proper study (5-8 interviews, synthesis, report). Skipping it to "move fast" and building the wrong thing costs 10-50x that in wasted engineering. A $200K feature built on assumptions that fail in production = $200K thrown away when 2 weeks of research would have revealed the flaw. **Total cost: $50K-$300K per feature built without user validation.** The rule: research investment should be 5-10% of the feature's build cost — $10K research for a $150K feature.
- **Committing to fixed scope and date without a discovery buffer.** Teams commit to "3 features by Q2" during annual planning based on rough t-shirt estimates. When one feature reveals 2x complexity during discovery — an undocumented legacy API, a regulatory requirement nobody knew existed, a third-party dependency that doesn't support the use case — the team either ships garbage by cutting quality and testing, or misses the date and burns stakeholder trust. Either outcome costs engineering morale, customer confidence, and often a failed quarterly OKR that cascades into re-planning the entire roadmap. **Total cost: $50K-$200K per quarter in wasted effort, re-planning chaos, and missed OKR targets.** Reserve 20-30% of every cycle as a discovery buffer. If discovery confirms the estimate, the buffer becomes capacity for the next priority — if it doesn't, you have room to adjust without breaking commitments.
- **RICE scoring with false precision**: Reach (500K users) × Impact (3.5) × Confidence (87%) / Effort (6 person-months) = 253,750. The score looks objective but the inputs are all estimates. A competing feature scored 251,000 — that 1% difference is pure noise, not a real priority signal.
- **User stories with "As a user, I want..."** create a false assumption that all users want the same thing. "As a power user" vs "As a first-time user" of the SAME feature produce diametrically opposed requirements. Split personas FIRST, then write stories per persona.
- **Customer interview "would you use this?"** questions — people say yes to avoid conflict. 80% of users who say "I would definitely use this" in interviews never adopt. Instead, ask "when was the last time you had this problem?" and "how do you solve it today?".
- **Roadmap as a Gantt chart** set 12 months out — the first unexpected customer escalation, competitor launch, or platform dependency change invalidates everything after month 2. Roadmaps should set outcomes and themes with rolling 6-week certainty windows, not fixed timelines.
- **"Technical debt" as a catch-all** for "we need to refactor." Actual tech debt (trade-offs made knowingly) can be quantified with interest payments (e.g., "deployments take 3x longer due to X"). Vague "clean up the codebase" initiatives without interest-rate calculations never get prioritized.

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| PRD written without engineering input, requiring major rework during implementation | $20K-$100K in wasted sprint cycles | Co-write technical sections with engineering lead; conduct technical feasibility review before PRD finalization; include non-functional requirements |
| Feature shipped without success metrics defined, making impact unmeasurable | $50K-$200K in unvalidated engineering investment | Define North Star and counter metrics before development starts; instrument analytics during build, not after launch; set evaluation timeline with go/kill criteria |
| Stakeholder alignment meeting ends with false consensus due to unvoiced concerns | $25K-$100K in rework when hidden objections surface | Use anonymous pre-read feedback before alignment meetings; explicitly ask for dissenting views; document decisions with named dissent where applicable |
| User research participants recruited from convenience sample biasing all findings | $30K-$150K in product decisions built on wrong user data | Define screening criteria based on target segments; recruit from multiple channels; validate sample against customer base demographics before analysis |
| Roadmap presentation to executives fails due to lack of strategy narrative connecting features to business outcomes | $50K-$250K in lost confidence and deprioritized initiatives | Frame every feature as hypothesis with expected business impact; connect roadmap items to company OKRs; prepare trade-off scenarios for resource discussions |

| Gotcha | Cost | Fix |
|--------|------|-----|
| PRD written without engineering input, requiring major rework during implementation | $20K-$100K in wasted sprint cycles | Co-write technical sections with engineering lead; conduct technical feasibility review before PRD finalization; include non-functional requirements |
| Feature shipped without success metrics defined, making impact unmeasurable | $50K-$200K in unvalidated engineering investment | Define North Star and counter metrics before development starts; instrument analytics during build, not after launch; set evaluation timeline with go/kill criteria |
| Stakeholder alignment meeting ends with false consensus due to unvoiced concerns | $25K-$100K in rework when hidden objections surface | Use anonymous pre-read feedback before alignment meetings; explicitly ask for dissenting views; document decisions with named dissent where applicable |
| User research participants recruited from convenience sample biasing all findings | $30K-$150K in product decisions built on wrong user data | Define screening criteria based on target segments; recruit from multiple channels; validate sample against customer base demographics before analysis |
| Roadmap presentation to executives fails due to lack of strategy narrative connecting features to business outcomes | $50K-$250K in lost confidence and deprioritized initiatives | Frame every feature as hypothesis with expected business impact; connect roadmap items to company OKRs; prepare trade-off scenarios for resource discussions |

## Verification
<!-- STANDARD: 3min -->

- [ ] PRD review: stakeholders from Engineering, Design, QA, and Support have reviewed and approved
- [ ] User stories: each story has acceptance criteria written in Given/When/Then format
- [ ] RICE scoring: inputs (Reach, Impact, Confidence, Effort) are documented with sources/assumptions
- [ ] Competitive analysis: reviewed within last 90 days, includes at least 3 competitors
- [ ] Customer validation: at least 5 customer interviews support the problem hypothesis
- [ ] Success metrics: North Star metric identified, baseline measured, target set with timeline

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## Production Checklist
<!-- STANDARD: 3min -->

**(STANDARD)**

- [ ] **[PM1]** PRD written with: Executive Summary, Problem Statement, Success Metrics, Target Personas, User Stories, Functional & Non-Functional Requirements, Out of Scope, Assumptions & Risks
- [ ] **[PM2]** Every user story has Gherkin acceptance criteria (GIVEN/WHEN/THEN) covering happy path, edge cases, and error states
- [ ] **[PM3]** RICE prioritization complete: Reach, Impact, Confidence, and Effort documented with sources for each initiative
- [ ] **[PM4]** Kill criteria defined for every feature: target metric, baseline, 90-day target, and threshold below which feature is deprecated
- [ ] **[PM5]** Roadmap uses Now/Next/Later format with rolling 6-week certainty windows; no date-based commitments beyond current quarter
- [ ] **[PM6]** Stakeholder communication prepared: engineering brief (technical context), executive summary (risk/ROI), sales enablement (talking points/timeline)
- [ ] **[PM7]** Discovery buffer allocated: 20-30% of cycle capacity reserved for validation, spikes, and customer conversations
- [ ] **[PM8]** Competitive analysis reviewed within last 90 days; covers at least 3 competitors with feature parity and differentiation analysis
- [ ] **[PM9]** Customer validation: minimum 5 customer interviews support the problem hypothesis with behavioral evidence (not stated intent)
- [ ] **[PM10]** Post-launch retro scheduled within 2 weeks of GA; success metrics compared against PRD targets
- [ ] **[PM11]** Open questions have assigned owners and resolution dates; no question marked "TBD" without an owner
- [ ] **[PM12]** Every feature request (including executive requests) passes the same validation bar: user evidence or experiment data before greenlight

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
