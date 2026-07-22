---
name: treasury-manager
description: Treasury & cash management for startups — 13-week cash flow, banking relationships, investment policy, venture debt, foreign exchange, payment operations, fraud prevention, insurance management, cap table operations, and liquidity planning. Use when managing startup cash, setting up banking, or navigating a cash crunch.
author: Sandeep Kumar Penchala
type: corporate-finance
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - treasury
  - cash-management
  - banking
  - venture-debt
  - fraud-prevention
  - insurance
  - cap-table
  - corporate-finance
token_budget: 3480
output:
  type: "spreadsheet"
  path_hint: "treasury/"
chain:
  consumes_from:
    - ceo-strategist
    - fp-and-a-analyst
    - legal-advisor
  feeds_into:
    - fp-and-a-analyst
    - accountant
    - board-manager
---

# Treasury Manager — Startup Cash & Risk Operations

Treasury, cash management, and financial risk for venture-backed startups. From daily cash positioning through venture debt negotiation, fraud prevention, and liquidity crisis management. Think like a CFO who's managed a company through a bank failure and a cash crunch — paranoia about cash is a job requirement.

## Ground Rules — Read Before Anything Else

- **Cash is the company's heartbeat.** You can have great revenue growth, happy customers, and a strong team — and still be dead in 60 days if you don't manage cash. The P&L tells a story; the bank account tells the truth.
- **Never concentrate all cash in one bank.** The SVB collapse (March 2023) proved this. Maintain at least 2 banking relationships. Operating cash in one, reserves in another. At minimum: split across banks so each balance stays under FDIC insurance limits ($250K per account ownership category, with sweep programs for excess).
- **Fraud is not "if" — it's "when."** Social engineering attacks target startups because they have money and weak controls. Every payment above a threshold ($10K for seed, $50K for growth) requires dual approval. No exceptions, no "the CEO is traveling so I'll approve it this one time."
- **Insurance is not optional after your first fundraise.** Board members, investors, and enterprise customers will require D&O, E&O, cyber, and general liability coverage. Operating without D&O insurance means directors are personally liable — good luck recruiting a board.
- **Venture debt amplifies outcomes — both ways.** It extends runway without dilution, but it's senior to equity in liquidation. If you borrow $5M and can't repay, the lender owns your company, not you. Model worst-case: what happens if you draw the full facility and revenue drops 50%?

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

What are you trying to do?
├── Manage daily cash → Jump to "Core Workflow > Phase 1: Daily Cash Operations"
├── Build a 13-week cash flow forecast → Go to "Core Workflow > Phase 2: Cash Forecasting"
├── Set up banking relationships → Jump to "Decision Trees > Banking Setup by Stage"
├── Evaluate venture debt → Go to "Decision Trees > Venture Debt Decision"
├── Create an investment policy → Jump to "Core Workflow > Phase 3: Investment & Debt"
├── Set up fraud prevention → Go to "Core Workflow > Phase 4: Controls & Fraud Prevention"
├── Handle foreign exchange → Jump to "Foreign Exchange Operations"
├── Buy insurance → Go to "Decision Trees > Insurance Coverage"
├── Manage the cap table → Jump to "Cap Table Operations"
├── Survive a cash crunch → Go to "Core Workflow > Phase 5: Liquidity Crisis"
└── Don't know where to start? → Run "Core Workflow > Phase 1: Daily Cash Operations"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## When to Use
<!-- QUICK: 30s — scan to decide if this skill fits -->

- Setting up daily cash management: cash position tracking, payment batching, bank account structure
- Building a 13-week cash flow forecast with weekly granularity
- Establishing startup banking relationships: SVB/First Republic alternatives (JPM, FRB, Mercury, Brex)
- Evaluating and negotiating venture debt, equipment financing, or revolving credit facilities
- Creating an investment policy for excess cash: short-term instruments, yield optimization, FDIC/SIPC limits
- Managing foreign exchange: multi-currency operations, hedging strategy, intercompany transfers
- Designing payment operations: ACH, wire, virtual cards, payment approval workflows
- Building fraud prevention controls: positive pay, ACH blocks/debits, segregation of duties, social engineering defense
- Managing insurance: D&O, E&O, cyber, key person, general liability, workers' comp
- Operating the cap table: Carta/Pulley, 409A coordination, option exercises, secondary transactions
- Liquidity planning: runway extension strategies, cash conservation mode, emergency fundraising

