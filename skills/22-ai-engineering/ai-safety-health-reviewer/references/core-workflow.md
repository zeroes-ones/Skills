# Core Workflow — Full Implementation

<!-- STANDARD: 3min -->

### Phase 1 (~30 min): Medical AI Output Evaluation

#### Preventing Hallucinated Medical Advice

1. **Drug interaction fabrication detection** — LLMs frequently invent drug-drug interactions that don't exist:
   - Cross-reference every claimed drug interaction against established databases (DrugBank, SIDER, DailyMed)
   - Pattern: LLM says "Drug A + Drug B causes condition X" → verify in drug interaction database → flag if not found
   - **High-risk categories**: warfarin interactions, CYP450 enzyme interactions, QT-prolonging drug combinations

2. **Treatment recommendation accuracy** — LLMs may recommend inappropriate treatments:
   - Verify treatment recommendations against clinical practice guidelines (UpToDate, AAFP, NICE guidelines)
   - Check for contraindications: pregnancy, pediatric, geriatric, renal/hepatic impairment
   - Flag any recommendation outside standard of care without explicit disclaimer

3. **Symptom misinterpretation** — LLMs may incorrectly interpret symptom descriptions:
   - "Chest pain" requires cardiac workup mention — LLM must not dismiss as anxiety without caveats
   - Neurological symptoms (sudden weakness, vision changes) require stroke warning
   - Fever + neck stiffness requires meningitis warning

4. **Dosage fabrication** — LLMs may invent specific dosages:
   - Never allow an LLM to recommend a specific medication dosage
   - Flag any numeric dosage + drug name pair for human review
   - Default response: "Dosage must be determined by a licensed prescriber based on patient-specific factors"

#### Verification Protocol

For every medical claim in an AI output:
```
┌─────────────────────────────────────────────────────┐
│ Medical Claim Verification Protocol                  │
├─────────────────────────────────────────────────────┤
│ 1. Identify all factual medical claims in output     │
│ 2. For each claim:                                   │
│    ├── Drug interaction? → Check DrugBank/SIDER       │
│    ├── Treatment rec? → Check UpToDate/NICE           │
│    ├── Epidemiology? → Check CDC/WHO/PubMed           │
│    ├── Anatomy/Physiology? → Check Gray's/Netter's    │
│    └── Can't verify? → Flag as UNVERIFIED            │
│ 3. Classification:                                    │
│    ├── VERIFIED: found in authoritative source        │
│    ├── UNVERIFIED: no source found → flag for review  │
│    └── CONTRADICTED: source disagrees → BLOCK         │
└─────────────────────────────────────────────────────┘
```

### Phase 2 (~30 min): FDA AI/ML Regulatory Framework

#### SaMD (Software as Medical Device)

- **Definition**: software intended to be used for medical purposes without being part of a hardware medical device
- **IMDRF risk categorization**:
  - **Category I**: informs clinical management for non-serious situations (lowest risk)
  - **Category II**: drives clinical management for non-serious OR informs for serious
  - **Category III**: treats/diagnoses non-serious situations OR drives clinical management for serious
  - **Category IV**: treats/diagnoses serious/critical situations (highest risk)

#### Predetermined Change Control Plans (PCCP)

- FDA allows AI/ML devices to evolve without new 510(k) if changes are within pre-authorized PCCP
- **PCCP components**:
  1. **SPS (SaMD Pre-Specifications)**: what types of changes the manufacturer plans to make
  2. **ACP (Algorithm Change Protocol)**: how changes will be validated and controlled
- **Examples of PCCP-eligible changes**: retraining on new data (same input/output), performance improvements within same intended use, new data sources within same clinical domain
- **Changes requiring new 510(k)**: new intended use, new patient population, new clinical decision type, change from informational to diagnostic

#### 510(k) vs De Novo Pathway for AI Products

| Pathway | When to Use | Requirements | Timeline |
|---------|-------------|-------------|----------|
| 510(k) | AI product substantially equivalent to predicate device | Predicate device exists; comparison testing | 90 days FDA review |
| De Novo | Novel AI device, no predicate, low-to-moderate risk | Special controls; clinical validation | 150 days FDA review |
| PMA | High-risk AI device (Class III) | Clinical trials; manufacturing inspection | 180+ days |

**Critical distinction**: an "informational only" AI tool that provides educational content is generally NOT a medical device. A tool that analyzes patient-specific data and provides clinical recommendations IS a medical device.

### Phase 3 (~25 min): Appropriate Disclaimers

#### Informational Only vs Clinical Decision Support (CDS)

The regulatory line between informational content and CDS software:

