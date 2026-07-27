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
<!-- QUICK: 30s -->

## Route the Request
<!-- STANDARD: 3min -->

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

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Never display patient data without a visible PHI indicator — users must know they're viewing protected information | `file_contains(output, "patient|PHI|health.record")` AND NOT `file_contains(output, "PHI.badge|lock|protected|confidential|auto.logout")` | REFUSE. "Patient data must be visually marked as PHI. Add lock badge, 'Confidential' label, and auto-logout timer indicator." |
| G2 | Never show medication names or dosages without both brand AND generic names, and never abbreviate units of measure | `file_contains(output, "mg|mcg|mL|IU")` AND NOT `file_contains(output, "milligram|microgram|milliliter|international.unit")` | DETECT. "Medication units must be spelled out: 'milligram' not 'mg', 'microgram' not 'mcg'. Include generic name alongside brand name." |
| G3 | Never use red for non-critical information — in healthcare, red means emergency, error, or critical alert | `file_contains(output, "red")` AND NOT `file_contains(output, "critical|emergency|error|alert|warning")` | STOP. "Red is reserved for critical/emergent information in healthcare. Use amber/orange for warnings, blue/info for neutral." |
| G4 | Never design a clinical workflow that requires more than 3 clicks to complete a common task | `file_contains(output, "clinician|nurse|physician")` AND `file_contains(output, "step.*[4-9]|step.*10")` | REFUSE. "Clinicians work under time pressure. Common tasks (medication administration, vitals entry, note signing) must complete in ≤3 clicks." |
| G5 | Never design patient-facing content above a 6th-grade reading level without offering a simplified version | `file_contains(output, "patient|portal|consumer")` AND NOT `file_contains(output, "simplified|plain.language|easy.read|grade.level")` | DETECT. "Patient content must target 6th-grade reading level. Provide simplified versions for all medical terminology. Test with readability tools." |
| G6 | Never specify UI logging, error tracking, or analytics that could capture PHI in plaintext | `file_contains(spec, "log|analytics|crash.report|error.track|telemetry")` AND NOT `file_contains(spec, "PHI.redact|HIPAA.log|sanitize|de.identify|no.PHI")` | REFUSE. "Healthcare UI must never log PHI to analytics, crash reporters, or error trackers. Specify: all patient data redacted from logs, crash reports stripped of screen contents, analytics use only de-identified tokens. Reference HIPAA 164.312(c)(1) — audit controls must not themselves become PHI leaks. If the crash reporter captures screenshots, it must be disabled for patient-data screens." |
| G7 | Never specify animations that could trigger seizures, obscure clinical data, or interfere with assistive technology — every animation must have a zero-motion fallback | `file_contains(spec, "animate|transition|motion|pulse|flash|spring")` AND NOT `file_contains(spec, "prefers-reduced-motion|seizure.safe|accessibility|no.motion|0ms")` | REFUSE. "Healthcare UI animations must be safe and functional: (1) no flashing >3 times/second — seizure threshold per WCAG 2.3.1, (2) critical alerts: gentle pulse at 1Hz with static indicator fallback, (3) every animation must respect `prefers-reduced-motion: reduce` → instant, (4) animations must never be the sole channel for critical information — always pair with static text/icon, (5) medication confirmation: green checkmark (static) + haptic, not a distracting celebration animation." |

## The Expert's Mindset
<!-- STANDARD: 3min -->

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

**Animation principles for healthcare UI:**

| Context | Animation | Duration | Reduced Motion | Safety Rule |
|---|---|---|---|---|
| Critical alert (vital sign out of range) | Gentle red pulse (1Hz) + static badge | Continuous until acknowledged | Static red badge + "Critical" text | ≤2 pulses/second — never exceed 3/sec (seizure threshold). Alert must remain visible when animation stops |
| Warning alert | Amber highlight fade-in | 200ms | Static amber badge | Single animation. Do not loop warnings — loop = critical |
| Info notification | Blue fade-in | 150ms | Instant replace | Subtle. Information already visible in the data — don't distract |
| Medication administered confirmation | Green checkmark appear (no animation beyond CSS transition) | 100ms | Static checkmark | Pair with haptic. NO celebration/pop/confetti — this is serious, not gamified |
| Lab result loaded | Row highlight fade-in (top to bottom) | 100ms per row (staggered) | All rows appear instantly | Data before decoration. Render values first, animate highlights after |
| Auto-logout countdown (PHI screen) | Countdown number + progress bar | Idle timer (15 min) | Static timer text | The animation IS the information. Must be visible peripherally. Pulse in last 60 seconds |
| Patient list reorder (severity sort) | FLIP animation — rows move to new position | 300ms | Instant reorder | FLIP (First, Last, Invert, Play) preserves context. Without animation, reorder looks like data changed |

