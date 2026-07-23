# Best Practices

<!-- STANDARD: 3min -->

- **One source of truth for assumptions.** Every driver lives in exactly one cell on the assumptions tab. No exceptions. When you debate a number, you debate that one cell.
- **Model in months, not years, through at least month 36.** Annual models hide seasonality, hiring timing, and cash flow gaps. A company that's fine on an annual basis can miss payroll in month 9.
- **Gross margin by product line, not blended.** High-margin software revenue subsidizing low-margin services revenue creates a ticking time bomb. As the mix shifts, blended margin deteriorates — and you won't see it coming.
- **Cash flow statement from the balance sheet, not the P&L.** Indirect method: start with net income, add back non-cash items (D&A, SBC, bad debt), then adjust for working capital changes (ΔAR, ΔAP, Δprepaid, Δdeferred revenue). The balance sheet must balance every period.
- **AR = Revenue × DSO / Days.** If your SaaS company bills annually and DSO is 45, you have a collections problem. SaaS DSO should be < 30 for monthly billing, < 15 for annual upfront.
- **Deferred revenue is a liability, not revenue.** SaaS companies that bill annually show high cash but low GAAP revenue. Model the unwinding: deferred revenue balance / monthly revenue recognition = months of booked-but-unrecognized revenue.
- **SBC is a real expense.** Stock-based compensation reduces your ownership and will dilute you. Model it on the P&L (ASC 718) and show diluted share count. Investors will calculate EBITDA - SBC anyway.
- **Never model to a desired outcome.** If the model shows you run out of cash in 14 months, don't adjust assumptions until it shows 24. Present the real number and plan the bridge (raise sooner, cut burn, grow faster).
- **Version your models.** `Company_Model_v12_final_FINAL.xlsx` is not a system. Use: `YYYY-MM-DD_Model_v[#]_[change description].xlsx`. Archive old versions, don't overwrite.
- **Peer benchmark every quarter.** Pull public SaaS comps: gross margin, opex ratios, Rule of 40, ARR per FTE. If your model diverges >20% from median, write a footnote explaining why.

<!-- QUICK: 30s — key rule-of-thumb benchmarks -->

| Stage | ARR | Gross Margin | OpEx % Rev | Rule of 40 | Burn Multiple |
|-------|-----|-------------|-----------|------------|---------------|
| Seed | $0-3M | 65-75% | 150-250% | N/A (negative) | N/A |
| Series A | $3-8M | 70-78% | 100-150% | 20-40% | 1.5-2.5x |
| Series B | $8-25M | 72-80% | 80-110% | 35-55% | 1.0-1.8x |
| Series C | $25-100M | 73-82% | 60-90% | 45-70% | 0.5-1.2x |
| Pre-IPO | $100M+ | 75-85% | 50-75% | 50%+ | <0.8x |
