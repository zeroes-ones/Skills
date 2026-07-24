---
name: legal-advisor
description: >
  Use when drafting SaaS agreements, reviewing contracts, developing IP protection
  strategy, evaluating open-source license compliance, structuring fundraising term
  sheets, or generating terms of service and privacy policies. Handles contract review
  frameworks, corporate structure guidance, IP strategy (patent, trademark, copyright,
  trade secret), open-source license compliance, fundraising term sheets (SAFE,
  convertible note, Series Seed), and employment classification. Do NOT use for
  regulatory compliance (FDA, HIPAA), privacy law implementation, or security
  engineering.
license: MIT
allowed-tools: Read Grep Glob
tags:
- legal
- contracts
- ip
- open-source
- fundraising
- saas
- terms
- privacy-policy
author: Sandeep Kumar Penchala
type: legal
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
  - accessibility-auditor
  - ai-safety-health-reviewer
  - board-manager
  - health-regulatory-submission
  - hipaa-technical-implementation
  - privacy-engineer
  feeds_into:
  - accountant
  - bizdev-manager
  - board-manager
  - ceo-strategist
  - compliance-officer
  - content-policy-manager
  - crisis-response-manager
  - gdpr-privacy
  - health-regulatory-submission
  - hipaa-technical-implementation
  - hr-manager
  - investor-relations
  - medical-content-reviewer
  - partnerships-manager
  - people-ops
  - regulatory-specialist
  - treasury-manager
---

# Legal Advisor
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Comprehensive legal advisory framework for software and SaaS businesses. Covers document drafting, intellectual property strategy, open-source compliance, and risk assessment — designed to be used alongside qualified legal counsel, not as a replacement.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "We're just friends — we don't need a written co-founder agreement." | 18 months later, one founder leaves and disputes equity, IP ownership, and responsibilities. With zero written documentation, you have he-said/she-said with no enforceable terms. Cost: $50K-$500K in legal fees litigating what was "agreed" over coffee versus what's provable in court. Every agreement must be in writing before money moves or code ships. |
| "We'll copy Stripe's ToS — they're in our space, they know what they're doing." | Stripe's ToS includes PCI-DSS obligations, financial services disclaimers, and jurisdiction-specific clauses that don't apply to your SaaS analytics tool. When a dispute arises, half the clauses are unenforceable, and the ones you actually need are missing. Cost: $25K-$250K in legal remediation, plus exposure from invalid provisions during the gap. |
| "The contractor built it, we paid them — we own the code." | Under US copyright law, the contractor owns the code they wrote until they explicitly assign it in writing. No IP assignment clause in the contract = the contractor can demand additional payment, block your Series A, or license the same code to your competitor. Cost: $100K-$1M to negotiate retroactive assignment or rewrite disputed modules from scratch. |
| "We'll classify workers as 1099 contractors — it saves 30% on payroll taxes." | The IRS 20-factor test and state ABC tests don't care what the contract says. If you set hours, provide equipment, and the role is core to your business, they are employees. Penalties include back overtime, back payroll taxes, unpaid benefits, and civil penalties — per worker, going back 3 years. Cost: $100K-$1M+ in back taxes, penalties, and class-action exposure. |
| "A verbal handshake is fine for now — we'll paper it later." | There is no such thing as a verbal contract that survives a dispute. 100% of "we had an understanding" cases devolve into contested recollections with zero documentary evidence. The party with the better lawyer wins, not the party who was right. Every deal, every partnership, every equity split — write it down, sign it, date it. Before the conflict, not after. |

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to produce legal advice without disclaimer.** Everything here is educational — the user must consult a qualified attorney for their specific situation | Trigger: response contains legal conclusion, contract language, or regulatory interpretation without visible disclaimer: "This is a draft template, not legal advice. Review with qualified counsel before use." | STOP. Prepend to response: "⚠️ This is educational information, not legal advice. Laws vary by jurisdiction and depend on specific facts. Consult a qualified attorney for your situation. Any generated document language is a draft template — review with counsel before use." |
| **R2** | **REFUSE to cite specific statutes without verification marker.** Laws, regulations, and interpretations change — stale citations create false confidence | Trigger: response mentions specific statute (e.g., "GDPR Art. 17," "CCPA §1798.100," "15 U.S.C. §") without appending verification notice | STOP. Append: "Verify this section is current — it may have been amended or reinterpreted since this was written. Check official sources for the most recent text." |
| **R3** | **REFUSE to answer without flagging jurisdiction dependencies.** Most legal answers depend on WHERE — US federal, California, EU, China, etc. have fundamentally different rules | Trigger: response provides legal guidance but `grep -c "jurisdiction\|assumes.*law\|under.*law\|this answer assumes"` < 1 | STOP. Prefix: "This answer assumes [JURISDICTION]. If your situation involves users/entities in other jurisdictions (EU, California, China, etc.), different rules apply. Confirm your applicable legal regime before relying on this analysis." |
| **R4** | **REFUSE to draft without warnings for high-risk provisions.** Unlimited liability, uncapped indemnification, and IP assignment without consideration can bankrupt a company | Trigger: response generates contract language containing "unlimited liability\|uncapped\|indemnify.*all\|assign.*all.*IP\|no.limitation.of.liability" without accompanying risk flag | STOP. Flag: "⚠️ This provision contains high-risk terms that could expose the company to uncapped liability or loss of core IP. These clauses should not be accepted without board-level approval and external counsel review." |
| **R5** | **STOP and ASK when the user describes a situation requiring "consult an attorney" over confident guidance.** Prefer professional legal review when two reasonable interpretations exist | Trigger: request involves litigation, regulatory investigation, criminal allegation, whistleblower complaint, or M&A due diligence | STOP. Respond: "This situation involves [litigation/regulatory/criminal/M&A] implications that require privileged legal advice from a qualified attorney. I can explain general legal concepts and frameworks, but specific legal strategy in this context must come from your counsel. May I proceed with the educational overview?" |
| **R6** | **DETECT and WARN about copyleft license contamination in proprietary code.** GPL/AGPL in proprietary codebase = dealbreaker for acquisition and potential forced open-sourcing | Trigger: `grep -rn "GPL\|AGPL\|EUPL\|LGPL\|copyleft" package.json go.mod Cargo.toml requirements.txt` returns matches in a proprietary codebase | WARN: "Copyleft licenses (GPL/AGPL/EUPL) detected in proprietary codebase. This can: (1) force source disclosure obligations, (2) block acquisition/funding due diligence, (3) create legal liability. Isolate behind API boundary or replace with MIT/Apache 2.0 alternatives immediately." |
| **R7** | **DETECT and WARN about missing IP assignment from contractors/founders.** Without signed IP assignment, the contractor owns what they built — this is the #1 deal-killer in M&A due diligence | Trigger: user describes code contributed by contractors, founders, or external contributors, but `grep -rn "IP.assignment\|work.for.hire\|invention.assignment" contracts/ employment/` returns no matching signed agreements | WARN: "Without signed IP assignment agreements, the individuals who contributed code may still own their work. This is the #1 deal-killer in M&A and funding due diligence. Audit every contributor and get signed assignments before pursuing fundraising or acquisition. A single unsigned contractor who contributed 20% of the codebase can kill a deal." |

