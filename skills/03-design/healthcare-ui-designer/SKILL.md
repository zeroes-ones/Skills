---
name: healthcare-ui-designer
description: >
  Use when designing user interfaces for healthcare applications — electronic health
  records (EHR), patient portals, clinical decision support tools, telemedicine
  platforms, medical device interfaces, pharmacy systems, and health tracking apps.
  Handles clinical data display patterns (lab results, vitals trends, medication
  schedules), PHI-aware UI design (lock badges, auto-logout, consent checkpoints,
  audit trails), FDA human factors requirements for medical devices, patient-facing
  UX for varying health literacy levels, and clinical workflow efficiency. Do NOT
  use for HIPAA compliance implementation (route to hipaa-technical-implementation),
  health regulatory submissions (route to health-regulatory-submission), or general
  healthcare UX research (route to patient-experience-researcher).
license: MIT
allowed-tools: Read Grep Glob
tags:
  - healthcare
  - medical
  - ehr
  - clinical
  - patient
  - telemedicine
  - fda
  - hipaa
  - accessibility
  - health-literacy
author: Sandeep Kumar Penchala
type: design
status: stable
version: 1.0.0
updated: 2026-07-26
token_budget: 3200
chain:
  consumes_from:
    - ui-ux-designer
    - accessibility-auditor
    - patient-experience-researcher
  feeds_into:
    - frontend-developer
    - mobile-developer
    - hipaa-technical-implementation
---
# Healthcare UI Designer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

Design interfaces for healthcare — a domain where **clarity saves lives, ambiguity causes harm, and accessibility is a legal requirement.** Healthcare UI serves two fundamentally different audiences: clinicians (power users under time pressure who need efficiency) and patients (diverse health literacy levels who need clarity and reassurance).

## Route the Request

### Auto-Route

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.tsx", "FHIR|patient|medication|lab.result|vital")` | Clinical app detected. Jump to **Core Workflow → Clinical Interfaces**. |
| A2 | `file_contains("*.tsx", "appointment|portal|message|prescription.refill")` | Patient portal detected. Jump to **Core Workflow → Patient-Facing UX**. |
| A3 | `file_contains("*.css", "telemedicine|video.call|virtual.visit")` | Telemedicine platform. Jump to **references/telemedicine-patterns.md**. |
| A4 | `file_contains("requirements", "FDA|510(k)|human.factors|IEC.62366")` | Medical device software. Jump to **Core Workflow → Medical Device UI**. |

### Intent Route

```
What are you building?
├── Clinical interface (EHR, lab results, medication administration) → Clinical Interfaces
├── Patient portal (appointments, prescriptions, secure messaging) → Patient-Facing UX
├── Telemedicine platform (virtual visits, waiting room, post-visit summary) → Telemedicine UX
├── Medical device UI (patient monitor, infusion pump, diagnostic device) → Medical Device UI
├── Pharmacy system (medication management, drug interactions, dispensing) → Pharmacy UX
├── Health tracking app (symptoms, vitals, activity, sleep) → Consumer Health UX
├── Clinical decision support (alerts, guidelines, risk scores) → Decision Support UX
└── Not sure → Describe the clinical context and primary user
```

## Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Never display patient data without a visible PHI indicator — users must know they're viewing protected information | `file_contains(output, "patient|PHI|health.record")` AND NOT `file_contains(output, "PHI.badge|lock|protected|confidential|auto.logout")` | REFUSE. "Patient data must be visually marked as PHI. Add lock badge, 'Confidential' label, and auto-logout timer indicator." |
| G2 | Never show medication names or dosages without both brand AND generic names, and never abbreviate units of measure | `file_contains(output, "mg|mcg|mL|IU")` AND NOT `file_contains(output, "milligram|microgram|milliliter|international.unit")` | DETECT. "Medication units must be spelled out: 'milligram' not 'mg', 'microgram' not 'mcg'. Include generic name alongside brand name." |
| G3 | Never use red for non-critical information — in healthcare, red means emergency, error, or critical alert | `file_contains(output, "red")` AND NOT `file_contains(output, "critical|emergency|error|alert|warning")` | STOP. "Red is reserved for critical/emergent information in healthcare. Use amber/orange for warnings, blue/info for neutral." |
| G4 | Never design a clinical workflow that requires more than 3 clicks to complete a common task | `file_contains(output, "clinician|nurse|physician")` AND `file_contains(output, "step.*[4-9]|step.*10")` | REFUSE. "Clinicians work under time pressure. Common tasks (medication administration, vitals entry, note signing) must complete in ≤3 clicks." |
| G5 | Never design patient-facing content above a 6th-grade reading level without offering a simplified version | `file_contains(output, "patient|portal|consumer")` AND NOT `file_contains(output, "simplified|plain.language|easy.read|grade.level")` | DETECT. "Patient content must target 6th-grade reading level. Provide simplified versions for all medical terminology. Test with readability tools." |

## The Expert's Mindset

Healthcare UI is **safety-critical design**. A confusing medication list can cause a wrong dose. A poorly designed alert can cause alert fatigue and missed critical warnings. A patient who can't understand their discharge instructions will be readmitted. Every pixel in a healthcare interface carries ethical weight.

### Mental Models

| Model | Description |
|---|---|
| **Clinical context is everything** | A heart rate of 120 means different things for a neonate (normal), an adult (tachycardia — investigate), and a marathon runner (expected). Never display vitals without age-adjusted reference ranges. |
| **Alert fatigue kills** | When everything is critical, nothing is. Reserve red and "Alert" for life-threatening conditions only. Use amber for warnings, blue for info. If a clinician dismisses 50 alerts per shift without reading them, your alert design has failed. |
| **Patient health literacy is 6th grade** | The average American reads at a 7th-8th grade level. Health information must be at 6th grade or below. "Take one tablet by mouth twice daily" not "Administer one tablet orally BID." |
| **Every click costs seconds — seconds cost lives** | A clinician sees 20+ patients per shift. If your UI adds 30 seconds per patient, that's 10+ minutes lost — time that could prevent a medication error. Optimize for speed without sacrificing safety. |

### Cognitive Biases in Healthcare UI

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Automation bias** | Clinicians trust computer-generated alerts without questioning them | Every alert must show the data that triggered it. "Alert: K+ 6.2 mEq/L (normal: 3.5-5.0)" — never just "Alert: High Potassium." |
| **Confirmation bias** | Clinicians see what they expect to see — missing unexpected findings | Display normal AND abnormal values. Don't collapse abnormal results. Use visual hierarchy to draw attention to outliers. |
| **Framing effect** | "90% survival rate" vs "10% mortality rate" — same data, different reactions | Present both absolute and relative risk. Use consistent framing: always show "X out of 100 patients" alongside percentages. |
| **Base rate neglect** | Over-reacting to a positive test result without considering disease prevalence | Show pre-test probability, test sensitivity, and post-test probability. Make Bayesian reasoning visual. |

### What Masters Know

- **The medication list is the most dangerous part of the UI.** Drug name confusion (look-alike/sound-alike), wrong dose, wrong route, wrong frequency — these errors kill patients. Tall Man lettering (e.g., hydrOXYzine vs hydrALAzine) reduces errors by 35%.
- **Normal ranges are age, sex, and context-dependent.** A "normal" lab value that's flagged red because the reference range is wrong for the patient causes unnecessary panic and workup. Reference ranges must be patient-specific.
- **Clinical notes are designed for speed, not readability.** Templates with smart defaults, voice dictation integration, and auto-populated fields save minutes per patient. A well-designed note template is a clinical productivity tool.

## Operating at Different Levels