**Hard rules for clinical animations:**
- **No animation on medication names, dosages, or allergy flags.** These must render instantly. Any delay = risk of misread.
- **No animation that loops continuously.** Looping animations trigger alert fatigue and increase cognitive load.
- **No parallax, scroll-triggered reveals, or "delight" animations in clinical views.** These belong in patient-facing wellness apps, not clinical tools.
- **Haptic pairing**: critical alerts = heavy haptic, warnings = medium, confirmations = light. Match platform haptic APIs (UIKit `UIImpactFeedbackGenerator`, Android `VibrationEffect`).

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | User | Scope | What Changes |
|-------|------|-------|-------------|
| **L1 — Apprentice** | New designer building a simple health tracker | Single-user health log: vitals entry, basic trends | Learn healthcare data display: vitals formatting, units, reference ranges. Understand PHI basics. |
| **L2 — Solo** | Startup building a patient app or clinical tool | Patient portal OR single-practice clinical tool | Add PHI indicators, consent flows, 6th-grade reading level content. Basic medication list display. |
| **L3 — Small Team** | Health tech company, multi-provider | Multi-role platform (patient + provider + admin) | Role-based views. Clinical decision support basics. FHIR data integration. Telemedicine features. |
| **L4 — Medium** | Hospital system, health plan, major health app | Enterprise EHR, integrated delivery network | FDA human factors compliance. Clinical workflow optimization. Interoperability with multiple EHR systems. Advanced CDS alerts with alert fatigue management. |
| **L5 — Enterprise** | National health system, global health platform | Multi-country, multi-language, multi-regulation | EU MDR / FDA Class III device compliance. Clinical validation studies. AI/ML decision support with explainability. Real-world evidence integration. |

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: Role-Based View Selection

        ┌── INPUT: Who is the primary user?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Clinician]       [Patient]          [Administrator]
Physician,        Self-service,      Scheduling,
nurse,            results,           billing,
pharmacist        messaging          reporting
   │                 │                  │
   ▼                 ▼                  ▼
High-density      Plain language     Tabular data,
clinical data,    (6th-grade         search-heavy,
CDS alerts,       reading level),    batch operations,
quick-entry       large touch        role-permission
workflows         targets            gating

### Decision Tree 2: Clinical Alert Severity

        ┌── INPUT: What is the clinical risk?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Critical/STAT]   [Warning]          [Informational]
Life-threatening  Action needed      Routine
allergy, drug     soon: abnormal     notification,
interaction,      lab, overdue       appointment
critical lab      medication         reminder
   │                 │                  │
   ▼                 ▼                  ▼
Red, modal,       Amber, banner,     Blue/gray,
requires          persistent until   dismissible,
immediate         acknowledged,      non-blocking,
acknowledgment    blocks related     logged to
→ audit trail     actions            audit trail

### Decision Tree 3: PHI Visibility & Consent

        ┌── INPUT: What PHI is being displayed?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Direct View]     [Glanceable]       [Shared Screen]
Patient's own     Lock screen        Waiting room,
record, full      notifications,     hallway display,
detail            watch face         teaching
   │                 │                  │
   ▼                 ▼                  ▼
Show full data,   Mask PHI until     No PHI visible,
auto-logout       authentication,    generic labels
after inactivity, show "New lab      only, room
audit every       result" without    number/initials
access            values             anonymized

