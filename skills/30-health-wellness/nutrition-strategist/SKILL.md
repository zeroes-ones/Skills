---
name: nutrition-strategist
description: "Use when you need practical, evidence-based nutrition strategies. Handles macros by goal, micronutrient adequacy, dietary frameworks, supplement evidence review, hydration, and gut-support. Do NOT use for clinical nutrition therapy or eating disorder treatment."
license: MIT
author: Sandeep Kumar Penchala
type: health-wellness
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [nutrition, macros, supplements, hydration, gut-health, meal-planning, metabolic-health]
token_budget: 4000
chain:
  consumes_from: [habit-engineer]
  feeds_into: [fitness-programmer, longevity-biohacker]
  alternatives: [registered-dietitian, clinical-nutritionist]
---

# Nutrition Strategist
Portability: universal (text + CSV/JSON output)

<!-- QUICK: 30s -->
One-liner: Generate a goal-aligned nutrition plan with calorie & macro targets, supplement recommendations, and micronutrient checklists.

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
| RP8 | Consent to non-clinical nutrition guidance |

### Iterative Research Loop
| Loop | Objective | Output |
| --- | --- | --- |
| Loop 0 | Collect goals & constraints | Calorie intent (cut/maintain/bulk), dietary restrictions |
| Loop 1 | Estimate energy needs | TDEE estimate + activity multiplier; initial calorie target |
| Loop 2 | Macro allocation | Protein/fat/carbs split by goal and training load |
| Loop 3 | Micronutrient & supplement plan | Food-first micronutrient checklist and evidence-backed supplements |

## Quickstart (30s)
1. Ask: goal (cut/maintain/bulk), activity level, allergies, preferred diet framework.
2. Calculate BMR (Mifflin-St Jeor) and TDEE with chosen multiplier.
3. Output: Calorie target and macros (protein 1.6–2.2 g/kg; fats 20–35% kcal; remainder carbs).

<!-- STANDARD: 3min -->
## Ground rules
- Conservative deficits: 10–20% for sustainable fat loss; aggressive only with clinical oversight.
- Protein targets: 1.6–2.2 g/kg for most active adults; higher for calorie deficits.
- Hydration: ~30–35 ml/kg/day baseline; adjust for exercise and climate.

## Decision Tree
Start
├─ Clinical conditions? -> Refer to registered dietitian (out of scope)
├─ Goal = Cut? -> Set -10 to -20% calorie deficit, maintain protein high
├─ Goal = Bulk? -> Set +5 to +15% surplus, prioritize protein + progressive overload
└─ Plant-based preference? -> Adjust protein sources and B12/D3 supplementation

<!-- STANDARD: 3min -->
## Core Workflow
1) Intake & triage (Loop 0) <!-- STANDARD: 3min -->
- Capture dietary preferences, intolerances, meal timing, and prior dieting history.

2) Energy needs & targets (Loop 1) <!-- STANDARD: 3min -->
- BMR (Mifflin-St Jeor): Men: 10*kg + 6.25*cm -5*age +5; Women: 10*kg + 6.25*cm -5*age -161.
- TDEE multiplier: sedentary 1.2, light 1.375, moderate 1.55, active 1.725, very active 1.9.

3) Macro allocation (Loop 2) <!-- DEEP: 10+min -->
- Protein: 1.6–2.2 g/kg (higher for deficit/higher training loads). War story: a client on 1.0 g/kg lost strength rapidly during a 12-week cut; increasing to 2.0 g/kg and adding timed protein at breakfast and peri-workout restored performance and preserved lean mass.
- Fats: 20–35% kcal (min 0.5 g/kg). Edge case: very-low-fat diets (<15%) can reduce testosterone in males—monitor levels if sustained below 20% kcal.
- Carbs: remaining kcal to support training; prioritize peri-workout carbs (0.5–1.0 g/kg pre, 0.5–1.5 g/kg post for intense sessions) for high-intensity training. For endurance athletes, increase to 6–10 g/kg/day during heavy volume weeks.
- Timing & distribution: aim for 3–5 protein-containing meals with 20–40 g protein each to maximize MPS; prioritize 0.3–0.4 g/kg protein within 1–2 hours post-workout.

