---
name: stress-resilience-coach
description: "Use when you need to build physiological and psychological resilience. Handles vagal-tone training, HRV protocols, breathwork, cold exposure, burnout prevention, and recovery modalities. Do NOT use for clinical anxiety or PTSD treatment."
license: MIT
author: Sandeep Kumar Penchala
type: health-wellness
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [stress, resilience, HRV, breathwork, cold-exposure, burnout, vagal-tone]
token_budget: 4000
chain:
  consumes_from: [mental-fitness-coach, mindfulness-practitioner]
  feeds_into: [life-architect, productivity-master]
  alternatives: [clinical-psychologist, psychiatrist]
---

# Stress Resilience Coach
Portability: protocols + daily practices (text + JSON scheduling)

<!-- QUICK: 30s -->
One-liner: Deliver an actionable resilience plan combining breathwork, HRV training, cold exposure, and behavioral recovery protocols to reduce allostatic load.

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
| RP8 | Consent to non-clinical resilience interventions |

### Iterative Research Loop
| Loop | Objective | Output |
| --- | --- | --- |
| Loop 0 | Assess stressors & baseline | Identify acute vs chronic stressors and HRV baseline |
| Loop 1 | Prioritize interventions | Rank breathwork, cold exposure, sleep, and social recovery by feasibility |
| Loop 2 | Prescribe protocols | Detailed breathwork/HRV schedule and cold exposure ramp plan |
| Loop 3 | Monitor & adapt | HRV trends, subjective recovery, burnout scales every 2–4 weeks |

## Quickstart (30s)
1. Ask: current stress levels, sleep, daily schedule, medical issues.
2. Immediate action: 3x daily 2-minute diaphragmatic breathing (6 breaths/min) and 1 cold shower 30–60s after warm shower.
3. Provide 2-week starter plan with HRV tracking instructions.

<!-- STANDARD: 3min -->
## Ground rules
- Mechanical triggers: syncope, cardiac history, uncontrolled hypertension, or severe psychiatric conditions -> clinician referral.
- Cold exposure: start gradual (face splash -> 30–60s cold shower) and avoid prolonged exposure without supervision if cardiovascular disease present.
- Breathwork: avoid prolonged Valsalva-like breath holds in populations with cardiovascular risk without clearance.

## Decision Tree
Start
├─ Cardiac risk? -> Medical clearance before cold exposure or HRV pacing
├─ High burnout scores? -> Emphasize sleep, workload reduction, social support
├─ Low HRV & high stress? -> Begin paced breathing + daily recovery interventions
└─ Desire for performance benefits? -> Combine cold exposure with controlled breathing and progressive training

<!-- STANDARD: 3min -->
## Core Workflow
1) Intake & baseline (Loop 0) <!-- STANDARD: 3min -->
- Collect perceived stress scale, burnout screen (OLBI or Copenhagen Burnout Inventory), HRV baseline (7 days morning) if device available.

2) Prioritization (Loop 1) <!-- STANDARD: 3min -->
- Rank interventions by safety & feasibility: breathwork (low friction), sleep optimization, social recovery, cold exposure (moderate), HRV biofeedback (requires device).

3) Protocol prescription (Loop 2) <!-- DEEP: 10+min -->
- Breathwork:
  - Box breathing: 4-4-4-4 for 2–5 min when stressed.
  - Resonance frequency breathing: ~6 breaths/min (5s inhale/5s exhale) for 10–20 min daily to increase HRV.
  - 4-7-8 for acute anxiety: inhale 4, hold 7, exhale 8 x4 cycles.
- Cold exposure ramp:
  - Week 1: face splashes & 30–60s cold end-of-shower x3/week.
  - Week 2–4: increase to 90–120s cold shower 4–5x/week; monitor tolerance.
- HRV training:
  - Use HRV baseline to set respiration target; practice 10–20 min daily biofeedback sessions.

