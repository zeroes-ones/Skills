# Core Workflow — Full Implementation

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