## Core Workflow
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---------|--------|-----|
| Medication list without generic names | Flag: "Add generic name alongside brand name. Include Tall Man lettering for look-alike drugs." | Drug name confusion causes 25% of medication errors. |
| Lab results without reference ranges | Flag: "Every lab value needs a reference range. Normal ranges vary by age, sex, and lab method." | A value without context is clinically meaningless and dangerous. |
| Clinical alert without severity tier | Flag: "Implement 3-tier alert severity: Critical (red, requires action), Warning (amber, be aware), Info (blue, for reference)." | Alert fatigue from undifferentiated alerts causes missed critical findings. |
| Patient content above 8th-grade reading level | Flag: "Simplify to 6th-grade level. Define medical terms. Test with readability tool. Offer audio version." | 36% of US adults have basic or below-basic health literacy. |
| No auto-logout on patient data screen | Flag: "Add session timeout (15 min idle) with visible countdown. PHI exposure from unattended screens is a HIPAA violation." | Unattended screens with PHI are the most common HIPAA breach cause. |

## What Good Looks Like
<!-- STANDARD: 3min -->

> A clinician logs in, views their patient list with severity-based sorting (critical first), opens a patient chart, and sees the medication list with Tall Man lettering, allergy check, and interaction warnings — all in under 3 seconds. Lab results show patient-specific reference ranges with trend arrows. Medication orders complete in 3 clicks: select medication → confirm dose/route/frequency → sign. The PHI badge and 15-minute session timer are always visible. A patient opens their portal, sees their next appointment and medications due today in plain language at a 6th-grade reading level, and understands exactly what to do. All screens pass WCAG 2.2 AA and have been tested with screen readers.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Clinicians ignore all alerts | Undifferentiated alerts — every alert looks equally urgent | Implement 3-tier severity: Critical (red, action required), Warning (amber, aware), Info (blue, reference). Reduce total alert volume by 60%. |
| Patients don't understand discharge instructions | Content written at medical professional reading level | Rewrite at 6th-grade level. Add teach-back confirmation: "Tell us in your own words what you'll do when you get home." |
| Wrong medication administered | Drug name confusion (look-alike/sound-alike) | Implement Tall Man lettering. Show drug images. Require barcode scanning confirmation. |
| PHI exposed on unattended screen | No auto-logout or too-long timeout | 15-minute idle timeout with visible countdown. Auto-logout at 0. Watermark with user identity. |

## Best Practices

1. **Do design clinical alerts with a 3-tier severity system (Critical/Warning/Info) and reduce total alert volume by ≥ 60%** — Alert fatigue is the #1 patient safety risk in clinical software. When all alerts are red and critical, clinicians dismiss them without reading — a 2017 study found clinicians override 49-96% of medication alerts. Tier alerts: Critical (red, blocks workflow — "Allergy: Penicillin. Do NOT administer"), Warning (amber, acknowledge required — "Duplicate therapy: patient already on lisinopril"), Info (blue, dismissible — "Lab result available"). Audit alert volume before/after tiering; must drop ≥ 60%.
2. **Prefer Tall Man lettering and fully spelled-out medication names over abbreviated forms** — "hydrOXYzine" vs "hydrALAzine" — one letter distinguishes an antihistamine from a vasodilator. Abbreviated units cause dosing errors: "5.0 mg" misread as "50 mg" when the decimal is missed. ISMP and FDA mandate Tall Man lettering and a Do Not Use abbreviation list. A medication display error caused by abbreviated units costs $100,000-$500,000 in liability per incident and can be fatal.
3. **Always display PHI indicators (lock badge + "Confidential" label + auto-logout countdown) on every screen with patient data** — Users must never be uncertain whether they're viewing protected health information. The lock badge provides visual assurance; the auto-logout timer (≤ 15 minutes idle, configurable) enforces HIPAA session management (45 CFR §164.312(a)(2)(iii)). A missing PHI indicator that leads to a screen-surfing breach costs $50,000-$1.5M in HIPAA fines per incident.
4. **Never use red for non-critical information in a clinical context** — In healthcare, red means emergency, life-threatening, or stop. A red "New Feature!" badge or a red accent color on a dashboard desensitizes clinicians to real red alerts. Reserve red exclusively for: abnormal critical lab values, contraindicated medication interactions, emergency alerts, and error states that block workflow. A red decorative element that causes a clinician to miss a critical allergy alert has a non-monetary cost measured in patient harm.
5. **Measure click count for the top 5 clinical workflows** — How many clicks/interactions to: administer medication, enter vitals, sign a note, review a lab result, and order a test? Target: ≤ 3 clicks per task from the primary workflow screen. Clinicians see 20+ patients per shift; every 30 seconds of UI friction per patient costs 10+ minutes per shift — time that could prevent a medication error. Instrument with RUM analytics segmented by clinician role and shift.