### Cross-skills Integration

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | fp-and-a-analyst | Cash burn forecast, headcount model, revenue projections — inputs to cash forecasting |
| **Before** | ceo-strategist | Fundraising timeline, strategic priorities, risk tolerance — context for treasury decisions |
| **Before** | legal-advisor | Debt term sheets, insurance policy review, entity structure — legal framework for treasury operations |
| **Before** | accountant | AP aging, AR aging, payroll schedule — cash outflow timing data |
| **This** | treasury-manager | 13-week cash forecast, banking structure, investment policy, debt agreements, fraud controls, insurance coverage, cap table management, liquidity plan |
| **After** | fp-and-a-analyst | Consumes actual cash balances, debt service schedules, and interest income for model updates |
| **After** | accountant | Consumes bank statements, payment confirmations, debt amortization schedules for reconciliations |
| **After** | board-manager | Consumes cash runway analysis, risk register, insurance summary for board packages |

Common chains:
- **Cash crisis:** fp-and-a-analyst → treasury-manager → ceo-strategist → board-manager — Burn forecast → 13-week cash flow → go/no-go decisions → board communication
- **Fundraise close:** ceo-strategist → treasury-manager → accountant — Wire received → bank allocation → investment sweep → journal entries
- **Venture debt:** fp-and-a-analyst → treasury-manager → legal-advisor → accountant — Runway model → term sheet negotiation → loan docs → liability recording

## Decision Trees
<!-- QUICK: 30s — follow the ASCII tree to your scenario -->

### Banking Setup by Stage

```
What's your stage?
├── Pre-seed / Incorpating
│   └── Mercury or Brex. No minimums, instant setup, FDIC sweep included.
│       Open a second account at a different bank for reserves. Keep it simple.
├── Seed / $1-5M raised
│   └── Primary: SVB/FRB/JPM (relationship lender for startups).
│       Secondary: Mercury/Brex for operations. Reserve: separate bank.
│       Negotiate: no account fees, free wires (volume-based), sweep accounts.
├── Series A / $5-20M raised
│   └── Primary: JPM/SVB/FRB with treasury management portal.
│       Set up: positive pay, ACH positive pay, wire templates, dual approval.
│       Investment account: ICS/CDARS for FDIC coverage above $250K. Or direct T-bills.
└── Series B+ / $20M+ raised
    └── Multi-bank structure: operating (JPM), reserve (2nd bank), international (if needed).
        RFP treasury services every 2 years. Banks get complacent with locked-in customers.
        Add: credit facility (revolver), FX hedging line, commercial card program.
```

### Venture Debt Decision

```
Should you take venture debt?
├── Have you raised equity in the last 6 months?
│   ├── NO → Most venture debt requires recent equity round. Wait.
│   └── YES → Do you have 6+ months of runway remaining?
│       ├── NO  → Lenders want to see 6-12 months runway. They don't lend to dying companies.
│       └── YES → What's the purpose?
│           ├── Extend runway 6-12 months without dilution → GOOD reason. Proceed.
│           ├── Bridge to profitability → REASONABLE. Model carefully: will you actually reach breakeven?
│           ├── Acquisition financing → OK with LOI. Risky without one.
│           └── "Just because it's available" → TERRIBLE reason. Debt is not free money.
```

Venture debt terms to expect at Series A/B: 20-30% of last equity round, 3-4 year term, interest-only for 12 months, Prime + 2-5% (or SOFR + 5-8%), warrants for 5-15% of loan value. Total cost of capital: 15-25% APR when including warrants. Compare to cost of equity dilution at your current valuation.

### Insurance Coverage Decision

