# Checkout Flow Patterns

## Flow Architecture

### Single-Page Checkout
Best when: ≤5 total fields, simple product, consumer/SMB

```
[Plan Selected] → [Email → Password → Name → Card → Pay] → [Confirmation]
All on one page. Stripe Checkout is the gold standard.
```

### Multi-Step Checkout
Best when: >5 fields, complex product, enterprise, international (tax/VAT)

```
Step 1: [Email + Password] → Step 2: [Name + Company + VAT ID] → Step 3: [Card + Billing Address] → Step 4: [Review + Pay]
```

## Field Optimization

| Before | After | Rationale |
|--------|-------|-----------|
| Username + Email + Password + Confirm | Email + Password (or Google/GitHub SSO) | 4 fields → 1-2 fields. Social login eliminates form entirely |
| First Name + Last Name | Full Name (single field) | 2 fields → 1. Separate only if needed for personalization |
| Company + VAT ID + Billing Address | Company (auto-fill billing from company domain) | 3 fields → 1 with Clearbit/domain lookup |
| Card Number + Expiry + CVC + ZIP | Card Number + Expiry + CVC (ZIP from billing) | 4 fields → 3. ZIP auto-filled |
| Phone (required) | Phone (optional, post-purchase for onboarding) | Remove from checkout. Collect after payment |

## Address Autocomplete

Services: Google Places API, Loqate, SmartyStreets
- Type 3+ characters → show suggestions
- Auto-fill: street, city, state, ZIP, country
- Reduces typing errors by 90%, speeds form completion by 30%

## VAT/Tax Display

### B2B SaaS (Standard)

```
Plan Price: $99/mo (excl. VAT)
Enter VAT ID → VAT reverse-charged (0%)
No VAT ID → VAT added based on billing country
Total at checkout: $99/mo or $99 + local VAT
```

### B2C SaaS

```
Show VAT-inclusive price by default
Plan Price: $119/mo (incl. VAT) ← what customer sees
Breakdown available: $99 + $20 VAT
```

## Abandoned Cart Recovery

### Email Sequence

| Timing | Subject | Content |
|--------|---------|---------|
| 1 hour | "Complete your [Product] setup" | Reminder + direct checkout link. Assuming technical issue, not objection |
| 24 hours | "Your [Product] trial is waiting" | Value reminder + social proof. "Join X companies already using [Product]" |
| 72 hours | "[Name], anything I can help with?" | Personal. From founder/CS. "Reply to this email — happy to answer questions." |

### Exit Intent Modal

```
Trigger: cursor moves toward browser close/back button on checkout page
Content: "Wait — your trial is ready! Complete setup in 30 seconds."
CTA: "Continue Setup" → back to checkout
```

## Payment Method Display

Show accepted methods BEFORE the form:

```
We accept: [Visa] [Mastercard] [Amex] [Apple Pay] [Google Pay] [PayPal]
           [Bank Transfer — for annual plans] [PO — for Enterprise]
```

## Trust Signals at Checkout

Place near payment form:
- 🔒 SSL/TLS badge: "256-bit encryption"
- PCI compliance badge
- "No hidden fees. Cancel anytime."
- Money-back guarantee: "30-day money-back guarantee"
- Support availability: "Need help? Chat with us" (live, not bot)
