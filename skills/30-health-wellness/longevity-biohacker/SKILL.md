---
name: longevity-biohacker
description: "Use when you want an evidence-oriented longevity strategy. Handles biomarker tracking, epigenetic clock interpretation, exercise stacks (zone 2, strength), fasting strategies, and supplement evidence review. Do NOT use for geriatric medicine or disease treatment."
license: MIT
author: Sandeep Kumar Penchala
type: health-wellness
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [longevity, biomarkers, epigenetics, fasting, senolytics, NAD, VO2max, HRV]
token_budget: 4000
chain:
  consumes_from: [fitness-programmer, nutrition-strategist, sleep-optimizer]
  feeds_into: []
  alternatives: [geriatrician, clinical-gerontology]
---

# Longevity Biohacker
Portability: research + clinical-lab-friendly (CSV outputs for labs)

<!-- QUICK: 30s -->
One-liner: Produce an individualized longevity monitoring & intervention plan: labs cadence, exercise and fasting prescriptions, supplement stack with evidence tiers.

## RESEARCH_PREREQUISITE (hard gate)
| Code | Requirement |
| --- | --- |
| RP1 | Clear user goals & constraints (age, sex, medical conditions, medications) |
| RP2 | Training history or activity log (last 12 weeks) |
| RP3 | Current body metrics (weight, height, body fat if available) |
| RP4 | Equipment & time availability (list of equipment, hours/wk) |
| RP5 | Sleep and recovery baseline (7-day average) |
| RP6 | Nutrition baseline or dietary restrictions |
| RP7 | Movement screen / injury history |
| RP8 | Consent to non-clinical longevity interventions |

### Iterative Research Loop
| Loop | Objective | Output |
| --- | --- | --- |
| Loop 0 | Risk stratification & priorities | Top 3 actionable biomarker areas (lipids, glucose, inflammation) |
| Loop 1 | Baseline biomarker panel | List of labs and ideal cadence (quarterly/annually) |
| Loop 2 | Intervention mapping | Exercise, nutrition, sleep, supplement stack prioritized by impact |
| Loop 3 | Monitoring & adjustment | Quarterly review plan and triggers for clinician referral |

## Quickstart (30s)
1. Ask: age, family history, current meds, major health goals (extend healthspan, improve biomarkers).
2. Recommend baseline labs: CMP, fasting glucose, HbA1c, lipid panel, hs-CRP, vitamin D, TSH, fasting insulin, CBC, ferritin.
3. Output: 3-point intervention: Zone 2 cardio 2–3x/wk, strength 2x/wk, fasting 16:8 or 5:2 trial; consider creatine, omega-3, vitamin D.

<!-- STANDARD: 3min -->
## Ground rules
- Mechanical triggers: new cardiac symptoms, unexplained weight loss, or abnormal lab flags -> urgent clinical referral.
- Supplements: prefer agents with human RCT data; avoid experimental drug regimens without clinician oversight (rapamycin, metformin off-label).
- Testing cadence: labs quarterly for first year when optimizing, then 6–12 months stable.

## Decision Tree
Start
├─ Primary concern?
│  ├─ High cardiometabolic risk -> Prioritize glucose/lipid interventions, weight management, and statin/medication review with PCP
│  ├─ Frailty/low muscle mass (older adults) -> Prioritize resistance training, protein intake, DEXA and physical therapy handoff
│  ├─ Low cardiorespiratory fitness -> Zone 2 base and VO2max testing + progressive intervals
│  ├─ Interested in advanced interventions (epigenetics/senolytics) -> Clinical consultation, informed consent, and research-grade monitoring
│  └─ Maintenance-focused -> Annual labs + lifestyle reinforcement and monitoring cadence
├─ Age considerations?
│  ├─ <40 -> Focus on preventive lifestyle, metabolic screening every 1–3 years
│  └─ 40+ -> Consider more frequent labs (annual or semi-annual) and functional testing
├─ Medication interactions or complex comorbidity?
│  ├─ Yes -> Coordinate with PCP / specialist prior to supplements or drugs
│  └─ No -> proceed with tiered interventions and regular monitoring
└─ Goal timescale?
   ├─ Short-term ( months ) -> target VO2/strength and metabolic markers
   └─ Long-term (years) -> longitudinal biomarker program and lifestyle systems

