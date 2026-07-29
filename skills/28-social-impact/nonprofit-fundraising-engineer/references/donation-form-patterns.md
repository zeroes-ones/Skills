# Donation Form Patterns
> Reference: Gift array design, recurring toggle UX, impact copy, mobile optimization

## Gift Array Architecture

### Data Model

```json
{
  "gift_array": [
    {"amount": 25, "impact": "Provides meals for 5 families", "preselected": false},
    {"amount": 50, "impact": "Provides meals for 10 families", "preselected": true},
    {"amount": 100, "impact": "Provides meals for 20 families", "preselected": false},
    {"amount": 250, "impact": "Supports a family for a month", "preselected": false}
  ],
  "custom_amount_enabled": true,
  "min_amount": 5,
  "currency": "USD"
}
```

### Amount Calculation
- Low: 25th percentile of one-year historical gifts
- Medium (preselected): Median gift × trending factor
- High: 75th percentile
- Stretch: 2× median gift

## Recurring Toggle UX

- Default: Monthly (opt-out pattern)
- Labels: "Monthly" / "One-Time" (not "Recurring" — term tests lower)
- Annual option: Show with 10-15% discount, display monthly equivalent
- Impact: Dynamically update impact copy when toggle changes

## Mobile Optimization Checklist
- Stacked vertical layout (single column)
- Tap targets ≥ 44×44px
- Sticky CTA button at bottom
- No horizontal scrolling
- Apple Pay / Google Pay buttons when available
- Test on $100 Android phone on 3G

## A/B Testing Protocol
1. Test one element at a time
2. Minimum 1,000 visitors per variant
3. Statistical significance: p < 0.05
4. Run for minimum 2 weeks (capture weekday/weekend variance)
5. Primary metric: revenue per visitor (not conversion rate alone)

Version: 1.0
