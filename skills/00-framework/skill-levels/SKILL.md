---
name: skill-levels
description: >-
  Universal competency taxonomy mapping 5 mastery levels (L1 Apprentice → L5 Transformative)
  across all role families. Defines scope, autonomy, impact, and craft expectations at each
  level. Use to calibrate skill output depth, guide career development, and define what
  world-class means at every stage. Trigger: skill level, competency level, what level,
  senior vs staff, career ladder, engineering level, design level, PM level.
author: Sandeep Kumar Penchala
type: framework
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - skill-levels
  - competency-framework
  - career-ladder
  - mastery-taxonomy
  - level-calibration
token_budget: 4000
chain:
  feeds_into:
    - backend-developer
    - frontend-developer
    - fullstack-developer
    - mobile-developer
    - system-architect
    - api-designer
    - database-designer
    - ui-ux-designer
    - product-manager
    - product-strategist
    - devops-engineer
    - code-reviewer
    - qa-engineer
    - security-reviewer
    - engineering-manager
    - staff-engineer
    - director-engineering
    - vp-engineering
    - cloud-architect
    - platform-engineer
    - site-reliability-engineer
    - observability-engineer
    - docker-kubernetes
    - ci-cd-builder
    - business-strategist
    - ceo-strategist
    - cto-advisor
    - ux-researcher
    - brand-guidelines
    - accessibility-auditor
    - networking-engineer
    - tdd-guide
    - scrum-master

license: MIT
output: "reference"
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Skill Levels — Universal Competency Taxonomy
A 5-level mastery taxonomy defining what separates practitioners at every stage, from apprentice to transformative leader. Use this to calibrate skill output depth, set expectations, and define what excellence means concretely at each level.

**Inspired by**: Google Engineering Ladder (L3→L9), Stripe Engineering Levels, Dropbox Career Framework, Dreyfus Model of Skill Acquisition, Nielsen Norman Design Maturity, SVPG Product Career Levels.

---
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



## <!-- QUICK: 30s --> Route the Request

```
What are you trying to do?
├── Understand what a level means → Jump to "The Five Levels"
├── Calibrate a specific role at a specific level → Jump to "Role Family Calibration"
├── Integrate levels into skill invocation → Go to "Integration Guide"
├── Define what "world-class" means at each level → Read "The Expert's Mindset" + "What World-Class Means at Each Level"
└── Compare levels (e.g., Senior vs Staff) → Jump to "Level Transitions"
```

---

## The Expert's Mindset

Levels are a map, not the territory. The best practitioners don't think about their level — they think about the problem in front of them and apply whatever level of thinking it demands. A world-class L2 will occasionally think at L4 depth on a critical feature. A world-class L4 will occasionally write L2-level code when that's what's needed. **Mastery is knowing what level of thinking the situation requires and having the full range available.**

### Mental Models

| Model | Description |
|---|---|
| **Levels are lenses, not labels** | "I'm an L4" is a prison. "I can think at L4 depth when the problem demands it" is a superpower. Use levels to calibrate your thinking, not to constrain your identity. |
| **The best at any level operate one level up in critical moments** | When the most important project of the quarter hits a crisis, the world-class L2 thinks like an L3. The world-class L3 thinks like an L4. Not always — just when it matters. |
| **Promotion is a lagging indicator** | You get promoted to L4 after you've been operating at L4 for 6-12 months. The title recognizes what you've already become. Don't chase the title; chase the capability. |
| **Every level has its own form of excellence** | The goal is not to reach L5. The goal is to be world-class at whatever level you're at. A world-class L3 is worth more than a mediocre L5 in almost every context. |

### Cognitive Biases in Leveling

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Title inflation** | Assuming a "senior" title at a 20-person startup means the same thing as a "senior" title at Google | Always calibrate against behavioral anchors, not titles. "What's your scope? How many people do your decisions affect?" |
| **Level envy** | Feeling inadequate because you're "only L2" while peers are L3 | Compare yourself to the behavioral anchors, not to peers. Are you world-class at your level? That's the only comparison that matters. |
| **The Peter Principle** | Getting promoted to your level of incompetence because the skills at L(N) don't prepare you for L(N+1) | Every level transition requires deliberate skill-building in new dimensions. Don't assume L3 excellence predicts L4 success. |
| **Credentialism** | Over-weighting level/title in evaluation and under-weighting demonstrated capability | Evaluate the work, not the level. Some of the best code ever written was by L2 engineers. |

### What Masters Know That Others Don't

