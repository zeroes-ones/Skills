## Decision Trees

<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### 1. Library Adoption Decision Tree

```
                    ┌──────────────────────────┐
                    │ START: Considering       │
                    │ adopting tool X?         │
                    └───────────┬──────────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Popularity Check:   │
                     │ GitHub Stars >1K?   │
                     │ OR npm DL >100K/wk? │
                     └────┬───────────┬────┘
                          │NO         │YES
                     ┌────▼────┐      │
                     │ Niche   │      │
                     │ tool —  │      │
                     │ proceed │      │
                     │ with    │      │
                     │ caution │      │
                     └────┬────┘      │
                          │           │
                          └─────┬─────┘
                                │
                     ┌──────────▼──────────┐
                     │ Maintenance Check:  │
                     │ Commits in last     │
                     │ 3 months?           │
                     └────┬───────────┬────┘
                          │NO         │YES
                     ┌────▼────────┐ │
                     │ RED FLAG:   │ │
                     │ Possibly    │ │
                     │ abandoned.  │ │
                     │ Check for   │ │
                     │ community   │ │
                     │ forks.      │ │
                     └────┬────────┘ │
                          │         │
                          └───┬─────┘
                              │
                     ┌────────▼──────────┐
                     │ Security Check:   │
                     │ Unresolved CVEs   │
                     │ HIGH/CRITICAL?    │
                     └────┬─────────┬────┘
                          │YES      │NO
                     ┌────▼────┐   │
                     │ RED:    │   │
                     │ Avoid.  │   │
                     │ If must │   │
                     │ use,    │   │
                     │ plan    │   │
                     │ mitiga- │   │
                     │ tions.  │   │
                     └────┬────┘   │
                          │       │
                          └──┬────┘
                            │
                     ┌──────▼────────────┐
                     │ Bundle Size Check │
                     │ (frontend only):  │
                     │ <50KB gzipped?    │
                     └────┬─────────┬────┘
                          │NO       │YES
                     ┌────▼────┐   │
                     │ YELLOW: │   │
                     │ Evaluate│   │
                     │ necessity│   │
                     │ vs.      │   │
                     │ lighter  │   │
                     │ alt.     │   │
                     └────┬────┘   │
                          │       │
                          └──┬────┘
                            │
                     ┌──────▼────────────┐
                     │ License Check:    │
                     │ MIT/Apache2.0/BSD │
                     │ for commercial?   │
                     └────┬─────────┬────┘
                          │NO       │YES
                     ┌────▼────┐   │
                     │ YELLOW: │   │
                     │ GPL/AGPL│   │
                     │ may     │   │
                     │ restrict│   │
                     │ commer- │   │
                     │ cial use│   │
                     └────┬────┘   │
                          │       │
                          └──┬────┘
                            │
                     ┌──────▼────────────┐
                     │ Docs Quality:     │
                     │ Comprehensive     │
                     │ docs + examples?  │
                     └────┬─────────┬────┘
                          │NO       │YES
                     ┌────▼────┐ ┌─▼──────────┐
                     │ YELLOW: │ │ GREEN:      │
                     │ Factor  │ │ Adopt with  │
                     │ 2x dev  │ │ confidence. │
                     │ time    │ │ Monitor      │
                     │ cost.   │ │ quarterly.  │
                     └─────────┘ └─────────────┘
```

**Stars >1K AND maintained → green path.** Stars <1K but well-maintained → niche tool, proceed with caution. No commits in 6+ months → abandoned, avoid unless you're willing to fork and maintain.


### 2. Tool Replacement Decision Tree

```
                    ┌──────────────────────────┐
                    │ START: What's wrong with │
                    │ your current tool?       │
                    └───────────┬──────────────┘
                                │
          ┌─────────────────────┼──────────────────────┐
          │                     │                      │
    ┌─────▼──────┐       ┌──────▼──────┐       ┌───────▼──────┐
    │ Missing    │       │ Too         │       │ Abandoned /  │
    │ features?  │       │ expensive?  │       │ dead?        │
    └─────┬──────┘       └──────┬──────┘       └───────┬──────┘
          │                     │                      │
    ┌─────▼──────────┐  ┌───────▼───────┐      ┌───────▼──────────┐
    │ Find           │  │ Cost          │      │ Check for        │
    │ alternatives   │  │ Optimization  │      │ community forks. │
    │ that have the  │  │ Matrix:       │      │ If none:         │
    │ feature.       │  │ - Free tier?  │      │ Plan migration   │
    │ Compare        │  │ - OSS alt?    │      │ to maintained    │
    │ feature matrix │  │ - Self-host?  │      │ alternative.     │
    │ for candidates │  │ - Negotiate?  │      │ Do NOT stay on   │
    └────────────────┘  └───────────────┘      │ dead tool.       │
                                               └──────────────────┘
          │                     │                      │
          └─────────────────────┼──────────────────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Bundle too large?   │
                     │ (frontend only)     │
                     └────┬───────────┬────┘
                          │YES        │NO
                     ┌────▼────────┐ │
                     │ Find lighter│ │
                     │ alternative │ │
                     │ with tree   │ │
                     │ shaking.    │ │
                     │ Check       │ │
                     │ bundlephobia│ │
                     └─────────────┘ │
                                     │
                              ┌──────▼─────────┐
                              │ Proceed with    │
                              │ Multi-Dimension │
                              │ Comparison of   │
                              │ replacement     │
                              │ candidates.     │
                              └─────────────────┘
```

