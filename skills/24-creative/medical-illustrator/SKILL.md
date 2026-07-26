---
name: medical-illustrator
description: >
  Use when creating clinical diagrams, anatomical illustrations, patient
  education infographics, mechanism-of-action animations, or visual design
  systems for regulated health products. Handles FDA labeling compliance for
  patient-facing visuals, color-blind safe palettes, medical accuracy
  verification workflows, motion design for health education, and accessible
  medical illustration (alt text, tactile graphics, high-contrast). Do NOT use
  for general graphic design, brand identity creation, non-health illustration
  work, or UI component design without clinical content.
license: MIT
author: Sandeep Kumar Penchala
type: creative
status: stable
version: 1.1.0
updated: 2026-07-23
tags:
- medical-illustration
- patient-education
- clinical-diagrams
- health-visualization
- anatomical-illustration
- motion-design
- visual-health-literacy
token_budget: 3800
chain:
  consumes_from:
  - medical-content-reviewer
  - patient-health-educator
  - ui-ux-designer
  - ux-writer
  feeds_into:
  - brand-guidelines
  - patient-health-educator
  - ux-writer
---
# Medical Illustrator / Visual Designer (Health Tech)
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Create accurate, accessible, and compassionate visuals for health — from anatomical diagrams and mechanism-of-action animations to patient education infographics, all designed for clinical accuracy, regulatory compliance, and health literacy.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.svg\|*.ai\|*.eps", "anatomy\|artery\|organ\|skeletal\|muscle\|pathology")` OR `file_contains("*", "clinical.diagram\|patient.education\|FDA.labeling\|surgical.illustration")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.xml\|*.dcm", "DICOM\|Modality\|StudyInstanceUID")` OR `file_contains("*", "DICOM\|MRI\|CT.scan\|ultrasound\|radiology")` | This may require DICOM visualization. Jump to **Decision Trees** — 2D vs 3D Rendering Pipeline. |
| A3 | `file_contains("*", "FDA\|510.k\|regulatory\|labeling\|prescribing.information\|CFR")` AND `file_contains("*.svg\|*.eps", "dosage\|administration\|contraindication")` | Jump to **Core Workflow** — Phase 4 (Regulatory Illustration Standards). FDA labeling graphics require specific compliance. |
| A4 | `file_contains("*.svg", "color\|palette\|#")` AND NOT `file_exists("accessibility-audit.json")` | Jump to **Decision Trees** — Color Accessibility. All medical illustrations need deuteranopia/protanopia/tritanopia testing. |
| A5 | `file_contains("*", "brand\|logo\|style.guide\|visual.system")` AND `file_contains("*", "health\|medical\|clinical\|pharma")` | Jump to **Core Workflow** — Phase 8 (Visual Brand for Health). |
| A6 | `file_contains("*", "animation\|motion\|video\|timeline\|60fps\|storyboard")` AND `file_contains("*", "surgical\|mechanism\|drug\|cellular\|procedure")` | Jump to **Core Workflow** — Phase 5 (Motion Design for Health). |
| A7 | `file_contains("*", "alt.text\|accessibility\|WCAG\|CVD\|color.blind\|tactile\|braille")` AND `file_contains("*", "illustration\|diagram\|visual\|graphic")` | Jump to **Core Workflow** — Phase 7 (Accessibility in Medical Illustration). |
| A8 | `file_contains("*", "translate\|localize\|i18n\|multi.language\|Spanish\|French\|German")` AND `file_contains("*.svg", "text\|label\|callout")` | Jump to **Best Practices** — Localization-Ready Illustration. Text separation from artwork is critical. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Create a clinical diagram (anatomy, pathology, surgical, MoA) → Jump to "Core Workflow" — Phase 1 (Clinical Diagram Design)
├── Design patient education visuals → Jump to "Core Workflow" — Phase 2 (Patient Education Visuals)
├── Apply visual health literacy principles → Jump to "Core Workflow" — Phase 3 (Visual Health Literacy)
├── Meet FDA/regulatory illustration standards → Jump to "Core Workflow" — Phase 4 (Regulatory Illustration Standards)
├── Create animated medical content → Jump to "Core Workflow" — Phase 5 (Motion Design for Health)
├── Ensure medical accuracy via clinical review → Go to "Core Workflow" — Phase 6 (Visual Design for Medical Accuracy)
├── Make illustrations accessible (CVD, alt text, tactile) → Jump to "Core Workflow" — Phase 7 (Accessibility in Medical Illustration)
├── Build a visual brand for health → Jump to "Core Workflow" — Phase 8 (Visual Brand for Health)
├── Need radiology or DICOM image processing? → Invoke clinical-informatics-specialist instead
├── Need patient experience or comprehension testing? → Invoke ux-researcher instead
└── Not sure? → Describe the illustration need (audience, clinical context, output format) and I'll route you

```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to generate illustrations without verified anatomical references.** Every anatomical diagram must cite a specific source (Netter's Atlas 7th ed., Gray's Anatomy 42nd ed., or equivalent) with page/plate number. | Trigger: generated output contains `anatomy\|artery\|organ\|muscle\|skeletal` labels AND `grep -rn "Netter\|Gray's\|Thieme\|Sobotta\|Grant's" *.svg *.ai *.md 2>/dev/null` returns 0 citations | STOP. Respond: "I need a verified anatomical reference before I can produce this illustration. Specify the source (e.g., Netter's Atlas, 7th edition, Plate 234) or confirm the anatomical relationships you want depicted. I won't draw anatomy from memory." |
| **R2** | **REFUSE to finalize clinical illustrations without documented clinical reviewer sign-off.** Every diagram used in patient care, surgical guidance, or drug labeling must have a named clinical reviewer. | Trigger: generated output is a final illustration AND `grep -rn "reviewed.by\|clinical.review\|sign.off\|approved.by" *.md *.yaml 2>/dev/null` returns no clinician name with credentials | STOP. Respond: "This illustration must be reviewed by a clinician before publication. Mark it [PENDING CLINICAL REVIEW] with reviewer name and expected date. Never ship a clinical illustration without documented sign-off." |
| **R3** | **REFUSE to use red/green as the sole differentiator for critical vs. safe zones.** 8% of male viewers (deuteranopia) cannot distinguish red/green. All risk-critical color pairs must have pattern or luminance backup. | Trigger: generated SVG or color palette contains `fill="#ff\|fill="#00ff00\|fill="red"\|fill="green"` in adjacent critical/safe regions AND no `pattern="hatch\|stripes\|dots"` on the same elements | STOP. Insert pattern overlay: add hatching to danger zones, stippling to safe zones. Respond: "Red/green alone fails for 8% of viewers with deuteranopia. I've added pattern differentiation (hatching = danger, dots = safe). Also test with `npx coblis-simulator --image output.svg --type deuteranopia`." |
| **R4** | **REFUSE to rasterize text labels into flat images when localization is needed.** Text must remain in a separate SVG `<text>` layer with translation keys. Rasterized text = re-creating artwork for every language. | Trigger: generated output is a raster image (PNG/JPG) AND `file_contains("*", "translate\|localize\|i18n\|multi.language")` is true | STOP. Respond: "This illustration contains text that will need localization. Export text as a separate SVG layer with translation keys. I won't produce rasterized text if this asset ships to multiple languages." |
| **R5** | **DETECT and WARN about color-only information encoding.** Every visual element that uses color to convey meaning must also use a secondary differentiator (pattern, label, shape, or luminance). | Trigger: generated SVG uses `fill` color to distinguish categories (e.g., `fill="#ff0000"` for artery, `fill="#0000ff"` for vein) AND no `stroke-dasharray` or `<text>` label or pattern on those elements | WARN: Add comment `<!-- COLOR-DEPENDENT: Add pattern/label backup for color-blind viewers -->` and insert `stroke-dasharray="4,2"` or text labels on each color-coded element. Test with: `npx coblis-simulator --image output.svg --type all` |
| **R6** | **DETECT and WARN about motion content exceeding seizure-safe flash thresholds.** Animations must limit flash rate to ≤3 per second and respect `prefers-reduced-motion`. | Trigger: generated animation timeline shows frame changes faster than 333ms between high-contrast alternations OR `file_contains("*.mp4\|*.gif", "flash\|strobe\|blink")` without `prefers-reduced-motion` media query | WARN: "This animation exceeds WCAG 2.2 seizure-safe thresholds (≤3 flashes/sec). Reduce flash rate and add `@media (prefers-reduced-motion: reduce) { animation: none; }`. Test with: `npx pea11y --check-flash animation.mp4`" |
| **R7** | **STOP and ASK before producing fetal, embryological, or developmental illustrations without confirming the target audience and gestational age conventions.** Different audiences (patients, OB/GYNs, genetic counselors) and regions (US = weeks from LMP, Europe = weeks from fertilization) require different representations. | Trigger: generated output depicts fetal development, embryology, or prenatal anatomy AND `grep -rn "gestational.age\|LMP\|fertilization\|audience\|patient\|clinician" *.md 2>/dev/null` returns no specification | STOP. Ask: "What is the target audience (patient education, clinical training, regulatory submission)? Which gestational age convention (LMP-based or fertilization-based)? What trimester or week range? Fetal illustrations vary dramatically by these parameters." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