- **The quietest person in the room is often operating at the highest level.** L4s and L5s don't need to prove themselves. They ask questions that reframe the problem. They speak less and change the conversation more.
- **The best career strategy is to be undeniable.** Don't lobby for promotion. Produce work so clearly at the next level that promoting you becomes the obvious decision. Make your manager's case for them.
- **Levels are most useful for self-calibration, not for judging others.** Use the taxonomy to identify your growth edges. Using it to rank colleagues is a misuse that destroys psychological safety.
- **The skills that get you promoted are not the skills that make you fulfilled.** Many people reach L4 or L5 and discover they miss the craft work of L2/L3. The best career is the one where the work you do every day energizes you, regardless of level.

---

## <!-- STANDARD: 3min --> Ground Rules — Read Before Anything Else

- **Levels describe capability, not title.** Titles vary across companies. L3 at Google ≠ L3 at a startup. Use the behavioral anchors, not the number.
- **Level is a range, not a point.** A person can operate at L3 in architecture but L2 in communication. Level is the intersection of multiple dimensions.
- **Higher level ≠ better person.** L5 is not "better" than L3 — it's different. The best L3 practitioner in the world may deliver more value than a mediocre L5. Every level has its own form of excellence.
- **Level expectations compound.** L3 includes everything L2 does, plus new capabilities. Levels are cumulative, not replacement.
- **Admit when level calibration is uncertain.** If you lack context about a person's scope, impact, or craft, say so and ask.

---

## <!-- STANDARD: 3min --> Operating at Different Levels — The Five Levels

### Overview

| Level | Name | Scope | Time Horizon | Primary Output | Signature Question |
|---|---|---|---|---|---|
| **L1** | Apprentice | Task | Hours → Days | Correct implementation | "How do I do this?" |
| **L2** | Practitioner | Feature | Days → Weeks | Reliable delivery | "What needs to be done?" |
| **L3** | Senior | Project / Team | Weeks → Months | Direction + execution | "What should we do?" |
| **L4** | Staff / Lead | Multi-Team / Org | Months → Quarters | Standards + strategy | "How should we think about this?" |
| **L5** | Principal / Transformative | Company / Industry | Quarters → Years | Paradigm shift | "What's possible that wasn't before?" |

### The Four Dimensions

Every level is evaluated across four dimensions that compound:

| Dimension | What It Measures | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|---|
| **Scope** | Breadth of influence | Self | Feature / component | Project / team | Multiple teams / org | Company / industry |
| **Autonomy** | Degree of guidance needed | Close supervision | Independent within defined tasks | Self-directed; seeks input at boundaries | Defines own work; seeks input on strategy | Creates the direction others follow |
| **Impact** | Magnitude of outcomes | Task completion | Feature delivery | Team outcomes | Org-wide standards & multiplier effects | Industry patterns & paradigm shifts |
| **Craft** | Depth of domain mastery | Learning fundamentals | Solid execution | Deep expertise; teaches others | Defines craft standards | Redefines the craft |

---

### L1 — Apprentice

**The fundamental posture**: "I am learning how to learn in this domain."

An L1 practitioner is building the foundational mental models of the craft. They need clear task definitions, close guidance, and frequent feedback. Their primary goal is to build correct habits and understand *why* things work, not just *that* they work.

| Dimension | Behavioral Anchor |
|---|---|
| **Scope** | Individual tasks with clear boundaries and acceptance criteria. |
| **Autonomy** | Works from detailed instructions. Needs regular check-ins. Asks "is this the right approach?" before proceeding. |
| **Impact** | Delivers assigned tasks correctly and on time. Impact is measured in task completion quality. |
| **Craft** | Learning the tools, patterns, and vocabulary of the domain. Makes mistakes and learns from them. |

**What world-class L1 looks like**: Asks questions that reveal they're building mental models, not just getting unblocked. Documents their learning so the next L1 doesn't need to ask the same questions. Ships small things reliably — reliability at L1 builds the trust that enables L2 autonomy.

**Key transition — L1 → L2**: You stop needing detailed instructions. Someone says "add search to the API" and you can break that down into tasks yourself.

---

### L2 — Practitioner

**The fundamental posture**: "I deliver reliably and independently."

An L2 practitioner owns features end-to-end. They write code/tests/docs, handle edge cases, and know when to escalate. They are the reliable engine of the organization — the person you trust to get things done without drama.

| Dimension | Behavioral Anchor |
|---|---|
| **Scope** | Features or components. Owns a well-defined area of the product or system. |
| **Autonomy** | Works independently on defined features. Escalates when blocked or when requirements are ambiguous. |
| **Impact** | Delivers complete, tested, documented features. Impact is measured in feature delivery velocity and quality. |
| **Craft** | Solid fundamentals. Writes clean, tested, maintainable work. Knows the standard patterns and applies them correctly. |

