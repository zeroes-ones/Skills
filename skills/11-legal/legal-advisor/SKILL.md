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

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Open Source License Selection
```
                     ┌──────────────────────────┐
                     │ START: Which open-source   │
                     │ license?                   │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Want to require derivative  │
                    │ works to also be open       │
                    │ source (copyleft)?          │
                    └────┬──────────────────┬───┘
                         │ YES              │ NO
                    ┌────▼──────┐    ┌──────▼──────────┐
                    │ Strong    │    │ Want to prevent   │
                    │ copyleft  │    │ others from       │
                    │ or weak?  │    │ using your name   │
                    └──┬───┬────┘    │ in promotion?     │
                       │   │        └──┬──────────┬────┘
                  ┌────▼┐ ┌▼────────┐  │YES       │NO
                  │GPL  │ │Weak:    │ ┌▼──────┐ ┌──▼──────────┐
                  │v3.0 │ │MPL 2.0  │ │MIT +  │ │Completely   │
                  │(most│ │(file-   │ │Apache │ │unrestricted:│
                  │restrictive)│ │level)  │ │2.0    │ │CC0 / Public │
                  └─────┘ │LGPL     │ │(patent│ │Domain        │
                           │(library)│ │grant) │ └──────────────┘
                           └─────────┘ └───────┘
```
**When to choose GPL v3:** Want maximum copyleft — anyone distributing modified versions must also release source under GPL. Strongest community enforcement.
**When to choose MPL 2.0/LGPL:** Weak copyleft — file-level (MPL) or library-level (LGPL). Allows linking from proprietary code while keeping your library open.
**When to choose MIT/Apache 2.0:** Permissive — MIT is simplest (no patent grant), Apache 2.0 adds explicit patent grant and contributor protection. Both allow proprietary use.
**When to choose CC0:** Abandon copyright entirely — public domain dedication. Use for documentation, reference implementations, or when you truly don't care.

### SaaS Agreement Risk Triage
```
                     ┌──────────────────────────────┐
                     │ START: Reviewing contract —    │
                     │ what risk level?               │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Annual contract value < $5K?   │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Low risk:     │    │ ACV > $50K OR    │
                    │ Accept        │    │ involves DPA,    │
                    │ standard terms│    │ HIPAA BAA, or    │
                    │ unless glaring│    │ custom IP terms? │
                    │ red flag      │    └──┬──────────┬────┘
                    └───────────────┘       │YES       │NO
                                       ┌────▼────┐ ┌──▼──────────┐
                                       │High Risk│ │Medium Risk: │
                                       │Engage   │ │Negotiate    │
                                       │External │ │key terms:   │
                                       │Counsel  │ │liability cap│
                                       │for every│ │IP ownership,│
                                       │redline  │ │indemnity    │
                                       └─────────┘ └─────────────┘
```
**When to accept standard terms:** Low ACV ($0-5K), no data processing obligations, no custom IP — accept vendor paper with minimal redlines (cap at fees paid, no indemnity).
**When to negotiate key terms:** Medium ACV ($5-50K) — negotiate liability cap (2× fees), clarify IP ownership of deliverables, mutual confidentiality, and termination for convenience.
**When to engage external counsel:** High ACV (>$50K), DPAs (GDPR), BAAs (HIPAA), custom software development, IP transfer — specialized counsel, full redline, board visibility.

