---
name: home-chef
description: "Use when you want complete home-cooking mastery: kitchen setup, knife skills, 5 mother sauces, meal planning, flavor balancing, pantry systems, cooking methods, fermentation basics. Handles practical templates, recipes, and systems. Do NOT use for professional kitchen operations or food-business compliance."
license: MIT
author: Sandeep Kumar Penchala
type: home-domestic
status: stable
version: 1.0.0
updated: 2026-08-02
tags: [cooking, meal-planning, techniques, fermentation, pantry]
token_budget: 4000
chain: |
  iterative: technique-first, test, document
---

# Home Chef — portability: kitchen / stovetop / sous-vide

<!-- QUICK: 30s --> One-liner: Build a minimalist, high-output home kitchen and daily cook system using precise tools, five mother-sauce templates, and a weekly batch plan that yields fresh meals every day.

## RESEARCH_PREREQUISITE
RP1-RP8 table (copy verbatim)


### Iterative Research Loop
| Step | Action | Artifact |
|---|---|---|
| Observe | Track one week of meals, time, cost, and waste | Meal log CSV |
| Hypothesize | Pick one bottleneck to fix (e.g., prep time) | Hypothesis note |
| Prototype | Implement a 3-step change (mise, batch roast, sauce jar) | New schedule |
| Measure | Track changes for 7 days | Before/After metrics |
| Iterate | Keep winning changes, scrap losers | Versioned system |


Quickstart (30s):
1) Assemble: 8" chef's knife (German or Japanese), 10" skillet (cast iron), 12" stainless sauté pan, 6-qt Dutch oven, immersion blender.
2) Stock: kosher salt, kosher sugar, olive oil, neutral oil, white wine vinegar, canned tomatoes, chicken stock concentrate, dried pasta, rice.
3) Plan: print weekly template; pick 3 proteins, 4 veg sides, 2 starches; schedule two batch-cook sessions.

<!-- STANDARD: 3min --> Ground Rules (mechanical triggers):
- Trigger A: "Sunday prep" — 90-minute block: roast one tray of veg (425°F, 25–35 min), cook one grain (stovetop or rice cooker), braise one protein (2–3 hrs low), make one mother sauce jar.
- Trigger B: "Pantry low" — if any 5 staple items drop below threshold (salt, oil, canned tomatoes, stock, dry grain), add to shopping list automatically.
- Trigger C: "Night mise" — wash, chop, label, and refrigerate ingredients for next day before 10pm.

Decision Tree (6 levels):
```
Start
├─ Is this a planned dinner or emergency? -> Planned -> Follow weekly menu -> prep day schedule -> Execute batch-cook if scheduled
│   └─ Emergency -> Do I have 45+ minutes? (Y) -> Cook fresh sauté / roast -> Plate with fast sauce (pan jus or gremolata) -> Serve
│       └─ No -> Is there frozen prepared meal? (Y) -> Reheat: oven 160–180°C for even heat or pan-sear for crisp -> Serve
│           └─ No -> Pantry check: proteins (canned tuna/chicken), staples (pasta, rice), canned tomatoes
│               ├─ Pasta present -> Make aglio-anchovy-tomato or oil+chili sauce -> Serve
│               └─ Rice present -> Quick fried rice template (2 eggs, veg, soy, sesame) -> Serve
├─ Is entertaining required? -> (Y) -> Select menu for 60–70% make-ahead items -> Assign tasks: roast, sauce, garnish -> Set timeline T-3h/T-1h/T-10m
│   └─ No -> Weeknight routine -> 20–30 minute template: protein + veg + starch
│       ├─ Protein available raw -> Use 10–15 min pan-sear or 35–45 min roast depending cut
│       └─ Only leftovers -> Re-purpose into bowls/tacos/soup depending on texture
└─ Do we have dietary constraints? -> (Y) -> Check alternate pantry staples -> Balance macros with legume+grain template -> Note allergens on plate
    └─ No -> Default: seasonal veg + protein + acid/fat finish
```

Core Workflow (STANDARD)
1. Plan: Choose 3 proteins and 4 vegetables for week. Allocate 2 batch-cook sessions.
2. Shop: Use pantry-first shopping list; buy perishables for two days.
3. Batch-cook (DEEP): Roast tray veg, slow-braise protein, make 3 sauce jars (Béchamel, Velouté, Espagnole, Tomato, Hollandaise template variations), portion.
4. Daily assembly: 10–20 minute finish per meal: reheat protein, refresh veg with acid/fat, plate.

