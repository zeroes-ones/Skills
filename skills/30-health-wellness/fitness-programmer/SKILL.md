---
name: fitness-programmer
description: "Use when you need evidence-based strength & cardio programming. Handles periodized templates (5x5, 5/3/1, GZCL), progressive overload, deloads, mobility, RPE-based auto-regulation, and home-gym design. Do NOT use for clinical rehabilitation or physical therapy prescription."
license: MIT
author: Sandeep Kumar Penchala
type: health-wellness
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [strength, cardio, periodization, programming, mobility, home-gym, autro-reg, training-plans]
token_budget: 4000
chain:
  consumes_from: [habit-engineer]
  feeds_into: [nutrition-strategist, longevity-biohacker]
  alternatives: [personal-trainer, strength-coach]
---

# Fitness Programmer
Portability: universal (text + JSON templating)

<!-- QUICK: 30s -->
One-liner: Produce an evidence-backed, periodized training plan (strength + cardio + mobility) tailored to goals, equipment, and training age in under a minute.

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
| RP8 | Consent to non-clinical fitness guidance |

### Iterative Research Loop
| Loop | Objective | Output |
| --- | --- | --- |
| Loop 0 | Surface constraints & goals | One-line goal summary + red flags (injury, medication) |
| Loop 1 | Baseline metrics & training age | Training age classification (novice/intermediate/advanced) and 1RM estimates |
| Loop 2 | Equipment & schedule mapping | Weekly plan skeleton (sessions, duration, focus) |
| Loop 3 | Microcycle templating & auto-reg rules | 4-week mesocycle with deload and RPE/RIR rules |

## Quickstart (30s)
1. Ask: goal (strength/hypertrophy/weight-loss/conditioning), days/week, key equipment, training age.
2. Classify: Novice/Intermediate/Advanced using last 12-week progress & ability to squat/press/pull.
3. Output: 4-week sample microcycle (3 sessions) with sets, reps, intensity bands (RPE) and daily mobility.

<!-- STANDARD: 3min -->
## Ground rules
- Mechanical triggers: stop if acute pain, red-flag symptoms, or clinical instructions from a provider.
- Use RPE 6–9 for main work; leave 0–2 RIR on accessory sets unless hypertrophy block demands closer to failure.
- Autoregulation: apply RPE-based load selection, jump sets when progress stalls for 2+ weeks.

## Decision Tree (routing)
Start
├─ Primary Goal?
│  ├─ Strength → Periodization path
│  │   ├─ Training age = Novice → Linear progression (3x/week full-body)
│  │   ├─ Training age = Intermediate → Block periodization (4–12 weeks accumulation/intensification)
│  │   └─ Training age = Advanced → Undulating/conjugate + peaking
│  ├─ Hypertrophy → Volume management path
│  │   ├─ Weekly sets per muscle <10 → increase to 10–20 sets/week
│  │   └─ Already high volume → implement intensity techniques (drop sets, rest-pause)
│  ├─ Fat loss → Energy-first path
│  │   ├─ Time-limited? → Prioritize resistance training 2–3x/wk + 2 low-impact cardio
│  │   └─ Long-term → Higher frequency strength maintenance + progressive overload
│  └─ Mixed/General Fitness → Concurrent approach
│       ├─ Time ≥6 hrs/wk → Balanced strength & conditioning split
│       └─ Time <6 hrs/wk → Prioritize one modality; use low-intensity maintenance for the other
├─ Equipment constraints?
│  ├─ Full barbell setup → Use barbell-focused templates (5x5, 5/3/1, GZCL)
│  ├─ Dumbbells/KBs only → Use density/tempo progressions and unilateral emphasis
│  └─ Bodyweight only → Progressions via leverage, eccentrics, and density (AMRAP, EMOM)
├─ Injury or joint limitation?
│  ├─ Acute red-flag → Medical clearance before program
│  ├─ Chronic tendon/joint issue → Reduce high-impact loading, prioritize tempo + higher rep ranges for tissue adaptation
│  └─ Post-rehab maintenance → Low-shear variations + mobility & prehab blocks
├─ Sport-specific seasonality?
│  ├─ In-season → Low-volume maintenance, focus on power/expressive work
│  └─ Off-season → Build volume and capacity (8–12 weeks base)
└─ Testing & readiness
   ├─ Want max testing? → Schedule testing week after a deload
   └─ Want performance peaking? → Implement 3-week taper prior to event

