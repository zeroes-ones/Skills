---
name: environmental-tech-developer
description: >
  Use when building environmental and sustainability technology — carbon footprint
  trackers, climate action platforms, waste reduction and recycling apps, conservation
  monitoring systems, environmental data collection and visualization, sustainable
  consumption guides, renewable energy monitoring, air/water quality tracking,
  biodiversity observation platforms, circular economy marketplaces, or climate
  education tools. Handles environmental data integration (satellite imagery, IoT
  sensors, government datasets), carbon accounting (Scope 1/2/3), life cycle
  assessment integration, citizen science data collection, geospatial mapping for
  environmental applications, energy optimization algorithms, and sustainability
  impact measurement. Do NOT use for general data visualization (route to
  data-visualization-engineer), IoT without environmental context (route to
  embedded-engineer), or enterprise ESG reporting (route to compliance-officer).
license: MIT
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-07-25
tags:
  - environmental
  - climate
  - sustainability
  - carbon-tracking
  - conservation
  - renewable-energy
  - citizen-science
  - geospatial
  - social-impact
  - green-tech
token_budget: 5000
chain:
  consumes_from:
    - backend-developer
    - data-engineer
    - data-visualization-engineer
    - database-designer
    - embedded-engineer
    - frontend-developer
    - mobile-developer
    - qa-engineer
    - system-architect
  feeds_into:
    - qa-engineer
    - analytics-engineer
    - data-scientist
    - data-visualization-engineer
    - growth-engineer
  alternatives: []
---

# Environmental Tech Developer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end environmental technology development — from carbon footprint calculators to satellite-powered conservation platforms. This skill covers the full stack of building technology for planetary health: sensor networks monitoring air and water quality, citizen science apps engaging millions in data collection, renewable energy dashboards optimizing grid performance, waste management systems routing collection fleets, and geospatial platforms tracking deforestation in near real-time. Every recommendation integrates environmental data standards, scientific rigor, accessibility for global audiences, and measurable impact metrics. The goal is not just writing code — it is building tools that measurably reduce emissions, protect ecosystems, and accelerate the transition to a sustainable future.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Carbon calculator returns 0 or NaN for valid inputs — "flight from LHR to JFK returns 0.00 kg CO2" | Emission factor lookup failed — airport codes not in database, or API key for emission factor service expired | Verify emission factor API key and rate limits. Add fallback: distance-based estimation using great-circle formula × avg emission factor when API unavailable. Log all zero/NAN results with input trace for debugging. Validate: test with known routes monthly |
| Satellite imagery ingestion pipeline stalls after 48 hours — no new tiles processed | Sentinel/Landsat API changed auth requirements or tile format. Pipeline error silently swallowed by try/catch with no alerting | Add dead-letter queue for failed imagery processing. Monitor: alert if 0 tiles processed in 6 hours during scheduled ingestion window. Version-pin API clients. Store raw downloaded imagery before processing — enables replay without re-download |
| IoT sensor network reports impossible values — "water temperature: 900°C" from river monitoring station | Sensor hardware failure or calibration drift. Edge device uploads corrupt data that passes basic range checks because range was set too wide | Implement statistical outlier detection (3-sigma rule per sensor type). Flag >6σ readings for manual review. Require sensor calibration certificates updated quarterly. Use median-of-three readings from redundant sensors at each station |
| Deforestation alert system misses 40% of actual deforestation events — ground-truth data shows clearing undetected | ML model trained on regional data applied globally. Tropical forest patterns differ from boreal — one model doesn't fit all biomes | Train biome-specific models. Validate against ground-truth data quarterly. Require precision + recall > 85% before deploying to new region. Use human-in-the-loop for low-confidence detections |
| Citizen science app has 90% drop-off after first use — millions spent on app, no data collected | UI designed for scientists, not citizens. Requires taxonomic knowledge, GPS coordinates in decimal degrees, and 12-field data entry form | Design with citizens, not for them. Simplify: photo-based identification (AI-assisted), auto-geotag from phone GPS, gamification (streaks, badges, leaderboards). Target: 30-second observation submission. Field-test with non-scientists before launch |
| Environmental compliance dashboard shows "compliant" when site is actually violating permit limits | Data pipeline averages readings over hour/day — peak violations smoothed out. Permit limits apply to instantaneous readings, not averages | Store raw readings at native sensor frequency (typically 1-15 minute intervals). Alert on any single reading exceeding permit threshold. Report both instantaneous compliance (any exceedance = violation) and time-weighted compliance separately |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Building environmental models without peer-reviewed science backing — "our algorithm says this forest is sustainable" with no methodology paper | $500K-$5M in legal liability + reputational destruction; greenwashing accusations destroy NGO partnerships and grant funding. Models without peer review are marketing, not science | Publish methodology as open-access preprint before deploying. Cite emission factors with source + year (e.g., "EPA eGRID2022, subregion RFCW"). Every model output must reference its data source and uncertainty bounds. Partner with academic institution for validation |
| Hardcoding emission factors — app reports 2015 grid intensity for 2025 calculations | $50K-$200K in misreported carbon accounting; grid decarbonizes ~2-5%/year. Using 2015 factors for 2025 overstates emissions by 20-50% in regions with rapid renewable adoption | Use annually updated emission factor databases (eGRID, IEA, Climate TRACE). Refresh factors on January 15 each year. Store factors with effective_date and expiry_date. Alert if `CURRENT_DATE - emission_factor_date > 365 days` |
| Assuming perfect connectivity — environmental sensors deployed in remote areas with intermittent satellite/cellular | $100K-$500K in "dark data" — sensors deployed but no data received for months. Field teams dispatched to reboot devices that just needed better store-and-forward logic | Design for offline-first: edge devices buffer data locally (SD card, 30-day ring buffer). Sync when connectivity available. Use LoRaWAN for <50km range, satellite (Iridium/Swarm) for truly remote. Test with 48-hour connectivity blackout scenarios |
| Ignoring accessibility for global environmental audiences — app works on iPhone 15 but not on the $50 Android phones used by farmers in developing countries | $200K-$1M in failed adoption; environmental data collection depends on the people living in the ecosystems. If they can't use the app, data is biased toward wealthy regions | Target: works on Android 8+, 2GB RAM, 480p screen, offline-capable. Progressive Web App with <500KB initial load. Test on real low-end devices. Support offline data collection with background sync. Translate into local languages, not just English |
| Measuring vanity metrics (app downloads, page views) instead of environmental outcomes (tons CO2 reduced, hectares conserved) | $500K-$5M in grant funding lost; funders increasingly demand MRV (Monitoring, Reporting, Verification) of actual impact. Downloads don't prove emissions reduced | Design measurement from day 1: what is the counterfactual? How do you prove your tool caused the change? Use established protocols: GHG Protocol for emissions, VERRA/ICVCM for carbon credits, IUCN Green List for conservation outcomes. Budget 10% of project for M&V |
| Releasing open-source environmental data without privacy review — sensor locations reveal indigenous community territories or endangered species locations | $50K-$500K in harm to vulnerable communities + legal liability under GDPR/informed consent. Poachers use public species location data | Fuzz GPS coordinates: ±1km for community locations, ±10km for endangered species. Implement data tiering: public (anonymized, fuzzed), research partner (precise, NDA-required), internal only (raw). Review with community representatives before publishing |
| Building on proprietary environmental data formats — data trapped in vendor-specific format, can't share with research community | $100K-$500K in data lock-in; environmental science depends on open data sharing. Proprietary formats prevent integration with global datasets (GBIF, WDPA, Climate TRACE) | Use open standards: GeoJSON/GeoParquet for spatial, CF-NetCDF for climate model output, Darwin Core for biodiversity, SensorML for IoT. Export to standard formats is a launch-blocking requirement. Test: can you export all data to CSV + GeoJSON in <5 minutes? |

## Anti-Hallucination
<!-- STANDARD: 3min -->

* Admit uncertainty. If you cannot determine the correct approach, ask — do not guess.
* Flag your knowledge cutoff. If this project uses tools or patterns you have not seen, state your assumptions.
* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
* [VERIFIED] before any production guidance: Verify assumptions. Verify compatibility. Verify correctness.

## Route the Request
<!-- STANDARD: 3min -->

<!-- QUICK: 30s — auto-route first, then intent-route -->


## Auto-Route (No User Input Required)
<!-- STANDARD: 3min -->

Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "carbon" || "emission" || "ghg" || "scope.*[123]" || "carbon.*footprint" || "carbon.*accounting")` | Carbon tracking project detected. Jump to **Decision Trees** — Carbon Accounting Path, then **Core Workflow > Phase 2 (Carbon Data Integration)**. |
| A2 | `file_contains("*", "@tensorflow/tfjs" || "onnx" || "ml5" || "mobilenet" || "species.*classif" || "wildlife.*detect")` | ML-based environmental classification detected. Jump to **Core Workflow > Phase 3 (ML Model Pipeline)**. |
| A3 | `file_contains("*", "leaflet" || "mapbox" || "google.*maps" || "openlayers" || "GeoJSON" || "TopoJSON" || "geotiff")` | Geospatial visualization detected. Jump to **Decision Trees** — Geospatial Stack, then **Core Workflow > Phase 4 (Geospatial Implementation)**. |
| A4 | `file_contains("*", "mqtt" || "lorawan" || "modbus" || "opc-ua" || "sensor.*data" || "iot.*platform")` | IoT sensor integration detected. Jump to **Decision Trees** — Sensor Architecture, then **Core Workflow > Phase 5 (IoT Data Pipeline)**. |
| A5 | `file_contains("*", "sentinel" || "landsat" || "modis" || "ndvi" || "satellite.*imagery" || "remote.*sensing")` | Satellite/remote sensing project. Jump to **Decision Trees** — Satellite Data Pipeline, then **Core Workflow > Phase 6 (Satellite Processing)**. |
| A6 | `file_contains("*", "recycling" || "waste.*audit" || "circular.*economy" || "compost")` | Waste management project detected. Jump to **Core Workflow > Phase 7 (Waste Management)**. |
| A7 | `file_contains("*", "renewable" || "solar.*panel" || "wind.*turbine" || "energy.*forecast" || "battery.*storage")` | Renewable energy project detected. Jump to **Core Workflow > Phase 8 (Energy Systems)**. |
| A8 | `file_contains("*", "citizen.*science" || "community.*data" || "crowd.*source" || "volunteer.*monitor")` | Citizen science project detected. Jump to **Decision Trees** — Citizen Science Platform, then **Core Workflow > Phase 9 (Data Quality)**. |
| A9 | `file_contains("*", "gfp" || "climate.*risk" || "tcfd" || "esrs" || "sustainability.*report")` | Corporate sustainability reporting detected. Route to **compliance-officer** skill — this is enterprise ESG, not environmental tech development. |
| A10 | No environmental tech stack detected (`!file_exists("package.json" || "requirements.txt" || "go.mod")` AND no domain keywords) | Greenfield environmental project. Jump to **Intent Route** below. |


## Intent Route (Ask the User)
<!-- STANDARD: 3min -->

If no auto-route matched, use this intent tree:

```
What environmental problem are you trying to solve?
├── Carbon footprint tracking (personal or organizational) → Start at "Decision Trees" — Carbon Accounting Path, then Core Workflow Phase 2
├── Climate action / climate education platform → Jump to "Decision Trees" — Climate Data Sources, then Core Workflow Phase 1
├── Air quality or water quality monitoring → Go to "Decision Trees" — Sensor Architecture, then Core Workflow Phase 5
├── Waste management / recycling / circular economy → Start at "Decision Trees" — Waste Tech Stack, then Core Workflow Phase 7
├── Renewable energy monitoring or optimization → Jump to "Decision Trees" — Energy Data Sources, then Core Workflow Phase 8
├── Conservation / wildlife tracking / anti-poaching → Go to "Decision Trees" — Conservation Tech, then Core Workflow Phase 10
├── Citizen science data collection platform → Start at "Decision Trees" — Citizen Science Platform, then Core Workflow Phase 9
├── Sustainable consumption / ethical shopping guide → Jump to "Decision Trees" — Product Impact Data, then Core Workflow Phase 11
├── Geospatial environmental visualization → Go to "Decision Trees" — Geospatial Stack, then Core Workflow Phase 4
├── Satellite imagery analysis for land use / deforestation → Start at "Decision Trees" — Satellite Data Pipeline, then Core Workflow Phase 6
├── General environmental data dashboard → Invoke data-visualization-engineer, then return here for domain expertise
├── Enterprise ESG/Sustainability reporting → Route to compliance-officer skill — this is compliance, not environmental tech
├── Need hardware/sensor design → Invoke embedded-engineer or hardware-architect skill
├── Need environmental science domain expertise → You need a domain scientist. Flag what I can build vs. what needs scientific validation
└── Not sure where to start? → Answer discovery questions below