## Production Checklist

Before deploying or delivering work from this skill, verify:

| # | Check | Verify |
|---|-------|--------|
| ☐ | Every screen with PHI displays a visible lock badge, "Confidential — PHI" label, and auto-logout countdown timer (≤ 15 minutes idle) | Verify PHI badge renders on all screens with patient data; auto-logout timer counts down and triggers session termination at expiry |
| ☐ | All medication names display both brand and generic names with fully spelled-out units (milligram, not mg; microgram, not mcg) | Spot-check every medication reference in the UI; no abbreviated units; Tall Man lettering applied to look-alike/sound-alike drug names per ISMP list |
| ☐ | Red color reserved exclusively for critical/emergency/error states; amber for warnings; blue for informational | Run a color audit script: `grep -rn 'red\|#FF0000\|Color.red' --include="*.swift" --include="*.tsx"` — verify each red instance maps to a critical/error/emergency context |
| ☐ | Common clinical tasks (medication admin, vitals entry, note signing) complete in ≤ 3 clicks from the primary workflow screen | Time and count clicks for each top-5 workflow with a clinician tester; any task > 3 clicks must be restructured |
| ☐ | Clinical alerts use 3-tier severity (Critical red, Warning amber, Info blue); total alert volume reduced ≥ 60% from unfiltered state | Audit alert count before/after tiering implementation; total alert count must decrease by at least 60% |
| ☐ | Patient-facing content scored at 6th-grade reading level (Flesch-Kincaid) with teach-back confirmation prompts for discharge and medication instructions | Run readability tool on every patient-facing string; any score > grade 8 must be rewritten; teach-back prompt renders after key instructions |
| ☐ | All UI logging, crash reporting, and analytics redact PHI at the pipeline — no patient data, account numbers, or identifiers in any log at any level | Inspect DEBUG-level log output: no patient names, MRNs, dates of birth, SSNs, or full account numbers; crash reporter screenshots disabled for patient-data screens |
| ☐ | Rollback plan is documented and tested | Verify: EHR downtime procedure documented; rollback maintains data integrity (no lost entries); auto-logout timer and PHI indicators persist through version rollback; FDA human factors validation repeated if rollback changes clinical workflows |

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|---|---|
| ☐ | Complete when every screen displaying PHI has a visible lock badge, "Confidential" label, and auto-logout timer countdown indicator | Verify PHI badge renders on all screens with patient data; auto-logout timer is visible and counts down from ≤ 15 minutes of inactivity |
| ☐ | Complete when all medication names show both brand and generic names, with units of measure fully spelled out (milligram, not mg; microgram, not mcg) | Verify every medication reference in the UI pairs brand + generic names; no abbreviated units appear anywhere in medication display |
| ☐ | Complete when red color is reserved exclusively for critical/emergency/error states, with amber for warnings and blue for informational | Verify via color audit that no red appears outside critical alert contexts; non-critical elements using red trigger Ground Rule G3 violation |
| ☐ | Complete when common clinical tasks (medication administration, vitals entry, note signing) complete in ≤ 3 clicks from the primary workflow screen | Verify click count for each common task; if > 3 clicks, restructure workflow to reduce steps or add shortcuts |
| ☐ | Complete when clinical alerts use a 3-tier severity system: Critical (red, action required), Warning (amber, be aware), Info (blue, reference) with total alert volume reduced by ≥ 60% from unfiltered state | Verify alert tiering system is in place; audit alert volume before/after tiering — must drop by at least 60% |
| ☐ | Complete when patient-facing content is written at a 6th-grade reading level with teach-back confirmation prompts for discharge and medication instructions | Verify via readability tool (Flesch-Kincaid) that patient content scores at grade 6 or below; teach-back prompt renders after key instructions |
| ☐ | Complete when auto-logout triggers after ≤ 15 minutes of idle time with a visible countdown during the final 60 seconds and screen watermark showing logged-in user identity | Verify idle timeout fires at 15 minutes; countdown appears at 14:00; watermark shows username/role persistently |
| ☐ | Complete when look-alike/sound-alike drug names use Tall Man lettering and barcode scanning confirmation is required for medication administration | Verify Tall Man formatting on high-risk drug name pairs (e.g., hydrOXYzine vs hydrALAzine); barcode scan step cannot be bypassed |
| ☐ | Complete when all clinical data displays (lab results, vitals trends, medication schedules) include reference ranges, measurement units, and collection timestamps | Verify every lab value shows normal range, unit, and "Collected: [timestamp]"; abnormal values are visually distinct from normal |
| ☐ | Complete when accessibility covers: screen reader labels on all interactive elements, keyboard navigation for every workflow, and minimum 4.5:1 contrast on all text | Verify via automated accessibility scan (axe-core, Accessibility Inspector) with zero critical violations; manual screen reader pass completes all workflows |

