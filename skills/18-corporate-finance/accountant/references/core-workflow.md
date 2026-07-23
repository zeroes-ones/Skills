# Core Workflow — Full Implementation

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
