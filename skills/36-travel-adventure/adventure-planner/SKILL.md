---
name: adventure-planner
description: "Use when designing adventure travel and experience progression. Handles adventure-type selection, skill pathways, gear frameworks, risk matrices and expedition logistics. Do NOT use for extreme or professional expedition (Everest/Antarctica) planning."
license: MIT
author: Sandeep Kumar Penchala
type: travel-adventure
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [trekking, mountaineering, diving, risk-management, gear, expedition, backcountry]
token_budget: 4000
chain: |
  - required_checks: [fitness-assessment, permit-list, emergency-contact]
  - max_group_size_per-guide: 8
  - evacuation_threshold_meters: 6000
---

# Adventure Planner — Portability target: outdoor enthusiasts, small expedition leaders

<!-- QUICK: 30s --> One-liner: A tactical adventure design system that maps adventure types to skill paths, prescriptive gear frameworks (buy vs rent), fitness timelines, permit logistics and a risk-assessment matrix tailored for remote-field travel.

## RESEARCH_PREREQUISITE

| Key | Requirement |
| --- | --- |
| RP1 | Local permitting authorities & season windows |
| RP2 | Rescue & evacuation options (local SAR contacts) |
| RP3 | Route beta & reliable topo/sea charts |
| RP4 | Weather climatology and microclimate seasonality |
| RP5 | Rental availability & prices (local shops) |
| RP6 | Medical & evacuation insurance scope |
| RP7 | Skill baseline for participant group |
| RP8 | Leave-No-Trace & local conservation rules |

> Note: copy verbatim RP1-RP8 as the minimum input set for the iterative research loop.

### Iterative Research Loop

| Iteration | Objective | Inputs | Output | Timebox |
| --- | --- | --- | --- | --- |
| 1 | Route selection | RP1, RP3, RP4 | Primary + alternate route with weather windows | 180m |
| 2 | Skill-gap analysis | RP7 | Training timeline per participant | 120m |
| 3 | Gear decision | RP5 | Buy vs rent matrix + budget | 90m |
| 4 | Permits & logistics | RP1, RP2 | Permit list, guide contact, emergency plan | 120m |
| 5 | Final risk mitigation | RP2, RP6 | Communication plan + med-evac triggers | 60m |

## Quickstart — 30 seconds

1. Identify adventure type (trek, dive, ski, surf) and target dates.
2. Run a binary rental vs buy check: rental price >30% of purchase price and infrequent use -> rent.
3. Contact local guide or ranger to confirm permit windows and current route hazards.

<!-- STANDARD: 3min --> Ground Rules & Mechanical Triggers

- Mechanical trigger: For any multi-day remote route, require two independent location-tracking devices (e.g., PLB + satellite messaging device like Garmin inReach).
- Mechanical trigger: If group average fitness < required threshold, enforce a minimum 6-week progressive conditioning program.
- Trigger: If worst-case evacuation cost estimate > 25% of budget, buy evacuation insurance with helicopter coverage.

## Decision Tree — Adventure Type & Logistics

Start
├─ Type? (Trek / Climb / Dive / Surf / Ski / Cycle / Kayak)
│  ├─ Trek: Multi-day? (Y/N)
│  │  ├─ Y: Remoteness > 2 days? (Y/N)
│  │  │  ├─ Y: Require permit + guide; identify resupply points (Y/N)
│  │  │  │  ├─ Y: Plan resupply logistics + cache points
│  │  │  │  └─ N: Carry full self-supported weeks' rations
│  │  │  └─ N: Local trail multi-day -> light logistics
│  │  └─ N: Local trail day plan -> check access & parking
│  ├─ Dive: Depth & certification? -> Open-water / Advanced / Tech
│  │  ├─ Tech or deep (>30m)? -> Require gas mixes & deco plan
│  │  └─ Recreational -> check local refills & recompression chamber proximity
│  ├─ Climb: Altitude & grade -> Alpine vs rock -> gear list
│  │  ├─ Altitude >4,000m? -> Add acclimatization schedule
│  │  └─ Rock only -> bolt & anchor info + rescue access
│  └─ Water: Flow & season -> river classification or sea-state threshold
│     ├─ River class >= IV -> vetted guide + throw bag + spare paddle
│     └─ Coastal surf -> check swell window & local rip policies
└─ Risk tolerance? (low/medium/high)
   ├─ Low: Use certified guide + commercial route; insurance mandatory
   ├─ Medium: Hybrid leader + certified local partner; carry PLB
   └─ High: Self-supported with redundancy and local permits; require team leader with nav/med cert