**What world-class L2 looks like**: You never have to ask them "did you handle the edge cases?" — they already did. Their work is so thorough that code review finds logic gaps, not sloppiness. They anticipate problems before they happen. When they escalate, they come with options, not just problems.

**Key transition — L2 → L3**: You stop waiting to be told what to build. You see the problem, propose the solution, and drive it to completion. You start making others better through code review, documentation, and mentoring.

---

### L3 — Senior

**The fundamental posture**: "I define what should be built and make the team better."

The L3 shift is from *execution* to *direction*. An L3 defines the approach, not just implements it. They lead projects, mentor juniors, and make technical/design/product decisions that affect the team. This is the hardest transition in most careers because the skills that made you a great L2 (execution speed, individual throughput) are not the skills that make you a great L3 (decision quality, multiplying others).

| Dimension | Behavioral Anchor |
|---|---|
| **Scope** | Project or team. Designs solutions for ambiguous problems within a bounded domain. |
| **Autonomy** | Self-directed. Identifies problems worth solving and proposes solutions. Seeks input at project boundaries. |
| **Impact** | Team-level outcomes. The team is more effective because of this person's leadership — not just their individual output. |
| **Craft** | Deep expertise. Teaches L1s and L2s. Makes trade-off decisions with explicit rationale. Can design a solution and explain *why* it's the right approach. |

**What world-class L3 looks like**: When a world-class L3 leaves the team, velocity drops noticeably for weeks — not because they wrote all the code, but because they were the decision-making backbone. They make the team 2x better by raising standards through review, documentation, and teaching. Their technical/product/design judgment is trusted: when they say "this approach will work," people believe it.

**Key transition — L3 → L4**: You stop optimizing your team and start optimizing the system of teams. Your primary leverage shifts from teaching individuals to designing standards, patterns, and processes that scale without you.

---

### L4 — Staff / Lead

**The fundamental posture**: "I set the standards and direction for the organization."

The L4 shift is from *team leverage* to *organizational leverage*. An L4 doesn't just make their team better — they make multiple teams better through standards, architecture decisions, hiring bars, and cross-team coordination. They solve problems that no single team can solve.

| Dimension | Behavioral Anchor |
|---|---|
| **Scope** | Multiple teams or an entire organization. Solves cross-cutting problems: architecture that spans 5 teams, design systems used by 50 designers, product strategy for a product line. |
| **Autonomy** | Defines what problems are worth solving. Leadership asks them "what should we do?" not "can you do this?" |
| **Impact** | Organizational multiplier. A decision this person makes affects 20-100+ people. Their standards become the org's standards. |
| **Craft** | Defines craft standards. Writes the RFCs, design patterns, and best practices that others follow. External visibility: speaks at conferences, writes for the industry. |

**What world-class L4 looks like**: When a world-class L4 solves a problem, it stays solved. They don't just fix the symptom — they design a system that prevents the entire class of problem from recurring. Their documents (RFCs, strategy memos, design systems) influence decisions for years after they wrote them. They make the organization 5x better, not by doing more, but by making better decisions about what everyone should do.

**Key transition — L4 → L5**: You stop solving problems within the existing paradigm and start changing the paradigm itself. Your influence extends beyond your organization into the industry.

---

### L5 — Principal / Transformative

**The fundamental posture**: "I redefine what the craft can achieve."

An L5 practitioner doesn't just operate within the current understanding of the field — they expand what's understood to be possible. They create new patterns, new methodologies, new ways of thinking that others adopt. Their impact is measured in years and industries, not quarters and teams.

| Dimension | Behavioral Anchor |
|---|---|
| **Scope** | Company or industry. Creates approaches that become standard practice across organizations. |
| **Autonomy** | Defines the direction for the entire function. The organization builds strategy around their technical/product/design vision. |
| **Impact** | Paradigm shift. Something works differently — and better — across the industry because of their work. |
| **Craft** | Redefines the craft. Writes the book (literally or figuratively) that the next generation learns from. Creates tools, frameworks, or methodologies adopted industry-wide. |

**What world-class L5 looks like**: L5 practitioners are rare — maybe 1% of the field. They're the people whose blog posts you read, whose conference talks you watch, whose open-source projects you use. They see patterns before others and articulate them clearly enough that others can see them too. Their legacy is not code or designs — it's the *way people think* about the craft.

**Note**: L5 is not a promotion target. It's a description of impact that some people achieve. Most people will spend their careers at L3 or L4 and deliver extraordinary value. The goal is mastery at your current level, not racing to the next one.