Core Workflow (DEEP)
- Mise steps with timings: sharpen knife (3 min), set 3 bowls for waste, wash veg (cold soak 5 min), preheat pans 2–5 min.
- Temperature control: pan heat levels mapped to tasks (med-high: sear, medium: sauté, low: simmer).

<!-- DEEP: 10+min --> War stories, failure narratives, expert techniques:
- Failure: sous-vide salmon turned mush from 130°F for 45 min; fix: reduce to 115–122°F for 20–30 min for tender, not flaky; finish with butter-sear 30s per side.
- Story: a home cook attempted all five mother sauces in one weekend; hollandaise repeatedly broke when held above 160°F. Recovery: cool to 140°F, whisk in one yolk tempered with 1 tbsp warm water off heat until emulsified, then gently re-warm over a bain-marie at 55–60°C. Lesson: time-box delicate emulsions and make hollandaise last.
- Technique: knife-chopping rhythm: 3-count push-chop cadence — position tip, rock, rotate, repeat; uniformity target: 6–8 mm dice for brunoise; practice on onion 7x per week. Advanced drill: 100 repeats of julienne→brunoise in under 5 minutes; track speed and accuracy with phone stopwatch and photo record.
- Sauces: mother-sauce rescue: when Béchamel splits, whisk in 1 tbsp cold milk plus 1 tbsp clarified butter off heat, then return to low heat. For broken emulsions (Hollandaise/Mayonnaise) use warm water tempering: drop 1 tsp warm water while whisking vigorously or blend in a 1 tbsp paste of mustard + water as an emulsifier.
- Fermentation: failed kimchi slimy -> cause: inadequate salt-percent (should be 2–3% by weight of vegetables); rectify by weighing veg+salt next batch. Seasonal note: ferment slower in <60°F; extend timeline proportionally (double days at 55–60°F). Warm-season tip: keep below 75°F to avoid over-acidification.
- Failure: bread with large oven spring but gummy crumb — cause: underbaked core or too-steamy finish; fix: increase bake time by 5–10 min at 10–20°F lower, check internal temp 200–205°F for lean loaves. For enriched breads target 190–200°F.
- Advanced technique: pan-sauce reduction with controlled fond deglaze: after searing, add 60–80ml wine, scrape, reduce by 2/3, add 200ml stock and reduce to glaze; finish with 1 tsp cold butter for shine. Use a wide pan for faster evaporation and more concentrated flavor.
- Recovery method: scorched stock — skim off burned top if localized; if strong bitter taste, dilute with equal parts fresh stock and simmer with 1 raw peeled potato for 20 min to absorb off-notes, then strain.
- Seasonal adaptations: summer batch-cooking uses short braises (1–1.5 hr) and more fresh sauces (chimichurri, salsa verde) to avoid long oven heat; winter uses long braises (3+ hr) and one-pot oven roasts to economize heat.
- Expert practice: train palate weekly — cook the same simple vinaigrette (3:2:1 oil:acid:mustard) and adjust salt until you can blind-identify the acid type; log results and adjustments.
- Mise refinement: use color-coded cutting boards (red/protein, green/veg, brown/veggies, white/dairy) and keep a 10-cm safety buffer on counters; map space so each prep surface is within 1.2 m of stovetop or sink.
- Failure: over-reduction of tomato sauce leading to acidic burn — fix: add 1 tsp baking soda at low heat and stir until foaming stops (neutralizes acidity) then correct flavor with salt and a touch of sugar or fat.
- Advanced fermentation: sourdough temperature control — aim for 24–26°C for mature starter activity; for longer fermentation maintain 18–20°C to favor acidity and complex flavors for overnight retards.
- Equipment tip: calibrate oven with 3-point test: place thermometers at front, middle, back; run at 180°C for 30 min and adjust offset. Note running offsets in an oven log.
- Food safety story: under-salted corned beef brine led to botulism risk when canning; always follow tested brine ratios and use pressure canning for low-acid meats.
- Advanced plating: use odd-numbered clusters, negative space (30–40% plate), and micro-herbs as 1–2 mm accent; use tweezers for precision.
- Seasonal sourcing: winter root-roasting template (mix carrot, parsnip, beet in 2:1:1 ratio, roast 200°C, 35–45 min, toss with 2 tbsp brown butter + 1 tbsp sherry vinegar).
- Failure recovery: broken vinaigrette — whisk with 1 tsp warm water and 1 tsp Dijon mustard, then slowly stream oil while whisking to re-emulsify.
- Practice regimen: set 3-month cycle — knife speed drills, sauce week, baking week, fermentation week — rotate and record failures and fixes in a cook log.



