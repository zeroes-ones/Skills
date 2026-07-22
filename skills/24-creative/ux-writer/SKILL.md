---
name: ux-writer
description: UX writing and content design for digital health products — product copy design for onboarding flows, empty states, loading states, error messages, and success confirmations; medical disclaimer
  language with regulatory requirements, placement patterns (inline, modal, footer), and when-to-show logic; informed consent UX with granular consent options, withdrawal pathways, and health literacy-adjusted
  reading levels; plain-language health messaging at ≤8th grade reading level with visual reinforcement and localization strategies; error message design for health contexts with clinical data preservation
  assurances; voice and tone systems spanning compassionate, professional, and encouraging registers for sensitive health topics; content design systems with reusable patterns, content tokens, and localization-ready
  string design; microcopy A/B testing, comprehension testing, and trust impact analysis; content accessibility including screen reader content, alt text for medical diagrams, and plain-language alternatives
  for complex terms. Use when writing product copy for health tech, designing medical disclaimers, crafting consent language, optimizing microcopy for health literacy, or building a content design system
  for regulated digital health products.
author: Sandeep Kumar Penchala
type: creative
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- ux-writing
- content-design
- health-literacy
- medical-disclaimers
- microcopy
- consent-language
- product-copy
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - brand-guidelines
  - medical-illustrator
  - patient-health-educator
  - product-manager
  - product-marketing-manager
  - technical-writer
  - ui-ux-designer
  feeds_into:
  - content-strategist
  - frontend-developer
  - localization-engineer
  - medical-illustrator
  - patient-health-educator
---
# UX Writer / Content Designer (Health Tech)

Craft the words that make digital health products feel safe, clear, and human. From onboarding microcopy to medical disclaimers, consent flows to error messages — every word builds trust, reduces anxiety, and drives health outcomes.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Write product copy for a flow → Jump to "Core Workflow > Phase 1: Product Copy Design"
├── Draft a medical disclaimer → Jump to "Core Workflow > Phase 2: Medical Disclaimers"
├── Design consent language → Jump to "Core Workflow > Phase 3: Consent Language"
├── Simplify health content for literacy → Go to "Core Workflow > Phase 4: Health Literacy"
├── Write error messages for health contexts → Jump to "Core Workflow > Phase 5: Error Messages"
├── Define voice and tone → Jump to "Core Workflow > Phase 6: Voice & Tone Systems"
├── Build a content design system → Go to "Core Workflow > Phase 7: Content Design Systems"
├── Test microcopy → Jump to "Core Workflow > Phase 8: Microcopy Testing"
├── Ensure content accessibility → Jump to "Core Workflow > Phase 9: Accessibility"
└── Don't know where to start? → Run "Core Workflow > Phase 1"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never write medical content without clinical review.** Every claim about health outcomes, treatment effects, or clinical data must be reviewed by a qualified clinician. Mark all unverified claims with `[NEEDS CLINICAL REVIEW]`. Do not publish language that implies medical certainty without evidence.
- **Never bury disclaimers in fine print.** Medical disclaimers must be visible at the point of decision, not hidden in a 12-page terms document. Use inline, modal, or persistent footer patterns — never rely on "by continuing you agree" as the sole disclosure mechanism.
- **Never assume health literacy.** Default all patient-facing content to ≤8th grade reading level (Flesch-Kincaid). If a term like "contraindication" or "thrombocytopenia" appears, provide a plain-language alternative or inline definition.
- **Never design consent as a checkbox.** Informed consent in health contexts requires granular options, clear withdrawal pathways, and comprehension checks. A single "I agree" button is never sufficient for clinical data sharing or treatment consent.
- **Always preserve user trust in error states.** Every error message that interrupts a clinical workflow must explicitly confirm data safety: "Your information is saved. You can resume where you left off." Never show a generic "Something went wrong" when clinical data is involved.
- **Admit what you don't know.** If a question requires domain-specific regulatory knowledge (FDA labeling rules, HIPAA consent requirements, EMA guidance), flag it for legal/regulatory review. Do not guess.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Writing onboarding flows, empty states, tooltips, or confirmation messages for a health product
- Drafting medical disclaimers for a patient-facing or provider-facing interface
- Designing informed consent flows with granular options and withdrawal paths
- Adapting clinical content to ≤8th grade reading level for health literacy
- Writing error messages that preserve trust and confirm clinical data safety
- Building a voice and tone system with compassionate, professional, and encouraging registers
- Creating a content design system with reusable patterns, tokens, and localization-ready strings
- Running A/B tests on microcopy to measure comprehension and trust
- Auditing content for screen reader compatibility and plain-language alternatives

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Disclaimer Placement Decision Tree

