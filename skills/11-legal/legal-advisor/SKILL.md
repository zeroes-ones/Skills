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

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- Never copy-paste legal documents from competitors — this creates copyright issues and may not fit your business model.
- Ensure clickwrap (user must click "I agree") rather than browsewrap (passive notice) — courts consistently uphold clickwrap.
- Version all legal documents with effective dates. Archive old versions. Notify users of material changes with at least 30 days notice.
- Segregate open-source components with strong copyleft licenses into separate services communicating via API — this may avoid the "derivative work" trigger.
- Include an open-source attribution page in your product (usually in Settings > Legal) listing all third-party components and their licenses.
- When processing data on behalf of enterprise customers, sign a DPA that incorporates the latest EU Standard Contractual Clauses (SCCs).
- Trademark clearance should happen before finalizing any product name — rebranding is expensive and disrupts SEO.

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Copy-pasting competitor's Terms of Service and changing company name — copyright infringement and their terms may not fit your business model | Draft from industry templates (YC Series Seed, Cooley GO) customized to your data practices, liability model, and jurisdiction. Review with qualified attorney before publishing | `grep -rn "©.*20[0-9][0-9].*[Cc]ompetitor\|all rights reserved.*[Cc]ompetitor" ToS/ privacy-policy/` → finds copied copyright notices. `diff -w your-tos.md competitor-tos.md \| wc -l` → low diff = likely copied | CI check: run `similarity-check.sh` against known competitor ToS — flag if similarity > 30%. Template generator: use Cooley GO / YC templates as starting point, not competitor docs |
| Using browsewrap (passive "by using this site you agree") instead of clickwrap for binding terms — courts routinely strike down browsewrap as unenforceable | Implement explicit clickwrap: user must check a box or click "I Agree" before proceeding. Record timestamp, version, and user identifier for every acceptance | `grep -rn "by.using.this\|continued.use.constitutes\|browsewrap\|implied.consent" ToS/ terms/` → finds browsewrap language. `grep -rn "I.Agree\|checkbox\|clickwrap\|explicit.consent"` → must find clickwrap implementation | Clickwrap validator: `curl -s https://app.example.com/signup \| grep -c "I Agree\|checkbox.*accept\|clickwrap"` → must be ≥ 1. CI: reject ToS without version tracking and `acceptance_method: clickwrap` metadata |
| Treating all open-source licenses as "free to use" without understanding copyleft triggers — GPL/AGPL in backend can force open-sourcing entire codebase | Segregate strong copyleft (GPL, AGPL, EUPL) into separate services behind API boundary. Use FOSSA/Snyk for automated license compliance. Maintain SPDX-compliant SBOM. Understand permissive vs copyleft vs source-available | `npx license-checker --json \| jq '.[] \| select(.licenses \| contains("GPL"))'` → find copyleft deps. `fossa analyze --output json \| jq '.dependencies[] \| select(.license \| test("GPL\|AGPL\|EUPL"))'` → find all instances | CI license gate: `fossa test` blocks non-approved licenses. Pre-merge: if PR adds dependency with copyleft license, require legal sign-off or architecture review for API isolation |
| Collecting user data first, then figuring out privacy policy and consent later — per se illegal under GDPR (fines up to 4% global revenue) and several US state laws | Privacy-by-design: define data collection purpose, legal basis, and retention period BEFORE writing data ingestion code. Implement consent management at project kickoff, not launch-day panic. Pre-collection disclosure is universal requirement | `git log --oneline --diff-filter=A -- "*/analytics*" "*/tracking*" "*/user-data*"` → find data collection start. `git log --oneline -- "privacy-policy*"` → policy must predate collection code. If policy postdates collection → violation | CI gate: if PR adds data collection endpoint or new analytics integration, require privacy-impact check or documented "no user data" assertion before merge. Auto-flag repos with tracking code but no privacy policy |
| Filing trademark application without clearance search — rebranding after cease-and-desist costs $50K-250K in design, domain, SEO, customer confusion | Commission comprehensive clearance search (USPTO TESS + common law + domain + social media) BEFORE finalizing any product name. Budget $500-2K — cheapest insurance you'll buy | Check USPTO TESS for exact and phonetic matches: `curl -s "https://tsdr.uspto.gov/..."`. Check domain availability, social media handles. Document search results in `trademarks/clearance-*.md` | Procurement gate: no product name finalization without `trademarks/clearance-{name}.md` file. CI: validate clearance document exists and includes: (1) USPTO TESS search results, (2) common law search, (3) domain check, (4) social media handle check |
| Signing enterprise contracts without limitation of liability cap — uncapped liability means one data breach could bankrupt the company | Include mutual liability caps tied to contract value (12-24 months of fees) with standard carve-outs for gross negligence, willful misconduct, IP infringement. Never accept uncapped indemnification for third-party claims | `grep -rn "unlimited.liability\|uncapped\|no.limit\|liability.*unlimited" contracts/*.pdf` → flag uncapped provisions. `pdfgrep -i "limitation of liability" contracts/*.pdf \| grep -c "UNLIMITED\|NO CAP"` → flag risky clauses | Contract review checklist CI: reject contracts missing liability cap. Standard playbook: cap = MAX(12 months fees, insurance coverage). Escalate any uncapped liability request to board level |
| Using NDAs as substitute for IP assignment agreements with contractors — NDA prevents disclosure but does NOT transfer ownership | Always use written IP assignment agreement (work-for-hire clause) with every contractor BEFORE work begins. For employees: employment agreements must include present assignment of future inventions. Without this, the contractor owns what they build | `grep -rn "NDA\|non.disclosure\|confidentiality" contracts/contractors/` → count NDAs. `grep -rn "IP.assignment\|work.for.hire\|invention.assignment\|assign.*rights" contracts/contractors/` → must match NDA count | Contractor onboarding gate: require both (1) signed NDA AND (2) signed IP assignment before any access or work begins. CI: `contractor-audit.sh` cross-references contractor list with signed IP assignments → flag gaps immediately |

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

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
Founder reviewing contracts themselves or with free templates. ToS/Privacy Policy from Termly/Iubenda ($0-50). Open source: MIT license default. Trademark: no registration, common law rights only. No DMCA registration. Contracts: clickwrap via checkbox. IP: employee agreements as work-for-hire. No external counsel unless existential risk. Cost: $0-200/month. Overkill: external counsel retainer, patent filings, formal CLAs, multi-jurisdiction trademark.

