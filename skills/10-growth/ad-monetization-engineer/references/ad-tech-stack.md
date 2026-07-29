# Ad Tech Stack Architecture

## Stack Layers

### 1. Ad Server (Google Ad Manager / GAM)
- Central nervous system of ad operations
- Manages inventory, line items, orders, yield groups
- Delivers ads to ad units based on targeting and priority
- Handles direct-sold, programmatic guaranteed, and remnant inventory

### 2. SSP / Exchange
- Connects publisher inventory to demand sources
- Google Ad Exchange (AdX) is the largest
- Key SSPs: Magnite, PubMatic, Index Exchange, Xandr, OpenX
- Run real-time auctions for each impression

### 3. Header Bidding Wrapper
- Prebid.js: open-source, community-maintained
- Amazon TAM (Transparent Ad Marketplace): Amazon's server-side solution
- Google Open Bidding (formerly EBDA): Google's server-to-server exchange
- Wrapper manages bidder timeout, currency conversion, bid validation

### 4. Demand Sources
- Direct-sold: highest CPM, requires sales team
- Programmatic guaranteed: fixed CPM, reserved inventory
- Private Marketplace (PMP): invite-only, deal ID based
- Preferred deals: fixed CPM, non-guaranteed
- Open auction: lowest CPM, fills remnant inventory

### 5. Analytics Layer
- GAM reporting: impression-level data
- Prebid Analytics: bidder performance, timeout rates, win rates
- Third-party: Moat, IAS, DoubleVerify for viewability/verification
- Custom: data warehouse (BigQuery, Snowflake) for revenue attribution

## Demand Type Comparison

| Type | CPM Relative | Fill Rate | Sales Effort | Latency |
|------|-------------|-----------|--------------|---------|
| Direct-Sold | 100% (baseline) | Variable | High | Low |
| Programmatic Guaranteed | 70-90% | Guaranteed | Medium | Low |
| PMP Deal | 60-80% | Medium-High | Low-Medium | Low |
| Preferred Deal | 50-70% | Medium | Low | Low |
| Open Auction | 20-50% | High | None | Medium |
| House/Remnant | 5-15% | Very High | None | Low |

## Key Decisions
- Self-hosted vs managed ad ops
- Single SSP vs multi-SSP waterfall
- Client-side vs server-side header bidding
- Unified vs per-bidder price floors
