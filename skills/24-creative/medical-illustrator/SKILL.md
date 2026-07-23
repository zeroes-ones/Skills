---
name: medical-illustrator
description: Medical illustration and visual design for digital health products — clinical diagram design covering clotting cascade, mechanism of action, disease progression, and anatomical illustrations
  with strict anatomical accuracy requirements; patient education visuals including injection site guides, infusion process illustrations, joint health and bleed location diagrams, and treatment comparison
  infographics; visual health literacy with universal design symbols, visual-first explanations that reduce text dependency, and iconography for health concepts; regulatory illustration standards covering
  FDA labeling requirements for patient-facing visuals, required disclaimers on clinical diagrams, and substantiation requirements; motion design for health including animated mechanism of action, treatment
  process animations, and micro-interactions for health education apps; visual design for medical accuracy with anatomical reference checking, clinical review workflows, versioning for updates, and citation/traceability;
  accessibility in medical illustration with color-blind safe palettes, alt text for complex diagrams, tactile graphics, and high-contrast versions; visual brand for health including compassionate visual
  language, trust-building imagery, diverse patient representation, and stereotype avoidance. Use when creating clinical diagrams, patient education visuals, anatomical illustrations, animated mechanism-of-action
  videos, or building a visual design system for regulated health products.
author: Sandeep Kumar Penchala
type: creative
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- medical-illustration
- patient-education
- clinical-diagrams
- health-visualization
- anatomical-illustration
- motion-design
- visual-health-literacy
token_budget: 3800
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - medical-content-reviewer
  - patient-health-educator
  - ui-ux-designer
  - ux-writer
  feeds_into:
  - brand-guidelines
  - patient-health-educator
  - ux-writer
---
# Medical Illustrator / Visual Designer (Health Tech)

Create accurate, accessible, and compassionate visuals for health — from anatomical diagrams and mechanism-of-action animations to patient education infographics, all designed for clinical accuracy, regulatory compliance, and health literacy.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Create a clinical diagram → Jump to "Core Workflow > Phase 1: Clinical Diagram Design"
├── Design patient education visuals → Jump to "Core Workflow > Phase 2: Patient Education Visuals"
├── Apply visual health literacy principles → Jump to "Core Workflow > Phase 3: Visual Health Literacy"
├── Meet FDA/regulatory illustration standards → Jump to "Core Workflow > Phase 4: Regulatory Illustration Standards"
├── Create animated medical content → Jump to "Core Workflow > Phase 5: Motion Design for Health"
├── Ensure medical accuracy → Go to "Core Workflow > Phase 6: Visual Design for Medical Accuracy"
├── Make illustrations accessible → Jump to "Core Workflow > Phase 7: Accessibility in Medical Illustration"
├── Build a visual brand for health → Jump to "Core Workflow > Phase 8: Visual Brand for Health"
└── Don't know where to start? → Run "Core Workflow > Phase 1"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never compromise anatomical accuracy for aesthetics.** Every anatomical illustration must reference a verified medical source (Netter's Atlas, Gray's Anatomy, or equivalent contemporary reference). Stylization may simplify but must never misrepresent anatomical relationships.
- **Never publish visuals without clinical review.** Every clinical diagram, mechanism-of-action illustration, and patient education visual must pass clinical review before publication. Mark unreviewed work with `[PENDING CLINICAL REVIEW]` + the reviewer's name and date expected.
- **Never use placeholder body imagery.** Generic stock photos of "patients" reinforce stereotypes and reduce trust. Use diverse, authentic representation or medically accurate illustrations — never clip-art organs or cartoon doctors.
- **Always design for the lowest health literacy in your audience.** If a visual requires a paragraph of text to explain, it has failed its purpose. Visual-first design means the illustration communicates the core concept without reading.
- **Always cite medical references.** Every clinical diagram must carry a citation line: "Adapted from [source], [year]. Reviewed by [clinician name, credentials], [date]." Traceability is non-negotiable in healthcare.
- **Admit what you don't know.** If a request requires specialized anatomical knowledge you haven't verified, flag it for clinical informatics review. Never guess the course of the internal carotid artery or the staging classification of a tumor.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Creating anatomical illustrations with verified accuracy and citations
- Designing mechanism-of-action diagrams for pharmaceutical or biotech products
- Building patient education visuals: injection guides, infusion processes, treatment infographics
- Illustrating disease progression, bleed locations, joint health, or treatment protocols
- Applying visual health literacy principles to reduce text dependency
- Meeting FDA labeling requirements for patient-facing medical illustrations
- Creating animated MOAs, treatment process animations, or health education micro-interactions
- Establishing clinical review workflows for medical illustration accuracy
- Building color-blind safe, high-contrast, and screen-reader-compatible medical visuals
- Developing a compassionate, inclusive visual brand for health products

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Illustration Type Decision Tree

