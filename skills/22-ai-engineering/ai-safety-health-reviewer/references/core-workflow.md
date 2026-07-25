## Core Workflow

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

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.