### Small (2-10 people, 100-10K users)
Fractional general counsel or law firm retainer (5-10 hours/month). Custom-drafted ToS/Privacy Policy ($3-8K). Trademark: USPTO registration for name + logo ($250-350/class). DMCA: registered agent + takedown process. Open source: license audit before funding round. Contractor IP assignments standardized. Cost: $1K-5K/month. Overkill: in-house counsel, patent portfolio, Madrid Protocol trademarks.

### Medium (10-50 people, 10K-1M users)
In-house counsel or dedicated law firm relationship. Full contract management system (Ironclad, LinkSquares). IP portfolio: patents (provisional + PCT), trademarks (USPTO + Madrid), trade secrets program. Open source: automated license compliance (FOSSA, Snyk). DMCA: automated notice processing. Data processing: DPAs for all vendors. Cost: $8K-30K/month. Overkill: patent litigation budget, multi-country regulatory filings (unless regulated industry).

### Enterprise (50+ people, 1M+ users)
Legal department (2-5+). Full IP management: patent prosecution, trademark enforcement globally, defensive publication program. Enterprise CLM: Salesforce/ironclad with AI review. Open source program office (OSPO). M&A due diligence capability. Regulatory compliance team. Litigation management. Board governance. Employment law counsel. Cost: $50K-500K+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | First enterprise contract, funding round, or user complaint | Hire fractional counsel; file USPTO trademark; do open-source audit |
| Small → Medium | Series A, 50+ employees, IP litigation threat, or international expansion | Hire in-house counsel; build IP portfolio (patents + Madrid marks); implement CLM |
| Medium → Enterprise | IPO prep, M&A, multi-country regulatory overlay, or legal team >3 | Build legal department; establish OSPO; add compliance team; formalize litigation management |


### Cross-skills Integration
```mermaid
graph LR
    A[compliance-officer] --> B[legal-advisor]
    B --> C[gdpr-privacy]
    D[ceo-strategist] --> B
    B --> E[regulatory-specialist]
```
Run skills in the order shown:
```bash
# Chain A: compliance-officer → legal-advisor → gdpr-privacy
# Chain B: ceo-strategist → legal-advisor → regulatory-specialist
```

## What Good Looks Like