## The Expert's Mindset

Master legal advisors understand that strategy is not about predicting the future — it's about **being less wrong than the competition, faster**.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Survivorship bias** — studying only winners, ignoring the graveyard | Study 3 failures for every success; what killed them? |
| **Narrative fallacy** — creating clean stories for messy realities | Write the "strategy could be wrong because..." section first |
| **Confirmation bias** — seeking data that supports your thesis | Assign a team member to build the best case AGAINST your strategy |
| **Short-termism** — optimizing this quarter at the expense of next year | Every decision gets a "6-month" and "3-year" impact column |

### What Masters Know That Others Don't
- **The bottleneck is always one thing.** Find it. Fix it. Then find the next one.
- **Strategy = what you say NO to.** If your strategy doesn't exclude anything, it's not a strategy.
- **Timing beats brilliance.** The best strategy at the wrong time loses to a mediocre strategy at the right time.

### When to Break Your Own Rules
- **Bet the company when the asymmetry is right.** If downside = $1M and upside = $1B, the math doesn't care about your process.
- **Ignore the data when you're creating a new category.** By definition, there's no data for something that doesn't exist yet.

## Route the Request

<!-- Machine-executable routing: 8 file_contains/file_exists rows A1-A8 + Intent Route fallback -->

| # | Detect Condition | Route To | Intent Route Fallback |
|---|-----------------|----------|----------------------|
| **A1** | `file_contains("contracts/*.pdf", "MSA\|master.service\|vendor.agreement\|NDA\|SOW")` or `file_exists("contracts/review-queue/")` | Sub-Skills → Contract Review & Drafting | "I detect contract documents — routing to Contract Review & Drafting workflow." |
| **A2** | `file_contains("package.json", "GPL\|AGPL\|LGPL")` or `file_exists("LICENSES/")` | Sub-Skills → Open Source License Compliance | "I detect copyleft licenses (GPL/AGPL/LGPL) — routing to Open Source License Compliance." |
| **A3** | `file_exists("trademarks/")` or `file_contains("README.md", "trademark\|patent.pending\|patent.filed")` | Sub-Skills → IP Portfolio Management | "I detect trademark/patent assets — routing to IP Portfolio Management." |
| **A4** | `file_contains("*.html\|*.tsx\|*.jsx", "clickwrap\|checkbox.*accept")` and `file_contains("*.md", "terms.of.service\|privacy.policy\|EULA")` | Sub-Skills → SaaS Legal Foundations | "I detect clickwrap acceptance patterns with legal docs — routing to SaaS Legal Foundations." |
| **A5** | `file_contains("*.md\|*.pdf", "SAFE\|convertible.note\|Series.Seed\|term.sheet\|fundraising")` | Sub-Skills → Funding & M&A Legal Prep | "I detect fundraising/investment documents — routing to Funding & M&A Legal Prep." |
| **A6** | `file_contains("contracts/", "employment\|contractor\|offer.letter\|equity.grant")` or `file_exists("hr/contracts/")` | Sub-Skills → Contract Review (employment focus) | "I detect employment/contractor agreements — routing to Contract Review for employment matters." |
| **A7** | `file_contains("contracts/", "DPA\|data.processing\|SCC\|standard.contractual")` | Sub-Skills → Data Processing Agreements | "I detect DPA/SCC infrastructure — routing to Data Processing Agreements workflow." |
| **A8** | `file_exists("SECURITY.md")` or `file_contains("README.md", "license\|legal\|compliance\|attorney")` | Core Workflow → Phase 1 | "I detect legal documentation — this is the legal-advisor skill domain. Routing to Core Workflow Phase 1." |

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Initiative | Execute a defined strategic initiative with clear metrics |
| **L2** | Product line / function | Define strategy for a product line; own outcomes |
| **L3** | Business unit | Set multi-year strategy for a business unit; allocate resources across competing priorities |
| **L4** | Company | Define company-wide strategy; make existential trade-off decisions |
| **L5** | Industry | Shape industry dynamics; create new market categories |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 legal advisor, develop..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Drafting or updating Terms of Service (ToS), Privacy Policy, or End User License Agreement (EULA) for a SaaS product
- Evaluating open-source license compatibility when incorporating third-party libraries into proprietary software
- Setting up a DMCA compliance process (notice-and-takedown, counter-notice, repeat infringer policy)
- Establishing an IP protection strategy: patents, trademarks, copyrights, trade secrets
- Reviewing vendor contracts or partnership agreements for liability, indemnification, and IP ownership clauses
- Conducting an open-source license audit of the codebase ahead of fundraising, acquisition, or IPO
- Crafting a trademark registration and enforcement strategy
- Building a contributor license agreement (CLA) or developer certificate of origin (DCO) process

