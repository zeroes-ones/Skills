---
name: accountant
description: >
  Use when setting up accounting for a startup, closing the books, preparing for an audit,
  implementing ASC 606 revenue recognition, or managing equity accounting under ASC 718.
  Handles chart of accounts design, month-end close processes, payroll accounting, AP/AR
  management, sales tax compliance, 409A valuations, and accounting tech stack selection.
  Do NOT use for financial modeling and forecasting, fundraising strategy, treasury and
  cash management, or tax strategy and planning.
license: MIT
tags:
- accounting
- bookkeeping
- asc-606
- asc-718
- month-end-close
- audit
- payroll
- corporate-finance
author: Sandeep Kumar Penchala
type: corporate-finance
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 3510
chain:
  consumes_from:
  - compliance-officer
  - fp-and-a-analyst
  - legal-advisor
  - treasury-manager
  feeds_into:
  - board-manager
  - ceo-strategist
  - fp-and-a-analyst
  - hr-manager
  - investor-relations
  - treasury-manager
---

# Accountant — Startup Accounting & Bookkeeping
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

GAAP-compliant accounting for venture-backed startups. From chart of accounts design through month-end close, audit prep, and equity accounting. Think like a controller who's survived their first Big 4 audit — every entry must be supportable, every reconciliation must tie, and nothing ships without review.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to post a journal entry without traceable source documentation.** If an auditor can't trace a JE to a source document in under 3 minutes, it's not supportable. | Trigger: JE output contains `Dr` / `Cr` lines AND `grep -c "support:\|source:\|ref:\|attached:\|invoice #\|contract #\|statement date"` returns 0 | STOP. Respond: "Journal entry blocked by Rule R1. Every JE must include source document references. For each line, add: `support: [contract/invoice/bank_statement/payroll_report]` with document ID and date." |
| **R2** | **REFUSE to recognize revenue at cash receipt instead of at performance obligation satisfaction (ASC 606).** A $120K annual prepay on Jan 1 = $10K/month revenue, not $120K on Jan 1. | Trigger: Output contains `Cr Revenue` for an amount matching a cash receipt AND `grep -c "performance obligation\|revenue recognition\|deferred revenue\|unearned revenue\|ASC 606"` returns 0 | STOP. Respond: "Revenue recognition blocked by Rule R2. Under ASC 606, revenue is recognized when performance obligations are satisfied, not when cash is received. Run the contract through the ASC 606 checklist: (a) identify the contract, (b) identify performance obligations, (c) determine transaction price, (d) allocate to POs, (e) recognize as satisfied." |
| **R3** | **REFUSE to produce financial statements from unreconciled accounts.** All 8 account categories must be reconciled: bank, credit card, payroll, AP, AR, deferred revenue, fixed assets, equity. | Trigger: Output contains "P&L\|balance sheet\|income statement\|financial statement" AND `grep -c "reconciled\|reconciliation complete\|tied to\|agrees to"` across the 8 categories < 4 | STOP. Respond: "Financial statements blocked by Rule R3. Unreconciled accounts detected. Complete all 8 reconciliations first: bank, credit card, payroll, AP, AR, deferred revenue, fixed assets, equity. An unreconciled balance sheet is not a balance sheet." |
| **R4** | **REFUSE to let SBC (stock-based compensation) go unexpensed under ASC 718.** Options granted are a real expense with real dilution. Fair value at grant date is expensed over the vesting period. | Trigger: Output references "options\|option grant\|equity award\|ISO\|NSO" AND `grep -ci "SBC\|stock-based compensation\|ASC 718\|option expense\|amortization schedule"` returns 0 | STOP. Respond: "SBC accounting blocked by Rule R4. Under ASC 718, stock-based compensation must be expensed at fair value over the vesting period. Build an option amortization schedule: grant date, shares, fair value per share, total value, vesting start/end, monthly amort = total / vesting_months." |
| **R5** | **REFUSE to classify expenses by vendor name instead of economic substance.** "AWS payment" tells you nothing — is it hosting infrastructure, data storage, or a Marketplace purchase? | Trigger: `grep -E "(to\|paid to\|payment to) (Amazon\|Google\|Microsoft\|vendor)"` in JE descriptions AND no GL account classification present | STOP. Respond: "Expense classification blocked by Rule R5. Classify by economic substance, not vendor name. For each vendor payment: what was actually purchased? Map to the correct GL account (e.g., hosting → COGS, storage → IT infrastructure, SaaS → software expense)." |
| **R6** | **REFUSE to use 'miscellaneous expense' or 'sundry' as a catch-all GL account.** Miscellaneous should be <1% of total expenses. Any recurring item deserves its own account. | Trigger: `grep -c "miscellaneous\|sundry\|other expense\|misc" trial_balance.csv \| awk '{if ($1/total_expenses > 0.01) print "EXCEEDS 1%"}'` | STOP. Respond: "Miscellaneous expense exceeds 1% threshold (Rule R6). Break out recurring items into specific GL accounts. Items appearing >3 times in miscellaneous must be assigned dedicated accounts." |
| **R7** | **STOP and flag if intercompany balances are not eliminated before consolidation.** Unreconciled intercompany accounts are the #1 cause of delayed multi-entity closes. | Trigger: Output includes consolidated financials AND `grep -c "intercompany\|elimination\|IC\|due to/from"` across entity trial balances > 0 AND `grep -c "eliminated\|netted\|consolidated"` returns 0 | STOP. Respond: "Consolidation blocked by Rule R7. Intercompany balances detected but no elimination entries found. Reconcile and eliminate all intercompany transactions before consolidation: due to/from, intercompany revenue/expense, intercompany loans." |