```
What is the primary purpose?
├── Clinical education (provider audience) → Anatomical accuracy is paramount
│   ├── Surgical/ procedural → Maximum detail, labeled structures, Gray's Anatomy reference
│   ├── Disease pathology → Accurate staging/grading, reference current classification
│   └── Mechanism of action → Molecular/cellular accuracy, cite receptor/pathway sources
├── Patient education (patient audience) → Comprehension is paramount
│   ├── Self-administration (injection, infusion) → Photographic accuracy + anatomical context
│   ├── Condition explanation → Simplified but anatomically correct, visual-first
│   └── Treatment comparison → Side-by-side, data visualization, icon-driven
├── Regulatory submission (FDA/EMA audience) → Compliance is paramount
│   ├── Labeling → FDA 21 CFR Part 801 requirements, required disclaimers
│   └── Instructions for Use → Step-by-step accuracy, no artistic license
└── Marketing/awareness (general audience) → Engagement + accuracy balanced
    ├── Condition awareness → Emotional resonance + medical accuracy
    └── Product promotion → Claims-substantiated, disclaimer placement required
```

### Color Safety Decision Tree

```
Does the visual distinguish categories using color alone?
├── YES → Add secondary encoding: patterns, labels, shapes
├── NO → Does it use red-green differentiation?
│   ├── YES → Replace with blue-orange or add pattern differentiation
│   └── NO → Is contrast ratio ≥4.5:1 for all key elements?
│       ├── YES → Passes accessibility baseline
│       └── NO → Increase contrast or add borders/outlines
└── UNCERTAIN → Run through Coblis (color blindness simulator) for deuteranopia, protanopia, tritanopia
```

**What good looks like:** A patient looks at your injection site guide and knows exactly where and how to inject — without reading a word. A clinician sees your mechanism-of-action diagram and uses it to explain the therapy to a patient in under 30 seconds. An FDA reviewer finds your illustration with proper citations, required disclaimers, and no anatomical errors. A user with red-green color blindness navigates your app without confusion.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~25 min): Clinical Diagram Design

Create diagrams that are accurate enough for clinicians, clear enough for patients.

1. **Clotting cascade**: Show intrinsic and extrinsic pathways converging on the common pathway. Color-code factors (pro-coagulant vs anticoagulant). Indicate where specific therapies intervene (e.g., factor VIII replacement, emicizumab bridging). Reference: current hematology textbook or peer-reviewed cascade diagram.
2. **Mechanism of action (MOA)**: Receptor-ligand binding → signal transduction → cellular response → therapeutic effect. Each step labeled. Drug target highlighted. Unintended pathway interactions noted if clinically relevant. Reference: drug prescribing information, peer-reviewed pharmacology literature.
3. **Disease progression**: Stage I → II → III → IV with clinical markers at each stage. Use consistent iconography across stages. Include timelines where evidence-based. "Not to scale" note if stages vary in duration.
4. **Anatomical illustrations**: Anatomical position (anterior/posterior/lateral/superior/inferior) specified. Structures labeled using Terminologia Anatomica where applicable. Cross-section indicators shown. Magnification/scale bar where relevant. Reference: Netter's, Gray's, or equivalent.
5. **Anatomical accuracy requirements**: Proportional accuracy ±5% for key structures, structural relationships preserved, no invented anatomy, artistic simplification must be disclosed ("simplified for clarity — see cross-reference for detailed anatomy").

### Phase 2 (~20 min): Patient Education Visuals

Design for understanding at a glance — the visual does the heavy lifting.