Error Decoder
| Symptom | Likely Cause | Fix |
|---|---:|---|
| Sauce broken | Fat emulsion separated or overheat | Off heat, whisk cold water/drop, emulsifier (egg yolk) or re-emulsify in blender with 1 tsp cold water |
| Meat dry | Overcooked or high temp | Lower cook temp, rest 5–10 min, baste with butter/oil, slice thin against grain |
| Bread dense | Under-proof or too much salt or weak flour | Increase proof time, do windowpane test, use higher-protein flour or autolyse for 20 min |
| Ferment off-odor | Contamination or insufficient salt | Discard if putrid; sanitize equipment, raise salt to 2–3% and manage temp 60–72°F |
| Bitter vegetables | Overcooked cruciferous veg at high temp | Blanch then shock, finish with acid and butter; add pinch of sugar if persistent |
| Sauce too thin | Insufficient reduction or roux undercooked | Reduce further, make beurre manié (butter+flour) and whisk in off-heat |
| Protein underdone | Inaccurate thermometer or cold core | Rest and finish in oven at 120–140°C with thermometer probe in center; calibrate probe in boiling water (should read 212°F / 100°C at sea level)
| Overly salty stew | Evaporation concentrated salt | Add unsalted liquid (stock/water), add raw potato to absorb salt for 10-15 min, or balance with acid and fat |
| Sticking to pan | Pan not hot enough or insulin on surface | Preheat pan for 2-4 min, dry protein surface, add fat when shimmering; use stainless vs nonstick accordingly |
| Gummy rice/pasta | Wrong water ratio or insufficient draining | Use 4-6x water for rice depending on variety; for pasta use plenty of water (4–5L per 500g) and salt, drain but reserve pasta water for sauce adjustment |


Best Practices (opinionated)
1. Master three knives: 8" chef, 2.5" paring, serrated 10" bread — keep edge angle 15–20° per side; hone daily for 10 strokes each side; sharpen with 1000/3000 grit stones monthly.
2. Use digital probe thermometer for proteins and check at thickest point: chicken 165°F, pork 145°F (rest 3 min), whole poultry 160–165°F, beef steaks 125–140°F depending doneness; calibrate probe quarterly.
3. Salt in layers by weight: use 0.9% for dough hydration, 1.5% for brining poultry (by water weight), 2.0–2.5% for lactic ferments; measure with kitchen scale.
4. Acid finish: always taste at end and add 1–2 tsp acid per 2–4 portions (1 tsp lemon juice ≈ 5ml) to brighten; for heavy dishes use 1 tbsp per 4 portions.
5. Control oil smoke: use refined oils (avocado, grapeseed) for searing; reserve extra-virgin olive oil for finishing and dressings; maintain pan surface temp records.
6. Batch-cook templates: roast veg at 200–220°C (400–425°F) for 20–40 min depending on cut; braise protein 140–160°C (285–325°F) for 2–6 hrs depending on cut.
7. Mise organization: left-to-right flow: wash → prep → cook → plate; maintain labeled bins: compost & trash & recycle; keep 1 small towel per station.
8. Reclaim & storage: freeze stock in 250ml and 1,000ml portions, leave 1cm headspace; label with date and recipe; rotate oldest-first; discard after 6 months for best flavor.
9. Fermentation safety and log: maintain 2–3% salt; record weight, salt grams, ambient temp and pH on day 0 and day 3; keep ferment between 60–72°F for controlled activity.
10. Waste reduction and cost control: clear-label leftover jars with date and intended use and suggested reuse recipe; target <5% weekly waste; use root-to-stem cooking for veg.
11. Temperature control: cold chain for perishables < 40°F (4°C) and freezer at -18°C; use fridge thermometer visible in food area.
12. Emulsions: when making vinaigrettes, aim 3:1 oil:acid ratio for average palates; when building mayonnaise use 1 yolk per 150–200ml oil as starting ratio.
13. Knife safety: maintain a 26 cm clear cutting zone; never catch a falling knife — step back; store knives in magnetic strip at 1.5m height recommended for households with children to avoid reach.
14. Pantry rotation: use FIFO for dry goods; keep opened beans and grains in airtight jars with desiccant packs; label with opened date and 6–12 month target shelf life.
15. Clean-as-you-go: wash one pot while another is simmering; schedule 10-minute post-cook cleanup so next meal prep is not bottlenecked.