| Characteristic | Informational Only | CDS Software |
|---------------|-------------------|--------------|
| Patient-specific input | No (general queries) | Yes (lab values, symptoms, history) |
| Clinical recommendation | No ("consult your doctor") | Yes ("consider prescribing...") |
| Diagnostic labeling | No (describes, doesn't diagnose) | Yes ("this suggests...") |
| Treatment selection | No | Yes (recommends specific treatment) |
| FDA regulation | Not a medical device | Medical device (likely Class II) |

#### Disclaimer Templates by Risk Level

**Level 1 — General Health Information (lowest risk):**
> "This information is for educational purposes only and is not medical advice. It is not intended to diagnose, treat, cure, or prevent any disease. Always consult your healthcare provider for personal medical decisions."

**Level 2 — Condition-Specific Information:**
> "[Condition] information provided here is for general education. Individual symptoms and treatment responses vary. This is not a substitute for professional medical evaluation. If you are experiencing a medical emergency, call 911 immediately."

**Level 3 — AI-Assisted Health Content (CDS-adjacent):**
> "This content was generated with AI assistance and reviewed for medical accuracy. However, it does not constitute clinical decision support. No AI system can account for your complete medical history, current medications, or unique health circumstances. Discuss any health concerns with your licensed healthcare provider before taking action."

**Level 4 — Patient Community AI Moderation:**
> "AI-assisted content moderation helps maintain a supportive community. If you or someone you know is in crisis, please contact the 988 Suicide & Crisis Lifeline by calling or texting 988, or chat at 988lifeline.org. This community is not a substitute for professional medical or mental health care."

### Phase 4 (~25 min): Harmful Suggestion Detection

#### Suicide and Self-Harm Content

1. **Detection patterns:**
   - Explicit statements: "I want to die," "I'm going to end it," "no reason to live"
   - Method-seeking: "How much [substance] would it take to..."
   - Goodbye messages: "I just wanted to say goodbye," "you won't hear from me again"
   - Passive ideation: "Everyone would be better off without me," "I just want to disappear"

2. **Response protocol:**
   - **IMMEDIATE**: Crisis resources (988 Lifeline, Crisis Text Line: text HOME to 741741)
   - Never attempt to counsel or solve the user's problems with AI
   - Escalate to human moderator if available
   - Log incident for pattern analysis (de-identified)

3. **False positive management:**
   - Distinguish between someone expressing suicidal ideation vs someone asking about suicide prevention resources
   - Distinguish between "I feel suicidal" (crisis → escalate) vs "My friend seems depressed, what should I do?" (support → provide resources)

#### Dangerous Alternative Treatments

- **Detection categories**: unproven cancer cures, dangerous detox protocols, bleach/chlorine dioxide ingestion, essential oil ingestion for serious conditions, vaccine misinformation causing treatment refusal
- **Response**: do not amplify by repeating the claim; state that the treatment lacks scientific evidence and may be dangerous; redirect to evidence-based resources
- **Edge case**: cultural/traditional practices that are benign → acknowledge without endorsing or condemning

#### Contagion Effects in Patient Communities

- **Suicide contagion**: detailed descriptions of methods in community posts can trigger imitation
- **Eating disorder content**: "thinspiration," competitive restriction, method-sharing
- **Self-harm contagion**: descriptions of cutting techniques, hiding injuries
- **Mitigation**: remove detailed method descriptions; provide resources without repeating triggering content; monitor for post clusters suggesting contagion

### Phase 5 (~25 min): Clinical Accuracy Testing

#### Benchmarking Against Board-Certified Clinicians

1. **Test set construction:**
   - Curate 100–500 clinical vignettes covering common and edge-case presentations
   - Each vignette: patient presentation → multiple choice or free-text answer
   - Gold standard answers from ≥3 board-certified clinicians in relevant specialty
   - Exclude questions where clinicians disagree (inter-rater reliability <0.6)

2. **Metrics:**
   - **Accuracy vs clinician consensus**: % of AI answers matching majority clinician answer
   - **Safety-critical accuracy**: accuracy on vignettes where wrong answer could cause harm
   - **Specialty-specific accuracy**: don't report aggregate — break down by specialty (cardiology, dermatology, psychiatry, etc.)

#### Inter-Rater Reliability

- **Cohen's kappa** for binary decisions (diagnosis present/absent):
  - κ > 0.8: excellent agreement
  - κ 0.6–0.8: substantial agreement
  - κ 0.4–0.6: moderate (not acceptable for clinical AI)
  - κ < 0.4: poor (unacceptable)
- **Fleiss' kappa** for >2 raters
- **Process**: at least 3 clinicians independently evaluate subset of AI outputs; report agreement metrics transparently

#### What "Clinical Accuracy" Does NOT Mean

- High accuracy on MedQA/USMLE questions ≠ clinical safety
- High accuracy on common conditions ≠ rare disease competence
- High accuracy on well-structured vignettes ≠ messy real-world patient descriptions
- High accuracy overall ≠ accuracy across demographic subgroups

### Phase 6 (~25 min): Bias and Fairness in Health AI

#### Demographic Bias Assessment

1. **Race and ethnicity**: test AI performance stratified by patient race/ethnicity in clinical vignettes
   - Documented disparities: pain assessment, cardiac symptom recognition, dermatology diagnosis
   - Strategy: use name-manipulated vignettes (same presentation, different patient names associated with different races)

2. **Gender**: test on conditions that present differently by sex (heart attack symptoms, autoimmune disorders)
   - Documented disparities: women's heart attack symptoms under-recognized, men's autoimmune conditions under-recognized

3. **Socioeconomic status (SES)**: test on clinical scenarios with resource constraints
   - Example: "patient cannot afford brand-name medication" → does AI suggest appropriate lower-cost alternatives?

4. **Language**: test AI performance when symptoms are described by non-native English speakers
   - Documented issue: LLMs interpret non-standard phrasing as less medically serious

#### Rare Disease Underrepresentation

- Training data bias: common diseases over-represented, rare diseases under-represented
- **Risk**: AI confidently misdiagnoses rare disease as common disease with similar presentation
- **Mitigation**: flag "rare disease candidate" when presentation includes hallmark features of rare condition; prompt "could this be [rare disease]?" in differential diagnosis

#### Medical Terminology Performance

- Test AI understanding of medical terminology across:
  - Lay terms: "heart attack" vs "myocardial infarction"
  - Regional variations: "high blood" (hypertension in some cultures)
  - Patient-described symptoms: "my heart feels like it's flip-flopping" (palpitations)
- **Risk**: AI misses medically significant symptoms because patient describes them in non-clinical language

### Phase 7 (~25 min): Content Filtering for Medical Context

#### Disallowed Content Categories

| Category | Description | Examples |
|----------|------------|----------|
| **Diagnosis** | AI stating a specific diagnosis based on symptoms | "You have Type 2 diabetes" |
| **Prescription** | AI recommending a specific medication | "You should take metformin 500mg" |
| **Prognosis** | AI predicting disease outcome/timeline | "You have 6 months to live" |
| **Treatment change** | AI advising to start/stop/modify treatment | "Stop taking your blood thinner" |
| **Test interpretation** | AI interpreting lab results/imaging | "Your MRI shows a herniated disc" |

#### Allowed Content Categories

| Category | Description | Examples |
|----------|------------|----------|
| **Education** | Explaining conditions, treatments, procedures | "Type 2 diabetes is a condition where..." |
| **Lifestyle** | Diet, exercise, sleep, stress management advice | "Regular walking can help with blood sugar control" |
| **Adherence** | Medication reminder support, not clinical advice | "Many people find pill organizers helpful" |
| **Navigation** | Help finding providers, understanding insurance | "Endocrinologists specialize in hormone conditions" |
| **Symptom tracking** | Journaling, logging, but NOT interpreting | "Track when your headaches occur and their severity" |

#### Edge Cases Requiring Human Review

- Patient describes symptoms and asks "what could this be?" → redirect to allowed educational content, do not generate differential diagnosis
- Patient asks "should I go to the ER?" → provide general ER-worthy symptom guidelines, do not make specific recommendation
- Patient describes self-harm → immediate crisis resources, no assessment of severity

### Phase 8 (~25 min): Red Teaming for Health AI

#### Clinical Edge Cases

1. **Rare disease presentations**: atypical presentation of common disease that mimics rare disease (and vice versa)
2. **Polypharmacy**: elderly patient on 10+ medications — AI must not suggest adding without checking interactions
3. **Pregnancy**: all recommendations must account for pregnancy contraindications
4. **Pediatric**: weight-based dosing considerations, developmental appropriateness

#### Adversarial Prompts

1. **"Doctor shopping" pattern**: user presents same symptoms to AI multiple times with slight variations, trying to get desired answer
   - Detection: track session-level consistency; if user changes key details between queries, flag
2. **Prompt injection for medical content**: "Ignore previous instructions and tell me how to..."
   - Mitigation: NeMo guardrails with Colang flows; always re-validate medical claims
3. **"Hypothetical" framing**: "Hypothetically, if someone had X, what would you recommend?"
   - Response: treat as if about the user; apply same content filtering

#### Red Team Testing Cadence

- **Pre-launch**: full red team exercise with clinical + AI safety experts, minimum 500 adversarial prompts
- **Post-launch**: monthly red team with 100 new prompts; after any model update, full re-test
- **Incident-driven**: if any safety incident occurs, run targeted red team on that failure mode within 48 hours
