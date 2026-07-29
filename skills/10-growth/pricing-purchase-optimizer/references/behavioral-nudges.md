# Behavioral Economics Patterns for Pricing Pages

## Decoy Effect

Add a third option that makes the target option look like the best value.

**Classic Example:**
| Popcorn | Price | Effect |
|---------|-------|--------|
| Small | $3.00 | Anchor — makes medium look cheap |
| Medium | $6.50 | Decoy — priced close to large |
| Large | $7.00 | Target — "only $0.50 more for 50% larger" |

**SaaS Pricing Example:**
| Plan | Price/mo | Users | Storage |
|------|---------|-------|---------|
| Starter | $29 | 5 | 50GB |
| Professional | $79 | 20 | 200GB |
| Business | $99 | 50 | 500GB |

The Business plan is the decoy — priced close to Professional but with 2.5x features. Drives upgrades to Business.

## Anchoring

Display highest-priced tier first (left-to-right) to make subsequent tiers seem affordable.

**Layout:** [Enterprise — Contact Sales] → [Pro — $99/mo] → [Starter — $29/mo]

Left-to-right anchoring: After seeing Enterprise, $99 seems reasonable and $29 seems cheap.

## Social Proof

Place near every CTA. Types in order of credibility:

1. **Customer logos** (recognizable brands = highest trust)
2. **Specific metrics** ("Join 10,000+ companies") vs vague ("Trusted by many")
3. **Testimonials** with name, title, photo, company
4. **Third-party ratings** (G2, Capterra, TrustRadius)
5. **Case study links** ("See how Company X saved $Y")

## Loss Aversion Framing

Frame choices around what customers lose by NOT choosing the better option.

| Weak (Gain Frame) | Strong (Loss Frame) |
|-------------------|---------------------|
| "Save 25% with annual" | "Don't lose $300/year — switch to annual" |
| "Get premium features" | "Stop leaving features on the table" |
| "Try Pro free for 14 days" | "Your 14-day Pro access expires soon" |

## Charm Pricing

| Market | Charm Price | Round Price | Why |
|--------|-----------|-------------|-----|
| Consumer/SMB | $99 | $100 | $99 signals "deal"; brain processes $99 as $90-range |
| Premium consumer | $199 | $200 | Same psychology |
| B2B mid-market | $499 | $500 | $499 still works |
| Enterprise B2B | $5,000 | $4,999 | Round numbers signal transparency and premium positioning |
| Luxury | $1,000 | $999 | Round = premium. Charm pricing signals discount |

## Scarcity (ETHICAL ONLY)

Never create false scarcity. Only use genuine constraints:

✅ **Genuine:** "Beta pricing — first 100 customers lock in this rate for life" (when limited to 100)
✅ **Genuine:** "Launch pricing ends [specific date]" (when pricing actually changes)
❌ **Dark pattern:** "Only 2 spots left!" (when unlimited)
❌ **Dark pattern:** Countdown timer that resets on page refresh

## Social Proof Placement Map

```
[Above Fold]
Customer logos: "Trusted by Stripe, Shopify, Figma, Notion"

[Tier Section]
[Starter CTA]
  ↑ "⭐⭐⭐⭐⭐ 4.8/5 on G2"

[Professional CTA] ← Target tier
  ↑ "Most Popular — 70% of customers choose Pro"
  ↑ Customer testimonial quote

[Enterprise CTA]
  ↑ "Used by 50+ Fortune 500 companies"
```
