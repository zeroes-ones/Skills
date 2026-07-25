## Core Workflow

This is the complete skill generation protocol — Phase 0 through Phase 10. Each phase builds on the previous. Skip phases only if you're in targeted enhancement mode (audit → identify gaps → fill only those gaps).

### Phase 0: Discovery & Domain Analysis (~15 min)

Before writing ANY content, answer these 8 questions. The answers determine the entire structure of the generated skill.

**1. What domain/task does this skill cover?**
Be specific. "React Native mobile development" — not "mobile development." "PostgreSQL database administration" — not "databases." The name becomes the skill's directory name and frontmatter `name` field.

**2. What problem does it solve?**
What does the agent produce after using this skill? A working React Native app with offline support? A hardened Kubernetes deployment? A HIPAA-compliant data pipeline? This becomes the "What Good Looks Like" paragraph.

**3. Who is the target user (agent persona)?**
Is this for backend developers, mobile developers, security engineers, data scientists, or a generalist? The persona determines the assumed knowledge level. A skill for security engineers can assume knowledge of OWASP; a skill for generalists must explain basic security concepts.

**4. What's the complexity tier?**
- **Tier 1 (core specialized):** Narrow domain, deep expertise. E.g., iOS Developer, GraphQL Engineer. 400-600 lines.
- **Tier 2 (broad applicable):** Wide domain, moderate depth. E.g., Fullstack Developer, DevOps Engineer. 500-700 lines.
- **Tier 3 (security/critical):** High-stakes domain. E.g., Security Reviewer, HIPAA Implementation. 600-1000 lines.

**5. What existing skills should it connect to (upstream/downstream)?**
Search the repository for related skills. A "Kubernetes Developer" skill should consume from `docker-kubernetes`, `devops-engineer`, `cloud-architect` and feed into `site-reliability-engineer`, `security-engineer`.

**6. Are there existing reference skills to model from?**
Identify 2-3 top-tier skills in related domains. Study their ground rules, gotchas, decision trees. Template from them — don't copy. The mobile-developer skill serves as a template for any platform-specific development skill. The security-reviewer skill serves as a template for any security domain skill.

**7. What are the 3 most expensive mistakes in this domain?**
These become gotchas. Research: search "[domain] expensive bug" on Hacker News, search "[domain] post-mortem", search CVE database for domain-specific vulnerabilities, search "[domain] outage cost" on Google. Each mistake should have a verifiable dollar figure from a real incident.

**8. What are the 3 most common rationalizations?**
These become anti-rationalization entries. Ask: "What lies do practitioners in this domain tell themselves?" For each rationalization, identify the cognitive bias behind it: optimism bias, normalcy bias, sunk cost fallacy, authority bias, Dunning-Kruger effect, diffusion of responsibility.

**Output:** A discovery document (in memory — do not create files) answering all 8 questions. This document drives all subsequent phases.

### Phase 1: Structural Scaffolding (~10 min)

**1. Determine the category directory.**
Map the domain to a category directory. Use this mapping:
- Strategy/leadership → `01-strategy/`
- Product management → `02-product/`
- Design/UX → `03-design/`
- Architecture → `04-architecture/`
- Development → `05-development/`
- Quality/testing → `06-quality/`
- DevOps/infrastructure → `07-devops/`
- Security → `08-security/`
- Data/AI → `09-data/`
- Growth/marketing → `10-growth/`
- Legal/compliance → `11-legal/`
- Operations → `12-operations/`
- Specialized/emerging → `13-specialized/`

If no category fits, use `13-specialized/`. Only create a new category with strong justification (at least 3 planned skills).

**2. Generate the YAML frontmatter.**
```yaml
---
name: {kebab-case-name}
description: >
  Use when {triggers}. Handles {capabilities}. Do NOT use for {boundaries}.
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: {matching category type}
status: stable
version: 1.0.0
updated: {today's date}
tags: [{3-8 domain-specific tags}]
token_budget: {estimated based on tier}
chain:
  consumes_from: [{at least 2 upstream skills}]
  feeds_into: [{at least 2 downstream skills}]
  alternatives: []
---
```
**Critical:** The description must follow the triggers-only format: "Use when [situation]. Handles [capabilities]. Do NOT use for [boundaries]." No process language in the description field.

**3. Create the file and directory structure.**
```bash
mkdir -p skills/{category}/{skill-name}/references/
```
The file path must match: `skills/{category}/{skill-name}/SKILL.md`

