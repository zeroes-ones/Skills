---
name: accountant
description: Accounting & bookkeeping for startups — chart of accounts, ASC 606 revenue recognition, month-end close, payroll accounting, equity accounting (ASC 718, 409A), AP/AR, sales tax compliance, audit preparation, and accounting tech stack. Use when setting up accounting for a startup, closing the books, or preparing for an audit.
author: Sandeep Kumar Penchala
type: corporate-finance
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - accounting
  - bookkeeping
  - asc-606
  - asc-718
  - month-end-close
  - audit
  - payroll
  - corporate-finance
token_budget: 3510
output:
  type: "spreadsheet"
  path_hint: "accounting/"
chain:
  consumes_from:
    - fp-and-a-analyst
    - legal-advisor
  feeds_into:
    - fp-and-a-analyst
    - treasury-manager
    - compliance-officer
---

# Accountant — Startup Accounting & Bookkeeping

GAAP-compliant accounting for venture-backed startups. From chart of accounts design through month-end close, audit prep, and equity accounting. Think like a controller who's survived their first Big 4 audit — every entry must be supportable, every reconciliation must tie, and nothing ships without review.

## Ground Rules — Read Before Anything Else

- **Revenue is NOT cash received.** Under ASC 606, you recognize revenue when you satisfy a performance obligation, not when the customer pays. A $120K annual prepay on January 1 = $10K/month revenue for 12 months. The remaining $110K sits on your balance sheet as a liability (deferred revenue).
- **Every entry needs support.** If an auditor can't trace a journal entry to a source document (contract, invoice, bank statement, payroll report, option grant) in under 3 minutes, it's not supportable. No support = no entry.
- **Accrual basis only, from day 1.** Cash-basis accounting will kill you at your first fundraise or diligence process. Convert now. The rule: recognize revenue when earned, expenses when incurred, regardless of cash timing.
- **SBC is a real expense with real dilution.** Stock-based compensation hits your P&L under ASC 718. The fair value of options at grant date is expensed over the vesting period. Ignoring it doesn't make it free — it just makes your financials wrong.
- **Reconcile everything, every month.** Bank accounts, credit cards, payroll, AP, AR, deferred revenue, fixed assets, equity — all 8 must be reconciled within 10 business days of month-end. An unreconciled balance sheet is not a balance sheet.

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

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
└── Don't know where to start? → Run "Core Workflow > Phase 1: Accounting Setup"

Do not read the entire skill. Follow the route above and read only the sections it points to.

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
2. **Employer taxes:** Social Security 6.2% (up to wage base $168,600 for 2026), Medicare 1.45% (no cap), FUTA 0.6% (on first $7,000), SUTA (varies by state, typically 2-4% on first $10K-30K).
3. **Benefits accounting:** Health insurance premiums, 401(k) match, life insurance, commuter benefits — each posts to the P&L as benefits expense AND to the balance sheet as a payable until remitted.
4. **Contractor vs employee:** Misclassifying an employee as a 1099 contractor triggers IRS penalties ($50+ per form), back taxes, and potential class-action lawsuits. Use the IRS 20-factor test. When in doubt, classify as W-2.

### Phase 4: AP/AR & Compliance (~30 min daily)
1. **AP process:** Invoice received → 3-way match (PO, receiving report, invoice) → approval per delegation of authority → payment per terms. Net-30 is standard. Never pay without approval — segregation of duties: the person who approves cannot be the person who enters the invoice or initiates payment.
2. **AR process:** Invoice upon contract signing. Follow up at net-15 (friendly reminder), net-30 (call), net-45 (escalate to sales rep), net-60 (stop service threat). SaaS companies that bill annually should have DSO < 15 days.
3. **1099 tracking:** Any US contractor paid >$600 in a calendar year gets a 1099-NEC. Collect W-9 before first payment — chasing contractors for W-9s in January is a nightmare. File by January 31.
4. **Sales tax:** File monthly or quarterly per each state's schedule. Use Avalara/TaxJar to automate rates and filing. Never manually calculate sales tax rates — rate tables change quarterly and manual errors trigger audits.