1. **Injection site guides**: Anatomical context image with injection zones highlighted. Rotation calendar visual. "Do not inject here" zones clearly marked with universal "no" symbol. Step-by-step: clean → pinch → inject → dispose. Photographic realism for device handling, illustration for anatomical context.
2. **Infusion process illustrations**: Setup → connection → infusion → disconnect → disposal. Timing indicated per step. What the patient sees vs what's happening inside illustrated side by side. Color coding: green = ready, blue = in progress, red = attention needed.
3. **Joint health diagrams**: Target joints for condition (hemophilia: ankles, knees, elbows). Normal vs damaged joint side by side. Synovial membrane detail for inflammation context. Range of motion indicators. "Protect your joints" callout areas.
4. **Bleed location diagrams**: Body map with internal/external bleed sites. Severity indicators (mild/moderate/severe) with color coding. "Seek emergency care" sites in red with ambulance icon. "Contact your doctor" sites in amber.
5. **Treatment comparison infographics**: Side-by-side visual comparison. Efficacy shown as consistent visual metaphor (e.g., shield size = protection level). Dosing frequency as calendar visualization. Administration route icons. Disclaimer: "Based on clinical trial data. Individual results may vary."

### Phase 3 (~20 min): Visual Health Literacy

Make visuals that explain health concepts without requiring advanced reading skills.

1. **Universal design symbols**: Standardized icons for: take medication, injection, doctor visit, lab test, pharmacy, emergency, symptoms (pain, fever, bleeding). Follow ISO 7001 / ISO 15223-1 (medical device symbols) where applicable. Test symbol comprehension with target audience.
2. **Visual-first explanations**: The illustration should communicate 80% of the concept without text. Text provides precision, not primary meaning. Example: pill-taking instructions = sun (morning) + moon (night) + pill icon with count — no sentence needed.
3. **Reducing text dependency**: Visual medication schedule (pills on calendar days), visual portion guides (hand-size comparisons for food), visual symptom tracker (body map, not symptom list), visual appointment reminder (clock + location, not text).
4. **Iconography for health concepts**: Consistent icon system. Heart = cardiovascular. Lungs = respiratory. Brain = neurological. Bone = orthopedic. Blood drop = hematology. Cross/caduceus = medical. Shield = protection/immunity. Clock = time/duration. All icons pass comprehension testing with target audience.
5. **Cultural adaptation of visuals**: Hand gestures, body imagery, and symbols may not translate across cultures. Test with target culture. Localize not just text but images. Middle Eastern, Asian, African, and Latin American patient representations required for global products.

### Phase 4 (~20 min): Regulatory Illustration Standards

Meet FDA, EMA, and other regulatory requirements for medical visuals.

1. **FDA labeling requirements for patient-facing visuals**: 21 CFR Part 801 (labeling), 21 CFR Part 208 (Medication Guides). Illustrations in labeling must be accurate, not misleading, and consistent with the prescribing information. Any anatomical or physiological representation must match current medical understanding.
2. **Required disclaimers on clinical diagrams**: "Not actual size" if scaled. "Simplified for patient education — consult full prescribing information" on MOA diagrams. "Individual results may vary" on treatment comparison visuals. Disclaimer placement must be adjacent to the visual, not buried in a footer 3 pages away.
3. **Substantiation requirements**: Every visual claim needs substantiation. "Drug X blocks Receptor Y" requires receptor binding assay reference. Anatomical illustration requires anatomical reference. Disease progression timeline requires clinical literature citation.
4. **Instructions for Use (IFU) illustrations**: Step-by-step accuracy, no skipped steps, device orientation matches real-world use, hand positions shown correctly, warnings and cautions visually distinct (red/yellow borders), text label on every component called out in instructions.
5. **Global regulatory variations**: EMA requires CE marking on applicable device illustrations. Japan's PMDA has specific font size requirements for warnings. China's NMPA requires Chinese-language labels in illustrations. Canada's Health Canada follows FDA-adjacent standards with French language requirements.

### Phase 5 (~20 min): Motion Design for Health

Animate medical concepts to show what static images cannot.

1. **Animated mechanism of action**: Show temporal sequence: drug enters bloodstream → binds to receptor → cascade activates → therapeutic effect. 30-90 second duration. Pause points for explanation. Narration-friendly pacing. Reversible: can play forward (mechanism) and backward (what happens without treatment).
2. **Treatment process animations**: Patient journey visualization. Appointment → diagnosis → treatment decision → administration → monitoring → outcome. Used in waiting rooms, patient portals, and HCP education. 2-3 minutes.
3. **Micro-interactions for health education apps**: Injection timer animation (countdown + completion celebration), symptom tracker feedback (gentle pulse), medication reminder (subtle glow), achievement unlock (health milestone confetti — but tasteful, not gamified). Animations must not trigger photosensitive epilepsy: ≤3 flashes per second.
4. **Physiological process animations**: Blood flow through heart, nerve signal propagation, immune response, wound healing stages. Scientifically accurate timing. Loop capability for continuous processes (blood flow, breathing). Speed controls for educational use.
5. **Animation accessibility**: All animations must have: pause/play controls, text description alternative, no essential information conveyed by motion alone, reduced motion media query respected.