Decision routing note: always re-evaluate after Loop 1 and use RPE/RIR to gate load increases. For mixed goals, adopt an 80/20 priority split (prioritize 80% of adaptation target).

<!-- STANDARD: 3min -->
## Core Workflow
1) Intake & triage (Loop 0) <!-- STANDARD: 3min -->
- Collect goals, availability, equipment list, injury notes.
- Red-flag screening: recent cardiac symptoms, uncontrolled hypertension, severe joint pain.

2) Baseline & classification (Loop 1) <!-- STANDARD: 3min -->
- Estimate 1RM via submax rep testing (e.g., 5RM -> Epley formula) or auto-estimate from RPE logs.
- Determine training age: Novice (0–6 months structured), Intermediate (6–36 months), Advanced (3+ years consistent).

3) Macrocycle & mesocycle design (Loop 2) <!-- DEEP: 10+min -->
- Choose periodization: linear for novices, undulating/conjugate for advanced.
- Example: 12-week plan: 4wk accumulation (volume), 4wk intensification, 4wk peaking/deload.

4) Weekly microcycle templating (Loop 3) <!-- DEEP: 10+min -->
- Example 4-day upper/lower split for intermediate:
  - Day 1 Upper Strength (main: bench 5x5 @ RPE7)
  - Day 2 Lower Strength (squat 5x5 @ RPE7)
  - Day 3 Conditioning/Active Recovery (zone 2 30–45min)
  - Day 4 Upper Volume (4x8–12 accessory)
  - Day 5 Lower Volume (glute/ham emphasis)
  - Day 6 Optional conditioning
  - Day 7 Rest/deliberate recovery

5) Session-level programming
- Warm-up: 6–10 minutes dynamic + movement prep; 2–4 ramps to working weight.
- Main lift prescription: sets x reps @ %1RM or RPE band.
- Accessory work: target weaknesses, 6–12 reps, 3–4 sets.
- Mobility: 5–12 minutes post-session mobility: thoracic extensions, hamstring flossing, hip CARs.

6) Auto-regulation & progression rules
- Weekly progression: +2.5–5 lb for upper body, +5–10 lb for lower on successful top sets.
- If RPE > target two consecutive sessions, reduce load 2.5–5% or deload week.
- Deload: reduce volume 40–60% and intensity ~10–20% for 1 week every 4–8 weeks depending on training age. <!-- DEEP: 10+min -->
  - Deep narrative: Common failure is skipping deloads during a long hypertrophy block. Example: a competitive lifter skipped deloads for 10 weeks chasing PRs and developed CNS fatigue—top-set velocities dropped 12% and sleep quality fell. Introducing a mandatory deload every 4th week, plus a monitored 48–72 hour low-load recovery window after heavy sessions, restored velocity and returned progression within two cycles. Use objective readiness: morning HRV (7-day rolling average), PRS (perceived recovery status <4/10) and bar speed loss >8% to trigger an unscheduled micro-deload.
  - Edge cases: advanced athletes in peaking phases may tolerate shorter deloads (3–4 days) with active recovery (mobility & light aerobic). Novices benefit from full week deloads every 6–8 weeks. When in-season, swap volume deloads for intensity maintenance to preserve neuromuscular adaptations.
  - Failure narrative: A gym cohort showed higher injury rates when deloads were optional—mandatory deload scheduling reduced soft-tissue complaints by 35% across 12 weeks.