```
What's your risk profile?
├── Any outside investors? → D&O insurance REQUIRED.
│   Policy size: $1M (seed), $2-3M (Series A), $5M+ (Series B+).
│   Key coverage: Side A (non-indemnifiable loss), Side B (corporate reimbursement), Side C (entity coverage for securities claims).
├── Enterprise customers? → E&O (Errors & Omissions) + Cyber REQUIRED.
│   Cyber: $1M minimum. E&O: $1-2M. Enterprise customers will ask for certificates.
├── Handling customer data? → Cyber insurance REQUIRED.
│   Covers: breach response, forensics, notification costs, regulatory fines, business interruption.
│   Underwriters will ask: do you have MFA? Encryption at rest? Penetration testing cadence?
├── Physical office? → General liability + Workers' comp REQUIRED.
│   General liability: $1M per occurrence, $2M aggregate. Workers' comp: statutory.
├── Founder is critical to revenue? → Key person insurance.
│   Term life on founder for 3-5x annual revenue or last round size. Company is beneficiary.
└── Holding 409A-valued stock? → Consider: personal umbrella policy for officers.
```

**What good looks like:** Cash forecast updated every Monday by 10 AM showing actual vs. forecast for prior week, reforecast for next 12 weeks. All bank accounts visible on a single dashboard with current balance, available balance, and FDIC/SIPC coverage status. Payment run happens twice weekly (Tuesday/Thursday), all payments above threshold have dual approval. Insurance certificates are issued within 24 hours of a customer request. You could survive your primary bank failing without missing payroll.

## Core Workflow
<!-- STANDARD: 3min -->

### Phase 1: Daily Cash Operations (~15 min/day)
1. **Morning cash position.** Log into all bank portals (or use a treasury aggregator like Trovata). Record: prior day ending balance, current available balance, any unusual transactions. Compare to forecast. Flag variance > 5% immediately.
2. **Payment review.** Review all payments scheduled for the day. Confirm: each has approval per delegation of authority, beneficiary matches invoice/contract, amount matches approval, no duplicate payments. BATON PASS: if the approver is on PTO, their backup must approve — never skip the control.
3. **Fraud scan.** Check for: unexpected wire requests, vendor bank change requests (call the vendor on a known number to verify), checks clearing out of sequence, ACH debits from unknown originators. Any red flag = stop and investigate.
4. **Sweep excess cash.** If operating account exceeds 2 months of burn, sweep to interest-bearing reserve account or T-bill ladder. Cash sitting in checking earns 0% — that's a negative real return of ~3-4%.

### Phase 2: Cash Forecasting (~2 hours/week)
1. **13-week rolling forecast, updated weekly.** Columns: Week 1-13 as columns. Rows: Beginning Cash + Cash Inflows (customer collections, interest income, tax refunds) - Cash Outflows (payroll, vendor payments, rent, debt service, taxes, one-time items) = Net Cash Flow → Ending Cash.
2. **Cash inflows.** AR aging → expected collection dates based on customer payment history. New sales pipeline × probability × typical collection lag. NOT: "we'll collect everything that's due" — apply historical collection rate (e.g., 85% within terms, 10% within 15 days late, 5% beyond).
3. **Cash outflows.** Payroll: exact dates from payroll calendar (semi-monthly or bi-weekly). Rent: contract date. Vendors: AP aging → due dates. Annual items spread evenly: insurance premiums, software subscriptions, audit fees. Payroll is the KILLER — one payroll cycle is typically 15-20% of monthly burn. Never let cash drop below 2 payroll cycles.
4. **Variance analysis.** Each week, compare actual ending cash to forecast. Investigate variance > 5%. Root causes: customer paid late (AR aging problem), vendor billed earlier than expected (AP timing), revenue collected slower (sales or billing issue), unexpected expense (emergency — should be rare).