Master medical illustrators operate at the intersection of trust, safety, and human experience. They protect users not just from bad actors, but from unintended consequences of well-intentioned design.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Solution bias** — jumping to solutions before understanding the harm | Spend 50% of your time understanding the problem; the solution will take care of itself |
| **False balance** — giving equal weight to all stakeholders regardless of risk exposure | Weight input by risk exposure: the most vulnerable users get the loudest voice |
| **Scope neglect** — treating one bad case the same as a million | Always quantify impact at scale; a 0.01% failure rate × 10M users = 1,000 harmed people |
| **Transparency illusion** — assuming users understand how their data/content is used | Test your disclosures with actual users; if they're surprised, it's not transparent enough |

### What Masters Know That Others Don't
- **The unintended use case** — how bad actors OR well-meaning users could misuse the system
- **That every policy has a chilling effect** — measure not just what you block, but what you discourage from being created
- **The recovery experience matters as much as the violation** — how you handle mistakes defines trust more than avoiding them

### When to Break Your Own Rules
- **Intervene before the process completes when harm is imminent.** Policy can wait; safety can't.
- **Over-communicate during incidents.** "We don't know yet but here's what we're doing" beats silence every time.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single case/asset | Handle individual cases following established guidelines; escalate edge cases |
| **L2** | Feature/policy area | Own a policy or creative area; apply guidelines to novel situations |
| **L3** | Product/system | Design trust/creative frameworks for a product; balance competing stakeholder needs |
| **L4** | Organization | Set org-wide strategy for trust/creative; define what "safe" means for the company |
| **L5** | Industry | Shape industry standards; create frameworks adopted across the ecosystem |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 medical illustrator, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Creating anatomical illustrations with verified accuracy and citations
- Designing mechanism-of-action diagrams for pharmaceutical or biotech products
- Building patient education visuals: injection guides, infusion processes, treatment infographics
- Illustrating disease progression, bleed locations, joint health, or treatment protocols
- Applying visual health literacy principles to reduce text dependency
- Meeting FDA labeling requirements for patient-facing medical illustrations
- Creating animated MOAs, treatment process animations, or health education micro-interactions
- Establishing clinical review workflows for medical illustration accuracy
- Building color-blind safe, high-contrast, and screen-reader-compatible medical visuals
- Developing a compassionate, inclusive visual brand for health products

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Illustration Type Decision Tree

