# Peer-to-Peer Fraud Prevention
> Reference: P2P fraud patterns, velocity checking, CAPTCHA, chargebacks

## Common P2P Fraud Patterns

| Pattern | Description | Detection |
|---------|-------------|-----------|
| Card testing | Fraudsters test stolen cards with small donations | Velocity: >5 attempts/minute from same IP |
| Fake campaigns | Fraudster creates campaign, donates with stolen cards, withdraws to personal account | Approval queue for >$10K campaigns |
| Refund fraud | Donate large amount, request refund to different card | Match refund card to original payment method |
| Money laundering | Layer illicit funds through multiple small donations | Unusual donation patterns: many $X donations from different cards to same campaign |

## Defense Layers

### Layer 1: Donation Form
- Minimum donation: $5 (prevents micro-charge card testing)
- CAPTCHA: reCAPTCHA v3 (invisible, score-based)
- Honeypot field: hidden field that bots fill in

### Layer 2: Rate Limiting
- IP-based: 5 donations/minute, 20/hour
- Session-based: 10 donations/session
- Card fingerprint: 3 donations/card/day across all campaigns

### Layer 3: Admin Controls
- Auto-flag: campaigns raising >$5K in <24 hours
- Manual approval: campaigns >$10K total
- Payout delay: funds held 7 days before disbursement

### Layer 4: Monitoring
- Chargeback rate monitored daily (target: <0.5%)
- Unusual velocity alerts to admin
- Daily fraud report: flagged transactions, blocked attempts

Version: 1.0