> When legal advisory is applied perfectly, contracts are negotiated with precision using playbook-driven redlines that close in days not weeks, open source licenses are cataloged with zero copyleft surprises in shipping code, IP portfolios are strategically filed to create durable competitive moats, every partnership agreement protects the company's core assets while enabling commercial velocity, and the legal function is seen by the business as an enabler, not a gatekeeper.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **Contract Review & Drafting** | Any B2B agreement, vendor contract, partnership, or employment agreement | Ironclad, LinkSquares, DocuSign CLM — redlining, clause libraries, negotiation playbooks |
| **Open Source License Compliance** | Using or distributing open source software in products | FOSSA, Snyk, SPDX — license compatibility matrix, copyleft analysis, SBOM generation |
| **IP Portfolio Management** | Building moat through patents, trademarks, and trade secrets | USPTO, WIPO, Madrid Protocol — patent filing strategy (provisional → PCT → national), trademark classes |
| **SaaS Legal Foundations** | Launching or updating ToS, Privacy Policy, EULA for web/mobile app | Clickwrap/ browsewrap, GDPR/CCPA integration, limitation of liability, arbitration clause, auto-renewal |
| **DMCA & Content Liability** | Platform hosting user-generated content | DMCA safe harbor registration, notice-and-takedown, counter-notice, repeat infringer policy, Section 230 |
| **Funding & M&A Legal Prep** | Preparing for fundraising, acquisition, or IPO | IP assignment audit, cap table clean-up, open-source license audit, data room preparation, reps & warranties |
| **Contributor Agreements (CLA/DCO)** | Managing external contributions to company open-source projects | CLA (individual + corporate), DCO (Developer Certificate of Origin), license grant vs IP assignment |
| **Data Processing Agreements (DPAs)** | Vendors processing user personal data | GDPR Art. 28 clauses, SCCs, sub-processor disclosure, security measures, audit rights, breach notification |


