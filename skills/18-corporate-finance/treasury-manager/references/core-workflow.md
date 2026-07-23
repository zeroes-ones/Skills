# Core Workflow — Full Implementation

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