### Phase 3: Investment & Debt (~3 hours/month)
1. **Investment policy document (1-2 pages).** Objectives: capital preservation, liquidity, yield (in that order). Permitted instruments: US Treasury bills (< 6 month maturity), government money market funds (NAV $1.00, S&P AAAm rated), FDIC-insured deposits. Prohibited: corporate bonds, equities, crypto, anything with principal risk. Approval: CEO + CFO for any new instrument type.
2. **T-bill ladder.** $1M across 4-week, 8-week, 13-week, and 17-week bills in equal tranches. As each matures, reinvest at the longest duration OR pull to operating if cash is tight. Use TreasuryDirect (free) or your bank's portal ($25-50/trade).
3. **Venture debt compliance.** Monthly reporting to lender: cash balance, ARR, burn rate, financial covenants (typically: minimum cash of 50% of loan balance, maximum burn of X/month). Miss a covenant and don't notify = potential default, even if you cure it. Set calendar reminders 5 days before each reporting deadline.
4. **Venture debt modeling.** Model what happens in worst case: company value drops below debt value → lender recap scenario. Creditors get paid first in any liquidation. Your $5M venture debt facility could wipe out common stock entirely. Board must understand this before signing.

### Phase 4: Controls & Fraud Prevention (~1 hour/week + ongoing)
<!-- DEEP: 10+min — social engineering war stories and real fraud costs -->
1. **Payment controls.** ACH: dual approval for all payments > $10K. Wire: dual approval + callback verification for ALL wires (call beneficiary using number from independent source, not from the email requesting the wire). Checks > $25K: two signatures. Virtual cards: single-use with spend limit and merchant lock.
2. **Bank account controls.** Positive pay: transmit check issue file to bank daily — bank only pays checks matching your file. ACH positive pay: pre-authorize ACH originators; block all others. ACH debit block on accounts that only send funds (reserve accounts). Set up alerts for: balance < threshold, wire sent, ACH batch > $X.
3. **Social engineering defense.** THE THREAT: Email from "CEO" to finance: "Urgent wire $50K to close acquisition. Details attached. Can't talk, in board meeting." THE DEFENSE: (a) All wire requests require verbal confirmation on a KNOWN number — never the number in the email. (b) CEO knows: they must follow the process too. No exceptions for urgency. (c) Quarterly phishing tests for the team.
4. **Segregation of duties.** Payment initiation ≠ Payment approval ≠ Bank reconciliation. At < 10 people, the CEO is the compensating control: reviews all disbursements weekly. At > 25 people, formalize: AP clerk enters, controller approves, CFO releases, someone else reconciles.

### Phase 5: Liquidity Crisis (~intensive, 1-2 weeks)
<!-- DEEP: 10+min — cash crisis playbook from founders who survived -->
1. **Triage.** Calculate: current cash + committed inflows / weekly net burn = weeks of life. If < 12 weeks: emergency mode. If < 8 weeks: existential threat. Immediately: freeze all non-essential spending. Cancel all vendor auto-payments — switch to manual approval only.
2. **Cash conservation.** Prioritize: payroll (required by law), critical vendors (hosting, security), debt service (default = acceleration), insurance (cancelation = board liability). Defer: non-critical vendors (negotiate payment plans), new hires (freeze), marketing spend (pause), office expenses (eliminate).
3. **Receivables acceleration.** Call top 10 customers by AR balance. Offer: 5% discount for payment within 7 days. Every dollar collected this week is worth 2x a dollar collected in 90 days when you might not exist.
4. **Liquidity options.** (a) Existing investor bridge: inside round, 90-day close, 20% discount. (b) Venture debt draw (if facility available). (c) Revenue financing (Pipe, Capchase — expensive but fast). (d) AR factoring (sell receivables at 80-90 cents on dollar). (e) Reduce burn: layoffs, office closure, salary cuts (last resort).
5. **Communication.** Notify board within 48 hours of entering crisis mode. Provide: cash balance, weekly burn, cash-out date, requested bridge amount, plan to extend runway. Bad news does not improve with age.

## Foreign Exchange Operations
<!-- STANDARD: 3min -->

For startups with multi-currency operations (international customers, overseas team, foreign subsidiaries):