### Phase 5: Audit Preparation (~2-3 weeks before fieldwork)
<!-- DEEP: 10+min — real audit horror stories and what they cost -->
1. **PBC list.** Auditors will request: trial balance, general ledger detail, bank reconciliations (all 12 months), AP/AR aging, fixed asset rollforward, debt agreements, equity transactions (board consents, 409A reports, option grants), revenue contracts (sample of top 20 by value), payroll reports, sales tax filings, minutes from all board meetings.
2. **Prepare supporting schedules.** For every material balance sheet line, create a rollforward: Beginning Balance + Additions - Deductions = Ending Balance. Tie to the trial balance.
3. **Revenue walkthrough.** Prepare a memo walking through a sample customer contract from signature → invoicing → cash receipt → revenue recognition → deferred revenue tracking. Show your ASC 606 analysis for each performance obligation.
4. **Equity rollforward.** List every option grant, exercise, and forfeiture during the audit period. Tie grant dates and fair values to board consents and 409A reports. Reconcile fully diluted share count.
5. **Pre-audit meeting.** Walk the auditor through your business model, accounting policies, internal controls, and any unusual transactions. Asking "what would you flag?" before fieldwork starts saves weeks of back-and-forth.

## Equity Accounting (ASC 718)
<!-- STANDARD: 3min -->

### The 409A → Option Grant → Expense Chain

1. **409A valuation** (every 12 months or after material event): Independent firm determines fair market value of common stock. This sets the strike price for options. Early-stage FMV is typically $0.10-$2.00/share.
2. **Option grant:** Board approves grant with: number of shares, strike price (= 409A FMV), vesting schedule (standard: 4-year, 1-year cliff, monthly thereafter), exercise period (10 years from grant).
3. **Fair value calculation:** Use Black-Scholes or binomial model. Inputs: stock price (= 409A FMV), strike price, expected term (use simplified method if no history: (vesting term + contractual term) / 2), risk-free rate (US Treasury matching expected term), volatility (use public company comparables), dividend yield (0% for startups).
4. **Expense recognition:** Total fair value / vesting period = monthly SBC expense. Dr SBC Expense, Cr APIC. Straight-line over vesting period. For performance-based vesting, assess probability each period.
5. **Option exercises:** Dr Cash (strike × shares), Dr APIC (remaining SBC not yet amortized), Cr Common Stock + APIC. Early exercises (83(b) election) — employee pays tax on spread at exercise, not at liquidity.

**DEEP: 10+min — War story:** A Series B startup got a $2.00/share 409A in January. By June, they had a term sheet at $15/share (Series C). They granted options at the $2.00 strike in July — but didn't get a new 409A. The IRS audited and determined the FMV at grant date was actually $8.00 based on the term sheet progression. Result: all July grants were discounted options with $6/share of compensation income to employees AND a $500K penalty for the company. Rule: new 409A before any option grant where > 6 months since last valuation OR any material event (fundraise term sheet, major customer win, revenue 2x).

## Best Practices
<!-- STANDARD: 3min -->
<!-- DEEP: 10+min — practices forged from audit findings, IRS notices, and restatements -->

- **Close monthly, not quarterly.** A 3-month gap in reconciliations means 90 days of errors compounding. By the time you find a problem, you've been making decisions on wrong numbers for a quarter.
- **Separate duties.** The person who opens the mail should NOT record cash receipts. The person who approves invoices should NOT enter them. The person who reconciles the bank should NOT sign checks. At < 5 people, the CEO reviews all disbursements as compensating control.
- **Deferred revenue is sacred.** Never recognize deferred revenue to "smooth" earnings. That's not smoothing — it's fraud. ASC 606 is clear: performance obligation satisfied = revenue recognized. Period.
- **Accrue as you go, not at quarter-end.** If you know about a vendor invoice or a commission payment, accrue it in the same month the expense was incurred. "We'll catch it next month" creates a rolling error that never gets fixed.
- **Document your policies in writing.** If it's not written down, it doesn't exist for audit purposes. An accounting policy memo (5 pages, signed by CEO) saves 20+ hours of auditor Q&A.
- **SBC is an expense — show it separately.** Put SBC on its own P&L line, not buried in department opex. Investors and acquirers will calculate EBITDA - SBC anyway. Transparency builds trust.
- **Reconcile equity quarterly with Carta.** The cap table in Carta/Pulley must match your balance sheet. Founders issuing side letters for "extra equity" without updating the cap table is the #1 cause of equity reconciliation nightmares.
- **Sales tax nexus monitoring is ongoing.** Your obligation changes when you hire a remote employee in a new state, open an office, exceed a state's revenue threshold, or attend a trade show. Review nexus quarterly.
- **1099s are January 31, not "whenever you get around to it."** Late filing penalty: $60/form (up to $630/year for small businesses). Intentional disregard: $630/form, no cap. The IRS does not accept "we were busy fundraising" as an excuse.
- **Your auditor is not your accountant.** Auditors test what you've done. They do not prepare your financials, fix your reconciliations, or tell you what entries to make. Going into an audit with messy books costs 3-5x more in audit fees.

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

