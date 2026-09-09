# Estimation & Services Pricing — Research Base

Gap analysis, methodology digest, and benchmark numbers behind the estimation skill cluster:
`software-project-estimator`, `services-engagement-pricing`,
`software-maintenance-support-estimator`. Written so the three skills can cite numbers instead
of vibes, and so a reviewer can check where each figure came from.

## 1. Gap analysis (why these skills exist)

A full name/body scan of the 303-skill corpus found **no dedicated estimation or services-pricing
skill**. Closest coverage and where it stops:

| Existing skill | Has | Missing |
|---|---|---|
| `project-manager` | planning, RAID, EVM, critical path | no sizing→effort→price pipeline |
| `scrum-master` | story-point estimation process | no client-facing quote/price output |
| `technical-program-manager` | cross-team forecasting | no category/rate modeling |
| `sales-engineer`, `revops-manager` | pre-sales, pipeline | estimation internals only, no rate card |
| `enterprise-pricing-strategist`, `saas-monetization-strategist` | **product** pricing | **project/SOW/services** pricing |

**Cluster wiring (self-contained trio, chain edges symmetric within the cluster):**

```
software-project-estimator ⇄ services-engagement-pricing      (mutual: estimate→price,
software-project-estimator ⇄ software-maintenance-support-estimator   price/support actuals→calibration)
services-engagement-pricing ⇄ software-maintenance-support-estimator
```

Each skill also documents cross-skill coordination (scrum-master/sales-engineer/project-manager/
accountant as input/output neighbors in prose) without hard chain edges, so consumers can route
by prose while the graph stays internally symmetric.

Input → output flow the user asked for: (scope, size class, engagement category, rates) →
effort estimate → engagement price → maintenance/support price.

## 2. Sizing & effort — methodology digest

- **Planning altitude decides the method.** T-shirt XS–XXL for roadmap/budget altitude (before
  user stories exist); story points + calibrated velocity for sprint altitude; never map points
  rigidly to hours ("1 point = 4 hours" is the most-cited anti-pattern).
  A common mapping is XS=1, S=2, M=3, L=5, XL=8, XXL=13 relative points (GitLab).
- **Three-point / PERT:** `Expected = (O + 4M + P) / 6`; widen ranges for large items because
  larger items carry disproportionate uncertainty.
- **Reference-class forecasting:** anchor to actuals of past similar projects, not to hopes.
- **Accuracy reality (use these, not CHAOS headlines):**
  - Cone of Uncertainty: early estimates can be ~±4×; narrows as work proceeds.
  - Peer-reviewed synthesis (Jørgensen & Moløkken-Østvold, 2006): typical **cost overruns
    30–40%**, with **60–80% of projects** overrunning in some form; the CHAOS 89–189% figures are
    inflated by sampling bias toward failed projects.
  - Calibrated teams with relative sizing + tracked actuals are the practical accuracy ceiling;
    expert judgment remains the most-used method.
- **Fixed-bid / SOW discipline (vendor side):** write all assumptions down, publish a
  **re-estimation trigger at ~15–20% scope change**, keep historical calibration data, and get
  independent review above materiality thresholds. SOW language is legal: unclear specs are where
  disputes start.

Sources: GitLab handbook (professional-services estimation), Wrike/Boundev/Viprasol estimation
guides, Scrum.org ("Estimation isn't broken…"), ScienceDirect critique of CHAOS (Jørgensen &
Moløkken-Østvold), Ridiculous Engineering estimation guide.

## 3. Pricing & engagement categories — methodology digest

- **Models:** hourly · fixed-fee/fixed-bid · time & materials (T&M) · retainer · value-based.
  Providers mix them (fixed for a scoped build + T&M for post-launch iteration is common).
- **Risk split is the deciding factor:** fixed-price → provider carries estimation/overrun risk;
  T&M → client does (mitigate with not-to-exceed caps, low/high hour ranges, weekly burn reports).
- **Rate math:**
  - Billable load ≈ **1,200–1,400 hours/year** (60–70% utilization of ~2,000), NOT 2,080.
  - `profitable rate = (desired salary + overhead + profit) ÷ annual billable hours`.
  - Overhead is lean at 25–40% of labor; rule-of-thirds (⅓ comp, ⅓ overhead, ⅓ tax/margin).
  - Firms price by multiplier: billing rate = direct pay × overhead factor (2.0–3.7×) × profit
    markup (1.10–1.25).
  - Retainer = premium over project rate (guaranteed availability), not a discount.