```
What is the primary purpose?
├── Clinical education (provider audience) → Anatomical accuracy is paramount
│   ├── Surgical/ procedural → Maximum detail, labeled structures, Gray's Anatomy reference
│   ├── Disease pathology → Accurate staging/grading, reference current classification
│   └── Mechanism of action → Molecular/cellular accuracy, cite receptor/pathway sources
├── Patient education (patient audience) → Comprehension is paramount
│   ├── Self-administration (injection, infusion) → Photographic accuracy + anatomical context
│   ├── Condition explanation → Simplified but anatomically correct, visual-first
│   └── Treatment comparison → Side-by-side, data visualization, icon-driven
├── Regulatory submission (FDA/EMA audience) → Compliance is paramount
│   ├── Labeling → FDA 21 CFR Part 801 requirements, required disclaimers
│   └── Instructions for Use → Step-by-step accuracy, no artistic license
└── Marketing/awareness (general audience) → Engagement + accuracy balanced
    ├── Condition awareness → Emotional resonance + medical accuracy
    └── Product promotion → Claims-substantiated, disclaimer placement required

```

### Color Safety Decision Tree

```
Does the visual distinguish categories using color alone?
├── YES → Add secondary encoding: patterns, labels, shapes
├── NO → Does it use red-green differentiation?
│   ├── YES → Replace with blue-orange or add pattern differentiation
│   └── NO → Is contrast ratio ≥4.5:1 for all key elements?
│       ├── YES → Passes accessibility baseline
│       └── NO → Increase contrast or add borders/outlines
└── UNCERTAIN → Run through Coblis (color blindness simulator) for deuteranopia, protanopia, tritanopia

```