**Output:** Frontmatter written, directory created, file scaffolded.

### Phase 2: Domain-Specific Ground Rules (~20 min)

Ground rules are the HARDEST section to write well. They must be:
- **Domain-specific:** Not "Be careful with auth" but "Never embed API keys in client-side code — use OAuth2 PKCE with secure token storage"
- **Actionable:** The agent can mechanically check for violations
- **Testable:** A behavioral eval can verify the agent follows the rule
- **Violation-illustrated:** Each rule shows exactly what happens when broken

**Research process for ground rules:**
1. Search OWASP Top 10 for the domain's technology stack
2. Search CWE Top 25 for domain-specific weakness categories
3. Search "[domain] common mistakes" on Stack Overflow (sort by votes)
4. Search "[domain] production incident" on Hacker News
5. Identify platform-specific constraints (OS limits, framework quirks, language footguns)
6. For each finding, formulate as: "REFUSE/DETECT [bad thing] → Mechanical Trigger → Violation Response"

**Ground rule format (non-negotiable):**
| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---|---|---|
| R1 | REFUSE [action] | Trigger: [grep-able condition] | STOP. Respond: "[Exact message with fix]" |

**Target:** 6-10 ground rules. Standard skills: 6-8. Security/critical skills: 8-10.

**What good looks like for Phase 2:** Every ground rule is domain-specific. No rule could be copied into a different skill without modification. A domain expert reads the rules and says "yes, these are exactly the 8 things that go wrong in this domain."

### Phase 3: Decision Trees (~25 min)

Build 3-5 ASCII decision trees. Each tree must have:
- A clear START node with a decision question
- At least 2 levels of YES/NO branching
- Terminal nodes with concrete recommendations
- "When NOT to use" guidance at terminal nodes
- ASCII box-drawing characters: `┌─┐└─┘├─┤│▼`

**Decision trees to build (in priority order):**

**1. Architecture/approach selection tree**
The core "what technology/approach should I use?" question. E.g., for a mobile skill: Native vs React Native vs Flutter vs PWA. For a database skill: PostgreSQL vs MongoDB vs DynamoDB. Include performance benchmarks, team skill requirements, and deployment complexity at terminal nodes.

**2. Pattern selection tree**
A common implementation choice. E.g., CQRS vs CRUD, Event-driven vs Request-response, Microservices vs Monolith, REST vs GraphQL vs gRPC. Terminal nodes must include: "Use [pattern] when [3 conditions]. Do NOT use when [2 conditions]."

**3. Safety/security decision tree**
A security-critical choice. E.g., Self-hosted vs managed service, Encrypt at rest vs application-level encryption, OAuth2 vs API keys. Terminal nodes must include worst-case scenarios for wrong choices.

**4. Scale/deployment decision tree**
A deployment or scaling decision. E.g., Serverless vs Container vs VM, Single-region vs Multi-region, CDN vs origin-only. Terminal nodes must include cost estimates and latency comparisons.

**5. Domain-specific workflow tree (optional for standard skills, required for security/critical)**
A decision that's unique to this domain. E.g., for a healthcare skill: "PHI data handling: de-identify vs encrypt vs tokenize."

**ASCII tree formatting rules:**
- Use `┌─┐` for start nodes, `└─┘` for terminal nodes
- Branch with `├──` and `└──`, vertical lines with `│`
- Label branches with `YES` and `NO`
- Include a brief explanation paragraph after each tree
- Verify rendering in raw markdown — no broken characters

**What good looks like for Phase 3:** An agent facing the domain's core architectural question can follow the decision tree to a concrete recommendation in under 30 seconds. The tree encodes 5+ years of practitioner experience in choosing the right approach.

### Phase 4: Core Workflow Phases (~35 min)

Design 8-10 progressive phases that mirror the real development/execution lifecycle for this domain.

**Phase structure pattern:**
```
### Phase N (~time estimate): Phase Title
1. **Action verb:** Concrete step with exact commands, code, or configuration
2. **Action verb:** Next concrete step
3. **Verify:** What to check to confirm the phase is complete
**Output:** Tangible deliverable from this phase
```

