---
name: medical-content-reviewer
description: Clinical accuracy review of health content — medical misinformation detection and prevention, evidence-based content validation (use of citations, GRADE framework for evidence quality), community
  Q&A medical accuracy, health claims fact-checking, clinical guideline compliance, disclaimer and liability language, adverse event reporting triggers. Use when reviewing patient-facing content for clinical
  accuracy, building medical misinformation detection rules, or establishing a content review workflow.
author: Sandeep Kumar Penchala
type: health-clinical
status: stable
version: 1.0.0
updated: 2026-07-22
tags:
- medical-content-review
- clinical-accuracy
- misinformation
- evidence-based-medicine
- health-content
token_budget: 3500
output:
  type: document
  path_hint: review/
chain:
  consumes_from:
  - ai-safety-engineer
  - clinical-informatics-specialist
  - compliance-officer
  - legal-advisor
  feeds_into:
  - ai-safety-health-reviewer
  - content-policy-manager
  - medical-illustrator
  - patient-health-educator
  alternatives:
  - compliance-officer
---
# Medical Content Reviewer

Ensure every piece of health content in your app is clinically accurate, evidence-based, and legally defensible. This skill covers medical accuracy review workflows, misinformation detection, evidence quality assessment, disclaimer drafting, and adverse event trigger identification — specifically for digital health apps and patient communities.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── REVIEW patient-facing education content for clinical accuracy → Jump to "Core Workflow" — Phase 1
├── RESPOND to a potentially harmful community post → Go to "Decision Trees > Community Content Triage"
├── BUILD medical misinformation detection rules → Jump to "Core Workflow" — Phase 2 (Detection)
├── ASSESS whether a claim is evidence-based → Go to "Decision Trees > Evidence Quality Assessment"
├── WRITE medical disclaimers for app content → Jump to "Best Practices — Disclaimers"
├── REPORT a potential adverse event discovered in community content → Go to "Core Workflow" — Phase 4
├── Need compliance/regulatory sign-off → Invoke `compliance-officer` after this skill
├── Need clinical terminology, FHIR, or EHR integration expertise? → Invoke `clinical-informatics-specialist` for coded clinical references and data standards
├── Detected an adverse event or patient safety concern? → Invoke `crisis-response-manager` immediately — do NOT just delete the content
├── Creating patient-facing education content? → Invoke `patient-health-educator` for health-literate content design; return here for clinical review
├── Need AI safety review of health content? → Invoke `ai-safety-health-reviewer` for automated clinical validation guardrails
├── Need content policy alignment for misinformation rules? → Invoke `content-policy-manager` for policy enforcement and triage criteria
└── Not sure where to start? → Start at "Ground Rules" then "When to Use"
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- QUICK: 30s -->
These rules apply to *every* response this skill produces. Medical content review is a clinical responsibility, not an editorial one.

- **Never approve clinical content without cited evidence.** Every treatment claim must cite a peer-reviewed source, clinical practice guideline (MASAC, WFH, ISTH, NHF), or FDA labeling. "My doctor told me" is not evidence for content — it's a signal for peer support, not clinical reference material.
- **The absence of evidence is not evidence of absence.** If no study supports or refutes a claim, say "there isn't enough research to know" rather than implying the claim is false. Distinguish between "proven false" and "insufficient evidence to evaluate."
- **Community content is not medical advice unless you make it so.** Adding a doctor's comment, pinning a reply, or "verified" badge to a community post changes the user's perception of authority. When you amplify community content, you assume responsibility for its accuracy.
- **Treatment decisions are between patients and their providers.** Content that contradicts a patient's prescribed treatment plan should be flagged and reviewed, but never removed solely because it differs from standard of care. Note: "This is different from what your doctor may have recommended. Always talk to your doctor before changing your treatment."
- **Adverse events must be reported, not just deleted.** If a patient reports a serious side effect or device malfunction in community content, that may be a reportable adverse event to the FDA (or equivalent regulator). Deleting the post does not delete the reporting obligation. Follow the AE reporting workflow.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- Before publishing any new patient-facing health education content (article, video, infographic, FAQ)
- Reviewing community Q&A content where medical advice is being given by other patients
- Building automated detection rules for medical misinformation (treatment claims, cure claims, vaccine misinformation)
- Responding to flagged community posts about treatment experiences, side effects, or alternative therapies
- Writing medical disclaimers, terms of use, and liability language for health content in the app
- Identifying adverse event signals in community content that may need regulatory reporting
- Evaluating whether a pharma partner's educational content meets your clinical accuracy standards
- Auditing existing app content for outdated or inaccurate medical information

