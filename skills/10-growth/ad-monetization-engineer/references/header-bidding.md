# Header Bidding Setup Guide

## Prebid.js Configuration

### Basic Setup

```javascript
pbjs.setConfig({
  debug: false,
  priceGranularity: 'medium',
  enableSendAllBids: false,
  useBidCache: true,
  bidderTimeout: 1500,
  timeoutBuffer: 200
});
```

### Bidder Adapters
Key demand partners and their Prebid adapter codes:
- **appnexus** — Xandr/AppNexus
- **rubicon** — Magnite
- **pubmatic** — PubMatic
- **ix** — Index Exchange
- **amazon** — Amazon TAM (server-side only)
- **sovrn** — Sovrn
- **openx** — OpenX
- **triplelift** — TripleLift (native)
- **sharethrough** — Sharethrough (native)

### Timeout Management
- Standard: 1000-2000ms total auction timeout
- Bidder timeout = auction timeout - timeoutBuffer
- Monitor: timeout rate per bidder, average response time
- Adjust: increase for high-value bidders, decrease for slow responders

### Price Floors

```javascript
pbjs.setConfig({
  floors: {
    enforcement: {
      floorsEnabled: true,
      enforcementRate: 100
    },
    data: {
      currency: 'USD',
      schema: {
        fields: ['mediaType', 'size', 'domain'],
        values: {
          'banner|728x90': 0.50,
          'banner|300x250': 0.75,
          'banner|300x600': 1.00,
          'video': 15.00
        }
      }
    }
  }
});
```

### Floor Module (Dynamic)
- Use `priceFloors` module for per-bidder dynamic floors
- Integrate historical performance data
- Adjust by: geo, device, ad unit, time of day, day of week

## Prebid Server (S2S)
- Reduces client-side latency by moving auction to server
- More bidder connections (no browser connection limits)
- Cookie sync still required for user matching
- Best for: high-traffic sites, mobile web, video-heavy inventory

## Hybrid Setup
- Client-side: display banners (fast, cookie-based)
- Server-side: video, native (high-value, connection-intensive)
- Use Prebid.js + Prebid Server together

## Key Metrics
- Bid rate: % of auctions receiving at least one bid
- Win rate: % of bids that win the impression
- Timeout rate: % of bidders exceeding timeout
- Avg CPM per bidder
- Revenue lift vs. no header bidding