## Decision Trees

Key decision paths (full trees in [references/decision-trees.md](references/decision-trees.md)):

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Open Source License Selection

```
                     ┌──────────────────────────┐... [See full decision trees →](references/decision-trees.md)

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Document Inventory & Gap Analysis

1. **Legal Document Audit** — Inventory all existing legal documents: ToS, Privacy Policy, EULA, DPA (Data Processing Agreement), Cookie Policy, Acceptable Use Policy, Refund Policy, Service Level Agreement, MSAs with enterprise customers.
2. **Regulatory Gap Analysis** — Map applicable regulations to existing compliance: GDPR (EU users), CCPA/CPRA (California residents), PIPEDA (Canada), LGPD (Brazil), DMA/DSA (EU platforms), COPPA (children under 13), CalOPPA (California online privacy). Flag each as compliant, partially compliant, or non-compliant.
3. **Jurisdiction Mapping** — Identify where the company operates, where data is stored/processed, and which jurisdictions' laws apply. This drives governing law selection and dispute resolution clauses.
4. **Deliverable: Legal Audit Report** — Prioritized matrix of missing or outdated documents, compliance gaps, and recommended remediation timeline.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Document Drafting & Review

1. **Terms of Service** — Key clauses to include:
   - **Acceptance of terms**: explicit consent mechanism (clickwrap, not browsewrap).
   - **Account responsibilities**: user's obligation to secure credentials, liability for account activity.
   - **Acceptable use**: prohibited activities (illegal content, reverse engineering, scraping, spamming).
   - **Intellectual property**: clarify who owns what — customer owns their data, company owns the platform.
   - **Payment terms**: subscription billing, auto-renewal, refunds, taxes.
   - **Termination**: grounds for termination, effect on data (export window before deletion).
   - **Disclaimers & limitations of liability**: "as-is" disclaimer, liability cap (e.g., fees paid in last 12 months).
   - **Indemnification**: mutual or one-way, scope, procedure.
   - **Dispute resolution**: governing law, venue, arbitration clause (opt-out provision for consumers), class action waiver.
   - **Changes to terms**: notice period, user's right to reject by discontinuing use.
2. **Privacy Policy** — Must cover (per GDPR/CCPA template):
   - Categories of personal data collected (with examples)
   - Purposes and legal bases for processing
   - Third-party data sharing and categories of recipients
   - Cross-border data transfer mechanisms (SCCs, DPF)
   - Data retention periods per category
   - User rights: access, rectification, erasure, portability, objection, automated decision-making
   - Cookie and tracking technology disclosures
   - Children's privacy (COPPA)
   - Contact information for DPO or privacy inquiries
   - Effective date and change notification process
3. **EULA** — For installed/distributed software:
   - License grant: scope (perpetual, subscription), restrictions, permitted copies.
   - Updates and maintenance: auto-update permission, end-of-life policy.
   - Data collection: telemetry, crash reporting, usage analytics.
   - Third-party components: open-source attribution and license notices.
   - Source code escrow (enterprise deals).
4. **Contract Review Framework** — Standardized checklist for reviewing third-party agreements:
   - **IP ownership**: who owns deliverables, work product, and pre-existing IP.
   - **Confidentiality**: definition of confidential info, exceptions, term, post-termination obligations.
   - **Indemnification**: scope (IP infringement, bodily injury, data breach), caps, exclusions.
   - **Limitation of liability**: carve-outs (gross negligence, willful misconduct, breach of confidentiality, IP infringement).
   - **Termination**: for convenience, for cause, cure period, effect (transition assistance, data return).
   - **Data processing**: if vendor processes personal data, require DPA with SCCs if cross-border.
   - **Insurance**: require minimum coverage (CGL, E&O, cyber) and certificate of insurance.
   - **Assignment**: change of control clause, no assignment without consent.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): IP & Open-Source Strategy

1. **Patent Strategy** — Decide: defensive (build portfolio to deter lawsuits), offensive (assert against competitors), or none (rely on trade secrets and speed). File provisionals to establish priority date. Conduct freedom-to-operate searches before major product launches.
2. **Trademark Strategy** — File for name, logo, and tagline in key classes (9 for software, 42 for SaaS). Conduct clearance search before adopting any brand element. Monitor for infringement (watch service). Enforce consistently — failure to police can weaken mark. Use ® for registered, ™ for unregistered.
3. **Open-Source License Audit** — Run `license-checker` or FOSSA across the entire dependency tree. Categorize licenses:
   - **Permissive** (MIT, Apache 2.0, BSD): safe for proprietary use with attribution.
   - **Weak copyleft** (LGPL, MPL): okay in library/linking context; may require sharing modifications to the library itself.
   - **Strong copyleft** (GPL, AGPL, SSPL): avoid in proprietary core unless legal reviews and isolates as a separate process. AGPL is particularly risky for SaaS — triggers if users interact with the code remotely.
   - **Source-available / non-commercial** (BSL, Elastic License, CC BY-NC): read the specific terms — some prohibit competitive use.
4. **Contributor License Management** — For open-source projects: DCO (lighter, trust-based, sign-off-by in commits) vs. CLA (formal, signed agreement assigning or licensing rights to the project). CLA needed if you plan to relicense or offer commercial licenses later.
5. **Trade Secret Protection** — Identify trade secrets: algorithms, training data, pricing models, customer lists. Implement reasonable measures: access controls, NDAs with employees and contractors, document labeling, exit interview procedures, non-compete/non-solicit where enforceable.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->
Legal advice touches every function. Missed coordination creates liability; over-lawyering blocks velocity. Balance is structural.

### Decision Gates & Artifacts

| Decision Gate | Trigger | Artifact / Deliverable |
|---------------|---------|------------------------|
| Contract liability cap acceptable | Vendor/partner agreement with liability clause >2x ACV | Risk assessment memo + board approval if material |
| Open-source license compatible | New third-party dependency with copyleft license (GPL, AGPL) | License compatibility matrix + legal sign-off before integration |
| IP assignment verified | New hire, contractor, or acquisition | Signed IP assignment agreement + chain-of-title documentation |
| Fundraising term sheet reviewed | SAFE, convertible note, or Series Seed offer received | Term sheet redline + cap table impact analysis |
| Trademark cleared | New product/brand name proposed | Trademark clearance search + availability opinion |
| DMCA process triggered | Takedown notice or counter-notice received | Takedown/counter-notice within statutory deadline + repeat infringer policy check |
| Corporate structure decision made | New entity, subsidiary, or international expansion | Entity formation documents + tax/liability analysis |

### Route to Other Skills

| Request Pattern | Route To | Why |
|-----------------|----------|-----|
| DPA, privacy policy, or cookie consent drafting | `gdpr-privacy` | Specialized privacy compliance knowledge beyond general legal |
| FDA, HIPAA, or medical device regulation | `regulatory-specialist` | Industry-specific regulatory frameworks for healthcare/life sciences |
| Fundraising strategy, M&A, board governance | `ceo-strategist` | Business-level deal strategy, cap table, and fiduciary duty |
| General regulatory filing, audit prep, compliance programs | `compliance-officer` | Cross-domain regulatory compliance program management |
| Content moderation, platform policy, user-generated content rules | `content-policy-manager` | Platform-specific content governance and moderation frameworks |
| Business development deals, partnership structuring | `bizdev-manager` | Commercial terms, partnership economics, go-to-market strategy |

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **CEO Strategist** | Fundraising, M&A, IP strategy, major contracts | Deal terms, cap table implications, fiduciary duties, risk appetite |
| **CTO Advisor** | Open-source licensing, IP assignment, tech transactions | License compatibility matrix, contributor agreements, technology due diligence |
| **GDPR/Privacy Specialist** | Privacy policies, data processing agreements, breach response | Data processing purposes, consent mechanisms, cross-border transfer assessments |
| **Regulatory Specialist** | FDA, HIPAA, financial services compliance | Industry-specific regulatory frameworks, audit readiness |
| **Product Strategist** | Terms of Service, feature launches, pricing changes | Feature legal review, ToS updates, consumer protection requirements |
| **Security Reviewer** | Data breaches, security incidents, vulnerability disclosure | Breach notification obligations, regulatory reporting timelines, disclosure policies |
| **Growth Engineer** | A/B testing terms, referral programs, sweepstakes | Promotional law compliance, contest rules, marketing claims substantiation |
| **Project Manager** | Contract review cycles, legal hold notices, litigation | Legal review SLAs, resource allocation for legal workstreams |
| **HR/People Ops** | Employment agreements, contractor classification, equity grants | Offer letter templates, IP assignment clauses, worker classification tests |
| **All Engineering Teams** | Open-source compliance, 3rd-party library licensing | License approval process, attribution requirements, copyleft triggers |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| New open-source dependency with copyleft license (GPL, AGPL) | CTO Advisor, Engineering Lead | Copyleft can force source disclosure; evaluate alternatives before integration |
| DMCA takedown notice received | CTO Advisor, Security Reviewer, Content Team | 24-72 hour response window; content removal and counter-notice process |
| Data breach or suspected breach | GDPR/Privacy Specialist, Security Reviewer, CEO Strategist | 72-hour regulatory notification clock starts; parallel breach investigation |
| Third-party IP claim or cease-and-desist letter received | CEO Strategist, Product Strategist | Litigation risk; product changes may be required |
| New product feature collecting sensitive data (health, financial, minors) | GDPR/Privacy Specialist, Regulatory Specialist, Product Strategist | Enhanced regulatory obligations; DPIA may be required |
| Contract with liability cap >2x annual contract value | CEO Strategist, CFO | Enterprise risk exposure; board-level decision |
| Employee invention assignment dispute | CTO Advisor, HR | IP ownership at risk; product IP chain of title affected |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Regulatory investigation or subpoena received | **External Counsel** + CEO Strategist | Privileged response required; in-house may not be sufficient |
| Patent infringement claim from competitor | **External IP Litigation Counsel** + CEO Strategist | Specialized litigation; business existential risk |
| Whistleblower complaint (internal) | **Board/Audit Committee** + External Counsel | Governance obligation; independent investigation required |
| Cross-border M&A or IPO preparation | **External Transactional Counsel** + CEO Strategist + CFO | Complex multi-jurisdiction; specialized expertise required |
| Criminal allegation involving employee or company | **External Criminal Defense Counsel** + Board | Personal and corporate liability; privilege critical |

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| User mentions "we're launching in Europe next month" without discussing GDPR readiness | Prompt: "GDPR requires a Data Protection Officer, lawful basis documentation, and a records of processing activities (Art. 30) BEFORE processing EU resident data. Fines are up to 4% of global annual revenue. Want me to run the GDPR-readiness checklist?" | GDPR is not post-launch compliance — it's a pre-launch requirement. Launching without Art. 30 documentation and consent mechanisms creates immediate liability. EU regulators have fined companies within weeks of market entry |
| Developer asks to integrate a GPL-licensed library into the main backend codebase | Flag: "GPL/AGPL is a strong copyleft license — integrating it may require you to open-source your entire backend. Consider: (1) Is there an MIT/Apache alternative? (2) Can this run as a separate service behind an API boundary? Let me audit all current dependencies for copyleft triggers" | One GPL dependency integrated into proprietary code can create an enforceable obligation to release the entire codebase. This is how many startups discover they've accidentally open-sourced their core IP during due diligence |
| User describes "we don't have a privacy policy yet, we'll add one before launch" | Intervene: "Privacy policy must be published BEFORE you collect any user data — not at launch. Under GDPR, CCPA, and similar laws, you need to disclose what data you collect, why, and how long you keep it at the point of collection. A retroactive privacy policy is legally meaningless and creates ongoing exposure" | Pre-collection disclosure is a universal requirement across privacy regulations. A privacy policy posted after data collection began does not cure the original violation. This creates liability for every user whose data was collected without notice |
| Co-founder asks to use personal funds for company expenses without proper documentation | Alert: "Commingling personal and business funds pierces the corporate veil — eliminating limited liability protection. Every company expense must go through a business bank account with clear documentation. This is how founders lose personal asset protection in litigation. Set up a business account and expense policy now" | Commingling is the #1 way courts pierce the corporate veil. Once pierced, founders are personally liable for all company debts and judgments. This applies to LLCs and corporations equally — the protection is conditional on separation of finances |
| Product team describes collecting health data or children's data without special handling | Escalate: "Health data (HIPAA) and children's data (COPPA, GDPR Art. 8) trigger additional regulatory frameworks with mandatory requirements. This is not general privacy — these are regulated data categories with per-violation fines. The product design must include age verification, parental consent flows, and data segregation BEFORE implementation" | Regulated data categories impose obligations that general privacy laws don't — mandatory breach notification timelines (HIPAA: 60 days), verifiable parental consent (COPPA), data minimization requirements. Designing the product without these constraints means expensive redesign or regulatory action |
| Developer proposes an "accept terms on signup" flow without version tracking or change notification | Warn: "Terms of service need: (1) version tracking with effective dates, (2) user re-consent for material changes, (3) archived versions accessible to users, (4) audit trail of who accepted which version and when. A simple checkbox without versioning means you can't prove a user agreed to the current terms in a dispute" | Without versioned acceptance records, you cannot enforce arbitration clauses, liability limitations, or class action waivers against users who signed up under old terms. Courts require proof that the specific user agreed to the specific version being enforced |
| User mentions "we'll just use the same contract template for all our enterprise customers" without customization | Flag: "Enterprise contracts need per-customer negotiation on: liability caps, SLA commitments, data processing terms, termination rights, and IP ownership of custom work. A one-size template either gives away too much (low liability cap for a $500K deal) or is too aggressive (no SLA for a mission-critical deployment). Each enterprise deal needs legal review of these 5 key terms" | Enterprise contract standardization saves time but creates risk at both ends. Underselling liability caps loses money; overselling SLAs creates unbounded operational liability. The gap between a $5K and $500K contract should be reflected in the legal terms |
| Team discusses an acquisition or funding round without having done IP assignment cleanup | Intervene immediately: "Due diligence will require: (1) signed IP assignment agreements from every founder, employee, and contractor who ever contributed code, (2) open-source license audit (SBOM), (3) trademark registration status, (4) patent filings if any. Missing IP assignments from a former contractor who contributed 20% of the codebase can kill a deal. Start the IP cleanup audit now — it takes months" | IP ownership gaps are the #1 deal-killer in M&A and funding due diligence. A single contractor without a signed IP assignment means the company doesn't own its own product. This is unfixable retroactively without locating and negotiating with the former contractor |

## What Good Looks Like

> When legal advisory is applied perfectly, contracts are negotiated with precision using playbook-driven redlines that close in days not weeks, open source licenses are cataloged with zero copyleft sur

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


## Deliberate Practice

```mermaid
graph LR
    A[Formulate<br/>thesis] --> B[Test in<br/>market] --> C[Study<br/>outcome] --> D[Refine<br/>mental model] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Write a strategy memo for a past business event; compare your reasoning to what actually happened | Monthly |