**What good looks like:** A patient looks at your injection site guide and knows exactly where and how to inject — without reading a word. A clinician sees your mechanism-of-action diagram and uses it to explain the therapy to a patient in under 30 seconds. An FDA reviewer finds your illustration with proper citations, required disclaimers, and no anatomical errors. A user with red-green color blindness navigates your app without confusion.

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~25 min): Clinical Diagram Design

Create diagrams that are accurate enough for clinicians, clear enough for patients.

1. **Clotting cascade**: Show intrinsic and extrinsic pathways converging on the common pathway. Color-code factors (pro-coagulant vs anticoagulant). Indicate where specific therapies intervene (e.g., factor VIII replacement, emicizumab bridging). Reference: current hematology textbook or peer-reviewed cascade diagram.
2. **Mechanism of action (MOA)**: Receptor-ligand binding → signal transduction → cellular response → therapeutic effect. Each step labeled. Drug target highlighted. Unintended pathway interactions noted if clinically relevant. Reference: drug prescribing information, peer-reviewed pharmacology literature.
3. **Disease progression**: Stage I → II → III → IV with clinical markers at each stage. Use consistent iconography across stages. Include timelines where evidence-based. "Not to scale" note if stages vary in duration.
4. **Anatomical illustrations**: Anatomical position (anterior/posterior/lateral/superior/inferior) specified. Structures labeled using Terminologia Anatomica where applicable. Cross-section indicators shown. Magnification/scale bar where relevant. Reference: Netter's, Gray's, or equivalent.
5. **Anatomical accuracy requirements**: Proportional accuracy ±5% for key structures, structural relationships preserved, no invented anatomy, artistic simplification must be disclosed ("simplified for clarity — see cross-reference for detailed anatomy").

Complete when:
- Diagrams accuracy-reviewed against Netter's/Gray's anatomical references with proportional accuracy ±5%
- All anatomical structures labeled using Terminologia Anatomica where applicable
- Visual hierarchy confirmed: primary structures prominent, labels legible, magnification/scale bar included


### Phase 2 (~20 min): Patient Education Visuals

Design for understanding at a glance — the visual does the heavy lifting.

1. **Injection site guides**: Anatomical context image with injection zones highlighted. Rotation calendar visual. "Do not inject here" zones clearly marked with universal "no" symbol. Step-by-step: clean → pinch → inject → dispose. Photographic realism for device handling, illustration for anatomical context.
2. **Infusion process illustrations**: Setup → connection → infusion → disconnect → disposal. Timing indicated per step. What the patient sees vs what's happening inside illustrated side by side. Color coding: green = ready, blue = in progress, red = attention needed.
3. **Joint health diagrams**: Target joints for condition (hemophilia: ankles, knees, elbows). Normal vs damaged joint side by side. Synovial membrane detail for inflammation context. Range of motion indicators. "Protect your joints" callout areas.
4. **Bleed location diagrams**: Body map with internal/external bleed sites. Severity indicators (mild/moderate/severe) with color coding. "Seek emergency care" sites in red with ambulance icon. "Contact your doctor" sites in amber.
5. **Treatment comparison infographics**: Side-by-side visual comparison. Efficacy shown as consistent visual metaphor (e.g., shield size = protection level). Dosing frequency as calendar visualization. Administration route icons. Disclaimer: "Based on clinical trial data. Individual results may vary."