Add decision nodes for logistics & cost tradeoffs
├─ Cost constraint? -> Willing to pay for guide? (Y/N)
│  ├─ Y: Prioritize licensed operator with liability insurance
│  └─ N: Plan for self-supported with higher contingency budget (20–30%)
├─ Time constraint? -> Tight window? (Y/N)
│  ├─ Y: Choose shorter, high-probability routes
│  └─ N: Use longer acclimatization-friendly itineraries
├─ Evacuation complexity high? -> Pre-contract med-evac or HEMS


Start
├─ Type? (Trek / Climb / Dive / Surf / Ski / Cycle / Kayak)
│  ├─ Trek: Multi-day? (Y/N)
│  │  ├─ Y: Require permit + guide if remoteness > 2 days
│  │  └─ N: Local trail day plan
│  ├─ Dive: Depth & certification? -> Open-water / Advanced / Tech
│  ├─ Climb: Altitude & grade -> Alpine vs rock -> gear list
│  └─ Water: Flow & season -> river classification or sea-state threshold
└─ Risk tolerance? (low/medium/high)
   ├─ Low: Use certified guide + commercial route
   ├─ Medium: Hybrid leader + certified local partner
   └─ High: Self-supported with redundancy and local permits

## Core Workflow (STANDARD / DEEP)

1. Adventure selection (STANDARD): Map participant goals to adventure type.
2. Skill progression (DEEP): Build a 12–52 week curriculum: baseline assessment, core skills, scenario drills, culminating field test.
3. Gear strategy (DEEP): Apply "Buy Once Cry Once" — choose lifetime-grade items for load-bearing and rental for specialty/seasonal items.
4. Permits & guide contracting (STANDARD): Book permits; secure guide with local SAR insurance.
5. Risk assessment & comms (DEEP): Fill risk matrix, set evacuation triggers, create call/response plan.
6. Field logistics (STANDARD): Daily meal plan, water strategy, cache points, campsite selection.
7. After-action & storytelling (STANDARD): Debrief, media curation, leave-no-trace report.

<!-- DEEP: 10+min --> War Stories, Failure Narratives, Expert Hacks

- Failure narrative: In a multi-day New Zealand traverse, the party relied on a single smartphone map; a drained battery and sudden fog left them off-route. Outcome: emergency bivouac. Lesson: always carry physical map + compass and power redundancy (solar panel + battery bank).
- War story: For a Baja diving expedition, surface support underestimated nitrogen loading after multiple dives. Outcome: one diver required oxygen and a diversion to La Paz for recompression therapy. Fix: implement strict dive-log discipline, conservative no-fly buffers (minimum 24–48h depending on profile), and mandatory buddy checks with dive-computer conservative settings.
- Expert hack: For alpine start efficiency, pre-pack a "summit kit" in a dedicated drybag with fastest-access items (headlamp, crampon straps, emergency bivvy). Place it on top of the pack and set an alarm for departure 30 min earlier to reduce exposure to afternoon weather.
- Tactical equipment tip: For ultralight multi-day treks, replace bulky foam pads with high-R-value inflatable pads (R-value 3.5+) and use a 3-season sleeping bag plus a micro-bivy. Test the system at home in a cold night to validate thermal comfort.

Expanded failure narratives & edge cases:

