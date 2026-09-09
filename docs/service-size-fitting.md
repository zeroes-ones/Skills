# Service Size Fitting — Right-Size Any Services Job (XS → XL)

For freelancers, agencies, and delivery orgs: whatever the work — **SaaS or product
development, any kind of development, design/content/data/ML services, discovery and
consulting, support and retainers** — this page tells you how to *size it (XS → XL)* and what
*"fits"*: the effort band, who delivers it, the engagement model, the skills, the runnable
example to copy, the estimate → price → SOW path, and where the human gates sit.

Pair with `docs/client-request-playbook.md` (fit by *type* of request). This page fits by
*size* of job. Both route into the same estimators and pricing chain.

---

## 1. The unified size scale (fits all work kinds)

One scale across products, development, and services. Effort bands are *consultant/
engineer-days* (services) or *engineer-weeks/months* (build); use the estimator that matches
the work:

| Size | Effort band | Who delivers | Model that fits | Estimator |
|---|---|---|---|---|
| **XS** | ≤ 3 days | solo freelancer | fixed (day-box) or hourly | consulting-effort-estimator |
| **S** | 3–10 days | solo / 1 specialist | fixed (buffered) | software-project-estimator (S) or consulting |
| **M** | 2–6 eng-weeks | 1–3 people (solo + reviewer) | fixed or fixed + T&M | software-project-estimator (M) |
| **L** | 1.5–3 eng-months | small team | fixed slices + T&M, staged | software-project-estimator (L) |
| **XL** | 3–9 eng-months | team / multi-track | program, phased, T&M lanes | software-project-estimator (XL) |
| **XXL** | > 9 eng-months | multi-team / org | portfolio, staged gates | estimator + program review |

Work kinds map onto the same scale:

| Work kind | XS–S anchor | M anchor | L–XL anchor |
|---|---|---|---|
| SaaS / product feature | 1 feature | MVP slice (auth+core+payments) | product v1 / platform |
| Any development | small change | one module + integration | multi-area build |
| UI/design/content | 1 view / deliverable | design system slice | multi-deliverable program |
| Data / ML | 1 model / report | pipeline + model | data platform |
| Discovery / consulting | advisory 0.5–2 d | roadmap/audit 4–10 d | options program 10–25 d |
| Support / retainer | 2–5 d/mo bucket | 6–12 d/mo retainer | SLA tiers + team |
| Fractional / staff-aug | — | 4–10 d/mo role | multiple roles |

---

## 2. Fit by size — the full map

| Size | Typical client job | Copy this example | Skills to load | Money path | Your gates |
|---|---|---|---|---|---|
| **XS** | invoice export feature, one UI tweak, advisory call | `examples/add-feature` or `examples/ui-change` | idea-to-spec → backend/frontend → qa | consulting/software estimator → pricing → SOW (or proposal under $5K) | acceptance |
| **S** | change an API, create a DB/schema, small design deliverable | `examples/api-change`, `examples/db-create` | api-designer/database-designer → backend → secure → qa | estimator (S band ±25%) → pricing (buffer 15–25%) → SOW | schema review + acceptance |
| **M** | SaaS MVP slice, small-team product release | `examples/payments-api-ship`, `examples/team-product` | spec → architect → parallel tracks → qa loop → agent gate → human release | estimator (M ±30%) → pricing → SOW | prod/release gate |
| **L** | product v1, DB/system migration, one platform module | `examples/strangler-migration`, `examples/team-product` | migration-architect/api-designer → impl → parity loop → cutover | estimator (L ±40%) + risk → pricing staged → SOW per slice | plan + cutover (two humans) |
| **XL** | platform build, regulated release, multi-track program | `examples/enterprise-platform` | parallel readiness (impl/security/compliance) → loop → compliance → canary → board | estimator (XL ±50%) → pricing program → SOW + annexes | compliance + release board |
| **Retainer** | support & maintain month, fractional role | `examples/support-maintain` | customer-support/intake → fix loop → month close | maintenance estimator (15–25%/yr) → retainer terms → SOW annex | month close / SLA scope |
| **Firefight** | prod incident (any size) | `examples/production-incident` | triage → stabilize loop → commander | T&M / emergency terms | declare / rollback |

---

## 3. Fit rules (the "that fits" logic)

1. **Size first, then fit.** Classify the job into a size band, then pick the row — don't pick
   the example by habit.
