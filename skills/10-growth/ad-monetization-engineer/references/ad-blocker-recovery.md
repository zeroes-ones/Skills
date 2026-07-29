# Ad-Blocker Recovery Strategies

## Detection

### Client-Side Detection

```javascript
// Bait method: create a fake ad element and check if it's hidden
async function detectAdBlocker() {
  const bait = document.createElement('div');
  bait.className = 'adsbox pub_300x250';
  bait.style.cssText = 'position:absolute;left:-9999px;';
  document.body.appendChild(bait);
  await new Promise(r => setTimeout(r, 100));
  const blocked = bait.offsetHeight === 0;
  bait.remove();
  return blocked;
}
```

### Ad Slot Empty Check
- Monitor ad slots: if ad server returns no ad consistently for a user, they may be blocking
- Compare fill rate: if a user segment consistently has 0% fill, suspect blocking

### Third-Party Solutions
- **Blockthrough**: ad-blocker recovery with acceptable ads
- **Admiral**: visitor relationship management including ad-block recovery
- **Uponit**: ad-blocker recovery and analytics

## Recovery Strategies

### 1. Messaging (Lowest Risk)
- "We notice you're using an ad blocker. Ads support our free content."
- Options: whitelist us / subscribe for $X/month / continue with ads
- Single polite message — not a persistent nag
- GDPR-compliant: no tracking for wall detection

### 2. Acceptable Ads Program
- Join the Acceptable Ads Committee program
- Adblock Plus whitelist for complying sites
- Strict criteria:
  - No animation or auto-play
  - Clearly labeled as advertising
  - Above content, not inline
  - Size limitations
  - One ad per page maximum through this program

### 3. Ad Reinsertion (Technical Risk)
- Serve ads from first-party domain to bypass filter lists
- DNS CNAME cloaking: map first-party subdomain to ad server
- **Risk**: Google policy violation if deceptive, filter list updates catch on
- **Legal risk**: GDPR/CCPA implications if circumventing user choice

### 4. Paywall / Subscription Upsell
- "Support us with $3.99/month for ad-free experience"
- Works best for content-heavy sites (news, analysis)
- Must offer genuine value behind paywall
- Conversion rates: 0.5-3% of ad-blocking users

## Subscription vs Ads Hybrid Model
- Freemium: free with ads, paid ad-free
- Metered: X articles/month free with ads, then subscribe
- Donation: "If you use an ad blocker, consider a one-time donation"
- Newsletter upsell: collect email in exchange for ad-free reading

## Measuring Recovery
- Ad-block rate: % of users blocking ads
- Recovery rate: % of ad-blocking users who whitelist or subscribe
- Revenue recovered: $ from recovered impressions
- Subscription revenue: $ from ad-block users who subscribe
