# Startup Legal Checklist

> **Author:** Sandeep Kumar Penchala

A comprehensive legal playbook for early-stage startups. Covers incorporation through compliance. Companion to the [Legal Advisor SKILL.md](../SKILL.md).

---

## 1. Incorporation

### Entity Choice: Delaware C-Corp vs LLC

| Factor | Delaware C-Corp | LLC |
|---|---|---|
| **Investor preference** | Required by VCs | Uncommon for VC-backed |
| **Tax treatment** | Double taxation (corp + personal) | Pass-through (single) |
| **Stock issuance** | Authorized shares, classes (common/preferred) | Membership units |
| **Option pool** | Standard; ISO/NSO qualified | Taxed differently; less standard |
| **Corporate governance** | Board, officers, annual meetings | Operating agreement governs |
| **Cost** | ~$500–$2,000 formation; $400+ annual franchise tax | ~$500–$1,500 formation; ~$300 annual |
| **Exit readiness** | Straightforward acquisition or IPO | Conversion to C-Corp often needed pre-exit |

### Incorporation Steps (Delaware C-Corp)
1. Reserve company name with Delaware Division of Corporations
2. File Certificate of Incorporation (include authorized shares, par value)
3. Appoint registered agent (e.g., CSC, CT Corporation, Incorporate.com)
4. Adopt Bylaws at organizational board meeting
5. Issue founder stock with vesting (see below)
6. File 83(b) election within 30 days of stock issuance
7. Obtain EIN from IRS (Form SS-4)
8. Open business bank account
9. File Form D (if raising via securities exemption)
10. Register as foreign entity in state of operation

---

## 2. Founder Agreements

### IP Assignment
Every founder must sign a **Proprietary Information and Inventions Assignment Agreement (PIIA)** transferring all relevant IP to the company. Without it, a departing founder retains their IP, which can kill fundraising or acquisition.

### Vesting Schedule
Standard: **4-year vesting with 1-year cliff**

```
Year 1: 0% vested (cliff)
Month 13+: 25% vests immediately at cliff, then 1/36th monthly
Year 4: 100% vested
```

### Decision Rights
- CEO: day-to-day operations
- Unanimous consent: financing, M&A, IP sale, new equity grants, budget > $X
- Deadlock resolution: buy-sell provision or third-party mediator

### Departure Clauses
- **Voluntary resignation (without cause):** unvested shares forfeited; vested shares retained
- **Termination for cause:** board may repurchase vested shares at cost
- **Death/disability:** accelerate vesting by 12 months (typical)
- **Right of first refusal (ROFR):** company gets first shot at purchasing departing founder shares

---

## 3. Cap Table Management

| Term | Definition |
|---|---|
| **Authorized shares** | Max shares the certificate allows (e.g., 10M common, 5M preferred) |
| **Issued & outstanding** | Shares actually sold/delivered (founders + investors + exercised options) |
| **Fully diluted** | Issued + outstanding options + warrants + convertible notes/SAFEs |
| **Option pool** | Reserved shares for future employees; typically 10–20% post-Series A |
| **Liquidation preference** | Order of payout in exit; preferred stock paid first |

### Cap Table Template (Columns)
`Shareholder | Share Class | Shares | Ownership % | Fully Diluted % | Issue Date | Vesting Status`

> **Pro tip:** Use software (Carta, Pulley, AngelList) once you have >5 shareholders. Spreadsheet errors are the #1 cap table mistake.

---

## 4. Fundraising Documents

### SAFE (Simple Agreement for Future Equity)
| Feature | Pre-Money SAFE | Post-Money SAFE |
|---|---|---|
| **Dilution clarity** | Dilution opaque until priced round | Dilution known at signing |
| **Founder ownership** | Harder to forecast | Easier to model |
| **Investor preference** | Older standard (pre-2018) | Current market (YC standard) |
| **Conversion** | Converts in next priced round at discount/cap | Same mechanism |

### Convertible Note vs SAFE vs Series Seed

| Feature | Convertible Note | SAFE | Series Seed |
|---|---|---|---|
| **Debt or equity?** | Debt (with interest) | Equity-like (not debt) | Equity |
| **Maturity date** | Yes (12–24 months) | None | N/A (priced round) |
| **Interest rate** | 2–8% | None | N/A |
| **Valuation** | Cap + discount on conversion | Cap + discount on conversion | Priced valuation |
| **Governance** | None | None | Board seat possible |
| **Cost** | $2K–$5K legal | $500–$2K legal | $15K–$40K legal |
| **Best for** | Bridge rounds | Pre-seed / friends & family | Seed/Series A |

---

## 5. IP Protection

| Type | What It Protects | Timeline | Cost (USD) |
|---|---|---|---|
| **Provisional patent** | Invention; 12-month placeholder | 2–4 weeks to file | $2K–$5K |
| **Non-provisional patent** | Full utility/design patent | 1–3 years to grant | $10K–$25K+ |
| **Trademark (USPTO)** | Brand name, logo, slogan | 9–12 months | $1K–$2K per class |
| **Copyright** | Original creative works (code, designs, content) | Automatic + registration optional | $45–$65 e-filing |
| **Trade secret** | Proprietary algorithms, processes, customer lists | Ongoing (NDA + access controls) | Internal policy cost |

### Patent Strategy for Startups
1. File provisional first (lower cost, locks priority date)
2. Assess commercialization within 12 months
3. Convert to PCT (international) or non-provisional if worth protecting
4. **Do NOT publicly disclose before filing** — destroys international patent rights