| **Competent** | Write 3 strategies for the same goal with different constraints; debate which wins | Quarterly |
| **Expert** | Reverse-engineer a competitor's strategy from public information; validate against their next move | Quarterly |
| **Master** | Board-level strategy for a company in a different industry; present to a peer CEO for feedback | Semi-annually |

**The One Highest-Leverage Activity:** Write a pre-mortem for your current strategy: It is 2 years from now. Our strategy failed. Why?

## Anti-Patterns

- **"I am not a lawyer, but..."** followed by legal advice — this disclaimer doesn't protect the company from unauthorized practice of law claims AND doesn't protect the recipient from relying on non-lawyer legal opinions. If you're not a barred attorney in the relevant jurisdiction, don't give legal conclusions. Give risk assessments and options, not legal opinions.
- **Accepting the other party's contract without redlines** — their contract was written by their lawyers to protect them, not you. Every clause favors them by default. A contract that arrives "pre-approved" is a negotiation opening, not a final document. Always redline.
- **"We'll sort out the legal details later"** — the deal closes, the relationship sours, and there's no written agreement on IP ownership, payment terms, termination rights, or dispute resolution. The "legal details" are now a lawsuit that costs 10x what the deal was worth.
- **Using a template contract for a fundamentally different deal** — your SaaS subscription agreement used for a custom development project. It doesn't cover: IP assignment (who owns the custom code?), acceptance criteria, milestone payments, or warranty on deliverables. Templates are starting points, not universal contracts.
- **Signing personally instead of as an authorized representative of the company** — "John Smith" instead of "John Smith, CEO, on behalf of Acme Corp." The contract now binds John Smith personally. If the company can't pay, John's personal assets are at risk.