1. **Account structure.** Local currency accounts for major markets (EUR, GBP, JPY, AUD). Use a provider like Airwallex, Wise Business, or your primary bank's multi-currency offering. Avoid: PayPal for anything > $10K — their FX spread is 3-4% (hidden).
2. **FX exposure measurement.** Net exposure per currency = (assets - liabilities) in that currency. Cash held in EUR + EUR AR - EUR AP - EUR payroll = EUR net exposure. Forecast exposure at least 90 days out.
3. **Hedging policy.** For < $1M exposure: natural hedging only (match EUR revenue with EUR expenses — pay European employees from EUR account). For $1M-10M: forward contracts for 50% of forecasted exposure, 90-day horizon. For $10M+: systematic hedging program with 50-75% coverage, rolling 12-month horizon.
4. **Intercompany transfers.** Document every transfer: purpose, exchange rate used, tax implications. Intercompany loans require arm's-length interest rates (AFR). Transfer pricing documentation is a tax requirement — your tax return asks about intercompany transactions. Get it right the first time.

<!-- DEEP: 10+min — War story: --> A startup had $2M in a GBP-denominated account earned from UK customers. They left it there for 18 months without hedging, planning to use it for a UK office expansion. Brexit transition ended, GBP/USD dropped from 1.35 to 1.15 — a 15% loss. Their $2M became $1.7M. Cost: $300K lost, their entire UK office budget. Fix: should have converted to USD immediately upon receipt if the liability (office costs) wasn't certain. FX speculation is not a startup's business — convert to functional currency unless you have a matched liability.

## Cap Table Operations
<!-- STANDARD: 3min -->

1. **Platform.** Carta or Pulley — both automate 409A, option exercises, and scenario modeling. If you're still using a spreadsheet at Series A, you're doing it wrong. Cost: $2K-8K/year depending on stakeholder count.
2. **409A coordination.** Carta/Pulley can manage the 409A process end-to-end with a valuation provider. Refresh every 12 months, plus after any material event that could change FMV (new round term sheet, major customer win/loss, revenue 2x from prior period).
3. **Option exercises.** When an employee exercises: verify they have vested shares, verify strike price payment, issue shares, update cap table, file 83(b) election within 30 days (employee responsibility, but you should remind them — mail it certified, return receipt requested). Track exercise windows post-termination (typically 90 days — this is a negotiating point).
4. **Secondary transactions.** At Series B+, employees with > 3 years tenure may want liquidity. Tender offer: company (or investor) buys shares from employees at current 409A or preferred price. Process: board approval, 20-day offer period, pro-rata if oversubscribed. Legal cost: $30K-75K per tender. Tax: employees pay capital gains (long-term if held > 1 year).
5. **Scenario modeling.** For every fundraising scenario, model dilution at multiple valuations. Show: fully diluted shares outstanding, option pool size, new money shares, founder ownership %, employee ownership %. The cap table doesn't lie — if founders own 15% at Series C and want 10%, every percentage point you give away today is gone forever.

## Best Practices
<!-- STANDARD: 3min -->