## When to Use
<!-- STANDARD: 3min -->

| Condition | Use This Skill | Use Instead |
|-----------|---------------|-------------|
| Designing EHR interface (lab results, medication administration, vitals) | ✅ Clinical data display, 3-click workflows, severity-tiered alerts | — |
| Building patient portal (appointments, prescriptions, secure messaging) | ✅ 6th-grade reading level, teach-back confirmation, PHI indicators | — |
| Designing telemedicine platform (virtual visits, waiting room) | ✅ HIPAA-compliant video UX, pre-visit intake, post-visit summary | — |
| Building medical device UI (patient monitor, infusion pump, diagnostic) | ✅ FDA human factors (IEC 62366), alarm tiering, barcode confirmation | — |
| HIPAA compliance implementation (backend) | ❌ | `hipaa-technical-implementation` |
| FDA 510(k) regulatory submission | ❌ | `health-regulatory-submission` |
| General healthcare UX research | ❌ | `patient-experience-researcher` |
| Pharmacy system UI | ✅ Medication display with Tall Man lettering, drug interaction alerts | — |
| Health tracking app (symptoms, vitals, activity) | ✅ Consumer health UX, data visualization for non-clinicians | — |
| Clinical decision support (alerts, guidelines, risk scores) | ✅ Alert tiering, clinical workflow integration, cognitive load management | — |

## Deliberate Practice
<!-- STANDARD: 3min -->