```
Is the content clinical advice or treatment guidance?
├── YES → Is it a critical safety warning?
│   ├── YES → Modal with explicit acknowledgment required
│   └── NO → Inline disclaimer adjacent to content
├── NO → Is it a general medical information disclaimer?
│   ├── YES → Persistent footer + link to full disclaimer
│   └── NO → No disclaimer needed
└── UNCERTAIN → Legal/regulatory review required before publishing
```

### Consent Complexity Decision Tree

```
What is the data sensitivity?
├── PHI (Protected Health Information) → Granular consent with per-purpose toggles
├── De-identified clinical data → Simplified consent with opt-out option
├── Non-clinical health data (fitness, wellness) → Standard consent with plain-language summary
└── Anonymous usage data → Notice only (no consent required in most jurisdictions)
```

**What good looks like:** A patient reads your onboarding flow and completes it without calling support. A clinician sees your disclaimer and nods — it's where they expect it, says exactly what's needed, and doesn't slow them down. A regulator reviews your consent language and finds no gaps. A usability test participant with 6th-grade reading level correctly explains what they just consented to.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~20 min): Product Copy Design

Design the words that guide users through the product experience.

1. **Onboarding flows**: Progressive disclosure. Each screen = one concept. "Let's set up your treatment plan" not "Configure clinical parameters." Use benefit language: "This helps us show you relevant information" not "This populates the database."
2. **Empty states**: Never show a blank screen. "You haven't logged any symptoms yet. Tap + to start tracking." Include illustration + CTA. For clinical dashboards: "No lab results available. They'll appear here once your provider shares them."
3. **Loading states**: Explain the wait. "Retrieving your health records…" beats a spinner. For long clinical loads: "Gathering your complete health history — this may take up to 30 seconds. Thanks for your patience."
4. **Success confirmations**: Confirm what happened + what's next. "Your symptoms were logged. View your trend report →" Not just a checkmark.
5. **Modals and dialogs**: Title = action. Body = consequence. Buttons = verb + object. "Delete Symptom Log — This removes all entries from March. This can't be undone. [Cancel] [Delete Entries]"

### Phase 2 (~25 min): Medical Disclaimers

Craft disclaimers that protect legally without degrading the user experience.

1. **When to show**: Before clinical decision support results, before treatment cost estimates, on any page containing medical advice, before data sharing with third parties, on AI-generated health content.
2. **How to phrase**: Lead with the limitation, not the liability shield. "This tool provides information, not medical advice. Always consult your doctor before making health decisions." Not: "Company X assumes no liability for…"
3. **Placement patterns**:
   - **Inline**: Short disclaimer adjacent to specific content. "This is an estimate based on your plan. Actual costs may vary."
   - **Modal**: Critical safety warnings requiring acknowledgment. "This medication may interact with [drug]. Please review with your doctor."
   - **Footer**: Persistent general disclaimer. "This app does not replace professional medical advice."
4. **Regulatory requirements**: FDA 21 CFR Part 11 for electronic records, HIPAA for PHI, GDPR Art. 9 for health data in EU, FTC Health Breach Notification Rule, state-specific telehealth consent laws.
5. **Progressive disclosure**: Show essential disclaimer inline, link to full legal text. Never dump 5,000 words of legalese into a 300px modal.

### Phase 3 (~25 min): Consent Language Design

Design consent flows that are truly informed — not just legally compliant.

1. **Informed consent UX**:
   - **Pre-consent summary**: 3 bullet points max. What data, why, who sees it. "Your symptom logs help us personalize your care plan. Only your care team can see them."
   - **Granular options**: Separate toggles for treatment, research, marketing, third-party sharing. Default all to OFF.
   - **Comprehension check**: Ask one question to confirm understanding. "In your own words, who can see your health data?" with multiple-choice options.
   - **Withdrawal pathways**: "You can change these settings anytime in Settings > Privacy. Withdrawing consent won't affect your care."
