# 6. Data Protection Impact Assessments (DPIAs)

A DPIA is a process for identifying and minimizing the data protection risks of a project. It is a legal requirement (Art. 35) for processing that is likely to result in a high risk to individuals. The DPIA must be completed *before* the processing begins.

For a comprehensive DPIA template with all sections elaborated, risk matrix, and fillable indicators, see `references/dpia-template-detailed.md`.

### 6.1 When is a DPIA Required?

The EDPB (WP248) established 9 criteria. A DPIA is required if processing meets **2 or more** of these criteria:

1. **Evaluation or scoring** -- including profiling and predicting behavior (credit scoring, performance assessment)
2. **Automated decision-making with legal or similar significant effect** (hiring algorithms, loan decisions)
3. **Systematic monitoring** -- of publicly accessible areas (CCTV, location tracking in apps)
4. **Sensitive data or highly personal data** -- special categories, financial data, location data, communications data
5. **Data processed on a large scale** -- consider number of subjects, volume of data, duration, geographic extent
6. **Matching or combining datasets** -- from multiple sources in a way that exceeds reasonable expectations
7. **Data concerning vulnerable persons** -- children, employees, patients, asylum seekers, mentally ill persons
8. **Innovative use of technological or organizational solutions** -- AI, machine learning, IoT, biometric identification
9. **Preventing data subjects from exercising a right or using a service** -- deny-listing, fraud databases that block access

**Mandatory DPIA triggers (regardless of criteria count):**
- Systematic and extensive profiling with significant effects
- Large-scale processing of special categories of data or criminal conviction data
- Systematic large-scale monitoring of publicly accessible areas

**National DPA lists:** Many EU DPAs publish their own lists of processing activities that require a DPIA. Check your lead DPA's list. The UK ICO, for example, requires DPIAs for: innovative technology, denylisting, biometric/genetic data, data matching, invisible processing, tracking, targeting children, risk of physical harm.

### 6.2 DPIA Methodology

1. **Describe the processing:** What data? How collected? How stored? Who accesses? How long? What systems? Who are the data subjects? (See detailed template for structured questionnaire.)
2. **Assess necessity and proportionality:** For each purpose -- why is this processing necessary? Why can't less data achieve it? Why can't it be done with less intrusive means?
3. **Identify risks:** Using the WP29 risk criteria, enumerate risks to rights and freedoms. Each risk: describe the risk event, the potential impact, and the likelihood.
4. **Identify mitigation measures:** For each risk, specify the measure (technical or organizational) that reduces likelihood or impact.
5. **Assess residual risk:** After mitigation, is the risk low, medium, or high? If high, consultation with the DPA is required before processing.
6. **Document and sign off:** DPO review, stakeholder approvals, version control.
7. **Integrate into project plan:** DPIA outcomes feed into design decisions, not sit on a shelf.

### 6.3 Risk Assessment Matrix

Use a 5x5 likelihood x severity matrix:

| Likelihood \ Severity | 1 (Minimal) | 2 (Limited) | 3 (Significant) | 4 (Severe) | 5 (Maximum) |
|---|---|---|---|---|---|
| **5 (Almost Certain)** | Medium (5) | High (10) | Extreme (15) | Extreme (20) | Extreme (25) |
| **4 (Likely)** | Medium (4) | Medium (8) | High (12) | Extreme (16) | Extreme (20) |
| **3 (Possible)** | Low (3) | Medium (6) | High (9) | High (12) | Extreme (15) |
| **2 (Unlikely)** | Low (2) | Low (4) | Medium (6) | Medium (8) | High (10) |
| **1 (Rare)** | Low (1) | Low (2) | Low (3) | Medium (4) | Medium (5) |

**Risk acceptance thresholds:**
- Low (1-3): Acceptable, document monitoring plan
- Medium (4-6): Acceptable with ongoing monitoring, periodic review
- High (8-12): Requires additional mitigation; if residual risk remains high after mitigation, DPA consultation
- Extreme (15-25): Stop. Redesign. Processing cannot proceed without fundamental changes.

### 6.4 DPA Consultation (Art. 36)

If the DPIA indicates high residual risk and no mitigation can reduce it, you must consult the DPA before processing. The consultation must include: responsibilities of controller/processor, purposes and means of processing, measures and safeguards, DPO contact details, DPIA, and any other information the DPA requests. The DPA has 8 weeks (extendable to 14) to respond. Processing without consultation when required can result in fines and orders to suspend processing.

---
