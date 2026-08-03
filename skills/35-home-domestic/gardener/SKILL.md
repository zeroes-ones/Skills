---
name: gardener
description: "Use when you want a practical home-gardening system: garden planning, soil health, seasonal vegetable calendars, container strategies, water-wise irrigation, IPM pest control, seed starting and saving. Handles templates and planting calendars. Do NOT use for commercial farming or large-scale agriculture."
license: MIT
author: Sandeep Kumar Penchala
type: home-domestic
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [gardening, soil, vegetables, water-wise, compost]
token_budget: 4000
chain: |
  iterative: plan -> test -> amend
---

# Gardener — portability: balcony / raised bed / backyard

<!-- QUICK: 30s --> One-liner: Plan and build a productive, low-water home garden using sun-mapping, soil testing, composting, seasonal templates, and IPM to produce continuous harvests with minimal synthetic inputs.

## RESEARCH_PREREQUISITE
RP1-RP8 table (copy verbatim)


### Iterative Research Loop
| Step | Action | Artifact |
|---|---|---|
| Map | Sun map 7 days, soil sample | Sun map PNG, soil test pdf |
| Hypothesis | Which beds suit what crop | Plant list by bed |
| Prototype | Plant small succession row | Harvest log |
| Measure | Yield per sq ft, water use | Yield spreadsheet |
| Iterate | Amend soil and schedule | Updated bed plan |


Quickstart (30s):
1) Sun map: note 3 points of sun at 9am, 1pm, 5pm for 7 days.
2) Soil test: collect 6 subsamples 6" deep, mix, send to lab or use DIY kit (pH, NPK).
3) Build 1 raised bed 4'x4' with 30cm depth; fill with 40% topsoil, 40% compost, 20% coarse sand or grit for drainage.

<!-- STANDARD: 3min --> Ground Rules (mechanical triggers):
- Trigger A: "Water check" — soil probe > 2" dry at root zone -> water with drip at 2 L/hr for 30–60 min per 1 sq ft depending on soil texture.
- Trigger B: "Pest scouting" — weekly 10-min walk: inspect 10 plants per bed for chewed leaves, eggs, or aphid colonies.
- Trigger C: "Succession" — sow new row every 2 weeks for cool-season crops, every 3–4 weeks for warm-season transplants.

Decision Tree (4 levels):
```
Weed / Pest / Deficiency observed
├─ Is pest visible? -> Yes -> Identify (aphid, caterpillar, slug) -> IPM step
│   └─ No -> Check soil moisture -> pH or nutrient deficiency test
├─ Is crop stunted? -> Check root health and drainage -> amend with compost tea and aerate
└─ Is harvest low? -> Adjust succession plan, increase planting density, inoculate with mycorrhizae
```

Core Workflow (STANDARD)
1. Plan: space, companion planting, rotate families per bed each season.
2. Prepare: test and amend soil in fall with 2–3" compost and 1 kg kelp meal per 10 sq ft.
3. Plant: timing per zone calendar; label rows with seed date and variety.
4. Maintain: weekly watering, mulching, pest scouting.
5. Harvest & Store: process produce, blanch and freeze or preserve; update seed bank with save details.

Core Workflow (DEEP)
- Soil biology protocol: inoculate new beds with 100–200 mL aerobic compost tea per plant monthly during establishment; add 1 tsp mycorrhizal granules per transplant root ball.
- Irrigation calibration: time-to-wet test: run drip valve for 20 min and measure soil moisture at 0–6" and 6–12" depths; adjust run time until 60% field capacity achieved at root zone.

<!-- DEEP: 10+min --> War stories, failure narratives, expert techniques:
- Failure: new blueberry bush died — cause: pH 7.2; fix: acidify soil with sulfur 50 g per sq ft and top-dress with ericaceous compost; re-test in 3 months.
- Technique: seed-start staging — use 1020 flats, 128-cell tray for microgreens; bottom heat 20–25°C for tomatoes and peppers; use 18/6 light schedule at 300–400 µmol/m²/s for seedlings.
- Pest control story: tomato hornworm outbreak controlled by night scouting with flashlight; removed by hand and placed in bucket of soapy water; followed by Bacillus thuringiensis kurstaki (Btk) spray at label rate for remaining larvae.
- Composting fail: anaerobic odor and pests — fix: turn pile weekly, add dry carbon (shredded paper), monitor C:N ~ 25–30:1, maintain 55–65°C for pathogen kill.

Error Decoder
| Symptom | Likely Cause | Fix |
|---|---:|---|
| Yellow lower leaves | Nitrogen deficiency or waterlogging | Apply compost tea or 5-5-5 granular, correct drainage |
| Wilting midday | Transpiration stress, root damage | Check irrigation schedule, inspect roots |
| Holes in leaves | Slugs/caterpillars/snails | Handpick at dusk, set beer traps, use iron phosphate bait |
| Powdery mildew | High humidity + low airflow | Prune for airflow, apply potassium bicarbonate spray |
| Poor germination | Old seed or cold soil | Increase soil temp, viability test, fresh seed |