<!-- DEEP: 10+min -->
## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep -rn "GPL\|AGPL\|copyleft" package.json go.mod Cargo.toml` + `fossa analyze --json \| jq '.dependencies[] \| select(.license \| test("GPL"))' \| wc -l` > 0 | Acquisition deal fell through when buyer's due diligence found GPL-licensed code in proprietary product — copyleft triggered source disclosure requirements | Engineering included GPL library in core product without legal review. No automated license scanning in CI. License policy not documented. GPL in proprietary codebase = dealbreaker for any acquisition | 1. Replace GPL dependency with MIT/Apache 2.0 equivalent. 2. If no equivalent, isolate behind API boundary. 3. Run `fossa analyze` on entire codebase. 4. Document remediation in data room | 1. `npx license-checker --json \| jq '.[] \| select(.licenses \| contains("GPL"))'` → inventory copyleft. 2. For each: find MIT/Apache alternative or isolate. 3. `fossa analyze && fossa test` → verify clean. 4. CI: `fossa test` blocks non-approved licenses going forward |
| `grep -rn "auto.renew\|evergreen\|automatic.renewal" contracts/*.pdf` + `pdfgrep -i "renewal.*term" contracts/*.pdf \| grep -c "3.year\|36.month"` > 0 | Vendor contract auto-renewed for 3 years at 3x market rate — evergreen clause with 90-day termination window requiring written notice, team missed the window | Contract had evergreen auto-renewal with narrow termination window. No renewal tracking system. No calendar alerts. Written notice requirement meant email didn't count | 1. Add contract renewal tracking with 120/60/30-day alerts. 2. Renegotiate: shorter terms, mutual termination for convenience, 60-day notice. 3. Every contract must have renewal reminder in legal calendar from day one | 1. `pdfgrep -i "renewal\|auto.renew\|termination.*window" contracts/*.pdf` → inventory all auto-renew clauses. 2. For each: create calendar event at 120/60/30 days. 3. `contract-review.sh --check-renewals` → monthly audit of upcoming renewals. 4. CI: flag contracts where `renewal_notice_days < 60` |
| `grep -rn "contractor\|freelance\|consultant\|external" contracts/` → count contributors. `grep -rn "IP.assignment\|work.for.hire\|invention.*assign\|assign.*all.*rights" contracts/` → compare counts — mismatch = gap | Employee who built core algorithm left and started competing product — employment agreement had general IP clause, but contractor agreement for prototype had NO IP assignment | Contractor agreement for initial prototype had no IP assignment clause — company only licensed, didn't own, the prototype. Without assignment, the contractor owns what they built | 1. Audit every contractor agreement for IP assignment language. 2. Get retroactive assignments signed. 3. Standardize: every contractor agreement includes present assignment of future IP rights + moral rights waiver. 4. Verify before any code contribution | 1. `contractor-audit.sh` → cross-reference contractor list with signed IP assignments. 2. For each gap: generate IP assignment agreement from template. 3. `grep -c "hereby.assigns\|work.made.for.hire\|present.assignment" contracts/contractors/*.pdf` → must match contractor count. 4. CI gate: no contractor access without signed IP assignment |
| `grep -rn "DMCA\|takedown\|counter.notice\|17.USC.*512" policies/` → verify process exists. `grep -rn "counter.notice.*clock\|14.business\|restoration.*timeline"` → verify counter-notice tracking | DMCA counter-notice deadline missed — user's content stayed down after counter-notice, user sued for wrongful takedown | Takedown processed but no system tracked 14-business-day counter-notice window. Files stayed down permanently by default. DMCA safe harbor requires honoring counter-notices, not just processing takedowns | 1. Implement DMCA workflow automation: notice intake → takedown → counter-notice clock → content restoration after 14 days if no lawsuit. 2. Register designated agent with USCO. 3. Automate both directions | 1. `grep -rn "designated.agent\|DMCA.*agent\|USCO.*registration" policies/` → verify agent registered. 2. `python3 scripts/test-dmca-workflow.py` → verify both takedown and counter-notice flows. 3. CI: if takedown processed, auto-start 14-business-day counter-notice clock with alert at day 10 |
| `grep -rn "trademark\|USPTO\|Class.9\|Class.42" trademarks/` → check filing status. `curl -s "https://tsdr.uspto.gov/"` check for `--search TERM` → find confusingly similar marks | Trademark registration rejected due to likelihood of confusion with existing mark — clearance search was quick Google check, not USPTO database search for similar marks in relevant classes | Clearance search did not include USPTO TESS for similar marks in Class 42 (SaaS). Google search doesn't find pending applications or phonetic similarities. Rebranding costs 10x the clearance search | 1. Use USPTO TSDR or trademark search service before adopting any brand name. 2. Search for phonetic and visual similarity, not just exact matches. 3. Budget $500-1K per clearance search. 4. Document search results | 1. `trademark-search.sh --name "BRAND" --classes 9,42` → run TESS + common law + domain + social media. 2. Generate clearance report: `trademarks/clearance-{name}.md`. 3. CI: no brand name finalization without clearance document. 4. Annual: re-run clearance for new competitive entries |
| `grep -rn "GPLv3\|AGPLv3\|SSPL\|BSL\|Elastic.License" LICENSE* package.json` → check if dependency license changed. `git diff HEAD~10..HEAD -- package.json \| grep "^+.*\"license\""` → detect license changes | GPLv2 dependency migrated to AGPLv3 in new version — auto-upgraded via dependabot, copyleft scope expanded to network use without anyone noticing | Dependabot auto-merged minor version bump of a library that relicensed from MIT to AGPLv3 in a patch release. No license-change detection in CI. AGPLv3 extends copyleft to network use (SaaS loophole closed) | 1. Run `fossa analyze` or `snyk test --all-projects` with license policy. 2. Add license-change detection: diff dependency licenses between current and proposed updates. 3. Block auto-merge if license changes or copyleft scope expands | 1. `npx license-checker --json --start HEAD~1 > before.json && npx license-checker --json > after.json && diff <(jq -S '.[].licenses' before.json) <(jq -S '.[].licenses' after.json)` → detect license changes. 2. CI gate: block merge if license changed from permissive → copyleft. 3. Auto-escalate to legal review |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Terms of Service, Privacy Policy, and EULA published, versioned, and accessible from every page footer | `curl -s https://example.com \| grep -c "terms\|privacy\|EULA"` → ≥ 3 links. `grep -rn "version.*20[2-9][0-9]\|effective.*date\|last.updated" ToS/ privacy-policy/` → version metadata present | `legal-docs-audit.sh`: crawl all pages → verify footer links. Check version tracking. Flag docs without `effective_date` and `version` metadata |
| **[S2]** | Clickwrap acceptance implemented with timestamped records of user consent | `grep -rn "I.Agree\|checkbox.*accept\|clickwrap\|explicit.consent" signup/ onboarding/` → implementation found. `grep -rn "consent.record\|acceptance.log\|agreement.timestamp"` → audit trail exists | `clickwrap-validator.sh`: simulate signup flow → verify explicit action required → verify consent record stored with timestamp + user ID + document version |
| **[S3]** | Privacy Policy accurately reflects all data collection, processing, and sharing — updated at least annually | `grep -rn "data.we.collect\|information.we.collect\|how.we.use" privacy-policy*.md` → sections present. `git log --oneline --since=365.days -- privacy-policy*` → at least 1 commitment | `privacy-policy-audit.sh`: cross-reference policy claims with actual data collection (analytics, cookies, APIs). Flag discrepancies. Alert if `last_updated` > 365 days |
| **[S4]** | Open-source license audit complete and results documented with remediation plan for any copyleft conflicts | `fossa test` → exit 0. `find sbom/ -name "*.json" \| wc -l` → ≥ 1 per service. `grep -rn "GPL\|AGPL\|EUPL\|copyleft" license-audit/` → each flagged with remediation | CI: `fossa analyze && fossa test` on every PR. Generate SBOM as build artifact. Flag copyleft deps: auto-create Jira ticket with remediation plan |
| **[S5]** | Open-source attribution page exists in-product listing all third-party components and licenses | `grep -rn "attribution\|third.party\|open.source.*notice\|license.notice" app/` → page exists. `curl -s https://app.example.com/attributions \| wc -c` → > 500 bytes (not empty) | `attribution-generator.sh`: scan all deps → generate attribution page from `npx license-checker --json`. CI: verify attribution page updates on dependency changes |
| **[S6]** | DMCA policy published with designated agent registered at U.S. Copyright Office | `grep -rn "DMCA\|17.USC.*512\|designated.agent" policies/` → policy exists. `curl -s "https://dmca.copyright.gov/osp/" ` → agent registration verified | `dmca-audit.sh`: verify policy page accessible, agent registration current, takedown workflow documented. Auto-renew agent registration annually |
| **[S7]** | Trademark applications filed for core brand elements in classes 9 and 42; monitoring/watch service active | `grep -rn "USPTO.*filed\|trademark.*registered\|Reg..*No\." trademarks/` → filing/registration found. `grep -rn "watch.service\|trademark.monitor\|TM.watch" trademarks/` → monitoring active | `trademark-status.sh`: check USPTO TSDR for application status. If not filed: generate class 9 + 42 application checklist. If no watch service: recommend providers |
| **[S8]** | Data Processing Agreement (DPA) template with SCCs available for enterprise customers | `find dpa/ -name "*.pdf\|*.md" \| wc -l` → ≥ 1. `pdfgrep "standard.contractual.clause\|2021/914\|data.processing" dpa/*.pdf` → SCCs incorporated | Generate DPA template with: Art. 28 GDPR clauses + 2021 SCCs + sub-processor list + security measures. CI: `dpa-template-check.sh` validates required sections exist |
| **[S9]** | Contract review checklist standardized and used for all vendor and partnership agreements | `grep -rn "contract.review\|review.checklist\|redline\|negotiation.playbook" contracts/` → checklist exists. `find contracts/ -name "*.md" -mtime -90` → recently reviewed | `contract-review-check.sh`: validate every new contract has completed checklist before execution. Flag contracts without `reviewed_by` and `review_date` metadata |
| **[S10]** | Contributor license process (CLA or DCO) configured for all public open-source repositories | `grep -rn "CLA\|DCO\|contributor.license\|sign.off.by" .github/ CONTRIBUTING.md` → process documented. Check each public repo for CLA bot or DCO GitHub App | `cla-audit.sh`: enumerate all public repos → verify each has CLA bot or DCO workflow. Auto-install DCO GitHub App on repos missing contributor verification |
| **[S11]** | Trade secret inventory documented and reasonable protection measures implemented | `grep -rn "trade.secret\|confidential.information\|proprietary" trade-secrets/` → inventory exists. `grep -rn "access.control\|NDA\|need.to.know" security/ hr/` → protection measures documented | `trade-secret-audit.sh`: verify inventory covers algorithms, training data, pricing models, customer lists. Check access controls, NDAs, and exit procedures for each |
| **[S12]** | Insurance requirements met: CGL, E&O, cyber insurance with adequate coverage for business size | `grep -rn "insurance\|CGL\|E&O\|cyber.insurance\|coverage" compliance/` → policy documentation exists. Coverage amounts match business stage (MVP: $1M, Growth: $2-5M, Scale: $5-10M+) | `insurance-gap-check.sh`: compare coverage amounts against business stage benchmarks. Flag if cyber insurance doesn't include breach response and regulatory defense coverage |