## The Expert's Mindset

Master accountants understand that their domain is not about numbers or policies — it's about **enabling human potential and organizational health**. The best work is often invisible: preventing problems, not solving them.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Fundamental attribution error** — attributing outcomes to character rather than context | For every performance issue, ask "what system produced this behavior?" before "what's wrong with this person?" |
| **Recency bias** — evaluating based on the last interaction | Maintain a running log of contributions; review the full record, not the last month |
| **Overconfidence in models** — trusting the spreadsheet more than reality | Every model gets a "what would make this wrong?" section; stress-test assumptions |
| **Similarity bias** — favoring people/approaches that look like you | Audit decisions for pattern: who/what gets approved vs. rejected; look for systemic skew |

### What Masters Know That Others Don't
- **The 20% that causes 80% of issues** — identify and fix the systemic root, not the symptoms
- **When process helps vs. when it suffocates** — the same process that saves a 50-person team destroys a 5-person team
- **The story behind the numbers** — every metric is a proxy for human behavior; understand the behavior, not just the number

### When to Break Your Own Rules
- **Bend policy for the outlier.** Rules are for the 95%. The top 5% need exceptions — give them.
- **Trust intuition when data is noisy.** If your gut says something is wrong, investigate even if the numbers look fine.

## Route the Request

<!-- QUICK: 30s — auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.csv\|*.xlsx", "trial_balance\|general_ledger\|chart_of_accounts\|journal_entry")` OR `file_contains("*.md", "month-end close\|reconciliation\|financial statement\|AP aging\|AR aging")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.pdf\|*.docx", "contract\|MSA\|SLA\|service agreement\|revenue arrangement")` AND `file_contains("*", "ASC 606\|performance obligation\|revenue recognition\|SSP")` | Invoke **legal-advisor** instead. This is contract review — legal determines the contract structure; accounting applies the recognition treatment after. |
| A3 | `file_contains("*.xlsx\|*.csv", "budget\|forecast\|variance\|headcount plan\|board deck")` AND NOT `file_contains("*", "trial_balance\|general_ledger\|reconciliation")` | Invoke **fp-and-a-analyst** instead. This is financial planning & analysis work. |
| A4 | `file_contains("*", "cash flow\|venture debt\|banking\|treasury\|wire\|ACH")` AND NOT `file_contains("*", "reconciliation\|bank rec\|journal entry")` | Invoke **treasury-manager** instead. This is treasury/cash management work. |
| A5 | `file_contains("*", "tax filing\|sales tax\|nexus\|1099\|VAT\|GST\|R&D credit")` | Invoke **compliance-officer** instead. This is tax compliance work. |
| A6 | `file_contains("*", "investor\|fundraise\|data room\|LP\|due diligence")` AND NOT `file_contains("*", "GAAP financials\|audit PBC\|close package")` | Invoke **investor-relations** instead. This is investor communication work. |
| A7 | `file_contains("*", "ASC 606\|revenue recognition\|performance obligation\|SSP\|contract modification\|over-time\|point-in-time")` | Jump to **Decision Trees** — Revenue Recognition Path. |
| A8 | `file_contains("*", "ASC 718\|stock option\|SBC\|black-scholes\|409A\|option grant\|vesting schedule")` | Jump to **Decision Trees** — Equity Accounting. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

What are you trying to do?
├── Set up accounting from scratch → Jump to "Core Workflow > Phase 1: Accounting Setup"
├── Close the books (month-end) → Go to "Core Workflow > Phase 2: Month-End Close"
├── Handle revenue recognition (ASC 606) → Jump to "Decision Trees > Revenue Recognition Path"
├── Set up payroll accounting → Go to "Core Workflow > Phase 3: Payroll & Equity"
├── Account for stock options (ASC 718) → Jump to "Equity Accounting"
├── Manage AP/AR → Go to "Core Workflow > Phase 4: AP/AR & Compliance"
├── Handle sales tax → Jump to "Decision Trees > Sales Tax Nexus"
├── Prepare for an audit → Go to "Core Workflow > Phase 5: Audit Preparation"
├── Choose accounting software → Jump to "Decision Trees > Accounting Tech Stack"
├── Need financial planning/forecasting? → Invoke `fp-and-a-analyst` for budgets, models, and board financials
├── Need cash management or banking? → Invoke `treasury-manager` for cash flow, venture debt, and fraud prevention
├── Need legal/tax advice on revenue recognition? → Invoke `legal-advisor` for contract review and ASC 606 determination
├── Need compliance/regulatory guidance? → Invoke `compliance-officer` for tax filings and regulatory changes
├── Preparing investor financials? → Invoke `investor-relations` to package GAAP financials for investors
└── Don't know where to start? → Run "Core Workflow > Phase 1: Accounting Setup"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Individual cases | Handle standard situations following established policies and frameworks |
| **L2** | Team/Function | Own a function for a team or department; adapt frameworks to context |
| **L3** | Department | Design frameworks and policies for a department; handle exceptions and edge cases |
| **L4** | Organization | Set org-wide strategy for your function; influence C-suite decisions |
| **L5** | Industry | Define best practices adopted across the industry; shape professional standards |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 accountant, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s — scan to decide if this skill fits -->

- Designing a SaaS-specific chart of accounts
- Implementing ASC 606 revenue recognition: performance obligations, SSP, contract modifications
- Setting up expense categorization and accrual accounting
- Running month-end close: reconciliation checklist, flux analysis, financial statement preparation
- Processing payroll accounting: gross-to-net, employer taxes, benefits withholding, journal entries
- Accounting for equity: stock-based compensation under ASC 718, 409A valuations, option expense modeling
- Managing accounts payable and accounts receivable with internal controls
- Handling sales tax compliance: nexus determination, marketplace facilitator laws, international VAT/GST
- Preparing for financial statement audit: PBC list, auditor relationship management, walkthrough preparation
- Selecting and configuring accounting tech: QuickBooks/Xero/Netsuite, Bill.com, Ramp/Brex

### Cross-skills Integration

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | legal-advisor | Entity structure, option plan documents, 409A valuation referral, sales tax nexus opinion — legal framework for accounting treatment |
| **Before** | fp-and-a-analyst | Budget model, headcount plan — baseline for flux analysis (actual vs budget) |
| **This** | accountant | Chart of accounts, month-end close package, GAAP financial statements, payroll entries, equity entries, AP/AR aging, sales tax filings, audit PBC |
| **After** | fp-and-a-analyst | Consumes actuals for variance analysis, reforecasting, and board reporting |
| **After** | treasury-manager | Consumes AP aging, cash position data for cash forecasting and payment runs |
| **After** | compliance-officer | Consumes sales tax filings, 1099 reporting, statutory financials |

Common chains:
- **Month-end close:** accountant → fp-and-a-analyst → ceo-strategist — Actuals → variance analysis → board review
- **Audit cycle:** accountant → auditor (external) → board-manager — PBC → audit report → board presentation
- **Fundraising diligence:** accountant → fp-and-a-analyst → investor-relations — GAAP financials → fundraise model → data room

## Decision Trees

<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### Revenue Recognition Path (ASC 606)

```
What are you selling?
├── SaaS subscription (monthly/annual)
│   └── Recognize ratably over the subscription period.
│       Annual prepay: Dr Cash $120K, Cr Deferred Revenue $120K.
│       Each month: Dr Deferred Revenue $10K, Cr Revenue $10K.
│       Contract modifications (upgrades/downgrades): prospective treatment.
├── SaaS + implementation/setup (bundled)
│   └── Are they distinct performance obligations?
│       ├── YES (customer can use SaaS without your setup help)
│       │   └── Allocate transaction price using SSP. Recognize setup rev at go-live.
│       └── NO  (setup is integral to SaaS functionality)
│           └── Combine into one performance obligation. Recognize ratably.
├── Usage-based pricing (API calls, seats, transactions)
│   └── Recognize as usage occurs. Estimate if you have sufficient data.
│       Constraint: don't recognize revenue you might have to reverse.
└── Professional services
    ├── Fixed fee: Recognize over time if customer receives benefit as you perform.
    └── T&M: Recognize as hours are worked (right to invoice practical expedient).