**Feature gap → find alternatives with that feature.** Cost issue → cost optimization ladder first. Abandoned → community fork or migrate. Bundle too large → lighter alternative with tree shaking.


### 3. Stack Composition Decision Tree

```
                    ┌──────────────────────────┐
                    │ START: Building a new     │
                    │ project/feature?          │
                    └───────────┬──────────────┘
                                │
          ┌─────────────────────┼──────────────────────┐
          │                     │                      │
    ┌─────▼──────┐  ┌───────────▼──────────┐  ┌───────▼──────┐
    │ What's     │  │ What's the team's    │  │ What's the   │
    │ the budget?│  │ skill set?           │  │ timeline?    │
    └─────┬──────┘  └───────────┬──────────┘  └───────┬──────┘
          │                     │                      │
    ┌─────▼──────┐  ┌───────────▼──────────┐  ┌───────▼──────┐
    │ <$500/mo  │  │ Mostly JS/TS        │  │ <2 weeks    │
    │ → OSS+    │  │ → Node/Next.js      │  │ → Monolith  │
    │ free tier │  │ ecosystem            │  │ + managed   │
    │ + server- │  │                      │  │ services    │
    │ less      │  │ Mostly Python        │  │             │
    │           │  │ → FastAPI/Django     │  │ <3 months   │
    │ $500-5K/mo│  │                      │  │ → Modular   │
    │ → Managed │  │ Mostly Go/Rust       │  │ monolith    │
    │ services  │  │ → Go stdlib +        │  │ + some      │
    │ + some    │  │ minimal deps         │  │ services    │
    │ paid      │  │                      │  │             │
    │           │  │ Mixed team           │  │ 3+ months   │
    │ $5K+/mo   │  │ → Pick ecosystem     │  │ → Micro-    │
    │ → Enter-  │  │ with best tooling    │  │ services    │
    │ prise tier│  │ + most hiring pool   │  │ or modular  │
    └───────────┘  └──────────────────────┘  └─────────────┘
```

**Budget drives infrastructure choices.** Team skills drive language/framework choices. Timeline drives architecture complexity. All three must align — a mismatch in any dimension creates expensive rework.


### 4. OSS vs Paid Decision Tree

```
                    ┌──────────────────────────┐
                    │ START: OSS or paid tool? │
                    └───────────┬──────────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Budget available    │
                     │ for paid tools?     │
                     └────┬───────────┬────┘
                          │NO         │YES
                          │           │
                     ┌────▼────┐ ┌────▼───────────┐
                     │ Go OSS  │ │ Need SLA/support│
                     │ + self- │ │ guarantee?      │
                     │ support │ └────┬───────┬────┘
                     └─────────┘      │NO     │YES
                                      │       │
                                ┌─────▼──┐ ┌──▼──────────┐
                                │ Go OSS │ │ Go paid     │
                                │ +      │ │ (vendor SLA)│
                                │ option │ │              │
                                │ to pay  │ │ OSS with    │
                                │ for     │ │ enterprise  │
                                │ support │ │ support      │
                                │ later   │ │ option       │
                                └─────────┘ └─────────────┘
                                      │       │
                                ┌─────▼───────▼─────┐
                                │ Compliance         │
                                │ requirements?      │
                                │ (SOC2, HIPAA,      │
                                │ GDPR, FedRAMP)     │
                                └────┬──────────┬────┘
                                     │YES       │NO
                                ┌────▼────┐     │
                                │ Verify  │     │
                                │ vendor/ │     │
                                │ OSS     │     │
                                │ compli- │     │
                                │ ance    │     │
                                │ certs.  │     │
                                │ Prefer  │     │
                                │ paid    │     │
                                │ with    │     │
                                │ DPA.    │     │
                                └────┬────┘     │
                                     │          │
                                     └────┬─────┘
                                          │
                                   ┌──────▼──────────┐
                                   │ Integration      │
                                   │ complexity?      │
                                   └────┬────────┬────┘
                                        │YES     │NO
                                   ┌────▼────┐  │
                                   │ Paid    │  │
                                   │ often   │  │
                                   │ has     │  │
                                   │ better  │  │
                                   │ SDKs,   │  │
                                   │ docs,   │  │
                                   │ support │  │
                                   └────┬────┘  │
                                        │      │
                                        └──┬───┘
                                           │
                                    ┌──────▼──────────┐
                                    │ DECISION: Choose │
                                    │ based on budget, │
                                    │ support needs,   │
                                    │ compliance, and  │
                                    │ integration cost │
                                    └──────────────────┘
```

**No budget → OSS with self-support.** SLA needed → paid or OSS with enterprise support. Compliance → verify certs regardless of OSS/paid. Complex integration → paid tools often save more in dev time than they cost.
