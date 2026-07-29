# Ad Revenue Analytics & Reconciliation

## Key Metrics Dashboard

### Real-Time (15-min latency)
- Ad requests per second
- Fill rate (current)
- eCPM (current, by ad unit)
- Bid rate (header bidding)
- Timeout rate

### Daily (Financial Reporting)
- Total ad revenue
- RPM (revenue per 1000 pageviews)
- eCPM by ad unit / geo / device
- Fill rate by demand source
- Viewability rate
- Ad CTR (if applicable)
- IVT rate

### Weekly/Monthly (Trend Analysis)
- Revenue trend vs. prior period
- Yield group performance
- Demand source mix (direct vs programmatic %)
- Header bidding lift
- Ad-blocker impact

## Revenue Attribution

### Dimensions
- Content category / section
- Author (for content sites)
- Traffic source (organic, social, direct, referral)
- Device (desktop, mobile, tablet)
- Geography (country, region)
- Browser
- Time of day / day of week

### Attribution Method
1. GAM Data Transfer files → hourly impression/revenue logs
2. Join with analytics data (page URL → content metadata)
3. Attribution model: last-touch (impression served on page = revenue for that page)

## Discrepancy Reconciliation

### Expected Discrepancy
- GAM vs SSP: 5-15% (normal — counting methodology, time zone, latency)
- GAM vs actual bank deposit: 2-5% (payment terms, fees, currency conversion)
- >15%: investigate data pipeline, counting methodology, fraud

### Reconciliation Process
1. Export GAM monthly report
2. Export each SSP monthly report
3. Compare: impressions, revenue, CPM by demand source
4. Identify outliers (>10% discrepancy for a single demand source)
5. Investigate: counting method, time zone, currency, fees
6. Document and either accept or escalate

### Common Causes
- GAM counts gross, SSP counts net (after IVT filtration)
- Currency conversion rates and timing
- Time zone differences (UTC vs local)
- Billing cycle offsets (SSP reports on different calendar)
- Ad serving fees not reflected in SSP reports

## Yield Groups
- Segment inventory into yield groups by performance
- High-yield: US, desktop, direct traffic → optimize for CPM
- Mid-yield: Western Europe, mobile, social → balance CPM and fill
- Low-yield: Rest of world → optimize for fill rate, experiment with formats
- Review and rebalance monthly

## Alert Thresholds
- RPM drops >15% day-over-day → investigate
- Fill rate drops below 50% → floor price may be too high
- IVT rate exceeds 3% → investigate traffic quality
- Timeout rate exceeds 10% → reduce number of bidders or increase timeout
- Viewability drops below 50% → review ad placement