4) Recovery protocols
- Schedule nature exposure 2x/week (30–90 min) and creative-flow activities weekly as buffers against burnout.
- Digital boundary protocol: 60–90 min device-free window before bed, email batching, and fixed work cut-off times.

5) Monitoring & adaptation (Loop 3) <!-- DEEP: 10+min -->
- Track HRV trend, sleep quality, and burnout scores every 2–4 weeks; adapt breath duration, cold exposure, and workload accordingly.

## <!-- DEEP: 10+min --> 14-Day Allostatic Load Reset Protocol
This protocol is designed for someone showing signs of burnout (PSS-10 score >20, HRV trending down for 2+ weeks, subjective exhaustion). It combines physiological and behavioral interventions in escalating doses.

**Days 1-3: Stabilize**
- Morning: 5 min resonance breathing (5.5s in/5.5s out) before getting out of bed. No cold exposure yet.
- Day: Reduce workload 30-50% if possible. No high-intensity training — walking or gentle yoga only (20-30 min).
- Evening: Digital sunset at 8pm — no screens. Take 200mg magnesium glycinate 30 min before bed. Target 8-9h sleep.
- Track: Morning HRV, sleep duration, subjective stress (1-10), energy (1-10).

**Days 4-7: Repair**
- Morning: 10 min resonance breathing + 30s cold at end of warm shower (face only first day, full body by day 7).
- Day: Add one 10 min mindful walk (no phone, notice 5 sensory details). Resume light exercise at 50% volume.
- Evening: Gratitude journal: 3 specific things that went well and why. Continue magnesium, 8-9h sleep target.
- Track: Continue HRV, add mood score (1-10). Expect HRV to stabilize or begin upward trend by day 7.

**Days 8-14: Rebuild**
- Morning: 15 min resonance breathing + 60s cold shower end. Add one Physiological Sigh (double inhale, long exhale) if waking stress is high.
- Day: Resume exercise at 70% normal volume — strength training 2x/week, zone 2 cardio 2x. Add one social connection event per week (coffee, call, group activity).
- Evening: Plan next-day priorities (max 3) to reduce decision load. Continue 8-9h sleep.
- Track: Full PSS-10 at day 14. Compare HRV 7-day rolling average to pre-protocol baseline.

**War Story:** A software engineer with PSS-10 of 28 and HRV at 32ms (well below age norm of 50-60ms) ran this protocol. By day 14 PSS-10 dropped to 18 and HRV rose to 44ms. The key turning point was the social connection component added at day 8 — they'd been doing all solo practices and missing the most potent recovery lever.

**Failure Narrative:** A startup founder tried to do the Rebuild phase while maintaining 14-hour workdays. HRV continued to decline. Lesson: resilience practices cannot outpace chronic sleep deprivation and workload overload — the environmental stressors must be addressed concurrently.

## HRV Training Protocol (Advanced)
1. **Establish baseline**: 7 days of morning HRV readings (same time, position, device). Calculate 7-day rolling average and coefficient of variation (CV). CV >15% indicates unstable autonomic state — focus on stabilization before optimization.
2. **Find resonance frequency**: Use HRV biofeedback app (Elite HRV, Welltory, or Polar chest strap) with paced breathing. Start at 6 bpm (5s/5s), adjust in 0.5 bpm increments until highest LF power achieved (typically 4.5-6.5 bpm for most adults). This is YOUR personal resonance frequency.
3. **Daily practice**: 10-20 min at resonance frequency, 1-2x/day. Morning session most impactful for all-day HRV improvement.
4. **Progressive target**: Aim for HRV increase of 15-30% over 8-12 weeks of consistent practice. If no change after 4 weeks, verify practice consistency >80%, check sleep quality, and reduce training/life stressors.