---

## <!-- STANDARD: 3min --> Role Family Calibration

Each role family maps the universal levels to domain-specific behavioral anchors.

### Engineering (backend, frontend, fullstack, mobile, embedded, firmware)

| Level | Engineering Anchor |
|---|---|
| **L1** | Implements well-specified functions/components. Learning the language, framework, and toolchain. Needs code review on every change. |
| **L2** | Independently implements features. Writes tests, handles edge cases, debugs production issues. Code review focuses on design choices, not correctness. |
| **L3** | Designs features/systems for a team. Makes architectural decisions within a bounded domain. Mentors L1-L2. Writes design docs. On-call leadership. |
| **L4** | Designs systems spanning 3+ teams. Sets coding standards, architectural patterns, and quality bars for the org. Writes RFCs that influence 50+ engineers. |
| **L5** | Creates frameworks, languages, or methodologies adopted across companies. Industry-recognized expertise. "That library/pattern/tool everyone uses? They built it." |

### Design (UI/UX, brand, accessibility)

| Level | Design Anchor |
|---|---|
| **L1** | Creates UI components from existing design system specs. Learning interaction patterns, visual hierarchy, and tooling. |
| **L2** | Independently designs features with user validation. Produces component specs, handles states, delivers developer-ready handoff. |
| **L3** | Defines design patterns for a product area. Leads design for complex flows. Establishes the design rationale others follow. |
| **L4** | Creates design systems used org-wide. Defines visual language, interaction paradigms, and quality standards for 20+ designers. |
| **L5** | Industry-recognized design leadership. Creates methodologies or tools adopted across companies. "That interaction pattern/design system approach? They defined it." |

### Product Management

| Level | Product Anchor |
|---|---|
| **L1** | Writes user stories and acceptance criteria under guidance. Manages a well-defined backlog area. Learning discovery and prioritization. |
| **L2** | Owns a feature area end-to-end. Runs discovery, defines metrics, manages stakeholders. Delivers features that move metrics. |
| **L3** | Owns a product area. Sets roadmap, manages PM/stakeholder relationships. Makes prioritization decisions with incomplete data. |
| **L4** | Owns a product line or portfolio. Defines product strategy, manages PMs, negotiates cross-functional trade-offs at the org level. |
| **L5** | Company-level product strategy. Industry thought leadership. "That product framework/approach? They wrote the book." |

### Architecture (system, API, database, cloud, network)

| Level | Architecture Anchor |
|---|---|
| **L1** | Documents existing architecture under guidance. Learns modeling techniques and trade-off analysis. |
| **L2** | Designs components within established patterns. Makes technology choices within bounded contexts. |
| **L3** | Designs systems for complex domains. Makes build-vs-buy decisions. Produces architecture decision records with trade-off analysis. |
| **L4** | Defines architecture patterns for the organization. Sets technical standards (API design, data modeling, security) that all teams follow. |
| **L5** | Creates architecture methodologies adopted across the industry. "That architecture pattern/methodology? They established it." |

### DevOps & Infrastructure (DevOps, SRE, platform, observability, cloud, containers, CI/CD)

| Level | DevOps Anchor |
|---|---|
| **L1** | Operates existing infrastructure following runbooks. Learns IaC, monitoring, and incident response. |
| **L2** | Independently provisions and manages infrastructure for a service. Writes Terraform/Pulumi, configures monitoring and alerting. |
| **L3** | Designs infrastructure for complex systems. Manages multi-environment deployments, DR strategy, and SLO definition. |
| **L4** | Defines platform strategy for the organization. Builds self-service infrastructure, golden paths, and org-wide reliability standards. |
| **L5** | Creates infrastructure patterns or tools adopted across the industry. "That deployment strategy/platform approach? They pioneered it." |

### Quality & Security (QA, security, TDD, code review, accessibility testing)

| Level | Quality Anchor |
|---|---|
| **L1** | Executes test cases from test plans. Learns testing frameworks and bug reporting standards. |
| **L2** | Independently writes test automation for features. Designs test cases, reports bugs with reproduction steps. |
| **L3** | Defines test strategy for a product area. Sets quality standards, chooses testing approaches, mentors QA engineers. |
| **L4** | Defines quality strategy for the organization. Implements testing infrastructure, quality gates, and security review processes used by all teams. |
| **L5** | Creates testing/security methodologies adopted across the industry. "That testing framework/security approach? They developed it." |

### Data (data engineer, data scientist, analytics, ML/AI, database reliability)