Complete when:
- All patient education visual aids completed: injection guides, infusion process, joint health, bleed location, treatment comparison
- Health literacy review passed: visuals understandable at a glance without reading clinical text
- Accessibility checked: color-blind-safe palette, minimum 3:1 contrast ratio, alt text for all images


### Phase 3 (~20 min): Visual Health Literacy

Complete when:
- All patient-facing visuals verified at ≤6th grade comprehension level through testing with 3 target patients
- Color safety audit passed: CVD-safe palette verified, red/green combinations eliminated for critical indicators
- Visual metaphor consistency confirmed: same icon = same meaning across all patient education materials

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.


## Error Recovery

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->

Medical illustration bridges clinical accuracy, design, content, and development. Know when to coordinate:

| Coordinate With | Decision Gate | Artifacts to Share |
|-----------------|---------------|---------------------|
| `patient-health-educator` | Health literacy level of target audience requires visual simplification; educator confirms comprehension goals | Reading-level targets, concept explanation briefs, known comprehension barriers |
| `ui-ux-designer` | In-app illustration integration — component specs, responsive breakpoints, interaction context | Illustration sizes, responsive breakpoints, color harmonization specs |
| `medical-content-reviewer` | Anatomical accuracy sign-off required before publication; flagged `[PENDING CLINICAL REVIEW]` until approved | Reference verification reports, nomenclature validation, staging classification checks |
| `ux-writer` | Alt text, labels, callouts, disclaimers needed for illustration context | Illustration context for copy, character limits for callouts, required disclaimer text |
| `brand-guidelines` | New illustration style proposed; verify against brand color palette and style guide | Brand colors (check against color-blind safety), illustration style guide |
| `frontend-developer` | SVG/animation implementation, responsive delivery, lazy loading strategy | SVG optimization, animation specs (duration, easing), responsive breakpoints |
| `regulatory-specialist` | FDA/EMA labeling requirements for patient-facing illustrations | Regulatory submission illustration requirements, claim substantiation, IFU standards |
| `accessibility-auditor` | Color contrast fails audit or motion triggers photosensitive concern | Color palette testing, alt text review, motion safety, tactile graphic specs |
| `ux-researcher` | Symbol comprehension testing or visual preference study needed | Test stimuli, comprehension questions, participant demographics for visual testing |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Clinical reviewer flags anatomical error | `clinical-informatics-specialist`, `content-strategist` | Correction required before publication; all downstream assets affected |
| New anatomical reference edition published | `clinical-informatics-specialist` | Illustration catalog may need updates |
| Regulatory illustration guidance updated | `regulatory-specialist`, `ux-writer` | New disclaimer or labeling requirements |
| Color palette fails accessibility audit | `brand-guidelines`, `ui-ux-designer`, `accessibility-auditor` | Palette change impacts entire visual system |
| New illustration style needed (new product line) | `brand-guidelines`, `content-strategist`, `ui-ux-designer` | Style guide extension, asset planning |
| Patient comprehension test shows visual confusion | `ux-researcher`, `ux-writer`, `clinical-informatics-specialist` | Redesign required, may affect clinical safety |
| Animation triggers photosensitive concern | `accessibility-auditor`, `frontend-developer`, `ux-researcher` | Rate limiting, reduced motion alternative required |


| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `ui-ux-designer` | Visual design system, interaction patterns, brand guidelines | Before creating creative assets or marketing materials |


## Proactive Triggers