- Permit quota miss: In Nepal's Annapurna region, a small party attempted a last-minute trek without securing TIMS permits and Annapurna Conservation Area entry; park rangers redirected them, costing two days extra and $250 in expedited permits. Lesson: monitor permit windows and local quota apps; hire a licensed agency when quotas are enforced.

- Altitude shock edge-case: A group attempted Kilimanjaro with only a 3-day acclimatization window; two members developed AMS requiring descent. Cost of guided evacuation and lost nonrefundable fees exceeded $4,000. Lesson: adopt agreed acclimatization schedule (7-day Lemosho or Machame-style), include at least one extra acclimatization night, and train participants with stair/pack sessions.

- Weather corridor collapse: In Patagonia, sudden westerly storms closed the only valley pass; a rescue helicopter could not land for 36 hours. Lesson: always have two egress routes and pre-identified shelter locations with food caches.

Advanced strategies & expert hacks:

- Training-to-performance mapping: Turn fitness tests into pass/fail gates. Example: for a 6,000m peak, require a 3-hour loaded hike (20kg) with 800–1,000m elevation gain within 6 weeks of departure. Use time-to-ascent metrics as selection thresholds.
- Local guide economics: In Nepal, hiring a certified guide for 7-day trek (licensed) can cost $200–400 plus permits — often cheaper than rescheduling fees for permit issues. For islands, local skippers often demand 30–40% deposit; use escrow or reputable operator marketplaces (e.g., PADI-affiliated centers).
- Weather window exploitation: Use long-range ECMWF/GFS + local METAR trends to select start dates that minimize monsoon/jet-stream impact; for avalanche-prone slopes, seek AIARE reports and recent snowpack bulletins.

Country-specific case studies (with numbers):

- Kilimanjaro (Marangu vs Lemosho): Typical operator cost $1,200–$3,000 (guides, park fees, park rescue levy). Fitness prep: 2 months minimum, 3x/week stair hikes with 30lb pack, one 5–8 mile hike per week. Permits and park fees typically $800–$1,200 of total cost.

- Patagonia multi-day trek (Torres del Paine W): Local park fee ~$30; refugio beds $40–$120/night; guided package 5-day ~$1,200–$2,000. Edge-case weather reroute can increase transport costs by $200–$600 per person in remote seasons.

- Scuba liveaboard in the Philippines: Liveaboard week (7 nights) $1,000–$2,000 including dives; emergency evacuation to Manila hospitals can exceed $10,000 without insurance. Enforce DAN/Global Underwater Evac plan and local recompression chamber proximity checks.



## Error Decoder — Specific Pitfalls

| Symptom | Root cause | Signal | Fix |
| --- | --- | --- | --- |
| Group pace splits | Poor baseline fitness or uneven training | Split groups > 30 min; frequent rest stops | Re-plan with staggered start + additional local guide; set bailout points every 6 hours and enforce turnaround times
| Water contamination in remote rivers | No treatment or improper filter maintenance | GI upset within 24–72h or cloudy output | Carry dual treatment: gravity filter + chemical drops (Katadyn + Aquatabs); periodically backflush filters; test water at base
| Local permit denial | Incomplete docs, quota filled, or local policy change | Email or Ranger notice; denied access on arrival | Maintain scanned docs, apply earlier, hire local licensed outfitter with quota access
| Rental gear mismatch | Wrong sizing, degraded kit, or shop inventory errors | Ill-fitting harness/boots; shop cannot replace at remote location | Ship or courier pre-checked spare; buy fit-critical items (boots, harness) and rent the rest
| Evacuation delay | Weather, logistics, or permit constraints | SARETA > 12h; medevac denied due to weather | Pre-buy HEMS or med-evac policy; identify ground-evac routes; pre-share ETA windows with SAR
| Altitude illness cluster | Rapid ascent profile without acclimatization | Multiple participants report headache/nausea above 3,000m | Enforce halt & descend protocols; carry pulse oximeter; include acetazolamide protocol per med guidance
| Dive-related decompression incident | Profile miscalculation or multiple repetitive dives | Diver symptoms post-dive; dizziness, numbness | Immediate O2, emergency recompression logistics, plan for diversion to nearest chamber; log and report to DAN
| Weather-driven route closure | Sudden storms, avalanches, or floods | Trail closure notices, river level rises | Activate alternate-route plan; hold shelter caches and extend contingency days
| Communications blackout | Satellite or local coverage failure | No messages after expected check-in window | Send PLB / activate SOS protocols; guide initiates local search plan


