# Library Gap Analysis (GAP-ANALYSIS.md)

> **Generated:** 2026 (live audit)
> **Scope:** Whole library — all 37 skill domains (283 canonical skills)
> **Method:** Frontmatter inventory extraction → per-domain coverage scoring → fresh audit run (`python3 scripts/audit-library.py`) → targeted absence checks against candidate gap roles.

---

## 1. Executive Summary

The library is in strong shape structurally but has three distinct classes of gaps:

| Class | Severity | Where | Nature |
|---|---|---|---|
| **A. Breadth gaps** | Medium | Thin/young domains (17-customer-success, 19-governance, 33-real-estate, 32-relationship-family, 11-legal, 18-corporate-finance, 26-web3, 36-travel-adventure) | Underserved roles that a "superior" library should cover |
| **B. Quality debt** | **High** | 14-finance trading cluster (18/24 flagged) + `00-framework/cross-skill-communication` | Missing required sections (Error Decoder, Best Practices, Production Checklist, DEEP markers) |
| **C. Documentation / metadata drift** | Medium | `skills-audit-report.txt`, `README.md`, `SUB-SKILL-MAP.md` | Committed artifacts disagree with the actual 283-skill / 37-domain state |

**Headline numbers (fresh audit, 2026):**
- 283 canonical skills across 37 domains (README says 214/29; committed audit report says 233/37 — both stale).
- Overall library score: **9.7/10** (skeleton 9.7, error decoder 9.6, best practices 9.4, prod checklist 9.6, scale depth 9.8, progressive disclosure 9.8).
- 19 skills carry audit flags; **18 of 19 are in 14-finance**.

---

## 2. Current State (verified)

### 2.1 Domain density

| Density | Domains |
|---|---|
| Heavy (14–27 skills) | 05-development (27), 14-finance (24), 07-devops (17), 13-specialized (14), 22-ai-engineering (14) |
| Medium (6–11) | 08-security (11), 04-architecture (11), 21-health-clinical (10), 06-quality (10), 12-operations (9), 29-personal-finance (9), 09-data (8), 03-design (8), 31-personal-growth (8), 10-growth (7), 23-trust-safety (7), 28-social-impact (7), 30-health-wellness (7), 01-strategy (6), 02-product (6), 15-sales (6), 16-people (6) |
| **Thin (2–5)** | 00-framework (5), 24-creative (5), 27-creator-finance (5), 20-hardware (4), 25-engineering-leadership (4), 34-philosophy-wisdom (4), 35-home-domestic (4), **11-legal (3)**, **18-corporate-finance (3)**, **26-web3 (3)**, **36-travel-adventure (3)**, **17-customer-success (2)**, **19-governance (2)**, **32-relationship-family (2)**, **33-real-estate (2)** |

### 2.2 Fresh audit vs committed report

`python3 scripts/audit-library.py` (live, 291 skills): **9.9/10 overall** (raised from 9.7 by the 2026-09-03 Class B repair); Error Decoder, Best Practices, and Production Checklist all at **10.0 with 0 missing**; 0 skills flagged across the quality-debt dimensions.