```

### Sales Tax Nexus Decision

```
Do you have economic nexus in a state?
├── Revenue > threshold (typically $100K-500K) OR transactions > 200?
│   ├── YES → Register in that state. Collect and remit sales tax.
│   └── NO  → No obligation to collect. But monitor quarterly.
├── Physical presence (employees, office, inventory, contractors)?
│   └── YES → Register immediately. Physical nexus always triggers obligation.
└── Selling through a marketplace (AWS Marketplace, Shopify, etc.)?
    └── Marketplace facilitator laws: platform collects/remits, but you still need to register in some states. Confirm with your marketplace.
```

### Accounting Tech Stack Selection

```
What's your stage and complexity?
├── Pre-revenue / < $1M ARR, simple model
│   └── QuickBooks Online Simple Start + Brex/Ramp for cards.
│       Cost: ~$30/mo + card platform. No integrations needed.
├── $1M-$10M ARR, SaaS, multiple revenue streams
│   └── QuickBooks Online Plus/Advanced OR Xero + Bill.com (AP) + Gusto (payroll).
│       Add: SaaS metrics tool (Baremetrics/ChartMogul) for MRR tracking.
│       Cost: ~$500-1,500/mo all-in. Integrate via native connectors.
├── $10M-$50M ARR, multi-entity, ASC 606 complexity
│   └── Netsuite (or Intacct) + Stripe/Chargebee revenue recognition module.
│       Add: Avalara (sales tax), Carta (equity), Expensify (T&E).
│       Cost: ~$3K-8K/mo. Dedicated accounting hire needed.
└── $50M+ ARR, IPO path, SOX readiness
    └── Netsuite/Intacct + full ERP modules + BlackLine (close management).
        Add: FloQast (close checklist), Workiva (SEC reporting).
        Cost: $15K-40K/mo. Controller + accounting team of 3-5.