2. **Reading levels by audience**:
   - Patient-facing: ≤6th grade. "We'll use your health info to give you better care. You can say no anytime."
   - Caregiver-facing: ≤8th grade. "Your child's treatment data helps us track progress and adjust the care plan."
   - Provider-facing: Professional level with clear summaries.
3. **Consent for minors**: Age of consent varies by jurisdiction (13-18). Parental consent flows with child assent language for ages 7-17.
4. **Research consent**: Distinguish between treatment consent and research consent explicitly. "Participating in this study is separate from your treatment. Declining won't affect your care."

### Phase 4 (~20 min): Health Literacy Messaging

Make health information understandable to everyone, regardless of education level.

1. **Plain language principles**:
   - ≤8th grade reading level (target ≤6th for patient-facing)
   - Active voice: "Take this medicine with food" not "This medication should be administered with meals"
   - Short sentences: ≤15 words per sentence
   - Common words: "high blood pressure" not "hypertension"; "blood thinner" not "anticoagulant"
   - Define unavoidable clinical terms inline: "Hemophilia (a condition where blood doesn't clot normally)"
2. **Visual reinforcement**: Every written instruction pairs with an illustration. Pill identification = photo. Injection site = anatomical diagram. Treatment schedule = calendar visualization.
3. **Translations and localization**: Design English source strings for translatability. Avoid idioms ("feeling under the weather"), cultural references, and English-only wordplay. Allow 30% text expansion for Romance languages, 40% for German.
4. **Readability testing tools**: Flesch-Kincaid Grade Level, SMOG Index, PEMAT (Patient Education Materials Assessment Tool). Test with actual patients from your target demographic.

### Phase 5 (~20 min): Error Message Design for Health Contexts

Error messages in health apps carry higher stakes. Design for trust preservation.

1. **Session timeout**: "Your session timed out to protect your privacy. Your last entry was saved. Log in again to continue." Never: "Session expired."
2. **Clinical data save failure**: "We couldn't save your last entry. Don't close this screen — your data is still visible here. Try saving again or take a screenshot." Provide recovery path.
3. **Connectivity loss during data entry**: "Connection lost. Your entries since [timestamp] are saved on your device and will sync when you're back online."
4. **Medication interaction warning**: "This medication may interact with [drug name] in your profile. Please contact your doctor before taking it." Red banner, not subtle toast.
5. **Lab result unavailable**: "Your lab results aren't ready yet. We'll notify you when they are — typically within 24-48 hours." Set expectations.
6. **Generic error replacement rule**: Never show "Error 500" or stack traces. Every error = what happened + what it means for the user + what to do next.

### Phase 6 (~25 min): Voice and Tone Systems

Define how your health product sounds in different contexts.

1. **Voice dimensions (stable)**:
   - **Clear**: Jargon-free, concrete, scannable
   - **Compassionate**: Acknowledges emotion, never dismissive
   - **Trustworthy**: Evidence-based, accurate, transparent about limitations
   - **Empowering**: Gives users agency, never paternalistic
2. **Tone shifts (context-dependent)**:
   - **Sensitive health topics** (cancer, mental health, sexual health): Compassionate + gentle. "We understand this is difficult. Take your time. You're not alone."
   - **Clinical information** (lab results, treatment plans): Professional + clear. "Your A1C is 7.2%, down from 8.1%. This shows your treatment plan is working."
   - **Treatment adherence** (medication reminders, PT exercises): Encouraging + specific. "You've taken your medication 5 days in a row. That's a new record! 🎉"
   - **Urgent safety** (drug interactions, critical results): Direct + actionable. "Important: Contact your doctor before taking this medication. [View interaction details]"
   - **Errors and setbacks**: Supportive + solution-focused. "It looks like you missed your last 2 doses. That's okay — here's what to do now."
3. **Tone anti-patterns**: Never cheerful for serious conditions ("Congrats on your diabetes!"), never clinical-jargon with patients, never blame the user ("You entered an invalid value"), never minimize ("Just a little lump").

### Phase 7 (~20 min): Content Design Systems