## Best Practices (Opinionated)

1. Use the 3-device rule: primary comms (satellite messenger like Garmin inReach), backup (mobile with local eSIM) and a short-range radio/whistle. Test all devices 72h before departure.
2. Buy lifetime-grade footwear and load-bearing items; rent bulky seasonal gear (skis, inflatable kayaks). Budget 30% of gear spend on footwear and pack.
3. Train to the event with progressive overload and specificity: for trekking, 3x/week hikes with weighted pack increasing 5% load weekly; for climbing, 2 strength + 2 technical sessions weekly.
4. Keep a 20% gear redundancy budget and a small spares bag (extra leash, inner tube, crampon strap, duct tape, multi-tool).
5. Use conservative margins: plan for the 75th percentile of transit time and 90th percentile of weather disruption; add 1–2 contingency days per week of remote travel.
6. Document and rehearse emergency evacuation: list med-evac insurer, claim number, nearest HEMS base, evacuation cost cap (verify $ limits), and practice the call flow.
7. Apply Leave No Trace at expedition scale: human waste protocol, fuel stove fuel transfer, pack-out policy; record waste handling plan in team brief.
8. Use modular meal planning: 300–450 kcal per meal with 20% calorie buffer for high-exertion days; plan for 3,500–5,000 kcal/day on heavy alpine days.
9. Camera & data protocol: two storage redundancies (on-device + encrypted SSD) and daily media ingest routine; budget 1TB SSD per 7–10 days of RAW shooting.
10. Financial contingency: set aside 15–30% of trip budget for medevac, resupply, or forced itinerary changes; pre-load local currency equal to 48h expenses.

## Production Checklist

- [ ] Route topo and charts downloaded and printed; digital copies on GPS and offline maps
- [ ] Permits applied, confirmed, and receipt copies saved (PDF + print)
- [ ] Satellite messenger (PLB or Garmin inReach) + battery bank tested for 48h
- [ ] Evacuation insurance with HEMS coverage purchased and policy number recorded
- [ ] Group fitness baseline recorded and training schedule assigned with milestones
- [ ] Guide/porter contracts with contact, insurance, and cancellation terms confirmed
- [ ] Gear list split into personal vs group kit; color-code shared items
- [ ] Water treatment plan tested in local tap sample; carry filter + chemical backup
- [ ] Food & resupply points mapped with calorie counts and emergency rations
- [ ] Fuel management plan for stoves and resupply options (spares stored)
- [ ] Leave-No-Trace checklist reviewed and responsibilities assigned to team members
- [ ] Local SAR contact, embassy/consulate info, and local health facility locations saved
- [ ] Durable medical records & medications list with dosages and storage notes
- [ ] Communications plan with check-in cadence and failure escalation flow


## Concrete Templates

1) Risk Assessment Template (columns)
- Hazard | Likelihood (1–5) | Consequence (1–5) | Risk score | Mitigation | Residual risk | Responsible

2) 12-week Trek Conditioning Plan (sample)
Weeks 1–4: Base endurance (3 runs/week, 1 long hike) — target: 60–90 min continuous
Weeks 5–8: Load progression (weighted hikes, stair training) — target: 2x/week with 10–20% added pack weight each 2 weeks
Weeks 9–12: Specificity (terrain, night-hike, simulation 2-day hike) — simulate elevation gain and 12–16 hour days