The committed `skills-audit-report.txt` was generated 2026-07-30 against **233** skills and is out of date (50 skills newer than the report; its per-skill flags no longer match the live audit's exemption logic).

### 2.3 Enumeration of quality-debt skills (replicated audit logic)

19 skills flagged; **18 in 14-finance**, 1 in 00-framework:

- `14-finance`: advanced-options-structures, options-automation-engineer, trade-performance-analyst, volatility-arbitrage-engineer, futures-trader, commodities-analyst, swing-options-trader, crypto-trader, algorithmic-trader, intraday-options-trader, forex-trader, macro-strategist, options-strategist, market-data-engineer, quantitative-analyst, fixed-income-analyst, home-buying, leaps-strategist (varying combos of ERR-DECODER / BEST-PRACTICES / PROD-CHECKLIST / DEEP-MARKER)
- `00-framework`: cross-skill-communication (missing Best Practices)

---

## 3. Class A — Breadth Gaps (candidate new skills)

Candidate roles are proposed only where an absence check confirmed no existing skill covers the role, and where the role fits the library's stated mission ("build products end-to-end — from idea to production, solo to enterprise", plus adjacent personal domains).

### 3.1 Company-lifecycle gaps (highest impact for the mission)

| # | Candidate skill | Suggested domain | Rationale / evidence |
|---|---|---|---|
| A1 | **M&A / Corporate Development Strategist** | 01-strategy or 18-corporate-finance | `SUB-SKILL-MAP.md` explicitly promises `m-and-a-strategy` under CEO Strategist, but **no skill and no reference file implements it** (checked `ceo-strategist/references/`: only fundraising + equity/cap-table). Gap between documented promise and shipped capability. |
| A2 | **Data Governance Officer** | 09-data | No data-governance skill exists (`dependency-governance` in devops is a different concern). 09-data has 8 engineering skills but no governance/quality/ownership role — a visible hole for enterprise-stage products. |
| A3 | **Customer Onboarding / Time-to-Value Specialist** | 17-customer-success | Domain has only 2 skills (account-manager, customer-success-manager). Onboarding is *mentioned* inside them, but there is no dedicated onboarding/Lifecycle role; domain is the thinnest in the company lifecycle. |
| A4 | **Learning & Development (corporate training) lead** | 16-people | 16-people = hiring/HR/career only; L&D appears only as incidental text in hr-manager/job-search-strategist. No dedicated L&D skill. |
| A5 | **Procurement / Vendor Management** | 12-operations | Only `event-planner/references/vendor-management.md` touches it (event-specific). No general procurement/supplier-management skill for ops at scale. |

### 3.2 Vertical/life-domain gaps (medium impact, thinner domains)

| # | Candidate skill | Suggested domain | Rationale / evidence |
|---|---|---|---|
| A6 | **Residential Real Estate Agent / Brokerage** | 33-real-estate | Domain has commercial-real-estate-analyst + property-manager only; `home-buying` (14-finance) is buyer-side personal finance. No residential sales/listing/brokerage skill. |
| A7 | **Intellectual Property Strategist (patents/trademarks/copyright)** | 11-legal | legal = legal-advisor, gdpr-privacy, regulatory-specialist. IP appears only as passing text inside legal-advisor references; no dedicated IP strategy skill for product companies. |
| A8 | **Corporate Tax Strategist** | 18-corporate-finance | `tax-strategist` exists but is personal-finance (29-personal-finance); corporate tax (provision, structure, transfer pricing) has no owner in 18-corporate-finance (accountant, fp-and-a, treasury only). |
| A9 | **Motion/Video or Brand Copywriter** | 24-creative | 24-creative = email-composer, medical-illustrator, presentation-designer, product-marketing-manager, ux-writer (health-tuned). No general brand copywriting or motion/video skill; `ux-writer` is explicitly health-focused. |
| A10 | **Tokenomics / DeFi Product Designer** | 26-web3 | web3 = smart-contract-auditor, cryptographic-engineer, zkp-engineer (all security/crypto-side). No tokenomics/economy-design skill on the product side. |

### 3.3 Notes on domains that are NOT gaps (verified)

- **02-product `grilling`, 12-operations `teach`/`wayfinder`** — odd placements, but verified intentional meta-primitives (Socratic interrogation, structured learning, large-scale exploration), not mis-filed skills.
- **01-strategy sub-skill promises** (`fundraising-playbook.md`, `equity-&-cap-table.md`) ARE implemented as reference files under `ceo-strategist/references/` — except `m-and-a-strategy` (A1 above).
- **Domain-specific UI designers** (fintech/game/healthcare) and **HIG/Material experts** — healthy coverage in 03-design; no action.

---

## 4. Class B — Quality Debt (fix, don't add)

Highest-leverage "make everything superior" work is **repairing the 14-finance cluster**, not adding finance skills:

1. **14-finance (18 skills):** add missing Error Decoder (4-column with Lesson), Best Practices, Production Checklist, and `<!-- DEEP` progressive-disclosure markers to match sibling skills.
2. **00-framework/cross-skill-communication:** add missing Best Practices section.
3. Re-run `python3 scripts/audit-library.py` afterwards — target ≥ 9.9/10 and 0 flagged skills.

Rationale: 14-finance is the second-largest domain but carried 95% of all flags; 24 finance skills skew toward trading/options (advanced-options-structures, options-automation-engineer, volatility-arbitrage-engineer, intraday-options-trader, swings/leaps/futures/forex) while the broader corporate-finance side stays thin — quality first, breadth second.

> **Status: COMPLETED 2026-09-03.** All 18 flagged 14-finance skills + `00-framework/cross-skill-communication`
> repaired: missing Error Decoder tables (4-column with Lesson), Best Practices, Production Checklist, and
> `<!-- DEEP` markers added — content mined from each skill's own references/ or inline Anti-Patterns/Gotchas
> (no fabricated content). `python3 scripts/audit-library.py` now reports **9.9/10 overall** with
> Error Decoder / Best Practices / Production Checklist at **10.0 and 0 flagged skills** (0/0/0/0).

---

## 5. Class C — Documentation / Metadata Drift

| Artifact | Current claim | Reality | Fix |
|---|---|---|---|
| `README.md` | 214 skills / 29 domains / 1,675 chain edges | 283 skills / 37 domains | Update counts, domain table rows 28–37, quality banner |
| `skills-audit-report.txt` | 233 skills, generated 2026-07-30 | 283 skills, 9.7/10 live | Regenerate from `scripts/audit-library.py` |
| `SUB-SKILL-MAP.md` | Covers only Domains 01–13 | 37 domains; 24 domains undocumented | Extend map to Domains 14–37 (or explicitly mark scope) |
| `QUICKSTART.md` / `USAGE-GUIDE.md` / activation tiers | "214 skills", "all 29 domains" | 283 / 37 | Grep and fix counts |
| **Chain symmetry (repaired 2026)** | README once claimed "1,675 edges with 0 asymmetries" | **REPAIRED.** `validate_chains.py` reported 948 asymmetric edges on the pristine tree; a dedicated repair pass (3 legacy-schema conversions + reciprocal `consumes_from`/`feeds_into` edges across ~155 skills) brought it to **0 errors** | **DONE — `validate_chains.py` now passes with 0 asymmetries** |

---

## 6. Prioritized Recommendation

**Impact ordering for "superiority":**

1. **Fix Class B** (quality debt) — cheap, mechanical, lifts 18 finance skills + library score toward 9.9+.
2. **Fix Class C** (metadata drift) — cheap, restores trust in published numbers.
3. **Add Class A breadth skills**, highest-value first:
   - Shortlist: **A1 M&A / Corporate Development**, **A2 Data Governance Officer**, **A3 Customer Onboarding**, **A4 L&D**, **A6 Residential Real Estate**.
   - Second wave: A5 Procurement, A7 IP Strategist, A8 Corporate Tax, A9 Creative, A10 Tokenomics.

> Authoring scope for this pass is decided at the Phase 2 checkpoint (user selects from the shortlist above; default = top 3–5 breadth skills + optional Class B fixes for the 14-finance cluster).

---

## 7. Appendix — Data Files (scratch, /tmp)

- `/tmp/gapanalysis/canonical.json` — 283-skill inventory (frontmatter)
- `/tmp/gapanalysis/coverage.json` — per-domain scoring (count, quality debt, SUB-SKILL-MAP presence)
- `/tmp/gapanalysis/quality-debt.txt` — per-skill audit flags
- `/tmp/gapanalysis/audit-fresh.json` — live `audit-library.py --json` output

---

## 8. Addendum — Deep Platform Audit: App Development Across All Platforms (2026-09-03)

Follow-up request: *"We need superior skills for any app developments for all platforms too."*
Method: verified platform coverage by searching all 288 SKILL.md files for platform keywords and
reading the scope of each core platform skill's frontmatter.

### 8.1 Current coverage — already strong

| Platform family | Skills that cover it (verified in frontmatter) | Depth |
|---|---|---|
| **iOS native** | `ios-developer` (Swift/SwiftUI/UIKit, App Store, Xcode) | Deep |
| **Android native** | `android-developer` (Kotlin/Compose, Play Store, Gradle) | Deep |
| **Apple ecosystem design** | `apple-hig-expert` (iOS/macOS/watchOS/visionOS + Liquid Glass) | Deep (design) |
| **Android ecosystem design** | `material-design-expert` (incl. Wear OS, Android TV, Auto) | Deep (design) |
| **macOS native** | `macos-developer` (SwiftUI/AppKit, notarization, Universal Binaries) | Deep |
| **Cross-platform desktop** | `desktop-developer` (Electron/Tauri/.NET MAUI/Qt/WPF, IPC, installers) | Deep |
| **Cross-platform mobile** | `react-native-developer` (Expo/EAS), `flutter-developer`, `kotlin-multiplatform`, `mobile-developer` (offline-first, push, deep links) | Deep |
| **Web / full-stack** | `frontend-developer`, `website-builder`, `fullstack-developer` | Deep |
| **Architecture patterns** | `mobile-architecture-patterns`, `desktop-architecture-patterns`, `event-driven-architect`, `codebase-design`, `domain-modeling` | Deep |
| **Platform-adjacent** | `game-developer` cluster, `accessibility-testing`, `appsec-engineer`, `shipping-and-launch` | Good |

### 8.2 Verified gaps (platform keyword search across all 288 skills)

| # | Gap | Evidence | Suggested addition |
|---|---|---|---|
| P1 | **watchOS developer** (implementation, not just HIG) | watchOS appears only in `ios-developer` (Handoff mention) + `apple-hig-expert`; no watchOS build/watch-face/complications skill | `watchos-developer` (05-development) |
| P2 | **tvOS / smart-TV developer** | tvOS found in **zero** skills | `tvos-developer` (05-development) |
| P3 | **visionOS / spatial-computing developer** | visionOS in `apple-hig-expert` + `ui-ux-designer` (design only); no build skill | `visionos-developer` (05-development) |
| P4 | **Wear OS / Android TV / Automotive implementation** | `material-design-expert` covers design; `android-developer` has no Wear/TV/Auto implementation scope | Extend `android-developer` or add wearable/TV references |
| P5 | **PWA / offline-first web app** | "PWA"/"service worker" appears only incidentally across web skills; no dedicated PWA skill | `pwa-developer` (05-development) |
| P6 | **Cross-platform strategy / build-vs-native router** | No skill answers "one codebase vs native vs hybrid" as a first-class decision | Router/reference inside `mobile-developer` or a small strategy skill |
| P7 | **Desktop: Windows-native (WinUI/Win32) & Linux-native depth** | `desktop-developer` is cross-platform-toolkit focused; no Windows-native or Linux-native deep skill | Extend `desktop-developer` references |

### 8.3 Recommendation (trending real-user lens — updated after user steer)

The user clarified the selection criterion: *"new trending and most useful that real people
uses."* Re-ranking by actual user reach and 2025-26 momentum rather than platform novelty:

| Rank | Platform / skill | Why real people use it (verified market reality) | Coverage status |
|---|---|---|---|
| 1 | **Web apps / PWA** | Most-used software surface on Earth; installable web apps reach users who never visit app stores | `frontend-developer`/`website-builder` deep; **no dedicated `pwa-developer`** |
| 2 | **Cross-platform mobile (React Native/Flutter)** | Majority of new consumer apps; one codebase, two stores | Already deep (`react-native-developer`, `flutter-developer`, `mobile-developer`) |
| 3 | **iOS + Android native** | The two app stores remain the default distribution for real users | Already deep (`ios-developer`, `android-developer`) |
| 4 | **Wearables (Apple Watch / Wear OS)** | Health/fitness apps are among the most-used app categories; watches are the primary health-data device | Design covered (`apple-hig-expert`, `material-design-expert`); implementation now extended in `android-developer` (Wear OS) — `watchos-developer` build skill optional |
| 5 | **visionOS / spatial** | Newest Apple platform with real developer momentum | Design covered; build skill optional |
| 6 | **Desktop (Windows/macOS/Linux)** | Enterprise and creator desktops remain essential; cross-platform toolkits + native depth both matter | `desktop-developer` deep and now extended with Windows/Linux-native depth |
| 7 | **tvOS** | Smallest consumer reach of the extended set | **Left out** of the trending shortlist (deferred) |

**Executed in this pass (user-approved "extend existing dev skills"):**
- `android-developer` + `references/android-wear-tv-auto.md` — Wear OS, Android TV, Android Auto implementation depth.
- `desktop-developer` + `references/windows-linux-native.md` — WinUI/WPF/Win32 and GTK/Qt native depth.

**Open decision (pending user):** author new dedicated trending skills — `pwa-developer`
(top pick by reach), `visionos-developer`, and/or `watchos-developer` — at the same 10/10 bar.

---

## 9. Addendum — Trending AI/ML · Backend · Crypto Skills (2026-09-03, verified absence)

Follow-up steer: *"any AI, ML, backend, crypto, like that"* — trending, most-used tech that
real people build with. Method: keyword audit across all 288 SKILL.md files AND their
`references/` (a listed "NONE" means zero matches anywhere in the library).

### 9.1 Verified gaps (genuine — no coverage in any skill or reference)

| # | Trending skill area | Evidence (searched, zero hits) | Suggested skill (domain) |
|---|---|---|---|
| T1 | **Computer vision** (object detection, image classification, video understanding) | `computer vision\|object detection\|image classification` → NONE | `computer-vision-engineer` (22-ai-engineering) |
| T2 | **Speech & voice AI** (STT/TTS, Whisper, voice assistants) | `speech\|whisper\|TTS\|voice assistant\|STT` → NONE | `speech-ai-engineer` (22-ai-engineering) |
| T3 | **On-device / local AI** (Ollama, llama.cpp, CoreML, TFLite, edge) | `on-device\|llama.cpp\|ollama\|coreml\|tflite` → NONE | `on-device-ai-engineer` (22-ai-engineering) |
| T4 | **Vector database & semantic-search ops** (pgvector, Qdrant, Weaviate, Pinecone) | `vector database\|pgvector\|qdrant\|weaviate\|pinecone` → NONE (llm-engineer covers RAG *patterns*, not vector-store operations) | `vector-search-engineer` (09-data or 22-ai-engineering) |
| T5 | **DeFi protocol engineering** (AMM, lending, yield) | `defi\|lending protocol\|amm\|liquidity pool` → NONE | `defi-protocol-engineer` (26-web3) |
| T6 | **Wallet infrastructure** (account abstraction/ERC-4337, MPC wallets) | `account abstraction\|ERC-4337\|mpc wallet` → NONE | `wallet-infrastructure-engineer` (26-web3) |
| T7 | **Onchain data & indexing** (subgraphs, indexers, chain analytics) | `subgraph\|onchain index\|blockchain data` → NONE (crypto-trader touches market data only) | `onchain-data-engineer` (26-web3 or 09-data) |

### 9.2 Backend — verified covered, no new skill warranted

Realtime/WebSocket (backend-developer 10 hits), gRPC (api-designer), streaming/Kafka
(event-driven-architect + data-engineer), auth/OAuth/passkeys (secure-api-design), rate
limiting/API gateway (api-designer + secure-api-design), serverless/edge (cloud-architect).
Recommendation: **no backend skill added**; extend references only if a specific gap emerges.

### 9.3 AI/ML — already deep (do not duplicate)

AI agents/agentic workflows (ai-engineer + multi-agent-orchestration + agent-persona-orchestrator
+ agent-handoff-protocol), agent evals (agent-eval-pipeline), RAG (llm-engineer + ai-engineer
rag-patterns), fine-tuning (llm-engineer + ml-engineer), multimodal (ai-engineer), MLOps/LLMOps
(mlops-engineer), guardrails (applying-llm-guardrails), AI security (ai-security).

### 9.4 Recommendation (ranked by real-user reach × trend × fit)

1. **T3 on-device/local AI** — the 2025-26 cost/privacy wave; pairs with llm-engineer.
2. **T1 computer vision** — largest real-world AI usage after language.
3. **T2 speech/voice AI** — every assistant/transcription product needs it.
4. **T4 vector-search infra** — the operational backbone of every RAG system.
5. **T5 DeFi + T6 wallet infra** — core of real-user web3 (decentralized finance + self-custody).
6. T7 onchain data — dev-facing; lowest urgency.

> Decision executed (2026-09-03, user steer "any AI, ML, backend, crypto"): authored
> `on-device-ai-engineer` (22-ai-engineering), `defi-protocol-engineer` (26-web3), and
> `wallet-infrastructure-engineer` (26-web3) at the 10/10 quality bar. Remaining from this
> list for a future pass: T1 computer-vision-engineer, T2 speech-ai-engineer, T4
> vector-search-engineer, T7 onchain-data-engineer.