**Phase template (adapt to domain):**
- **Phase 0:** Discovery/Requirements gathering — What problem are we solving? What are the constraints?
- **Phase 1:** Setup/Environment — Tool installation, project scaffolding, configuration
- **Phase 2:** Core Architecture — System design, component structure, data flow
- **Phase 3:** Primary Implementation — The main feature/system/process being built
- **Phase 4:** Integration — Connecting with external systems, APIs, databases
- **Phase 5:** Error Handling & Edge Cases — What goes wrong and how to handle it
- **Phase 6:** Performance Optimization — Profiling, benchmarking, optimization
- **Phase 7:** Security Hardening — Threat modeling, vulnerability remediation, security testing
- **Phase 8:** Testing & Validation — Unit, integration, e2e, load testing
- **Phase 9:** Deployment & Monitoring — Production deployment, observability, alerting

**For non-development domains (strategy, operations, design):** Adapt the phases to the domain's workflow. A "Business Strategist" skill's phases would be market analysis → model design → financial projection → validation → iteration. A "Technical Writer" skill's phases would be audience analysis → outline → draft → review → publish.

**What good looks like for Phase 4:** A practitioner can follow the phases sequentially and produce a complete, production-quality output. Each phase has time estimates that are realistic. No phase says "think about X" — every phase says "DO X" with concrete steps.

### Phase 5: Gotchas (~25 min)

Research and document 10+ dollar-quantified gotchas. This is where the skill earns its 10/10* rating — generic warnings get 6/10; dollar-quantified incident-backed gotchas get 10/10*.

**Gotcha research protocol:**
1. **CVE database search:** Search NVD for domain-specific CVEs (e.g., "react native CVE", "kubernetes CVE"). For each CVE, calculate: breach cost (IBM average: $4.45M), remediation hours × engineer hourly rate ($150/hr), downtime hours × revenue/hour.
2. **Hacker News post-mortems:** Search `site:news.ycombinator.com "[domain] outage" OR "[domain] breach" OR "[domain] bug"`. Extract the cost figures from the post-mortem.
3. **Cloud provider outage reports:** AWS, GCP, Azure publish post-mortems with impact analysis. Extract the customer impact costs.
4. **Stack Overflow:** Search "[domain] most expensive mistake" or "[domain] cost us". The war stories have real dollar figures.
5. **Industry reports:** IBM Cost of a Data Breach report, Google SRE book incident chapters, Honeycomb outage post-mortems.

**Gotcha format (each must follow this pattern):**
```
- **Gotcha title with dollar figure in first sentence.** Description of the temptation and what goes wrong.
  **Total cost: $XX,XXX-$XXX,XXX in [specific impact — not just "costs"].**
  Fix: [3-5 concrete prevention steps — exact commands, configuration, architecture changes].
```

**Target:** 10+ gotchas for standard skills, 15+ for security/critical skills. Every gotcha must have a SPECIFIC dollar range. "Can be expensive" → reject. "$15,000-$50,000 in lost installs from negative reviews" → accept.

**What good looks like for Phase 5:** A domain expert reads the gotchas and says "I wish I had read this before my $50,000 mistake in 2021." Every gotcha references a real incident class (even if anonymized).

### Phase 6: Anti-Rationalization Table (~20 min)

The anti-rationalization table is the agent's psychological defense system. It preempts the lies practitioners tell themselves.

**Research process for anti-rationalization:**
1. For each gotcha from Phase 5, ask: "What rationalization leads to this mistake?"
2. For each rationalization, identify the cognitive bias: optimism bias ("it won't happen to us"), normalcy bias ("this is how everyone does it"), sunk cost ("we've already invested in this approach"), authority bias ("the framework authors know best"), Dunning-Kruger ("we know enough, we don't need experts"), diffusion of responsibility ("security team handles that").
3. For each rationalization, craft the "Why It Feels Right" — the genuine, psychologically valid reason this feels reasonable. This is the hardest column. It must make the reader think "yeah, I've thought that."

**Format (4 columns, non-negotiable):**
| The Temptation | Why It Feels Right | The Devastating Reality | Prevention |
|---|---|---|---|
| "The specific rationalization" | The genuine, valid-feeling reason this is tempting | The concrete, dollar-quantified outcome | The specific counter-action |

**Target:** 6+ entries for standard skills, 8+ for security/critical skills.

**What good looks like for Phase 6:** A practitioner reads the table and feels personally called out by at least 3 entries. The "Why It Feels Right" column makes them uncomfortable because it's exactly what they've told themselves.

### Phase 7: Error Recovery & Verification (~20 min)