4) Micronutrients & supplements (Loop 3) <!-- DEEP: 10+min -->
- Vitamin D: screen; supplement 1000–4000 IU/day if deficient (verify with blood 25(OH)D). Failure narrative: athlete supplemented 2000 IU without testing and remained deficient—order labs before long-term dosing.
- Creatine monohydrate: 3–5 g/day maintenance; optional 20g/day loading x5–7 days. Evidence: robust for strength/hypertrophy; safe in healthy adults.
- Omega-3 EPA+DHA: 1–3 g/day for general health; higher doses for TG lowering under clinician oversight.
- Protein powder: 20–40g serving to reach protein targets when whole food insufficient; choose whey for rapid leucine delivery, plant blends for vegan needs.
- Iron/B12: screen when plant-based or with heavy menstrual bleeding; iron therapy requires labs and clinical guidance—do not empirically dose high iron without tests.
- Magnesium: 200–400 mg (glycinate or citrate) for sleep/muscle relaxation when deficient; check renal function in at-risk groups.
- Supplement interactions & safety: review medication interactions (e.g., vitamin K and warfarin) and renal/hepatic contraindications. Document all supplements and review quarterly.
- Gut-support: recommend fiber diversity (25–40 g/day mixed soluble/insoluble) and fermented foods (1 serving/day) for microbiome health; introduce fiber increases gradually to avoid GI upset.


## Meal planning templates
- Cut example: 25 kcal/kg/day baseline -> -15% = target. Protein 2.0 g/kg, fats 25% kcal, carbs remainder.
- Bulk example: +10% kcal, protein 1.8 g/kg, fat 25–30% kcal.
- Time-restricted feeding: 16:8 can assist adherence; ensure total calories met.

## Error Decoder
| Error Message / Pitfall | Root Cause | Fix | Lesson |
| --- | --- | --- | --- |
| Rapid weight loss with disproportionate strength loss | Aggressive deficit (>20%), protein <1.4 g/kg, high cardio | Increase calories modestly, protein to 1.6–2.2 g/kg, reduce high-intensity cardio; add targeted refeeds once/week | Preserve lean mass by prioritizing protein and strength work during cuts |
| Micronutrient gaps (iron, B12, vitamin D) | Plant-based diet, low variety, or inadequate sun exposure | Order labs (ferritin, B12, 25-OH D), supplement per results, increase food sources (legumes, fortified foods) | Test before supplementing high-dose micronutrients |
| Poor training performance on heavy days | Low peri-workout carbs or inconsistent fueling | Increase carbs on heavy days (1–3 g/kg total day), add 20–40 g protein post-session | Align daily intake to training demands; periodize carbs by session intensity |
| Persistent GI distress after fiber increase | Rapid fiber change, high FODMAPs, or low gut diversity | Slow fiber increase over 2–4 weeks, swap high-FODMAP items, add probiotic/fermented foods trial | Gradual changes reduce GI side effects and improve adherence |
| Supplement adverse interaction (e.g., stimulant + caffeine) | Multiple stimulant products or high-dose pre-workouts | Review all supplements, remove overlapping stimulants, reduce caffeine timing | Central nervous system load can impair sleep and recovery—track timing and dose |
| Inconsistent weight despite adherence | Under-reporting intake, inaccurate portions, or metabolic adaptation | Implement weighed food logs for 7 days, estimate NEAT, adjust calories by 100–200 kcal | Accurate measurement resolves many apparent plateaus |
| Dehydration during endurance efforts | Inadequate electrolyte replacement and sodium loss | Prescribe 500–1000 ml fluid/h with electrolytes during long sessions; include sodium 300–700 mg/h depending on sweat rate | Match hydration strategy to sweat rate and environment |

## Best Practices
1. Prioritize protein distribution (20–40 g/meal) across 3–5 meals; aim for 0.3–0.4 g/kg per meal for muscle protein synthesis.
2. Periodize carbohydrates: low on light days (2–4 g/kg), high on heavy endurance or high-volume days (6–10 g/kg) for endurance athletes.
3. Use food-first micronutrient approach; check labs before prescribing high-dose supplements (vitamin D, iron).
4. Monitor weight and performance weekly; adjust calories 100–200 kcal and retest over 2 weeks before large changes.
5. Hydration baseline: 30–35 ml/kg/day, and during prolonged exercise use 300–700 mg sodium/hour depending on sweat rate.
6. Protein during deficit: maintain ≥1.6 g/kg; for aggressive cuts use 1.8–2.2 g/kg and include resistance training 2–3x/week.
7. Introduce fiber increases gradually (5 g/week) to target 25–40 g/day of mixed fibers to support gut diversity.
8. Supplement hierarchy: Level 1 (creatine, protein, vitamin D when deficient, omega-3); Level 2 (magnesium, probiotics); Level 3 (experimentals—use cautiously).
9. Use weighed food logs for 7–14 days when progress stalls; correct portion size assumptions before altering calories.
10. Favor Mediterranean-style patterns for long-term adherence but adapt to cultural preferences for sustainability.