Decision routing note: risk stratify first; high-risk or complex patients always require clinician coordination before any pharmacologic or experimental intervention.

<!-- STANDARD: 3min -->
## Core Workflow
1) Intake & risk stratification (Loop 0) <!-- STANDARD: 3min -->
- Collect age, family history, medication list, prior labs, and primary goal.

2) Baseline biomarker set (Loop 1) <!-- STANDARD: 3min -->
- Essential panel: fasting glucose, fasting insulin, HbA1c, lipid panel (LDL-C, HDL-C, TG), hs-CRP, CMP, TSH, vitamin D25-OH, CBC, ferritin, eGFR.
- Optional advanced: DEXA, VO2max test, LP(a), ApoB, telomere/epigenetic clocks, gut microbiome sequencing.

3) Intervention mapping (Loop 2) <!-- DEEP: 10+min -->
- Exercise: Zone 2 (60–70% HRmax) 2–4x/week 30–60 min for mitochondrial and endurance gains; strength: 2–3x/week heavy compound focus with progressive overload to preserve sarcopenia risk. War story: a 58-year-old restarted zone 2 3x/week and added twice-weekly strength; VO2 improved by 8% and lean mass increased 1.5 kg over 12 weeks.
- Nutrition: Mediterranean-style pattern with target protein 1.2–1.8 g/kg; emphasize legumes, oily fish, olive oil, and diverse plant fiber. Intermittent fasting options (16:8 or 5:2) can be trialed but monitor lipids, glucose, and lean mass during caloric restriction.
- Sleep: 7–9 hours; integrate sleep-optimizer recommendations (fixed wake time, light exposure, temperature control) and monitor via sleep diary/actigraphy.
- Supplements (tiered): Tier A (strong evidence): omega-3 EPA/DHA 1–3 g/day, vitamin D3 if low, creatine 3–5 g/day for muscle and cognition benefits; Tier B: NAD+ precursors (NR/NMN) with mixed human evidence (250–1000 mg/day), CoQ10 for those on statins; Tier C: senolytics (fisetin, dasatinib+quercetin) reserved for clinical trials or physician-guided protocols.
- Safety & interactions: Always check renal/hepatic function and drug interactions before any chronic supplement use. Document baseline CMP and follow-up labs at 8–12 weeks for new agents.

4) Advanced interventions & safety <!-- DEEP: 10+min -->
- Rapamycin / mTOR modulators: evidence from animal models and small human studies suggests potential longevity signal, but dosing, scheduling, and safety profiles are not settled—use only under clinical supervision or trial.
- Metformin: epidemiologic signals in diabetics; off-label geroprotection remains controversial—coordinate with PCP and monitor B12, renal function, and GI tolerance.
- NAD+ precursors (NR/NMN): human trials show increases in NAD+ metabolites; long-term benefits unclear. Dosing range 250–1000 mg/day in studies; monitor for GI side effects.
- Senolytic agents: agents like fisetin or D+Q are experimental—document risks, contraindications (immunosuppression), and require clinician oversight.
- Failure narrative: an overly eager self-experimenter combined high-dose NR with an unregulated supplement blend and developed GI distress and transient LFT elevations—stopping supplements and clinician review resolved the issue. Lesson: test incrementally and verify baseline labs.