## Cross-Skill Coordination
<!-- QUICK: 30s — table of who to talk to when -->
Medical content review operates at the intersection of clinical accuracy, regulatory compliance, and patient safety. Every content approval carries clinical liability — coordination with clinical, regulatory, and content teams ensures evidence-based content that is legally defensible and medically safe.

### Coordinate With

| Coordinate With | When | What to Share/Ask | Clinical Validation Gate |
|-----------------|------|-------------------|--------------------------|
| **Clinical Informatics Specialist** | Content requiring FHIR terminology mapping, EHR integration context, clinical workflow validation | Terminology codes (SNOMED, LOINC, ICD-10), clinical workflow context, data standard alignment | Gate: All coded clinical references must map to validated ValueSets before content approval. |
| **Compliance Officer** | Regulatory review of health claims, FDA labeling compliance, disclaimer language | Content for regulatory review, health claim assessment, labeling compliance check | Gate: Any content making therapeutic claims requires regulatory sign-off before publication. Artifact: Regulatory review checklist with sign-off. |
| **Legal Advisor** | Liability review of content, disclaimer adequacy, adverse event reporting obligation assessment | Content with potential liability risk, AE trigger language, disclaimer effectiveness | Gate: Content with liability exposure must receive legal review before publication. Artifact: Legal review memo. |
| **Content Policy Manager** | Content policy alignment, misinformation flagging rules, community content triage criteria | Medical misinformation detection rules, content policy gaps, triage criteria updates | Gate: Misinformation detection rules validated against clinical evidence before deployment. |
| **Patient Health Educator** | Patient-facing content for clinical accuracy review, readability assessment, health literacy validation | Education content drafts, behavior change frameworks, health literacy scores | Gate: All patient education content must pass clinical accuracy review before reaching patients. Artifact: Clinical accuracy sign-off form. |
| **AI Safety Health Reviewer** | AI-generated health content review, automated clinical validation, safety guardrail testing | AI content outputs, safety validation results, guardrail effectiveness data | Gate: AI-generated health content must pass human clinical review before patient exposure. Artifact: AI safety validation report. |

### Regulatory Handoffs & Patient Safety Protocols

| Handoff Trigger | Route To | Protocol | Regulatory Timeline |
|----------------|----------|----------|---------------------|
| Adverse event signal detected in community content | `crisis-response-manager` | Flag → Isolate content → Do NOT delete → Document timestamp → Transfer to crisis response | Within 1 hour of detection |
| Content contains unapproved drug claims (off-label promotion) | `compliance-officer` → `legal-advisor` | Flag content → Halt publication → Regulatory review → Corrective action | Before publication or within 24 hours of discovery |
| Content contradicts FDA-approved labeling | `compliance-officer` → `clinical-informatics-specialist` | Flag → Clinical review → Regulatory assessment → Content correction or removal | Within 48 hours |
| Medical misinformation detected at scale (>100 posts) | `content-policy-manager` → `crisis-response-manager` | Triage → Pattern analysis → Policy update → Community notification | Within 24 hours |
| Patient safety concern (self-harm, suicide risk, abuse) | `crisis-response-manager` (immediately) | Warm handoff protocol → Do NOT leave patient with automated response → Document | Within 5 minutes |

### Escalation Path

```
Patient safety concern (self-harm, AE, abuse)? → crisis-response-manager. Within 5 minutes.
Regulatory concern (off-label claims, misleading content)? → compliance-officer + legal-advisor. Within 24 hours.
Content liability risk (potential lawsuit)? → legal-advisor + compliance-officer. Within 48 hours.
Systematic misinformation campaign detected? → content-policy-manager + crisis-response-manager. Within 24 hours.
```

### Decision Gates

- **Evidence quality gate:** Every treatment claim must cite GRADE-assessed evidence (High/Moderate/Low/Very Low). Claims supported only by Low or Very Low evidence require explicit disclaimer: "Limited evidence supports this claim — talk to your doctor."
- **Regulatory review gate:** Any content making therapeutic claims about prescription drugs, medical devices, or biologic products requires regulatory review before publication. No exceptions.
- **Clinical accuracy sign-off:** All patient-facing health content requires sign-off from a qualified clinical reviewer before publication. Content without sign-off is held from publication.

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Community Content Triage