<!-- DEEP: 10+min -->
## Programming Templates (practical protocols) <!-- DEEP: 10+min -->
- Novice Linear Strength (3x/week): Full body, A/B/C rotation, 3 sets main lifts 5–8 reps, add weight each session. War story: a novice who added weight every session without technique cues developed thoracic rounding—introducing a 2x/week video check and a once-weekly mobility slot fixed form and improved presses by 12% in 6 weeks.
- 5x5 Intermediate: 3–4 sessions, heavy compound focus, accessory hypertrophy 8–12 reps, weekly + progression. Edge case: intermediate lifters with poor recovery should convert to 3x5 with added RPE cap (RPE ≤8) to maintain progress.
- GZCL-style: Tiered template (T1 1–5, T2 6–12, T3 12+). Prescribe T1 volume low, T2 moderate, T3 high. Failure narrative: an athlete used GZCL but overloaded T2 and T3; outcome was chronic knee pain—solution: cap weekly T3 volume per muscle to 12–18 sets and add rotation for joint relief.
- 5/3/1: 4-week wave: Week1 (65/75/85 x5), Week2 (70/80/90 x3), Week3 (75/85/95 x1+), Week4 deload. Advanced tweak: use jokers/AMRAP only on de-loaded weeks for hypertrophy blocks.
- Cardio periodization: Base (8–12 weeks zone 2), Build (4–6 weeks threshold), Peak (VO2 intervals 2–4 weeks). Practical note: a cyclist stalled when switching to threshold too early—returning to an extra 4 weeks of zone 2 rebuilt aerobic base and raised power at lactate threshold by 6%.

Advanced protocols and edge cases (15–25 lines):
- Concurrent training management: For athletes requiring both strength and endurance, prioritize one modality per mesocycle (e.g., 8-week strength block with 1–2 low-intensity aerobic sessions) to mitigate interference; ensure at least 24-hour separation between high-intensity endurance and heavy strength sessions.
- Autoregulatory progressive overload (APRE): Use APRE 3-day protocol for bench/squat when weekly top-set reps vary — reduces failure risk while promoting steady load increases.
- Peaking for single events: Implement a 3-week taper (week -3 heavy accumulation, week -2 intensity maintenance with volume -30%, week -1 sharpness with volume -60%) to peak for meet/test.
- Home-gym variant: Substitute barbells with dumbbell/KB progressions using tempo and density progressions (increase sets/week or reduce rest) when absolute load increments are limited.
- Injury-aware substitution table: If shoulder impingement: replace heavy bench with incline DB press + banded pull-aparts; if low-back complaint: shift from conventional deadlift to trap-bar or Romanian with reduced ROM.
- RPE to %1RM conversion table inclusion and an algorithm for estimating training max from 3–8RM tests with conservative factor (-10% for training max for novices, -5% for advanced).
- Example failure case: a trainee stalled on squat for 8 weeks due to skipped deloads and poor sleep—prescribed scheduled deload every 4th week and nightly sleep target of 7.5+ hrs; progress resumed with +7% 1RM in 2 cycles.
- Programming hygiene: log top-set velocity or bar speed on three lifts; if speed drops >10% across sessions, apply micro-deload (reduce top-set load 5%) and retest after 5–7 days.


## Exercise Selection Guide
- Prioritize multi-joint lifts for strength: squat, deadlift, bench, overhead press, pull-up/row.
- Swap depending on mobility: front squat if limited dorsiflexion, trap-bar DL for lumbar protection.
- Accessory selection: pair agonist/antagonist, address glute/upper-back weakness, core anti-rotation drills.

## Programming Examples (JSON templates) <!-- DEEP: 10+min -->
- Provide machine-readable output: {"plan_name":"4wk strength","sessions":[{"day":1,"focus":"upper-strength","exercises":[{"name":"bench","sets":5,"reps":5,"intensity":"RPE7"}]}]}

### Evidence summary table
| Program | Best For | Weekly Time | Expected Results (12 weeks) | Evidence Level |
| --- | --- | ---:| --- | --- |
| Novice linear progression | New lifters (0–6 mo) | 3–4 hrs | +10–25% 1RM, improved motor patterns | High (consistent RCTs & comp models) |
| 5x5 | Strength-focused intermediates | 3–6 hrs | Stable strength gains, high CNS load | Moderate (programming & cohort data) |
| 5/3/1 | Intermediate/advanced peaking | 3–6 hrs | Conservative strength gains, durable progress | Moderate (widely used, coach reports) |
| GZCL/tiered | Advanced hypertrophy + strength balance | 4–8 hrs | Improved strength + hypertrophy with volume control | Moderate (programming case series) |
| Zone-2 Base Cardio | Endurance base building | 2–6 hrs | ↑VO2 threshold, mitochondrial adaptations | High (exercise physiology literature) |

Practical application: Use evidence level + athlete profile to weight program selection. For time-limited clients, prefer condensed full-body sessions (3x/week) with emphasis on compound lifts and progressive density.