Best Practices (opinionated)
1. Build beds in 4' widths to allow reach from both sides; use 12–18" paths with permeable material.
2. Rotate families: Solanaceae -> Cucurbitaceae -> Brassicaceae -> Legumes to reduce disease build-up.
3. Use 3" mulch (straw or wood chips) to suppress weeds and reduce evaporation.
4. Compost C:N target ~25:1; grind coarse material to 2–4 cm pieces to speed breakdown.
5. Water early morning for 20–40 min depending on emitter flow, avoid evening watering to reduce leaf disease.
6. Keep seed packets labeled with source, lot, and germination test date; replace if germination <70%.
7. Use floating row cover for brassicas early-season to block flea beetles; remove during flowering for pollinators.
8. Introduce beneficials: plant buckwheat and alyssum for hoverfly and parasitoid wasp habitat.
9. Test pH annually: vegetable optimum pH 6.2–6.8; adjust with lime or sulfur accordingly.
10. Save seeds only from open-pollinated varieties and isolate by distance or timing to maintain varietal purity.

Production Checklist (binary)
- [ ] Sun map completed
- [ ] Soil test completed
- [ ] Raised bed dimensions measured and secured
- [ ] Compost available (bags or on-site)
- [ ] Irrigation set up and calibrated
- [ ] Mulch on top of beds (3")
- [ ] Pest scouting schedule set in calendar
- [ ] Seed starting heat mat and lights functional
- [ ] Seed inventory logged with germ dates
- [ ] Harvest log template ready
- [ ] Seed-saving kit prepared (paper envelopes, labels)
- [ ] Garden tools cleaned and stored
- [ ] Winterize plan scheduled

Concrete Protocols / Recipes
Protocol: 4'x4' Raised Bed Mix (30 cm depth)
- Materials: 40% screened topsoil (48 L), 40% mature compost (48 L), 20% coarse sand or horticultural grit (24 L), 1 kg well-rotted manure per bed, 150 g bone meal or rock phosphate for P, 100 g kelp meal.
- Steps: mix on tarp until homogeneous; fill bed; water to settle; top-dress 50g granular balanced fertilizer per 4 sq ft at planting.

Protocol: Compost Tea (aerated)
- Equipment: 10-gallon food-grade bucket, aquarium air pump (10W), airline tubing, 1/4 cup unsulfured molasses, 1 cup well-aged compost, thermometer.
- Steps: fill bucket with dechlorinated water, add compost in mesh bag, add molasses, aerate 24–36 hours maintaining 20–25°C; apply diluted 1:5 to soil at transplant and monthly.

Verification
- Yield targets: per 4'x4' bed aim for 10–15 lbs of mixed salad greens per month in prime season.
- Water-use: track liters per 4'x4' per week; aim to reduce by 20% year-over-year with mulch and drip.
- Soil health: increase organic matter by 1% annually via compost and cover cropping.

Cross-Skill Coordination
| Skill | Coordinate with | How |
|---|---|---|
| home-chef | harvest schedule | coordinate fresh herbs and veg timing with menu plan |
| home-organizer | storage | design produce storage for shelf life (perforated bins) |
| interior-designer | edible landscaping | integrate productive plants into front-yard aesthetics |

What Good Looks Like
- Continuous harvest windows with staggered succession, minimal pest outbreaks (few manual removals per week), and soil tests showing pH in target range and organic matter > 5%.
- Seed bank with >80% viability for last year's saved seeds.

References
1. "All New Square Foot Gardening" — Mel Bartholomew
2. "The Vegetable Gardener's Bible" — Edward C. Smith
3. "Teaming with Microbes" — Jeff Lowenfels & Wayne Lewis
4. "The Rodale Book of Composting" — Grace Gershuny & Joe Smillie
5. "Carrots Love Tomatoes" — Louise Riotte (companion planting)
6. "Seed to Seed" — Suzanne Ashworth (seed saving)
7. "The Organic No-Till Farming Revolution" — Andrew Mechnikov (small scale adaptations)
8. Local extension service soil test guides (university extension)

Scale Depth
- Solo: balcony container system with 4–6 12" pots, automated drip micro-irrigation.
- Small household: 2–4 raised beds, small greenhouse for season extension, shared harvest planning.
- Medium: 8–12 beds, drip tape grid, composting hub, volunteer management.
- Enterprise (not applicable): transition to consulting; not for commercial agriculture.

Anti-Hallucination
- All fertilizer and amendment rates are listed by weight/area. When in doubt about disease ID, consult local extension or lab-tested diagnosis before applying treatments. For pesticide suggestions, always follow label rates and local regulations.