## MVP vs Growth vs Scale

| Phase | Team Size | Priority | Legal Approach |
|-------|-----------|----------|---------------|
| **MVP (0→1)** | 1-3 devs, no lawyer on staff | Ship legally without getting sued | Automated ToS/Privacy generators (Termly $10/mo, Iubenda $9/mo). State basic data practices. Register DMCA agent. No trademark filing yet — use ™. CLA: DCO (one-line sign-off in commits). |
| **Growth (1→10)** | 3-15 devs, part-time outside counsel ($200-500/hr, 5-10 hrs/mo) | Compliance + IP protection | Lawyer-drafted or lawyer-reviewed ToS/Privacy. File trademarks in class 9 + 42 ($1-3K per class). Open-source license audit with FOSSA. Contract review template + lawyer escalation for >$50K deals. |
| **Scale (10→N)** | 15+ devs, in-house counsel or dedicated outside GC | Defensible legal posture | Custom legal documents maintained by counsel. Full IP strategy (patents, trademarks globally). DPA with SCCs for all vendors. Compliance program (GDPR, CCPA, SOC 2). Regulatory monitoring. |

**MVP legal rule:** Don't let legal block your launch. Use generators for v1 documents. Get a lawyer to review before you have 1K users or raise funding. Nobody sues a startup with no money.

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Terms of Service | Termly / GetTerms.io generator ($10-20/mo) | Lawyer-drafted ($2K-5K one-time) | Revenue >$10K/mo, enterprise customers, or fundraising |
| Privacy Policy | Iubenda ($9/mo) or Termly | Lawyer-customized ($1K-3K) | Processing sensitive data, EU users, or B2B enterprise deals |
| Trademark filing | Self-file via USPTO TEAS ($250-350/class) | IP lawyer ($1K-3K/class including search) | Need comprehensive clearance search, international filing, or office action response |
| Open-source audit | `license-checker` + `pip-licenses` (free) | FOSSA ($330/mo startup) or Snyk | Fundraising, acquisition, or >50 dependencies with copyleft risk |
| Contract review | Template + checklist + lawyer for red flags | In-house counsel ($150K-250K/yr) | >5 contracts/month or contracts >$100K |
| DMCA compliance | Self-register agent ($6) + publish policy on site | Designated agent service | Receiving >5 DMCA notices/month |
| Patent filing | Provisional (self-file: $70-140 micro-entity) | Patent attorney ($8K-15K for non-provisional) | Strong IP asset for fundraising/defense, or competitors filing in your space |
| GDPR compliance | Self-assessment + ICO guidance (free) | Privacy consultant ($5K-15K engagement) | >10K EU users or enterprise customers requiring GDPR compliance |

