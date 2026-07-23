# 3. Legal Basis Decision Framework

Choosing the wrong legal basis is one of the most common GDPR violations and one of the hardest to fix retroactively (you cannot switch legal bases mid-stream without a new collection event). This framework walks through each legal basis, when to use it, and how to document it.

### 3.1 Consent (Art. 6(1)(a))

Consent is the most demanding legal basis and the most widely misunderstood.

**Valid consent checklist -- all must be YES:**

| Criterion | Test | Non-compliant example |
|---|---|---|
| **Freely given** | Can the data subject refuse without detriment? Is there a genuine choice? | To use our app, you must agree to marketing emails. (Bundling consent with service access = not freely given.) |
| **Specific** | Is consent granular per purpose? One consent per processing purpose. | A single checkbox: I agree to the Terms and Privacy Policy. (Bundling multiple purposes = not specific.) |
| **Informed** | Has the data subject been told: controller identity, purpose of each processing activity, types of data, right to withdraw, existence of automated decision-making, transfer to third countries and safeguards? | We use cookies to improve your experience. (Not specific enough about what data, which cookies, for what purposes.) |
| **Unambiguous** | Clear affirmative action. No pre-ticked boxes. Silence or inactivity is not consent. | A pre-ticked Sign me up for the newsletter checkbox. |
| **Withdrawable** | Must be as easy to withdraw as to give. At any time. No detriment for withdrawal. | Requiring a phone call to withdraw consent that was given by a single click. |
| **Named parties** | All controllers and processors relying on the consent must be named at the time of collection. | We and our partners -- which partners? What do they do with the data? |
| **Not conditional** | Consent cannot be a condition of service if the processing is not necessary for that service (Art. 7(4), bundling prohibition). | Accept all cookies or leave the site. (Cookie wall -- see Section 5 below.) |

**Consent record requirements (Art. 7(1)):** Must be able to demonstrate consent was given. Store: timestamp, consent text shown at the time, consent string/token, IP address, user agent, banner/notice version, purposes consented to, and withdrawal mechanism.

**When consent is the RIGHT choice:**
- Marketing communications (email, SMS, push notifications)
- Non-essential cookies and trackers (analytics, advertising, personalization)
- Processing special categories of data where no other Art. 9(2) basis applies
- Any processing that the data subject would not reasonably expect

**When consent is the WRONG choice:**
- Employment relationships (power imbalance -- consent is rarely freely given)
- Processing necessary to fulfill a contract (use Art. 6(1)(b) instead)
- Public authorities performing their tasks (use Art. 6(1)(e) instead)

### 3.2 Legitimate Interest (Art. 6(1)(f))

Legitimate interest is the most flexible legal basis -- but it requires a documented balancing exercise, and it is not available to public authorities performing their tasks.

**The Legitimate Interest Assessment (LIA) -- 3-Part Test:**

**Part 1: Purpose Test** -- Is there a legitimate interest?
- The interest must be lawful (not contrary to any law).
- The interest must be sufficiently specific. Commercial interest or business purposes is too vague. Examples of established legitimate interests: fraud prevention, direct marketing (to existing customers about similar products -- soft opt-in under ePrivacy), network and information security, intra-group administrative transfers, whistleblowing schemes (within limits).
- Document: What is the specific interest we are pursuing? Who benefits? How does this align with our business purpose as understood by data subjects?

**Part 2: Necessity Test** -- Is the processing necessary for that interest?
- Necessary means: is there a less intrusive way to achieve the same purpose? If you can achieve the same result with aggregated, anonymized, or pseudonymized data, the processing of personal data is not necessary.
- Document: Can we achieve this purpose without processing personal data? Can we achieve it with less data? Can we achieve it with less intrusive means? What alternatives did we consider and why were they rejected?

**Part 3: Balancing Test** -- Does the individual's interests override the legitimate interest?
- Consider: the nature of the data (is it sensitive? is it publicly available?), the reasonable expectations of the data subject (would they be surprised?), the status of the controller and data subject (is there a power imbalance? is the data subject a child?), the impact on the data subject (could this cause harm, distress, discrimination, loss of control?), the safeguards applied (pseudonymization, opt-out mechanisms, enhanced transparency).
- If the impact outweighs the interest, you cannot use legitimate interest.
- Document the balancing conclusion: The balancing test weighs in favor of [controller/data subject] because [reasoning]. Safeguards applied: [list].

