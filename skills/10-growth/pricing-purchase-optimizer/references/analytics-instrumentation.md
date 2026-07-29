# Pricing Page Analytics Instrumentation

## Funnel Stages

```
1. Visitor lands on site → [GA/Amplitude: page_view]
2. Navigates to /pricing → [GA: pricing_page_view]
3. Scrolls below 50% → [GTM: scroll_depth_50]
4. Hovers on tier card → [GTM: tier_hover + tier_name]
5. Clicks tier CTA → [GTM: tier_cta_click + tier_name]
6. Clicks annual/monthly toggle → [GTM: billing_toggle + selection]
7. Starts signup → [GA: signup_start + tier + billing]
8. Completes signup → [GA: signup_complete]
9. Enters payment → [GA: payment_start]
10. Completes payment → [GA: purchase + revenue + tier + billing]
```

## Key Metrics

| Metric | Formula | Target | Tool |
|--------|---------|--------|------|
| Pricing page view rate | pricing_views / total_visitors | 15-30% | GA |
| Tier click rate | tier_cta_clicks / pricing_views | 10-25% | GTM |
| Signup start rate | signup_starts / tier_cta_clicks | 60-80% | GA |
| Signup complete rate | signup_completes / signup_starts | 70-90% | GA |
| Payment complete rate | purchases / payment_starts | 80-95% | GA |
| Full funnel conversion | purchases / pricing_views | 2-5% | GA |
| Revenue Per Visitor (RPV) | total_revenue / pricing_views | Product-dependent | Calculated |

## Drop-Off Analysis

Find the highest-abandonment step:

```
pricing_views: 10,000
  ↓ 85% continue
tier_cta_clicks: 8,500
  ↓ 70% continue
signup_starts: 5,950
  ↓ 90% continue
signup_completes: 5,355
  ↓ 95% continue
payment_starts: 5,087
  ↓ 85% continue
purchases: 4,324

BIGGEST DROP: tier_cta → signup_start (70% = 2,550 lost)
ACTION: Optimize CTA-to-signup transition. Single-page checkout.
```

## Session Recording Tools

| Tool | Best For | Pricing | Setup |
|------|----------|---------|-------|
| **Hotjar** | Heatmaps + recordings, SMB-mid | Free-$99/mo | Script tag |
| **FullStory** | Enterprise, advanced search | Custom quote | Script tag |
| **Microsoft Clarity** | Free, decent features | Free | Script tag |
| **LogRocket** | Product analytics + recordings | $99+/mo | Script tag |
| **Mouseflow** | Funnel analysis + recordings | $31+/mo | Script tag |

### What to Watch in Recordings

- Rage clicks: user repeatedly clicks non-clickable element → UI bug
- Dead clicks: user clicks, nothing happens → broken interaction
- Scroll abandonment: user scrolls 25% then leaves → above-fold problem
- Form rage: user types, deletes, re-types → confusing field
- Price comparison loops: user toggles plans repeatedly → can't decide → need better differentiation

## Revenue Attribution

### Per-Variant Revenue Tracking

```
For each pricing page variant:
  variant_id → GTM custom dimension
  purchase event includes variant_id
  Report: revenue by variant (not just conversion by variant)
```

### LTV by Pricing Page Variant

Critical: variant that drives higher conversion but lower LTV may be net-negative.

```
Variant A: 5% conversion × $500 LTV = $25 RPV (Revenue Per Visitor)
Variant B: 4% conversion × $800 LTV = $32 RPV ← WINNER despite lower conversion
```

Always optimize for RPV, not conversion rate alone.