**Annual legal budget by phase:** MVP: $100-500. Growth: $5K-30K. Scale: $50K-300K+.

## Scalability Decision Tree

```
Do you have paying customers?
├── YES → Do you have Terms of Service?
│   ├── NO → Get them TODAY. Use Termly/GetTerms for v1. Lawyer review within 90 days.
│   └── YES → Good. Are they clickwrap (user clicks "I agree")?
│       ├── NO → Implement clickwrap. Browsewrap is unenforceable in most jurisdictions.
│       └── YES → Good.
└── NO → Terms can wait. Focus on building.

Do you collect ANY user data (email, analytics, cookies)?
├── YES → Do you have a Privacy Policy?
│   ├── NO → This is priority #1. Every data privacy law requires one. Iubenda/Termly today.
│   └── YES → Is it accurate? (Check: does it list all 3rd-party tools you use?)
│       ├── NO → Update it. Inaccurate privacy policy is worse than no privacy policy.
│       └── YES → Good.
└── NO → (Unlikely for any software product.) Privacy policy still recommended.

Are you using ANY open-source dependencies? (Answer: yes, you are.)
├── YES → Run `npx license-checker --summary` or `pip-licenses`. Any GPL/AGPL?
│   ├── YES (GPL/AGPL in core) → Urgent: isolate via separate service or replace with MIT/Apache alternative.
│   └── No copyleft → Run FOSSA or similar before fundraising/acquisition. Keep license docs updated.
└── NO → Impossible. Run the scan anyway.

Are you fundraising or being acquired within 12 months?
├── YES → IP audit NOW: trademark filings, open-source license clean, all contractor IP assigned.
└── NO → Maintain good practices. Audit annually.
```


**What good looks like:** All customer-facing legal documents (ToS, Privacy Policy, EULA) published and versioned. Contract template library covers MSA, DPA, and SOW with standard redlines. Clickwrap consent recorded with timestamps. GDPR data map documents every data field and its lawful basis.

## When NOT to Use This Skill (Overkill)

- **Solo developer with a side project and 0 users**: A full IP strategy, trademark filings, and lawyer-drafted ToS for a project with no users is burning money. Use MIT license. Add a basic privacy notice. Ship.
- **Internal tool never exposed externally**: ToS, Privacy Policy, DMCA — these are for public-facing products. Internal tools need access control docs, not legal docs.
- **You're building on a platform that handles legal (Apple App Store, Shopify, WordPress.com)**: Use their templates. Add your privacy points. Don't start from scratch.
- **Open-source hobby project**: MIT or Apache 2.0 license + DCO. That's 90% of what you need. Don't set up a legal entity for a weekend project.
- **You have in-house counsel**: This skill is designed for teams without dedicated legal. If you have counsel, defer to them and use this as a checklist for what to ask about.

## Token-Efficient Workflow

```
# Step 1: Quick audit — what legal docs exist and are they current?
python3 scripts/legal_audit.py --site example.com --output json
# Returns: {"tos": {"exists": true, "age_days": 200, "clickwrap": false},
#           "privacy": {"exists": true, "age_days": 400, "score": "outdated"},
#           "open_source": {"gpl_count": 2, "total_deps": 150}}

# Step 2: Decision tree → prioritize by risk
# No ToS on product with users → CRITICAL. Deploy within 48 hours.
# Privacy Policy >365 days → HIGH. Update with current practices.
# GPL/AGPL in codebase → HIGH. Isolate or replace.
# No clickwrap → MEDIUM. Add to signup flow, record consent.

# Step 3: Execute with exit codes
# Check if a site has a privacy policy link in footer
curl -s https://example.com | grep -qi "privacy" && echo "FOUND" || echo "MISSING"

# Run open-source license scan (one command, exit code 1 = GPL found)
npx license-checker --production --summary 2>&1 | \
  python3 -c "import sys; text=sys.stdin.read(); sys.exit(1 if 'GPL' in text or 'AGPL' in text else 0)"

# Step 4: Verify — re-run audit after changes
python3 scripts/legal_audit.py --site example.com --verify --output json
# Exit code 0 = all critical issues resolved
```