**When legitimate interest is appropriate:**
- Fraud detection and prevention
- IT security monitoring (IDS/IPS, log analysis for threats)
- Direct marketing to existing customers about similar products (with opt-out -- this is the ePrivacy soft opt-in)
- Internal reporting and analytics using pseudonymized data
- Business continuity and disaster recovery (backups containing personal data)

**When legitimate interest is NOT appropriate:**
- Any processing where consent is required by ePrivacy (cookies, electronic marketing to non-customers)
- Processing special categories of data (Art. 9 provides its own exhaustive list of exceptions)
- Processing that would surprise or distress the data subject
- Processing children's data for marketing or profiling

### 3.3 Contract Necessity (Art. 6(1)(b))

This is the most narrowly interpreted legal basis. Necessary for the performance of a contract means: without this processing, the contract cannot be performed. Not helpful for business, not mentioned in the terms, but *strictly necessary*.

**The Contract Necessity Test:**
- Is the processing objectively necessary to deliver the core service the data subject has requested?
- Would the contract be impossible to perform without this processing?
- Is there a less intrusive way to perform the contract?

**Qualifies as contract necessity:**
- Processing a delivery address to ship a purchased item
- Processing payment information to charge for a subscription
- Processing an email address to send a password reset link
- Processing a username to display in a multiplayer game

**Does NOT qualify as contract necessity:**
- Using purchase history to recommend products (this is a separate purpose -- use legitimate interest with opt-out, or consent)
- Sharing email with marketing partners (separate purpose -- requires consent)
- Profiling user behavior to improve the service (this is not necessary to deliver the service the user signed up for -- use legitimate interest or consent)
- Sending promotional emails about service upgrades (marketing -- requires consent or soft opt-in)

**Critical distinction -- services vs. features:** Just because a feature is described in your terms does not make all associated data processing contractually necessary. The test is objective, not contractual. You cannot contract your way into a wider legal basis.

### 3.4 Legal Obligation (Art. 6(1)(c))

Processing that is necessary for compliance with a legal obligation to which the controller is subject.

**Must be:**
- A specific law (EU or Member State law) -- not a general government request or recommendation.
- The obligation must be mandatory, not optional.
- **Examples by industry:**
  - **Financial services:** AML/KYC under 4AMLD/5AMLD -- customer due diligence, transaction monitoring, suspicious activity reporting, record-keeping for 5 years post-relationship.
  - **Employment:** Tax withholding and social security reporting, workplace safety reporting, minimum wage compliance records.
  - **Healthcare:** Medical device adverse event reporting, clinical trial documentation (ICH GCP), prescription records.
  - **Telecommunications:** Data retention under national laws (subject to CJEU case law limitations -- see Tele2 Sverige, La Quadrature du Net).
  - **E-commerce:** Invoice retention (typically 6-10 years depending on Member State), VAT reporting.

### 3.5 Vital Interests (Art. 6(1)(d))

Narrowly limited to processing necessary to protect the vital interests of the data subject or another natural person -- life-or-death situations. Emergency medical treatment, disaster response, humanitarian emergencies. Cannot be used for routine processing. If another legal basis is available (e.g., consent in a medical context), use that instead.

### 3.6 Public Task (Art. 6(1)(e))

Only available to public authorities or private organizations performing a task in the public interest vested by law. Not applicable to most commercial organizations.

### 3.7 Decision Tree: Which Legal Basis?

```
START: Is the processing necessary to comply with a specific, mandatory law?
  |-- YES -> Use Legal Obligation (Art. 6(1)(c))
  |-- NO -> Is it strictly necessary to perform the contract with the data subject?
            |-- YES -> Use Contract Necessity (Art. 6(1)(b))
            |-- NO -> Is the data subject in a life-or-death situation?
                      |-- YES -> Use Vital Interests (Art. 6(1)(d))
                      |-- NO -> Is consent required by ePrivacy or for special category data?
                                |-- YES -> Use Consent (Art. 6(1)(a)) -- must meet all validity criteria
                                |-- NO -> Can you pass the LIA 3-part test?
                                          |-- YES -> Use Legitimate Interest (Art. 6(1)(f)) -- document the LIA
                                          |-- NO -> Use Consent (Art. 6(1)(a))
```

**Switching legal bases:** You cannot switch retroactively. If you collected data under consent and the data subject withdraws, you must stop processing -- you cannot pivot to legitimate interest. If you collected under legitimate interest and the data subject objects successfully, you must stop. Choose carefully at collection time and document your reasoning.

---
