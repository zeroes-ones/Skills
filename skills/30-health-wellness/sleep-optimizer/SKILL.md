---
name: sleep-optimizer
description: "Use when you need to optimize sleep using circadian science and behavioral interventions. Handles light timing, temperature control, wind-down routines, chronotype alignment, supplement microdosing, and tracker interpretation. Do NOT use for clinical sleep disorders (sleep apnea, insomnia diagnosis)."
license: MIT
author: Sandeep Kumar Penchala
type: health-wellness
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [sleep, circadian, chronotype, sleep-hygiene, sleep-tracking, melatonin, recovery]
token_budget: 4000
chain:
  consumes_from: [habit-engineer]
  feeds_into: [mental-fitness-coach, longevity-biohacker]
  alternatives: [sleep-specialist, clinical-sleep-medicine]
---

# Sleep Optimizer
Portability: universal (checklist + routines + JSON schedule)

<!-- QUICK: 30s -->
One-liner: Deliver a concise sleep-improvement plan: light-timing, pre-bed routine, environment targets, and tracker interpretation.

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
| RP8 | Consent to non-clinical guidance |

### Iterative Research Loop
| Loop | Objective | Output |
| --- | --- | --- |
| Loop 0 | Gather sleep timing & complaints | Sleep-wake window and key complaints (latency, awakenings) |
| Loop 1 | Track & quantify | 7-day baseline: sleep duration, efficiency, bedtime variability |
| Loop 2 | Intervention mapping | Light/temperature/timing regimen + supplements if requested |
| Loop 3 | Adjustment & metrics | 2-week re-check and tracker trends with actionable tweaks |

## Quickstart (30s)
1. Ask: bed/wake times, caffeine/alcohol timing, device use, bedroom setup.
2. Set immediate action: dim lights 90–120 min before bed; keep bedroom 65–68°F; stop caffeine 8–10 hours before bed.
3. Provide a 7-day sleep hygiene checklist and 14-night tracker instruction.

<!-- STANDARD: 3min -->
## Ground rules
- Mechanical triggers: refer to clinician if suspected sleep apnea (snoring + daytime somnolence), parasomnias, or suicidal ideation.
- Use melatonin microdosing 0.1–0.5 mg for circadian phase shifting; 1–3 mg for sleep initiation only short-term.
- Temperature target: 18–20°C (65–68°F) for optimal sleep onset.

## Decision Tree
Start
├─ Primary complaint?
│  ├─ Excessive daytime sleepiness -> Screen for sleep apnea / hypersomnia
│  │   ├─ High STOP-Bang or loud snoring -> Refer to sleep clinic for polysomnography
│  │   └─ Low STOP-Bang -> Evaluate sleep opportunity, circadian misalignment, medications
│  ├─ Difficulty initiating sleep -> Insomnia/psychophysiological
│  │   ├─ High pre-sleep arousal -> CBT-I + stimulus control
│  │   └─ Delayed sleep phase -> Evening light avoidance + morning bright light + melatonin phase advance
│  ├─ Sleep maintenance (wake after sleep onset) -> Check alcohol, nocturia, pain, sleep apnea
│  ├─ Fragmented sleep with environmental drivers -> Optimize temperature, noise, and light
│  └─ Circadian disruption (shift work/jet lag) -> Chronotherapy (timed light + melatonin) and strategic naps
├─ Chronotype mismatch?
│  ├─ Morning type -> schedule demanding tasks early, avoid late stimulants
│  └─ Evening type -> adopt gradual phase-shift protocol if earlier schedule required
├─ Device discrepancies?
│  ├─ Tracker overestimates sleep -> reconcile with diary and consider actigraphy
│  └─ Tracker underestimates sleep (movement-based) -> validate with subjective reports
└─ Red flags -> Suicidal ideation, parasomnias, seizures, heavy daytime impairment -> urgent clinical referral

Decision routing note: Resolve mechanism first (circadian vs insomnia vs sleep disorder) before prescribing medication or supplements. Re-check after Loop 1 tracking and iterate.