```

**What good looks like:** Month-end close completed in 5 business days. Every balance sheet account reconciled — the reconciliation sheet shows book balance, bank/statement balance, and every reconciling item with an explanation. Revenue recognition entries are traceable to signed contracts. An auditor can walk into your office unannounced and complete a surprise audit in 2 weeks because everything is already organized.

## Core Workflow

<!-- STANDARD: 3min -->

### Phase 1: Accounting Setup (~2 hours, one-time)
1. **Chart of accounts design.** SaaS-specific structure:
```
1000 Assets
  1100 Cash & Equivalents (1101 Operating, 1102 Money Market, 1103 Restricted)
  1200 Accounts Receivable
  1300 Prepaid Expenses
  1400 Fixed Assets (1410 Equipment, 1415 Accumulated Depreciation)
2000 Liabilities
  2100 Accounts Payable
  2200 Accrued Expenses (2210 Payroll, 2220 Commissions, 2230 Vendor)
  2300 Deferred Revenue (2301 Annual, 2302 Monthly)
  2400 Debt (2410 Venture Debt, 2420 Equipment Financing)
3000 Equity
  3100 Common Stock, 3200 APIC, 3300 Accumulated Deficit
4000 Revenue
  4100 Subscription Revenue, 4200 Professional Services, 4300 Other