---

## 6. Data Privacy Compliance

### GDPR (EU Users)
- Lawful basis required (consent, legitimate interest, contract)
- Data Processing Agreement (DPA) with vendors
- Right to access, rectify, delete, port data
- Data Protection Officer (DPO) for large-scale processing
- 72-hour breach notification
- Fines: up to 4% of global annual revenue or €20M

### CCPA (California Residents)
- Right to know what data is collected
- Right to delete personal information
- Right to opt out of sale/sharing
- "Do Not Sell My Personal Info" link on website
- Applies to: revenue > $25M OR 100K+ consumer records OR 50%+ revenue from data sales

### DPA Template Checklist
- [ ] Categories of data processed
- [ ] Purpose and duration of processing
- [ ] Sub-processor authorization
- [ ] Security measures (encryption, access controls)
- [ ] Breach notification obligations
- [ ] Data subject request handling
- [ ] Return/deletion of data on termination

---

## 7. Commercial Contracts

### Key Contract Types

| Contract | Purpose | Key Clauses to Negotiate |
|---|---|---|
| **MSA (Master Services Agreement)** | Governs overall vendor relationship | Limitation of liability, IP ownership, indemnification |
| **SOW (Statement of Work)** | Specific project scope/deliverables | Acceptance criteria, timeline, payment milestones |
| **SLA (Service Level Agreement)** | Uptime/performance guarantees | Availability (e.g., 99.9%), credits for breach, carve-outs |
| **NDA (Non-Disclosure Agreement)** | Protect confidential info | Duration (2–5 years), residual clause, mark-as-confidential |
| **Vendor Agreement** | Purchase of goods/services | Payment terms (Net 30/60), termination for convenience |

### Limitation of Liability: Cheat Sheet
- Cap at fees paid (12 months trailing) — most favorable
- Cap at fees paid (contract value) — standard
- Uncapped for: IP infringement, confidentiality breach, gross negligence, willful misconduct
- No consequential damages (both sides)

---

## 8. Employment Law

### Contractor vs Employee: IRS 20-Factor Test (Key Factors)
1. **Behavioral control:** Does company control *how* work is done? → Employee
2. **Financial control:** Who bears profit/loss risk? Own tools? → Contractor
3. **Relationship:** Benefits? Indefinite duration? Core business function? → Employee

> **Misclassification penalty:** Back taxes, benefits, penalties up to 41.5% of compensation. In California, AB5 makes contractor classification very difficult for core-business roles.

### Required Employment Docs
- Offer letter (at-will, salary, title, start date)
- Confidential Information and Invention Assignment Agreement (CIIAA)
- Equity grant notice (Form of Stock Option Agreement)
- I-9 verification
- Employee handbook (anti-harassment, code of conduct, benefits)

### Equity Grant Docs for Employees
- **ISO (Incentive Stock Option):** tax-advantaged, employees only, $100K/year limit, 90-day post-termination exercise
- **NSO (Non-Qualified Stock Option):** flexible, advisors/contractors OK, ordinary income on exercise
- **RSU (Restricted Stock Unit):** no purchase needed, taxable at vest, common at growth/late stage

---

## 9. Terms of Service & Privacy Policy

### Terms of Service — Must-Have Clauses
- Acceptance of terms
- Account registration and responsibilities
- Acceptable use policy
- Intellectual property rights (who owns what)
- Payment terms and refunds
- Limitation of liability and warranty disclaimers
- Termination and account deletion
- Governing law and dispute resolution (arbitration clause)
- Changes to terms (notification method)

### Auto-Generated vs Attorney-Drafted
| Factor | Generator (Termly, Termageddon) | Attorney |
|---|---|---|
| **Cost** | $0–$500/year | $3K–$15K |
| **Compliance updates** | Automatic | Manual (billed hourly) |
| **Customization** | Templates, limited | Full customization |
| **Liability protection** | Basic | Stronger (jurisdiction-specific) |
| **Best for** | Pre-revenue, simple SaaS | Revenue-generating, regulated industries |

---

## 10. Industry-Specific Compliance

| Regulation | Industry | Key Requirement | Penalty Range |
|---|---|---|---|
| **HIPAA** | Healthtech (PHI handling) | BAAs, encryption, audit controls, breach notification | $100–$50K/violation, up to $1.5M/year |
| **PCI DSS** | Fintech / Payment processing | Secure cardholder data, penetration testing, access control | $5K–$100K/month; loss of processing |
| **SOC 2** | Enterprise SaaS | Trust services criteria (security, availability, confidentiality) | Contractual (customer loss) |
| **FERPA** | Edtech (student records) | Parental consent, data access/amendment rights | Loss of federal funding |
| **FINRA/SEC** | Fintech (broker-dealer, RIA) | Registration, recordkeeping, communications surveillance | Fines + bars from industry |

### Compliance Roadmap
1. **Pre-seed:** Terms + Privacy Policy (generator OK), basic IP protection
2. **Seed:** Attorney-drafted ToS/PP, DPA template, SOC 2 gap assessment
3. **Series A:** SOC 2 Type I audit, insurance (D&O, E&O, cyber), industry-specific compliance
4. **Series B+:** SOC 2 Type II, ISO 27001, dedicated compliance officer

---

*This checklist is educational, not legal advice. Always consult qualified counsel for your specific situation.*