## Breathwork Protocol Table
| Technique | Pattern | Duration | Best For | Contraindications |
| --- | --- | --- | --- | --- |
| Box Breathing | 4s in / 4s hold / 4s out / 4s hold | 5-10 min | Pre-meeting calm, acute stress spike | None for healthy adults |
| Resonance Breathing | 5.5s in / 5.5s out (~5.5 bpm) | 10-20 min, 2x/day | HRV improvement, chronic stress | Can cause lightheadedness if done too aggressively initially |
| 4-7-8 Breathing | 4s in / 7s hold / 8s out | 4 cycles, max 2x/day | Sleep onset, acute anxiety | Avoid with hypotension or after heavy meals |
| Physiological Sigh | Double inhale through nose, extended exhale through mouth | 1-3 cycles as needed | Immediate stress reset (30s) | None for healthy adults |
| Wim Hof Method | 30-40 forceful breaths + retention | 3-4 rounds, 15-20 min | Cold tolerance, immune activation | Cardiac conditions, pregnancy, epilepsy — avoid without clearance |
| Coherent Breathing | 5s in / 5s out (6 bpm) | 10-20 min daily | HRV resonance, emotional regulation | None; start with 5 min if new to breathwork |

## Error Decoder
| Error Message / Pitfall | Root Cause | Fix | Lesson |
| --- | --- | --- | --- |
| HRV not improving despite practice | Overtraining, poor sleep, or inconsistent practice | Check training load, sleep, and adherence; reduce stressors | HRV responds to systemic recovery, not isolated practices |
| Syncope during cold exposure | Autonomic mismatch or orthostatic stress | Stop cold exposure, medical evaluation; reintroduce gradually after clearance | Safety-first approach for thermal stressors |
| Increased anxiety with breath-holding | Hypercapnia sensitivity or panic response | Switch to gentle paced breathing without holds | Tailor breathing to tolerance |
| Cold exposure leads to chronic fatigue | Overexposure duration or frequency without recovery | Reduce to 2-3x/week at 60s max; add warm-up period; track HRV post-exposure | Dose cold like exercise — progressive overload with recovery |
| Burnout scores improve then plateau | Ignored root causes (toxic workplace, financial stress) | Address systemic stressors; resilience practices alone can't fix broken environments | Build resilience AND remove stressors |
| HRV drops sharply for 3+ days | Impending illness, overtraining, or major life stressor | Reduce training load 50%, prioritize sleep, increase hydration; check resting HR | HRV is a leading indicator — react before symptoms appear |
| "I don't feel anything" from breathwork | Inconsistent practice or wrong technique for goal | Switch to technique matching goal (Physiological Sigh for quick reset vs Resonance for HRV); track HRV to see invisible effects | Subjective feeling ≠ physiological effect; use metrics |
| Social isolation despite resilience practices | Over-focus on solo practices (breathwork, cold) without social recovery | Add 2x/week social connection blocks; join group breathwork or exercise class | Social connection is the most underrated resilience lever |

## Best practices
1. Start with low-friction interventions (breathwork, sleep boundaries) before stressors like cold exposure.
2. Use HRV as a trend metric over 7–14 days rather than reacting to single-day dips.
3. Pair physiological practices with social and behavioral recovery to mitigate allostatic load.
4. Use graded exposure and monitor vitals when introducing thermal or autonomic stressors.
5. Create a recovery menu: short practices (2–5 min), medium (10–30 min), and long (nature/creative flow sessions).
6. Track morning HRV within 15 min of waking, same position, same device for reliable baselines; a 7-day rolling average is your actionable metric.
7. Never increase cold exposure duration AND frequency simultaneously — change one variable per 2-week block.
8. For burnout recovery (allostatic load reset): prioritize sleep 7-9h → reduce workload 30% → add 10 min daily breathwork → reintroduce exercise at 50% volume. Ramp over 6-8 weeks.
9. Pair every stressor with a recovery practice: workout → sauna + hydration; high-stakes meeting → 4-7-8 breath; deadline sprint → mandatory nature walk within 24h.
10. Use subjective measures alongside HRV: Perceived Stress Scale (PSS-10) every 4 weeks, daily RPE for training, and morning readiness score (1-5).