## Error Decoder
<!-- QUICK: 30s — exact error → root cause → fix -->
<!-- DEEP: 10+min — each error is a war story from real startup accounting failures -->

| Error / Symptom | Root Cause | Fix |
|----------------|------------|-----|
| Balance sheet doesn't balance | Retained earnings not updated, intercompany entries not eliminated, or a journal entry only hit one side | Start at the trial balance. Check that total debits = total credits. Then check retained earnings: Ending RE = Beginning RE + Net Income - Dividends. Use a checklist: each JE must have equal debits and credits before posting. |
| Deferred revenue balance growing but revenue flat | Annual prepays not being unwound monthly | Set up a recurring JE: Dr Deferred Revenue, Cr Revenue for each active contract's monthly recognized amount. Build a deferred revenue waterfall schedule: contract start, end, total value, recognized to date, remaining. |
| Bank rec won't tie after 3 attempts | Deposits in transit or outstanding checks from prior period not cleared, OR bank feed imported transactions twice | Print last month's final reconciliation. Check each reconciling item — did it clear this month? If a deposit "in transit" from last month never hit the bank, it was never deposited. Investigate. |
| Payroll expense on P&L ≠ cash paid to employees | Employer taxes, benefits, and accruals not posted | JE must include: Dr Salary (gross), Dr Employer Tax, Dr Benefits Exp → Cr Cash (net pay), Cr Tax Payable, Cr Benefits Payable. The difference between total debits and net pay = employer burden. It should be 12-18% of gross salary for US-based employees. |
| SBC expense missing from P&L | Options not being valued or amortization schedule not set up | Build an option amortization schedule: grant date, shares, fair value per share, total value, vesting start, vesting end, monthly amort = total value / vesting months. Sum across all grants = monthly SBC expense. |
| Sales tax notice from a state you've never heard of | Nexus triggered without your knowledge — remote employee, trade show, or revenue threshold crossed | First: don't ignore it. Second: determine first date of nexus. File voluntary disclosure agreement (VDA) if available — reduces penalty and limits lookback period. Third: register going forward. |
| Audit fee 2x what you budgeted | Books not audit-ready — auditor spending time doing accounting work instead of auditing | Pre-audit: reconcile everything, prepare all schedules, document all policies. Submit PBC in one organized folder, not drip-fed over 6 weeks. Estimated fees assume clean books. Messy books = change order. |

### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| P&L doesn't tie to bank balance | Accrual accounting entries not reconciled | Run a monthly variance report: net income (accrual) vs cash flow from operations (cash). Every variance >5% needs a reconciling item identified. If accruals consistently drift from cash, review your revenue recognition and deferred revenue entries. |
| Board questions ARR calculation | SaaS metrics not defined with clear methodology | Document your SaaS metric calculation methodology: what counts as ARR (annualized recurring revenue, not one-time), how expansion/contraction/churn are attributed, and how multi-year contracts are counted. Publish this as a board appendix. |
| Fundraising model doesn't match historicals | Model was built forward-only, not reconciled backwards | Every fundraising model must start by reproducing the last 12 months of actuals within 5%. If it can't explain the past, it can't predict the future. Reconcile model vs actuals before presenting to investors. |
| Cash runway suddenly shorter than expected | 13-week cash flow not maintained | Update the 13-week cash flow forecast every Friday afternoon. If actual cash differs from forecast by >15% in any week, investigate the variance source. Key driver: AR timing vs actual collections — always track DSO. |
| Sales tax notice from a state you don't operate in | Economic nexus triggered by remote sales | Use a sales tax automation tool (TaxJar/Avalara). Monitor nexus thresholds in every state where you have customers. File in states where you have physical presence AND states where you cross economic nexus thresholds ($100K or 200 transactions). |
| Audit reveals material weakness in revenue recognition | ASC 606 review not done at contract signing | Every contract must go through an ASC 606 checklist at signing: is it a license or a service? Are there performance obligations? Is revenue recognized over time or at a point in time? Involve accounting in the deal review process, not after the contract is signed. |
| Cap table error discovered during fundraising | Stock ledger not maintained after every equity event | Update the cap table after every: funding round, option grant, option exercise, transfer, repurchase, and conversion. Use a platform (Carta/Pulley) — a spreadsheet cap table will have errors by the time you have >5 equity holders. |