Discovery Questions (when the environmental domain is unclear):
1. "What environmental metric are you trying to measure or change? (carbon / water / waste / biodiversity / energy / air quality / land use)"
2. "Who are the primary users? (individuals tracking personal footprint / scientists collecting field data / companies managing compliance / governments monitoring policy / general public education)"
3. "Where will users be? (urban — good connectivity / rural — intermittent / remote field — mostly offline / global — need multilingual and low-bandwidth)"
4. "What data sources do you already have? (sensors deployed / CSV exports / API access / satellite accounts / none — need to source everything)"
5. "What's the measurable environmental outcome? (X tons CO2 reduced / Y hectares protected / Z species monitored / W kg waste diverted)"
```

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules are non-negotiable constraints that detect environmental tech mistakes before they happen. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Example | Violation Response |
|---|-------------------|-------------------|-------------------|-------------------|
| R1 | **Never present environmental data without source attribution and uncertainty** — every number shown to users must have provenance and confidence interval | Trigger: displaying carbon, emissions, pollution, or ecological data without citing source API, collection date, and methodology | "Your carbon footprint is 12.4 tons CO2/year." — displayed as a single precise number with no source, no margin of error, no date range | STOP. Respond: "Environmental data at [display] lacks attribution and uncertainty. Every environmental metric must show: (a) Data source (e.g., 'EPA eGRID 2024, emission factor for US Northeast'), (b) Collection date or vintage, (c) Uncertainty range (e.g., '±15% based on methodology'), (d) Methodology (e.g., 'Spend-based using EXIOBASE 3'). Environmental numbers are estimates, not facts — present them as such." |
| R2 | **Never claim carbon neutrality or offsets without verification** — carbon offset claims require third-party verification (Gold Standard, Verra VCS, Climate Action Reserve) | Trigger: code that calculates or displays "carbon neutral" status, offset amounts, or net-zero claims without integrating a verification registry API | "Offset your flight — we partner with TreeCo to plant 3 trees per flight." — no verification registry, no additionality check, no permanence guarantee | STOP. Respond: "Carbon offset claim at [location] lacks verification. Carbon offsets require: (a) Registry verification (Gold Standard ID, Verra VCS project ID), (b) Additionality proof (would this reduction happen without the offset?), (c) Permanence guarantee (what happens if trees burn?), (d) No double-counting. Link offsets to public registry entries. Unverified offsets are greenwashing — they mislead users and expose you to legal liability under green claims directives." |
| R3 | **Environmental data degrades — always timestamp and expire it** | Trigger: storing or displaying environmental data (sensor readings, satellite imagery, emission factors) without timestamp and expiration logic | "Current air quality: AQI 42." — displayed indefinitely, served from a cache 3 days old | STOP. Respond: "Environmental data staleness at [location]. All environmental data must carry: (a) `observed_at` timestamp (ISO 8601 with timezone), (b) `valid_until` expiration (sensor data: 1 hour, satellite: revisit period, emission factors: fiscal year), (c) UI indicator when data exceeds freshness threshold. Stale environmental data is worse than no data — it creates false confidence. AQI from 3 days ago is not 'current.'" |
| R4 | **Privacy-first by design — environmental data reveals personal behavior** | Trigger: collecting location, energy usage, travel patterns, or consumption data without explicit privacy architecture | "Track all user trips via GPS to calculate carbon footprint." — storing granular movement data that reveals home address, workplace, medical visits | STOP. Respond: "Privacy gap at [data collection point]. Environmental data IS personal data. GPS traces reveal home, work, religion, health. Energy data reveals occupancy patterns. Consumption data reveals diet, lifestyle, income. Architect for privacy: (a) Process on-device when possible (edge computing), (b) Aggregate before transmission (daily totals, not per-second), (c) Differential privacy for shared datasets, (d) Clear deletion policy, (e) Never sell or share individual-level data. GDPR, CCPA, and environmental data laws apply." |
| R5 | **Offline-first for field deployment — field researchers don't have WiFi** | Trigger: building environmental app that assumes persistent connectivity, uses real-time API calls for core functionality, or has no local data store | "The species identification app uploads the photo to our ML API for classification." — researcher is in a rainforest with zero connectivity | STOP. Respond: "Connectivity assumption failure at [feature]. Environmental apps are used in: rainforests, oceans, mountains, remote sensors, developing regions. Architecture requirements: (a) Local-first data store (SQLite/IndexedDB/Realm), (b) On-device ML inference (TensorFlow Lite, Core ML, ONNX Runtime), (c) Queue-and-sync pattern for uploads, (d) Graceful degradation when offline, (e) Conflict resolution for multi-device sync. If your app requires a server to function, it doesn't work for 90% of field use cases." |
| R6 | **Validate against scientific ground truth — your app's output must be scientifically defensible** | Trigger: building environmental calculations without referencing published methodologies, peer-reviewed emission factors, or calibrated sensor baselines | "We calculate carbon savings by multiplying miles not driven × 404g CO2/mile." — uses a single emission factor from a blog post, ignores vehicle type, speed, occupancy | STOP. Respond: "Scientific rigor gap at [calculation]. Environmental calculations must cite: (a) Published methodology (e.g., 'GHG Protocol Scope 3 Category 6: Business Travel'), (b) Emission factor source and version (e.g., 'UK DEFRA 2025, passenger vehicle — average, with radiative forcing'), (c) Assumptions and limitations, (d) Peer-reviewed validation where available. If your methodology wouldn't survive scientific peer review, don't ship it. One viral debunking destroys user trust permanently." |
| R7 | **Green hosting mandate — your app's infrastructure must not contradict its mission** | Trigger: deploying environmental app on cloud provider without renewable energy commitment, or using energy-intensive architecture (always-on servers, unoptimized queries, large data transfers) | "The carbon tracker app runs on 3 always-on EC2 instances with 40% average utilization." — the app's own carbon footprint exceeds what it helps users save | STOP. Respond: "Infrastructure contradiction at [deployment]. An environmental app that runs on coal-powered servers is self-defeating. Requirements: (a) Host on carbon-neutral cloud (Google Cloud — 100% renewable match, Azure — 100% by 2025, AWS — 100% by 2025 goal with Carbon Footprint Tool verification), (b) Prefer serverless/edge (scale to zero, no idle servers), (c) Optimize data transfer and storage (every GB transferred has a carbon cost), (d) Report your app's own infrastructure carbon footprint. Lead by example." |
| R8 | **Accessibility is non-optional in environmental tech — your users are global and diverse** | Trigger: building environmental app with only English, text-heavy interfaces, high-bandwidth assets, or assumptions about user literacy/tech-savviness | "The climate education platform has 50 pages of English text with no translations." — excludes 75% of the world's population who don't speak English fluently | STOP. Respond: "Accessibility gap at [interface]. Environmental impact is global — your users are: farmers in developing nations, indigenous communities, field researchers with low-power devices, and citizens with varying literacy. Requirements: (a) Multilingual from day one (i18n framework, at minimum English + top 5 user languages), (b) Icon-based + visual interfaces for low-literacy users, (c) SMS/USSD fallback for areas without smartphones, (d) WCAG 2.2 AA for disability access, (e) Low-power mode (dark theme, reduced animations, minimal network)." |
| R9 | **Environmental data licensing — respect open data but verify redistribution rights** | Trigger: integrating third-party environmental datasets without checking their license, attribution requirements, or commercial use restrictions | "We scrape the EPA website for air quality data and display it in our app." — data is public domain but the specific API has rate limits and attribution requirements | STOP. Respond: "Data licensing gap at [integration]. Environmental data sources have diverse licenses: (a) Government data: usually public domain but with attribution requirements (EPA, NOAA, NASA), (b) Satellite data: Copernicus is free/open with attribution; commercial satellites may require licenses, (c) Citizen science: check contributor consent for data use, (d) Commercial APIs: review ToS for redistribution. Always: attribute source, cache responsibly, respect rate limits, check commercial-use clauses." |
| R10 | **Never gamify environmental harm** — game mechanics must incentivize positive action, not reward destructive behavior in disguise | Trigger: leaderboard or achievement system that rewards quantity over quality (e.g., most trees planted regardless of survival rate, most offsets purchased regardless of quality) | "Top offset buyer this month: User123 with 500 tons!" — incentivizes buying cheap, low-quality offsets to climb a leaderboard | STOP. Respond: "Gamification hazard at [mechanic]. Environmental gamification must reward verified outcomes: (a) Measure impact, not activity (trees survived, not trees planted; verified emission reductions, not offsets purchased), (b) Leaderboards must weight by data quality and verification level, (c) Prevent gaming through data validation, (d) Education beats competition — explain the 'why' behind every metric. Badly designed gamification creates perverse incentives that undermine the environmental mission." |
| **R11** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate API calls for environmental libraries (GDAL, rasterio, xarray, geopandas, leaflet, turf.js) from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving environmental libraries → run version detection → anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |

* **Admit uncertainty — never fabricate environmental data.** If you're not certain about an emission factor, API endpoint, sensor specification, or scientific methodology, say so explicitly: "I'm not certain about the current emission factor for [region/sector]. Check the latest at [authoritative source URL]." Never invent an emission factor, sensor reading range, or satellite band specification — fabricated environmental data has real-world consequences.
* **Flag your knowledge cutoff.** Environmental APIs, emission factor databases, and satellite data products change quarterly. If your training data predates the latest release, state your cutoff date and recommend verifying against current documentation. This is especially critical for: carbon offset registries (projects added/retired), satellite data products (Landsat Collection levels, Sentinel processing baselines), and environmental regulations (GHG Protocol updates, EU Taxonomy changes).
* **Never guess sensor configurations.** If you're unsure about sensor calibration requirements, LoRaWAN network server settings, or IoT security protocols, do NOT provide a "reasonable default." Say: "Sensor network configurations must be verified against the manufacturer's current documentation and local radio regulations. I cannot provide a definitive answer without current specifications."
* **Never guess security configurations.** If you're unsure about the correct data encryption, API security, or IoT device security measure for environmental monitoring systems, do NOT provide a "reasonable default." Say: "Security configurations for environmental data systems must be verified against current best practices for IoT and data privacy. I cannot provide a definitive answer without current documentation."
* **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official documentation or peer-reviewed source, [COMMON-PRACTICE] — widely used in environmental tech but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. Environmental claims carry legal and reputational risk — precision matters.

## The Expert's Mindset
<!-- STANDARD: 3min -->


## The Mental Model Shift
<!-- STANDARD: 3min -->

Competent developers build environmental apps that show a carbon number and call it done. Masters build tools that **integrate real-time satellite data, validate sensor readings against scientific ground truth, operate offline in the Amazon rainforest, communicate impact in 15 languages, and produce metrics auditable enough to withstand peer review.** The shift: your app is not just software — it is a scientific instrument. Every number displayed to a user must be traceable to a data source, a methodology, and a confidence interval. When your app tells someone their carbon footprint is 8.3 tons, that number becomes their reality — it shapes their decisions, their guilt, their behavior change. Getting it wrong does real harm: it erodes trust in environmental action and can direct resources away from effective solutions.


## Cognitive Biases That Kill Environmental Apps
<!-- STANDARD: 3min -->

| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Precision theater bias** | Displaying environmental metrics with false precision (e.g., "Your carbon footprint: 8,347.2 kg CO2") when the underlying data has ±30% uncertainty — creating an illusion of accuracy | Always display confidence intervals. "Your estimated carbon footprint: 7,500–9,200 kg CO2 (based on spend data, ±15%)." Round to significant figures that match data quality. A precise-looking number from imprecise data is misleading, not helpful. |
| **Build-it-and-they'll-come bias** | Building a citizen science app with perfect data schema and assuming users will appear. No community engagement, no onboarding, no incentive design — the app launches to zero contributors | Citizen science is community organizing with a tech component. Before writing code: identify existing communities, partner with local organizations, design contribution incentives. The tech is 30% of the work — community is 70%. |
| **Global default bias** | Building for your own context (urban, high-connectivity, English-speaking, high-literacy) and assuming it works everywhere. Your beautiful React dashboard is unusable on a $50 Android Go phone with 2G in rural Kenya | Design for the most constrained user first. Test on: low-power devices, intermittent connectivity, non-English interfaces, low-literacy users. If your app works for a farmer with a basic phone in a remote area, it works for everyone. |
| **Sensor infallibility bias** | Trusting sensor readings as ground truth without calibration, validation, or anomaly detection. A $20 PM2.5 sensor reports 150 µg/m³ — you display it as "Hazardous air quality" when the sensor is simply dirty | Every sensor deployment needs: calibration against reference instruments, drift detection, cross-validation with nearby sensors, anomaly flagging. A cheap sensor without validation is a random number generator. Correlate with reference-grade monitors (government stations) and flag discrepancies. |
| **Single-metric tunnel vision** | Optimizing for one environmental metric (carbon) while ignoring trade-offs (water use, biodiversity, toxicity, social impact). Your "low-carbon" recommendation increases water consumption by 40% | Use multi-criteria assessment. Carbon is important but not sufficient. Track: water footprint, land use, biodiversity impact, toxicity, social equity. Present trade-offs explicitly — "This option saves 2 tons CO2 but uses 15,000 L more water." Environmental problems are interconnected. |
| **Solutionism bias** | Assuming technology alone solves environmental problems. Building a recycling app without understanding that the local municipality has no recycling infrastructure — the app connects users to a system that doesn't exist | Technology amplifies existing systems — it doesn't replace them. Before building: map the physical infrastructure, understand the policy landscape, interview stakeholders. A recycling app in an area without recycling facilities is a well-designed dead end. |
| **Perfection paralysis** | Waiting for perfect data, peer-reviewed methodology, and complete sensor coverage before shipping anything. The climate can't wait for your perfect model | Ship with clearly communicated limitations. "This is a beta estimate based on limited data. Accuracy will improve as more sensors come online." Environmental problems are urgent — better an 80% accurate tool today than a 99% accurate tool in 3 years. Just always be transparent about the 20% uncertainty. |


## What Environmental Tech Masters Know That Others Don't
<!-- STANDARD: 3min -->

* **The difference between activity data and emission factors — and which is more important.** Activity data (miles driven, kWh consumed, kg waste generated) is what your users provide. Emission factors (kg CO2 per mile, per kWh, per kg waste) is what converts activity to impact. Most developers obsess over emission factor precision while ignoring activity data quality. Garbage activity data × perfect emission factors = garbage results. Invest your effort in helping users provide accurate activity data (automated tracking, receipt scanning, smart meter integration) before worrying about whether the emission factor is 0.404 or 0.412 kg CO2/kWh.
* **Environmental data has a shelf life — and different types expire at different rates.** Real-time sensor data (AQI, water quality): stale after 1 hour. Satellite imagery: stale after the revisit period (Landsat: 16 days, Sentinel-2: 5 days). Emission factors: updated annually by agencies. Climate projections: valid for their modeled scenario but superseded by newer IPCC assessments. Your architecture must handle these different expiration cadences — automatically refreshing, clearly labeling staleness, and degrading gracefully when fresh data is unavailable.
* **The most impactful environmental code you'll write is the code that eliminates the need for itself.** A successful waste reduction app reduces waste so effectively that usage declines. A successful carbon tracker helps users decarbonize so much that they stop needing to track. Design for this paradox: your app's success metric is its own declining usage. Build sustainability into your business model — don't depend on perpetual growth of the problem you're solving.
* **Citizen science data is only as good as its validation pipeline.** A million observations of "bird species X at location Y" are worthless if 30% are misidentified. Expert review, consensus algorithms, photo verification, and ML-assisted validation are not nice-to-haves — they are the difference between scientific data and noise. iNaturalist's research-grade threshold (2/3 community agreement) is the gold standard. Budget 40% of your citizen science development time on validation infrastructure.
* **Environmental APIs are unreliable by nature.** Government APIs go down during shutdowns. Satellite data has cloud cover gaps. Sensor networks have dead nodes. Community data has seasonal participation drops. Your app must handle missing data gracefully — interpolation, historical baselines, explicit "data unavailable" states, and never, ever silently filling gaps with fabricated data.
* **Green hosting is a credibility prerequisite, not a marketing bullet point.** An environmental app hosted on fossil-fuel-powered infrastructure is a contradiction users will notice. Google Cloud matches 100% of consumption with renewable energy. Use cloud carbon footprint tools (AWS Customer Carbon Footprint Tool, Google Cloud Carbon Footprint, Azure Emissions Impact Dashboard) and publish your infrastructure emissions alongside your impact metrics. Your hosting choice IS your environmental statement.


## When to Break Your Own Rules
<!-- STANDARD: 3min -->

* **Use a heavy framework when real-time environmental data processing demands it.** If your app ingests 10,000 sensor readings per second and needs sub-second latency for pollution alerts, a serverless-only architecture won't cut it. Use Apache Kafka for streaming, TimescaleDB for time-series, and WebSockets for real-time dashboards. Don't prematurely optimize for green hosting at the expense of functionality that saves lives.
* **Skip on-device ML when accuracy is safety-critical.** If your air quality app tells asthmatics it's safe to go outside, that classification must be accurate. On-device models (TensorFlow Lite) are great for offline use but may sacrifice accuracy. For safety-critical environmental data, prefer server-side inference with offline fallback that clearly indicates reduced confidence.
* **Accept lower data quality for urgent deployments.** When deploying sensors after a natural disaster, a wildfire, or an oil spill, a $20 sensor deployed today beats a $2,000 calibrated sensor deployed next week. Mark data as "emergency response quality" with wider uncertainty bounds. Environmental emergencies don't wait for perfect instrumentation.

## When to Use
<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->
* Building carbon footprint calculators — personal footprint tracking, corporate Scope 1/2/3 accounting, supply chain carbon analysis, travel emissions, or product carbon labeling
* Creating climate action and education platforms — climate literacy tools, personal action guides, community challenge platforms, policy tracking dashboards, or climate risk visualization
* Developing air quality, water quality, or environmental monitoring systems — IoT sensor networks, citizen monitoring stations, real-time dashboards, alert systems for vulnerable populations
* Building waste management and circular economy applications — recycling identification (barcode/material scanning), collection route optimization, waste audit tools, composting guides, upcycling marketplaces
* Creating renewable energy monitoring dashboards — solar panel performance, wind turbine analytics, grid integration visualization, home energy optimization, battery storage management
* Developing conservation technology — wildlife tracking with GPS/camera traps, anti-poaching alert systems, habitat mapping, species identification from photos/audio, biodiversity monitoring
* Building citizen science platforms — observation collection, data validation workflows, community engagement, researcher collaboration, scientific data export
* Creating sustainable consumption guides — product environmental impact scanning, ethical brand databases, food waste tracking, sustainable transportation planners
* Developing geospatial environmental applications — deforestation monitoring, land use change detection, pollution heatmaps, protected area management, climate vulnerability mapping
* Integrating satellite and remote sensing data — Landsat, Sentinel, MODIS imagery processing, NDVI calculation, land cover classification, change detection pipelines
* Don't use for enterprise ESG reporting platforms (route to compliance-officer), general IoT without environmental context (route to embedded-engineer), or pure data visualization without environmental domain (route to data-visualization-engineer)

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: Sensor & IoT Data Pipeline Architecture

        ┌── INPUT: What's the data ingestion frequency?
        │
   ┌────┼────────────────────┐
   │    │                    │
   ▼    ▼                    ▼
[Batch] [Near real-time]   [Real-time
(daily)  (every 5-15min)]   streaming]
   │    │                    │
   ▼    ▼                    ▼
CSV/JSON  MQTT +            Kafka/Redis
upload    InfluxDB/         + TimescaleDB
→ cron    TimescaleDB       → stream
jobs +    → edge gateway    processing
PostgreSQL  aggregation     → alerting on
or S3     before cloud      threshold
           ingest           breaches

### Decision Tree 2: Impact Measurement & Reporting

        ┌── INPUT: Who is the audience for your impact data?
        │
   ┌────┼────────────────────┐
   │    │                    │
   ▼    ▼                    ▼
[End    [Grant              [Scientific
users]   funders/donors]     community]
   │    │                    │
   ▼    ▼                    ▼
Personal   Verifiable claims  Open data +
dashboards: with methodology: reproducible
CO2 saved,  follow GHG        methods:
trees       Protocol or       publish dataset
planted,    GRI standards     DOI, document
water saved → avoid greenwash → peer-reviewed
→ gamify    → third-party     methodology
            audit if >$100K

### Decision Tree 3: Citizen Science Data Quality

        ┌── INPUT: How critical is data accuracy for your use case?
        │
   ┌────┴────┐
   │         │
   ▼         ▼
[High:     [Moderate:
policy,    educational,
research]  awareness]
   │         │
   ▼         ▼
Layered     Auto-validation:
validation: 1. Photo proof
1. Training   required
   module    2. GPS + time
2. Expert     stamp check
   review    3. Outlier flag
3. Consensus  → accept >90%
   (3+ users)  confidence


## Carbon Accounting Path
<!-- STANDARD: 3min -->

```
User wants carbon footprint tracking:
├── Personal carbon footprint
│   ├── Spend-based estimation (fast, low accuracy) → Use a spend-to-carbon model (EXIOBASE, environmentally-extended IO). Input: bank transaction categories + amounts. Output: Scope 1-3 estimate ±40%.
│   ├── Activity-based estimation (medium accuracy) → Collect: home energy (kWh × grid factor), transport (miles × mode × vehicle), diet (meals × type), goods (purchases × category). Output: ±20%.
│   └── Hybrid estimation (best accuracy) → Combine: automated data (smart meter, vehicle telematics, receipt OCR) + user surveys for gaps. Output: ±10%.
├── Organizational carbon accounting (GHG Protocol)
│   ├── Scope 1 (direct emissions) → Fuel combustion on-site, company vehicles, fugitive emissions (refrigerants). Data: fuel purchase records, vehicle telematics, refrigerant logs.
│   ├── Scope 2 (purchased energy) → Electricity, steam, heating, cooling. Data: utility bills × grid emission factors (EPA eGRID, IEA, local grid operator). Two methods: location-based (grid average) and market-based (specific energy contracts).
│   └── Scope 3 (value chain) → 15 categories: purchased goods, capital goods, fuel/energy not in Scope 1/2, upstream transport, waste, business travel, employee commuting, upstream leased assets, downstream transport, processing of sold products, use of sold products, end-of-life treatment, downstream leased assets, franchises, investments. Start with categories representing >80% of emissions.
└── Product carbon footprint (Life Cycle Assessment)
    ├── Cradle-to-gate (raw materials to factory) → Material extraction, processing, transport to manufacturing.
    ├── Cradle-to-grave (full lifecycle) → Add distribution, use phase, end-of-life.
    └── Tools: openLCA (open source), Brightway (Python LCA framework), ecoinvent database (commercial, most comprehensive LCI database).