## Production Checklist
- [ ] Baseline HRV & burnout measures taken (PSS-10 or OLBI)
- [ ] Breathwork schedule issued with specific technique, duration, and frequency
- [ ] Cold exposure ramp plan provided (week-by-week progression)
- [ ] Digital boundary & recovery menu created
- [ ] Morning HRV tracking set up (app + reminder)
- [ ] Sleep target set (7-9h) with consistent wake time
- [ ] 14-day burnout protocol initiated if PSS-10 >20
- [ ] Social connection blocks scheduled (min 2x/week)
- [ ] Training load adjusted to match recovery capacity
- [ ] Magnesium supplementation reviewed (200-400mg glycinate if indicated)
- [ ] Caffeine cutoff time set (no caffeine after 2pm or 8h before bed)
- [ ] Weekly review cadence established (Sunday evening 15 min review of HRV trends, stress scores, adherence)
- [ ] Nature exposure scheduled (min 2x 30 min/week)
- [ ] Handoff to mental-fitness-coach if cognitive patterns dominate stress response

## Verification
- Expect subjective stress reduction in 2–4 weeks with consistent practice.
- HRV upward trend over 4–8 weeks if recovery improved and training load stabilized.
- Reduced burnout scale scores after 8–12 weeks with workload adjustments.

## Cross-Skill Coordination
| Skill | When to hand off | Payload |
| --- | --- | --- |
| mental-fitness-coach | For cognitive patterns maintaining stress | CBT interventions for cognitive reframing |
| habit-engineer | For embedding practices | Habit stacks and accountability for breathwork/cold exposure |
| sleep-optimizer | When sleep quality is primary driver of low HRV | HRV trends, sleep schedules, caffeine timing |
| mindfulness-practitioner | For meditation integration with breathwork | Resonance breathing protocol, HRV baseline |
| fitness-programmer | When training load drives autonomic stress | HRV trends, recovery scores, recommended training adjustments |
| nutrition-strategist | For anti-inflammatory nutrition supporting resilience | Stress scores, inflammatory markers if available |

## What Good Looks Like
- Consistent daily breathing practice, progressive cold exposure tolerance, improved HRV trend, reduced burnout and improved sleep.

## References
- Porges S., "The Polyvagal Theory: Neurophysiological Foundations of Emotions, Attachment, Communication, and Self-Regulation," 2011 — foundational framework for autonomic state and vagal tone.
- Lehrer P. et al., "Heart Rate Variability Biofeedback: How and Why Does It Work?" Frontiers in Psychology, 2014 — evidence for resonance frequency breathing and HRV improvement.
- Huberman A., "Mastering Stress" podcast series — protocols for Physiological Sigh, cold exposure dosing, and HRV.
- Hof W., "The Wim Hof Method," 2020 — cold exposure and breathwork framework (use with medical screening).
- Cohen S. et al., "Perceived Stress Scale (PSS-10)" — validated stress assessment tool.
- Demartini B. et al., "Burnout assessment tools: OLBI and Copenhagen Burnout Inventory," various publications.
- Walker M., "Why We Sleep," 2017 — sleep's role in stress resilience and autonomic recovery.
- Sapolsky R., "Why Zebras Don't Get Ulcers," 3rd ed., 2004 — allostatic load and stress physiology.

## Scale Depth
- Solo: Self-guided breathwork and cold shower ramp.
- Small: Coach-monitored HRV biofeedback program.
- Medium: Corporate resilience programs with education + biofeedback hardware.
- Enterprise: Organizational burnout prevention and recovery systems integrated with HR and healthcare.

## Anti-Hallucination
- [VERIFIED] Resonance breathing (~6 breaths/min) increases HRV in many individuals.
- [COMMON-PRACTICE] Cold showers are a low-cost exposure method; evidence supports acute sympathetic activation and adaptation.
- [INFERRED] Magnitude of HRV change depends on baseline health and training load.
- [UNKNOWN] Long-term outcomes of scheduled cold exposure on major health endpoints remain under study.
