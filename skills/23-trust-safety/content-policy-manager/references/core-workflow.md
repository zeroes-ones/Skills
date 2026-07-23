# Core Workflow — Full Implementation

<!-- STANDARD: 3min -->

### Phase 1 — Medical Misinformation Taxonomy

**Goal:** Create a structured classification system for medical misinformation that enables consistent, defensible moderation decisions.

**Category Taxonomy:**

| Category | Definition | Examples |
|----------|-----------|----------|
| Diagnostic Claims | Unverified claims that a specific symptom or test result indicates a specific condition | "If your big toe tingles, you have pancreatic cancer" |
| Treatment Claims | Promotion of unproven, disproven, or dangerous treatments | "Drink bleach to cure COVID-19," "Stop insulin — cinnamon cures diabetes" |
| Conspiracy Theories | Claims of deliberate deception by medical establishment | "Vaccines contain microchips," "5G causes cancer — they're hiding it" |
| Miracle Cures | Claims of universal or effortless cures for complex conditions | "This one herb cures all types of cancer" |
| Anti-Vaccine Content | Claims that vaccines are ineffective, dangerous, or part of malicious agendas | "Vaccines cause autism," "Natural immunity is always superior" |
| Supplement/Product Scams | Promotion of unregulated supplements with therapeutic claims | "This essential oil blend replaces chemotherapy" |
| Research Misrepresentation | Distorted or fabricated interpretations of legitimate studies | Misquoting study conclusions, citing retracted papers as authoritative |

**Severity Tiers:**

```
Tier 1 — Life-Threatening (immediate action required)
  Content that, if followed, is likely to cause death or severe injury
  Examples: "Stop taking your insulin — this diet cures diabetes"
            "Chemotherapy is poison — refuse all treatment"
  Action: Immediate removal + permanent account suspension + report to authorities if applicable

Tier 2 — Potentially Harmful (urgent action)
  Content that, if followed, could cause significant health deterioration
  Examples: "Vaccines are more dangerous than the disease — never vaccinate"
            Unsubstantiated claims about serious medication interactions
  Action: Removal + final warning or temporary suspension (case-dependent)

Tier 3 — Misleading (corrective action)
  Content that contains factual inaccuracies but limited direct harm potential
  Examples: Overstating benefits of a benign supplement
            Misrepresenting correlation as causation
  Action: Context label with link to authoritative source + content may remain visible

Tier 4 — Low-Quality (no removal, quality signal)
  Content that is unsupported, anecdotal, or low-quality but not actively harmful
  Examples: "I heard vitamin C prevents colds — not sure if it's true"
            Personal anecdotes presented as general advice
  Action: Reduced visibility in feeds + no punitive action
```

### Phase 2 — Community Guidelines Creation

**Goal:** Write clear, accessible community guidelines that define acceptable and unacceptable health content with concrete examples and rationale.

**Guidelines Structure:**

1. **Introduction and Purpose** (plain language, 2-3 sentences)
   - What this community is for (peer support, information sharing, not medical advice)
   - Who these guidelines apply to (all members, moderators, staff)
   - Where to find help (report button, help center, contact info)

2. **What IS Allowed** (positive framing first)
   - Sharing personal health experiences and journeys
   - Discussing evidence-based treatments and research
   - Asking questions about health conditions and treatments
   - Providing emotional support and encouragement
   - Sharing reputable health resources and references

3. **What Is NOT Allowed** (prohibitive with rationale)
   - Medical misinformation (see taxonomy above)
   - Promotion of unproven or dangerous treatments — "This is not allowed because following unproven treatments can delay evidence-based care"
   - Harassment of members based on health conditions
   - Solicitation of private medical information
   - Impersonation of healthcare professionals
   - Spam and commercial promotion of health products

4. **Examples with Rationale** (the "why" section)
   - Allowed example: "I've been on Metformin for 3 months and my A1C dropped from 8.2 to 6.9. Has anyone else had this experience?"
   - Not allowed example: "Throw away your Metformin — Big Pharma is poisoning you. My herbal protocol reversed diabetes in 2 weeks."
   - Rationale: The first shares personal experience with a prescribed treatment. The second makes unsubstantiated claims that could cause someone to discontinue prescribed medication.

5. **Cultural Adaptations**
   - Translated versions in all supported languages (not machine-translated — human-reviewed)
   - Culturally specific examples that resonate with each audience
   - Adaptation for regions with different regulatory frameworks (EU vs. US vs. India)

**Plain-Language Version:**
- One-page summary at 6th-grade reading level
- Visual decision tree: "Should I post this? → Is it my personal experience? → Does it recommend a specific treatment? → Could someone be harmed by following this?"
- Accessible formats: large print, screen-reader-compatible, audio version