<!-- STANDARD: 3min -->
## Core Workflow
1) Intake & triage (Loop 0) <!-- STANDARD: 3min -->
- Collect chronotype, usual sleep window, caffeine/alcohol, medication, travel/shift schedule.

2) Baseline tracking (Loop 1) <!-- STANDARD: 3min -->
- Use sleep tracker or sleep diary for 7–14 days. Key metrics: TST, sleep onset latency, wake after sleep onset, sleep efficiency, bed/wake variability.

3) Intervention mapping (Loop 2) <!-- DEEP: 10+min -->
- Light: 30–60 min of bright light (2,500+ lux) upon wake for phase advance (morning types); for phase delay, avoid morning bright light and use evening light exposure 2–3 hours before desired bedtime. War story: a traveler using light boxes at wrong times worsened jet lag; a timed morning light protocol produced full re-entrainment in 3 days.
- Evening: dim amber/red light 90–120 min before bed; avoid screens or use 90–100% blue-light blocking if screen use unavoidable. Edge case: shift workers using blue-blocking at night may lose visual acuity for work tasks—balance safety and circadian goals.
- Temperature: pre-sleep cool-down routines (30–60 min warm shower followed by cool-down) and bedroom at 18–20°C (65–68°F). Failure narrative: a subject with night sweats required moisture-wicking bedding and ambient fan to stabilize TST.
- Caffeine: cease 8–10 hours before desired sleep time (e.g., before 2pm for 10pm bed); consider individual half-life differences and CYP1A2 polymorphisms in sensitive cases.
- Alcohol: avoid within 4–6 hours of bed; causes fragmented sleep and reduced REM in second half of night.
- Exercise timing: moderate exercise earlier in day preferred; vigorous exercise within 90 minutes of bedtime can increase sleep latency for some individuals—test and adjust.
- Supplements: melatonin 0.1–0.5 mg for phase shifts; 1–3 mg for acute sleep initiation short-term. Magnesium glycinate 200–400 mg may aid sleep continuity in deficient individuals.

4) Chronotype & scheduling alignment
- Morning lark: align cognitive workload early; schedule exercise 1–3 hours after wake for optimal performance.
- Night owl: gradual phase-shift with morning light, earlier meals, and earlier exercise timing; target 30–45 minute phase advance per day when practical.

5) Tracker interpretation
- Oura & Whoop: prioritize TST, sleep efficiency, and sleep stages as directional signals; use 7–14 day trends rather than nightly data.
- Actigraphy: reconcile with sleep diary; consider polysomnography if major discrepancies or clinical concerns.
- HRV: use as recovery trend; recognize device differences and use relative change thresholds (e.g., 10% deviation) rather than absolute values.

6) Jet lag / shift work protocols
- Eastward travel (advance): attempt 60–90 minute phase shifts per day with evening melatonin (0.1–0.5 mg) and morning bright light; pre-adjustment 2–3 days before travel accelerates adaptation.
- Westward travel (delay): use evening light exposure and strategic naps; aim for 1–2 naps (20–40 min) to reduce sleep debt during first 48 hrs.

<!-- DEEP: 10+min -->
## Protocol Examples (deep)
- Sleep onset insomnia: 6–8 week CBT-I informed approach: Week 0 – psychoeducation and baseline sleep window; Weeks 1–3 – stimulus control and sleep restriction (reduce time in bed to increase sleep efficiency to ≥85%); Weeks 4–6 – cognitive restructuring and graduated sleep compression; Week 7–8 – relapse prevention and tapering of active interventions. War story: a patient with chronic insomnia improved sleep efficiency from 68% to 88% after 8 weeks, but only after strict adherence to a 2-week initial sleep restriction period. Emphasize coaching on temporary daytime sleepiness.
- Melatonin phase advance protocol: 0.1–0.5 mg melatonin 1.5–2 hours before target bedtime combined with immediate morning bright light for 30–60 min, for 5–10 days. Edge case: older adults may have altered melatonin pharmacokinetics—start low and monitor next-day sedation.
- Night shift worker protocol: pre-shift 20–30 min nap, expose to bright light during night shift, use dark sunglasses when commuting home, blackout curtains and scheduled 6–8 hour sleep block during the day, stagger social commitments. Failure narrative: inconsistent darkening led to chronic sleep debt—objective blackout and consistent schedule reduced daytime TST variability by 40%.
- Jet lag hard-case: eastbound >6 time zones—combine pre-travel phase shifts (30–60 min/day), low-dose melatonin, and timed light exposure to minimize circadian mismatch. Expect 1 day recovery per time zone with aggressive chronotherapy.