```


## Environmental Data Source Selection
<!-- STANDARD: 3min -->

```
What type of environmental data do you need?
├── Climate and weather data
│   ├── Current conditions → OpenWeatherMap (free tier, current + forecast), Tomorrow.io (hyperlocal, free tier up to 500 calls/day), Visual Crossing (historical + forecast)
│   ├── Long-term climate → NASA POWER (solar, meteorological — free, global, 1981-present), Copernicus CDS (ERA5 reanalysis — free registration), NOAA NCEI (historical weather extremes)
│   └── Climate projections → IPCC WGI Interactive Atlas (CMIP6 scenarios), NASA NEX-GDDP (downscaled projections), WorldClim (bioclimatic variables)
├── Air quality data
│   ├── Global coverage → OpenAQ (aggregates government stations — free API), IQAir AirVisual (commercial, free tier 500 calls/day), WAQI (World Air Quality Index — free)
│   └── Satellite-derived → NASA GIBS (satellite AOD), Copernicus CAMS (global reanalysis), Sentinel-5P (NO2, SO2, CO, CH4, aerosols)
├── Water quality data
│   ├── Global → GEMStat (UN global water quality), Water Quality Portal (US — EPA + USGS), Global Freshwater Quality Database
│   └── Satellite → Copernicus Sentinel-3 (chlorophyll-a, turbidity, water temp), Landsat (suspended sediment, algal blooms)
├── Energy and emissions
│   ├── Grid emission factors → Electricity Maps (real-time grid carbon intensity — free tier), WattTime (marginal emissions — free tier), EPA eGRID (US annual factors), European Environment Agency (EU factors)
│   ├── Emission factors database → UK DEFRA (annual, free), EPA GHG Emission Factors Hub, IPCC Emission Factor Database (EFDB), EXIOBASE (MRIO for supply chain), ecoinvent (LCA database — commercial)
│   └── Carbon offset verification → Gold Standard registry API, Verra VCS project database, Climate Action Reserve, American Carbon Registry
├── Satellite and remote sensing
│   ├── Optical imagery → Copernicus Sentinel-2 (10m, 5-day revisit, free), NASA Landsat 8/9 (30m, 16-day, free), MODIS (250m-1km, daily, free), Planet (3-5m, daily, commercial)
│   ├── Radar (cloud-penetrating) → Sentinel-1 (C-band SAR, 12-day, free), ALOS PALSAR (L-band, commercial)
│   └── Derived products → Global Forest Watch (deforestation alerts), Dynamic World (land cover — 10m, near real-time), FAO WaPOR (water productivity), NASA FIRMS (active fire detection)
├── Biodiversity and conservation
│   ├── Species data → GBIF (Global Biodiversity Information Facility — free API, 2B+ occurrences), iNaturalist API (research-grade observations), IUCN Red List API (species conservation status), eBird API (bird observations)
│   └── Protected areas → World Database on Protected Areas (WDPA API), UNEP-WCMC, Protected Planet
└── Socio-economic / environmental justice
    ├── Environmental justice → EPA EJScreen (US), CalEnviroScreen (California), EJAtlas (global environmental conflicts)
    └── Climate vulnerability → ND-GAIN Country Index, World Bank Climate Change Knowledge Portal, IPCC vulnerability assessments