| Level | Data Anchor |
|---|---|
| **L1** | Writes queries and basic pipelines under guidance. Learning data modeling and the data stack. |
| **L2** | Builds data pipelines, models, and dashboards independently. Delivers reliable data products. |
| **L3** | Designs data architecture for a domain. Makes modeling decisions with downstream impact awareness. Mentors data practitioners. |
| **L4** | Defines data strategy for the organization. Sets data modeling standards, pipeline patterns, and quality bars for 20+ data practitioners. |
| **L5** | Creates data methodologies or tools adopted across the industry. "That data modeling approach/ML framework? They invented it." |

### Leadership (EM, director, VP, CTO, scrum master, project/program manager)

| Level | Leadership Anchor |
|---|---|
| **L3** | Manages a team of 4-8. Runs 1:1s, performance reviews, hiring. Translates strategy into team execution. |
| **L4** | Manages managers. Designs org structure for 20-80 people. Sets engineering/design/product culture for a department. |
| **L5** | Company-level leadership. Defines culture, sets org-wide strategy, manages executive relationships, represents the company externally. |

---

## What World-Class Means at Each Level

"World-class" is not a level — it's a description of **how** you operate at your current level. A world-class L2 is more valuable than a mediocre L4 at many things. Here's what world-class means concretely at each level:

| Level | World-Class Means... |
|---|---|
| **L1** | You learn faster than anyone expects. You ask questions that reveal you're building mental models. Your work is thorough beyond your experience level. Seniors fight to mentor you because the ROI is obvious. |
| **L2** | You deliver with a reliability that borders on boring. Edge cases are handled before anyone asks. Your code/designs/specs need minimal review. You make the senior engineers' lives easier, not harder. |
| **L3** | Your judgment is trusted without verification. When you say "this is the right approach," the team aligns behind it. The team is measurably better because you're on it — velocity, quality, and morale all improve. |
| **L4** | Your influence persists after you leave. The standards you set, the documents you wrote, the patterns you established continue shaping decisions years later. People you mentored become L3s and L4s themselves. |
| **L5** | You changed how the industry thinks. Practitioners who have never met you use your ideas daily. Your work created new possibilities that didn't exist before. |

---

## <!-- STANDARD: 3min --> Level Transitions

The hardest transitions in most careers:

| Transition | Why It's Hard | The Pivot |
|---|---|---|
| **L1 → L2** | Letting go of the need for detailed instructions. Building confidence in your own judgment. | Start proposing solutions instead of asking for them. "Here's my plan — does this look right?" |
| **L2 → L3** | The skills that made you a great L2 (execution speed, individual output) are not the skills that make you a great L3 (decision quality, multiplying others). | Spend less time doing. Spend more time deciding, teaching, and reviewing. Your output is the team's output. |
| **L3 → L4** | Letting go of team-level impact. Your "team" becomes the organization; your "code" becomes standards, RFCs, and patterns. | Stop optimizing your team. Start optimizing the system of teams. Write more. Speak less. |
| **L4 → L5** | The transition requires external impact — industry recognition, paradigm-shifting work — that can't be engineered through effort alone. | Build things that change how people think. Write, speak, and create tools that others adopt. This transition is earned, not promoted into. |

---

## Integration Guide

### How to Invoke a Skill at a Specific Level

When invoking any skill, you can specify the target level:

```
"As an L3 backend developer, design the API for a payment processing system."
"Review this PR at L4 staff engineer level — focus on architectural implications."
"Design this onboarding flow as an L2 UI/UX designer — I need production-ready specs."
"Prioritize this backlog at L4 product manager level — strategic, portfolio-wide view."
```

### How Levels Affect Skill Output

| Level | Output Characteristics |
|---|---|
| **L1** | Step-by-step guidance, explicit instructions, educational explanations of why. Safe defaults. |
| **L2** | Production-ready output with edge cases handled. Assumes competence, focuses on correctness. |
| **L3** | Trade-off analysis included. Design rationale. Considers team-wide implications. Mentoring notes included. |
| **L4** | Cross-team implications. Standards-setting. Patterns that scale. Organizational multiplier considerations. |
| **L5** | Paradigm-challenging. Industry context. Novel approaches. "Here's how this could change how we think about the problem." |

### Default Level Behavior

If no level is specified:
- **Individual contributor skills** default to **L2** (practitioner) — production-ready, independent execution
- **Leadership skills** default to **L3** (senior) — team-level direction
- **Architecture skills** default to **L3** (senior) — system-level design with trade-offs
- **Strategy skills** default to **L4** (staff/lead) — org-level thinking