**Error Recovery — 5+ scenarios:**
Each scenario must have:
- **Error description:** The exact error message or symptom
- **Root cause:** Why this happens in this domain specifically
- **Step-by-step recovery:** Numbered steps with exact commands
- **Prevention:** How to avoid it next time

**Error scenarios to cover:**
1. Deployment/release failure (most common)
2. Data corruption or loss (most expensive)
3. Security incident response (most urgent)
4. Performance degradation (most insidious)
5. Dependency/third-party failure (most unpredictable)
6. Configuration drift (most preventable)
7. Authentication/authorization failure (most user-impacting)

**Verification Guardrails — 10+ binary checklist items:**
Each item must be:
- Binary: pass/fail, yes/no — no "mostly" or "partially"
- Actionable: the agent can mechanically check it
- Domain-specific: not "tests pass" but "all 12 offline-mode test scenarios pass on a throttled 3G connection"

**Format:**
```
- [ ] **[PREFIX-1]** Specific, binary check that the agent can verify mechanically
- [ ] **[PREFIX-2]** Next check with domain-specific prefix (e.g., MOB, API, SEC, DB)
```

**Target:** 5+ error scenarios, 10+ verification guardrails.

### Phase 8: Scale Depth Matrix (~15 min)

Cover all four scales: Solo → Small → Medium → Enterprise.

**For each scale, answer:**
- **What changes:** Tools, processes, depth of application
- **What to skip:** What's overkill at this scale
- **Transition trigger:** What signals it's time to move to the next scale
- **Coordination model:** Who coordinates with whom at this scale
- **Domain-specific scaling concern:** What breaks at this scale in this specific domain

**Format:** Table with columns: Scale, What Changes, What to Skip, Transition Trigger.

**Cross-skills Integration table:**
| Step | Skill | What it produces |
|---|---|---|
| **Before** | {upstream skills} | {what they produce for this skill} |
| **This** | {this skill} | {what this skill produces} |
| **After** | {downstream skills} | {what they produce from this skill's output} |

### Phase 9: Cross-Skill Integration (~15 min)

**Upstream skills table:**
| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `{skill-name}` | Specific artifact, data, or decision | The trigger condition for involving this skill |

**Downstream skills table:**
| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `{skill-name}` | Specific artifact or decision | What happens if this skill's output is delayed |

**Communication triggers table:**
| Trigger | Notify | Why |
|---|---|---|
| Specific detectable event | Which skill to notify | Why this matters to the downstream skill |

**Escalation path (ASCII tree):**
```
{Specific problem}? → {First escalation target} → {Second escalation target}
```

**Common chains:**
```
- **Chain**: {skill-1} → {skill-2} → {skill-3} — {description of what flows through this chain}
```

### Phase 10: Quality Validation (~15 min)

**Automated checks:**
```bash
bash scripts/validate-skills.sh          # 6/6 governance checks
python3 scripts/skill-router.py --chain {name}  # Chain connectivity verification
```

**Manual checks (run through every item):**
- [ ] All 12+ mandatory sections present and non-empty
- [ ] YAML frontmatter has name, description, category, tier, chain_feeds_into (≥1), chain_consumes_from (≥1)
- [ ] Frontmatter description is one paragraph, triggers-only format
- [ ] At least 3 ASCII decision trees with YES/NO branching
- [ ] At least 6 ground rules, each with concrete violation example
- [ ] At least 10 gotchas with dollar figures ($X,XXX+)
- [ ] Anti-rationalization table has exactly 4 columns and 6+ rows
- [ ] Error Recovery has 5+ scenarios with step-by-step commands
- [ ] Verification Guardrails has 10+ binary [ ] checklist items
- [ ] Cross-Skill tables have upstream AND downstream
- [ ] Scale Depth covers Solo→Small→Medium→Enterprise with transition triggers
- [ ] Production Checklist has 13+ items with domain-specific prefixes
- [ ] No placeholder/TODO/TBD/"[...]" content anywhere
- [ ] File path matches pattern: skills/{category}/{skill-name}/SKILL.md
- [ ] Token budget: 400-700 lines (standard), 600-1000 (security/critical)

**The self-recreation test (ULTIMATE GATE):**
Read the generated skill from top to bottom. Ask: "If I fed this skill to a fresh agent with no other skills loaded, could that agent generate a 10/10* skill for any domain?" If the answer is no, identify which Phase's instructions are incomplete and return to that Phase.

**Output:** A validated, chain-connected, production-quality SKILL.md file ready for agent consumption.