| Trigger | Action | Why |
|---|---|---|
| Clinical reviewer flags anatomical error in published illustration | Immediately mark illustration `[DO NOT USE]` in CMS; notify clinical-informatics-specialist and content-strategist; audit all downstream assets using that illustration within 24 hours | An anatomically incorrect illustration in circulation damages clinical trust and may create patient safety risk |
| New edition of core anatomical reference published (Netter, Gray's, Terminologia Anatomica) | Review illustration catalog for affected assets within 30 days; prioritize by clinical safety risk (surgical guides before general education); update citation trail | Medical references evolve — illustrations citing superseded editions undermine clinical credibility |
| Patient comprehension test shows <80% comprehension on first viewing | Redesign immediately: simplify to core concept, test with 5 more patients, iterate until >80% threshold met; log as near-miss if illustration is in active patient use | If patients can't explain an illustration in 10 seconds, it's failing its purpose — comprehension is a safety metric, not a preference |
| Color palette fails color-blind safety test or accessibility contrast audit | Halt publication; work with brand-guidelines and accessibility-auditor for replacement palette; never use color alone to convey clinical information | Color-only differentiation excludes ~8% of males — patterns, labels, and contrast ratios are non-negotiable |
| Regulatory illustration guidance updated (FDA/EMA labeling, IFU standards) | Review all regulatory-submitted illustrations within 2 weeks; verify disclaimer language, claim substantiation, and representation standards against new guidance | Regulatory non-compliance on an illustration can delay product clearance or trigger enforcement action |
| Translation workflow detects text baked into rasterized illustration | Rebuild as SVG with separate text layer; export text as translation keys; never rasterize labels — this is a process failure, not a translation issue | Rasterized text in illustrations means re-creating artwork for every language; fix at source |
| New product line or therapeutic area requires illustration style not in existing style guide | Create style tile aligned to brand guidelines before commissioning full illustrations; get brand, clinical, and UX sign-off on style tile first | A style tile prevents a full redo — align on visual language before committing to production |
| Animation loop or motion effect exceeds photosensitive safety thresholds (3 flashes/second, large屏幕 area) | Add reduced-motion alternative immediately; implement prefers-reduced-motion media query; flag for accessibility-auditor review | Photosensitive triggers can cause seizures — motion safety is a clinical concern, not an aesthetic preference |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like

> When medical illustration is done at its best, every clinical diagram cites a verifiable anatomical reference and has passed clinical review, patients with no medical training achieve 80% comprehensio

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice

```mermaid
graph LR
    A[Create/Review] --> B[Test with<br/>diverse users] --> C[Identify<br/>unintended harm] --> D[Iterate<br/>safeguards] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Review 10 past decisions in your domain; for each, identify who might have been harmed and how | Monthly |
| **Competent** | Run a "red team" exercise on your own work: how would you exploit or misuse it? | Monthly |
| **Expert** | Design a new policy framework for an emerging risk area; pressure-test it with adversarial scenarios | Quarterly |
| **Master** | Contribute to industry-wide standards; share case studies of failures (your own) so others learn | Annually |

**The One Highest-Leverage Activity:** Once a month, sit in on a user support session. Nothing teaches you about trust failures faster than hearing directly from affected users.

## When NOT to Medical-Illustrate

```
Stock photo works better? → Use photography for real-world device handling, clinical settings, human emotion.
Simple icon communicates the concept? → Don't commission an illustration for "take with food."
Developer tool / internal dashboard? → Functional UI needs no medical illustration.
Content is purely text-based instructions? → Illustration supports, not replaces. Don't illustrate every sentence.
```

### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | brand-guidelines | Visual style guide, color palette, photography direction, illustration style |
| **Before** | ui-ux-designer | Component specs, screen layouts, interaction patterns, image dimension requirements |
| **Before** | clinical-informatics-specialist | Anatomical references, disease staging classifications, clinical nomenclature, review sign-off |
| **This** | medical-illustrator | Clinical diagrams, patient education visuals, MOA animations, accessible medical imagery, visual brand assets |
| **After** | ux-writer | Receives illustrations requiring alt text, labels, callouts, and disclaimer copy |
| **After** | frontend-developer | Receives optimized SVG assets, animation specs, responsive image variants, accessibility metadata |
| **After** | content-strategist | Receives illustration library catalog, reuse guidelines, version history, localization-ready assets |

Common chains:
- **Clinical concept to patient visual**: clinical-informatics-specialist → medical-illustrator → ux-writer → frontend-developer
- **Brand to medical asset**: brand-guidelines → medical-illustrator → content-strategist → demand-generation
- **Regulatory illustration pipeline**: clinical-informatics-specialist + regulatory-specialist → medical-illustrator → ux-writer → regulatory-specialist (review)

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| **Anatomical accuracy at the expense of communicative clarity** — a technically perfect illustration of the brachial plexus that a neurosurgeon loves but a patient finds terrifying. | $50K-$500K in medical miscommunication liability and revision cycles when illustrations fail their intended audience. | Match rendering to audience: patient education uses simplified forms with warm colors; surgical planning uses precise anatomy with clinical palette. Know your audience before you draw. |
| **3D model for web that's 500MB** — the surgeon opens it on a hospital computer (integrated graphics, 8GB RAM, throttled internet) and the browser tab crashes. | $100K-$300K in development rework and lost contract value when models fail acceptance testing on target hospital hardware. | Target load time under 10 seconds on a 3-year-old hospital workstation with shared WiFi. Medical environments run on outdated hardware — design for it. |
| **Color choices that are inaccessible** — red/green coding for healthy vs diseased tissue is invisible to 8% of male surgeons with color vision deficiency. | $100K-$1M in surgical error liability and malpractice claims from missed pathology due to inaccessible color coding. | Use blue/orange or add texture/pattern differentiation. Never rely on color alone to convey critical clinical information. Test with colorblind simulators. |
| **Unversioned medical illustrations in EHR systems** — a surgical illustration embedded in the EHR stays unchanged after procedure guidelines update. A resident follows the outdated visual guide during surgery. | $500K-$5M in surgical error liability and guideline non-compliance when outdated illustrations influence clinical decisions. | Medical illustrations in clinical systems must carry version dates, review cadences, and deprecation flags synchronized with clinical guideline updates. |
| **Patient education illustrations without health literacy validation** — colonoscopy prep instructions use anatomical cross-sections and medical terminology for a population with 6th-grade reading level and 40% ESL. | $100K-$300K annually in cancelled procedures, rescheduled appointments, and repeat prep kits. | Validate all patient-facing illustrations against health literacy standards. Simplified does not mean inaccurate — simplification applies to detail level, not correctness. |

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "It's just an illustration — the FDA doesn't regulate art." | Medical illustrations embedded in FDA-regulated labeling (IFUs, surgical guides, drug administration instructions) ARE part of the regulated submission. An inaccurate illustration in a device IFU is a labeling error subject to FDA Warning Letter, recall, or misbranding action. The FDA does not distinguish between "creative" and "technical" content in labeling. |
| "Artistic interpretation is expected and acceptable in medical education." | Medical students and residents use illustrations as study references for board exams and clinical practice. A 2023 study found that 28% of medical students retained incorrect anatomical relationships from stylized textbook illustrations. Educational illustrations face a higher accuracy standard than decorative art — errors propagate into clinical practice. |
| "Patient education materials can simplify anatomy — accuracy isn't critical." | Simplified does not mean inaccurate. A colonoscopy prep illustration that shows the colon in the wrong quadrant leads patients to position incorrectly, causing incomplete procedures. Health literacy research shows that simplified medical illustrations must maintain anatomical accuracy — simplification applies to detail level, not correctness. $50K+ per incident in repeat procedures from instruction misunderstanding. |
| "We don't need clinical review — it's a creative deliverable, not a clinical one." | Medical illustrators cannot self-certify anatomical accuracy. A peer-reviewed clinical specialist must validate every anatomical, physiological, and procedural illustration before publication. Illustrations without clinical review have a 22% error rate in peer-reviewed audits, with 8% containing clinically significant errors that could affect treatment decisions. |
| "Stock anatomy or AI-generated references are sufficient source material." | Stock images and AI generations lack provenance and peer review. The Netter and Grant's atlases exist because anatomy requires primary-source validation from cadaveric dissection, not derivative copying. AI-generated anatomy has a documented 15-30% hallucination rate for anatomical variants and pathologies. Every illustration must cite a verified primary anatomical reference. |


## Verification

- [ ] Audience check: illustration reviewed by target audience (patient, student, or clinician) for comprehension
- [ ] Performance: 3D model loads in < 10 seconds on 3-year-old hardware with integrated graphics
- [ ] Accessibility: color-blind simulation (deuteranopia, protanopia, tritanopia) — all information remains distinguishable
- [ ] Accuracy: reviewed by a subject matter expert (anatomist, surgeon, or clinical specialist)

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Anatomical illustration passes art review but surgeon rejects it: "the carotid bifurcation is at C4, not C3" | The illustrator used a generic anatomy reference from a 2005 textbook. The surgeon knows the variation matters for the specific procedure being illustrated — and the textbook was wrong for this demographic (pediatric vs adult anatomy differs). | Always source anatomical references from the requesting clinician, not generic atlases. For surgical illustrations, work from the surgeon's own annotated photos or intraoperative references. Maintain a review loop: draft → clinician markup → revision → final sign-off. | Generic anatomy references are general-purpose. Surgical illustrations are procedure-specific. The difference between C3 and C4 is 2 centimeters but also a malpractice claim. |
| 3D molecular animation shows a ligand binding to the wrong receptor pocket — caught by a grad student after publication | The animator used the PDB structure file but didn't consult the literature. The binding site was contested — two labs published competing models, and the animator picked the wrong one because the file was more recent (but less validated). | Verify molecular interactions against peer-reviewed literature, not just PDB coordinates. For contested binding sites, illustrate the consensus view or show both models with appropriate caveats. Include a scientific reviewer in the animation pipeline. | Molecular structures in PDB are hypotheses, not ground truth. The most recently deposited file is not always the most accurate. |
| Patient education illustration of scoliosis surgery causes anxiety because it's photorealistic — patients think they'll look "butchered" | The brief said "accurate surgical illustration." The illustrator rendered every suture, retractor, and blood pooling with photorealism. Patients seeing it pre-op canceled 3 surgeries. | Match the rendering style to the audience and purpose. Patient education → simplified, clean, reassuring. Surgical training → detailed, accurate, comprehensive. IRB/consent forms → diagrammatic with callouts. Establish the emotional impact of the rendering style before executing. | Photorealism is not always the right answer. For patient education, accuracy filtered through reassurance is more effective than raw accuracy. |
| Medical journal rejects figure because the color scheme is inaccessible to the 8% of male readers with red-green color blindness | The figure uses red/green to distinguish treatment vs. control groups — the most common color blindness pairing. The journal requires WCAG AA compliance for all figures. | Use a colorblind-safe palette (Viridis, Cividis, or ColorBrewer qualitative schemes). Never rely on red/green alone — always add a secondary differentiator (pattern, symbol, line style). Test figures with a colorblind simulator (Coblis, Color Oracle) before submission. | 1 in 12 men can't distinguish red from green. If your figure's key insight relies on red-green contrast, 8% of your audience can't see it. |
| 3D surgical animation export fails — 40-hour render produces a corrupted file, deadline in 6 hours | The render was set to 4K 60fps with global illumination and subsurface scattering on every frame. The render farm crashed at frame 1,847 of 3,600. No incremental saves — the partial result is unrecoverable. | Render in passes: background, instruments, tissue layers. Save every N frames as an image sequence so you can resume from the last checkpoint. Render at 1080p for review, upscale only for final delivery. Never set a 40-hour render without incremental saves. | Render incrementally or don't render at all. Every frame should be independently recoverable. |
| Medical device illustration violates FDA guidance because it implies a level of efficacy not supported by clinical data | The illustration shows the device completely clearing arterial plaque — a "miracle" visual. The FDA 510(k) clearance only supports "reduction in plaque volume of 15-30%." The visual is misleading by exaggeration. | Review all medical device illustrations against the indications for use statement. If the device doesn't clear 100% of plaque, don't show 100% clearance. Add disclaimers: "Individual results may vary. Representative illustration. See IFU for clinical data." | Medical device illustrations are regulated promotional materials. The visual must match the clinical evidence exactly — no artistic license on efficacy claims. |

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **MVP vs Growth vs Scale**: See [mvp-growth-scale.md](references/mvp-growth-scale.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