```
                    ┌──────────────────────────────┐
                    │ START: A community post is    │
                    │ flagged for medical content   │
                    └──────────────┬───────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │ Does the post contain a    │
                     │ specific treatment claim?  │
                     └────┬─────────────────┬────┘
                          │ YES             │ NO
                     ┌────▼──────────┐ ┌─────▼──────────────────────┐
                     │ Is the claim   │ │ Personal experience /     │
                     │ about a pre-   │ │ peer support? → Allow,    │
                     │ scription drug,│ │ add "individual results   │
                     │ dosage, or     │ │ vary" disclaimer on the   │
                     │ medical device?│ │ thread. No removal unless │
                     └────┬──────────┘ │ it's dangerous (see right).│
                          │ YES        └────────────────────────────┘
                     ┌────▼──────────┐
                     │ Does it match  │
                     │ FDA-approved   │
                     │ labeling?      │
                     └────┬──────────┘
                     ┌─────┴──────┐
                     │ NO         │ YES
                  ┌──▼──┐     ┌───▼───┐
                  │ Is  │     │ Allow │
                  │ the  │     │ with  │
                  │ claim│     │ dis-  │
                  │ dan- │     │ claim-│
                  │ ger- │     │ er +  │
                  │ ous? │     │ "not │
                  └──┬───┘     │ medi- │
                ┌────┴────┐    │ cal   │
                │ YES     │ NO │ adv-  │
             ┌──▼──┐  ┌──▼──┐ │ ice for│
             │ Re-  │  │ Add │ │ *you  │
             │ move │  │ flag│ │ spe-  │
             │ +    │  │: "ⓘ │ │ cifi- │
             │ warn │  │ This │ │ cally.│
             │ +    │  │ may  │ └───────┘
             │ re-  │  │ not  │
             │ port │  │ apply│
             │ AE if│  │ to   │
             │ harm │  │ ev-  │
             │ re-  │  │ ery- │
             │ port-│  │ one."│
             │ ed   │  └──────┘
             └──────┘
```

**Dangerous claims (remove immediately):** "Stop taking your factor — I switched to herb X and I'm cured." "Here's how to compound your own factor at home." "Children don't need prophylaxis; it's overprescribed." These cause direct harm. **Off-label but not dangerous (flag with context):** "My doctor prescribed X for my chronic synovitis" — off-label but may be legitimate. Add context, don't remove.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~20 min): Clinical Accuracy Review of Published Content
**Steps:** 1) Read every clinical claim in the content — highlight all disease, treatment, dosage, prognosis, and prevention statements 2) For each claim, verify against primary source: FDA label, NIH/PubMed, Cochrane Review, or clinical practice guideline (MASAC, WFH, NHF, ISTH). Secondary sources (WebMD, Wikipedia) are starting points, not evidence. 3) Classify each claim: Evidence-supported (✅), Insufficient evidence (⚠️ needs qualifier like "some studies suggest..."), Contradicted by evidence (❌ needs correction or removal), Outdated (⏳ guideline changed, needs update) 4) Add clinical context: "While this study shows X, the WFH guidelines note Y as the recommended approach" 5) Document review: claim, source, classification, action taken. Keep a permanent audit trail.

**What good looks like:** Content with 100% of clinical claims cited to primary sources. A review document showing every claim classified (✅/⚠️/❌/⏳) with source citations. No unverified treatment claims. Audit trail complete.

### Phase 2 (~25 min): Misinformation Detection Rules
**Steps:** 1) Define harm levels: Level 1 (dangerous — immediate removal, possible AE report), Level 2 (misleading — flag with corrective context), Level 3 (unsubstantiated — add "not enough research" note), Level 4 (personal experience — no action beyond threading disclaimer) 2) Build keyword and pattern rules: "cure" + "hemophilia" = Level 2 (no known cure). "Stop taking" + medication name = Level 1. "Natural treatment" + condition = Level 2. 3) Add context-aware rules: "My doctor switched me to X" = personal experience (Level 4) vs "Everyone should try X instead of Y" = medical advice (Level 2) 4) Set up escalation: level 1 → immediate removal + clinical review + AE assessment. Level 2 → 24-hour clinical review. Level 3-4 → flag but no removal. 5) Review and iterate on rules monthly — misinformation tactics evolve faster than your ruleset

**What good looks like:** Detection rule library with 20+ rules at multiple harm levels. Auto-triage catches 80% of Level 1 content before a human sees it. Human reviewers handle levels 2-4. Monthly rule update cadence.