5) Monitoring & iteration (Loop 3) <!-- DEEP: 10+min -->
- Lab cadence: initial baseline, re-test key labs (CMP, fasting glucose, lipids, hs-CRP, vitamin D) at 8–12 weeks after a new supplement or diet change, then quarterly during optimization, then 6–12 months when stable.
- Functional tests: VO2max or submax step test annually; DEXA for body composition yearly or every 18 months depending on cost and goals.
- Epigenetic clocks & biomarkers: use Horvath/Hannum/PhenoAge selectively and interpret directionally; expect large measurement noise—compare baseline vs 12 months and treat changes cautiously.
- Data-driven iteration: maintain a longitudinal dashboard of labs, activity (zone 2 minutes/week), strength metrics, sleep, and adherence. Use triggers: change in LDL>20% or HbA1c rise >0.3% to prompt clinical review.
- Example trigger: if creatinine or AST/ALT rise >1.5x baseline after supplement initiation, stop the agent and consult clinician.

## Error Decoder
| Error Message / Pitfall | Root Cause | Fix | Lesson |
| --- | --- | --- | --- |
| Over-optimization chasing biomarkers | Small effect sizes and measurement noise | Prioritize lifestyle changes; avoid chasing single-marker shifts | Focus on high-impact behaviors first (exercise, diet, sleep) |
| Adverse events from off-label drugs (rapamycin/metformin) | Lack of clinical oversight and inadequate baseline testing | Cease drug, urgent clinician review, document and report | Always run drugs through medical supervision; track labs closely |
| Conflicting lab signals (e.g., improved lipids but worse inflammation) | Measurement timing, acute illness, or inconsistent lab conditions | Repeat labs under standardized conditions; review clinical context | Labs are data points—interpret alongside clinical picture |
| Misinterpreting epigenetic clocks | Biological noise and algorithm differences | Use clocks directionally; require 12-month follow-up to assess trends | Epigenetic clocks are experimental; do not drive radical interventions alone |
| Supplement interactions causing organ stress | Polypharmacy and unmonitored supplement stacking | Stop suspect supplements, run CMP, coordinate with clinician | Simpler is safer—document every agent and check labs
| Insufficient follow-up leading to missed harms | Lack of monitoring cadence after starting agents | Establish scheduled re-tests (8–12 weeks) and symptom check-ins | Monitoring is part of the intervention—schedule it explicitly
| Behavioral drift (drop in adherence after 3 months) | Complexity, cost, or lack of reinforcement | Simplify program, focus on high-impact behaviors, use habit-engineer to rebuild routines | Sustainable interventions win over time |

## Best practices
1. Prioritize exercise, nutrition, sleep, and social connection before pharmacologic or supplement interventions—these deliver the largest effect sizes for healthspan markers.
2. Adopt a lab-first approach: obtain baseline CMP, fasting glucose/insulin, lipids, hs-CRP, vitamin D, and renal function before starting supplements.
3. Use functional endpoints: VO2max (or submax proxy) and DEXA for body composition as annual objective measures.
4. Tier interventions by evidence: lifestyle > Tier A supplements (omega-3, vitamin D, creatine) > Tier B (NAD+ precursors) > Tier C (senolytics/rapamycin) requiring clinical oversight.
5. Re-test labs at 8–12 weeks after new interventions, then quarterly during optimization, and every 6–12 months when stable.
6. Use a longitudinal dashboard for biomarkers, activity, sleep, and strength metrics; set automated flags for clinically relevant deltas (e.g., HbA1c +0.3%).
7. Start one intervention at a time to isolate effects; use n-of-1 design principles for self-experimentation.
8. Beware of polypharmacy and supplement stacking; perform interaction checks and coordinate with the prescribing clinician.
9. Document informed consent for any off-label or experimental agent and maintain clinical oversight notes.
10. Favor cost-effective tests (lipid panel, HbA1c, CMP) before expensive assays (epigenetic clocks) unless used in a formal research context.

## Production Checklist
- [ ] Baseline labs recommended and ordered (CMP, fasting glucose, HbA1c, lipids, hs-CRP, 25-OH D)
- [ ] Exercise prescription issued (zone 2 minutes/week target + strength plan)
- [ ] Supplement stack with evidence tiers and safety notes
- [ ] Monitoring cadence scheduled (8–12 week re-checks)
- [ ] Functional tests scheduled (VO2 proxy/DEXA as applicable)
- [ ] Medication & supplement reconciliation completed with PCP
- [ ] Consent and documentation for experimental agents (if applicable)
- [ ] Data dashboard template created for longitudinal tracking
- [ ] Follow-up appointment scheduled at 12 weeks
- [ ] Emergency/abnormal lab protocol established (who to contact)
- [ ] Nutrition handoff completed for macro & micronutrient alignment
- [ ] Sleep optimization referral made if recovery limiting
- [ ] Cost/benefit discussion documented for expensive testing (epigenetic clocks)