## Production Checklist
- [ ] Goal confirmed (cut/maintain/bulk + timeline)
- [ ] BMR & TDEE calculated and documented
- [ ] Macro targets set with meal-level distribution
- [ ] Supplement recommendations with doses and safety notes
- [ ] Micronutrient checklist & food sources provided
- [ ] 7-day weighed food log planned or received
- [ ] Labs ordered if indicated (25-OH D, ferritin, B12, fasting glucose, lipid panel)
- [ ] Hydration targets set (baseline ml/kg/day + exercise adjustments)
- [ ] Refeed/refuel strategy scheduled for heavy training blocks
- [ ] Allergy/intolerance checklist completed
- [ ] Grocery/shopping list and sample meal plan provided
- [ ] Monitoring cadence set (weekly weight/performance checks)
- [ ] Handoff requested to fitness-programmer if training intensity changes
- [ ] Adherence supports assigned (habit-engineer tools, tracking app)

## Verification
- Confirm protein meets 1.6–2.2 g/kg.
- Confirm calorie delta aligns with goal (% deficit/surplus).
- Ensure meal plan fits stated eating window and preferences.

## Cross-Skill Coordination
| Skill | When to hand off | Payload |
| --- | --- | --- |
| fitness-programmer | When intensity or volume rises | Updated calorie needs, peri-workout macros, refeeds |
| habit-engineer | For adherence tools | Habit stack for meal prep, tracking and accountability |
| sleep-optimizer | When sleep affects appetite/recovery | Timing of meals around sleep, caffeine schedule adjustments |
| longevity-biohacker | For biomarker-driven nutrition | Lab targets (lipids, insulin), supplement risks/benefits |
| mental-fitness-coach | When emotional eating or disordered patterns appear | CBT-informed nutrition adherence strategies |

## What Good Looks Like
- Weight trajectory aligns with target (0.5–1% body weight/week for loss), preserved lean mass (maintain strength).
- Labs within range after intervention (vitamin D, lipids improvement where applicable).
- Adherence >80% over 8 weeks.

## References
- Mifflin MD, St Jeor ST, et al., "A new predictive equation for resting energy expenditure in healthy individuals," Am J Clin Nutr, 1990 (Mifflin-St Jeor).
- International Society of Sports Nutrition, "Position Stand: Protein and Exercise," J Int Soc Sports Nutr, 2017/2018.
- Kremer S., "Creatine supplementation review," Nutrients, 2019; meta-analyses supporting 3–5 g/day dosing.
- Estruch R., et al., "Primary prevention of cardiovascular disease with a Mediterranean diet," NEJM, 2013.
- EFSA/Endocrine Society guidance on vitamin D supplementation and monitoring (2016–2020 consensus docs).
- Slavin JL, "Dietary fiber and microbiota diversity trials," Nutrients review, 2013.
- Grgic J., et al., "Resistance training frequency and hypertrophy," Sports Med, 2018.

## Scale Depth
- Solo: One-off macro and meal plan with shopping list. Tools: template meal plans, sample recipes, simple calorie calculator. Metrics: weight trend over 2 weeks, meal adherence %. Trigger to escalate: <70% adherence after 2 weeks or undesired weight trend.
- Small: 8–12 week coaching with weekly check-ins and adjustments. Tools: tracking app, weekly weigh-ins, 2-week food logs. Metrics: weekly weight change, training performance, adherence. Trigger: plateau >2 weeks or labs outside target range.
- Medium: Lab integration and periodic re-calculation per mesocycle. Tools: ordered labs, dietitian integration, structured meal plans for phases. Metrics: biomarkers (25-OH D, ferritin), body composition, performance data. Trigger: biomarker abnormalities or failure to hit performance/weight targets.
- Enterprise: Multi-disciplinary care with RD, exercise, and clinical labs pipeline. Tools: EHR integration, automated lab alerts, cohort nutrition programming. Metrics: cohort-level adherence, health outcome KPIs, lab compliance rates. Trigger: population-level adverse trends or regulatory compliance needs.

## Anti-Hallucination
- [VERIFIED] Protein 1.6–2.2 g/kg is supported by ISSN consensus for active adults.
- [COMMON-PRACTICE] Creatine 3–5 g/day as safe, effective ergogenic aid.
- [INFERRED] Hydration 30–35 ml/kg/day is a baseline; adjust per individual.
- [UNKNOWN] Lab-specific cutoffs require clinician interpretation.
