# Ad Unit UX Design & Placement

## Viewability Standards (IAB/MRC)
- Display ads: 50% of pixels in viewport for 1 continuous second
- Video ads: 50% of pixels in viewport for 2 continuous seconds
- Large display (242,500+ pixels): 30% of pixels for 1 second

## Placement Patterns

### Above-Fold Placements
- **Leaderboard (728x90)**: top of page, below navigation
- **Billboard (970x250)**: premium above-fold, high viewability
- Rule: never more than 1 above-fold ad on mobile

### Below-Fold Placements
- **Medium Rectangle (300x250)**: in-content, between paragraphs
- **Half Page (300x600)**: sidebar, sticky on scroll
- **Leaderboard (728x90)**: between content sections

### Mobile-Specific
- **Sticky Footer (320x50)**: persists at bottom during scroll
- **Interstitial**: between page transitions, max 1/user/24hr
- **Rewarded**: user opts in for content/reward access

## Ad Density Limits
- Google policy: max 30% ad-to-content ratio
- No more than 1 sticky ad per page
- No ads that float over content
- No auto-refresh faster than 30 seconds

## Cumulative Layout Shift (CLS) Prevention

```css
.ad-slot {
  min-height: 250px;
  width: 300px;
  background: #f5f5f5;
}
.ad-slot::before {
  content: "Advertisement";
  display: block;
  text-align: center;
  color: #999;
  font-size: 12px;
  padding: 4px;
}
```

### CLS Best Practices
- Reserve exact ad slot dimensions in CSS
- Never inject ads above existing content
- Use placeholder backgrounds while ads load
- Lazy load ads below the fold only

## Lazy Loading
- Load ads when within 200-400px of viewport
- Intersection Observer API preferred
- Prebid.js lazy loading via `sendBidsHandler`
- Exclude: first above-fold ad (load immediately for viewability)

## Ad Refresh Logic
- Valid only when ad is in viewport (viewability verified)
- Minimum 30 seconds between refreshes (MRC guideline)
- Use `document.visibilityState` — only refresh when tab is active
- Refresh on: new content load, user interaction, timer
- Never refresh: out-of-view ads, background tabs, inactive users

## User Experience Principles
- Ads must be clearly labeled (not disguised as content)
- Close buttons must be visible and functional
- No auto-playing video with sound
- No flashing or rapidly changing backgrounds
- Native ads must include "Sponsored" or "Ad" label
