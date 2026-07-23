# Decision Trees for legal-advisor

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
