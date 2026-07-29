# Recurring Giving Architecture
> Reference: Stripe Subscription lifecycle, dunning, card updater, upgrade/downgrade

## Subscription Lifecycle States

```
incomplete → incomplete_expired
active → past_due → unpaid → canceled
active → canceled
active → paused
```

## Dunning Management (Stripe)

| Retry | Days after failure | Action |
|-------|-------------------|--------|
| 1 | +1 day | Retry charge |
| 2 | +3 days | Retry + email notification |
| 3 | +7 days | Retry + SMS (if available) |
| Final | +9 days | Pause subscription, send "update payment" email |

## Card Updater
- Stripe Automatic Card Updater: enabled by default
- Network-level updates for Visa Account Updater, Mastercard ABU
- ~60% of expired cards get updated automatically

## Webhook Events
- `customer.subscription.created` → Create recurring donation in CRM
- `invoice.payment_succeeded` → Record payment, emit receipt
- `invoice.payment_failed` → Enter dunning, notify donor
- `customer.subscription.updated` → Sync plan changes to CRM
- `customer.subscription.deleted` → Mark lapsed in CRM

## Self-Service Portal
- View active subscriptions
- Upgrade/downgrade plan (with proration)
- Update payment method
- Pause subscription (don't cancel)
- Download receipts

Version: 1.0
