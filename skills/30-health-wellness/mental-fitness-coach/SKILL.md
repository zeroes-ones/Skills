---
name: mental-fitness-coach
description: "Use when you need practical mental fitness protocols. Handles CBT techniques, resilience training, emotional regulation frameworks, MBSR, positive psychology exercises, and ACT-based defusion. Do NOT use for clinical mental health diagnosis or therapy."
license: MIT
author: Sandeep Kumar Penchala
type: health-wellness
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [CBT, resilience, mindfulness, MBSR, emotional-regulation, positive-psychology, ACT]
token_budget: 4000
chain:
  consumes_from: [mindfulness-practitioner]
  feeds_into: [stress-resilience-coach, life-architect]
  alternatives: [licensed-therapist, clinical-psychologist]
---

# Mental Fitness Coach
Portability: universal (scripts + exercises + daily prompts)

<!-- QUICK: 30s -->
One-liner: Provide structured, evidence-based mental fitness interventions: CBT worksheets, MBSR micro-practices, and resilience-building plans.

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
| Loop 0 | Clarify presenting problem | One-sentence problem statement and red flags for clinical referral |
| Loop 1 | Baseline measures | PHQ-2/PHQ-9/GAD-7 screening (non-diagnostic) |
| Loop 2 | Intervention selection | CBT skills, MBSR, or positive-psych exercises mapped to needs |
| Loop 3 | Practice & review | Weekly practice plan and 4-week outcomes review |

## Quickstart (30s)
1. Screen: PHQ-2 and GAD-2; if positive, suggest referral to clinician.
2. Provide a 7-day micro-practice plan: 10 min daily mindfulness + 1 CBT thought record.
3. Output: Daily prompts, script for guided 10-minute MBSR session.

<!-- STANDARD: 3min -->
## Ground rules
- Mechanical triggers: suicidal ideation, self-harm, psychosis, or severe deterioration -> urgent clinical referral.
- Use short validated scales to monitor: PHQ-9, GAD-7 every 2 weeks for tracking.
- Maintain confidentiality & encourage clinician contact for diagnosis.

## Decision Tree
Start
├─ Presentation?
│  ├─ High distress or clinical flags -> Immediate clinical referral
│  │   ├─ Suicidal ideation, psychosis -> Emergency services / psychiatry
│  │   └─ Moderate-severe PHQ/GAD -> Recommend clinician + adjunct brief intervention
│  ├─ Negative thought patterns & avoidance -> CBT-focused plan
│  │   ├─ Avoidance dominant -> Graded exposure + behavioral activation
│  │   └─ Cognitive distortions dominant -> Thought records + Socratic questioning
│  ├─ Chronic stress & rumination -> MBSR + behavioral activation
│  │   ├─ High workload -> Time-limited acceptance exercises, micro-practice
│  │   └─ Chronic worry -> Worry time scheduling + defusion techniques (ACT)
│  └─ Low positive affect / anhedonia -> Positive psychology interventions
│       ├─ Low engagement -> Behavioral activation with mastery tasks
│       └─ Low pleasure -> Savoring exercises and gratitude journaling
├─ Comorbidity with sleep or substance use?
│  ├─ Yes -> Coordinate with sleep-optimizer or addiction specialist
│  └─ No -> proceed with selected brief intervention
└─ Follow-up cadence?
   ├─ High-risk -> weekly contact and symptom scale monitoring
   └─ Low-risk -> biweekly check-in and practice audits

Decision routing note: Start with least invasive, scalable interventions (micro-practices) while ensuring safety nets and referral pathways are active.

<!-- STANDARD: 3min -->
## Core Workflow
1) Intake & triage (Loop 0) <!-- STANDARD: 3min -->
- Document current symptoms, triggers, coping strategies, history of mental health care.

2) Baseline measurement (Loop 1) <!-- STANDARD: 3min -->
- Use PHQ-9, GAD-7, and a single-item sleep quality question. Record baseline scores.

3) Intervention mapping (Loop 2) <!-- DEEP: 10+min -->
- CBT: Thought record templates, behavioral experiments, graded exposure, behavioral activation scheduling. War story: a client with social anxiety avoided all group activities; a 6-week graded exposure hierarchy (start with 5-min coffee queue, progress to 30-min group meeting) restored functioning and work attendance in 10 weeks.
- MBSR micro-practices: 10–20 min daily practice (body scan, mindful breathing, mindful walking) with weekly reflection. Edge case: high-ruminators may initially experience increased distress during sitting practice—introduce brief movement-based practices and defusion techniques first.
- ACT/defusion: Cognitive defusion scripts to reduce thought fusion (labeling thoughts, thank-you-mind technique). Practical note: use with caution in clients with dissociative tendencies—prefer grounding anchors.
- Resilience training: deliberate challenge exposure (small, controlled stressors), narrative reframing (writing exercises), meaning-making exercises (valued-action mapping). Failure narrative: pushing graded exposure too fast led to avoidance rebound—always pace by tolerance.