## <!-- DEEP: 10+min --> Gotchas

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Using years-of-experience as the primary leveling criterion instead of scope and impact | Tenure is a poor proxy for capability; scope of influence determines actual level, not years served | Level by scope of influence (team → multi-team → org → company → industry), not by tenure. A 5-year engineer leading a 20-person migration is L4; a 15-year engineer maintaining a single service is L2 | **$150K-$300K/yr** — Over-leveled engineers stall team velocity 30-40%; under-leveled top performers leave within 6 months, each departure costing **$75K-$200K** in recruiting + onboarding. Level by scope, not tenure. |
| Creating a leveling ladder without behavioral anchors — just listing technical skills per level | Behavioral anchors make levels measurable and consistent; without them, two managers interpret the same rubric differently | Every level must define: (a) scope of ownership, (b) ambiguity handled, (c) influence radius, (d) craft excellence required. Include 3+ concrete behavioral examples per level from your actual codebase | **$500K-$2M/yr** — Inconsistent leveling across 50+ engineers creates systemic comp inequity, attrition clusters, and potential pay discrimination claims. Behavioral anchors prevent calibration drift. |
| Skipping calibration sessions between managers during promotion cycles | Without calibration, each manager applies the rubric differently, introducing systemic bias into promotion decisions | Run 2-hour calibration sessions every promotion cycle. Each manager presents evidence against level criteria. Use a calibration matrix: every engineer rated by 2+ managers independently before discussion | **$100K-$400K/yr** — Promotion rates vary 3-5x between managers; high performers under strict managers get stuck while mediocre engineers under lenient managers get promoted. Calibration sessions enforce consistency. |
| Copying another company's leveling ladder without adapting to your context | Leveling reflects organizational scale; a ladder for 10,000-person companies creates impossible bars at 50-person startups | Design levels around the *actual scope available in your organization*. If your biggest projects involve 5 engineers, your terminal level should reflect leading 5-person projects, not 30-person FAANG equivalents | **$1M-$5M/yr** — FAANG L6 scope doesn't exist at startups, causing stagnation or title inflation. Adapt leveling to your org's actual scale. |
| Not updating leveling criteria as the company scales (seed → Series A → Series C → public) | Leveling criteria designed for a 20-person company break at 200 people; what was "wears all hats" becomes "lacks specialization" | Review and recalibrate leveling ladder every 18-24 months or at each major scale milestone (50 → 150 → 500 → 2000 people). Grandfather existing employees with a 12-month transition window | **$2M-$10M/yr** — Engineers hired at Series A get trapped at L3 because the L4 bar shifted to "cross-org influence" that didn't exist at hiring time. Recalibrate at every scale milestone. |
| Using level as a proxy for respect, decision authority, or idea quality | When level determines who gets heard, organizations lose the best ideas from junior contributors and silence healthy challenge | Explicitly separate "decision rights" from "level." A L2 engineer with data should be able to challenge an L5 architect's design. Formalize this in your RFC/design review process: all levels participate, decisions are made on evidence not authority | **Immeasurable** — Junior engineers stop proposing ideas; senior engineers stop questioning bad decisions; psychological safety erodes; innovation collapses. Decouple decision rights from level. |
| No terminal (career) level — requiring continuous promotion to remain in good standing | Without a terminal level, the only growth path is management, forcing deep practitioners into roles they don't want | Define a terminal level (typically L4 or L5) where an engineer can stay indefinitely with cost-of-living adjustments. Career growth at terminal level means *deepening* craft, not climbing ladder. ~40% of engineers should be at or near terminal level in a healthy org | **$500K-$1.5M/yr** — Loses deep technical expertise; creates managers who resent managing. Terminal levels retain craft excellence and prevent forced management conversions. |


## Gotchas