| Level | User | Scope | What Changes |
|-------|------|-------|-------------|
| **L1 — Apprentice** | New designer building a simple health tracker | Single-user health log: vitals entry, basic trends | Learn healthcare data display: vitals formatting, units, reference ranges. Understand PHI basics. |
| **L2 — Solo** | Startup building a patient app or clinical tool | Patient portal OR single-practice clinical tool | Add PHI indicators, consent flows, 6th-grade reading level content. Basic medication list display. |
| **L3 — Small Team** | Health tech company, multi-provider | Multi-role platform (patient + provider + admin) | Role-based views. Clinical decision support basics. FHIR data integration. Telemedicine features. |
| **L4 — Medium** | Hospital system, health plan, major health app | Enterprise EHR, integrated delivery network | FDA human factors compliance. Clinical workflow optimization. Interoperability with multiple EHR systems. Advanced CDS alerts with alert fatigue management. |
| **L5 — Enterprise** | National health system, global health platform | Multi-country, multi-language, multi-regulation | EU MDR / FDA Class III device compliance. Clinical validation studies. AI/ML decision support with explainability. Real-world evidence integration. |

## Core Workflow

### Phase 1: Clinical Context Discovery (10 min)

1. **Identify users**: clinician (physician, nurse, pharmacist), patient, caregiver, administrator, researcher
2. **Identify clinical context**: inpatient (hospital), outpatient (clinic), home/remote, emergency, surgical
3. **Identify regulatory framework**: HIPAA (US), GDPR (EU), FDA Class I/II/III, EU MDR, NHS DTAC
4. **Identify safety-critical workflows**: medication administration, allergy checking, lab result review, clinical decision support

### Phase 2: Clinical Data Display (15 min)

**Vital signs display patterns:**

| Vital Sign | Format | Normal Range (Adult) | Critical Values |
|-----------|--------|---------------------|-----------------|
| Heart Rate | `72 bpm` | 60-100 | <40 or >130 (adult) |
| Blood Pressure | `120/80 mmHg` | <120/<80 (optimal) | >180/120 (hypertensive crisis) |
| Temperature | `98.6°F (37.0°C)` | 97.8-99.1°F | <95°F or >104°F |
| Respiratory Rate | `16 breaths/min` | 12-20 | <8 or >28 |
| O2 Saturation | `98% on room air` | 95-100% | <90% |
| Pain Score | `3/10` | Individual | — |

**Display rules:**
- Always show unit of measure
- Show reference range in lighter text
- Flag abnormal values: **bold + color** (not color alone)
- Show trend arrow when historical data available: `120 ▲` (increasing from last reading)
- On supplemental O2: show flow rate + device (e.g., "96% on 2L nasal cannula")

**Lab result display:**
```
| Test            | Result    | Flag | Reference Range | Units |
|-----------------|-----------|------|-----------------|-------|
| Sodium          | 142       |      | 135-145         | mEq/L |
| Potassium       | 5.8       | HIGH | 3.5-5.0         | mEq/L |
| Creatinine      | 2.1       | HIGH | 0.6-1.2         | mg/dL |
| Hemoglobin A1c  | 7.2       | HIGH | <5.7            | %     |
```

### Phase 3: Medication Display (10 min)

**Medication card pattern:**
```
┌─────────────────────────────────────────┐
│ 🔒 PHI — PROTECTED HEALTH INFORMATION     │
├─────────────────────────────────────────┤
│ AMOXICILLIN (amoxicillin)                │
│ 500 mg capsule                           │
│                                          │
│ 💊 Take 1 capsule by mouth               │
│    3 (three) times daily                 │
│                                          │
│ ⚠️  Allergies: Penicillin (Rash)          │
│                                          │
│ Prescribed: Dr. Smith | Pharmacy: CVS    │
│ Last filled: Jan 15, 2026               │
│ Remaining: 12 capsules (4 days)          │
│                                          │
│ [Refill] [View Interactions] [Report Issue] │
└─────────────────────────────────────────┘
```