### Phase 3 — Policy Enforcement Framework

**Goal:** Implement a progressive enforcement model that educates first and escalates only when necessary, with an emergency bypass for imminent harm.

**Progressive Enforcement Ladder:**

```
Offense 1 — Warning + Education
  ├── Remove violating content
  ├── Send educational message: what policy was violated, why it matters, link to guidelines
  ├── Offer appeal pathway
  └── No account restriction (can still post)

Offense 2 — Temporary Suspension
  ├── Remove violating content
  ├── 7-day suspension for Tier 3, 14-day for Tier 2
  ├── Educational message + link to guidelines + appeal pathway
  └── During suspension: read-only access (can view, cannot post/comment/message)

Offense 3 — Permanent Removal
  ├── Remove violating content
  ├── Permanent account suspension
  ├── Detailed removal notice: policy section, violation history, appeal pathway
  └── Appeal available (no permanent ban is truly final — always offer appeal)

Emergency Bypass — Imminent Harm
  ├── Triggered by: Tier 1 (life-threatening) content, active self-harm, credible threats
  ├── Immediate permanent suspension (skip warning and temporary stages)
  ├── Content preserved for law enforcement (if applicable)
  └── Manual review by senior moderator within 1 hour to confirm/override
```

**Enforcement Principles:**
- Consistency: same violation → same consequence, regardless of user's status or popularity
- Transparency: every enforcement action includes the specific policy violated
- Proportionality: consequences match the severity of the violation
- Appealability: every enforcement action has an appeal pathway
- Documentation: every enforcement action is logged with rationale

### Phase 4 — Escalation Framework

**Goal:** Define clear criteria for when content decisions must be escalated beyond the content policy team.

**Clinical Review Pathway:**
- **When to escalate:** Content involves nuanced medical claims where harm is not obvious, off-label treatment discussions where clinical context matters, emerging treatment discussions (e.g., new clinical trial results), content flagged as misinformation that might actually be accurate but poorly sourced
- **Who reviews:** Medical advisory board member with relevant specialty
- **SLA:** 24 hours for standard, 4 hours for urgent
- **Output:** Clinical opinion on whether content is: (a) evidence-based, (b) unproven but not harmful, (c) potentially harmful, (d) definitely harmful

**Legal Review Triggers:**
- Content that may constitute defamation of a named healthcare provider
- Copyright claims on medical content (study excerpts, medical images)
- Content that may violate FDA regulations on drug promotion
- Content involving named minors and potential COPPA/HIPAA violations
- Subpoena or law enforcement requests for content data

**Public Health Authority Notification:**
- **Notifiable events:**
  - Coordinated misinformation campaigns targeting vaccination programs
  - Content promoting treatments for reportable diseases outside approved channels
  - Threats to healthcare facilities or providers
  - Organized efforts to discourage participation in public health initiatives
- **Notification protocol:** Designated public health liaison, pre-established relationships with CDC/WHO/local health departments, notification template with content summary and engagement metrics

### Phase 5 — Regulatory & Liability Considerations

**Goal:** Understand the regulatory landscape governing medical content on platforms and design policies that manage liability risk.

**FDA Social Media Guidance:**
- FDA guidance on social media promotion of prescription drugs and devices applies primarily to manufacturers, but platforms hosting such content should be aware
- "Fair balance" requirement: benefit claims must be accompanied by risk information — platforms may need to provide space for balanced information
- Off-label promotion monitoring: if a pharmaceutical company uses your platform to promote off-label uses, the platform may have notification obligations
- Corrective messaging: when FDA requires a company to issue corrective communications, platforms must cooperate with dissemination

**HIPAA Implications:**
- The platform is generally not a Covered Entity or Business Associate unless it provides services to healthcare providers
- However, if the platform processes PHI on behalf of a Covered Entity (e.g., patient portal integration), a BAA is required
- User-volunteered health information in public posts is not PHI under HIPAA (it was not generated by a Covered Entity)
- Content removal: if a user posts another person's PHI without authorization, the platform should have a clear process for removal upon request

**Section 230 (47 U.S.C. § 230):**
- Section 230(c)(1): Platforms are not liable for user-generated content — "No provider or user of an interactive computer service shall be treated as the publisher or speaker of any information provided by another information content provider"
- Section 230(c)(2): Good Samaritan protection — platforms may restrict access to objectionable content without becoming liable
- Key limitation: Section 230 does not protect against federal criminal liability, intellectual property claims, or violations of sex trafficking laws (FOSTA-SESTA)
- **Policy implication:** Section 230 protects content moderation decisions made in good faith. Document the policy rationale for every content category to establish good faith.

