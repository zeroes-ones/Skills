# Volume Discount Models

## Discount Curve Types

### 1. Linear Discount

Simple percentage off based on volume tier.

| Seats | Discount | Price/Seat (List=$100) | Total ACV |
|-------|----------|------------------------|-----------|
| 1-99 | 0% | $100 | $100-$9,900 |
| 100-499 | 15% | $85 | $8,500-$42,415 |
| 500-999 | 25% | $75 | $37,500-$74,925 |
| 1000+ | 35% | $65 | $65,000+ |

**Formula**: `total = seats × list_price × (1 - discount_rate)`
**Excel**: `=A2*B2*(1-VLOOKUP(A2, discount_table, 2, TRUE))`

### 2. Tiered Discount

Different rates for different volume bands. First N at one price, next M at lower price.

| Band | Seats in Band | Discount | Price/Seat | Band Revenue |
|------|--------------|----------|-----------|-------------|
| 1-100 | 100 | 0% | $100 | $10,000 |
| 101-500 | 400 | 20% | $80 | $32,000 |
| 501-1000 | 500 | 30% | $70 | $35,000 |
| 1001+ | N-1000 | 40% | $60 | $(N-1000)×$60 |

**Formula**: Sum of `band_seats × list_price × (1 - band_discount)` for all bands
**Example (1000 seats)**: $10,000 + $32,000 + $35,000 = $77,000
**vs Linear**: 1000 × $65 = $65,000

Tiered discounting yields ~18% more revenue at the same volume point.

### 3. Platform/Consumption Pricing

Price scales with usage volume, not seats.

| Metric | Example Products | Pricing Model |
|--------|-----------------|---------------|
| API calls | Twilio, Stripe, AWS | $X per 1,000 calls, tiers at volume |
| MAUs (Monthly Active Users) | Slack, Figma | $X per MAU with volume tiers |
| Data volume | Snowflake, Datadog | $X per GB ingested/stored |
| Compute time | Vercel, Netlify | $X per build-minute or compute-hour |
| Events | Segment, Amplitude | $X per 1,000 MTU (Monthly Tracked Users) |

**Consumption Formula**:

```
base_fee + max(0, usage - included_usage) × overage_rate
```

## Discount Approval Matrix

| Discount % | Approver | Documentation Required | SLA |
|-----------|----------|----------------------|-----|
| 0-10% | Account Executive | CRM note with reason code | Auto-approved |
| 10-25% | VP Sales | Business case: deal size, strategic value, competitive context | 24hr |
| 25-40% | CFO | P&L impact analysis, multi-year total value, margin waterfall | 48hr |
| 40%+ | CEO | Strategic rationale, board notification for >$500K ACV | 72hr |

### Reason Codes (Required for All Discounts >10%)

1. **Volume commitment**: Multi-year, high seat count, platform-wide deployment
2. **Strategic logo**: Market-making customer, reference-able, industry leader
3. **Competitive displacement**: Replacing entrenched competitor, win-back
4. **New market entry**: First customer in new geo or vertical
5. **Product partnership**: Co-development, beta testing, feature collaboration

## Price Protection for Multi-Year Deals

### Standard Multi-Year Structure

| Year | Price | Annual Increase | Customer Benefit |
|------|-------|----------------|-----------------|
| Year 1 | $100,000 | — | Locked pricing for commitment |
| Year 2 | $107,000 | 7% | Price certainty, no renegotiation |
| Year 3 | $114,490 | 7% | Avoids market-rate increases (typically 10-15%) |

### Renewal Cap

Standard: 5-7% maximum annual increase on renewal. Protects customer from surprise 30%+ increases while accounting for inflation and added value.

## True-Up Process (Usage-Based Enterprise)

### Quarterly True-Up

```
Actual usage reported at end of quarter
  ↓
Compare to committed minimum
  ↓
If actual > committed: customer pays overage at contracted rate
If actual < committed: customer pays committed minimum (no refund)
  ↓
Annual reconciliation: adjust Year 2 commitment based on Year 1 actuals
```

### True-Up Clause Language

> "Customer commits to minimum annual usage of [X] units at [Y] rate. Quarterly true-up: Customer shall report actual usage within 15 days of quarter end. Overage beyond committed volume billed at contracted overage rate. Unused committed volume does not roll over. Annual reconciliation shall adjust subsequent year commitment to 90% of prior year actuals."