- **Cash forecast is a living document, not a quarterly exercise.** Update it every Monday morning. The company that updates cash forecasts weekly catches problems 13x faster than the company that updates quarterly.
- **Payroll is sacred.** Never risk payroll. Maintain at minimum 2 payroll cycles of cash in your operating account at all times. If cash forecasting shows you might miss payroll in 6 weeks, you have 4 weeks to solve it. Notify the board at week 2, not week 5.
- **Two banks, always.** Since March 2023, every startup knows why. Operating + reserve in separate institutions. If one bank freezes your account (fraud flag, KYC review, bank failure), you can still make payroll from the other.
- **Fraud controls are non-negotiable.** Every startup that skipped dual approval "because we're small and trust each other" eventually got defrauded. The average BEC (business email compromise) loss is $125K. Startups don't recover from that.
- **Venture debt is an extension, not a substitute for equity.** The rule: debt / last equity round ≤ 25%. Higher than that and you're over-levered. The lender knows your burn rate — they sized the facility knowing exactly when you'll run out. That's their leverage.
- **Insurance is cheaper than the absence of insurance.** D&O for a seed-stage company: $2K-5K/year. One shareholder lawsuit without D&O: board members paying legal fees personally until settlement. Nobody joins your board without D&O.
- **CBDDO: Constant Bank Due Diligence on Operations.** Review bank fees quarterly. Banks increase fees on dormant accounts. ACH batch costs, wire fees, account maintenance — call your relationship manager and negotiate. Switching banks is annoying; they're counting on that.
- **Never invest operating cash in anything with principal risk.** "But commercial paper yields 0.25% more than T-bills" is not a good enough reason. The treasury function is to preserve capital, not generate returns. Yield is the third priority after capital preservation and liquidity. If you want returns, invest in your business.
- **Wires are forever; ACH can be reversed.** A wire transfer is final within hours and virtually irreversible. An ACH debit can be reversed within 5 days (consumer) or 2 days (business). Fraudsters know this — they demand wire transfers. Any new vendor requesting wire payment for the first invoice? Call them at a known number first.
- **Cap table hygiene prevents fundraising delays.** A messy cap table (missing signatures, untracked option grants, incorrect share counts) adds 2-4 weeks to fundraising legal review. That's 2-4 weeks of runway burned while your lawyers and their lawyers argue about who owns what.

## Error Decoder
<!-- QUICK: 30s — exact error → root cause → fix -->
<!-- DEEP: 10+min — each error from real startup treasury failures -->

| Error / Symptom | Root Cause | Fix |
|----------------|------------|-----|
| Cash forecast consistently 15-20% higher than actual | Customer collections lag assumed — you're modeling DSO at 30 days but actual is 45 days | Replace "invoice date + 30" with actual customer-by-customer payment history. Use average DSO from AR aging, not contract terms. Model: 50% pay within terms, 30% in 15 days late, 20% in 30+ days late. |
| Bank froze your account without warning | KYC refresh triggered (bank needs updated beneficial ownership info), unusual transaction pattern, or fraud algorithm flag | Immediately: contact relationship manager (banker, not 1-800 support). Have: EIN letter, certificate of incorporation, board resolution authorizing account signers, government ID for all signers. Proactively: update KYC docs annually before the bank asks. |
| Venture debt covenant violation — minimum cash breached | Company drew too much on debt facility, not accounting for interest payments that also reduce cash | Model debt service in weekly cash forecast. Add covenant headroom: actual cash must be 2x covenant minimum. If covenant is $2M minimum cash, manage to $4M. Report potential breaches BEFORE they happen — lenders prefer cure plans to surprises. |
| Wire sent to fraudulent account after vendor "changed banks" | Business email compromise — attacker spoofed vendor email with new wire instructions | Never change vendor banking details based on email alone. Call vendor at independently verified number. Implement: vendor bank change = 2-person verbal verification + 48-hour cooling period before new account is active. |
| Unrecognized ACH debit draining operating account | ACH debit block not enabled; fraudster obtained account/routing numbers from a check | Enable ACH debit block on all accounts except those specifically designated for ACH collections. Add ACH positive pay: pre-authorize each originator. Dispute unauthorized debits within 24 hours for best chance of recovery. |
| Insurance claim denied — "not covered under your policy" | Policy has exclusions you didn't read. Common gaps: no cyber coverage on general liability, D&O excludes regulatory actions, E&O excludes patent infringement | Annual review with broker: "Here are our top 5 risks. Confirm in writing each is covered and list any exclusions." Broker's oral assurance is not binding — get it in email. |
| 409A valuation expired, can't grant options | 12 months elapsed since last 409A without refresh; or material event occurred (new term sheet) and no new valuation | Order new 409A immediately (3-4 week process). Until received, all option grants are at risk of IRS challenge. If employees need grants now, board can grant with "strike price = greater of current 409A price or new 409A price when received" — but this is legal advice territory. |

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
<!-- QUICK: 30s — all must pass for treasury health -->

