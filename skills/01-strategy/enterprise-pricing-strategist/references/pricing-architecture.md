# Pricing Architecture Reference

## Tier Design Patterns

### Good-Better-Best + Enterprise

The standard B2B SaaS tier structure with 4 tiers:

| Tier | Target | Price Point | Key Differentiators |
|------|--------|------------|---------------------|
| **Good** | Individual/Small team | $X/mo | Core features, community support, 99.5% SLA |
| **Better** | Growing team | $Y/mo (3-5x Good) | Advanced features, priority support, 99.9% SLA |
| **Best** | Department/Division | $Z/mo (2-3x Better) | All features, analytics, custom roles, 99.95% SLA |
| **Enterprise** | Organization-wide | Contact Sales (3-10x Best) | SSO, audit logs, dedicated CSM, 99.99% SLA, custom integrations |

### Feature Gating Strategy

Enterprise-only features (non-negotiable gates):
- **SSO/SAML**: #1 enterprise requirement. Never include below enterprise tier
- **Audit logs**: Compliance requirement for SOC 2, HIPAA, GDPR
- **Dedicated CSM**: Named contact with QBR cadence
- **Custom SLA**: 99.99% uptime with financial credits
- **Source code escrow**: Third-party code escrow for critical infrastructure
- **Custom integrations**: API access tier, dedicated solution architect
- **Data residency**: Choose data storage region (GDPR, data sovereignty)

### Per-Seat vs Usage-Based Comparison

| Model | Pros | Cons | Best For |
|-------|------|------|----------|
| **Per-Seat** | Predictable, easy to budget, scales linearly with organization | Hard to measure "seat" in shared accounts, seat-sharing | Collaboration tools, CRM, HR software |
| **Usage-Based** | Aligns with value delivered, low entry barrier | Unpredictable bills, hard to budget, sticker shock | API products, infrastructure, data platforms |
| **Hybrid** | Floor predictability + ceiling aligned to value | Complexity in quoting, harder to forecast | Products with variable consumption (API calls + seats) |

## Price Anchoring

### Anchor Psychology

Position the highest-value tier first in left-to-right display. The anchoring effect makes subsequent tiers appear more affordable.

```
[Enterprise — $Contact] [Best — $999/mo] [Better — $299/mo] [Good — $79/mo]
```

Left-to-right anchoring: Enterprise's high anchor makes $299 look reasonable.

### Floor, Ceiling, and Target

```
Floor (Cost-Plus):   Cost to serve + minimum margin (30-40%)
Ceiling (Value-Based): 10-30% of quantified customer value
Target (Market):     Competitive benchmark ± 20% based on differentiation
```

## ACV Minimums

Enterprise sales cost (CAC) typically $50K-$150K. Minimum ACV to justify:

| Sales Motion | CAC Estimate | Minimum ACV | Payback Period |
|-------------|-------------|-------------|----------------|
| Inside sales + light touch | $20K-$40K | $50K/year | 6-10 months |
| Field sales + SE support | $50K-$80K | $100K/year | 6-10 months |
| Strategic/Global account | $100K-$150K | $250K/year | 5-7 months |

Rule of thumb: ACV floor ≥ CAC × 1.5-2x for healthy unit economics.

## International Pricing Architecture

### PPP Adjustment Factors

Adjust US pricing by country purchasing power:

| Region | PPP Factor | Example (US=$100K) |
|--------|-----------|---------------------|
| Western Europe | 0.85-1.0 | $85K-$100K |
| Southern Europe | 0.60-0.80 | $60K-$80K |
| Eastern Europe | 0.35-0.55 | $35K-$55K |
| Latin America | 0.40-0.60 | $40K-$60K |
| India/SEA | 0.20-0.40 | $20K-$40K |
| ANZ | 0.80-0.95 | $80K-$95K |

### Local Entity vs International MSA

| Structure | Setup Time | Cost | Risk |
|-----------|-----------|------|------|
| Local entity | 3-6 months per country | $20K-$50K setup + annual compliance | Low — contracts governed by local law |
| International MSA | 2-4 weeks | $5K-$15K legal review | Medium — enforceability varies by jurisdiction |
| Reseller/partner | 1-3 months partner recruitment | 15-30% margin to partner | Low-medium — partner absorbs local legal risk |