- **Market segmentation:** B2B engagements price **~2–4×** B2C equivalents (procurement rigor,
  company budgets, exec-level work higher); C2C/B2C sessions price at the individual end;
  B2G adds compliance overhead and longer sales cycles. Use category multipliers on the base rate.
- **Value-based** ranks above project > retainer > day > hourly for income, but needs provable
  results and inbound demand.

Sources: Xero/HoneyBook/Plutio/Toggl consulting-pricing guides, Deltek consulting pricing models,
Catalant "Pricing to Win", Glencoyne hourly-billing guide, ClientCasa per-client profitability,
Small Business Chron / Architekwiki billing-rate multipliers.

## 4. Maintenance & support — methodology digest

- **Budget heuristic: 15–25% of original build cost per year** for ongoing maintenance +
  support (budget anchor, not a pricing formula).
- Adjust upward to **30–40%/yr** for regulated industries, legacy / high-technical-debt systems,
  high-SLA or critical systems; unmanaged debt compounds +15–20%/yr.
- **Lifecycle view:** maintenance is 50–80% of total cost of ownership (IEEE ~60%; IBM 50–75%;
  Gartner 55–80% of IT budgets); post-launch enhancement/modification ≈ **3–4× the original
  build over the system's lifetime** (Standish).
- **Maintenance mix** (ScienceSoft): corrective 20–25%, adaptive 15–20%, perfective 25–30%,
  preventive 10–15% — so "support" ≠ "all of maintenance."
- **Products to price:** SLA tiers (availability + response time), hours-bucket retainers,
  enhancement T&M above the retainer, and annual maintenance % of the build.

Sources: Axented, BlastAsia, Netguru, ScienceSoft via CodeStringers, JHAVTECH, PC Tech Magazine
(2026 maintenance-cost guides).

## 5. Services & consulting coverage matrix (what the cluster prices, and how)

Any client ask maps to an engagement type; each maps to a model, an estimator, and the pricing
skill. "Estimator" column = the skill that sizes the effort for the pricing skill.

| Engagement type | Client ask examples | Estimator | Default model | Key driver |
|---|---|---|---|---|
| Build (app/feature/API/DB) | new app, add feature, change API, create DB | `software-project-estimator` | fixed (scoped) or T&M | effort class + risk |
| Change/redesign | UI change, refactor | `software-project-estimator` (S class) | fixed | bounded scope |
| Migrate | DB/system migration | `software-project-estimator` + migration workflow | fixed per slice | parity risk |
| Incident / ops firefight | prod down | incident workflow | T&M / emergency terms | time-boxed |
| Support & maintain | retainer, SLA, annual | `software-maintenance-support-estimator` | retainer + T&M lane | % of build + risk |
| Discovery / consulting | audit, roadmap, tech advisory, options analysis | `consulting-effort-estimator` | day rate or fixed small | deliverable days |
| Non-software deliverables | design, content, data, ML model, training, docs | `consulting-effort-estimator` | fixed per deliverable | deliverable-based sizing |
| Ongoing / fractional | part-time CTO, staff augmentation, support-team placement | `consulting-effort-estimator` | monthly retainer / placement | availability premium |
| Value/outcome-based | growth on revenue, SLA-backed ops | pricing skill (value rules) | value-based | metric + floor |

Segment playbooks (how to present and buffer the same work):

| Segment | Presentation | Buffer/multiplier notes |
|---|---|---|
| Solo freelancer | simple fixed or hourly; build actuals | buffer 15–25% on fixed |
| Agency | structured SOW, milestone billing | firm multiplier 2.0–3.7× |
| Productized service | packaged tiers, published pricing | fixed scope per tier + T&M overflow |
| Enterprise / B2B | procurement-grade SOW + category multiplier | B2B 2–4×, compliance overhead |
| B2G | RFP-compliant, long cycles | 3–5× equivalent, payment lag priced |

This matrix is the routing layer for `docs/client-request-playbook.md`: every row above has a
runnable example there except the consulting rows, which the `consulting-effort-estimator` skill
covers directly (discovery, non-software deliverables, ongoing/fractional engagements).

## 6. Known weaknesses of these numbers

- Many maintenance "benchmarks" are vendor-published budget heuristics; treat as starting anchors
  and calibrate to your own actuals.
- B2C/B2B multiplier ranges are directional (2–4×), vary by niche; use your own historical win
  data where available.
- Estimation accuracy is distributional, not a point: always quote a range and a confidence band.