## Verification
- Expect improvements in cardiorespiratory fitness (VO2max +3–10% in 12 weeks with targeted training).
- Expect lipid and glycemic improvements within 8–12 weeks with diet/exercise adherence.
- Verify no adverse effects from supplements via CMP and symptom review.

## Cross-Skill Coordination
| Skill | When to hand off | Payload |
| --- | --- | --- |
| fitness-programmer | When exercise intensity increases | Training plan, zone 2 minutes, strength metrics and periodization needs |
| nutrition-strategist | For calorie/macro adjustments and supplement timing | Macro targets, micronutrient mitigation, refeed scheduling |
| sleep-optimizer | For recovery optimization | Sleep schedules, HRV trends, and recovery windows |
| habit-engineer | For adherence to long-term protocols | Habit stack for exercise, supplement routines, and lab adherence |
| primary-care/geriatrician | For clinical risk or drug planning | Full lab list, medication reconciliation, and intervention summary |

## What Good Looks Like
- Measurable improvements in functional biomarkers (VO2max, strength), stable labs, and preserved quality of life.
- Transparent documentation of any experimental interventions and clinician oversight.

## References
- López-Otín C., Blasco M.A., Partridge L., Serrano M., Kroemer G., "The Hallmarks of Aging," Cell, 2013.
- Mannick JB., et al., "mTOR inhibition improves immune function in the elderly," Science Translational Medicine, 2018 (rapalog studies overview).
- Horvath S., "DNA methylation age of human tissues and cell types," Genome Biology, 2013 (epigenetic clock foundational paper).
- Levine M., "PhenoAge/Epigenetic clocks" research and validation publications (2018–2020).
- International guidelines on omega-3 and vitamin D supplementation (various consensus documents, 2016–2021).
- ACSM Guidelines for Exercise Testing and Prescription (editions post-2014) for older adults.
- Reviews on NAD+ precursors (NR/NMN) and human trial summaries, Journal reviews 2019–2022.

## Scale Depth
- Solo: Individual plan with basic labs and lifestyle interventions. Tools: lab requisition templates, simple dashboard (CSV), sample exercise & sleep plans. Metrics: baseline labs, weekly zone-2 minutes, monthly strength log. Trigger: abnormal lab value or failure to hit basic targets after 12 weeks.
- Small: Integrated coaching with lab ordering and quarterly reviews. Tools: telehealth follow-up, structured re-testing, habit-engineer integration. Metrics: adherence %, VO2 proxy change, biomarker trends. Trigger: adverse lab changes or clinical flags.
- Medium: Multi-disciplinary clinic integration for advanced testing (DEXA, epigenetic clocks, cardiopulmonary testing). Tools: EHR integration, dietitian, physical therapy, cardiology consults. Metrics: longitudinal body composition, epigenetic clock trends (directional), functional tests. Trigger: any major clinical abnormality or planned experimental intervention.
- Enterprise: Longitudinal cohort management with research-grade assays and integrated care pathways. Tools: cohort dashboards, research protocols, compliance management. Metrics: population-level biomarker improvements, retention, adverse event rates. Trigger: cohort-level safety signals or regulatory review needs.

## Anti-Hallucination
- [VERIFIED] Zone 2 training improves mitochondrial markers and endurance; supported by exercise physiology literature.
- [COMMON-PRACTICE] Omega-3 and vitamin D are commonly recommended based on trials.
- [INFERRED] Epigenetic clock changes over short periods are noisy; interpret cautiously.
- [UNKNOWN] Long-term impacts of some senolytics and NAD+ boosters in humans remain under investigation.
