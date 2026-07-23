# 5. Cookie Compliance

Cookie compliance sits at the intersection of the ePrivacy Directive (2002/58/EC, as amended by 2009/136/EC) and GDPR. The ePrivacy Directive (the lex specialis for electronic communications) requires consent for storing or accessing information on a user's terminal equipment, with a narrow exemption for strictly necessary cookies. GDPR then governs what you do with any personal data collected via those cookies.

### 5.1 ePrivacy Directive + GDPR Interplay

**The rule:** You must obtain prior consent before setting any cookie or tracker that is not strictly necessary (ePrivacy Art. 5(3)). GDPR then provides the standard for what valid consent looks like (freely given, specific, informed, unambiguous -- Art. 4(11) and Art. 7). This means cookie consent must meet ALL the GDPR consent validity criteria.

**Strictly necessary exemption** covers only:
- Session cookies for login state (but not persistent login cookies)
- Shopping cart cookies
- Load-balancing cookies
- Security cookies (CSRF tokens)
- Cookies remembering cookie preferences (ironically)

**The exemption does NOT cover:**
- Analytics cookies (even first-party) -- unless they are essential to providing the service explicitly requested by the user
- A/B testing cookies
- Personalization cookies
- Advertising/targeting cookies
- Social media tracking pixels

### 5.2 Consent Management Platform (CMP) Selection Criteria

When selecting a CMP (OneTrust, Cookiebot, Usercentrics, Cookie Information), evaluate:

| Criterion | Requirement |
|---|---|
| **IAB TCF v2.2 compliance** | Must support the Transparency & Consent Framework for programmatic advertising |
| **Granular consent** | Per-purpose and per-vendor toggles, not just accept all / reject all |
| **Prior blocking** | Must block cookies/scripts before consent -- not just fire and then honor withdrawal |
| **Consent logging** | Records timestamp, consent string, IP, user agent, banner version, purpose list, vendor list |
| **Consent refresh** | Configurable refresh interval (13 months max), re-prompt on material change |
| **Withdrawal mechanism** | Persistent floating button or link; as easy to withdraw as to give |
| **Multi-domain/language** | If you operate across domains and languages |
| **Accessibility** | WCAG 2.1 AA compliant consent interface |
| **API/Webhook** | Programmatic access to consent state for downstream systems |
| **GPC signal** | Honors Global Privacy Control browser signal as opt-out |

### 5.3 Cookie Categorization

| Category | Description | Examples | Consent Required? |
|---|---|---|---|
| **Strictly Necessary** | Essential for the website to function; requested service cannot be provided without them | Session cookies, CSRF tokens, load balancers, shopping cart, cookie preferences | No |
| **Performance / Analytics** | Collect information about how visitors use the site (page views, time on site, error messages) | Google Analytics, Mixpanel, Hotjar heatmaps | Yes |
| **Functional** | Enable enhanced functionality and personalization (remembering preferences, language selection) | Language preference, region selector, video player cookies | Yes |
| **Targeting / Advertising** | Track browsing across sites to build profiles and serve targeted ads | Facebook pixel, Google Ads, retargeting, programmatic ad cookies | Yes (explicit) |

### 5.4 Consent Logs

Per Art. 7(1) accountability, you must be able to demonstrate that consent was given. Log every consent event:

| Field | Example |
|---|---|
| **Consent ID** | `cons_abc123def456` |
| **Timestamp** | `2026-01-15T14:32:17Z` |
| **Consent string** | IAB TCF consent string (e.g., `CO4QHXgO4QHXg...`) |
| **IP address** | `203.0.113.42` (hashed after 30 days) |
| **User agent** | `Mozilla/5.0 ... Chrome/120.0` |
| **Banner version** | `v3.2.1` |
| **Purposes consented** | `[store_and_access_info, create_personalised_ads_profile, measure_ad_performance, ...]` |
| **Purposes rejected** | `[use_limited_data_to_select_content]` |
| **Vendors consented** | `[Google (755), Facebook (89), ...]` |
| **GPC signal honored** | `false` |
| **Consent scope** | Domain(s) covered by this consent |

Store consent logs in an append-only, immutable data store. Retain for the life of the processing plus the statute of limitations for legal claims (typically 3-7 years after the consent expires or is withdrawn).

### 5.5 Consent Refresh

- **Maximum validity:** 13 months from the date consent was given (per IAB TCF policy and advocated by several EU DPAs -- notably CNIL). After 13 months, re-prompt.
- **Material change triggers:** If you add a new purpose, new vendor, new data category, or change how data is used, you must re-obtain consent. The existing consent does not cover the new processing.
- **CNIL guidance:** Recommends 6-month consent validity for advertising cookies specifically.

### 5.6 Cookie Walls Prohibition

A cookie wall is a mechanism that conditions access to a website or service on the user's acceptance of all cookies. The EDPB has stated (Opinion 04/2012, confirmed in post-GDPR guidance) that cookie walls are not valid consent because consent is not freely given when access is conditional. If your only options are "Accept all cookies" or "Leave the site," you do not have valid consent.

**Compliant alternative:** Offer a genuine choice. If the user declines non-essential cookies, they still access the content. You may offer a cookie-free paid alternative (e.g., ad-free subscription), but the free service cannot be contingent on accepting tracking.

---