Production Checklist (binary)
- [ ] Knife sharpened and honed today
- [ ] Pans preheated to intended temperature (test with water)
- [ ] Mise en place completed and staged in order of use
- [ ] Protein temperature probe calibrated and in tool drawer
- [ ] Pantry staples stocked (salt, oil, canned tomatoes, stock, grains) above threshold
- [ ] Batch sauces labeled & dated with contents and use-by
- [ ] Leftovers portioned & labeled with reheating instructions
- [ ] Ferments weighed & salted to target percent and weighted down
- [ ] Refrigerator temperature <= 40°F (4°C) and thermometer visible
- [ ] Freezer labeled with 3-month rotation and vacuum-sealed where possible
- [ ] Cleaning schedule set (daily/weekly) and checked off in app
- [ ] Food waste compost bin ready and emptied weekly
- [ ] Fire extinguisher accessible and last-inspected date recorded
- [ ] Child/pet hazards secured and hazardous items stored above 1.5m
- [ ] First-aid kit accessible and stocked (burn cream, bandages)
- [ ] Shopping list synced to phone and pantry CSV updated
- [ ] Spice jars labeled with expiry and opened date


Concrete Protocols / Recipes

Protocol: Basic Weeknight Pasta, 20 minutes
- Equipment: 4-qt pot, 12" sauté pan, silicone spatula, tongs.
- Ingredients per 2 portions: 160g dried pasta, 1 tbsp olive oil, 2 cloves garlic (sliced), 30g anchovy paste or 2 anchovy fillets, 400g canned crushed tomatoes, 30g unsalted butter, 20g parm.
- Steps: bring 3L salted water (15g salt) to boil; cook pasta to 1-2 min before package time. In pan: heat oil, add garlic + anchovy, sweat 30s, add tomatoes, simmer 4 min; reserve 100ml pasta water; add drained pasta, toss with 2 tbsp pasta water and butter; finish with grated parm and lemon zest.

Protocol: 2% Salt Kimchi (1.5 kg batch)
- Weigh napa cabbage: 1500g. Dissolve 30g sea salt into 500ml water; layer salt between leaves and weight 2 hrs; rinse twice and drain. Prepare paste: 80g gochugaru, 20g ginger, 30g garlic, 20g fish sauce, 60g daikon julienne, 30g scallion. Mix, coat cabbage, pack into jar with ferment weight. Ambient 68–72°F: ferment 2–5 days; taste daily. Refrigerate when desired acidity reached.

Protocol: Pan-Roasted Chicken Thighs with Braised Greens (serves 4)
- Equipment: ovenproof skillet 12", probe thermometer.
- Ingredients: 8 bone-in skin-on chicken thighs (~1.5 kg), 15g kosher salt, 5g black pepper, 30ml neutral oil, 4 garlic cloves crushed, 200ml chicken stock.
- Steps: dry chicken and season under skin and surface with salt/pepper 30 min before cooking. Preheat oven to 200°C (400°F). Sear thighs skin-side down in 12" skillet with oil over medium-high for 6-8 min until golden and crisp. Flip, add garlic and stock, transfer to oven and roast 12-15 min until internal temp 73°C (165°F). Rest 8 min. While resting, sauté chopped kale with 1 tbsp olive oil, 1 tsp chili flakes, 2 tbsp lemon juice until tender; serve with thighs.

Protocol: No-Knead Artisan Loaf (1 standard boule)
- Ingredients: 500g bread flour (12.5% protein), 360g water (72% hydration), 10g salt, 2g instant yeast.
- Steps: mix all until no dry flour, 30s slap-and-fold, cover at 24°C for 12-18 hr until doubled. Fold once, bench for 20 min, shape, proof in banneton 1.5–2 hr (or retard overnight at 4°C). Preheat Dutch oven at 250°C (482°F); bake covered 20 min, uncover and bake 20–25 min to internal temp 200–205°F. Cool 2 hrs.

Protocol: Fermentation Starter: Sourdough Build (feeding schedule)
- Day 0: combine 50g starter, 50g water, 50g flour (50/50 whole:bread). Keep at 24–26°C.
- Day 1–3: discard half, feed 50/50 twice daily until doubling in 4–6 hrs.
- Maintenance: feed 1:4:4 (starter:water:flour) when room-temp fermenting; refrigerate and feed weekly 1:5:5.

Templates