5000 COGS
  5100 Hosting, 5200 Customer Support, 5300 Third-Party Fees
6000-9000 Operating Expenses
  6000 S&M, 7000 R&D, 8000 G&A, 8100 SBC (separate line!)
```
2. **Configure accounting system.** Set fiscal year, close periods monthly, enable class/location tracking if multi-entity. Import opening balance sheet.
3. **Set up bank feeds.** Link all bank accounts and credit cards for automatic transaction import. Map recurring transactions to rules.
4. **Document accounting policies** in a 3-5 page memo: revenue recognition policy, expense capitalization threshold ($2,500 typical for startups), prepaid expense policy, accrual policy, equity accounting method.

### Phase 2: Month-End Close (~2-3 days per month)
1. **Day 1-3: Reconciliations.** Reconcile ALL bank and credit card accounts to statements. Reconcile AP to vendor statements (request statements from top 10 vendors by spend). Reconcile AR to customer payment records. Reconcile payroll to Gusto/ADP reports.
2. **Day 3-4: Accruals and adjustments.** Accrue unpaid expenses (commissions, bonuses, vendor invoices not yet received). Amortize prepaid expenses. Depreciate fixed assets. Record revenue recognition entries (deferred revenue unwind). Record SBC expense (options vesting × fair value per period).
3. **Day 4-5: Review and flux analysis.** Compare every P&L line to prior month AND same month prior year. Investigate any variance >10% or >$10K (whichever is larger). Write a 1-2 sentence explanation for each material flux. Prepare balance sheet and P&L in GAAP format.
4. **Day 5: Close the period.** Lock the period in your accounting system. No further entries without controller approval. Distribute financial package to CEO and FP&A.

### Phase 3: Payroll & Equity Accounting (~2 hours per payroll cycle)
1. **Payroll entry:** Dr Salary Expense (gross) + Employer Tax Expense, Cr Cash (net pay), Cr Payroll Tax Payable, Cr Benefits Payable. Never record only the net pay hitting the bank — that understates expenses by 15-25%.
2. **Employer taxes:**

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Cross-Skill Coordination

<!-- NEIGHBORS: Skills this accountant works with — financial data flows across the entire company -->

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `fp-and-a-analyst` | Budget, forecast, variance analysis requests | Monthly close — provide actuals for budget-to-actual comparison |
| `treasury-manager` | Cash position, debt covenants, banking updates | Weekly cash reconciliation; monthly balance sheet tie-out |
| `ceo-strategist` | Fundraising timeline, board deck requirements | Pre-fundraising — GAAP financials and cap table audit |
| `board-manager` | Board meeting schedule, financial reporting requirements | 2 weeks before each board meeting — financial package prep |
| `legal-advisor` | Contract review for ASC 606 implications, equity grant documentation | At contract signing — revenue recognition determination |
| `compliance-officer` | Tax filing deadlines, regulatory changes (nexus, R&D credit) | Monthly — sales tax nexus review; quarterly — estimated tax payments |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `fp-and-a-analyst` | Closed books, actuals by department, ARR schedule, cash flow statement | Delayed close = delayed forecast refresh = stale board materials |
| `treasury-manager` | Cash reconciliation, AP aging, AR aging, payroll register | Treasury can't manage cash without reconciled bank positions |
| `ceo-strategist` | GAAP P&L, balance sheet, cash flow statement, cap table | Fundraising models are garbage without clean historicals |
| `investor-relations` | Quarterly financial reports, SaaS metrics (ARR, NRR, LTV/CAC) | Investor updates without GAAP backing erode LP trust |
| `board-manager` | Financial package: P&L, BS, CF, ARR bridge, burn multiple, runway | Board can't govern without financial visibility |

**Coordination cadence:**
- **Daily:** Scan bank feeds for unusual transactions
- **Weekly:** AP run review with treasury-manager; payroll preview with people-ops
- **Monthly:** Close checklist execution; draft P&L to fp-and-a-analyst by Day 5; final by Day 10
- **Quarterly:** Sales tax nexus review; 409A refresh trigger check; board financial package
- **Annually:** Audit prep (PBC list), 1099 filing, tax return support, insurance renewal

**Decision Gates & Handoff Artifacts:**
- **Close completeness gate:** All 8 reconciliations (bank, credit card, payroll, AP, AR, deferred revenue, fixed assets, equity) complete before P&L draft is shared with `fp-and-a-analyst`. Incomplete reconciliation = stale forecast = wrong board materials.
- **Revenue recognition gate:** Every new contract runs through ASC 606 checklist (license vs service, performance obligations, point-in-time vs over-time recognition) at signing — not at close. Artifact: Signed ASC 606 determination memo per contract.
- **SBC valuation gate:** 409A must be current (within 12 months, or within 90 days of material event). Expired 409A = all option grants at risk of IRS challenge. Artifact: Current 409A report on file.
- **Sales tax nexus gate:** Monthly nexus threshold review across all states with customers. Crossing economic threshold ($100K or 200 transactions) triggers immediate registration. Artifact: Nexus tracker with state-by-state thresholds and current sales.
- **Audit readiness gate:** All PBC (Provided By Client) schedules prepared and organized before auditor arrival. Disorganized PBC = 2x audit fees. Artifact: PBC index with folder structure matching auditor request list.
- **Handoff to `fp-and-a-analyst`:** Closed books with variance commentary by Day 5; final P&L/BS/CF by Day 10. Artifact: Month-end close package with reconciliation proofs.
- **Handoff to `treasury-manager`:** Daily cash reconciliation; weekly AP aging; monthly debt schedule. Artifact: Cash position summary with all bank account balances.
- **Handoff to `investor-relations`:** Quarterly GAAP financials with ARR bridge, NRR calculation, and LTV/CAC. Artifact: Investor-grade financial package with methodology appendix.

## Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| Month-end close approaching and no reconciliation checklist circulated | Proactively publish the close calendar with owner assignments and cutoff dates | Prevents last-minute scrambling and ensures all reconciling items are identified early |
| Intercompany balance exceeds 5% of total intercompany volume | Flag to treasury and initiate bilateral reconciliation before close | Intercompany mismatches compound across entities and delay consolidation |
| More than 3 manual journal entries hitting the same account in a period | Investigate root cause and propose automation or process fix | Repeated manual entries signal a systemic issue that automation can eliminate |
| Accrual reversal not processed by Day 5 of new period | Chase the responsible cost-center owner and escalate if unreversed by Day 7 | Stale accruals distort both current and prior period P&L |
| Foreign currency revaluation rate differs >3% from prior month rate | Alert FP&A and treasury — assess balance sheet exposure impact | Material FX moves can trigger covenant breaches or hedge triggers |
| Fixed asset addition posted to expense account above capitalization threshold | Reclassify immediately and notify fixed asset accountant | Failure to capitalize distorts both EBITDA and depreciation schedules |
| Audit evidence request received without prior notice | Pull requested support within 2 hours and confirm completeness with auditor | Responsiveness builds auditor trust and can reduce substantive testing scope |
| Bank feed disruption >4 hours during business day | Switch to manual import protocol and notify all entities relying on auto-feed | Delayed bank data cascades into cash positioning, reconciliation, and payment runs |

## What Good Looks Like

Month-end close is completed on business day 5. The financial package (P&L, balance sheet, cash flow, flux analysis, SaaS metrics) is distributed before 10 AM. Every reconciliation has a signed-off worksheet with book balance, statement balance, and reconciling items listed individually. An auditor's PBC request is fulfilled by sharing a single organized folder — no files are "being prepared." The deferred revenue waterfall reconciles to the trial balance to the penny. The equity rollforward matches Carta exactly. A new controller starting Monday could take over the close process without a single phone call because everything is documented, labeled, and organized.

## Deliberate Practice

```mermaid
graph LR
    A[Apply<br/>framework] --> B[Observe<br/>outcome] --> C[Reflect on<br/>accuracy] --> D[Calibrate<br/>judgment] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Before making a decision, write down your prediction. After the outcome, compare. Track your calibration. | Weekly |