2. **Model follows risk + size:** XS–S → fixed (or hourly while you calibrate); M → fixed with
   buffer or fixed+T&M; L–XL → staged fixed slices + T&M lanes; retainer/ongoing → monthly
   commitment priced as a premium.
3. **Who delivers scales with size:** XS–S solo; M solo+reviewer/agents; L small team
   (parallel tracks); XL multi-track with compliance; XXL program governance.
4. **Human gates scale too:** acceptance (XS–S) → schema/release gates (M) → plan+cutover or
   compliance+board (L–XL) → month close (retainer) → commander (incidents).
5. **Every job flows the same money path:** estimator → services-engagement-pricing →
   statement-of-work-authoring → legal review; add software-maintenance-support-estimator when
   the client will need ongoing support.

---

## 4. Decision tree: size → fit in three steps

**Step 1 — Classify.** Effort estimate (estimator) or gut check by deliverable count.
```
≤3 days → XS    3–10 d → S    2–6 wk (1–3 ppl) → M    1.5–3 mo → L    3–9 mo → XL    >9 mo → XXL
```

**Step 2 — Match work kind to the anchor** (table in §1): product? dev? UI/design? data/ML?
discovery? support? fractional?

**Step 3 — Pick the row in §2** and run it: example + skills + money path + gates. If the job
spans kinds (build + migrate + support), chain rows: `payments-api-ship` +
`strangler-migration` + `support-maintain` terms.

---

## 5. Worked walkthroughs

**XS — freelancer: "export invoices to PDF" (SaaS).** 2–3 days → `examples/add-feature`;
estimate S/XS band; price fixed ~$1,500–2,500 with 15–25% buffer; proposal + acceptance email
is enough under $5K. Gates: your acceptance.

**S — "change the payments API" (product).** 3–10 days → `examples/api-change`; contract →
impl → secure → qa; estimate S band; fixed with assumptions register; SOW one-pager. Gates:
contract review + acceptance.

**M — "build a booking MVP" (SaaS).** 4–6 weeks → `examples/payments-api-ship`; parallel
audits, fix-verify loop, agent gate before human release; estimate M ±30% (≈ $48–60K base at
agency rates); fixed + buffer, milestone 30/30/40; SOW with deliverables + acceptance +
change control. Gates: spec sign-off, release approval.

**L — "migrate the legacy DB" (product/platform).** 6–12 weeks → `examples/strangler-migration`;
analyze → human plan gate → design → parity loop → human cutover; estimate per slice + cutover
risk; staged fixed + T&M lane; two SOW milestones. Gates: plan + cutover.

**XL — "regulated platform release" (org).** 3–9 months → `examples/enterprise-platform`;
parallel readiness (implement/security/compliance), canary, observability; compliance + board
gates; program pricing with retainers; SOW + annexes. Gates: compliance + release board.

**Retainer — "support and maintain the app."** monthly → `examples/support-maintain`;
15–25% of build/yr risk-adjusted; SLA tiers + bucket; SOW support annex; month-close review
with true-up. Gates: month close / renewals.

**Services (non-dev) — "discovery audit" or "fractional CTO".** consulting-effort-estimator
day-boxes (audit 5–25 d; fractional 4–10 d/mo) → pricing → SOW (or retainer terms). Gates:
deliverable acceptance; monthly availability review.

---

## 6. If it still doesn't "fit"

- **Job is too vague to size** → run a discovery day-box first (fixed 5-day sprint), then size.
- **Mixed-size program** → break into size bands and run each band's row; schedule the L/XL
  gates between slices.
- **You have no actuals** → widen the bands, mark [ESTIMATED], calibrate from the backtests in
  the estimator skills.
- **Support is part of the deal** → add `software-maintenance-support-estimator` terms while
  the build is fresh (15–25%/yr, true-up, enhancement T&M lane).

---

## Where this lives in the repo

- Estimators: `software-project-estimator`, `consulting-effort-estimator`
- Money + contract: `services-engagement-pricing`, `statement-of-work-authoring`,
  `software-maintenance-support-estimator`
- Runnable examples: `examples/` (index in `examples/README.md`, diagrams in
  `examples/DETAILED-DIAGRAMS.md`)
- Research: `docs/estimation-research.md` (coverage matrix + benchmarks)
