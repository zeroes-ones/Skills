---
name: content-policy-manager
description: Content policy and medical misinformation management for health platforms — medical misinformation taxonomy (diagnostic claims, treatment claims, conspiracy theories, miracle cures, anti-vaccine,
  with severity tiers from life-threatening to low-quality), community guidelines creation (what is/isn't allowed with examples, rationale, cultural adaptations, plain-language versions), policy enforcement
  framework (first offense warning + education, second offense temporary suspension, third offense permanent removal, emergency bypass for imminent harm), escalation framework (clinical review pathway,
  legal review triggers, public health authority notification), regulatory and liability considerations (FDA social media guidance, HIPAA implications, Section 230, platform liability for medical content),
  policy-in-practice loop (quarterly policy review, community feedback integration, emerging misinformation pattern updates), medical expert review board (clinical advisory panel establishment, policy review
  cadence, expert dispute resolution), and transparency reporting (takedown statistics, appeal rates, policy change log, public-facing transparency reports). Triggered by content policy, medical misinformation,
  community guidelines, health content moderation, policy enforcement, FDA social media, content governance.
author: Sandeep Kumar Penchala
type: governance
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- content-policy
- medical-misinformation
- community-guidelines
- health-content-moderation
- policy-enforcement
- fda-social-media
token_budget: 8000
dependencies:
  tools: []
  packages: []
  permissions: []
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - ai-safety-health-reviewer
  - community-operations-manager
  - compliance-officer
  - crisis-response-manager
  - legal-advisor
  - medical-content-reviewer
  - regulatory-specialist
  - trust-safety-engineer
  feeds_into:
  - community-operations-manager
  - crisis-response-manager
  - patient-health-educator
  - trust-safety-engineer
---

# Content Policy Manager / Medical Misinformation Officer

Define, enforce, and evolve content policies for health platforms where the stakes of misinformation are measured in lives, not engagement metrics. This skill covers medical misinformation taxonomy, community guidelines authoring, enforcement frameworks, escalation pathways, regulatory considerations, expert review boards, and transparency reporting. Health content moderation is fundamentally different from general content moderation — a wrong call on a vaccine post can contribute to a public health crisis.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules apply to *every* response this skill produces. Content policy decisions in health contexts have clinical, legal, and ethical dimensions — oversimplification causes harm.

- **Never remove content solely because it is "controversial."** The fact that a treatment is unproven, alternative, or debated within the medical community does not automatically make it removable. Distinguish between "I disagree with this" and "this creates imminent risk of harm." Policy must be viewpoint-neutral in application.
- **Survivor speech is protected.** Patients discussing their own lived experiences — including negative experiences with standard treatments, positive experiences with alternative approaches, or criticism of the healthcare system — are not spreading misinformation. These are personal narratives, not medical claims. Do not conflate the two in policy language.
- **Never claim a policy is "comprehensive" or "final."** Medical misinformation evolves faster than policy cycles. New conspiracy theories, emerging treatments, and platform-specific abuse patterns require continuous policy iteration. Every policy document should include a review date within 90 days.
- **Severity must be calibrated to potential harm, not offensiveness.** A post claiming "crystals cure cancer — stop chemo" is life-threatening. A post claiming "I found kale helped my digestion" may be unsupported but is not dangerous. Apply severity tiers consistently and document the rationale.
- **Admit when clinical expertise is required.** Content policy managers are not clinicians. When a decision requires medical judgment — distinguishing evidence-based off-label use from dangerous experimentation, for example — this must be escalated to the clinical review pathway. Never make clinical determinations without clinical input.

## Route the Request

<!-- QUICK: 30s — pick your path, skip the rest -->

```
What are you trying to do?
├── Classify medical misinformation → Jump to "Core Workflow — Phase 1 (Misinformation Taxonomy)"
├── Write or update community guidelines → Jump to "Core Workflow — Phase 2 (Community Guidelines)"
├── Design an enforcement framework → Jump to "Core Workflow — Phase 3 (Policy Enforcement)"
├── Escalate a borderline content decision → Jump to "Core Workflow — Phase 4 (Escalation Framework)"
├── Understand legal/regulatory exposure → Jump to "Core Workflow — Phase 5 (Regulatory & Liability)"
├── Set up a policy review cycle → Jump to "Core Workflow — Phase 6 (Policy-in-Practice Loop)"
├── Establish a medical expert review board → Jump to "Core Workflow — Phase 7 (Expert Review Board)"
├── Build transparency reporting → Jump to "Core Workflow — Phase 8 (Transparency Reporting)"
├── Need to enforce a specific policy violation → Invoke trust-safety-engineer skill instead
├── Legal question about Section 230 or liability → Invoke legal-advisor skill instead
├── FDA compliance for marketing content → Invoke regulatory-specialist skill instead
└── Not sure? → Start at "Core Workflow — Phase 1" and follow sequentially
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Decision Trees
<!-- STANDARD: 3min -->

### Medical Misinformation Severity Triage

```
Does the content contain a medical claim?

├── YES → Is the claim life-threatening if followed?
│   ├── YES → Tier 1 — Life-Threatening
│   │   Examples: "Stop your insulin — this diet cures diabetes"
│   │            "Chemotherapy is poison — refuse all treatment"
│   │   Action: Immediate removal + permanent suspension + report to authorities
│   │
│   ├── NO → Is the claim potentially harmful?
│   │   ├── YES → Tier 2 — Potentially Harmful
│   │   │   Examples: "Vaccines are more dangerous than the disease"
│   │   │            Unsubstantiated claims about serious medication interactions
│   │   │   Action: Removal + final warning or temporary suspension
│   │   │
│   │   └── NO → Is the claim factually inaccurate but low direct harm?
│   │       ├── YES → Tier 3 — Misleading
│   │       │   Examples: Overstating benefits of a benign supplement
│   │       │            Misrepresenting correlation as causation
│   │       │   Action: Context label + link to authoritative source
│   │       │
│   │       └── NO → Tier 4 — Low-Quality
│   │           Examples: "I heard vitamin C prevents colds — not sure if it's true"
│   │                    Personal anecdotes presented as general advice
│   │           Action: Reduced visibility in feeds, no punitive action
│   │
│   └── Is the claim from a credentialed medical professional?
│       ├── If YES and outside their specialty → escalate to clinical review
│       └── If NO and potentially harmful → proceed with enforcement action
│
└── NO → Is this a personal health narrative (survivor speech)?
    ├── YES → Protected. Do not remove. May apply context label if needed.
    └── NO → Non-medical content. Apply standard community guidelines.
```

### When to Escalate

```
Decision: Who should handle this content decision?

├── Involves nuanced medical judgment?
│   ├── Examples: distinguishing evidence-based off-label use from dangerous experimentation
│   └── → Escalate to Clinical Review (24h standard / 4h urgent SLA)

├── Involves potential legal liability?
│   ├── Defamation of named healthcare provider
│   ├── Copyright claims on medical content
│   ├── FDA drug promotion violations
│   ├── Content involving named minors (COPPA/HIPAA)
│   └── → Escalate to Legal Review

├── Involves coordinated public health threat?
│   ├── Organized anti-vaccination campaigns
│   ├── Promotion of treatments for reportable diseases outside approved channels
│   ├── Threats to healthcare facilities or providers
│   └── → Notify Public Health Authority (CDC/WHO/local health department)

└── Can be decided with existing policy?
    └── → Content policy team decides. Document rationale in enforcement log.
```

## When to Use

<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->

- Classifying medical content into misinformation categories and severity tiers
- Drafting or updating community guidelines for health platforms
- Designing progressive enforcement frameworks (warning → suspension → ban)
- Building escalation pathways for clinical, legal, and public health review
- Assessing regulatory and liability risk (FDA guidance, HIPAA, Section 230)
- Establishing medical expert review boards for policy governance
- Creating transparency reports with takedown statistics and appeal rates
- Integrating community feedback into policy iteration cycles

## Core Workflow
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

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

<!-- NEIGHBORS: Skills this policy manager works with — coordinate early, not after a crisis -->

### Decision Gates

| When faced with this decision... | Invoke | Key Artifact |
|---|---|---|
| New regulation requires policy update | `compliance-officer` + `legal-advisor` | Regulatory impact memo, revised enforcement tier definitions |
| Detection system reports new abuse pattern | `trust-safety-engineer` | False positive/negative analysis, automation feasibility assessment |
| Moderators report policy ambiguity in the field | `community-operations-manager` | Policy-in-practice review, edge case catalog, revised playbook draft |
| Crisis event needs emergency content rules | `crisis-response-manager` | Emergency bypass definition, post-crisis policy review framework |
| Policy involves clinical accuracy determinations | `medical-content-reviewer` | Evidence standard memo, expert panel recommendation |
| Policy design needs enforcement workflow definition | `trust-safety-engineer` | Enforcement matrix, severity tier definitions, detection rules |

### Upstream (What You Consume)

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `compliance-officer` | Regulatory framework interpretation, enforcement posture guidance | During policy creation, quarterly review, and any policy response to new regulation |
| `legal-advisor` | Section 230 analysis, liability exposure assessment, DMCA/takedown obligations | Before launching any new enforcement tier, before public transparency reports |
| `regulatory-specialist` | FDA social media guidance updates, FTC endorsement rules, state-level health claim regulations | Monthly sync; immediately when FDA/regulatory guidance changes |
| `trust-safety-engineer` | Detection system capabilities/limitations, false positive/negative rates, automation feasibility | When designing enforcement workflows — must align policy with technical reality |
| `community-operations-manager` | Moderator feedback on policy usability, appeal patterns, edge cases found in practice | Bi-weekly policy-in-practice review; before any policy change goes live |
| `crisis-response-manager` | Emergency override triggers, imminent harm escalation criteria | Jointly define emergency bypass rules and post-crisis policy review |
| `medical-content-reviewer` | Clinical review criteria, evidence standards, expert panel recommendations | Any policy involving clinical accuracy determinations |

### Downstream (What You Feed)

| Downstream Skill | What You Provide | Decision Gate / Impact of Delay |
|---|---|---|
| `trust-safety-engineer` | Policy rules for automated detection systems, severity tier definitions, enforcement matrices | **Gate:** Automation cannot ship without policy definitions — blocks detection pipeline |
| `community-operations-manager` | Moderator playbooks, appeal criteria, edge case guidance | **Gate:** Moderators enforce undefined policies inconsistently — high appeal rate |
| `crisis-response-manager` | Imminent harm definitions, emergency removal criteria | **Gate:** Without clear policy, crisis response is either over-broad or paralyzed |
| `patient-health-educator` | Approved health claim language, acceptable evidence standards for educational content | **Gate:** Educational content may contradict enforcement — erodes platform credibility |

**Coordination cadence:**
- **Weekly:** Sync with `trust-safety-engineer` on detection performance and policy gaps
- **Bi-weekly:** Policy-in-practice review with `community-operations-manager`
- **Monthly:** Regulatory alignment check with `compliance-officer` and `regulatory-specialist`
- **Quarterly:** Full policy review with `legal-advisor`, `medical-content-reviewer`, and all downstream consumers
- **Emergency:** `crisis-response-manager` and `legal-advisor` within 1 hour of imminent harm detection

## Best Practices
<!-- DEEP: 10+min -->

<!-- NON-NEGOTIABLES: These apply to every response — no exceptions, no shortcuts -->

1. **Taxonomy first, enforcement second.** Never write enforcement rules before defining what you're enforcing against. A clear medical misinformation taxonomy (diagnostic claims, treatment claims, conspiracy theories, miracle cures, anti-vaccine) with severity tiers is the foundation every policy decision rests on. Without it, enforcement is arbitrary.

2. **Examples are policy.** Community guidelines without concrete examples of what IS and IS NOT allowed are unenforceable. Every rule needs at least two examples: one that is just barely allowed (the boundary case) and one that is just barely not allowed. Moderators enforce examples, not abstractions.

3. **Severity tiers must map to potential harm, not offensiveness.** Life-threatening misinformation (discontinue insulin for cinnamon cure) requires immediate removal. Low-quality health claims (kale helps digestion) may require a label, not removal. Calibrate every tier to the worst plausible outcome if the content is believed and acted upon.

4. **Escalation pathways must exist before they're needed.** Define clinical review pathways, legal review triggers, and public health authority notification procedures in advance. When a post threatens self-harm or describes an adverse event from a regulated product, the window for action is minutes, not days. Pre-documented escalation prevents decision paralysis.

5. **Transparency reporting is a regulatory asset, not a PR exercise.** Public-facing reports with takedown statistics, appeal rates, and policy change logs demonstrate good-faith moderation to regulators. Courts and agencies look for evidence of consistent, principled enforcement — publish it proactively.

6. **Survivor speech protection must be explicit in policy language.** Patients discussing their own lived experience with treatments — positive or negative — are engaging in protected health discourse. The policy must explicitly distinguish between "I experienced X" (personal narrative) and "X works for Y condition" (treatment claim). When in doubt, protect the narrative and flag the claim for clinical review.

7. **Policy review cycles must outpace misinformation evolution.** Medical misinformation mutates faster than quarterly review cycles. Build a rapid-response mechanism: when a new misinformation pattern emerges (e.g., a novel conspiracy theory about a newly approved drug), the policy team must be able to deploy interim guidance within 48 hours, not wait for the next quarterly review.

8. **Never make clinical determinations without clinical input.** Content policy managers are not clinicians. A policy that classifies specific treatments as "misinformation" or "evidence-based" without medical expert review is practicing medicine without a license. Maintain a medical expert review board with defined review cadences and dispute resolution processes.

## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| A well-intentioned user posted a detailed account of how they "cured Stage 4 pancreatic cancer in 3 months" using a specific herbal protocol. The post was heartwarming, well-written, and generated thousands of supportive comments. The platform initially left it up because "survivor speech is protected." | Investigation revealed the user had never been diagnosed with cancer — their account was fabricated to promote a supplement company they owned. The herbal protocol they promoted was hepatotoxic at the doses described. Three users later reported discontinuing chemotherapy to follow the protocol. | Investigate the failure mode, document the root cause in the enforcement log, update policy rules, and deploy corrective controls. Re-train moderation team on the identified gap. | Survivor speech protection requires verification of survivorship. A post that claims a specific medical outcome AND recommends specific actions should be reviewed by clinical experts even if framed as personal narrative. The boundary between survivor speech and treatment promotion is not always clear in the first read. |
| A health platform implemented an aggressive keyword filter: any mention of "cure" + "cancer" was auto-flagged for removal. Within the first month, thousands of posts were removed — including posts from cancer patients discussing "what a cure would mean to me," threads about "my doctor says I'm cured" (remission announcements), and support group discussions about "hoping for a cure." | The keyword filter had no context awareness. "Cure" in a patient support context is fundamentally different from "cure" in a treatment claim context. The platform's own patient community felt silenced and policed. | Investigate the failure mode, document the root cause in the enforcement log, update policy rules, and deploy corrective controls. Re-train moderation team on the identified gap. | Keyword-based moderation without context analysis will always over-remove. Every auto-removal rule needs a precision metric, not just a recall metric. Run new filters in shadow mode for at least 2 weeks and measure the false positive rate on real content before enabling enforcement. |
| A platform with a global user base flagged traditional medicine discussions from South Asian and African communities as "medical misinformation." Posts about Ayurvedic dietary practices, traditional bone-setting, and herbal remedies used for generations were removed under the same rules that targeted anti-vaccine conspiracy theories. | The policy team was predominantly Western and clinically trained. They equated "not evidence-based by Western RCT standards" with "misinformation." This created a perception that the platform was culturally biased and disregarded traditional health systems that millions of people rely on. | Investigate the failure mode, document the root cause in the enforcement log, update policy rules, and deploy corrective controls. Re-train moderation team on the identified gap. | Global content policies need cultural competency review. Distinguish between "unproven by Western medical standards" and "actively harmful." Traditional practices with a long history of safe use should be treated differently from novel conspiracy theories. Include cultural anthropologists or traditional medicine experts in the expert review board. |
| A health platform expanded to a new market and auto-translated its community guidelines but didn't hire moderators fluent in the local language. For six months, a network of accounts posted fraudulent cancer treatment ads in the local language — targeting vulnerable patients with "guaranteed cure" clinics that were actually exploiting patients for money. | The platform assumed machine translation of guidelines was sufficient. The abuse was reported by a local journalist, not detected by the platform. The regulatory authority in that country opened an investigation into the platform's content moderation practices. | Investigate the failure mode, document the root cause in the enforcement log, update policy rules, and deploy corrective controls. Re-train moderation team on the identified gap. | Language coverage in guidelines does not equal language coverage in enforcement. Every supported language needs at least one human moderator who is a native speaker. Machine translation of reported content is a triage tool, not an enforcement tool. |
| A platform published its first transparency report showing that 0.3% of content was removed for misinformation. The report was intended to show responsible moderation. Instead, journalists calculated that 0.3% of 10 million monthly posts = 30,000 removed posts and ran stories about "massive censorship on health platform." | The report provided raw numbers without context: how many removals were reversed on appeal, what percentage were automated vs. human-reviewed, how many were for dangerous content (Tier 1) vs. low-quality (Tier 4). The lack of context allowed the narrative to be controlled by the platform's critics. | Investigate the failure mode, document the root cause in the enforcement log, update policy rules, and deploy corrective controls. Re-train moderation team on the identified gap. | Transparency reports need narrative framing. Provide breakdowns by severity tier, appeal rates, and overturn rates. Show the "why" behind the numbers. A transparency report that only shows takedown counts is ammunition for bad-faith critics. Include the stories of what the platform prevented. |

## Production Checklist
<!-- STANDARD: 3min -->

<!-- CHECKLIST: CP1-CP14 reference IDs for Content Policy production readiness -->

- **CP1** — Medical misinformation taxonomy defined with categories, severity tiers, and concrete examples for each
- **CP2** — Community guidelines drafted, reviewed with clinical and legal, published in all supported languages with plain-language version
- **CP3** — Progressive enforcement ladder: warning, suspension, ban workflow implemented with automated messaging
- **CP4** — Emergency bypass process for imminent harm content operational with 1-hour manual review SLA
- **CP5** — Clinical review escalation pathway established with medical advisory board and documented SLAs
- **CP6** — Legal review triggers documented; legal advisor relationship established for content escalations
- **CP7** — Public health authority notification protocol defined with pre-established contacts and templates
- **CP8** — Regulatory landscape assessment completed: FDA, HIPAA, Section 230, DSA-reviewed with legal counsel
- **CP9** — Quarterly policy review cycle operational with defined participants, agenda, and outputs
- **CP10** — Community feedback integration channels active: survey, advisory council, public feedback channel
- **CP11** — Medical expert review board established: members onboarded, first quarterly review completed
- **CP12** — Expert dispute resolution process documented and tested with mock scenarios
- **CP13** — Transparency reporting pipeline built: data collection automated, first report drafted and reviewed
- **CP14** — Policy change log maintained with all changes since policy inception; public version published

## Scale Depth
<!-- DEEP: 10+min -->

<!-- SCALE: How content policy management evolves as the platform grows -->

### Solo Community (1 moderator, < 1,000 users)
- One person writes policies, enforces them, and handles appeals
- Policy is a single document (Google Doc or Notion page)
- "Escalation" means asking the founder or a clinician friend
- Transparency reporting: a monthly forum post with basic stats
- Expert review: informal — one or two clinicians who review borderline cases as a favor
- **Key risk:** Policy knowledge lives in one person's head. If they leave, institutional knowledge is zero.

### Growing Platform (2-5 moderators, 1,000-100,000 users)
- Dedicated content policy manager role separates policy creation from enforcement
- Policy document with version control and change log
- Formal escalation pathways: named clinical and legal contacts with documented SLAs
- Basic enforcement tooling: flagging, queues, template messaging
- Quarterly policy review cycle begins (lightweight — 2-hour meeting)
- Transparency reporting: quarterly blog post with basic metrics
- Expert review board: 3 clinicians on retainer, monthly case review
- **Key risk:** Volume outpaces manual review. First automation decisions will set precedent.

### Enterprise Health Community (Trust & Safety team, 100,000-10M users)
- Dedicated content policy team (policy manager + policy analysts)
- Multi-language policy versions with cultural adaptation
- Full progressive enforcement ladder with automated workflows
- Clinical review panel: 5+ specialists with monthly case review and published opinions
- Legal review: established relationship with healthcare regulatory counsel
- Transparency reporting: quarterly interactive dashboard + downloadable data
- Community advisory council operational with rotating membership
- Cross-platform misinformation intelligence sharing
- **Key risk:** Policy complexity creates inconsistency. Different moderators apply the same policy differently.

### Multi-Platform Health Network (Trust org, 10M+ users)
- Policy governance board: policy, legal, clinical, product, and executive stakeholders
- AI-assisted policy enforcement with human-in-the-loop for borderline cases
- Real-time misinformation detection with cross-platform pattern sharing
- Global expert review board: 10+ members across geographies and specialties
- Regulatory affairs team dedicated to monitoring emerging legislation worldwide
- Transparency center: dedicated public website with real-time data, academic partnerships, external audits
- Policy sandbox: test policy changes against historical content before deployment
- **Key risk:** Regulatory fragmentation. A policy that satisfies the EU DSA may conflict with US Section 230 interpretation. Need jurisdiction-specific policy overlays.

## What Good Looks Like
<!-- STANDARD: 3min -->

<!-- OUTCOME: The north star for content policy management in health platforms -->

- **Users trust the platform because medical information is accurate.** When a user reads health content, they can see clear signals about what is evidence-based, what is personal experience, and what has been flagged as potentially misleading. Trust is built through transparency, not through hiding moderation decisions.

- **Moderators act with confidence because policies are clear.** Every content decision has a policy citation with rationale. Moderators don't have to guess whether something is removable — the taxonomy, severity tiers, and examples give them a defensible framework. When they're unsure, they have a documented escalation path to clinical review, not a Slack message to their manager.

- **Regulators see proactive content governance, not reactive cleanup.** The platform's transparency reports, policy review cycles, and expert board demonstrate that content safety is a designed feature, not an afterthought. When a regulator asks "what are you doing about medical misinformation?", the answer is a structured program with measurable outcomes, not a press release.

- **The expert review board is a strategic asset, not a liability shield.** Clinical experts are engaged in policy design, not just case review. Their published opinions become resources for the broader health information ecosystem. Other platforms reference your content policy framework as best practice.

- **Community members feel protected, not censored.** Users understand why content was removed because the guidelines are clear and the enforcement is transparent. Survivors of serious illness feel safe sharing their lived experiences because the policy explicitly protects survivor speech. The platform is known as a place where health conversations are both open and safe.

## Sub-Skills

<!-- QUICK: lookup specialized workflows -->

### misinformation-taxonomy

Categories: diagnostic claims, treatment claims, conspiracy theories, miracle cures, anti-vaccine, supplement scams, research misrepresentation. See Phase 1.

### community-guidelines-authoring

What is/isn't allowed, examples with rationale, cultural adaptations, plain-language versions, visual decision trees. See Phase 2.

### enforcement-framework

Progressive ladder (warning → suspension → ban), emergency bypass, enforcement principles. See Phase 3.

### escalation-framework

Clinical review pathway, legal review triggers, public health authority notification. See Phase 4.

### regulatory-liability

FDA social media guidance, HIPAA, Section 230, DSA, platform liability for medical content. See Phase 5.

### policy-review-cycle

Quarterly review process, community feedback integration, emerging pattern updates. See Phase 6.

### expert-review-board

Board composition, policy review cadence, dispute resolution, board operations. See Phase 7.

### transparency-reporting

Takedown statistics, appeal statistics, policy change log, public-facing reports. See Phase 8.
