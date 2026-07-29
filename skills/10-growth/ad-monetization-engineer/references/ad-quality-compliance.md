# Ad Quality & Compliance

## Made for Advertising (MFA) Detection

### What is MFA?
- Sites created solely to generate ad revenue
- Low-quality content, high ad density, purchased traffic
- Advertisers actively block MFA inventory

### Detection Tools
- **Jounce**: MFA site classification database
- **Deepsee.io**: supply path optimization and MFA detection
- **Pixalate**: ad fraud and quality measurement
- **HUMAN (WhiteOps)**: bot detection and IVT filtering

### Self-Audit Checklist
- [ ] Content-to-ad ratio > 70:30
- [ ] Organic traffic > 50% of total
- [ ] Average time on page > 60 seconds
- [ ] Unique content (not scraped or spun)
- [ ] No clickbait headlines or deceptive ad placement

## Invalid Traffic (IVT)

### GIVT (General Invalid Traffic)
- Known bot user-agents
- Known data center IPs
- Basic filtration at ad server level

### SIVT (Sophisticated Invalid Traffic)
- Advanced bots mimicking human behavior
- Click farms, impression fraud
- Domain spoofing, ad stacking, pixel stuffing
- Requires specialized detection (HUMAN, Pixalate, DoubleVerify)

## ads.txt / app-ads.txt

### Why Required
- Prevents domain spoofing (fraudsters selling inventory they don't own)
- IAB mandate — demand sources check ads.txt before bidding
- Missing ads.txt = $0 from premium demand sources

### Format

```
# ads.txt
google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
rubiconproject.com, 12345, DIRECT, 0bfd66d529a12345
appnexus.com, 1234, RESELLER, f5ab79cb980f1234
```

### Verification
- Must be at `https://domain.com/ads.txt`
- Crawlable by demand sources
- Updated when adding/removing demand partners
- Audit quarterly for stale entries

## sellers.json
- Google-required transparency file
- Lists all seller entities with business details
- Published at `https://domain.com/sellers.json`
- Must match ads.txt entries

## Brand Safety
- **IAS (Integral Ad Science)**: pre-bid brand safety filtering
- **DoubleVerify**: viewability, fraud, brand suitability
- Block categories: adult, violence, hate speech, drugs, weapons
- Contextual targeting: allow advertisers to target/avoid specific content

## Privacy & Consent

### GDPR (EU)
- Consent Management Platform (CMP) required
- TCF v2.2 framework integration
- Legal basis: consent or legitimate interest
- Data minimization: only request necessary permissions

### CCPA/CPRA (California)
- Right to opt-out of sale/sharing of personal information
- "Do Not Sell or Share My Personal Information" link
- GAM: enable restricted data processing for opted-out users

### COPPA (Children's Online Privacy)
- No behavioral advertising on child-directed content
- No interest-based ad targeting
- No personal information collection without parental consent
- Must tag ad requests as child-directed

### ATT (App Tracking Transparency)
- iOS 14.5+: must request tracking permission via ATT prompt
- Without IDFA: use SKAdNetwork for attribution
- Impact: 50-70% of users opt out, significantly reducing eCPM