3) Fitness benchmarks by adventure type (concrete)
- Kilimanjaro (3,900–5,895m): 2 months prep, 3x/week stair-hike with 30 lb pack; 5–8 mile hike with 800m gain sim 1x/week; target resting HR recovery < 60s after 3-min step test
- Technical rock climb multi-pitch: 12 weeks, 2x/week strength (pulling/pushing), 2x/week technique (toprope/lead practice), single-pitch endurance test: climb 500m total in a day
- Sea kayaking multi-day: 8–12 weeks paddling, 2x/week long endurance paddle 2–4 hours, capsize & re-entry drills every 3 weeks
- Backcountry skiing: 10–12 weeks aerobic + plyometric training; carry 15–20kg pack for distance endurance; avalanche course recommended

4) Gear decision table
- Item | Buy price | Rent price per day | Frequency of use | Decision (Buy/Rent) | Notes | Replacement plan

5) Expedition packing list template (modular)
- Personal kit: boots, base layers, insulating layer, shell, socks (4 pairs), gaiters
- Group kit: stoves, fuel canisters, shelter tarp, repair kit
- Safety kit: PLB, first aid, spare batteries, bivvy
- Media kit: single camera + 1 backup storage device

6) Backcountry meal plan example (3 days)
- Day 1: Breakfast 500 kcal (instant oats + powdered milk), Lunch 600 kcal (wraps + nuts), Dinner 900 kcal (dehydrated meal + olive oil)
- Day 2: Similar with increased carbs before long day; Day 3: high-calorie recovery meal
- Water: Plan 3L/day + 1L buffer; treat with filter + chemical backup (2% iodine tablets)

7) Risk Assessment sample row
- Hazard: River crossing | Likelihood: 3 | Consequence: 5 | Risk score: 15 | Mitigation: Scout crossing + rope belay | Residual risk: 6 | Responsible: Trip leader

8) Navigation rehearsal template
- Day/time | Route leg | Backup navigation method | Check-in schedule | Bailout points

9) Emergency communication script
- "Mayday" template, PLB activation steps, local SAR contact numbers, on-site medic duties and transport plan

10) After-action report template
- Timeline of events, decisions made, deviations from plan, equipment failures, injuries, lessons learned, media attach


## Verification

- Tests: Full-system rehearsal day: load gear, run communication checks, execute navigation leg with GPS+map only.
- KPI: Average group pace matches baseline within ±10%; hydration & calories on plan; zero infractions on Leave-No-Trace.
- Acceptance: Guide signs off on readiness and SAR has pre-alerted if remoteness index >8/10.

## Cross-Skill Coordination

| Skill | Role | Handoff Data |
| --- | --- | --- |
| travel-designer | Trip cluster & transport | Transfer points, arrival windows, buffer days |
| medical-officer | Health screening | Participant medical forms & evacuation triggers |
| logistics-manager | Resupply & shipping | Courier addresses, resupply calendars |
| photography-editor | Media curation | RAW folder + metadata timeline |

## What Good Looks Like

- A five-day alpine trek where all participants complete the route, there are no unplanned evacuations, all permits are validated on arrival, and post-trip debrief documents lessons + media packaged within 48h.

## References & Tools

- Garmin inReach (satellite comms)
- PADI course lists and dive tables (padi.org)
- Leave No Trace Center for Outdoor Ethics (lnt.org)
- Wilderness Medical Society (wms.org)
- REI Co-op expert advice & rental listings (rei.com)
- Mountain Safety Council / local ranger offices

## Scale Depth

- Solo: Self-supported with stringent redundancy and conservative weather margins.
- Small (2–6): Hire 1 local guide; share group kit and communications.
- Medium (7–15): Contract 2–3 guides or local company; permit quotas may require group split.
- Enterprise (expedition-style): Use a logistics company, local agency for permits, full medic on team.

## Anti-Hallucination

- Always verify medical advice and evacuation coverage directly with insurers; confirm guides' certifications with issuing bodies; check tide and current tables from official hydrographic services for water-based adventures. Avoid relying on single anecdotal trip reports for route safety.