| **Competent** | Study a past decision that went well AND one that went poorly. What information did you have at the time? | Monthly |
| **Expert** | Design a new framework or model for a recurring challenge in your domain. Test it for 3 months. | Quarterly |
| **Master** | Write a case study that teaches others your decision-making process. Include what you got wrong. | Semi-annually |

**The One Highest-Leverage Activity:** Maintain a decision journal. For every significant decision: what you decided, why, what you expect to happen, and what actually happened.

## Equity Accounting (ASC 718)

<!-- STANDARD: 3min -->

### The 409A → Option Grant → Expense Chain

1. **409A valuation** (every 12 months or after material event): Independent firm determines fair market value of common stock. This sets the strike price for options. Early-stage FMV is typically $0.10-$2.00/share.
2. **Option grant:** Board approves grant with: number of shares, strike price (= 409A FMV), vesting schedule (standard: 4-year, 1-year cliff, monthly thereafter), exercise period (10 years from grant).
3. **Fair value calculation:** Use Black-Scholes or binomial model. Inputs: stock price (= 409A FMV), strike price, expected term (use simplified method if no history: (vesting term + contractual term) / 2), risk-free rate (US Treasury matching expected term), volatility (use public company comparables), dividend yield (0% for startups).
4. **Expense recognition:** Total fair value / vesting period = monthly SBC expense. Dr SBC Expense, Cr APIC. Straight-line over vesting period. For performance-based vesting, assess probability each period.
5. **Option exercises:** Dr Cash (strike × shares), Dr APIC (remaining SBC not yet amortized), Cr Common Stock + APIC. Early exercises (83(b) election) — employee pays tax on spread at exercise, not at liquidity.