1. **Audit a real EHR screen.** Screenshot a patient chart from Epic or Cerner (or a publicly available demo). Count clicks to order a medication. Check: is the PHI indicator visible? Are lab results shown with reference ranges and timestamps? Is red used only for critical alerts? Identify 5 violations of best practices.
2. **Redesign medication administration for safety.** Take a medication order screen. Add: brand + generic name, Tall Man lettering for look-alike drugs, barcode scan confirmation step, allergy cross-check visual indicator, and drug-drug interaction warning. Test: can a nurse complete administration in 3 clicks without missing a safety check?
3. **Rewrite discharge instructions for health literacy.** Take a standard discharge summary (typically 12th-grade reading level). Rewrite at 6th-grade level. Add teach-back confirmation: "In your own words, what will you do when you get home?" Add visual icons for: take medication, schedule follow-up, watch for symptoms, call if worse.
4. **Design a clinical alert tiering system.** Start with an undifferentiated alert feed (50 alerts/day). Classify each: Critical (red, action required), Warning (amber, be aware), Info (blue, reference). Reduce total alerts by 60%. Design the visual hierarchy so Critical alerts are unmissable but Info alerts are non-interruptive.
5. **Build an accessible patient portal flow.** Design a prescription refill flow for a 65-year-old patient with low vision and limited tech literacy. Test: screen reader navigation, keyboard-only input, 200% text zoom, and touch targets ≥44pt. Measure time-to-complete — target under 3 minutes.

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Medication names without Tall Man lettering — look-alike/sound-alike drugs cause administration errors | $100K-$5M per medication error incident; 25% of medication errors from name confusion; preventable death liability | Implement Tall Man lettering (hydrOXYzine vs hydrALAzine). Show drug images. Require barcode scanning confirmation before administration |
| Clinical alerts without severity tiering — clinicians develop alert fatigue and ignore critical warnings | $500K-$10M in missed critical findings leading to adverse events; clinical burnout from constant low-value interruptions | 3-tier severity: Critical (red, action required), Warning (amber, aware), Info (blue, reference). Reduce total alert volume by ≥60% |
| Patient content written above 6th-grade reading level — 36% of US adults have basic or below-basic health literacy | $200K-$2M in readmission penalties (CMS Hospital Readmissions Reduction Program); medical errors from misunderstood instructions | Rewrite at 6th-grade Flesch-Kincaid level. Add teach-back confirmation. Offer audio version. Define all medical terms inline |
| No auto-logout on PHI screens — unattended screen exposes protected health information | $50K-$250K per HIPAA breach incident (tiered by record count); $1.5M average OCR settlement for systemic violations | 15-minute idle timeout with visible countdown. Auto-logout at 0. Screen watermark showing logged-in user identity. Audit logging on every session end |
| Red used for non-critical information — in clinical contexts, red means emergency/error | $30K-$150K in UX redesign; potential clinical error from misinterpreting non-critical red element as emergency alert | Reserve red exclusively for Critical/Emergency/Error. Use amber for warnings, blue for informational. Audit every red pixel in the UI |
| Clinical workflow requiring >3 clicks for common tasks — wastes clinician time under pressure | $100K-$500K/year in lost clinician productivity (15 clinicians × 5 min/day × $150/hr); clinician burnout and dissatisfaction | Common tasks (medication admin, vitals entry, note signing) must complete in ≤3 clicks. Add shortcuts and favorites. Measure time-motion |
| Lab results without reference ranges and timestamps — clinically meaningless and potentially misleading | $50K-$500K in diagnostic errors from out-of-context lab values; normal ranges vary by age, sex, lab method, and pregnancy status | Every lab value shows: reference range, units, collection timestamp, and trend arrow. Abnormal values visually distinct. "Collected: [datetime]" adjacent to value |
| Weight-based medication dosing without weight validation — pediatric overdose risk | $500K-$10M in pediatric medication error liability; children dosed by weight — a 10× dosing error from kg/lb confusion is fatal | Require weight entry with unit validation (kg only). Automatic dose calculation. Hard stops on doses exceeding mg/kg safety limits. Pharmacist verification for high-alert medications |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Decision | Status | Timestamp |
|----------|--------|-----------|
| (none yet) | — | — |

## References
<!-- STANDARD: 3min -->

- [FDA Human Factors Guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents) — Applying Human Factors and Usability Engineering to Medical Devices
- [IEC 62366-1:2015](https://www.iso.org/standard/63179.html) — Medical devices usability engineering standard
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html) — Technical safeguards for ePHI
- [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/) — Accessibility standard for healthcare applications
- `references/clinical-interface-patterns.md` — EHR design, lab result display, medication administration
- `references/patient-portal-patterns.md` — Health-literate content, appointment booking, prescription refill
- `references/telemedicine-patterns.md` — Virtual visit UX, waiting room design, post-visit summary
- `references/medical-device-ui.md` — FDA human factors, alarm design, vital sign monitoring
- `references/clinical-alert-design.md` — Severity tiering, alert fatigue reduction, interruptive vs non-interruptive
- `references/healthcare-accessibility.md` — Screen reader patterns for clinical data, colorblind-safe medical indicators

## Anti-Hallucination
<!-- STANDARD: 3min -->

- Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
- Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
- Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
- [VERIFIED] — Confirmed against FDA guidance, HIPAA requirements, or published clinical standards
- [COMMON-PRACTICE] — Widely used in major EHR systems (Epic, Cerner) or health tech products
- [INFERRED] — Reasonable extrapolation from healthcare UX principles
- [UNKNOWN] — Requires verification against specific clinical context or regulatory jurisdiction