### Phase 3 (~15 min): Disclaimer and Liability Language
**Steps:** 1) Primary disclaimer: "This content is for informational purposes only and is not medical advice. Always consult your healthcare provider about your specific condition and treatment." — REQUIRED on every education page 2) Community content disclaimer: "Posts in this community are from people with hemophilia and their caregivers. They reflect personal experiences, not medical advice. Always talk to your doctor before changing your treatment." — REQUIRED at the top of every community thread 3) AI-generated content disclaimer (if applicable): "This content was generated with the assistance of AI and has been reviewed by a clinician for accuracy." — REQUIRED for any AI-assisted health content 4) Adverse event reporting notice: "If you experience a serious side effect or device malfunction, report it to your doctor and to the FDA at MedWatch: 1-800-FDA-1088." — ADD to any page discussing treatment side effects

**What good looks like:** Disclaimers on every health content page, community thread, and AI-generated content. Legal reviewed and approved. Consistent placement and wording across the app.

### Phase 4 (~15 min): Adverse Event Signal Detection
**Steps:** 1) Define AE triggers: mention of hospitalization, ER visit, serious side effect, device failure, death, or permanent injury related to a treatment 2) When an AE signal is detected in community content, collect: what happened, what product/device was involved, when it happened, was it reported to the manufacturer or FDA? 3) Determine reportability: serious and unexpected AEs may be reportable to FDA within 15 days (if you are a manufacturer or have reporting obligations under your pharma partnership) 4) If reportable: document all available information, send to the appropriate party (FDA MedWatch, manufacturer, your legal team). Do NOT delete the post until the reporting obligation is fulfilled. 5) Non-reportable: document in your AE log for trend analysis. Multiple similar reports may indicate a safety signal.

**What good looks like:** AE detection workflow documented and understood by content moderation team. AE log maintained. Reportable AEs submitted within regulatory timelines. Privacy maintained throughout (no patient identity shared unless required by regulation).

## Best Practices
<!-- STANDARD: 3min -- rules extracted from health content review experience -->

- **One clinician reviewer is not enough for high-risk content.** For any content about treatment decisions, dosing, or procedural instructions, have two independent reviewers. Disagreements go to a third reviewer (medical director or specialist). A single reviewer can miss subtle errors.
- **Update content when guidelines change.** WFH (World Federation of Hemophilia) guidelines are updated every 4-5 years. NHF MASAC recommendations are updated annually. Set a content review schedule aligned with guideline update cycles. Outdated guidelines in patient-facing content are a liability.
- **Distinguish between "not approved by FDA" and "not proven."** Many treatments used in hemophilia care are used off-label (e.g., emicizumab was used off-label for some indications before full approval). Off-label ≠ unsafe. Flag off-label use with context, not alarm.
- **Language matters in health content.** "Prophylaxis prevents bleeds" is accurate. "Prophylaxis guarantees you won't bleed" is not. Always include appropriate qualifiers: may, can, some patients, in clinical trials, depending on your specific condition. Absolute statements in health content are almost always wrong.
- **Community content about side effects is both a risk and an opportunity.** Risk: unverified claims may scare patients away from effective treatments. Opportunity: real-world side effect patterns that clinical trials missed may be detected early. Treat community side effect discussion as safety surveillance, not noise.
- **AI-generated health content must meet the same standard as human-written content.** Never publish AI-generated health content without clinical review. The AI may cite papers that don't exist (hallucinated DOIs), quote guidelines that have been superseded, or make subtle errors that a non-clinician would miss.

## Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|------|
| Patient follows bad advice from community post and is harmed | Misinformation detection missed the post or escalated too slowly | Audit detection rules for that type of content. Add the trigger term. Re-train moderation team on harm levels. Ensure all Level 1 triage is sub-5 minute response time. |
| Legal flags a disclaimer as insufficient for regulatory liability | Disclaimer doesn't specify it's not medical advice or doesn't include AE reporting info | Use the disclaimer language from Phase 3 verbatim. Have legal review all disclaimer text before publication. Add AE reporting notice on any page that mentions specific medications. |
| Clinician reviewer finds an error in content that was already reviewed and published | Single-reviewer process missed an edge case | Add second reviewer requirement. Implement pre-publication hold: content cannot publish until 2 reviewers sign off. Retroactively fix all published content in that category. |
| Pharma partner complains that community content contradicts their product label | Community personal experiences may not match FDA label — which is expected and legal | Add contextual disclaimer on the specific thread: "This member's experience may differ from the FDA-approved labeling for [product]. Always follow your healthcare provider's guidance." Do not remove the post unless it's dangerous. |
| User reports that AI-generated health advice caused them harm | AI-generated content wasn't clinically reviewed before publication | Immediately remove ALL AI-generated health content from the app. Implement mandatory clinical review gate before any AI content is published. Add AI content disclaimer when restored. |
| Community post about a side effect goes viral, causing treatment discontinuation | No context was added to the post, and no clinician response was provided | Proactive protocol: when a side-effect post gains traction, have a clinician respond publicly within 24 hours. "We understand this member experienced X. If you're experiencing a side effect, talk to your doctor. Do not stop your medication without consulting them." |