4) Practice prescription & follow-up (Loop 3) <!-- DEEP: 10+min -->
- Week 0–2: Psychoeducation, baseline measures, and 10–12 min/day micro-practice (2x5–6 min sessions). Teach one CBT skill and one mindfulness anchor.
- Week 3–4: Introduce behavioral activation tasks (2 mastery + 3 pleasure tasks/week) and 1 graded exposure per week with clear metrics (SUDS pre/post, behavioral completion).
- Week 5–8: Consolidate skills, widen exposure, add self-compassion practices for setbacks, and plan relapse prevention.
- Measurement plan: PHQ-9 / GAD-7 every 2 weeks, weekly practice logs, pre/post SUDS for exposures. War story: Adding simple mood ratings before/after activities improved adherence by creating visible short-term reward signals.
- High-intensity escalation plan: If suicidal ideation or symptom escalation appears at any point, stop program and refer immediately with documentation for continuity of care.

## Protocol Examples (detailed)
- CBT Thought Record (template): Situation -> Emotion (0–100) -> Automatic Thought -> Evidence for/against -> Alternative thought -> Behavioral experiment -> Outcome (1 week). Use twice weekly for 6 weeks.
- Behavioral Activation protocol: Create a daily schedule with 5 slots (2 mastery, 2 pleasure, 1 social). Track pre/post mood (scale 0–10) to quantify effect. Expect acute mood lift within the week for mastery tasks.
- Self-Compassion Break script: 1) Notice suffering (label it), 2) Common humanity statement, 3) Offer self-kindness phrase. Practice 1–3x/day in response to setbacks.
- Graded exposure template: Build hierarchy (10 items), begin with item scoring 3/10 SUDS, complete exposure twice/week, measure SUDS reduction target of 50% by week 6.

### Evidence summary table
| Intervention | Effect Size (typical) | Timeframe | Confidence | Practical Notes |
| --- | ---:| --- | --- | --- |
| CBT (structured) | Large for depression/anxiety | 6–12 weeks | High (RCTs/meta-analyses) | Most evidence-based; requires adherence
| MBSR (8-week) | Small-medium on stress reduction | 8 weeks | Moderate-high | Works well for rumination, adjunct to CBT
| Behavioral Activation | Medium for depression | 4–8 weeks | Moderate | Simple, quick to implement
| ACT/Defusion | Small-medium for experiential avoidance | 6–12 weeks | Moderate | Useful for chronic worry and acceptance-based goals

## Error Decoder
| Error Message / Pitfall | Root Cause | Fix | Lesson |
| --- | --- | --- | --- |
| Low engagement (practice <3x/week) | Practice too long, low immediate reward, no habit anchor | Use 2-minute starts, habit-stack with existing cue (toothbrush, coffee), set micro-goals | Small wins compound; design for initial success |
| Worsening symptoms after homework | Underlying clinical pathology or improperly dosed exposure | Pause exposure, reassess with PHQ/GAD, escalate to clinician if suicidal or psychotic signs | Safety-first—coaching must triage to clinical care when needed |
| Cognitive avoidance (unable to complete thought records) | Too much cognitive load or triggering content | Use behavioral experiments and ACT defusion techniques first, then re-introduce CBT slowly | Match method to tolerance and readiness |
| No symptom change after 4 weeks | Low adherence, wrong match of technique, or comorbidity (sleep/substance) | Check adherence, coordinate with sleep-optimizer, consider alternative modality (ACT vs CBT) | Re-evaluate mechanism before persisting with one approach |
| Drop in motivation during exposure phase | Exposure progression too fast or lack of perceived benefit | Slow hierarchy, add reinforcement and social accountability, pair exposures with valued actions | Pace increases tolerance and builds self-efficacy |
| Avoidance rebound after failed experiment | Client generalizes failure to global incompetence | Normalize setbacks, run simpler behavioral experiments, and debrief learning | Frame experiments as data-gathering, not pass/fail tests |
| Measurement drift (scales inconsistent) | Rater bias, inconsistent scale use, or external life events | Standardize measurement timing, use multiple metrics (self-report + behavioral) | Multiple metrics reduce noise and improve decision-making |