```


## Geospatial Stack Selection
<!-- STANDARD: 3min -->

```
What's your geospatial use case?
├── Simple interactive environmental map (low data volume, web)
│   └── Stack: Leaflet + OpenStreetMap tiles (free, open source) + GeoJSON. Add Leaflet.markercluster for thousands of points. For offline: Leaflet + MBTiles.
├── High-performance environmental visualization (large datasets, web)
│   └── Stack: Mapbox GL JS (free tier 50K map loads/month) or MapLibre GL (open-source fork) + vector tiles. Deck.gl for WebGL-powered large-scale data (heatmaps, 3D terrain, time-series).
├── Satellite imagery browser (raster data)
│   └── Stack: OpenLayers (best for raster/WMS) + GeoTIFF.js for client-side GeoTIFF rendering. Geoserver (Java) or Titiler (Python, serverless-friendly) for dynamic tiling and COG (Cloud Optimized GeoTIFF) serving.
├── Offline field mapping (mobile, no connectivity)
│   └── Stack: MapLibre Native (mobile SDK) + MBTiles (offline vector/raster tiles). Export GeoJSON for field data collection. Realm/SQLite for local observations. Sync via queue when connectivity returns.
├── Scientific geospatial analysis (Python, server-side)
│   └── Stack: GDAL (raster/vector swiss army knife), rasterio (Pythonic raster I/O), xarray (N-dimensional labeled arrays — perfect for NetCDF climate data), geopandas (vector data), shapely (geometry operations), rioxarray (xarray + rasterio). For satellite: STAC (SpatioTemporal Asset Catalog) for discovery, pystac-client for search.
├── Real-time sensor mapping
│   └── Stack: MQTT broker (Mosquitto/EMQX) for sensor ingestion → PostgreSQL/PostGIS for spatial storage → Geoserver/MapServer for WMS/WFS → Leaflet/MapLibre for visualization. TimescaleDB extension for time-series sensor data.
└── Environmental modeling output visualization
    └── Stack: Xarray + hvPlot/HoloViews (Python interactive viz), Kepler.gl (Uber's open-source geospatial analysis tool — great for large datasets in browser), ParaViewWeb for 3D scientific visualization.
```


## IoT Sensor Architecture for Environment
<!-- STANDARD: 3min -->

```
Building an environmental sensor network:
├── Sensor selection
│   ├── Air quality → Plantower PMS5003 (PM2.5/PM10, ~$15), Sensirion SPS30 (PM, ~$40, better accuracy), Alphasense OPC-N3 (research-grade, ~$300). Gas sensors: Sensirion SGP30 (CO2, TVOC), Alphasense electrochemical (NO2, O3, SO2 — ~$80 each), Figaro MOS sensors (lower cost, lower accuracy).
│   ├── Water quality → Atlas Scientific (pH, DO, conductivity, temp — ~$50-200 per probe, lab-grade), DFRobot Gravity series (hobbyist, ~$10-30), In-Situ Aqua TROLL (professional, ~$3,000+).
│   ├── Weather → BME280 (temp, humidity, pressure, ~$3), Davis Vantage Pro2 (professional weather station, ~$600), optical rain gauge (RG-15, ~$80).
│   ├── Soil → Vegetronix VH400 (soil moisture, ~$35), Apogee quantum sensors (PAR, ~$200), TEROS 12 (soil moisture + temp + EC, ~$200).
│   └── Noise → MEMS microphones (ICS-43434, ~$5), Cirrus Optimus (professional sound level meter, ~$2,000).
├── Microcontroller selection
│   ├── Hobbyist/Prototype → ESP32 (WiFi + BLE, ~$5, great for urban sensors), Arduino MKR WAN 1300 (LoRa, ~$40).
│   ├── Field deployment → Pycom FiPy (WiFi + BLE + LoRa + Sigfox + LTE-M/NB-IoT, ~$50), Adafruit Feather ecosystem (modular sensors + radios).
│   └── Industrial → Particle Boron (LTE-M/NB-IoT with cloud, ~$60), Libelium Waspmote (professional environmental monitoring, ~$500+).
├── Connectivity for remote deployments
│   ├── Short range (<1km urban, 10km rural) → LoRa/LoRaWAN (The Things Network — free community network, Helium, or private gateway with ChirpStack). Frequency depends on region: 868 MHz (EU), 915 MHz (US), 433 MHz (Asia).
│   ├── Medium range (cellular coverage area) → LTE-M, NB-IoT (low-power cellular IoT). Check carrier coverage — not all carriers support both.
│   ├── Satellite (anywhere on Earth) → Swarm (low-cost satellite IoT, ~$5/month), Iridium SBD (global, ~$15/month), Argos (wildlife tracking, free for conservation — limited bandwidth).
│   └── Mesh networks → ESP-MESH (WiFi mesh for dense sensor arrays), OpenThread (Google's Thread implementation), Zigbee (low power, mature ecosystem).
├── Data pipeline architecture
│   ├── Protocol → MQTT (lightweight, pub/sub, ideal for IoT). Use MQTT-SN for really constrained sensors.
│   ├── Broker → Mosquitto (open-source, lightweight), EMQX (scalable, Kubernetes-friendly), VerneMQ (Erlang-based, highly available).
│   ├── Ingestion → Telegraf (plugin-based, 200+ input plugins) → InfluxDB (time-series, purpose-built for sensor data) OR TimescaleDB (PostgreSQL extension, SQL for time-series).
│   └── Processing → Node-RED (low-code IoT flows), Apache NiFi (data routing at scale), custom Python/Go microservices for complex processing.
└── Calibration and maintenance
    ├── Initial calibration → Co-locate with reference-grade instruments for 2+ weeks. Build calibration curve: `corrected_value = slope × raw_value + intercept`.
    ├── Drift detection → Deploy duplicate sensors at a subset of locations. Compare readings — divergence > threshold = recalibration needed.
    ├── Remote diagnostics → Monitor: battery voltage, signal strength (RSSI/SNR), uptime, data freshness (last report timestamp), temperature extremes (out-of-range operation).
    └── Alert → Notify when: sensor offline > 24 hours, battery < 20%, readings outside physical possible range (PM2.5 > 1000, temperature > 70°C), sudden step change (sensor failure vs. real event — correlate with nearby sensors).
```

## Core Workflow
<!-- STANDARD: 3min -->

Every environmental tech project follows this phased approach. The phases are sequential but iterative — each phase may reveal decisions that require revisiting earlier phases. Before writing a single line of code, answer five questions. The answers determine technology choices, data architecture, and user experience design.

**Phase 0: Problem Definition & Impact Hypothesis (1-3 days)**
Articulate the environmental problem and your theory of change. "We are building [tool] for [users] to [action] resulting in [measurable environmental outcome]." Example: "We are building a food waste tracking app for households to log weekly food waste, resulting in a 25% reduction in household food waste over 6 months." Define: success metric (what moves?), baseline (where are we starting?), measurement method (how will we know?). If you can't write this in one sentence, you don't understand the problem yet.

**Phase 1: Environmental Data Sourcing & Validation (3-10 days)**
Identify all data sources. Primary (your sensors, user inputs, direct measurements) and secondary (government APIs, satellite data, published research). For each data source document: provider, API endpoint or file location, update frequency, license and attribution requirements, known accuracy/uncertainty, rate limits and costs. Build a data freshness dashboard: every data source with `last_updated`, `next_expected`, and health status. Environmental data decays — your dashboard tells you when it has.

**Phase 2: Carbon Accounting & Emissions Modeling (5-15 days, if applicable)**
Implement GHG Protocol methodology. Scope 1 (direct): fuel records, vehicle logs → emission factors. Scope 2 (electricity): utility data × grid emission factor (location-based or market-based). Scope 3 (value chain): start with spend-based estimation (EXIOBASE), graduate to activity-based as data improves. Key decisions: emission factor database (DEFRA for UK/EU, EPA for US, IPCC for global), database version pinning (emission factors change annually — pin your version and document it), uncertainty propagation (Monte Carlo simulation for range estimates). Never ship a carbon number without its data vintage: "Based on 2025 DEFRA factors."

**Phase 3: ML Model Pipeline for Environmental Classification (3-10 days, if applicable)**
For species identification, material classification (recycling), land cover mapping, or pollution detection. Decision: on-device inference (TensorFlow Lite, Core ML, ONNX Runtime — good for offline field use, privacy) vs. server-side (more accurate models, needs connectivity) vs. hybrid (on-device for common cases, server fallback for edge cases). Data: pre-trained models (MobileNet for general image classification, iNaturalist species model, TrashNet for waste classification) vs. custom training (label your own data, use transfer learning). Validation: confusion matrix per class, field test with real users, blind test against expert-identified samples.

**Phase 4: Geospatial Implementation (5-20 days, if applicable)**
Choose stack based on Decision Trees — Geospatial Stack Selection. Key architecture decisions: tile serving (pre-generated MBTiles for offline, dynamic tiling for large datasets), data format (GeoJSON for small datasets <10MB, FlatGeobuf for medium, Cloud Optimized GeoTIFF for raster, PMTiles for single-file archives), projection (Web Mercator for web display — EPSG:3857, but store and analyze in geographic — EPSG:4326, or local UTM projection for area calculations). Never calculate area in Web Mercator — it distorts area by 2× at mid-latitudes and infinitely at poles.

**Phase 5: IoT Data Pipeline (5-20 days, if applicable)**
Architecture: sensor → radio (LoRa/WiFi/Cellular) → network server (ChirpStack/TTN) → MQTT broker → processing → time-series DB → API → dashboard. Key decisions: data retention (raw: 90 days, hourly aggregates: 2 years, daily: forever), downsampling strategy (mean, min, max, count per interval — never just mean, you lose extremes), alert thresholds (WHO guidelines for air quality: PM2.5 > 15 µg/m³ annual, > 45 µg/m³ 24-hour), sensor metadata (deployment location, calibration date, firmware version — essential for debugging).

**Phase 6: Satellite & Remote Sensing Pipeline (5-20 days, if applicable)**
STAC (SpatioTemporal Asset Catalog) for data discovery. Key processing steps: search (pystac-client → find scenes by AOI, date range, cloud cover < threshold), download (parallel with asyncio/aiohttp — satellite scenes are 1GB+), preprocess (atmospheric correction, cloud masking, band math — e.g., NDVI = (NIR - Red) / (NIR + Red)), analyze (land cover classification, change detection, time-series trends), serve (Cloud Optimized GeoTIFF in S3/GCS with range requests — no need to download entire scene). Tools: GDAL (swiss army knife), rasterio (Pythonic), xarray (multi-dimensional), Google Earth Engine (serverless planetary-scale — free for research/education, commercial licensing available).

**Phase 7: Waste Management & Circular Economy (5-15 days, if applicable)**
For recycling ID: barcode scanning → product database → material composition → local recycling rules (what's recyclable in this municipality? varies dramatically). Key challenge: recycling rules are hyperlocal — your app must know the user's municipality. Data: Open Food Facts (barcode → product, free API), municipality recycling databases (often PDF — need scraping). For collection route optimization: VRP (Vehicle Routing Problem) with OR-Tools (Google's optimization library) or VROOM (open-source). For circular economy: material passport concept (what materials are in this product? how can they be recovered?).

**Phase 8: Renewable Energy Systems (5-15 days, if applicable)**
Solar: panel specs → location (lat/lon) → orientation (azimuth, tilt) → weather data → PVGIS or NREL PVWatts API for production estimate. Wind: turbine power curve × wind speed distribution (Weibull parameters from weather data). Forecasting: time-series models (Prophet for simple, LSTM/Transformer for complex — but simpler is often better with limited data). Grid integration: real-time grid carbon intensity from Electricity Maps API — optimize consumption for low-carbon periods. Battery: state of charge tracking, degradation modeling, optimal charge/discharge schedule against time-of-use rates and carbon intensity.

**Phase 9: Citizen Science Platform (10-25 days)**
Core loop: observe → record (photo + location + time + metadata) → validate (community consensus, expert review) → publish (open data, research-grade threshold). Data model: Darwin Core standard (biodiversity) or compatible. Key features: offline data collection (queue and sync), photo upload with automatic geotagging from EXIF, species suggestion (ML pre-classification), community validation workflow (need N agreements for "research grade" — iNaturalist uses 2/3), bulk export (CSV, Darwin Core Archive, GeoJSON for researchers), project-based organization (specific location, taxon, time period). Engagement: streaks, challenges, leaderboards (but weight by data quality, not quantity).

**Phase 10: Conservation Tech (10-25 days)**
Wildlife tracking: GPS collar data ingestion → movement analysis (home range via MCP/kernel density, migration corridors, behavior classification). Camera trap: image upload → species detection (ML) → human review → population estimation (mark-recapture, occupancy modeling). Anti-poaching: sensor fusion (camera traps + acoustic gunshot detection + ranger patrol GPS + satellite deforestation alerts) → risk heatmap → patrol route optimization. Key constraint: security — poaching data in wrong hands endangers animals. Encrypt everything. Never publicly share real-time locations of endangered species. Data embargo periods are standard practice.

**Phase 11: Sustainable Consumption (5-15 days)**
Product scanning: barcode → product database (Open Food Facts, OpenBeautyFacts, soon: Open Products Facts for non-food) → environmental attributes (carbon, water, packaging, certifications). Data challenge: comprehensive product environmental databases don't exist yet. Strategy: start with what's available (brand-level sustainability ratings, certification databases), show data gaps transparently, let users contribute data (citizen science for products). Food waste: barcode → purchase date → shelf life estimation → spoilage prediction → recipe suggestions for items nearing expiration.

**Phase 12: Impact Measurement & Reporting (3-7 days)**
Build the impact dashboard before building the app. Define metrics upfront, instrument everything, measure from day one. Metrics: carbon reduced/sequestered (tons CO2e), waste diverted (kg), energy saved (kWh), water saved (liters), trees planted/survived (count, survival rate), land protected (hectares), species monitored (count, trend), volunteers engaged (people, hours), data contributions (observations, sensor readings). Methodology: every metric needs a calculation methodology (how do you go from "user logged a meatless meal" to "0.8 kg CO2e saved"?), baseline (compared to what?), counterfactual (would this have happened anyway?). Attribution: be honest about what your app contributed vs. what would have happened.

## Cost Matrix — Environmental Tech Budgeting
<!-- STANDARD: 3min -->

| Component | $0 (Bootstrapped) | $50-200/mo (Startup/Grant) | $500-2,000/mo (Funded/Enterprise) |
|-----------|-------------------|---------------------------|----------------------------------|
| **Hosting** | Cloudflare Pages + Workers (static + edge functions), or GitHub Pages. Google Cloud free tier (App Engine, Cloud Run 2M req/month). Render free tier. | Vercel Pro ($20), Fly.io ($5-50), Google Cloud Run (pay-per-use, ~$30-100). AWS with carbon footprint tracking. | AWS/GCP reserved instances. Multi-region deployment. CDN with edge compute. Dedicated database clusters. |
| **Database** | SQLite (single-server apps), PostgreSQL on Render free tier (90 days), Supabase free tier (500MB), PlanetScale free tier. | Supabase Pro ($25), PlanetScale Scaler ($29), TimescaleDB Cloud (free tier, then $30+), MongoDB Atlas free tier (512MB). | PostgreSQL on RDS/Cloud SQL with read replicas. TimescaleDB for time-series. Elasticsearch for sensor search. |
| **Geospatial** | Mapbox free tier (50K map loads/mo) or MapLibre (free, self-hosted tiles). OpenStreetMap tiles (free, rate-limited). | Mapbox ($2-5 per 1K loads for premium styles). Self-hosted Geoserver/Titiler on a $20 VPS. | Mapbox Enterprise. Self-hosted tile serving cluster. Google Earth Engine commercial license. |
| **ML Inference** | TensorFlow Lite on-device (free, offline). ONNX Runtime (free, cross-platform). Hugging Face free inference API. | RunPod serverless GPU ($0.20-0.50/hr), Replicate ($0.001-0.01 per inference). Google Cloud Run with GPU. | Dedicated GPU instances. SageMaker/Batch for satellite processing. Custom model hosting. |
| **IoT Platform** | The Things Network (free community LoRaWAN). ThingsBoard Community (self-hosted, open-source). Blynk free tier. | Helium Network ($0.001-0.01 per packet). Datacake ($15/mo). Ubidots ($50/mo). | AWS IoT Core, Azure IoT Hub. Custom ChirpStack deployment. Redundant brokers. |
| **Environmental APIs** | OpenAQ (free), OpenWeatherMap (1K calls/day free), NASA POWER (free), GBIF (free), Electricity Maps (free tier). | Tomorrow.io ($30-100/mo), Cloverly (carbon offset API, pay-per-use), Carbon Interface ($0.01-0.05 per estimate). | Premium data feeds. Commercial satellite data (Planet ~$500+/mo). Custom API agreements with data providers. |
| **Maps & Visualization** | Leaflet (free), Chart.js (free), Plotly open-source (free). | Kepler.gl (free, Uber's tool). Deck.gl with Mapbox ($2-5/K loads). | ArcGIS ($500+/mo), Tableau Server. Custom D3.js visualization development. |
| **Monitoring/Observability** | Sentry free tier (error tracking), UptimeRobot free (50 monitors), Plausible self-hosted (analytics). | Sentry Team ($26/mo), Better Uptime ($24/mo), Plausible Cloud ($9/mo), Datadog Infrastructure ($15/host). | Datadog APM, Grafana Cloud, PagerDuty, custom dashboards. |
| **Translation/i18n** | Weblate (self-hosted, free), Crowdin open-source tier (free). | Crowdin ($40/mo), Lokalise ($50/mo), POEditor ($20/mo). | Smartling, Transifex Enterprise, dedicated translation team. |
| **Total Range** | **$0-15/mo** | **$100-500/mo** | **$1,000-5,000+/mo** |

⚠️ All pricing as of 2026. Environmental data APIs and cloud provider pricing change — verify current rates before committing.

## Gotchas — Dollar-Quantified Environmental Tech Footguns
<!-- STANDARD: 3min -->

* **"We'll use a $15 PM2.5 sensor and call it good" → $250K in credibility damage.** Low-cost sensors drift 30-50% over 6 months without calibration. When your app reports "Air quality: Good (AQI 32)" based on a drifted sensor when actual AQI is 125 (Unhealthy for Sensitive Groups), users lose trust permanently. One viral tweet by a respiratory health organization showing your data is wrong can destroy your app. Budget for calibration: co-locate with reference monitors, recalibrate quarterly, display uncertainty.
* **"Offsets handled — we buy from a provider" → $0 environmental impact, potential greenwashing lawsuit.** The voluntary carbon market has a quality problem: 2023 investigations found 90%+ of rainforest offsets from major certifiers were "worthless" — no additional emissions reductions. If your app claims to offset user emissions through unvetted providers, you're exposed to greenwashing regulations (EU Green Claims Directive, FTC Green Guides). Solution: integrate only Gold Standard or Verra VCS verified projects with public registry IDs. Even better: prioritize reduction over offsetting in your UX.
* **"We'll source product environmental data later" → $50K in scraper infrastructure and 6 months of engineering time.** There is no single database of product environmental impacts. Building a product scanner that shows carbon/water/ethical ratings means aggregating from: Open Food Facts (free API, limited environmental data), brand sustainability reports (PDF scraping), certification databases (Fair Trade, Rainforest Alliance, B Corp — each with their own API or no API), and user-contributed data. Budget 3-6 months and dedicated data engineering for a comprehensive product database.
* **"Field researchers will have connectivity" → 80% of your target users can't use your app, $40K-$120K in rebuilding costs.** Rainforests, oceans, mountains, remote sensor deployments, developing regions — these are exactly where environmental work happens. Building an app that requires persistent internet eliminates your primary user base. Retrofitting offline support into a connectivity-dependent app costs 2-3× the original build. Architecture rule: core functionality must work offline. Test by turning on airplane mode and trying every feature.
* **"Citizen scientists will self-organize" → Empty platform at launch, $0 impact, $30K-$80K wasted in development costs over 12 months.** The "build it and they will come" fallacy kills citizen science platforms. Successful platforms (iNaturalist, eBird, Zooniverse) invested years in community building before the tech was self-sustaining. Budget: 50% of project time on community engagement (partnering with existing organizations, recruiting super-users, designing contribution incentives), 30% on validation infrastructure (data quality tools, expert review workflows), 20% on the actual app.
* **"We'll add multilingual support later" → Permanent exclusion of 75% of potential users, $15K-$50K in retrofit costs within 6 months.** Environmental problems are global. Climate vulnerability is highest in the Global South — exactly where English proficiency is lowest. "Later" never comes because retrofitting i18n into an existing codebase costs 3× more. Internationalize from the first scaffold: use a framework with i18n built in (react-i18next, vue-i18n, Rails i18n), mark every user-facing string as translatable, budget for professional translation of at minimum 5 languages covering your target regions.
* **"The grid emission factor database is updated annually — we can cache it" → Users act on last year's data in a rapidly changing grid, $5K-$20K in carbon accounting errors per year.** Grid decarbonization is happening fast. The UK grid went from 450 gCO2/kWh (2014) to 170 gCO2/kWh (2024). Using 2024 factors in 2026 overstates emissions by potentially 30%+ in rapidly greening grids. For an app with 100K users tracking daily, that's thousands of tons of misattributed carbon. Use Electricity Maps real-time API for current-hour carbon intensity. For annual accounting, use the latest available factors and clearly label their vintage.

## Error Recovery — Explicit Step-by-Step
<!-- STANDARD: 3min -->

**Symptoms:** Sensor data stops arriving. Dashboard shows "Last reading: 2 hours ago." No error logs, no crash — just silence.

**Diagnose:** Is it the sensor, the connectivity, the network server, or the data pipeline? Work backward from the user. 1. Check network server (ChirpStack/TTN) — are uplinks arriving? If yes, sensor and radio are fine — the problem is between network server and your pipeline. If no uplinks → sensor or connectivity issue. 2. Check sensor: is it powered? (Battery voltage in last telemetry.) Is it in range? (RSSI/SNR in last successful transmission.) 3. Check for known outages: The Things Network status page, Helium network status.

**Fix:** Pipeline issue: restart MQTT bridge or Telegraf ingestion. Connectivity: check gateway status — community gateways go offline when their maintainer moves. Sensor: if battery, deploy replacement. If permanent failure, flag location as "sensor offline — interpolation active."

**Symptom:** Carbon footprint calculation returns absurd values — "Your annual footprint: 0.02 tons CO2" or "2,400 tons CO2."

**Diagnose:** Check input data first. 0.02 tons = user provided near-zero activity data (just signed up, hasn't logged anything). 2,400 tons = unit mismatch (kg vs. metric tons, miles vs. km) or a spend-based calculation applied to annual spend when the input was monthly. 2,400 = roughly the footprint of someone spending $1M/year on air travel — are you double-counting or using wrong emission factors?

**Fix:** Add input validation: flag and explain when footprint is outside the expected range for the user's country (global median: ~4-7 tons CO2/year). Add unit confirmation: "Is your electricity usage 500 kWh/month or 500 kWh/year?" Show calculation trail: "500 kWh × 0.4 kg CO2/kWh = 200 kg CO2 = 0.2 metric tons." Users can spot their own data entry errors when they see the math.

**Symptom:** Species identification app returns "Unknown" for 80% of photos in the field.

**Diagnose:** Is your model trained on the right taxa and geography? A model trained on North American birds returns "Unknown" for Amazonian birds. Are field photos poor quality? (blurry, poor lighting, partial animal, camouflage). Check confidence threshold — default 0.7 may be too high for challenging field conditions.

**Fix:** Use a geo-aware model (knows what species are possible at the user's location). Fall back to "Suggestions at genus/family level" when species-level confidence is low. Guide users: "Try to photograph the whole animal, in good light, against a contrasting background." Crowdsource: "Submit for community identification" — human experts handle what ML can't.

**Symptom:** Geospatial map shows nothing — blank white tiles where environmental data should be.

**Diagnose:** Check browser console: CORS errors? 403 Forbidden on tile URLs? 404 — tile server returned nothing? Check data: is the GeoJSON/GeoTIFF valid? (geojsonlint.com, gdalinfo for GeoTIFF). Check projection: is data in EPSG:4326 but map expects EPSG:3857? Check bounds: does data exist at the current map viewport? Query your database: `SELECT COUNT(*) FROM observations WHERE ST_Within(geom, ST_MakeEnvelope(lng1, lat1, lng2, lat2, 4326))`.

**Fix:** CORS: configure tile server CORS headers. Projection mismatch: reproject with ST_Transform (PostGIS) or ogr2ogr (GDAL). Empty viewport: zoom to data bounds on load (`map.fitBounds(geoJsonLayer.getBounds())`). 403: check API key and referrer restrictions on Mapbox/Google Maps.

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Data sourcing: every environmental metric has documented source, methodology, vintage, and uncertainty range | Random sample 10 metrics → each has provenance link to methodology page |
| ☐ | Complete when Privacy architecture: location, energy, travel, consumption data processed with privacy-first design | On-device processing where possible; aggregation before upload; deletion mechanism tested |
| ☐ | Complete when Offline functionality: core features work in airplane mode; data syncs on reconnect without loss | Test: log 10 carbon entries offline → enable network → all 10 appear in cloud dashboard |
| ☐ | Complete when Scientific methodology: carbon accounting, sensor calibration, ML training data, classification approach documented publicly | Methodology page exists, linked from every data display; peer-reviewed where applicable |
| ☐ | Complete when Accessibility baseline: screen reader, keyboard nav, 320px width, offline, dark mode, high contrast all functional | Test with VoiceOver/TalkBack; minimum English + one additional language |
| ☐ | Complete when Green hosting: infrastructure on provider with public renewable energy commitment; app carbon footprint reported | Verify hosting provider's renewable energy percentage; calculate and publish app's own footprint |
| ☐ | Complete when Carbon accounting accuracy: spend-based vs. activity-based vs. hybrid methodology chosen and documented | Explain why chosen method; document ±error range; cross-validate against alternative method |
| ☐ | Complete when Sensor/device integration: IoT data pipeline handles device disconnection, data gaps, and calibration drift | Simulate 24h sensor outage → data gap flagged, not silently interpolated; calibration check scheduled |
| ☐ | Complete when API rate limits: environmental data APIs (weather, satellite, grid emissions) have fallback when rate-limited | Test hitting API limit → cached data served with staleness indicator; alert on > 1h staleness |
| ☐ | Complete when User impact reporting: dashboard shows user's environmental impact with actionable recommendations | Verify: total footprint displayed, trend over time, comparison to baseline, 3+ specific actions to reduce |

## Verification Guardrails — Binary Environmental Tech Checklist
<!-- STANDARD: 3min -->

Before ANY production deployment, every checkbox must be `[x]`. These are PASS/FAIL — no "mostly," no "we'll fix it next sprint."

* [ ] **V1. Data sourcing documented.** Every environmental metric displayed has a documented source, methodology, data vintage (year/date), and uncertainty range. No number appears without provenance.
* [ ] **V2. Privacy architecture reviewed.** Location data, energy usage, travel patterns, and consumption data are processed with privacy-first design (on-device where possible, aggregated, deletable). GDPR/CCPA compliance verified.
* [ ] **V3. Offline functionality tested.** Core features (data collection, species ID, carbon logging, sensor readings) work with airplane mode enabled. Data syncs correctly when connectivity returns. No data loss on connectivity transitions.
* [ ] **V4. Scientific methodology published.** Carbon accounting methodology, sensor calibration procedure, ML model training data source, and species classification approach are documented and publicly accessible. Methodology page exists and is linked from every data display.
* [ ] **V5. Accessibility baseline met.** App tested with: screen reader (VoiceOver/TalkBack), keyboard navigation, 320px width screen, offline mode, dark mode, high contrast mode. At minimum English + one additional language functional.
* [ ] **V6. Green hosting verified.** Infrastructure runs on provider with public renewable energy commitment. App's own carbon footprint calculated and reported. Idle resource waste eliminated (scale-to-zero, right-sized instances).
* [ ] **V7. Data freshness indicators implemented.** Every environmental data display shows: observation timestamp, data vintage, freshness indicator (green/yellow/red based on age thresholds). Stale data is clearly distinguished from current data.
* [ ] **V8. Alert thresholds validated.** Environmental alerts (AQI, water quality, deforestation, species detected) have thresholds validated against scientific/regulatory standards (WHO, EPA, IUCN). No alert fatigue from overly sensitive thresholds.
* [ ] **V9. Impact metrics instrumented.** Success metrics (carbon reduced, waste diverted, species monitored, etc.) are tracked from day one. Baseline established. Measurement methodology documented.
* [ ] **V10. Third-party API fallback tested.** For each external API (weather, air quality, emission factors, satellite data), a fallback or graceful degradation is implemented. Simulate API outage — app does not crash, does not show blank data, clearly indicates data unavailability.
* [ ] **V11. Data validation pipeline active.** Citizen science observations, user-reported data, and sensor readings have automated quality checks: outlier detection, consensus validation, ML-based anomaly flagging. High-quality data is distinguished from unverified data in UI.
* [ ] **V12. License compliance verified.** All data sources have documented licenses. Attribution displayed where required. Commercial use restrictions respected. No scraped data without permission.

## Sub-Skills — When to Use Specialized References
<!-- STANDARD: 3min -->

| Sub-Skill | When to Use | See Reference |
|-----------|-------------|---------------|
| **Carbon Accounting Specialist** | Implementing GHG Protocol (Scope 1/2/3), LCA calculations, offset verification, or emission factor selection  |
| **Environmental Sensor Deployment** | Hardware selection, calibration, LoRaWAN setup, sensor network design for air/water/soil monitoring  |
| **Satellite Data Processing** | Landsat/Sentinel/MODIS data access, NDVI processing, land cover classification, change detection pipelines  |
| **Geospatial Environmental Visualization** | Mapbox/Leaflet/Deck.gl for environmental data, heatmaps, time-series maps, offline field mapping  |
| **Citizen Science Platform Design** | Observation collection UX, community validation workflows, data quality standards, researcher collaboration features  |
| **ML for Environmental Classification** | Species ID from images/audio, waste material classification, land cover from satellite, pollution detection  |
| **Renewable Energy Systems** | Solar/wind modeling, grid integration, battery optimization, energy forecasting algorithms  |
| **Impact Measurement & Methodology** | Carbon accounting methodology, environmental KPI frameworks, counterfactual analysis, attribution modeling  |

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | When to Involve |
|----------------|-----------------|-----------------|
| **data-engineer** | Environmental data pipelines (ETL for sensor data, satellite data ingestion, emission factor database population), data warehouse schema for time-series environmental data, data quality monitoring infrastructure | Before Phase 1 (Data Sourcing) — environmental data integration is the foundation of every app |
| **data-visualization-engineer** | Dashboard designs, chart specifications, geospatial visualization patterns, real-time data display architecture | Before Phase 4 (Geospatial) or when building environmental dashboards |
| **mobile-developer** | Native mobile capabilities (offline storage, background location, camera integration for species ID, push notifications for environmental alerts), app store deployment | When building citizen science mobile apps, field data collection tools, or consumer-facing environmental apps |
| **frontend-developer** | Component architecture, responsive design, progressive web app capabilities for offline environmental tools | When building web-based environmental dashboards, education platforms, or consumer tools |
| **backend-developer** | API design, authentication, rate limiting, data processing pipelines for environmental calculations | Before any server-side environmental data processing or API development |
| **database-designer** | Schema for time-series sensor data, geospatial indexing (PostGIS), data partitioning strategy for large environmental datasets | Before Phase 5 (IoT Pipeline) or when designing data storage for multi-year environmental datasets |
| **embedded-engineer** | Sensor hardware selection, firmware for environmental monitoring devices, low-power optimization, LoRaWAN network configuration | Before Phase 5 (IoT Pipeline) — sensor hardware choices affect the entire data pipeline |
| **system-architect** | Overall system design for complex environmental platforms (multi-sensor networks, satellite processing pipelines, real-time alert systems), scalability planning | For large-scale environmental monitoring systems or platforms handling 100K+ sensors |

| Downstream Skill | What You Provide | Impact of Delay |
|-----------------|-----------------|-----------------|
| **qa-engineer** | Environmental app with data validation requirements, offline scenarios, sensor simulation data, alert threshold test cases | QA can't test without understanding environmental data quality requirements and offline use cases |
| **analytics-engineer** | Impact metrics definitions, environmental data schemas, calculation methodologies for carbon/savings metrics | Analytics can't build dashboards without knowing what "impact" means in this context |
| **data-scientist** | Labeled environmental datasets (citizen science observations, sensor readings), ML model requirements for species/land/material classification | Data scientists need domain context and labeled data to build accurate environmental models |
| **data-visualization-engineer** | Environmental data semantics (what do PM2.5/AQI/NDVI values actually mean to users?), alert thresholds, uncertainty visualization requirements | Visualization can't design effective displays without understanding the environmental meaning behind the numbers |
| **growth-engineer** | User personas (field researchers vs. urban consumers vs. citizen scientists), community engagement strategies, environmental impact storytelling | Growth can't position the product without understanding the environmental user segments and their motivations |


## Communication Triggers
<!-- STANDARD: 3min -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Emission factor database has new annual release (DEFRA, EPA, IPCC) | Data Engineer, Backend Developer | All carbon calculations must update to latest factors — stale factors produce misleading results |
| Sensor network detects anomalous readings across multiple sensors | Embedded Engineer, QA Engineer | May indicate calibration drift, environmental event, or sensor hardware failure — requires investigation |
| Satellite data provider changes API or data format (Landsat Collection upgrade, Sentinel processing baseline change) | Data Engineer, Backend Developer | Processing pipelines will break — satellite data format changes are breaking changes |
| Third-party environmental API deprecation or pricing change | Product Strategist, System Architect | May require data source migration — environmental API landscape shifts frequently |
| New environmental regulation or reporting standard (GHG Protocol update, EU Taxonomy, SEC climate rules) | Compliance Officer, Product Strategist | May require methodology changes and feature additions for compliance |
| Citizen science data quality drops below threshold (<70% research-grade) | UX Researcher, Frontend Developer | Validation workflow or user guidance may need redesign — quality decline indicates systemic issue |
| Infrastructure carbon footprint exceeds 20% of user-impact carbon savings | DevOps Engineer, System Architect | Self-contradiction — environmental app's own footprint is undermining its mission |
| User reports incorrect environmental data for their location | QA Engineer, Data Engineer | May indicate data source issue, stale cache, or location detection failure |
| Accessibility audit reveals non-compliance (missing translations, offline failure, screen reader issues) | UI/UX Designer, Frontend Developer | Environmental apps serve global, diverse users — accessibility failures exclude vulnerable populations |

## Proactive Triggers
<!-- QUICK: 30s — conditions that auto-activate this skill -->
| Trigger | Action | Rationale |
|---------|--------|-----------|
| User says "build a carbon footprint calculator" or "track emissions" | Start at Decision Trees → Carbon Accounting Path | Carbon accounting has specific methodology requirements — wrong approach is greenwashing |
| Codebase contains environmental data with no source attribution | Jump to Ground Rules → Rule R1 | Environmental data without provenance is the #1 mistake — fix before anything else |
| User wants to integrate satellite imagery | Start at Decision Trees → Satellite Data Pipeline, then Core Workflow Phase 6 | Satellite processing has specific toolchain and data volume requirements |
| Project mentions "sensors" or "IoT" with environmental context | Jump to Decision Trees → IoT Sensor Architecture | Sensor selection affects entire architecture — get it right upfront |
| User asks about carbon offsets or "making users carbon neutral" | Jump to Ground Rules → Rule R2, then Anti-Rationalization — Offset Quality | Offsets are the highest-risk environmental claim — legal and reputational exposure |
| Project has "citizen science" or "community data collection" | Jump to Anti-Rationalization — Citizen Science | Community engagement is 70% of citizen science success — tech is 30% |
| App will be used in field/remote/offline conditions | Jump to Ground Rules → Rule R5 (Offline-first) | Connectivity assumption is the most common fatal architecture decision |
| Environmental app being built for global audience | Jump to Ground Rules → Rule R8 (Accessibility) | Multilingual, low-bandwidth, low-literacy, low-power — design for constraints first |
| Project calculates any environmental savings/impact claims | Jump to Verification Guardrails → V11 (Impact Measurement) | Impact claims without methodology are unsubstantiated marketing — potentially fraudulent |
| User wants recycling/waste management features | Jump to Decision Trees → Waste Tech considerations, then Anti-Rationalization — Recycling Rules | Recycling is hyperlocal — generic advice is harmful |

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Environmental Tech Output Characteristics | Stack Evolution |
|-------|------------------------------------------|-----------------|
| **Solo Developer / Hackathon (1 person, $0-50/mo)** | Single-purpose environmental tool: personal carbon tracker, simple air quality display, waste sorting guide. Uses public APIs (OpenAQ, OpenWeatherMap, Electricity Maps free tier). On-device data with optional cloud backup. Offline-capable for core features. | React Native or Flutter (cross-platform mobile), Firebase/Supabase (backend), TensorFlow Lite (on-device ML), Leaflet (maps), Chart.js (visualization). SQLite for offline. Cloudflare Pages for web deployment. |
| **Small Team / Nonprofit (2-5 people, $50-500/mo)** | Multi-feature environmental platform: citizen science app with offline collection + cloud sync, sensor network dashboard for 50-500 sensors, carbon accounting for small businesses. Multiple data sources integrated. Community features (profiles, challenges, leaderboards). Basic data validation pipeline. | Next.js or React Native + FastAPI/Express backend. PostgreSQL + PostGIS + TimescaleDB for time-series + spatial. ChirpStack for LoRaWAN. Python (rasterio, xarray, geopandas) for satellite processing. MapLibre + Deck.gl for visualization. Crowdin (i18n). Sentry (error tracking). |
| **Funded Startup / Research Lab (5-20 people, $500-2,000/mo)** | Production environmental platform: real-time sensor network (1,000+ sensors), satellite imagery processing pipeline, species identification with custom ML models, carbon accounting with Scope 1/2/3 for enterprises. Research-grade data quality. Multilingual (10+ languages). Mobile + web. Public API for researchers. | Microservices (Go/Rust for performance-critical ingestion, Python for scientific computing, Node.js for web). Apache Kafka for sensor streams. Kubernetes (GKE/EKS). TimescaleDB cluster. Elasticsearch for sensor search. Custom ML models (PyTorch, ONNX deployment). GDAL/rasterio + dask for distributed satellite processing. Auth0 for auth. LaunchDarkly for feature flags. |
| **Enterprise / Government Scale (20+ people, $2,000-10,000+/mo)** | National/international environmental monitoring system: nationwide sensor network (10,000+ sensors), real-time satellite-based deforestation alerts, species monitoring at continental scale, carbon accounting platform for thousands of businesses. High-availability, multi-region deployment. SOC 2/ISO 27001 compliance. Academic partnerships for methodology validation. Policy advocacy features. | Multi-cloud (AWS + GCP for satellite data colocation). Apache Kafka + Flink for stream processing. Data lake (S3/GCS) with query engines (Athena/Trino). Custom STAC catalog for satellite data. GPU clusters for ML (satellite classification, species detection). GraphQL federation for API. Dedicated i18n team with professional translators. 24/7 on-call with environmental incident escalation path. Dedicated data quality team. |

## Best Practices
<!-- STANDARD: 3min -->

1. **Source everything — no unattributed environmental data.** Every emission factor, sensor reading, satellite pixel, and species observation must carry provenance: where it came from, when it was collected, how accurate it is. Build a data lineage view into your admin dashboard. When (not if) someone questions your numbers, you need the receipts.

2. **Prefer open data and open standards.** Environmental data should be accessible. Use OGC standards (WMS, WFS, WCS) for geospatial. Darwin Core for biodiversity. NetCDF/CF conventions for climate model output. STAC (SpatioTemporal Asset Catalog) for satellite imagery. Open standards enable interoperability — your data can be used by other environmental projects, amplifying impact.

3. **Design for data decay — everything has an expiration date.** Sensor readings: 1 hour. Weather forecasts: 3 hours. Emission factors: 1 year. Satellite imagery: revisit period. Climate projections: next IPCC assessment. Build TTL (time-to-live) into your data model and refresh pipelines. Show users when data is getting stale — don't wait for it to expire silently.

4. **On-device first, cloud-enhanced.** Core environmental functionality (species ID, carbon calculation, data collection) should work without internet. Use on-device ML (TensorFlow Lite, Core ML) for inference. Sync to cloud when connectivity is available. This architecture serves field researchers AND privacy-conscious urban users.

5. **Impact measurement from day zero.** Instrument impact metrics before you have users. Define: what is "impact," how is it calculated, what's the baseline, what's the counterfactual. Build the impact dashboard alongside the product. If you can't measure your environmental impact, you don't know if you're helping or just building another app.

6. **Community before code.** For citizen science, conservation, and community environmental monitoring: partner with existing organizations, build relationships with domain experts, recruit beta testers from the target community. The best environmental app with zero community engagement has zero impact. The simplest spreadsheet used by an engaged community has real impact.

7. **Transparency as a feature.** Publish your methodology. Open-source your calculations. Let users see the math. "Your carbon footprint is 8.3 tons. [Show calculation]" builds trust. A black box number builds skepticism. Environmental claims without transparency are indistinguishable from greenwashing — and will be treated as such by sophisticated users.

8. **Green your own stack.** Calculate and publish your infrastructure carbon footprint. Use providers with renewable energy commitments. Optimize data transfer (CDN caching, minimize payload sizes, compress images). Right-size your instances — idle servers emit carbon. Your environmental app's infrastructure IS part of its environmental statement. Lead by example.

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, data source decision, and methodology selection must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.


## How the State Log Works
<!-- STANDARD: 3min -->
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:

   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "environmental-tech-developer",
     "phase": "Phase 2: Carbon Accounting",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }

   ```

3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice — emission factor database selection, sensor hardware choice, methodology version, data license decisions.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.


## State Log Schema
<!-- STANDARD: 3min -->

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-25T13:00:00Z"` |
| `skill` | Which skill made it | `"environmental-tech-developer"` |
| `phase` | Which workflow phase | `"Phase 2: Carbon Accounting"` |
| `decision` | What was chosen | `"UK DEFRA 2025 emission factors for UK/EU operations, EPA eGRID 2024 for US locations"` |
| `rationale` | Why this over alternatives | `"DEFRA is most comprehensive for EU, EPA eGRID is authoritative for US. Both are free and updated annually. IPCC factors considered but are global averages — too coarse for country-level accuracy needed."` |
| `constraints` | What limits apply | `["Must update factors annually when new releases published", "GHG Protocol methodology compliance required", "Data vintage must be displayed with every calculation"]` |
| `alternatives_considered` | What was rejected | `["EXIOBASE (spend-based only, too coarse)", "IPCC default factors (global average, not country-specific)", "ecoinvent (commercial license, budget constraint)"]` |
| `reversible` | Can this be changed later? | `true` (switch emission factor databases between annual updates) |


## Anti-Drift Check
<!-- STANDARD: 3min -->
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
* [ ] Have I read the state log from the previous session?
* [ ] Do any prior decisions constrain what I'm about to do?
* [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
* [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?
* [ ] Are all environmental data sources still current and available? (Check API status, data freshness)
* [ ] Does the current phase's environmental methodology align with decisions made in earlier phases?

## Deliberate Practice
<!-- QUICK: 30s — exercises to build environmental-tech-developer mastery -->

| Exercise | Skill Targeted | Success Criteria | Time Investment |
|----------|---------------|------------------|-----------------|
| **Build a personal carbon footprint calculator using only public APIs** | Carbon accounting, API integration, uncertainty handling | Calculator shows Scope 1-3 estimate with source attribution and ±X% uncertainty for each category. Data vintage displayed. Methodology page auto-generated. | 4-8 hours |
| **Deploy an air quality sensor with LoRaWAN and build a real-time dashboard** | IoT hardware, sensor calibration, time-series visualization | Sensor co-located with reference monitor for 1 week. Calibration curve documented. Dashboard shows current + 24h trend + WHO guideline comparison. Offline fallback working. | 8-16 hours (plus co-location time) |
| **Build a satellite-based deforestation alert for a 100km² area** | Satellite processing, geospatial visualization, alert systems | Pipeline: auto-fetch Sentinel-2 scenes, calculate NDVI, detect changes > threshold, generate alerts with GeoJSON polygons, display on interactive map. False positive rate < 20%. | 10-20 hours |
| **Create a waste sorting guide app covering 5 municipalities** | Recycling rules engine, mobile UX, geolocation | App correctly identifies recyclability for 50 common items across 5 different municipalities. Offline-capable. Barcode scanning integrated. User can report errors. | 6-12 hours |
| **Build a citizen science observation platform with validation workflow** | Offline data collection, community validation, data quality | App: photo + GPS + metadata + species suggestion. Sync when online. Validation: N observers must agree. Research-grade threshold configurable. Darwin Core export working. | 15-25 hours |
| **Implement real-time grid carbon intensity optimization for EV charging** | Energy APIs, optimization algorithms, real-time data | App schedules charging for lowest grid carbon intensity using Electricity Maps API. Shows carbon savings vs. "charge immediately." Handles API outages gracefully. | 6-10 hours |
| **Audit and fix the environmental data attribution in an existing app** | Data provenance, methodology documentation | Every displayed number has source, date, uncertainty. Methodology page is complete. "Unknown" data is labeled as such — no misleadingly precise numbers. | 3-6 hours |
| **Build a multi-language environmental app from scratch** | i18n architecture, accessibility, offline support | App functions in English + 2 additional languages. All user-facing strings internationalized. RTL language support verified. Offline mode tested. Low-bandwidth mode (< 100KB initial load). | 8-16 hours |

## Error Decoder — War Stories from the Environmental Tech Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When environmental tech goes wrong, the failures are often invisible until someone gets bad data. Here are the most common failure signatures, their root causes, and the fix.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Carbon footprint shows 0 for all users after deploying to production. No errors — calculation returns 0 silently. | Emission factor fetch returns empty response (API rate limited, authentication expired). Code has `emissionFactor || 0` as a default — so missing factors become zero footprint instead of an error. `0 * activity = 0` for every calculation. | Never use `0` as default for environmental data. Use `null` or `undefined` and surface the error: `if (emissionFactor == null) { throw new DataUnavailableError('Emission factor unavailable for region X') }`. Display "Unable to calculate — data unavailable" instead of a false zero. Add health check endpoint that validates all data sources are returning non-zero values. | In environmental code, `0` is a dangerous default. Zero emissions, zero waste, zero impact — these are real values that users rely on. A silent zero from a data failure is indistinguishable from a genuine zero, and it's always wrong. Default to error, not zero. |
| Sensor dashboard shows "AQI 12 — Good" for weeks after a California wildfire starts. Users trust the data, go outside without masks, get exposed to hazardous air. | The sensor's PM2.5 inlet is clogged with ash. It's still reporting — just reporting clean air because particles can't reach the sensor. No anomaly detection because the sensor is technically "functioning" (reporting data within the physical range). | Add cross-validation: compare each sensor to nearby reference monitors and peer sensors. If Sensor A at Location X reports AQI 12 while the EPA reference monitor 2km away reports AQI 350, flag Sensor A as "likely faulty — verify." Add automatic divergence detection: `ABS(sensor_value - peer_median) / peer_median > 0.5` → alert. Add maintenance reminder: clean PM sensors monthly, more often in dusty/smoky conditions. | A "functioning" sensor is not a "correct" sensor. Environmental sensors fail in ways that produce plausible-looking data — clogged inlets, calibration drift, battery degradation. Without cross-validation against independent data sources, you're displaying fiction. The most dangerous sensor failure is the silent one that produces believable but wrong data. |
| iNaturalist-style observation app launched in Kenya. Zero observations after 3 months. Marketing budget spent on Facebook ads — still zero. | The app requires a photo of the organism, GPS coordinates, and species suggestion. In the target region: average smartphone has 8MP camera (poor macro), GPS accuracy is ±50m in rural areas, and most users have never used a species identification app. The UX assumes urban Western users with flagship phones and naturalist training. | Redesign onboarding for the actual user: (a) Accept lower-resolution photos with guidance ("try to fill the frame with the plant/animal"), (b) Allow manual location selection from a map (tap where you are), (c) Start with "What color is it? How big? Where did you see it?" — simple questions before ML suggestion. Test with actual users in the target region BEFORE launching. | The gap between "it works on my phone in San Francisco" and "it works for a farmer in rural Kenya" is a chasm. Every UX assumption — camera quality, GPS accuracy, data connectivity, literacy, prior tech exposure — must be validated with the actual target users in their actual environment. Assumptions are the enemy of global environmental impact. |
| Deforestation alert system detects 500 hectares of forest loss. Investigation reveals it was seasonal flooding — water was classified as "bare ground" by the land cover model. False alarm triggers emergency response, wastes resources, erodes trust. | Land cover classification model was trained on dry-season imagery. During the wet season, flooded areas have spectral signatures similar to bare soil in certain bands. The model has never seen water-covered vegetation. Training data lacks seasonal diversity. | Train land cover models on multi-temporal imagery (wet season + dry season). Include a "water" class with seasonal flooding examples. Add a temporal filter: "change must persist for 2+ consecutive observations to be classified as deforestation." Cross-reference with precipitation data — if rainfall was 3× normal in the detection period, flag as "likely seasonal — verify." | Environmental models are seasonal. A model trained on January data will fail in July. Always train on full annual cycle imagery. Add temporal persistence requirements — real deforestation doesn't appear and disappear between satellite revisits. Seasonal water, agricultural cycles, and snow cover are the top false-positive generators in land cover change detection. |
| Carbon offset marketplace shows "Verified: 10,000 tons CO2 retired." Users purchase offsets feeling good. Investigation reveals the forestry project was a plantation of non-native eucalyptus that dried up local water sources and displaced indigenous communities. | Offset verification checked: (a) Carbon sequestration modeled correctly (trees grew, carbon calculated), (b) Project registered in Verra VCS. It did NOT check: (c) Biodiversity impact (eucalyptus monoculture reduces biodiversity by 90%+), (d) Water impact (eucalyptus consumes 2-3× more water than native species), (e) Social impact (land rights, community displacement). Carbon tunnel vision. | Add multi-criteria offset evaluation: carbon + biodiversity + water + social. For forestry projects: require native species (or document why non-native), water impact assessment, Free Prior and Informed Consent (FPIC) documentation from local communities. Display trade-offs: "This project sequesters X tons CO2 but has medium biodiversity impact and high water consumption." Let users make informed choices — don't hide the trade-offs behind a "Verified" badge. | Carbon is not the only environmental metric. Mono-focus on carbon creates perverse outcomes: carbon-optimal projects that destroy biodiversity, deplete water, and harm communities. Offsets must be evaluated on multiple dimensions — and the trade-offs must be transparent. A "carbon neutral" claim that comes at the cost of indigenous land rights is not environmental progress. |
| Real-time energy dashboard for a solar-powered community center uses WebSockets for live updates. Works perfectly in development. Deployed, the dashboard on an old tablet in the community center shows "Connecting..." permanently. | The tablet runs Android 8 with Chrome 70 — WebSocket connection fails silently on this browser version. No fallback to HTTP polling. No error message beyond the spinner. The dashboard was tested on the developer's M1 MacBook with Chrome 120. | Implement transport fallback: WebSocket → Server-Sent Events → HTTP long polling. Test on the actual device fleet — especially old/cheap devices common in your target environment. Add explicit connection error states: "Connection lost. Data shown is from [timestamp]. Retrying..." with a manual refresh button. | Environmental tech is deployed on whatever hardware the community has — often 5+ year old devices. Your React 18 app with WebSocket streaming and WebGL rendering may work on your MacBook but fail on the community center's donated Windows 7 laptop. Test on the bottom 20% of devices — they're your actual users. |
| Food waste tracking app calculates "You've saved 50 kg CO2 this month!" User shares on social media. Friend asks: "How do you know?" App developer: "We assume each logged meal saves 2 kg CO2." The assumption was pulled from a single blog post citing a non-peer-reviewed report from 2019. | The "savings" calculation has no scientific basis. It's a marketing number dressed as an environmental metric. When (not if) this is challenged, there's no defense — the entire impact claim collapses. | Every environmental savings claim needs a cited methodology: "Based on [Source, Year]: average food waste meal = 2.5 kg CO2e (includes production, transport, and landfill methane). ±30% based on meal composition. See methodology." If you can't cite a methodology, don't make the claim. Build the methodology page BEFORE building the "share your impact" feature. Environmental claims are public statements — they must be defensible. | Impact numbers shared on social media are permanent and public. A viral tweet with an unsupported environmental claim is a future news story: "Environmental App Exaggerates Carbon Savings by 5×, Investigation Finds." The damage to environmental tech credibility is collective — one app's inflated claims make users skeptical of all environmental apps. |

## Production Checklist — Pre-Launch Verification
<!-- STANDARD: 3min -->

* [ ] **P1. Data provenance complete.** Every environmental metric displayed in the UI has a visible source, collection date, methodology version, and uncertainty range. No orphan numbers. The "How we calculate this" link works and is current.
* [ ] **P2. Offline mode functional.** Airplane mode test passes: core features (data collection, species ID, carbon logging, sensor check) work. Sync works when connectivity returns. No data loss. Clear offline indicator in UI.
* [ ] **P3. Privacy architecture validated.** Location, energy, consumption, and behavioral data processing reviewed. Data minimization confirmed. Deletion mechanism tested. GDPR/CCPA compliance documented.
* [ ] **P4. Green host deployed.** Infrastructure runs on provider with renewable energy commitment. App's own carbon footprint calculated. Scale-to-zero configured where applicable. No idle resources.
* [ ] **P5. Alert thresholds calibrated.** Environmental alerts (AQI, water quality, deforestation, species detection) tested with historical data. False positive rate acceptable. False negative rate < 5% for hazardous conditions. Alert fatigue assessed.
* [ ] **P6. i18n baseline shipped.** At minimum English + top-2 target languages functional. RTL languages render correctly. Date/time/number formatting localized. Currency and units use correct locale. Translation coverage ≥ 95% for user-facing strings.
* [ ] **P7. Accessibility tested.** Screen reader (VoiceOver + TalkBack) navigates all screens. Keyboard-only workflow tested. Color contrast passes WCAG 2.2 AA. Touch targets ≥ 44×44px. Works at 320px width. Dark mode supported.
* [ ] **P8. Scientific methodology published.** Public methodology page linked from every data display. Calculation formulas shown. Emission factors cited with version and year. Assumptions listed. Limitations section included.
* [ ] **P9. Impact measurement live.** Success metrics instrumented. Baseline recorded. Real-time impact dashboard operational. Methodology for converting user actions to environmental outcomes documented.
* [ ] **P10. API fallback tested.** Each external API tested for: timeout, 403, 500, malformed response, empty response, rate limit. Every failure mode has graceful degradation. No blank screens. No silent zeroes. Error states communicate clearly: "Air quality data temporarily unavailable. Last reading: [timestamp]. Check [official source] for current conditions."
* [ ] **P11. Data validation pipeline active.** Automated quality checks running. Consensus validation for citizen science data. Sensor anomaly detection operational. Data quality tier clearly displayed (verified/community/unverified).
* [ ] **P12. License compliance documented.** Every data source has: license type, attribution text (if required), commercial use permission, rate limits, last terms check date. Third-party library licenses reviewed. Open source license chosen and LICENSE file present.
* [ ] **P13. Security baseline.** HTTPS enforced everywhere. API keys in environment variables only. CSP headers set. Input sanitization on all user-submitted environmental data. Rate limiting on API endpoints. Penetration test completed (especially for apps collecting location data).
* [ ] **P14. Content security for conservation data.** Sensitive species locations encrypted or fuzzed. Anti-poaching data access controlled. Data embargo periods configured for vulnerable populations/sites. Public data release policy documented.
* [ ] **P15. Browser/device matrix tested.** Tested on: $150 Android phone (Android 10, Chrome 80), iPhone SE (latest iOS), mid-range laptop (4GB RAM, Windows 10), iPad (tablet UX tested). All pass core workflow. Offline mode tested on all.

## What Good Looks Like
<!-- STANDARD: 3min -->

> A farmer in rural Kenya opens the biodiversity monitoring app on a $80 Android Go phone. It loads in under 3 seconds on 2G, displays in Swahili, and lets her record a bird observation with a photo, GPS, and species suggestion — all without internet. When she returns to town and connects to WiFi, her observations sync and enter the community validation queue. Two other users confirm the species identification, elevating it to "research-grade." The data is exported in Darwin Core format and contributes to a peer-reviewed study on climate-driven range shifts. The app's carbon footprint for processing her observation is 0.02g CO2 — tracked and reported on a public dashboard. Every number in the app shows its source: "Species suggestion: 89% confidence (model v2.4, trained on East African birds, Feb 2026)." The environmental impact dashboard shows: 47,000 research-grade observations, 12 peer-reviewed publications supported, 230 community monitors trained. This is what a 10/10 environmental tech build looks like.

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

* **Anti-Rationalization**: See [anti-rationalization.md]
* **Best Practices**: See [best-practices.md]
* **Production Checklist**: See [checklist.md]
* **Deliberate Practice**: See [deliberate-practice.md]
* **Error Recovery**: See [error-recovery.md]
* **Gotchas**: See [gotchas.md]
* **State Log**: See [state-log.md]
* **Sub-Skills**: See [sub-skills.md]
* **Verification Guardrails**: See [verification-guardrails.md]
* **What Good Looks Like**: See [what-good-looks-like.md]
* **Carbon Accounting Methodology**: See [carbon-accounting.md]
* **Sensor Deployment Guide**: See [sensor-deployment.md]
* **Satellite Processing Pipeline**: See [satellite-processing.md]
* **Geospatial Visualization Patterns**: See [geospatial-visualization.md]
* **Citizen Science Platform Design**: See [citizen-science.md]
* **Environmental ML Classification**: See [environmental-ml.md]
* **Renewable Energy Systems**: See [renewable-energy.md]
* **Impact Measurement Framework**: See [impact-measurement.md]


## External Resources
<!-- STANDARD: 3min -->

* **Carbon Accounting Standards & Tools**: GHG Protocol (ghgprotocol.org), EPA GHG Emission Factors Hub, UK DEFRA Conversion Factors, EXIOBASE (exiobase.eu) for MRIO spend-based carbon, openLCA (openlca.org), Brightway LCA framework (brightway.dev), ecoinvent database (ecoinvent.org — commercial). Carbon offset registries: Gold Standard (goldstandard.org), Verra VCS (verra.org), Climate Action Reserve, American Carbon Registry.
* **Climate & Weather Data**: OpenWeatherMap API (openweathermap.org/api — free tier), NASA POWER (power.larc.nasa.gov — solar, meteorological, free), Copernicus Climate Data Store (cds.climate.copernicus.eu — ERA5, free registration), Tomorrow.io (tomorrow.io — hyperlocal weather, free tier), IPCC WGI Interactive Atlas (interactive-atlas.ipcc.ch), NOAA NCEI (ncei.noaa.gov).
* **Air & Water Quality**: OpenAQ (openaq.org — global air quality API, free), IQAir AirVisual (iqair.com — commercial, free tier), WAQI (waqi.info — free), EPA AirNow (airnow.gov — US), Sentinel-5P (atmosphere.copernicus.eu — satellite air quality), GEMStat (gemstat.org — global water quality), Water Quality Portal (waterqualitydata.us — US EPA + USGS).
* **Satellite & Remote Sensing**: Copernicus Open Access Hub (scihub.copernicus.eu — Sentinel-1/2/3/5P), USGS EarthExplorer (earthexplorer.usgs.gov — Landsat, MODIS), NASA GIBS (nasa.gov/gibs — satellite imagery tiles), Google Earth Engine (earthengine.google.com — planetary-scale analysis, free for research), STAC (stacspec.org — SpatioTemporal Asset Catalog standard), pystac-client (Python STAC search), GDAL (gdal.org), rasterio (rasterio.readthedocs.io), xarray (xarray.dev).
* **Biodiversity & Conservation**: GBIF (gbif.org — 2B+ species occurrences, free API), iNaturalist API (inaturalist.org/pages/api+reference), IUCN Red List API (iucnredlist.org), eBird API (ebird.org), Global Forest Watch (globalforestwatch.org — deforestation alerts, free API), Dynamic World (dynamicworld.app — near real-time land cover, 10m), NASA FIRMS (firms.modaps.eosdis.nasa.gov — active fire detection).
* **Energy & Grid Data**: Electricity Maps (electricitymaps.com — real-time grid carbon intensity, free tier), WattTime (watttime.org — marginal emissions, free tier for nonprofits), NREL PVWatts (pvwatts.nrel.gov — solar production estimates), PVGIS (EU photovoltaic geographical system), UK National Grid ESO API (carbon intensity).
* **IoT & Sensors**: The Things Network (thethingsnetwork.org — community LoRaWAN), Helium Network (helium.com — decentralized IoT), ChirpStack (chirpstack.io — open-source LoRaWAN server), ThingsBoard (thingsboard.io — IoT platform, open-source), Node-RED (nodered.org — low-code IoT flows), MQTT (mqtt.org), InfluxDB (influxdata.com — time-series DB), TimescaleDB (timescale.com — PostgreSQL time-series).
* **Geospatial Tools**: Leaflet (leafletjs.com — open-source web maps), MapLibre GL (maplibre.org — open-source Mapbox GL fork), Deck.gl (deck.gl — WebGL data visualization), Kepler.gl (kepler.gl — geospatial analysis), OpenLayers (openlayers.org — raster-heavy mapping), Turf.js (turfjs.org — geospatial analysis in browser), PostGIS (postgis.net — spatial PostgreSQL), QGIS (qgis.org — desktop GIS).
* **Environmental APIs & Services**: Carbon Interface (carboninterface.com — carbon estimates API), Cloverly (cloverly.com — carbon offset API), Open Food Facts (openfoodfacts.org — product database, free API), Ecosia (ecosia.org — green search, API for tree counter), Doconomy Åland Index (doconomy.com — carbon impact of transactions).
* **Green Hosting & Sustainable Software**: Google Cloud Carbon Footprint (cloud.google.com/carbon-footprint), AWS Customer Carbon Footprint Tool, Azure Emissions Impact Dashboard, Cloud Carbon Footprint (cloudcarbonfootprint.org — open-source multi-cloud tool), Green Software Foundation (greensoftware.foundation — principles and patterns), The Green Web Foundation (thegreenwebfoundation.org — green hosting checker).
* **Environmental Justice & Equity**: EPA EJScreen (epa.gov/ejscreen — US environmental justice mapping), EJAtlas (ejatlas.org — global environmental conflicts), ND-GAIN (gain.nd.edu — country climate vulnerability index), World Bank Climate Change Knowledge Portal (climateknowledgeportal.worldbank.org).
* **Scientific Data Standards**: Darwin Core (dwc.tdwg.org — biodiversity data), NetCDF/CF (unidata.ucar.edu — climate model output), OGC Standards (ogc.org — WMS, WFS, WCS, SensorThings API), STAC (stacspec.org — satellite imagery catalog), GeoJSON (geojson.org), Cloud Optimized GeoTIFF (cogeo.org).
* **Regulatory & Policy**: GHG Protocol (ghgprotocol.org), EU Green Claims Directive, FTC Green Guides (US), SEC Climate Disclosure Rules (US), EU Taxonomy for Sustainable Activities, TCFD (Task Force on Climate-related Financial Disclosures), TNFD (Taskforce on Nature-related Financial Disclosures).
* **Community & Learning**: Public Lab (publiclab.org — community environmental monitoring), iNaturalist (inaturalist.org — model citizen science platform), ClimateAction.tech (climateaction.tech — tech workers for climate), Earth Species Project (earthspecies.org — AI for animal communication), WILDLABS (wildlabs.net — conservation tech community), Open Sustainable Technology (opensustain.tech — open-source environmental projects directory).