### Trademark Protection Strategy
```
                     ┌──────────────────────────────┐
                     │ START: Trademark strategy?     │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Operating in US only vs         │
                    │ multiple countries?             │
                    └────┬──────────────────────┬───┘
                         │ US only             │ Multi-country
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ USPTO §1(a)   │    │ Revenue >$100K  │
                    │ (use-based)   │    │ in target       │
                    │ if product in │    │ country?        │
                    │ commerce.     │    └──┬──────────┬────┘
                    │ §1(b) (intent-│       │YES      │NO
                    │ to-use) if    │  ┌────▼────┐ ┌─▼──────────┐
                    │ pre-launch.   │  │Madrid   │ │File in key │
                    └───────────────┘  │Protocol:│ │markets only│
                                       │WIPO base│ │(US + top 3)│
                                       │+designate│ │nationally  │
                                       │countries │ └────────────┘
                                       └──────────┘
```
**When to file use-based US:** Product already in commerce — §1(a) filing with specimen of use, faster to registration, lower cost ($250-350/class).
**When to file intent-to-use US:** Pre-launch, want priority date now — §1(b) filing, reserves priority, but must prove use later (Statement of Use).
**When to use Madrid Protocol:** 3+ countries needed — file WIPO application based on home registration, designate member countries, single renewal, cheaper than individual national filings.
**When to file nationally:** Only 1-2 key markets — direct national filing may be faster and cheaper than Madrid route with fewer designated countries.

### IP Assignment vs License Decision
```
                     ┌──────────────────────────────┐
                     │ START: Contractor/employee     │
                     │ creates IP — how to secure?    │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Work done by employee within    │
                    │ scope of employment?            │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO (contractor)
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Work-for-hire│    │ Contractor using  │
                    │ doctrine     │    │ their own tools,  │
                    │ applies (US) │    │ no supervision?   │
                    │ — IP auto-   │    └──┬──────────┬────┘
                    │ owned by     │       │YES       │NO
                    │ employer.    │  ┌────▼────┐ ┌──▼──────────┐
                    │ Still get    │  │IP       │ │May qualify  │
                    │ signed       │  │Assign-  │ │as work-for- │
                    │ agreement    │  │ment +   │ │hire — but   │
                    │ confirming.  │  │Moral    │ │get assignment│
                    └──────────────┘  │Rights   │ │for certainty │
                                      │Waiver   │ └──────────────┘
                                      └─────────┘
```
**When work-for-hire applies:** US employee creating within scope — automatic IP ownership to employer. Still get written confirmation for audit trail and investors.
**When IP assignment needed:** Contractor or non-US contributor — signed agreement with "present assignment of future rights" language + moral rights waiver where applicable.
**When to use license instead:** Third-party contribution to your open source project — CLA with license grant (not assignment) may be sufficient for project stewardship.

### DMCA Safe Harbor Eligibility
```
                     ┌──────────────────────────────┐
                     │ START: Need DMCA safe harbor?  │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Do you host user-generated      │
                    │ content (comments, uploads,     │
                    │ repos, listings)?               │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Must register │    │DMCA safe harbor  │
                    │ DMCA agent    │    │not applicable.   │
                    │ with USCO     │    │Still need:       │
                    │ ($6 fee).     │    │respond to notices│
                    │ Implement:    │    │as matter of risk │
                    │ - Notice-and- │    │management.       │
                    │   takedown    │    └─────────────────┘
                    │ - Counter-notice│
                    │ - Repeat      │
                    │   infringer   │
                    │   policy      │
                    │ - No knowledge│
                    │   of infring. │
                    └───────────────┘
```
**When DMCA safe harbor needed:** Any platform hosting user-submitted content (comments, repos, uploads) — registration is $6, but failure to implement = full liability for user infringement.
**When not needed:** No UGC, only your own content — still respond to takedown notices as a matter of risk management but safe harbor unavailable.
**Key requirements:** Designated agent registered at copyright.gov, expeditious takedown, counter-notice process, repeat infringer termination policy, no actual knowledge of infringement.

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

> When legal advisory is applied perfectly, contracts are negotiated with precision using playbook-driven redlines that close in days not weeks, open source licenses are cataloged with zero copyleft surprises in shipping code, IP portfolios are strategically filed to create durable competitive moats, every partnership agreement protects the company's core assets while enabling commercial velocity, and the legal function is seen by the business as an enabler, not a gatekeeper.

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