Weekly Meal Plan Template (CSV-ready)
Fields: Day,Meal,Protein,Vegetable,Starch,Sauce,PrepTime(min),BatchCook(Y/N),LeftoverUse,Notes
Example row: Monday,Dinner,Chicken Thighs,Kale,Quinoa,Pan Sauce,35,Y,Repurpose for salad,Night mise prep: chop garlic

Shopping List Template (Grouped by store section)
Fields: Section,Item,Qty,Unit,Notes
Sections: Produce,Dairy,Meat,Bakery,Canned,Bulk,Spices,Household

Leftover Rotation Sticker (Label format)
Fields on sticker: DATE_MADE (YYYY-MM-DD), CONTENT, REHEAT (temp/time), USE_BY (YYYY-MM-DD)
Example: 2026-08-02 | Beef Ragù | Reheat 160°C 15m | Use by 2026-08-05



Verification
- Taste tests: perform a 5-point tasting rubric (salt balance, acid, fat, texture, aroma) on one plate per dish.
- Time trials: log cook time; target weeknight finish <= 25 minutes for 60% of meals.
- Cost tracking: track per-portion cost; aim for < $4/portion for staple meals.

Cross-Skill Coordination
| Skill | Coordinate with | How |
|---|---|---|
| nutrition-strategist | meal planning | feed macronutrient targets into weekly template |
| home-organizer | pantry systems | integrate pantry inventory CSV with shopping list |
| gardener | produce supply | sync seasonal harvest calendar with menu plan |

What Good Looks Like
- A stamped weekly planner with two batch sessions and a daily 15-min finish routine; documented cook log with timestamped photos.
- Fridge labeled jars with dates; average food waste < 2% by mass; weekly cost-per-portion report under target.
- Dinner served within 25 minutes on weeknights, with balanced flavor (salt/fat/acid/heat) on 90% of plates and 80% family satisfaction.
- Five mother-sauce jars on shelf, each with date, base ratio, and rescue notes.
- Pantry inventory CSV with accurate quantities and <48-hr restock turnaround for staples.

Advanced Sauce Derivations (practical templates)
- Béchamel base (500 ml): 40 g butter, 40 g AP flour, 500 ml warm milk; cook roux 2–3 min off-white, whisk milk in slowly; finish with 25 g grated Gruyère for Mornay.
- Velouté base (500 ml): 40 g butter, 40 g AP flour, 500 ml light stock (chicken/fish); add mushroom duxelles + cream to make Sauce suprême.
- Espagnole reduction: start with brown stock 500 ml + 2 tbsp tomato paste, reduce to 250 ml, strain, finish with butter to gloss.
- Hollandaise rescue: if over 62°C yolk coagulates; blend a fresh yolk with 1 tbsp warm water and slowly whisk the broken sauce into the blender to re-emulsify.
- Tomato sauce (basic 1L): 2 tbsp olive oil, 1 onion diced (120 g), 3 cloves garlic, 800 g canned whole peeled tomatoes, 1 tsp sugar, simmer 30–50 min; finish with 1 tbsp butter.

Five Technique-Based Practice Templates (generate infinite variations)
1. Sauté Template (15–25 min): protein 100–200 g, aromatics 5–10 g, deglaze 30–60 ml acid/wine, finish with 10–20 g butter + herbs.
2. Roast Template (40–75 min): roast veg/protein at 200–220°C; toss with 1 tbsp oil per 250 g veg; rotate tray at 25 min.
3. Braise Template (2–6 hr): brown protein, sweat aromatics, deglaze 100 ml wine, add stock to 2/3 cover, cook at 150°C oven until probe temp target for tenderness.
4. Quick Pickle (24–72 hr): 250 ml vinegar, 250 ml water, 50 g sugar, 15 g salt — hot-brine vegetables, cool, refrigerate 24–72 hr.
5. Pantry Bowl (10 min): base grain 100 g cooked, canned protein 100 g, pickled veg 50 g, sauce 30–50 ml, fresh herb, salt/acidity finish.

Verification (expanded metrics)
- Weekly KPIs: % on-plan meals, average prep time, waste % by mass, cost per portion.
- Sensory check: run blind taste on salt/fat/acid balance weekly with two other household members; document consensus.
- Food safety logs: record fridge/freezer temps daily for 7 days after any ferment starts.