## Error Decoder

- **"This clause is 'standard' or 'boilerplate'" from opposing counsel** → "Standard" means "we put this in every contract and hope you don't push back." Every clause is negotiable. "Boilerplate" clauses that matter: governing law, venue, indemnification, limitation of liability, termination, and assignment. These are never truly boilerplate.
- **"We need this signed by EOD"** → Artificial urgency is a negotiation tactic. If they really need it signed today, they should have sent it last week. Rushing legal review means you'll miss: auto-renewal clauses, uncapped liability, one-sided indemnification, and IP assignment traps.
- **NDA that defines "Confidential Information" as "all information disclosed"** → Including publicly available information, information you already knew, and information you independently developed. The NDA now restricts you from using information you already owned. Always add exclusions: publicly known, previously known, independently developed, rightfully received from third party.
- **Indemnification: "Each party indemnifies the other" (mutual)** → Sounds fair but isn't. If your product causes their data loss, you indemnify them (fair: it's your product). If they use your product to violate GDPR, they indemnify you (fair: it's their use). Mutual indemnification for DIFFERENT types of liability (IP infringement vs data misuse) is standard. Mutual for the SAME liability means you're paying for their mistakes.

## Production Checklist

- [ ] Contract review: reviewed by a barred attorney in the relevant jurisdiction (not just an AI-assisted review)
- [ ] Key clauses checked: governing law, venue, indemnification, limitation of liability, IP ownership, termination, auto-renewal
- [ ] Signing authority: signatory has documented authority to bind the company. Signature block includes title and "on behalf of [Company Name]."
- [ ] Redlines: all changes from the original are tracked (redlines saved). Rationale for each change documented.
- [ ] Open source license audit: all project dependencies have license checks. No GPLv3 in non-GPL projects. CLAs in place for external contributors.
- [ ] Terms of Service: last updated within 12 months. Consistent with privacy policy. Dispute resolution and governing law specified.
- [ ] Document retention: signed contracts stored in a durable, backed-up system with access controls. Retention schedule documented.

## Gotchas

- **Open-source license compatibility** — MIT code in an Apache 2.0 project is compatible (MIT is more permissive). GPLv3 code in an MIT project makes the ENTIRE project GPLv3 (copyleft propagation). Apache 2.0 and GPLv2 are INCOMPATIBLE (patent grant vs termination clauses). License compatibility must be checked at the dependency-graph level, not per-package.
- **Contributor License Agreements (CLAs)** require contributors to sign over rights. But a CLA that says "you grant us an irrevocable, perpetual, worldwide license" without specifying what "us" can do — the contributor's employer may claim the code was created on company time. CLAs must include IP ownership attestation: "I certify this is my original work and not owned by my employer."
- **Terms of Service "governing law" clause** — choosing Delaware because it's "business-friendly" applies Delaware law to a dispute between a French user and your UK entity. EU consumer protection laws (which can't be waived by contract) may override, creating a situation where no one knows which law applies. Consider local incorporation for major markets.
- **Data residency vs data sovereignty** — your data is stored in Frankfurt (residency), but your parent company in the US can access it under the CLOUD Act (sovereignty). EU customers demand sovereignty (data can't leave the EU under any legal order), not just residency. Separate legal entity + data trustee required for true sovereignty.
- **Indemnification clauses** in enterprise contracts — "Customer indemnifies Vendor against all third-party claims arising from Customer's use of the service." A third party sues YOU for something YOUR customer did with your software — and the customer pays your legal bills. But if YOUR software was the CAUSE (e.g., security vulnerability), customer indemnification doesn't apply. Mutual indemnification for IP infringement is standard; unilateral for customer conduct.
- **Handshake deals without written contracts.** Two founders agree on equity split, responsibilities, and IP ownership over coffee — 18 months later, one leaves and disputes everything because nothing was memorialized. Even among friends, verbal agreements devolve into "he said/she said" with zero enforceable terms. **Total cost: $50K-$500K in legal fees litigating what was "agreed" versus what's provable, plus equity dilution and startup paralysis.** Every agreement — even between co-founders — must be reduced to writing with signatures before any money changes hands or code is written.
- **Copying a competitor's Terms of Service verbatim.** A startup copies Stripe's ToS because "they're in the same space" — but Stripe's ToS includes PCI-DSS obligations, financial services disclaimers, and jurisdiction-specific clauses that don't apply to a SaaS analytics tool. When a dispute arises, half the clauses are unenforceable and the ones that matter are missing. **Total cost: $25K-$250K in legal remediation to rewrite the ToS, plus exposure from unenforceable provisions during the gap period.** Terms of Service must be drafted for YOUR business model, YOUR data flows, and YOUR jurisdiction — templates from competitors are starting points at best, never final documents.
- **Missing IP assignment clauses in contractor agreements.** You hire a freelance developer who builds your core feature, but the contract only says "develop X feature for $Y" with no IP assignment language — under US copyright law, the contractor owns the code they wrote until they explicitly assign it. When you raise a Series A, the investor's IP audit discovers you don't own your codebase. **Total cost: $100K-$1M to negotiate retroactive IP assignment with contractors who now have leverage, or to rewrite disputed modules from scratch.** Every contractor agreement must include a present-tense IP assignment clause: "Contractor hereby assigns all right, title, and interest in any work product created under this agreement to the Company."

- **Using equity as a substitute for market-rate cash compensation.** Early-stage startups offer 30-50% below-market salary in exchange for 0.5-2% equity — but with standard 4-year vesting and a 1-year cliff, employees terminated or departing before the 12-month mark walk away with zero equity and below-market wages. Disgruntled ex-employees with neither cash nor equity file wage-and-hour claims, triggering Department of Labor audits that examine every employee's classification and pay history. **Total cost: $50K-$500K in back-pay settlements (often 2-3x the wage differential), DOL penalties, legal defense fees, and talent-market reputation damage when a single lawsuit cascades into multiple claims. One misclassified-employee lawsuit at a 15-person startup can consume 6-12 months and the entire legal budget.** Fix: ensure every equity grant is paired with at least minimum wage compliance and preferably 70%+ of market salary for the role. Document the equity-for-cash trade explicitly in offer letters with both parties acknowledging the risk in writing. Consult a compensation attorney when designing equity-heavy compensation structures.

- **Classifying workers as independent contractors to avoid employment taxes and benefits.** The IRS 20-factor test and state-level ABC tests (California, Massachusetts, New Jersey) set a high bar — if you set hours, provide equipment, supervise the work, and the role is core to your business, the law considers them employees regardless of what the contract says. Misclassification penalties include back overtime pay, back payroll taxes (employer + employee portions), unpaid benefits, and civil penalties — per worker, going back up to 3 years. **Total cost: $100K-$1M+ in back taxes, penalties, benefits restitution, and class-action exposure. Uber's $100M misclassification settlement is the high-profile example, but small companies with 5-10 misclassified workers face six-figure DOL audit findings that exceed their annual revenue.** Fix: if a worker is full-time, uses your equipment, follows your schedule, performs core business functions, and can't subcontract the work — they are an employee. Use a staffing agency or Employer of Record (EOR) like Deel or Rippling if you need flexible workforce arrangements. Consult an employment attorney before classifying anyone as a 1099 contractor — the legal analysis must happen before the engagement starts, not during an audit.

## Verification

- [ ] License audit: `fossa` or `license-checker` — all dependencies have licenses, no GPLv3 in non-GPL projects
- [ ] CLA/contributor agreement: reviewed within last 12 months, includes IP ownership attestation
- [ ] Terms of Service: last updated date visible, governing law specified, dispute resolution process documented
- [ ] Privacy: privacy policy and ToS are consistent (no "we never share data" in privacy + "we share with affiliates" in ToS)
- [ ] Open source: projects with > 100 stars have contributing guide, code of conduct, and license

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Cost-Effective Decision Table**: See [cost-decisions.md](references/cost-decisions.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **MVP vs Growth vs Scale**: See [mvp-growth-scale.md](references/mvp-growth-scale.md)
- **Scalability Decision Tree**: See [scalability-tree.md](references/scalability-tree.md)
- **Scale Depth**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)
- **Token-Efficient Workflow**: See [token-workflow.md](references/token-workflow.md)
- **When NOT to Use This Skill (Overkill)**: See [when-not-to-use.md](references/when-not-to-use.md)

