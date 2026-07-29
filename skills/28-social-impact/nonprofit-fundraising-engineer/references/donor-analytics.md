# Donor Analytics
> Reference: Funnel analytics, donor LTV model, segmentation, dashboards

## Donation Funnel Metrics

| Stage | Metric | Target |
|-------|--------|--------|
| Landing page → Donation page | Click-through rate | >15% |
| Donation page → Form interaction | Engagement rate | >40% |
| Form start → Form submit | Completion rate | >60% |
| Submit → Confirmation | Confirmation rate | >95% |
| Overall: Visitor → Donor | Conversion rate | 3-8% |

## Donor Lifetime Value (LTV) Model

```
LTV = Average Gift × Annual Frequency × Retention Years × Upgrade Factor

Components:
- Average Gift: median one-time or monthly amount
- Annual Frequency: 1 for one-time, 12 for monthly
- Retention Years: 1.5-2 for one-time, 5-7 for monthly
- Upgrade Factor: 1.1-1.2 (10-20% upgrade/downgrade over lifetime)
```

## Segmentation Dimensions

| Segment | Criteria | Strategy |
|---------|----------|----------|
| New Donor | First gift <30 days | Welcome series, monthly upgrade prompt |
| Active Monthly | Recurring, active | Retention focus, upgrade opportunities |
| Lapsed Monthly | Recurring, cancelled | Win-back campaign, feedback survey |
| Major Donor | Cumulative >$1K or single >$500 | Personal outreach, impact reporting |
| Event Donor | Gave via P2P/event | Convert to direct supporter |

## Dashboard Design
- Top row: Total raised (MTD/YTD), donor count, average gift, recurring %
- Funnel: conversion rate at each stage with week-over-week trend
- Health: recurring churn rate, new donor acquisition, lapsed donor recovery
- Campaign: per-campaign performance with ROI

Version: 1.0