## Error Decoder
| Error Message / Pitfall | Root Cause | Fix | Lesson |
| --- | --- | --- | --- |
| Client stalls for 3+ weeks (no PRs, rep loss on top sets) | Under-recovery (sleep <7 hrs/wk average), insufficient progressive overload, or inconsistent volume | Audit sleep & nutrition, reduce weekly volume 10–20% for 1–2 weeks, apply RPE gating, reintroduce micro-loads (2.5–5 lb) | Recovery gating is primary — progress returns when workload matches capacity |
| Persistent joint pain localized to one joint (knee, shoulder) | Movement pattern fault, unaddressed mobility deficit, or cumulative tendon load >12 sets/week | Substitute variations (front squat/trap-bar), add prehab (banded eccentrics), cap weekly sets for offending muscle to 8–12 | Protect tissue by managing chronic load and movement mechanics |
| No measurable strength gains despite adherence | Program lacks progressive overload or poor intensity control (no RPE tracking) | Implement daily RPE logging, set 3-week progression plan with APRE or linear load increases, re-test 1RM after 6–8 weeks | Discipline in tracking reveals missed opportunities for progression |
| Rapid weight loss with disproportionate strength loss | Aggressive calorie deficit (>20%), low protein (<1.4 g/kg), high cardio | Increase calories by 100–300 kcal, raise protein to 1.6–2.2 g/kg, shift some cardio to low-intensity steady state | Prioritize lean mass preservation when cutting fast |
| Overtraining indicators (elevated resting HR >7 bpm above baseline, persistent fatigue) | Accumulated high-intensity volume + inadequate recovery | Immediate 7–14 day reduced load (volume -40%), increase sleep and nutrition, medical review if severe | Implement preventive deload schedules and monitor objective readiness metrics |
| Failed peaking for event (timing mismatch) | Taper started too late/early or intensity mismanaged | Reconstruct taper: heavy maintenance 10–14 days before test, volume step-down at -7 to -3 days, sharp reduction -1 week; retest after full taper cycle | Peaking requires reverse engineering from event date; schedule it, don't guess |
| Poor adherence (missed 30–50% sessions over 8 weeks) | Unattainable schedule, life friction, lack of accountability | Reduce sessions to sustainable minimum, convert to time-efficient full-body sessions, add habit-engineer stack and accountability partner | Match plan to lifestyle; consistency beats complexity |


## Best practices
1. Measure performance, not just body composition—track bar speed (m/s), reps in reserve, and session RPE; flag >10% speed drop on main lifts.
2. Use conservative incremental loading (2.5 lb upper, 5 lb lower) and micro-loading plates when possible to maintain steady progress.
3. Prioritize movement quality over ego-loads—record video every 2–4 weeks and use frame-by-frame checklists for squat depth, knee track, and lumbar posture.
4. Implement scheduled deloads: every 4th week for intermediates, every 6–8 weeks for novices, with volume -40–60% and intensity -10–20%.
5. Use tiers for exercise selection: primary compound (60–75% session time) > secondary compound (15–25%) > single-joint accessory (10–15%).
6. Monitor objective readiness: morning HRV 7-day rolling average, resting HR, and PRS; trigger micro-deload if HRV drops >10% or PRS <4/10.
7. Preserve strength during calorie deficit: maintain ≥2 heavy sessions/week and protein ≥1.6 g/kg to minimize strength loss.
8. Match weekly sets to goals: hypertrophy 10–20 sets/muscle/week; strength-focused lower volume with higher intensity (6–12 heavy sets per lift/week).
9. Use tempo and density progressions when load increments unavailable: increase time under tension by 10–20% or reduce rest by 15–30% across 2–4 weeks.
10. Document and audit: weekly adherence, mobility flags, and subjective recovery; prioritize fixing systemic recovery issues before adding volume.