**DEEP: 10+min — War story:** A Series B startup got a $2.00/share 409A in January. By June, they had a term sheet at $15/share (Series C). They granted options at the $2.00 strike in July — but didn't get a new 409A. The IRS audited and determined the FMV at grant date was actually $8.00 based on the term sheet progression. Result: all July grants were discounted options with $6/share of compensation income to employees AND a $500K penalty for the company. Rule: new 409A before any option grant where > 6 months since last valuation OR any material event (fundraise term sheet, major customer win, revenue 2x).

## Gotchas

- **Revenue recognition for SaaS** — a customer pays $120K upfront for a 12-month contract. You can't recognize $120K in month 1. ASC 606 requires ratable recognition: $10K/month over 12 months. The $110K you haven't recognized yet sits on the balance sheet as deferred revenue (a LIABILITY, not cash you've earned).
- **Prepaid expenses amortization** — you pay $24K for annual software in January. Only $2K hits January P&L. The remaining $22K is a prepaid asset. If you forget to amortize, Q1 P&L is $18K understated ($2K/month × 9 remaining months), and your runway calculation is wrong.
- **Sales tax nexus** — you registered in Delaware and Texas. But you hired a remote employee in Colorado, and Colorado now considers you to have economic nexus. You owe 2 years of uncollected sales tax + penalties. Nexus is triggered by employees, not just revenue. Every state where you have an employee needs a nexus review.
- **Bank reconciliation** that says "difference = $42.17, immaterial" — but the $42.17 is 12 micro-transactions ($3.51 each) that are actually bank fees you didn't record. Over 12 months, that's $504 in unreported expenses. Immaterial ≠ zero. Track and categorize all differences; don't force-balance.

## Verification

- [ ] Close process: month close completed within 5 business days — all reconciliations done
- [ ] Revenue recognition: deferred revenue schedule reconciled — recognized revenue matches delivery
- [ ] Accounts receivable: AR aging report reviewed — > 90 days past due items have collection plan
- [ ] Tax compliance: sales tax nexus reviewed quarterly for new states (employees, revenue thresholds)
- [ ] Audit readiness: all material balances have supporting schedules with source data references

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)