**Platform Liability for Medical Content:**
- No current US federal law specifically makes platforms liable for medical misinformation
- State-level legislation is emerging (e.g., California AB 2098 on COVID misinformation by physicians — later repealed but signals trend)
- EU Digital Services Act (DSA): Very Large Online Platforms (VLOPs) must assess systemic risks including "negative effects on the protection of public health"
- Best practice: implement policies that exceed current legal minimums to stay ahead of regulatory trajectory

### Phase 6 — Policy-in-Practice Loop

**Goal:** Establish a continuous improvement cycle for content policies that incorporates data, community feedback, and emerging threats.

**Quarterly Policy Review Process:**

```
Q1 Review Cycle:
  Week 1-2: Data Collection
    ├── Takedown statistics by category and severity tier
    ├── Appeal rates and overturn rates by policy section
    ├── Community feedback themes (surveys, focus groups, advisory council)
    └── Emerging misinformation pattern report from trust and safety team

  Week 3: Policy Review Meeting
    ├── Attendees: Content policy manager, clinical advisor, legal advisor, trust and safety lead
    ├── Agenda: Review metrics, discuss borderline cases, propose policy changes
    └── Output: Policy change proposals with rationale

  Week 4: Implementation
    ├── Update policy documents and community guidelines
    ├── Update enforcement workflows and moderator training materials
    ├── Publish policy change log (transparency report update)
    └── Communicate changes to community (announcement post, FAQ)
```

**Community Feedback Integration:**
- Annual community guidelines survey (target: 5% response rate)
- Community advisory council (rotating membership, diverse health conditions, quarterly meetings)
- Public policy feedback channel (dedicated forum category or email)
- Feedback categorization: policy gap, policy overreach, unclear language, implementation issue

**Emerging Misinformation Pattern Updates:**
- Ad-hoc policy updates for novel misinformation (new conspiracy theories, trending harmful claims)
- Expedited review: 72-hour turnaround for emergency policy additions
- Cross-platform intelligence sharing: participate in industry misinformation working groups
- Pattern documentation: maintain a living taxonomy of misinformation narratives with examples

### Phase 7 — Medical Expert Review Board

**Goal:** Establish and maintain a clinical advisory panel that provides expert input on medical content policy decisions.

**Board Composition:**
- Minimum 5 members with diverse specialties relevant to the platform's health focus areas
- Required specialties (example for general health platform): internal medicine, infectious disease, oncology, psychiatry, pediatrics
- Diversity requirements: gender, race, geography (at least 2 non-US members for global platforms)
- Term: 2-year renewable terms, staggered to ensure continuity

**Policy Review Cadence:**
- Monthly: review of escalated content decisions (up to 10 cases)
- Quarterly: policy review participation (see Phase 6)
- Annual: comprehensive policy audit and recommendations report
- Ad-hoc: emergency consultation for novel public health situations

**Expert Dispute Resolution:**
- When board members disagree on a content decision:
  - Document all positions with clinical rationale and supporting evidence
  - Majority vote decides the content moderation action
  - Dissenting opinion is documented and retained
  - If tied or split on life-threatening content → err on the side of removal
  - If tied on non-life-threatening content → err on the side of keeping content with context label

**Board Operations:**
- Compensation: honorarium per review session, not per-decision (avoids incentive to escalate)
- Liability protection: board members are advisors, not final decision-makers — platform retains legal responsibility
- Conflict of interest disclosure: annual disclosure, recusal from relevant decisions
- Board materials: confidential, HIPAA-compliant storage, retention per legal requirements

### Phase 8 — Transparency Reporting

**Goal:** Publish regular transparency reports that build trust through openness about content moderation practices.

**Takedown Statistics (per reporting period):**
- Total content items reviewed (automated + human)
- Content removed by category: misinformation, harassment, spam, CSAM, self-harm, other
- Content removed by severity tier
- Removal method: automated vs. human-reviewed
- Geographic breakdown: removals by country/region
- Proactive detection rate: % of removed content detected by platform vs. user reports

**Appeal Statistics:**
- Total appeals received
- Appeal outcomes: upheld (%), overturned (%), reduced penalty (%)
- Average appeal response time vs. SLA
- Appeals by policy category (which policies generate the most appeals)

**Policy Change Log:**
- Date-stamped log of all policy changes
- Each entry: what changed, why, who approved, effective date
- Public-facing summary (non-confidential version)
- Internal detailed version with borderline cases and discussion

**Public-Facing Transparency Reports:**
- Publish quarterly (minimum: semi-annually)
- Formats: interactive dashboard + downloadable PDF + machine-readable CSV
- Plain-language summary for non-technical audience
- Methodology section: how data is collected, limitations, definitions
- Historical comparison: trends over time (at least 4 quarters)
- Available in all supported platform languages