### Protocol caveats & edge cases (15–25 lines)
- Polysomnography indicated when STOP-Bang high, parasomnias suspected, or when objective/subjective mismatch persists despite 2–4 weeks of intervention.
- CBT-I contraindications: active mania or certain psychoses — coordinate with psychiatry.
- Use caution with pharmacologic hypnotics; reserve for short-term rescue or under clinician supervision.
- When incorporating wearable feedback, educate users about false positives (movement vs wake) and set realistic expectations: devices estimate sleep, they don't diagnose disorders.
- For older adults with advanced sleep phase, use evening light and delay meals to shift phase later when socially necessary.

## Error Decoder
| Error Message / Pitfall | Root Cause | Fix | Lesson |
| --- | --- | --- | --- |
| Tracker shows low HRV but subject feels fine | Device variability or short-term stress | Look at trend over 7–14 days, correlate with activity/sleep | Avoid overreacting to single-night fluctuations; treat trends not nights |
| No improvement after hygiene | Behavioral non-adherence or wrong treatment target (circadian vs insomnia) | Introduce CBT-I, enforce sleep restriction, and monitor adherence for 3+ weeks | Align intervention to mechanistic diagnosis before escalating |
| Excessive daytime sleepiness | Possible sleep disorder (apnea) or insufficient sleep opportunity | Screen (STOP-Bang), refer for polysomnography if indicated, increase sleep opportunity if behavioral | Daytime function is a safety metric — escalate early |
| Fragmented sleep after alcohol use | Alcohol reduces REM & fragments second-half sleep | Eliminate alcohol within 4–6 hours of bedtime and re-assess within 1 week | Small behavioral changes can yield big stage improvements |
| Persistent jet lag >7 days | Incorrect timing of light/melatonin or circadian inertia | Recalculate phase-targeted light and melatonin schedule; consider advancing pre-travel | Time-based interventions must be precise to be effective |
| Night shift maladaptation | Irregular sleep timing, inadequate darkening | Implement strict sleep timing, blackout, scheduled naps, and limit social obligations during adaptation | Consistency and environment are non-negotiable for shift work recovery |
| Tracker/diary mismatch | Device algorithms vs subjective reports | Use combined diary+device approach; if mismatch persists, consider actigraphy or clinical testing | Use multiple data streams to form a coherent picture |

## Best practices
1. Prioritize consistent sleep timing — reduce variability to <30–60 minutes nightly; aim for fixed wake time first.
2. Light is the strongest circadian cue — get 30–60 minutes of morning bright light within 1 hour of wake to anchor phase.
3. Treat trackers as directional — validate with a sleep diary and use 7–14 day rolling averages for metrics.
4. Use melatonin for phase-shifting at low doses (0.1–0.5 mg) and only short-term for sleep initiation at 1–3 mg.
5. Combine behavioral (CBT-I) with environmental mods; prioritize stimulus control and sleep restriction for chronic insomnia.
6. Monitor sleep opportunity before labeling insomnia — ensure 7+ hours opportunity window for adults aiming 7–9 hrs sleep.
7. For shift workers, adopt strict darkening and scheduling; expect adaptation over weeks, not days—measure by TST consistency.
8. Use objective readiness markers (next-day alertness, reaction times) to guide intensity of daytime training or cognitive tasks.
9. Avoid heavy meals and vigorous exercise within 60–90 minutes of bedtime for sensitive individuals; test individual tolerance.
10. Reassess and escalate early: if no improvement after 4 weeks with good adherence and no red flags, refer to sleep medicine.

