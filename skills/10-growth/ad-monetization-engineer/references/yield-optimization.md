# Yield Optimization Guide

## Key Metrics for Yield
- **RPM (Revenue Per Mille)**: total revenue / (pageviews / 1000)
- **eCPM**: effective cost per thousand impressions
- **Fill rate**: impressions served / ad requests
- **Viewability rate**: viewable impressions / total impressions
- **CPM floor**: minimum price to serve an ad

## RPM vs CPM
- CPM measures per-impression value
- RPM measures per-pageview value (accounts for multiple ads + fill)
- OPTIMIZE FOR RPM, not CPM
- Higher CPM + lower fill can = lower RPM than moderate CPM + high fill

## Price Floor Strategy

### Unified Pricing Rules (GAM)

```
Geography tiers:
  US/CA/UK/AU → Floor $1.50 CPM
  Western Europe → Floor $0.80 CPM
  Rest of World → Floor $0.20 CPM

Device tiers:
  Desktop → Floor +20% (higher engagement)
  Mobile → Floor baseline
  Tablet → Floor +10%
```

### Dynamic Floor Optimization
- Adjust floors based on historical clearing prices
- Raise floors during high-demand periods (Q4, holidays)
- Lower floors during low-demand periods (January, weekends)
- Use 15-day rolling average of clearing CPM

## A/B Testing Ad Configurations
1. Test one variable at a time: floor price, ad layout, timeout
2. Minimum 2-week test duration (account for weekly cycles)
3. Segment by: device, geo, traffic source, time of day
4. Statistical significance: p < 0.05, minimum 10K impressions/variant
5. Metrics: RPM (primary), viewability, page speed, user engagement

## Header Bidding Optimization
- Add/remove bidders based on incremental lift
- Adjust timeout per bidder performance
- Enable S2S for latency reduction
- Implement dynamic floors per bidder
- Monitor: bid rate, win rate, timeout rate, avg CPM per bidder

## Dynamic Allocation
- Let AdX compete with direct-sold and PG line items
- Enable "Optimized Competition" in GAM
- Set appropriate value CPM for non-guaranteed line items
- AI-driven: Google's algorithm learns and optimizes over time

## Seasonal Optimization
- Q4 (Oct-Dec): raise floors 20-40%, add seasonal demand partners
- January: lower floors 10-20%, focus on fill rate
- Events: Presidential elections, Olympics, Black Friday = demand spikes

## Revenue Attribution
- Track RPM by: content category, author, traffic source, device, geo
- Identify high-RPM content for replication
- Identify low-RPM content for optimization or demonetization