## Production Checklist
<!-- QUICK: 30s — all must pass before month-end close is "done" -->

- [ ] **[S1]** All bank and credit card accounts reconciled to statements — no unexplained differences
- [ ] **[S2]** Deferred revenue waterfall ties to contract listing — every active contract has a schedule
- [ ] **[S3]** AP aging reviewed — nothing > 90 days past due without an explanation
- [ ] **[S4]** AR aging reviewed — collection action taken on anything > 60 days
- [ ] **[S5]** Fixed asset rollforward prepared — additions, disposals, depreciation all supported
- [ ] **[S6]** Payroll reconciled to Gusto/ADP — gross pay, employer taxes, benefits all match
- [ ] **[S7]** SBC amortization schedule updated — new grants added, forfeitures removed, expense posted
- [ ] **[S8]** Sales tax filings submitted for all registered jurisdictions — filing dates confirmed
- [ ] **[S9]** 1099 tracking current — W-9s collected from all US contractors
- [ ] **[S10]** Flux analysis written — every P&L line > 10% variance vs prior month has explanation
- [ ] **[S11]** Accounting period locked — no further entries without controller approval
- [ ] **[S12]** Financial package distributed: P&L, balance sheet, cash flow statement, flux analysis
- [ ] **[S13]** Equity reconciliation: Carta/Pulley cap table matches balance sheet equity accounts
- [ ] **[S14]** Accounting policies memo reviewed and signed by CEO within last 12 months

## What Good Looks Like

Month-end close is completed on business day 5. The financial package (P&L, balance sheet, cash flow, flux analysis, SaaS metrics) is distributed before 10 AM. Every reconciliation has a signed-off worksheet with book balance, statement balance, and reconciling items listed individually. An auditor's PBC request is fulfilled by sharing a single organized folder — no files are "being prepared." The deferred revenue waterfall reconciles to the trial balance to the penny. The equity rollforward matches Carta exactly. A new controller starting Monday could take over the close process without a single phone call because everything is documented, labeled, and organized.

## Scale Depth
<!-- QUICK: 30s -- how this skill changes as the company grows -->

| Stage | Scope | Focus | Key Difference |
|-------|-------|-------|----------------|
| **Solo** | Outsourced bookkeeping, tax prep by CPA firm | Stay compliant, don't get fined | External bookkeeper does monthly recs; founder reviews P&L; minimal process |
| **Startup** | First in-house accountant, QuickBooks/Xero, month-end close | Build internal capability, reliable financials | Dedicated accountant; close process defined; basic internal controls |
| **Scale-up** | Finance team (staff accountant, AP/AR, payroll), ERP migration | Scale the function, prepare for audit | Segregation of duties; NetSuite/Intacct; formal close calendar; flux analysis |
| **Enterprise** | Controller + audit committee, SOX/internal controls, GAAP expertise | Public-company readiness, audit defense | Controller org; external audit; SEC reporting readiness; ASC 606 mastery |

## References
<!-- QUICK: 30s — deeper reading and templates -->

- **Templates:** `assets/chart-of-accounts-saas.xlsx` — SaaS-specific chart of accounts, ready to import into QuickBooks/Xero
- **Templates:** `assets/month-end-close-checklist.xlsx` — 50-item close checklist with signoff columns and flux thresholds
- **Templates:** `assets/deferred-revenue-waterfall.xlsx` — Contract-level deferred revenue schedule with automated monthly unwind
- **Templates:** `assets/payroll-je-template.xlsx` — Payroll journal entry template with employer burden calculator
- **References:** `references/asc-606-saas-guide.md` — Revenue recognition for SaaS: performance obligations, SSP, contract modifications, practical expedients
- **References:** `references/asc-718-equity-guide.md` — Stock-based compensation accounting: 409A, Black-Scholes inputs, amortization schedules, modification accounting
- **References:** `references/sales-tax-nexus-guide.md` — State-by-state economic nexus thresholds, marketplace facilitator rules, international VAT/GST primer
- **References:** `references/audit-pbc-checklist.md` — Complete PBC list with examples, timing, and common auditor follow-up questions
- **Books:** Accounting for SaaS (Ben Murray/The SaaS CFO), GAAP Guide, PPC's Guide to Audits of Small Businesses
- **Related skills:** `fp-and-a-analyst` (financial modeling and SaaS metrics), `treasury-manager` (cash management and banking), `compliance-officer` (regulatory filings), `legal-advisor` (entity structure and option plans)
