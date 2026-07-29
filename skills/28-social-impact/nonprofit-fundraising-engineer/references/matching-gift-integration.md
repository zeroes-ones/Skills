# Matching Gift Integration
> Reference: Double the Donation, Benevity, CyberGrants API integration

## Major Matching Gift Platforms

| Platform | API | Coverage | Integration Complexity |
|----------|-----|----------|----------------------|
| Double the Donation | REST API, JavaScript widget | 20,000+ companies | Low (drop-in widget) |
| Benevity | REST API | Enterprise (Fortune 500 focused) | Medium |
| CyberGrants | REST API | Enterprise | Medium |

## Double the Donation Integration Flow

1. Donor completes donation
2. Post-donation screen: "See if your employer matches" + company search
3. Donor searches/selects company
4. API returns: match ratio, min/max amounts, eligible employees, submission instructions
5. If eligible: auto-submit or provide link to employer portal
6. Track status: submitted → approved → received in CRM

## Match Pipeline Tracking

CRM Custom Fields:
- match_eligible (boolean)
- match_company (text)
- match_ratio (e.g., "1:1")
- match_amount_potential (calculated)
- match_status (pending, submitted, approved, received)
- match_received_date
- match_received_amount

## Revenue Impact
- 65% of donors don't know their employer matches (Double the Donation research)
- In-flow matching lookup increases match completion 3-5x
- Average match: $500-$1,000 per donor
- Organizations with matching gift integration report 10-25% additional revenue

Version: 1.0