**Principle:** `legal_audit.py` outputs structured JSON with issue severity. Agent maps severity → action via decision tree. Never reads legal document text into context (token waste). Exit codes verify fixes.

## Footguns
<!-- DEEP: 10+min — war stories from startup legal counsel -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Founder used a "standard NDA template" Googled at 11 PM — it had a forum selection clause requiring disputes in Delaware Chancery Court, and when the partnership collapsed, the founder had to litigate in a state they'd never visited | A technical founder found an NDA template on a legal blog labeled "Standard Mutual NDA — Free Download." They signed it with a potential manufacturing partner without reading the boilerplate. The forum selection clause required all disputes to be resolved in Delaware Court of Chancery. When the partner reverse-engineered the product and launched a competitor, the founder had to hire Delaware counsel ($650/hr), fly to Wilmington for depositions, and litigate in a court with no connection to either party. Legal fees: $180K for a dispute that should have cost $20K in their home state. | The founder treated all boilerplate as identical. Forum selection is one of the most consequential clauses in any contract — it determines which law applies, where you'll litigate, and how much it will cost. The template was drafted by a Delaware lawyer for Delaware clients. | **Read 3 clauses in every contract before signing: (1) forum selection/governing law, (2) limitation of liability, (3) IP ownership.** If the forum is a state you've never been to, demand your home state. If the counterparty refuses, that's a red flag — they're planning for litigation. Never use a template without knowing who wrote it, for whom, and under which state's law. |
| Startup signed MSA with a Fortune 500 customer that had no limitation of liability clause — the customer's integration broke their own production environment and sued the startup for $2.3M in "consequential damages" | A 12-person SaaS startup landed their first enterprise customer. The customer sent a 47-page MSA with a clause: "Vendor shall indemnify Customer for all losses, damages, and liabilities arising from Vendor's services." The founder was excited about the deal and signed without redlines. Six months later, the customer's internal team misconfigured the integration. Their production ERP system went down for 14 hours. The customer claimed $2.3M in lost revenue and sued under the unlimited liability clause. The startup's insurance covered $1M. The founder personally guaranteed the remaining $1.3M settlement. | No limitation of liability. Most commercial contracts cap liability at 12 months of fees paid or $X (whichever is higher). The clause should exclude gross negligence and willful misconduct but cap everything else. The founder didn't know what a limitation of liability clause was. | **Never sign a contract without a limitation of liability clause. Never.** Standard cap: 12 months of fees or the contract value. For SaaS: never accept uncapped liability for data breaches, IP infringement, or service failures. Invest $500 in a contract review by outside counsel for ANY deal over $50K — it's insurance, not overhead. If the customer says "legal will never approve a liability cap," they're bluffing. Every enterprise procurement team has a liability cap template. |
| Two co-founders split with a handshake — the one who left started a competitor using code they both wrote, and 18 months of litigation established they'd each owned 50% of the IP, rendering both companies unsellable | Two friends built an MVP over 6 months with no written agreement. One wanted to raise VC; the other wanted to bootstrap. They "agreed to part ways." The VC-bound founder incorporated and started fundraising. The other used the same codebase to launch a direct competitor. When the VC-bound founder sent a cease-and-desist, the competitor's lawyer asked: "Show us the IP assignment agreement." There was none. The code was a joint work — both owned 50% of the IP. Neither could transfer clean title to investors. The startup died. | No CIIA (Confidential Information and Invention Assignment Agreement). No entity formation before writing code. Every line of code written before incorporation is jointly owned by the people who wrote it unless there's a signed assignment. | **Incorporate FIRST, then write code.** The day you have a co-founder, file incorporation papers. Every founder and contractor signs a CIIA BEFORE touching the codebase. The CIIA assigns all IP to the company. Use Clerky or Stripe Atlas ($500) for standard formation docs — don't DIY incorporation any more than you'd DIY surgery. If code was written pre-incorporation, the founders sign a "Founder IP Assignment" retroactively assigning it to the company. Do this before your first investor meeting. |
| VC term sheet said "standard participating preferred with 3× liquidation preference" — founders celebrated a $50M exit and got $0 because the preference stack consumed every dollar | A startup raised $8M Series A on a term sheet the founders' lawyer called "market standard." At exit: the company sold for $50M. The investors held participating preferred with 3× liquidation preference. Calculation: 3 × $8M = $24M to investors first (liquidation preference), then investors participate pro-rata in remaining $26M as if they'd converted to common, taking another ~$20M. What about the founders and employees who owned 60% of fully diluted equity? They split $6M. But the option pool strike prices, tax withholding, and transaction fees consumed the remaining $6M. Founders: $0 each. Employees: worthless options. | The founders and their lawyer didn't understand the economic impact of participating preferred × 3×. They focused on valuation ($50M! Great!) and ignored liquidation preference structure. "Participating" means investors get their preference AND participate in proceeds. "3×" means they get 3× their investment before anyone else sees a dollar. | **Model the exit waterfall before signing a term sheet.** Build a cap table with every liquidation scenario: what does each shareholder get at $10M, $25M, $50M, $100M exits? If founders get $0 at a $50M exit, the deal is bad regardless of the headline valuation. Standard (non-participating) 1× preference is founder-friendly. Participating preferred with a cap (e.g., "participating up to 3×") is a compromise. Uncapped participating preferred is a trap. If your lawyer can't explain the waterfall in plain English, get a new lawyer. |
| Employment offer letter used a template from 2012 — the "at-will employment" clause was unenforceable in Montana, and the company paid $90K to settle a wrongful termination claim they should have won | A startup used the same offer letter template for all hires across 50 states. They fired a Montana-based employee for documented performance issues. The employee sued for wrongful termination. Montana is the only US state that doesn't recognize at-will employment — after a probationary period, terminations require "good cause." The startup's documentation was solid (PIP, written warnings, performance reviews), but their offer letter said "employment is at-will" — which is a misrepresentation of Montana law. The court found the termination was substantively justified but the company's failure to follow Montana-specific procedure (the Wrongful Discharge from Employment Act requires specific steps) made the termination procedurally defective. Settlement: $90K. | The offer letter template was written by a California lawyer and assumed California law applies everywhere. Employment law is hyper-local — every state has different rules for at-will, non-competes, final paycheck timing, and mandatory notices. | **Employment templates must be jurisdiction-specific, not one-size-fits-all.** At minimum, maintain state-specific addenda for CA, NY, MA, MT, and WA. Use an HR platform (Rippling, Gusto, Deel) that generates compliant offer letters per jurisdiction. If you have remote employees in 10+ states, invest in a multi-state employment law audit ($5K-15K) — it's cheaper than one wrongful termination settlement. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can redline a contract but can't explain to a founder which 3 clauses will determine whether they get rich or get destroyed | You can look at a term sheet for 5 minutes and tell the founder: "The $20M valuation with this liquidation structure leaves you with nothing below a $60M exit — here's the math" | A VC's general counsel reads your term sheet redlines and responds with: "These are the best founder-protective terms I've seen in 15 years" — and the deal still closes |
| You forward contracts to "outside counsel" for every question because you're afraid to make a call | You handle 90% of commercial contracts in-house (MSAs, DPAs, SOWs, NDAs) and escalate only the 10% that genuinely need specialist attention | You design the contract playbook that a 200-person legal team uses globally — every clause has a fallback position, an explanation for sales, and an escalation trigger |
| You tell a founder "you need to talk to a lawyer" without being able to name the specific issue or what kind of lawyer they need | You can tell a founder in 10 minutes whether their cap table is clean enough for Series A, their open-source licenses won't kill a acquisition, and their contractor agreements won't blow up in diligence | An acquirer's $2,000/hr M&A partner reviews your client's legal due diligence and finds nothing — not because the client hid things, but because you anticipated every diligence request and had the answer ready before they asked |

**The Litmus Test:** A founder hands you a 40-page MSA from their biggest customer and says "should I sign this?" Can you identify the 3 highest-risk clauses in under 10 minutes, explain the risk to a non-lawyer in plain English, and propose specific redlines that protect the founder without killing the deal? If you can't find the liability cap, IP indemnity, and termination rights within 2 minutes of skimming, you're not ready for L3.

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
<!-- QUICK: 30s -- links to deeper reading -->
- [IAPP — Privacy Policy Template Guidance](https://iapp.org/)
- [FOSSA — Open Source License Compliance](https://fossa.com/)
- [Choose a License](https://choosealicense.com/)
- [U.S. Copyright Office — DMCA Designated Agent](https://www.copyright.gov/dmca-directory/)
- [USPTO — Trademark Basics](https://www.uspto.gov/trademarks/basics)
- [Open Source Initiative — Approved Licenses](https://opensource.org/licenses/)
- [European Commission — Standard Contractual Clauses (SCCs)](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en)