## Production Checklist
- [ ] Goal & constraints documented (primary goal, timeline, red flags)
- [ ] Training age classified (novice/intermediate/advanced)
- [ ] Equipment list confirmed (barbell, dumbbells, machines, cardio)
- [ ] 4-week mesocycle generated with weekly sessions and durations
- [ ] Autoregulation rules set (RPE gates, micro-loading scheme)
- [ ] Mobility and prehab included (movement screening + corrective exercises)
- [ ] Deload schedule established (every 4–8 weeks as per training age)
- [ ] Testing week scheduled (1RM or submax protocol after deload)
- [ ] Nutrition handoff request sent to nutrition-strategist (if needed)
- [ ] Habit/accountability plan created with habit-engineer
- [ ] Sleep & recovery targets documented (sleep hours, HRV baseline)
- [ ] Video submission plan for movement checks established
- [ ] Safety & emergency instructions reviewed with client
- [ ] Tracking template (CSV/JSON) provided for logging RPE, load, and notes

## Verification
- Verify plan completeness (sessions/week, sets, reps, RPE bands).
- Check progression rules are explicit and numbers given for micro-loading.
- Simulate 1-week plan and ensure time estimates match user availability.

## Cross-Skill Coordination
| Skill | When to hand off | Payload |
| --- | --- | --- |
| nutrition-strategist | After program intensity & goal set | Calorie targets, peri-workout macros, refeeds for heavy blocks |
| habit-engineer | During adherence planning | Habit stack for session prep, travel/training consistency, accountability system |
| sleep-optimizer | If recovery low | Sleep window scheduling, nap strategy, HRV trends |
| longevity-biohacker | For long-term athlete care | DEXA/VO2 data, biomarker changes, supplement interactions |
| physical-therapist | If persistent movement/pain issues | Movement screen, referrals, rehab-to-performance handoff |

## What Good Looks Like
- 12-week measurable strength increase: +5–15% in main lifts for intermediate, 10–25% for novice.
- Session adherence >=80% over 8 weeks.
- No unresolved joint pain; mobility improvements recorded.

## References
- Rhea MR et al., "Progression models in resistance training for healthy adults." Med Sci Sports Exerc. 2003.
- American College of Sports Medicine, "Position Stand: Progression Models in Resistance Training for Healthy Adults," Med Sci Sports Exerc. 2009.
- Schoenfeld BJ, "Science and Development of Muscle Hypertrophy," Human Kinetics, 2016.
- Epley B., "Estimating 1RM from submaximal loads," Strength & Conditioning literature, 1985.
- Zourdos MC et al., daily undulating periodization and practical applications (peer-reviewed cohort studies), 2016.
- Bompa T., Haff G., "Periodization: Theory and Methodology of Training," Human Kinetics, 2019.
- Grgic J., et al., "Resistance training frequency and hypertrophy," Sports Medicine review, 2018.
- Baker D., Newton R., "Velocity-based training: Practical applications," Strength & Conditioning Journal, 2017.

## Scale Depth
- Solo: 3x/week novice linear with minimal equipment. Tools: simple spreadsheet tracker, video submissions, sheet-based progression. Metrics: body mass, session RPE, top-set reps logged weekly. Trigger to escalate: failure to progress for 6–8 weeks or recurring pain.
- Small (trainer-to-client): Personalized split with weekly check-ins and 1–2 monthly video reviews. Tools: coach dashboard, shared tracker, short-form testing (3–5RM). Metrics: adherence %, top-set velocity, weekly training load. Trigger: plateau >3 weeks or injury signal.
- Medium (gym program): 12-week cohort with auto-reg tracking, standardized testing (1RM/submax), group skill sessions, mobility clinics. Tools: membership LMS, velocity devices (optional), scheduled testing. Metrics: cohort median improvement, retention rate, injury incidence. Trigger: cohort-level drop in adherence or injury clusters prompting program redesign.
- Enterprise: Longitudinal athlete management with periodization across seasons, diagnostics (DEXA, VO2max), and multidisciplinary team (nutrition, physio). Tools: LMS + EHR integration, lab scheduling, performance dashboards. Metrics: longitudinal strength curves, body composition trends, injury-adjusted availability. Trigger: performance metric decline across quarter or medical flags — convene multidisciplinary review.

## Anti-Hallucination
- [VERIFIED] 5/3/1 and 5x5 are established periodization templates with community and literature support.
- [COMMON-PRACTICE] RPE-based autoregulation is widely used in strength coaching.
- [INFERRED] Load increments assume standard barbells and fractional plates available.
- [UNKNOWN] Specific clinical contraindications require provider input.