## Best practices
1. Use short, daily micro-practices (5–15 min) to build consistency; aim for 5–7 sessions/week initially.
2. Combine CBT skills with behavioral activation for depression-related low motivation—schedule 2 mastery tasks/week and track mood pre/post.
3. Use MBSR scripts for stress reactivity — 10–20 min/day for 8 weeks shows measurable reductions in perceived stress.
4. Track symptoms quantitatively (PHQ-9/GAD-7) every 2 weeks and mood ratings daily to catch drift.
5. Employ socio-contextual strategies: coordinate with sleep-optimizer and fitness-programmer to target sleep and activity as adjuncts.
6. Use graded exposure with concrete SUDS targets and progress only when SUDS decreases by 30–50% across repetitions.
7. Prioritize self-compassion and relapse planning—build an automated check-in and coping menu for setbacks.
8. Use behavioral experiments for belief testing—pick one hypothesis per week and measure outcome objectively.
9. Keep documentation concise and shareable for smooth handoffs to clinicians when needed.
10. Use digital prompts sparingly—no more than 2 reminders/day to avoid user fatigue and promote intrinsic motivation.

## Production Checklist
- [ ] Baseline screening completed (PHQ-9/GAD-7 and safety screen)
- [ ] 4–8 week plan issued with weekly objectives
- [ ] Daily practice scripts provided with audio/video where possible
- [ ] Escalation plan documented with clinician contacts
- [ ] Measurement schedule set (PHQ-9/GAD-7, daily mood logs, SUDS for exposures)
- [ ] Habit integration plan with habit-engineer for adherence
- [ ] Sleep handoff to sleep-optimizer if rumination affects sleep
- [ ] Emergency safety plan discussed and documented
- [ ] Consent for data-sharing with clinician (if requested)
- [ ] Weekly adherence and outcome review scheduled
- [ ] Behavioral experiment templates provided with success criteria
- [ ] Relapse prevention and maintenance checklist created

## Verification
- Expect symptom reduction of 20–40% on PHQ-9/GAD-7 scores over 6–8 weeks for mild-moderate cases with adherence.
- Monitor adherence: >=5 practices/week for 4 weeks signals good engagement.

## Cross-Skill Coordination
| Skill | When to hand off | Payload |
| --- | --- | --- |
| sleep-optimizer | When rumination affects sleep | Sleep-focused CBT elements, wind-down routines, timing adjustments |
| habit-engineer | For embedding practices | Habit stacks, commitment devices, tracking tools, accountability plans |
| stress-resilience-coach | For physiological regulation adjuncts | HRV-informed breathing protocols, cold exposure contraindications |
| life-architect | For long-term goal alignment | Narrative reframing outputs, meaning-making exercises, values mapping |
| nutrition-strategist | When nutrition influences mood (caffeinated stimulants, deficiencies) | Micronutrient checks, timing of meals, supplement plans |

## What Good Looks Like
- Consistent daily practice for 4+ weeks, symptom improvement, increased behavioral activation and functioning.
- No escalation to clinical services required; if required, smooth handoff with documentation.

## References
- Beck AT, "Cognitive Therapy and the Emotional Disorders," foundational CBT texts and clinical trials (1970s–present).
- Kabat-Zinn J., "Full Catastrophe Living," MBSR manuals and RCT evidence (1990s–2010s).
- Cuijpers P., et al., "CBT for depression: meta-analytic reviews," Psychological Medicine, 2016.
- Martinsen EW, "Behavioral activation and depression reviews," Clinical Psychology Review, 2015.
- Hayes SC, Strosahl K., "Acceptance and Commitment Therapy (ACT): model and applications," various RCTs and manuals.
- Seligman M., "Positive Psychology Interventions: Gratitude, savoring evidence," PPND and meta-analyses.

## Scale Depth
- Solo: 4–8 week self-guided program with digital prompts and audio scripts. Tools: guided audio, worksheets, habit-builder app. Metrics: PHQ-9/GAD-7 change, practice frequency. Trigger to escalate: worsening PHQ/GAD or suicidal ideation.
- Small: Coach-led weekly check-ins with homework review and structured BA/CBT sessions. Tools: shared tracking, video coaching. Metrics: adherence, symptom reduction, functional improvement measures.
- Medium: Group MBSR cohorts with facilitator and measured outcomes (pre/post ISI, PSS). Tools: group platform, facilitator guide, peer accountability. Metrics: group retention, average symptom drops.
- Enterprise: Workplace resilience program integrated with EAP resources and manager training. Tools: program dashboards, training modules, outcome tracking. Metrics: reduced time-off, improved productivity indices, HELP referrals.

## Anti-Hallucination
- [VERIFIED] CBT and MBSR have strong RCT evidence for mild-to-moderate symptoms.
- [COMMON-PRACTICE] PHQ/GAD screening is standard for monitoring.
- [INFERRED] Expected symptom change depends on adherence; estimate given is typical but not guaranteed.
- [UNKNOWN] Individual response heterogeneity requires clinician oversight for diagnosis.
