# LogSnap MVP — UI Design

## Screen Count: 6

Every screen has one job. If a screen can't justify itself in a sentence, it gets cut.

1. **Dashboard**: Monitor list with status dots and uptime %. Home screen after login.
2. **Add Monitor**: URL field, interval dropdown (30s/60s/5min), alert email. One form, no wizard.
3. **Monitor Detail**: 24h uptime sparkline, check history table, attached alert rules.
4. **Alert Rules**: Per-monitor threshold (how many regions down = alert) + notification email. No escalation chains.
5. **Status Page**: Public-facing. Team name, monitor list with green/red dots. The product's face.
6. **Settings**: Team name, Stripe billing portal link. Four fields total.

## Mobile-First, Dark-Only

80% of users check status on their phone. The dashboard is a vertical list of green/red dots — scannable in three seconds.

One color: Blue (#256EB3). Everything else gray scale. Tailwind CSS utility classes — no component library, no `theme.ts` with 47 tokens. Dark mode only: status pages look better in dark, and it's one theme to maintain.

## Status Page (The Differentiator)

- **Team name** centered at top, large and weighty. This is your brand.
- **Monitor list**: Name left, green/red dot right. "Checked 32s ago" in muted gray below. 90-day uptime % as a small badge.
- **No clutter**: No logo upload, custom domain, incident history, or subscribe form. Phase 2.
- **Rendering**: ISR revalidating every 60 seconds. Loads like a static site backed by live data.

## The "Aha Moment"

Empty state → "Add your first monitor" → URL input → spinner with "Checking..." → within 60 seconds, the row flips from gray to green. The user watches their site go from unknown to confirmed-up in under a minute. If onboarding takes more than 90 seconds, I've failed.

## Component Inventory

- **MonitorRow**: Name, truncated URL, status dot (green/yellow/red), uptime % badge
- **StatusBadge**: Colored pill — "Operational" (green), "Degraded" (yellow, one region down), "Down" (red)
- **UptimeChart**: 200px sparkline, last 24h response times. No axes, no labels, just the line.
- **AlertRuleForm**: Threshold slider (1–3 regions) + email input. Two fields.
- **CheckoutButton**: Stripe-hosted checkout, new tab. No custom billing UI.
