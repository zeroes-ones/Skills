# Mobile Ad Mediation Guide

## Mediation Platforms

### Google AdMob Mediation
- Largest ad network + mediation combined
- Integrated with Google Ad Manager
- Supports waterfall and in-app bidding
- Native integration with AdMob Network + third-party networks

### ironSource LevelPlay
- Strong in gaming vertical
- In-app bidding support via ironSource Exchange
- Rewarded video and interstitial optimization
- Acquired by Unity (merged with Unity Ads)

### MAX (AppLovin)
- High eCPM for gaming apps
- In-app bidding with AppLovin Exchange
- Supports 25+ ad networks
- Real-time auction for every impression

### Unity LevelPlay
- Formerly ironSource LevelPlay
- Gaming-focused mediation
- Rewarded video specialization
- A/B testing tools for waterfall optimization

## Waterfall vs In-App Bidding

### Waterfall

```
Request → Network A ($15 CPM) → No fill → Network B ($10 CPM) → No fill → Network C ($5 CPM) → Fill

```

- Sequential — high CPM first, fall back
- Latency: each hop adds 200-500ms
- Inefficient: high-CPM networks get first look even if they wouldn't have bought

### In-App Bidding

```

Request → All networks bid simultaneously → Highest bid wins
```

- Unified auction — all demand sources compete in real-time
- Lower latency: single round-trip
- Higher yield: true price competition
- Revenue lift: 10-30% over waterfall

## Ad Units for Mobile

| Format | eCPM Range | Best For | UX Impact |
|--------|-----------|----------|-----------|
| Rewarded Video | $10-$50 | Gaming, utility apps | Opt-in, positive UX |
| Interstitial | $5-$20 | Natural breaks | Medium — interrupts flow |
| Native | $2-$10 | Content apps, social | Low — blends with content |
| Banner | $0.50-$3 | All apps | Low — persistent but small |
| MREC (300x250) | $2-$8 | Tablet, in-content | Low-Medium |

## Frequency Capping
- Banner: unlimited but rotate creatives
- Interstitial: max 1 per 3 minutes, 3 per session
- Rewarded: user initiates — no cap needed
- Native: unlimited but relevancy matters

## ATT Compliance (iOS)
- Request tracking via ATT prompt
- If denied: use SKAdNetwork for campaign measurement
- Serve non-personalized ads to opted-out users
- eCPM impact: 30-60% reduction for opted-out users
- Implement consent management via CMP

## Performance Monitoring
- ARPDAU (Average Revenue Per Daily Active User)
- eCPM by ad unit and network
- Fill rate per network
- Latency per auction
- User retention impact of ad frequency