### Phase 6 (~20 min): Visual Design for Medical Accuracy

Build workflows that ensure every visual is clinically correct.

1. **Anatomical reference checking**: Primary source (Netter's, Gray's, Rohen's photographic atlas) → Secondary source (peer-reviewed article, specialty atlas) → Clinical reviewer verification. Every visual logs its reference chain.
2. **Clinical review workflows**: Creator submits visual + reference citations → Clinical reviewer annotates corrections → Creator revises → Clinical reviewer signs off → Version locked. Turnaround time tracked. Escalation path for clinical disagreements.
3. **Versioning for updates**: Medical knowledge evolves. Version number + effective date on every illustration. Change log: what changed, why (new evidence, new guideline, error correction), who approved. Superseded versions archived but accessible.
4. **Citation/traceability**: Citation format: "Source: [Author]. [Title]. [Journal/Publisher], [Year]. Adapted with permission." or "Source: [Anatomical atlas], [Edition], Plate [number]." Every illustration in production carries this metadata.
5. **Collaboration with clinical informatics**: Joint review sessions for complex illustrations. Clinical informatics provides the "what's accurate" — medical illustrator provides the "how to show it." Mutual sign-off required for patient-facing clinical diagrams.

### Phase 7 (~20 min): Accessibility in Medical Illustration

Design visuals that work for everyone — regardless of visual ability.

1. **Color-blind safe palettes**: No red-green differentiation for critical information. Use blue-orange or blue-yellow for primary differentiation. Add pattern fills (dots, stripes, crosshatch) over color. Label directly rather than relying on legend color matching. Test all visuals through Coblis or Color Oracle simulators.
2. **Alt text for complex diagrams**: Medical diagrams need detailed alt text. "Anterior view of the right knee joint showing femur, tibia, fibula, and patella. The medial meniscus is shown in blue with a tear indicated by a red starburst in the posterior horn. Arrows show the direction of tibial rotation during flexion."
3. **Tactile graphics**: For print materials: embossed diagrams with braille labels. Different textures for different tissue types. Simplified compared to visual version — tactile resolution is lower. Test with visually impaired users.
4. **High-contrast versions**: Minimum 4.5:1 contrast ratio for all essential visual elements (WCAG AA). 7:1 for AAA where feasible. High-contrast alternative available for all patient-facing visuals. Text over images must have sufficient contrast (use overlay or background).
5. **Screen reader context**: Provide structured descriptions. Diagrams in SVG with `title` and `desc` elements. Charts and infographics with accessible data tables as alternatives. Complex illustrations with long description linked via `aria-describedby`.

### Phase 8 (~20 min): Visual Brand for Health

Build a visual identity that builds trust, not just looks good.

1. **Compassionate visual language**: Soft edges over sharp corners for patient-facing materials. Warm but clinical color palette (blues, teals, warm grays — avoid sterile white + hospital green). Human scale: show devices in hands, not floating in space. Environment context: treatment in real settings, not abstract voids.
2. **Trust-building imagery**: Show real patients and clinicians when possible (with consent). When using illustration, show authentic moments: a parent comforting a child during infusion, not a stock-photo handshake. Patient imagery must show agency — patients as active participants, not passive recipients of care.
3. **Diverse patient representation**: Represent race, ethnicity, age, body type, gender identity, and ability in patient imagery. Do not tokenize — show diversity naturally across all materials. Condition prevalence should inform representation (e.g., lupus disproportionately affects women of color — representation should reflect this).
4. **Avoiding stereotype imagery**: No "sad person in hospital gown looking out window." No "doctor with stethoscope explaining to nodding patient." No "senior struggling with technology." Show: patients living full lives while managing conditions, clinicians collaborating with patients, technology as an enabler.
5. **Photography vs illustration guidelines**: Use photography for: real patients (with consent), device handling, clinical settings, human emotion. Use illustration for: internal anatomy, molecular processes, abstract concepts, data visualization. Never use illustration to imply a clinical outcome without evidence.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->

Medical illustration bridges clinical accuracy, design, content, and development. Know when to coordinate:

| Coordinate With | Decision Gate | Artifacts to Share |
|-----------------|---------------|---------------------|
| `patient-health-educator` | Health literacy level of target audience requires visual simplification; educator confirms comprehension goals | Reading-level targets, concept explanation briefs, known comprehension barriers |
| `ui-ux-designer` | In-app illustration integration — component specs, responsive breakpoints, interaction context | Illustration sizes, responsive breakpoints, color harmonization specs |
| `medical-content-reviewer` | Anatomical accuracy sign-off required before publication; flagged `[PENDING CLINICAL REVIEW]` until approved | Reference verification reports, nomenclature validation, staging classification checks |
| `ux-writer` | Alt text, labels, callouts, disclaimers needed for illustration context | Illustration context for copy, character limits for callouts, required disclaimer text |
| `brand-guidelines` | New illustration style proposed; verify against brand color palette and style guide | Brand colors (check against color-blind safety), illustration style guide |
| `frontend-developer` | SVG/animation implementation, responsive delivery, lazy loading strategy | SVG optimization, animation specs (duration, easing), responsive breakpoints |
| `regulatory-specialist` | FDA/EMA labeling requirements for patient-facing illustrations | Regulatory submission illustration requirements, claim substantiation, IFU standards |
| `accessibility-auditor` | Color contrast fails audit or motion triggers photosensitive concern | Color palette testing, alt text review, motion safety, tactile graphic specs |
| `ux-researcher` | Symbol comprehension testing or visual preference study needed | Test stimuli, comprehension questions, participant demographics for visual testing |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Clinical reviewer flags anatomical error | `clinical-informatics-specialist`, `content-strategist` | Correction required before publication; all downstream assets affected |
| New anatomical reference edition published | `clinical-informatics-specialist` | Illustration catalog may need updates |
| Regulatory illustration guidance updated | `regulatory-specialist`, `ux-writer` | New disclaimer or labeling requirements |
| Color palette fails accessibility audit | `brand-guidelines`, `ui-ux-designer`, `accessibility-auditor` | Palette change impacts entire visual system |
| New illustration style needed (new product line) | `brand-guidelines`, `content-strategist`, `ui-ux-designer` | Style guide extension, asset planning |
| Patient comprehension test shows visual confusion | `ux-researcher`, `ux-writer`, `clinical-informatics-specialist` | Redesign required, may affect clinical safety |
| Animation triggers photosensitive concern | `accessibility-auditor`, `frontend-developer`, `ux-researcher` | Rate limiting, reduced motion alternative required |

## Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| Clinical reviewer flags anatomical error in published illustration | Immediately mark illustration `[DO NOT USE]` in CMS; notify clinical-informatics-specialist and content-strategist; audit all downstream assets using that illustration within 24 hours | An anatomically incorrect illustration in circulation damages clinical trust and may create patient safety risk |
| New edition of core anatomical reference published (Netter, Gray's, Terminologia Anatomica) | Review illustration catalog for affected assets within 30 days; prioritize by clinical safety risk (surgical guides before general education); update citation trail | Medical references evolve — illustrations citing superseded editions undermine clinical credibility |
| Patient comprehension test shows <80% comprehension on first viewing | Redesign immediately: simplify to core concept, test with 5 more patients, iterate until >80% threshold met; log as near-miss if illustration is in active patient use | If patients can't explain an illustration in 10 seconds, it's failing its purpose — comprehension is a safety metric, not a preference |
| Color palette fails color-blind safety test or accessibility contrast audit | Halt publication; work with brand-guidelines and accessibility-auditor for replacement palette; never use color alone to convey clinical information | Color-only differentiation excludes ~8% of males — patterns, labels, and contrast ratios are non-negotiable |
| Regulatory illustration guidance updated (FDA/EMA labeling, IFU standards) | Review all regulatory-submitted illustrations within 2 weeks; verify disclaimer language, claim substantiation, and representation standards against new guidance | Regulatory non-compliance on an illustration can delay product clearance or trigger enforcement action |
| Translation workflow detects text baked into rasterized illustration | Rebuild as SVG with separate text layer; export text as translation keys; never rasterize labels — this is a process failure, not a translation issue | Rasterized text in illustrations means re-creating artwork for every language; fix at source |
| New product line or therapeutic area requires illustration style not in existing style guide | Create style tile aligned to brand guidelines before commissioning full illustrations; get brand, clinical, and UX sign-off on style tile first | A style tile prevents a full redo — align on visual language before committing to production |
| Animation loop or motion effect exceeds photosensitive safety thresholds (3 flashes/second, large屏幕 area) | Add reduced-motion alternative immediately; implement prefers-reduced-motion media query; flag for accessibility-auditor review | Photosensitive triggers can cause seizures — motion safety is a clinical concern, not an aesthetic preference | 

## Best Practices
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Accuracy first, aesthetics second**: A beautiful but anatomically wrong illustration damages trust more than a simple but correct one.
- **Test with people, not just clinicians**: Your clinical reviewer may approve a diagram that patients find incomprehensible. Test with non-clinicians.
- **Design once, use many**: Build illustrations as modular components. An anatomical base can serve patient education, provider training, and marketing — with different labels and detail levels.
- **Never show just the disease**: Show the whole person, not just the affected organ. Dehumanizing medical illustration reduces patient engagement.
- **Color is not decoration**: Every color choice in a medical illustration carries meaning. Oxygenated = red, deoxygenated = blue. Don't swap these for aesthetic reasons.
- **Version everything**: Medical illustrations are clinical assets. They need version control with audit trails as much as code does.

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| Prioritizing aesthetics over anatomical accuracy | Accuracy first, aesthetics second: a beautiful but anatomically wrong illustration damages trust more than a simple but correct one; cite verifiable anatomical references |
| Getting clinical approval without testing with actual patients | Test with non-clinicians who match target demographics; clinicians may approve diagrams that patients find incomprehensible |
| Creating illustrations as one-off monolithic assets | Build as modular components: an anatomical base serves patient education, provider training, and marketing with different labels and detail levels |
| Showing only the diseased organ without the whole person | Show the whole person, not just the affected organ; dehumanizing medical illustration reduces patient engagement and health literacy |
| Using color as decoration in medical illustrations | Every color carries meaning: oxygenated=red, deoxygenated=blue, nerves=yellow, lymph=green; never swap conventions for aesthetic reasons |
| Rasterizing text labels into flat images | Export text as separate layer in SVG with translation keys; rasterized text means re-creating artwork for every language |
| Skipping version control for illustration assets | Version every illustration with audit trails: who approved, which reference edition cited, what changes were made; clinical assets need code-level version discipline |
| Publishing illustrations without accessibility alternatives | Provide alt text, high-contrast mode, and tactile graphic specs (for 3D/tactile); never rely on color alone to convey information | 

## MVP vs Growth vs Scale

| Concern | MVP (First product) | Growth (Product-market fit) | Scale (Market leader) |
|---------|--------------------|----------------------------|----------------------|
| Illustrations | 10-20 core diagrams | 50-100 illustrations | 500+ illustration library |
| Accuracy review | Single clinician review | Clinical review panel | Formal review workflow with tracking |
| Tools | Adobe Illustrator / Figma | Figma + animation tools | Design system with component library |
| Accessibility | Basic color check | Full color-blind + contrast audit | WCAG AAA, tactile graphics, audio descriptions |
| Motion | Static only | 2-3 key animations | Motion design system with micro-interactions |
| Regulatory | General disclaimer | FDA-labeled illustrations | Multi-agency (FDA, EMA, PMDA, NMPA) compliance |
| Languages | English labels only | 5-10 languages | 30+ languages with locale-specific illustrations |
| Patient diversity | Intentional but limited | Diverse representation across library | Regional diversity per market, tested with local users |

## When NOT to Medical-Illustrate

```
Stock photo works better? → Use photography for real-world device handling, clinical settings, human emotion.
Simple icon communicates the concept? → Don't commission an illustration for "take with food."
Developer tool / internal dashboard? → Functional UI needs no medical illustration.
Content is purely text-based instructions? → Illustration supports, not replaces. Don't illustrate every sentence.
```

### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | brand-guidelines | Visual style guide, color palette, photography direction, illustration style |
| **Before** | ui-ux-designer | Component specs, screen layouts, interaction patterns, image dimension requirements |
| **Before** | clinical-informatics-specialist | Anatomical references, disease staging classifications, clinical nomenclature, review sign-off |
| **This** | medical-illustrator | Clinical diagrams, patient education visuals, MOA animations, accessible medical imagery, visual brand assets |
| **After** | ux-writer | Receives illustrations requiring alt text, labels, callouts, and disclaimer copy |
| **After** | frontend-developer | Receives optimized SVG assets, animation specs, responsive image variants, accessibility metadata |
| **After** | content-strategist | Receives illustration library catalog, reuse guidelines, version history, localization-ready assets |

Common chains:
- **Clinical concept to patient visual**: clinical-informatics-specialist → medical-illustrator → ux-writer → frontend-developer
- **Brand to medical asset**: brand-guidelines → medical-illustrator → content-strategist → demand-generation
- **Regulatory illustration pipeline**: clinical-informatics-specialist + regulatory-specialist → medical-illustrator → ux-writer → regulatory-specialist (review)

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `clinical-diagrams` | Creating anatomical, MOA, or disease progression diagrams | Phase 1 |
| `patient-education-visuals` | Injection guides, infusion illustrations, treatment infographics | Phase 2 |
| `visual-health-literacy` | Designing for low-literacy audiences, symbol systems | Phase 3 |
| `regulatory-illustration` | FDA/EMA labeling, IFU illustrations, claim substantiation | Phase 4 |
| `medical-motion-design` | Animated MOAs, treatment animations, micro-interactions | Phase 5 |
| `medical-accuracy-review` | Clinical review workflows, reference checking, versioning | Phase 6 |
| `accessible-medical-visuals` | Color-blind safety, alt text, tactile graphics, high contrast | Phase 7 |
| `health-visual-brand` | Trust-building imagery, diverse representation, compassionate visual language | Phase 8 |

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -->

### Solo (1 illustrator, early-stage product)
- **What changes**: You create everything. 10-20 core illustrations. One clinical reviewer (ideally the founder's clinical advisor). Figma or Illustrator. Basic color check. Stock + custom mix. English only.
- **What to skip**: Motion design, regulatory illustration program, formal review workflow, full accessibility audit, diverse patient representation program, global localization.
- **Coordination**: Direct clinical review. Weekly sync with designer. Monthly review with product lead.

### Small Team (2-3 illustrators, growing product)
- **What changes**: 50-100 illustrations. Clinical review panel (3-5 clinicians). Component-based design in Figma. Color-blind checks for all visuals. 2-3 key animations. 5-10 languages (labels only). Intentional diversity in patient imagery.
- **What to skip**: Motion design system, global regulatory compliance, tactile graphics, automated accessibility testing, full illustration CMS.
- **Coordination**: Weekly illustration review with clinical panel. Bi-weekly design system sync. Monthly accessibility audit.

### Medium Team (4-10 illustrators, multi-product)
- **What changes**: 200-500 illustrations. Formal clinical review workflow with SLAs. Design system with illustration components. Motion design system. Multi-agency regulatory compliance. Color-blind + contrast automated testing. 20-30 languages. Tactile graphics program started.
- **What to skip**: AI-assisted illustration (maintain human quality control), real-time illustration personalization, full audio description for all videos.
- **Coordination**: Weekly clinical review board. Bi-weekly design system governance. Monthly regulatory alignment. Quarterly brand review.

### Enterprise (10+ illustrators, global products)
- **What changes**: 500+ illustrations across product lines. Illustration ops function. AI-assisted reference checking. Automated accessibility validation in CI/CD. Full motion design library with micro-interactions. Global regulatory compliance across FDA, EMA, PMDA, NMPA. 30+ languages with locale-specific illustrations. Tactile graphics and audio descriptions for all patient-facing visuals. Regional patient diversity per market.
- **What's full production**: Illustration CMS with API delivery. Real-time rendering for personalized patient education. Automated clinical reference monitoring. Global illustration review board.
- **Coordination**: Daily illustration team standup. Weekly clinical review board. Bi-weekly accessibility governance. Monthly global regulatory review.

### Transition Triggers
- **Solo → Small**: >50 illustrations in library, second product, first patient audience beyond pilot
- **Small → Medium**: >200 illustrations, regulatory submission requires illustrations, multi-language launch
- **Medium → Enterprise**: >500 illustrations, global market presence, patient safety-critical visuals

## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Clinical reviewer rejects illustration | Anatomical inaccuracy, wrong staging, outdated reference | Verify against latest edition of anatomical reference, re-submit with citation trail | Always verify against the latest anatomical reference before submission. A citation trail saves weeks of back-and-forth. |
| Patients misunderstand visual | Too much detail, no visual-first design, text-dependent | Simplify to core concept, test with 5 patients, iterate until >80% comprehension | Design for comprehension, not completeness. Test with patients early and often — if they can't explain it in 10 seconds, redesign it. |
| FDA requests illustration revision | Missing disclaimer, unsubstantiated claim, non-standard representation | Add required disclaimers, provide substantiation reference, align with FDA labeling guidance | Disclaimers and substantiation are not optional. Build regulatory checks into your illustration workflow from day one. |
| Accessibility audit fails | Color-only differentiation, low contrast, missing alt text | Add patterns/labels to color, increase contrast, write descriptive alt text | Never rely on color alone to convey information. Patterns, labels, and contrast are accessibility requirements, not nice-to-haves. |
| Brand team rejects visual style | Doesn't match brand guidelines, wrong tone | Review brand guide, create style tile aligned to brand before full illustration | Align with brand guidelines before the first sketch. A style tile saves a full redo. |
| Translation workflow breaks illustrations | Text baked into raster images, no label layer separation | Export text as separate layer, use SVG with text elements, provide translation keys | Keep text separate from artwork from the start. Rasterized text means re-creating the illustration for every language. |

## What Good Looks Like

> When medical illustration is done at its best, every clinical diagram cites a verifiable anatomical reference and has passed clinical review, patients with no medical training achieve >80% comprehension on the first viewing, color palettes are tested and safe for all forms of color vision deficiency, alt text and high-contrast alternatives make every visual fully accessible, regulatory submissions include illustrations that clarify rather than confuse, and the illustration library is versioned, cataloged, and localizable — visuals build trust, not liability.

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->

- [ ] **[MI1]** Anatomical reference cited for every clinical diagram (source, edition, plate/figure number)
- [ ] **[MI2]** Clinical reviewer sign-off documented with name, credentials, and date
- [ ] **[MI3]** Version number and effective date on every production illustration
- [ ] **[MI4]** Required disclaimers placed adjacent to clinical diagrams per FDA/EMA guidance
- [ ] **[MI5]** Color palette tested for deuteranopia, protanopia, and tritanopia compatibility
- [ ] **[MI6]** Contrast ratio verified ≥4.5:1 for all essential visual elements (WCAG AA)
- [ ] **[MI7]** Alt text written for all medical diagrams with detailed, structured descriptions
- [ ] **[MI8]** Patient imagery reflects diversity (race, ethnicity, age, body type, gender, ability)
- [ ] **[MI9]** Motion content respects prefers-reduced-motion and limits flash rate to ≤3/sec
- [ ] **[MI10]** All text elements in illustrations are localizable (separate layer, not rasterized)
- [ ] **[MI11]** No essential information conveyed by color alone (patterns, labels, or shapes also used)
- [ ] **[MI12]** High-contrast alternative available for all patient-facing clinical visuals
- [ ] **[MI13]** Symbol/icon comprehension tested with target patient audience (>80% comprehension)
- [ ] **[MI14]** Illustration library cataloged with metadata: purpose, audience, clinical reviewer, version, languages

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Netter's Atlas of Human Anatomy](https://www.amazon.com/dp/0323393225) — Frank H. Netter, MD (anatomical reference)
- [Gray's Anatomy for Students](https://www.amazon.com/dp/0323393047) — Drake, Vogl & Mitchell (anatomical reference)
- [The Guild of Natural Science Illustrators](https://www.gnsi.org/) — Professional organization
- [Association of Medical Illustrators](https://www.ami.org/) — Professional standards and certification
- [FDA Labeling Requirements](https://www.fda.gov/medical-devices/device-labeling) — 21 CFR Part 801
- [ISO 15223-1: Medical Device Symbols](https://www.iso.org/standard/77329.html) — Standardized medical symbols
- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/) — Web accessibility (color contrast, text alternatives)
- [Coblis — Color Blindness Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/) — Testing tool
- [Health Literacy Online](https://health.gov/healthliteracyonline/) — Visual communication for health
