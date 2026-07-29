# International Pricing UX

## Currency Localization

### Auto-Detection + Manual Override

```
1. Detect user country via IP geolocation
2. Display pricing in local currency
3. Show currency selector dropdown for manual override
4. Persist currency preference in cookie/localStorage
```

### Currency Display Conventions

| Country | Symbol Position | Format | Example |
|---------|----------------|--------|---------|
| US | Prefix | $X,XXX.XX | $1,299.00 |
| EU | Suffix | X.XXX,XX € | 1.299,00 € |
| UK | Prefix | £X,XXX.XX | £1,299.00 |
| Japan | Prefix | ¥X,XXX | ¥129,900 |
| India | Prefix | ₹X,XX,XXX | ₹1,29,900 |

## PPP Pricing Strategy

### Adjustment Factors

Based on World Bank PPP conversion factors:

| Market | PPP Factor vs USD | $99/mo US → Local |
|--------|------------------|-------------------|
| Germany | 0.75 | €74/mo |
| Brazil | 0.45 | R$223/mo |
| India | 0.25 | ₹2,079/mo |
| Japan | 0.90 | ¥14,850/mo |
| UK | 0.70 | £69/mo |

### Parity Grid (Publish Transparently)

```
| Country | Monthly Price (Annual) | Why? |
|---------|----------------------|------|
| United States | $99/mo | Base pricing |
| Germany | €74/mo | Adjusted for EU market pricing |
| Brazil | R$223/mo | Adjusted for local purchasing power |
| India | ₹2,079/mo | Adjusted for local purchasing power |
```

## Language Localization

### Translation Priority

| Priority | Content | Why |
|----------|---------|-----|
| Critical | Pricing, features, CTAs | Revenue-critical |
| High | Value proposition, testimonials | Conversion-critical |
| Medium | FAQ, comparison tables | Trust-building |
| Low | Footer, legal (use professional translation) | Required but lower impact |

### RTL Support

For Arabic, Hebrew, Farsi:
- Entire page layout mirrors
- Tier order: right-to-left (Enterprise on right, Starter on left)
- Numbers remain LTR within RTL text
- Icons may need directional variants (arrows)

## Regional Payment Methods

| Market | Must-Have Payment Methods |
|--------|--------------------------|
| United States | Visa, MC, Amex, Apple Pay, Google Pay, PayPal |
| Germany | SEPA Direct Debit, SOFORT, Giropay, PayPal |
| Netherlands | iDeal (70%+ of e-commerce), SEPA |
| Brazil | Boleto Bancário, PIX, local credit cards (installments) |
| India | UPI, NetBanking, Paytm, local cards |
| China | Alipay, WeChat Pay, UnionPay |
| Japan | Konbini (convenience store payment), Pay-easy |

## VAT/Tax by Region

| Region | B2B Treatment | B2C Treatment | Rate Examples |
|--------|-------------|--------------|---------------|
| EU | Reverse charge with valid VAT ID | VAT-inclusive display required | 19-27% |
| UK | Reverse charge with valid VAT ID | VAT-inclusive display required | 20% |
| US | No VAT. Sales tax by state | Show pre-tax; tax at checkout | 0-10% |
| Australia | GST applied regardless | GST-inclusive display | 10% |
| Canada | GST/HST applied | Show pre-tax; tax at checkout | 5-15% |
| Singapore | GST applied regardless | GST-inclusive | 9% |