- **Level inflation — everyone is "Senior" or "Lead."** A 30-person startup with 15 "Senior Engineers" and 8 "Staff Engineers" has no actual leveling — just title generosity as a retention tactic. When titles inflate, real senior people lose motivation (their title means nothing), and junior people stop growing (they already have the title). The fix: define level criteria before assigning titles, and be willing to have the hard conversation when someone's title doesn't match their scope. **Total cost: $300K-$800K annually** — inflated titles create compensation arms races (every "Senior" expects senior-market pay), make external hiring confusing (candidates can't gauge actual seniority), and cause real senior talent to leave when their hard-earned level is diluted.

- **Levels that don't translate across functions.** Your engineering ladder has granular levels (L1-L7) with detailed behavioral anchors, but Design, Product, and Marketing have "Junior / Mid / Senior / Director" with no shared criteria. Cross-functional calibration becomes impossible — is a "Senior PM" equivalent to an L5 Engineer or an L4? Compensation bands drift, internal transfers create equity disputes, and IC paths disappear in functions without engineering's rigor. **Total cost: $200K-$500K annually** — misaligned leveling across functions creates comp inequity that surfaces in every promotion cycle and exit interview. Designers and PMs leave for companies where their career path is as clearly defined as engineering's.

- **Using levels to justify compensation without performance calibration.** Two L4 engineers on the same team: one is a top performer delivering 3x the output, the other is coasting. Both get the same "L4 band" raise because "that's the compa-ratio for the level." Within 6 months, the top performer leaves for a company that pays for performance, and the coaster stays forever. Levels define responsibility scope — they are not a substitute for differentiating pay based on impact. **Total cost: $150K-$400K per departure** — losing a top performer costs 1.5-2x salary in recruiting + onboarding + lost productivity. Over 3-5 years, performance-blind leveling systematically drives out your best people while retaining mediocrity.

## Error Recovery

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Two managers assign different levels to the same engineer using the same rubric | Leveling rubric lacks behavioral anchors — managers fill gaps with personal interpretation | Add 3+ concrete behavioral examples per level from actual work. Run calibration sessions where managers independently rate the same 5 cases, then discuss divergence | **$500K-$2M/yr in attrition** — Inconsistent leveling across managers causes pay inequity and retention crises. Behavioral anchors + calibration sessions are the only defense |
| Skill output is consistently at wrong depth (too shallow for senior work, too complex for junior) | The skill was invoked without a level parameter, defaulting to L2/L3 regardless of actual need | Always pass a level parameter when invoking skills. Every SKILL.md should accept `--level L1-L5` as a top-level parameter | **Skills produce wrong-level output silently** — an L4 design review with L2 depth misses architectural risks; an L2 onboarding with L5 depth overwhelms |
| Engineer got promoted but can't perform at the new level | The Peter Principle: L(N) skills don't prepare for L(N+1). The promotion was based on L(N) excellence | Every level transition requires deliberate skill-building in new dimensions. Create a 90-day transition plan for each promotion with explicit new-scope milestones | **$75K-$200K per failed promotion** — Promoting people to their level of incompetence loses both the excellent contributor they were AND the leader they can't become |

## Deliberate Practice

To build leveling calibration instinct:

1. **Reverse-calibrate 5 people you've worked with.** Take 5 colleagues and independently rate them on all 4 dimensions (scope, autonomy, impact, craft). Write down your rationale. Then compare with the leveling rubric. Where did you diverge? Why?
2. **Write a promotion packet for a hypothetical candidate.** Pick a level transition (L2→L3, L3→L4, L4→L5). Write a complete promotion justification using the behavioral anchors. Have someone who's been through that transition review it.
3. **Calibrate 3 public figures.** Pick 3 well-known engineers/designers/PMs whose work you can observe publicly (conference talks, open-source, blog posts). Map them to levels based on observable scope and impact. This builds calibration independent of title.
4. **Run a mock calibration session.** Gather 3+ peers, present 3 anonymized cases, and have everyone independently rate. Discuss divergence. This builds the muscle for real calibration panels.

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Company passes a scale milestone (50→150, 150→500, 500→2000 people) | Recalibrate leveling ladder within 90 days. Scope expectations at each level shift with org size | Leveling designed for 50 people breaks at 200. What was "org-wide impact" at 50 is "team impact" at 500 |
| Promotion rate varies >2x between managers or departments | Run emergency calibration session. Audit last 2 promotion cycles for systemic bias | Promotion rate disparity indicates inconsistent application of the rubric — fix the process, not the people |
| >20% of engineering is at the same level for >3 years | Investigate: is this a healthy terminal level or a bottleneck? If bottlenecked, identify the barrier (scope unavailable, rubric too hard, manager gatekeeping) | Mass stagnation at one level means either the leveling ladder is wrong or career paths are blocked |
| New role family introduced without level mapping | Within 30 days: map the new role to all 5 levels using the 4-dimension framework. Run calibration with adjacent role families | Ungraded roles create comp anomalies and career dead-ends |

## State Log

This skill maintains a **decision ledger** for level calibration sessions.

### How the State Log Works

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for prior calibration decisions.
2. **After each major decision:** Record level assignments, calibration rationales, and scope judgments.
3. **Before completing work:** Verify all leveling decisions are documented with behavioral evidence.
4. **On context recovery:** Read the last 5 entries before proposing level changes.

### Anti-Drift Check

- [ ] Have I read the state log from the previous calibration session?
- [ ] Do any prior level assignments constrain what I'm about to recommend?
- [ ] Is my calibration consistent with the 4-dimension framework?
- [ ] If I'm contradicting a prior level assignment, have I documented WHY with behavioral evidence?

## Complete When

| # | Complete when... | Verify |
|---|---|---|
| ☐ | Level assignment includes behavioral evidence from all 4 dimensions (scope, autonomy, impact, craft) — not just title or years | Audit the assignment rationale; every dimension has ≥1 concrete behavioral example |
| ☐ | Calibration session has ≥2 independent raters who assigned levels BEFORE discussion — no anchoring bias | Check calibration records; independent ratings precede consensus discussion |
| ☐ | Terminal level exists and ~40% of org population is at terminal with COLA — no up-or-out pressure | Check org distribution; terminal-level engineers have documented "sustained contribution" expectation |
| ☐ | Level transitions include 3+ documented behavioral examples per level from actual work — not abstract rubrics | Audit behavioral anchors; every level-pair has concrete "here's what L(N) → L(N+1) looks like" |
| ☐ | New role family is mapped to all 5 levels within 30 days of creation — no ungraded roles | Cross-reference role families against leveling guide; zero unmapped families |
| ☐ | Cross-manager calibration sessions run every promotion cycle — leveling is not manager-dependent | Audit promotion records; every promotion has calibration-session sign-off from ≥2 managers |
| ☐ | Decision rights are decoupled from level — L2s can challenge L5s in design reviews with evidence-based arguments | Audit design review records; challenges are evaluated on evidence, not seniority |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `people-ops` | Compensation bands, promotion budgets, headcount planning aligned to levels | Before finalizing level assignments that have compensation implications |
| `hr-manager` | Performance review frameworks, PIP templates, career development plans | When leveling decisions intersect with performance management |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `backend-developer` | Level calibration for backend output depth | Skill produces wrong-depth output without level parameter |
| `frontend-developer` | Level calibration for frontend output depth | Same as above |
| `system-architect` | Level calibration for architecture design depth | Architecture at wrong level misses risks or over-engineers |
| `engineering-manager` | Career ladder framework for team development | Managers can't set growth expectations without leveling |
| `staff-engineer` | L4→L5 transition criteria, scope definitions | Staff+ engineers need clear scope expectations |

## What Good Looks Like

A world-class leveling system produces:

- **Consistent evaluations:** Two managers independently rate the same engineer within 0.5 levels 90%+ of the time
- **Clear behavioral anchors:** Every level has 3+ concrete examples of what L(N) behavior looks like in practice, drawn from actual work
- **Terminal level exists:** Engineers can stay at L4/L5 indefinitely with COLA — ~40% of the org should be at terminal level
- **Calibration sessions run:** Every promotion cycle includes cross-manager calibration with independent ratings before discussion
- **Scale-adapted:** Leveling criteria reviewed every 18-24 months and recalibrated at each major scale milestone
- **Decoupled from authority:** Decision rights are based on expertise and evidence, not level. L2s can challenge L5s in design reviews
- **Transparent:** Every engineer knows what L(N+1) requires, has a growth plan, and understands the evidence standard for promotion

The leveling system doesn't rank people — it creates clarity. Everyone knows where they are, what's next, and how to get there.

## <!-- DEEP: 10+min --> Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We just need more senior engineers" | Adding senior ICs without clear scope ownership and decision rights creates parallel work streams that collide — senior talent under bad system design amplifies waste, not throughput. |
| "Titles don't matter — just focus on the work" | Titles calibrate scope, autonomy, and compensation expectations across the organization; ambiguous leveling creates resentment and attrition among top performers who see peers with same title but half the scope. |
| "Our leveling guide is comprehensive enough" | A leveling guide without behavioral examples and calibration exercises produces inconsistent evaluations — two managers reading the same rubric can reach opposite conclusions for the same engineer. |
| "We can borrow FAANG leveling criteria" | FAANG leveling reflects FAANG-scale problems with abundant support staff; mid-size companies need different scope expectations at each level or they over-hire for narrow roles and under-develop generalists. |
| "Promotions will happen when people are ready" | Without explicit leveling criteria, documented evidence standards, and cross-manager calibration sessions, promotion decisions become manager-dependent and favor the loudest advocates, not the most impactful contributors. |

---

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## Anti-Hallucination
<!-- STANDARD: 3min -->

* Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
* Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
- [VERIFIED] — Confirmed against official documentation or published standards
- [COMMON-PRACTICE] — Widely used in the industry
- [INFERRED] — Reasonable extrapolation from general principles
- [UNKNOWN] — Requires verification against specific context

## References

Detailed reference material loaded on demand:

- **Production Checklist**: See [checklist.md](references/checklist.md)