Build reusable, scalable content infrastructure.

1. **Reusable content patterns**: Error message template, empty state template, confirmation message template, disclaimer snippet library, consent language components, notification templates (push, email, in-app).
2. **Content tokens**: Define variables for product name, company name, support contact, app store links. Use `{{product_name}}` not hardcoded strings.
3. **Localization-ready string design**:
   - Never concatenate strings: `"You have " + count + " messages"` breaks in every language
   - Use ICU MessageFormat: `{count, plural, one {# message} other {# messages}}`
   - Provide translator context comments: `/* Button: initiates medication refill. Max 20 chars. */`
4. **Character limits per component**:
   - Push notification title: 40 chars
   - Push notification body: 120 chars
   - Button label: 25 chars (20 for mobile)
   - Modal title: 50 chars
   - Toast/ snackbar: 80 chars
   - Tooltip: 150 chars
   - Error message body: 200 chars
5. **Content audit**: Quarterly review of all strings. Flag outdated medical claims, broken links, non-inclusive language, reading level regressions.

### Phase 8 (~15 min): Microcopy Testing

Test whether your words actually work.

1. **A/B testing error messages**: Test trust impact. "Something went wrong" vs "We hit a snag — your data is safe." Measure: task completion rate, support tickets generated, trust survey score.
2. **Comprehension testing**: 5-second test — show the consent screen for 5 seconds, then ask: "What did you just agree to?" If >80% can't answer correctly, rewrite.
3. **Trust impact of phrasings**: "We share your data with partners" vs "Your data helps us improve care for everyone." Test trust before and after with Likert scale.
4. **Click-through on CTAs**: "Learn more" vs "See how this works" vs "Understand your results." Measure actual clicks.
5. **Readability validation**: Run every patient-facing string through Flesch-Kincaid. Flag anything above 8th grade. Test with users who have limited health literacy.

### Phase 9 (~15 min): Accessibility in Content

Ensure content is accessible to all users.

1. **Screen reader content**: Every non-decorative image needs alt text. Medical diagrams need descriptive alt text: "Diagram showing the ankle joint with labels for tibia, fibula, and talus bones. Arrow indicates common sprain site." Provide text alternatives for infographics and charts.
2. **Alt text for medical diagrams**: "Illustration of the heart showing four chambers. Left ventricle highlighted in red to indicate the site of the myocardial infarction described below."
3. **Plain language alternatives**: For every clinical term, provide a tooltip or parenthetical with plain language: "Myocardial infarction (heart attack)." Ensure screen readers can access these alternatives.
4. **Link text**: Never "click here" or "read more." Use descriptive links: "View your full lab results" or "Learn about treatment options."
5. **Reading order**: Content must make sense when linearized. Headings must follow hierarchy (H1 → H2 → H3, no skips).
6. **Cognitive accessibility**: Allow users to hide complex medical explanations behind "Show plain-language version" toggles. Provide summaries before detailed clinical reports.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->

UX writing sits at the intersection of design, clinical, regulatory, and engineering. Know when to coordinate:

| Coordinate With | Decision Gate | Artifacts to Share |
|-----------------|---------------|---------------------|
| `ui-ux-designer` | Screen design needs content-first wireframes; copy length exceeds component constraints | Content requirements (char limits, truncation rules), content-first wireframes |
| `technical-writer` | Medical terminology needs plain-language translation; documentation standards affect UX copy | Terminology glossary, plain-language alternatives, documentation style guide |
| `product-manager` | Feature scope affects copy volume; new flows need content design before implementation | Content requirements, flow diagrams, feature briefs for copy scoping |
| `brand-guidelines` | Voice/tone definition, style guide alignment, terminology preferences | Brand voice attributes, terminology preferences, naming conventions |
| `frontend-developer` | String implementation, i18n setup, ICU MessageFormat strings | ICU MessageFormat strings, translator comments, key naming conventions |
| `localization-engineer` | String extraction, pseudo-localization, expansion buffer requirements | Key structure, pluralization rules, expansion buffer requirements |
| `patient-health-educator` | Patient-facing copy needs health literacy validation (≤8th grade reading level) | Copy drafts for comprehension testing, reading-level scores, simplification requests |
| `medical-illustrator` | Illustrations need alt text, labels, and callouts in product copy | Illustration context, character limits for callouts, visual description for screen readers |
| `clinical-informatics-specialist` | Medical accuracy, terminology validation, drug name verification | Clinical term approval, reading level simplification check, drug name validation |
| `regulatory-specialist` | Disclaimer language, consent text need FDA/EMA/HIPAA compliance review | FDA/EMA requirements, HIPAA consent rules, state-specific telehealth laws |
| `legal-advisor` | Disclaimer review, terms of use, liability language | Legal sufficiency of disclaimers, liability language, jurisdiction-specific requirements |
| `ux-researcher` | Comprehension testing, trust studies, A/B test hypothesis validation | Test stimuli (copy variants), hypothesis for A/B tests, participant screeners |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Medical disclaimer draft complete | `regulatory-specialist`, `legal-advisor` | Legal and regulatory review required before publishing |
| Consent language changes | `legal-advisor`, `regulatory-specialist`, `ux-researcher` | Legal compliance + user comprehension impact |
| Voice/tone system defined | `brand-guidelines`, `ui-ux-designer`, `content-strategist` | Cross-channel consistency, design alignment |
| String freeze for translation | `localization-engineer`, `frontend-developer` | Pipeline kickoff, key extraction, pseudo-localization |
| Microcopy test results (significant) | `ux-researcher`, `product-manager`, `ui-ux-designer` | May trigger design changes, flow redesign |
| Reading level regression detected | `clinical-informatics-specialist`, `ux-researcher` | Patient comprehension at risk |
| New regulatory requirement discovered | `regulatory-specialist`, `legal-advisor`, `ui-ux-designer` | May require flow redesign, new disclaimers |

## Best Practices
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Write for scanning, not reading**: Users don't read health information — they scan for what matters to them. Use headings, bullets, and bold keywords.
- **Test with real patients, not colleagues**: Your team has 100x the health literacy of your users. Test with people who match your target demographic.
- **Design content before design**: Wireframe with real copy, not lorem ipsum. If the content doesn't fit, the design is wrong.
- **One action per screen**: Especially in consent flows. Don't ask users to consent to research, marketing, and data sharing on one screen.
- **Error messages are UX, not engineering**: Don't let developers write error strings. Every error message is a content design opportunity.
- **Translations are not an afterthought**: Design strings for internationalization from day one. Retrofitting i18n costs 3x more.
- **Disclaimers are content, not legal CYA**: A disclaimer that no one reads is not a disclaimer. Design it for comprehension.

## MVP vs Growth vs Scale

| Concern | MVP (Pre-launch) | Growth (Active users) | Scale (Enterprise/Regulated) |
|---------|-----------------|----------------------|------------------------------|
| Copy volume | 50-100 strings | 500-1000 strings | 5000+ strings across products |
| Disclaimers | 1 general medical disclaimer | Inline + modal + footer | Per-feature disclaimers, jurisdiction-specific |
| Consent | Simplified single-purpose | Granular multi-purpose | Multi-jurisdiction, multi-product, audit-ready |
| Reading level | ≤8th grade target | ≤6th grade patient-facing, validated | PEMAT-certified, continuous monitoring |
| Voice/tone | 2-page guide | Full system with tone shifts | Automated tone scoring, brand voice AI |
| Localization | English only | 5-10 languages | 30+ languages, RTL support, locale-specific disclaimers |
| Testing | Internal review only | A/B testing, comprehension testing | Continuous experimentation, trust NPS tracking |
| Accessibility | Basic alt text | Screen reader audit | WCAG AAA content, cognitive accessibility features |
| System | Spreadsheet | CMS + TMS integration | Content design system with tokens, API-driven strings |

## When NOT to Write UX Content

```
MVP with < 10 screens? → Designer writes the copy. Dedicated UX writer is overhead.
Single-language, single-region? → UX writer can handle. No localization specialization needed.
No clinical content? → Generalist UX writer works. Health specialization not required.
Purely internal tool (clinician-only)? → Clinical informatics specialist writes. UX writer contributes tone.
```

### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | ui-ux-designer | Screen layouts, component specs, interaction patterns, character limit constraints |
| **Before** | brand-guidelines | Voice attributes, terminology, visual style that content must complement |
| **Before** | accessibility-auditor | WCAG requirements, screen reader patterns, reading order specifications |
| **This** | ux-writer | Product copy, disclaimers, consent language, error messages, voice/tone system, content design system |
| **After** | frontend-developer | Receives production-ready strings with i18n keys, implements content in components |
| **After** | translation-manager | Receives source strings with context, glossary entries, and locale-specific instructions |
| **After** | localization-engineer | Receives string keys with ICU MessageFormat, pluralization rules, and expansion buffers |

Common chains:
- **Content-to-code**: ui-ux-designer → ux-writer → frontend-developer — Design specs → final copy → implementation
- **Content localization**: ux-writer → translation-manager → localization-engineer — Source strings → translation pipeline → localized build
- **Accessible content**: accessibility-auditor → ux-writer → ui-ux-designer — Accessibility requirements → accessible copy → accessible design
- **Brand-aligned content**: brand-guidelines → ux-writer → content-strategist — Brand voice → product voice → content strategy

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `product-copy-design` | Writing onboarding, empty states, CTAs | Phase 1 |
| `medical-disclaimers` | Drafting regulatory disclaimers | Phase 2 |
| `consent-language` | Designing informed consent flows | Phase 3 |
| `health-literacy` | Simplifying clinical content | Phase 4 |
| `error-message-design` | Crafting health-context error states | Phase 5 |
| `voice-tone-systems` | Defining product voice | Phase 6 |
| `content-design-systems` | Building reusable content infrastructure | Phase 7 |
| `microcopy-testing` | A/B testing copy variants | Phase 8 |
| `content-accessibility` | Screen reader and alt text | Phase 9 |

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -->

### Solo (1 writer, 1 product)
- **What changes**: You write everything. Spreadsheet for string tracking. One general disclaimer. Flesch-Kincaid check in Word. No A/B testing — judgment calls.
- **What to skip**: Content design system, content tokens, automated tone scoring, multi-jurisdiction consent, continuous testing.
- **Coordination**: Weekly sync with designer. Monthly review with legal for disclaimers.

### Small Team (2-5 writers, 2-3 products)
- **What changes**: Shared content guidelines. Glossary in a wiki. Disclaimers in a shared library. Manual readability checks. Basic A/B testing on critical flows. 5-10 languages.
- **What to skip**: Full content design system (shared templates are enough), automated readability monitoring, continuous trust NPS tracking.
- **Coordination**: Bi-weekly content review. Quarterly voice/tone audit. Monthly sync with translation team.

### Medium Team (5-15 writers, multi-product)
- **What changes**: Content design system with tokens. TMS integration for strings. Automated readability checks in CI. A/B testing program. Designated clinical content reviewer. 20-30 languages. Per-feature disclaimers.
- **What to skip**: AI-assisted tone scoring (manual review at this scale), fully automated consent personalization.
- **Coordination**: Weekly content design system review. Bi-weekly cross-product consistency audit. Quarterly accessibility audit.

### Enterprise (15+ writers, global products)
- **What changes**: Full content design system with API-driven strings. Automated tone and readability scoring in CI/CD. Multi-jurisdiction consent engine. Continuous experimentation across all copy. Dedicated health literacy specialist. 30+ languages with locale-specific disclaimers. WCAG AAA content accessibility.
- **What's full production**: Content ops function. Brand voice AI training. Real-time translation quality monitoring. Trust NPS as a KPI. Regulatory change monitoring for disclaimer updates.
- **Coordination**: Daily content system standup. Weekly experimentation review. Monthly regulatory alignment. Quarterly board-level trust report.

### Transition Triggers
- **Solo → Small**: >200 strings, second product launch, first international market
- **Small → Medium**: >1000 strings, >10 languages, first FDA-regulated product, consent complexity exceeds manual management
- **Medium → Enterprise**: >5000 strings, multi-jurisdiction regulatory requirements, patient safety-critical content

### Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Users ignore disclaimer | Disclaimer buried in footer or too long | Move inline, use progressive disclosure, cut to 3 essential points | A disclaimer no one sees is no disclaimer at all. Place it at the decision point, not the page footer. |
| Consent comprehension <50% | Reading level too high, single checkbox pattern | Simplify to ≤6th grade, add comprehension check, split into granular options | If users can't explain what they just consented to, consent isn't informed. Test comprehension, not just checkbox completion. |
| High support tickets for "how to" | Empty states missing CTAs, onboarding skips key concepts | Add tooltips, progressive onboarding, contextual help triggers | Good UX writing anticipates confusion before the support ticket arrives. Empty states are your first documentation. |
| Translation quality complaints | English idioms, concatenated strings, no translator context | Rewrite source strings, use ICU MessageFormat, add translator comments | Source strings designed for translatability prevent downstream issues. Idioms and concatenation are the enemy of localization. |
| Accessibility audit fails | Missing alt text, heading skip, non-descriptive links | Add alt text for all images, fix heading hierarchy, rewrite link text | Accessibility in content starts at the writing stage, not during audit. Descriptive alt text and proper heading hierarchy are writing responsibilities. |
| Trust survey score drops | Tone mismatch (cheerful error for serious condition), cop-out disclaimer | Tone audit, shift to compassionate register, rewrite disclaimer for clarity | Tone mismatches erode trust faster than factual errors. The right register for the right context is critical in healthcare. |
| Regulatory finding | Disclaimer missing for AI-generated content, consent scope too broad | Add per-feature disclaimers, narrow consent options, document rationale | Regulatory requirements change. Build disclaimers and consent flows with flexibility for evolving compliance landscapes. |

## What Good Looks Like

> When UX writing is applied perfectly, every screen state — empty, loading, error, success — has clear, concise copy that guides the user forward, medical disclaimers appear at decision points without disrupting flow, all patient-facing content reads at or below 8th grade level, consent flows use granular options with comprehension checks, error messages explain what happened, the impact, and the next action, and the voice is consistent from onboarding to recovery — words build trust, reduce support tickets, and make the product feel human.

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->

- [ ] **[UW1]** Product copy reviewed for all screens: onboarding, empty states, loading, errors, success
- [ ] **[UW2]** Medical disclaimers placed at decision points with appropriate pattern (inline/modal/footer)
- [ ] **[UW3]** All patient-facing content at ≤8th grade reading level (Flesch-Kincaid validated)
- [ ] **[UW4]** Consent flows use granular options with comprehension checks and withdrawal pathways
- [ ] **[UW5]** Every error message includes: what happened + user impact + next action
- [ ] **[UW6]** Voice and tone system documented with register shifts for sensitive/clinical/encouraging contexts
- [ ] **[UW7]** All strings use ICU MessageFormat with translator context comments
- [ ] **[UW8]** Character limits defined and enforced per component type
- [ ] **[UW9]** Microcopy A/B test results documented with trust impact analysis
- [ ] **[UW10]** All images have descriptive alt text; complex diagrams have long description alternatives
- [ ] **[UW11]** Heading hierarchy valid (H1→H2→H3, no skips) and content linearizes sensibly
- [ ] **[UW12]** Content tokens defined for product name, company name, and repeated dynamic values
- [ ] **[UW13]** Disclaimer language reviewed by Legal and Regulatory before publishing
- [ ] **[UW14]** Content audit completed: no outdated medical claims, broken links, or non-inclusive language

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Strategic Writing for UX](https://www.amazon.com/dp/1492049395) — Torrey Podmajersky
- [Content Design](https://www.amazon.com/dp/B09ZYRWGHX) — Sarah Winters
- [Nicely Said](https://www.amazon.com/dp/0321988191) — Nicole Fenton & Kate Kiefer Lee
- [Health Literacy Online](https://health.gov/healthliteracyonline/) — Office of Disease Prevention and Health Promotion
- [Plain Language in Healthcare](https://www.plainlanguage.gov/) — U.S. General Services Administration
- [FDA Guidance on Medical Device Patient Labeling](https://www.fda.gov/regulatory-information/search-fda-guidance-documents) — FDA
- [PEMAT (Patient Education Materials Assessment Tool)](https://www.ahrq.gov/health-literacy/patient-education/pemat.html) — AHRQ
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — W3C Web Content Accessibility Guidelines
- [ICU MessageFormat](https://unicode-org.github.io/icu/userguide/format_parse/messages/) — Unicode Consortium