## Production Checklist
<!-- QUICK: 30s -- all must pass before clinical content review is operational -->

- [ ] **[M1]** Clinical content review workflow documented: claim extraction → source verification → classification → action
- [ ] **[M2]** Review covered by at least 1 clinician (2 for treatment/dosing/procedural content)
- [ ] **[M3]** Misinformation detection rule library built with minimum 20 rules across all 4 harm levels
- [ ] **[M4]** Disclaimers placed on all health education pages, community threads, and AI-generated content
- [ ] **[M5]** Legal reviewed and approved all disclaimer and liability language
- [ ] **[M6]** Adverse event detection workflow documented: triggers identified, reporting obligations understood, AE log active
- [ ] **[M7]** Content review schedule aligned with clinical guideline update cycles (WFH, NHF MASAC, ISTH)
- [ ] **[M8]** AI-generated health content gate: mandatory clinical review before publication
- [ ] **[M9]** Community content triage response SLAs defined: Level 1 < 5 min, Level 2 < 24h, Level 3-4 < 72h
- [ ] **[M10]** Audit trail maintained for all clinical content reviews (claim, source, classification, action, reviewer)
- [ ] **[M11]** Second reviewer required for high-risk content (treatment decisions, dosing, procedures)
- [ ] **[M12]** Cultural and language adaptation reviewed for diverse patient populations

## Cross-Skill Integration
<!-- QUICK: 30s -- table of who to talk to when -->

| Step | Skill | What It Produces |
|------|-------|-----------------|
| **Before** | `patient-health-educator` | Patient education modules → needs clinical accuracy review before publication |
| **Before** | `content-strategist` | Health blog content, social media content → needs clinical fact-checking |
| **Before** | `trust-safety-engineer` | Flagged community posts with medical content → needs clinical triage |
| **This** | `medical-content-reviewer` | Clinical accuracy review, misinformation detection, AE signal detection, disclaimers |
| **After** | `compliance-officer` | Reviewed content, AE report log, disclaimer documentation → feeds compliance audit |
| **After** | `legal-advisor` | Disclaimer language, AE reporting obligations, liability review → legal sign-off |
| **After** | `product-manager` | Clinical accuracy findings → informs feature decisions (e.g., community Q&A redesign) |

## Scale Depth
<!-- QUICK: 30s -- how this skill changes as the company grows -->

| Stage | Scope | Focus | Key Difference |
|-------|-------|-------|----------------|
| **Solo** | Single reviewer checks all content manually | Accuracy above all — don't publish bad info | One clinician reviews everything; manual checklist; no tooling |
| **Startup** | Review team + style guide, basic content management | Scale review throughput, build consistency | Multiple reviewers; documented guidelines; editorial calendar; version control |
| **Scale-up** | Specialized reviewers by content type, automated checks | Deep expertise, automated first-pass screening | Cardiology reviewer vs. endocrinology reviewer; automated fact-checking; AE signal detection |
| **Enterprise** | Clinical review board, regulatory-grade process, published content governance | Institutional credibility, regulatory defense | Medical director + review board; SOPs for every content type; FDA/EMA-compliant process; content audit trail |

## What Good Looks Like
- **Every piece of health content published in the app has been clinically reviewed** with documented source citations. A user reading "Factor VIII prophylaxis reduces bleeds by 87%" sees a footnote linking to the clinical trial. No unverified claims exist in the app.
- **A community post claiming "essential oils cured my hemophilia" is detected and removed within 3 minutes** — the misinformation detection rules catch it, a reviewer confirms it's Level 1 dangerous content, and the user who posted it receives a private message explaining why and offering verified information.
- **A concerning pattern of patients reporting similar side effects triggers a safety signal investigation.** The AE log reveals 8 reports of the same issue in 2 months. The clinical team investigates and contacts the manufacturer. Patients are not harmed because the signal was detected early.
- **The app's health content passes a legal audit** with no liability gaps. Disclaimers are present where they should be. AI-generated content is clearly labeled. The adverse event reporting workflow is documented and followed. The company is protected against claims of practicing medicine without a license.