**Medication safety rules:**
- **Tall Man lettering**: Use mixed case for look-alike drug names (hydrOXYzine, hydrALAzine, DOBUTamine, DOPamine)
- **Do Not Use abbreviations**: "U" (write "units"), "IU" (write "international units"), "QD" (write "daily"), "QOD" (write "every other day")
- **Allergy check**: Always visible. Cross-reference current meds with known allergies. Red alert if matching allergen detected.
- **Interaction check**: Color-coded severity. Major (red) = contraindicated, Moderate (amber) = monitor, Minor (blue) = be aware

### Phase 4: Patient-Facing UX (10 min)

**Health literacy design rules:**
1. Target 6th-grade reading level (Flesch-Kincaid). Test every patient-facing string.
2. Define every medical term on first use: "Hypertension (high blood pressure)"
3. Use active voice: "Take this medicine with food" not "This medication should be administered with meals"
4. Chunk information: 3-5 items per screen. Never a wall of text.
5. Use teach-back: "In your own words, tell me how you'll take this medicine" — in the interface

**Patient portal layout:**
```
┌──────────────────────────────────────────┐
│ 👤 Hi, Jane                    🔔 3 New   │
├──────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│ │ 📅       │ │ 💊       │ │ 📊       │      │
│ │ Appoint- │ │ Medica-  │ │ Lab      │      │
│ │ ments    │ │ tions    │ │ Results  │      │
│ │          │ │          │ │          │      │
│ │ Next:    │ │ 2 due    │ │ 1 new    │      │
│ │ Mar 15   │ │ today    │ │ result   │      │
│ └─────────┘ └─────────┘ └─────────┘      │
├──────────────────────────────────────────┤
│ 📋 Upcoming                               │
│ • Mar 15 — Annual Physical, Dr. Smith     │
│ • Mar 22 — Blood work (fasting)           │
├──────────────────────────────────────────┤
│ 💬 Messages from Your Care Team           │
│ • Dr. Smith: "Your lab results look..."   │
│ • Nurse Jones: "Reminder about your..."   │
└──────────────────────────────────────────┘
```

### Phase 5: PHI-Aware UI Design (5 min)

**PHI indicators (always visible when viewing patient data):**
- Lock icon + "PHI — Protected Health Information" banner
- Auto-logout timer: "Session expires in 14:32" with refresh button
- Session timeout: 15 minutes idle (configurable per organization policy)
- "Break glass" emergency access: override with reason capture and audit log
- Watermark: user's name + timestamp on every screen (prevents screenshots)
- Print control: "Printed by Dr. Smith on Jan 15, 2026. Confidential — destroy when no longer needed."

**Consent checkpoints:**
- Data sharing: "Share my records with Dr. Jones? [View what will be shared] [Yes, share] [No]"
- Research: opt-in, never pre-checked. Clear description of what data is used.
- Marketing: must be separate from treatment consent. Cannot be required for care.

## Medical Device UI

For FDA-regulated medical devices (Class II/III) and SaMD (Software as a Medical Device):

### Human Factors Requirements (IEC 62366 / FDA Guidance)
- **Use error analysis**: Document every possible use error and how the UI prevents or mitigates it
- **Formative testing**: Test with 15+ representative users per user group before design freeze
- **Summative testing**: Validate with 15+ users per group. Must demonstrate safe and effective use.
- **Critical tasks**: Identify and test all tasks where failure could cause harm

### Medical Device Display Patterns
- **Alarm systems**: IEC 60601-1-8 compliant. Priority: High (red, flashing, audible), Medium (amber), Low (cyan)
- **Numerical displays**: Large font (≥24pt at viewing distance), high contrast (≥7:1), non-blinking
- **Waveform displays**: ECG, SpO2 plethysmograph, capnography. Fixed sweep speed. Grid overlay.
- **Trend displays**: Vital signs over time. Selectable timescale (1h, 4h, 8h, 24h).