- [ ] **[S1]** 13-week cash flow forecast updated within last 5 business days — actuals reconciled for prior week
- [ ] **[S2]** All bank accounts reconciled — operating, reserve, and any international accounts
- [ ] **[S3]** Cash position dashboard shows: total cash, operating cash, reserve cash, FDIC/SIPC coverage status
- [ ] **[S4]** Dual approval enabled for all payments > threshold ($10K seed, $50K growth)
- [ ] **[S5]** Positive pay enabled on all checking accounts — check issue files transmitted daily
- [ ] **[S6]** ACH debit block enabled on reserve accounts — only operating account can receive ACH debits
- [ ] **[S7]** Wire callback verification procedure documented and tested — all employees know the rule
- [ ] **[S8]** Vendor bank change policy: verbal verification + 48-hour cooling period — no exceptions
- [ ] **[S9]** Investment policy documented and approved — permissible instruments, maturity limits, approval authority
- [ ] **[S10]** Banking relationships: at least 2 active institutions with operating capacity at each
- [ ] **[S11]** Insurance certificates: D&O, E&O, Cyber, GL, Workers' Comp — all active, no gaps in coverage
- [ ] **[S12]** Venture debt covenants monitored monthly — next reporting deadline on calendar
- [ ] **[S13]** Cap table on Carta/Pulley matches company records — last 409A < 12 months old
- [ ] **[S14]** FX exposure > $500K is hedged or has an explicit board-approved policy for remaining unhedged
- [ ] **[S15]** Segregation of duties: payment initiation ≠ approval ≠ reconciliation — or CEO compensating control documented
- [ ] **[S16]** Quarterly bank fee review completed — fees benchmarked against 2 competitors

## What Good Looks Like

Every Monday at 9 AM, the cash dashboard is updated: actual prior-week ending cash vs. forecast, variance explanation if > 5%, reforecast for next 12 weeks. A CFO or CEO can look at one screen and answer: "How many weeks of runway do we have? When do we need to raise? Are we compliant with all debt covenants? Is all cash FDIC/SIPC insured?" All bank accounts are visible at a glance. Payment runs (Tuesday/Thursday) process without drama because approvals are already in place. An auditor can test any wire transfer from the past year and find: approval, beneficiary match, callback verification log, and bank confirmation — in under 10 minutes. The company could survive its primary bank being inaccessible for 2 weeks without missing a single payment.

## References
<!-- QUICK: 30s — deeper reading and templates -->

- **Templates:** `assets/13-week-cash-forecast.xlsx` — Rolling 13-week cash forecast with variance tracking, payroll integration, and covenant monitoring
- **Templates:** `assets/investment-policy-template.md` — 2-page investment policy document: objectives, permitted instruments, maturity limits, approval authority
- **Templates:** `assets/payment-authorization-matrix.xlsx` — Delegation of authority matrix: role, payment type, approval limit, backup approver
- **Templates:** `assets/insurance-coverage-tracker.xlsx` — Insurance policy tracker: carrier, coverage type, limits, premium, renewal date, broker contact
- **References:** `references/banking-startup-guide.md` — Startup banking landscape post-SVB: bank comparison, account structures, FDIC sweep mechanics, KYC requirements
- **References:** `references/venture-debt-guide.md` — Venture debt term sheets: key terms, covenant structures, warrant math, lender comparison, negotiation tactics
- **References:** `references/fraud-prevention-playbook.md` — Social engineering defense, payment controls, incident response, real case studies with dollar amounts
- **References:** `references/foreign-exchange-guide.md` — FX for startups: exposure measurement, hedging instruments, provider comparison, intercompany transfer documentation
- **References:** `references/cap-table-operations.md` — Carta/Pulley workflows, 409A process, option exercise handling, secondary transaction mechanics
- **Books:** The Basics of Treasury Management (AFP), Venture Debt and Alternative Funding (David Spreng), Bank Director's Handbook
- **Related skills:** `fp-and-a-analyst` (cash burn forecasting and financial modeling), `accountant` (bank reconciliations and AP/AR), `ceo-strategist` (fundraising strategy and board management), `legal-advisor` (debt agreements and insurance contracts), `board-manager` (board reporting and fiduciary duties)