References (added)
15. "Bread" — Jeffrey Hamelman (2004) — professional bread techniques adapted to home ovens
16. "The Taste of Country Cooking" — Edna Lewis (1976) — seasonal templates and preserving
17. YouTube: ChefSteps (sous-vide technique library), Serious Eats channel (science-backed recipes)
18. Tool review: Cook's Illustrated equipment recommendations and annual test reports
19. Local extension or public health pages for canning and pressure-canning safety

Appendix: Ingredient Substitution Table (common swaps)
| Needed | Use instead (ratio) | Notes |
|---|---|---|
| Buttermilk | Milk + 1 tbsp lemon juice per 240 ml | Let sit 5 min before using |
| Breadcrumbs | Rolled oats or crushed crackers (1:1) | Adds texture differences |
| Egg (binder) | 1 tbsp chia + 3 tbsp water per egg (rest 10 min) | Good for baking, not for leavening-sensitive recipes |
| Heavy cream | Milk + 2 tbsp butter per 240 ml | OK for cooking, not whipping |
| Fresh herbs | 1/3 dried herbs by volume | Add earlier for rehydration |

Monthly Audit Template (CSV-ready)
Fields: Date, KPI_onplan_percent, Avg_prep_min, Waste_percent, Cost_per_portion_USD, Ferments_active_count, Pantry_missing_items_count, Notes
Example: 2026-08-01,85,22,3,3.60,2,4,"Reduced pork usage; ordered stock"

Entertaining Checklist (for 8 guests)
- 7 days: confirm menu, confirm dietary restrictions, test any new dish once.
- 3 days: finalize shopping list, defrost proteins, ensure plates and linens clean.
- 24 hours: batch-cook make-ahead items, set out garnish stations, chill wines.
- T-3 hours: finish hot items, set serving platters, reheat and rest proteins.
- T-10 minutes: garnish, final seasoning, light candles, assign plating roles.

Training Schedule (90-day practice plan)
- Weeks 1–4: Knife fundamentals & speed drills (10 min/day). Prepare 5 vegetable cuts and photograph.
- Weeks 5–8: Sauce week — practice three mother sauces twice each (one rescue attempt per sauce).
- Weeks 9–12: Bread & fermentation — 2 sourdough bakes, 1 kimchi, 1 yogurt cycle.
- Weeks 13+: Rotate cycle with monthly metrics review.

Glossary (short)
- Beurre manié: equal parts butter + flour kneaded and whisked into sauce to thicken.
- Autolyse: mixing flour and water, resting to develop gluten pre-salt/yeast.
- Fond: browned bits on pan used to develop pan sauces.

Appendix: Quick reference temperatures
- Beef rare: 52–54°C (125–130°F)
- Beef medium-rare: 55–57°C (131–135°F)
- Pork safe: 63°C (145°F) with 3-min rest
- Chicken safe: 74°C (165°F) internal
- Bread doneness: 95–96°C (200–205°F) internal temp

Audit and Practice Logs (template)
Fields: Date, Drill, Duration_min, Result_notes, Photo_path, Next_action
Example: 2026-08-02,Knife Julienning,10,"4mm consistent, 18s/row",/photos/julienne1.jpg,Repeat 10x



Scale Depth
- Solo: streamlined toolset, 8 recipes covering 80% of meals
- Small household (2–4): batch sizes scale x2–3; store in 500–750ml jars
- Medium (5–8): schedule two batch-cook sessions; use 12–quart Dutch oven and 2 full-sheet tray
- Enterprise (cater-for-home events 12–30): transition to commercial cookware, food-safety SOPs, and consult a food-safety specialist (this skill is not for food-business operations)

Anti-Hallucination
- Every technique lists explicit temperatures, weights, and times. If unsure, default to source: "The Food Lab" or USDA guidelines for safety temperatures. Cite product names only for tool categories. Avoid ambiguous claims about fermentation unless salt %, temp, and time are specified.



Scale Depth
- Solo: streamlined toolset, 8 recipes covering 80% of meals
- Small household (2–4): batch sizes scale x2–3; store in 500–750ml jars
- Medium (5–8): schedule two batch-cook sessions; use 12–quart Dutch oven and 2 full-sheet tray
- Enterprise (cater-for-home events 12–30): transition to commercial cookware, food-safety SOPs, and consult a food-safety specialist (this skill is not for food-business operations)

Anti-Hallucination
- Every technique lists explicit temperatures, weights, and times. If unsure, default to source: "The Food Lab" or USDA guidelines for safety temperatures. Cite product names only for tool categories. Avoid ambiguous claims about fermentation unless salt %, temp, and time are specified.