## Cross-Skill Coordination

| Upstream Skill | What We Need | When |
|---------------|-------------|------|
| `ui-ux-designer` | Design system, accessible color palette, component library | Before designing any healthcare UI |
| `accessibility-auditor` | WCAG 2.2 AA compliance baseline, screen-reader testing patterns | Before launch — healthcare is legally required to be accessible |
| `patient-experience-researcher` | Patient journey maps, health literacy data, usability test findings | Before designing patient-facing features |

| Downstream Skill | What We Provide | When |
|-----------------|----------------|------|
| `frontend-developer` | Clinical UI specs, PHI-aware components, medication display patterns | After design — implement in React/Vue/Next.js |
| `mobile-developer` | Mobile clinical workflows, touch-optimized vitals entry, telemedicine mobile UX | After desktop design — adapt for mobile clinical use |
| `hipaa-technical-implementation` | UI-level PHI requirements: auto-logout timing, access indicators, consent flows, audit trail UI events | During implementation — align UI with HIPAA technical controls |

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Medication list without generic names | Flag: "Add generic name alongside brand name. Include Tall Man lettering for look-alike drugs." | Drug name confusion causes 25% of medication errors. |
| Lab results without reference ranges | Flag: "Every lab value needs a reference range. Normal ranges vary by age, sex, and lab method." | A value without context is clinically meaningless and dangerous. |
| Clinical alert without severity tier | Flag: "Implement 3-tier alert severity: Critical (red, requires action), Warning (amber, be aware), Info (blue, for reference)." | Alert fatigue from undifferentiated alerts causes missed critical findings. |
| Patient content above 8th-grade reading level | Flag: "Simplify to 6th-grade level. Define medical terms. Test with readability tool. Offer audio version." | 36% of US adults have basic or below-basic health literacy. |
| No auto-logout on patient data screen | Flag: "Add session timeout (15 min idle) with visible countdown. PHI exposure from unattended screens is a HIPAA violation." | Unattended screens with PHI are the most common HIPAA breach cause. |

## What Good Looks Like

> A clinician logs in, views their patient list with severity-based sorting (critical first), opens a patient chart, and sees the medication list with Tall Man lettering, allergy check, and interaction warnings — all in under 3 seconds. Lab results show patient-specific reference ranges with trend arrows. Medication orders complete in 3 clicks: select medication → confirm dose/route/frequency → sign. The PHI badge and 15-minute session timer are always visible. A patient opens their portal, sees their next appointment and medications due today in plain language at a 6th-grade reading level, and understands exactly what to do. All screens pass WCAG 2.2 AA and have been tested with screen readers.

## Error Recovery

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Clinicians ignore all alerts | Undifferentiated alerts — every alert looks equally urgent | Implement 3-tier severity: Critical (red, action required), Warning (amber, aware), Info (blue, reference). Reduce total alert volume by 60%. |
| Patients don't understand discharge instructions | Content written at medical professional reading level | Rewrite at 6th-grade level. Add teach-back confirmation: "Tell us in your own words what you'll do when you get home." |
| Wrong medication administered | Drug name confusion (look-alike/sound-alike) | Implement Tall Man lettering. Show drug images. Require barcode scanning confirmation. |
| PHI exposed on unattended screen | No auto-logout or too-long timeout | 15-minute idle timeout with visible countdown. Auto-logout at 0. Watermark with user identity. |

## Anti-Hallucination

- [VERIFIED] — Confirmed against FDA guidance, HIPAA requirements, or published clinical standards
- [COMMON-PRACTICE] — Widely used in major EHR systems (Epic, Cerner) or health tech products
- [INFERRED] — Reasonable extrapolation from healthcare UX principles
- [UNKNOWN] — Requires verification against specific clinical context or regulatory jurisdiction