## Production Checklist
- [ ] Sleep baseline recorded (7–14 days sleep diary + tracker)
- [ ] Chronotype & schedule documented
- [ ] Light & temperature plan issued (timing + lux targets)
- [ ] Wind-down routine scripted with exact timings
- [ ] Tracker interpretation guidance provided and validated with diary
- [ ] Melatonin or supplement plan documented with doses and safety notes
- [ ] CBT-I elements scheduled if indicated (stimulus control, sleep restriction sessions)
- [ ] Jet-lag/shift-work schedule prepared (if relevant)
- [ ] Bedroom environment checklist completed (blackout, noise, bedding)
- [ ] Emergency/clinical referral criteria documented for the client
- [ ] Follow-up 2-week re-check scheduled
- [ ] Data-sharing plan with mental-fitness-coach or PCP if needed

## Verification
- Verify improvements in sleep onset latency and sleep efficiency after 2 weeks.
- Check week-to-week reduction in bedtime variability.
- Confirm subjective sleep quality improvement via Likert scale.

## Cross-Skill Coordination
| Skill | When to hand off | Payload |
| --- | --- | --- |
| mental-fitness-coach | If insomnia linked to rumination | CBT techniques, brief thought-record templates, sleep-focused cognitive tools |
| habit-engineer | For routine adherence | Habit stacks for wind-down, morning light exposure, and device curfew strategies |
| nutrition-strategist | When caffeine/alcohol or meal timing affects sleep | Timing of last caffeine, evening meal sizes, alcohol interactions |
| longevity-biohacker | For biomarker-driven sleep interventions | HRV integration, chronotype data, and long-term sleep impacts on biomarkers |
| fitness-programmer | When training timing affects sleep quality | Move high-intensity sessions away from sensitive pre-bed windows, prescribe recovery sessions |


## What Good Looks Like
- Sleep efficiency >85% and total sleep time aligned to target (7–9 hrs), commensurate with age.
- Reduced sleep onset latency (<20 min) and fewer night awakenings.
- Subjective daytime functioning improved.

## References
- Czeisler CA et al., circadian rhythm research and chronobiology reviews (various journals, 2010–2020).
- American Academy of Sleep Medicine clinical practice guidelines (insomnia, obstructive sleep apnea management).
- Buysse DJ, "Cognitive Behavioral Therapy for Insomnia: A Practical Guide," 2011 and related RCTs.
- Elliott JA, "Light and human circadian rhythms: applied chronobiology," Sleep Medicine Reviews, 2019.
- Aricò D. et al., "Melatonin dosing and timing for circadian phase shifts," Journal of Pineal Research, 2018.
- Lockley SW, Czeisler CA, "Effects of light on human circadian physiology," Sleep Medicine Clinics, 2016.

## Scale Depth
- Solo: Rapid 2-week sleep hygiene + light protocol. Tools: sleep diary template, basic light recommendations, household lux meter app. Metrics: TST change, sleep onset latency, bedtime variability. Trigger to escalate: daytime sleepiness or no improvement after 2 weeks.
- Small: 6–8 week CBT-I informed program with weekly checks. Tools: CBT-I worksheets, digital diary, therapist check-ins. Metrics: sleep efficiency, ISI (Insomnia Severity Index) change, adherence. Trigger: ISI not improved by 8 points or worsening symptoms -> clinician referral.
- Medium: Tracker integration and clinician coordination for diagnostics. Tools: actigraphy, Oura/Whoop integration, telehealth coordination with sleep clinics. Metrics: PSG referral rate, diagnostic yield, population adherence. Trigger: elevated STOP-Bang scores or alarming PSG indications.
- Enterprise: Population-level sleep health programs with light therapy design and workplace scheduling interventions. Tools: environmental light design, employee sleep education, policy changes for shift scheduling. Metrics: population sleep health index, workplace incidents, productivity measures. Trigger: cohort-level deterioration or safety incidents related to sleepiness.

## Anti-Hallucination
- [VERIFIED] Temperature 65–68°F (18–20°C) is a commonly recommended sleep range.
- [COMMON-PRACTICE] Morning bright light improves circadian phase for most individuals.
- [INFERRED] Optimal melatonin microdose varies; start low and titrate.
- [UNKNOWN] Individual melatonin pharmacokinetics require clinician oversight for chronic use.
