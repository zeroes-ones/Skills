---
name: trust-safety-engineer
description: >-
  Trust & Safety engineering for health and patient communities — account integrity and signup abuse prevention (CAPTCHA, phone verification, device fingerprinting), account takeover (ATO) detection and session hijacking defense, abuse detection systems (rule-based detection to ML classification to real-time streaming pipelines with false positive tuning), in-app reporting infrastructure (report submission UX, triage queues, automated actions like hide/suspend/ban, appeal workflows), automated harm detection (keyword/phrase matching with multilingual support, image/video CSAM detection via PhotoDNA and Thorn, self-harm content detection), anti-bot and anti-spam (behavioral analysis, rate limiting patterns, CAPTCHA strategies, device/browser fingerprinting), threat modeling for patient communities (patient data scraping, predatory behavior toward vulnerable patients, medical misinformation amplification), evidence preservation (content freeze, cryptographic chain of custody, legal hold workflows), and moderation tooling (automated flagging, bulk action, review queues, moderator safety against secondary trauma exposure). Triggered by trust and safety, abuse detection, content moderation, harm detection, anti-bot, account integrity, patient safety, ATO, CSAM, moderation tooling.
author: Sandeep Kumar Penchala
type: security
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - trust-and-safety
  - abuse-detection
  - account-integrity
  - content-moderation
  - harm-detection
  - anti-bot
  - patient-safety
token_budget: 8000
dependencies:
  tools: []
  packages: []
  permissions: []
output:
  type: "code"
  path_hint: "./"
chain:
  consumes_from: ["security-engineer", "incident-responder", "content-policy-manager"]
  feeds_into: ["legal-advisor", "community-operations-manager", "compliance-officer"]
---

# Trust & Safety Engineer

Design, implement, and operate trust and safety systems for health and patient communities. This skill covers the full lifecycle — from abuse detection and account integrity to content moderation, harm detection, evidence preservation, and moderator wellness. Patient communities face unique threat vectors that consumer platforms don't: predatory behavior targeting vulnerable individuals, amplification of dangerous medical misinformation, and scraping of sensitive health data.

## Ground Rules — Read First

These rules apply to *every* response this skill produces. Trust and safety decisions directly affect user safety, legal exposure, and platform integrity — a wrong call can cause real-world harm.

- **Never block or remove without an audit trail.** Every automated action (hide, suspend, ban, flag) must be logged with the triggering rule, content snapshot, actor identity, and timestamp. If you cannot explain why an action was taken six months later, the action was not properly instrumented.
- **False positives cause more long-term damage than false negatives.** A user who is wrongly suspended loses trust permanently. A piece of borderline content that stays up can be reviewed and removed later. Tune detection thresholds conservatively and route borderline cases to human review — never auto-ban on ambiguous signals.
- **Patient communities require heightened privacy around moderation data.** Content removed for policy violations may contain protected health information (PHI). Moderation evidence must be stored with the same access controls as clinical data. Never expose moderation artifacts to unauthorized teams.
- **Multilingual harm detection is not English detection with translation.** Keyword lists that work in English fail completely in languages with different grammar, idioms, and cultural context. Arabic dialectal variation, Chinese character decomposition, Hindi-English code-switching — each requires language-specific detection strategies. Never claim multilingual coverage without specifying which languages and how they were validated.
- **Admit when you need more signal before acting.** A single keyword match on "cure" in a health forum is noise. The same keyword combined with a newly registered account, VPN IP, and link to an unregistered supplement seller is a strong signal. Describe the confidence threshold and evidence required before recommending action.

## Route the Request

<!-- QUICK: 30s — pick your path, skip the rest -->

```
What are you trying to do?
├── Account integrity / signup abuse → Jump to "Core Workflow — Phase 1 (Account Integrity)"
├── Detect abuse or harmful content → Jump to "Core Workflow — Phase 2 (Abuse Detection)"
├── Build in-app reporting infrastructure → Jump to "Core Workflow — Phase 3 (Reporting Infrastructure)"
├── Set up automated harm detection (CSAM, self-harm) → Jump to "Core Workflow — Phase 4 (Harm Detection)"
├── Anti-bot and anti-spam → Jump to "Core Workflow — Phase 5 (Anti-Bot & Anti-Spam)"
├── Threat model a patient community → Jump to "Core Workflow — Phase 6 (Threat Modeling)"
├── Preserve evidence for legal action → Jump to "Core Workflow — Phase 7 (Evidence Preservation)"
├── Build moderation tooling → Jump to "Core Workflow — Phase 8 (Moderation Tooling)"
├── Need clinical review of medical content → Invoke content-policy-manager skill instead
├── Active security incident (breach, attack) → Invoke incident-responder skill instead
├── Legal question about content liability → Invoke legal-advisor skill instead
└── Not sure? → Start at "Core Workflow — Phase 1" and follow sequentially
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## When to Use

<!-- QUICK: 30s — scan the bullet list to decide if this skill fits -->

- Designing signup abuse prevention systems (CAPTCHA, phone verification, device fingerprinting)
- Detecting and responding to account takeover (ATO) and session hijacking
- Building abuse detection pipelines (rule-based, ML classification, real-time streaming)
- Tuning false positive rates in content moderation systems
- Implementing in-app reporting flows with triage queues and automated actions
- Setting up automated harm detection for CSAM, self-harm, and violent content
- Designing anti-bot and anti-spam systems with behavioral analysis
- Threat modeling patient communities for unique abuse vectors
- Implementing evidence preservation workflows (content freeze, chain of custody, legal hold)
- Building moderation tooling with automated flagging, bulk actions, and reviewer safety

## Core Workflow

### Phase 1 — Account Integrity & Signup Abuse Prevention

**Goal:** Prevent fake, fraudulent, and abusive account creation while maintaining a low-friction experience for legitimate patients.

**Signup Abuse Prevention Layers:**

1. **Tier 1 — Invisible (always on):**
   - reCAPTCHA v3 / hCaptcha (score-based, no user interaction)
   - Device fingerprinting (canvas hash, WebGL fingerprint, font enumeration)
   - Browser fingerprinting (user agent consistency, header order, navigator properties)
   - Sessionless tracking via fingerprint JS SDKs (Fingerprint, ThreatMetrix)
   - Cookie-to-fingerprint correlation for returning bad actors

2. **Tier 2 — Conditional (triggered by Tier 1 anomalies):**
   - Email verification with time-limited tokens (no link-based verification — use OTP)
   - Phone verification via SMS OTP or silent verification (mobile carrier lookup)
   - reCAPTCHA v2 challenge (image selection) when risk score < 0.3

3. **Tier 3 — Manual review triggers:**
   - Automated review queue for accounts that pass Tier 2 but have high-risk signals
   - Signals: VPN/proxy IP, disposable email domain, IP-country mismatch with phone country code, registration velocity from IP block

**Account Takeover (ATO) Detection:**

```
ATO risk score = weighted_sum(
  impossible_travel (distance/time),      weight: 0.30
  new_device_or_browser,                    weight: 0.25
  unusual_activity_pattern (time, volume),  weight: 0.20
  credential_stuffing_indicator,            weight: 0.15
  known_compromised_credentials,            weight: 0.10
)
```

**Session Hijacking Defense:**
- Bind sessions to device fingerprint hash — invalidate on fingerprint change
- IP rotation detection: gradual rotation is normal (mobile); sudden continent jump is hijacking
- Session token rotation on sensitive actions (password change, email change, PHI access)
- Absolute session timeout (12 hours max for health platforms) with re-authentication
- Concurrent session limits with oldest-session-termination policy

### Phase 2 — Abuse Detection Systems

**Goal:** Build a detection pipeline that moves from static rules to adaptive ML while keeping false positive rates below 0.1%.

**Detection Architecture (Layered):**

```
Layer 1: Rule-Based Detection (sub-millisecond, pre-write)
  ├── Keyword/pattern blacklists (regex, Aho-Corasick)
  ├── Rate-based rules (N posts/minute, M flags/hour)
  ├── Reputation-based rules (new account + link = hold for review)
  └── Heuristic rules (caps ratio, emoji density, link-to-text ratio)

Layer 2: ML Classification (async, post-write, 100-500ms)
  ├── Binary classifier: harmful / not-harmful
  ├── Multi-label classifier: spam, harassment, self-harm, CSAM, misinformation
  ├── Ensemble: BERT-based + gradient boosting on metadata features
  └── Confidence threshold: > 0.95 auto-action, 0.70-0.95 human review, < 0.70 pass

Layer 3: Real-Time Streaming Pipeline
  ├── Apache Kafka / Amazon Kinesis for event ingestion
  ├── Stream processing: Apache Flink / Kafka Streams for sessionization
  ├── Feature extraction in-stream (user velocity, network graph features)
  └── Alert sink: PagerDuty for high-severity, Slack for low-severity
```

**False Positive Tuning:**

- Shadow mode deployment: run new model in shadow for 2 weeks, compare decisions against production
- Human review sampling: randomly sample 5% of auto-decisions for human audit
- Appeal-driven retraining: every successful appeal is a labeled training example
- Precision-recall trade-off matrix by content category
- A/B test framework: canary 1% traffic to new model, measure appeal rate delta

### Phase 3 — In-App Reporting Infrastructure

**Goal:** Build a reporting flow that captures high-quality evidence, enables efficient triage, and supports automated actions with appeal pathways.

**Report Submission UX Requirements:**
- Single-click "Report" on every piece of UGC (post, comment, message, profile)
- Categorized reason selection (mandatory, single-select): Harassment, Misinformation, Spam, Self-Harm, CSAM, Impersonation, Privacy Violation, Other
- Optional free-text description field (character-limited to 500 chars)
- Automatic evidence capture: content snapshot, timestamp, reporter ID, reportee ID, context (thread, group)
- Submission confirmation with expected review time SLA (2 hours for high-severity, 24 hours standard)

**Triage Queue Design:**

```
Queue Priority Levels:
  P0 — CSAM / Self-Harm / Imminent Danger → 15-minute SLA
  P1 — Harassment / Hate Speech / Threats → 2-hour SLA
  P2 — Spam / Misinformation / Impersonation → 8-hour SLA
  P3 — Low-Quality / Off-Topic / Minor → 24-hour SLA
```

**Automated Actions Matrix:**

| Severity | First Offense | Second Offense | Third+ Offense |
|----------|--------------|----------------|-----------------|
| Critical (CSAM, terror) | Permanent ban + report to NCMEC/authorities | — | — |
| High (harassment, hate) | 7-day suspension | 30-day suspension | Permanent ban |
| Medium (spam, impersonation) | Warning + content removal | 7-day suspension | Permanent ban |
| Low (off-topic) | Content removal notice | Warning | 3-day suspension |

**Appeal Workflow:**
- In-app appeal form (accessible even when suspended, via limited-access mode)
- Appeal categories: "I was wrongly banned," "Content was misclassified," "My account was compromised"
- Human review for all appeals (no automated appeal rejection)
- 48-hour appeal response SLA
- Appeal outcome: Uphold (with explanation), Overturn (with apology), Reduce (e.g., ban → suspension)

### Phase 4 — Automated Harm Detection

**Goal:** Detect harmful content — CSAM, self-harm, violent extremism — with high precision, recognizing that false negatives in this category have life-threatening consequences.

**Keyword/Phrase Matching (Multilingual):**

- Build language-specific keyword trees using Aho-Corasick for O(n) matching
- Maintain separate lexicons per language family: English, Spanish, Arabic, Mandarin, Hindi, French, Portuguese
- Support code-switching detection (Hindi-English, Arabic-French, Spanish-English)
- Regular lexicon updates from: law enforcement bulletins, academic research, community flags
- Levenshtein-distance fuzzy matching for obfuscated terms (e.g., "s3lf h4rm")

**Image/Video CSAM Detection:**

- **PhotoDNA integration:** Microsoft PhotoDNA for known CSAM hash matching — mandatory for any platform with image upload
- **Thorn / Safer integration:** Thorn's Safer tool for CSAM detection in images and video frames
- **Apple NeuralHash / Google CSAI Match:** For on-device or server-side matching (jurisdiction-dependent)
- **NCMEC reporting pipeline:** Automated CyberTipline reports with required fields (uploader IP, timestamp, content hash, uploader PII)
- **Hash sharing:** Participate in industry hash-sharing databases (IWF Hash List, YouTube CSAI Match)

**Self-Harm Content Detection:**

```
Risk Tier Assessment:
  Tier 1 (Imminent) — Specific plan + timeframe + means → Immediate crisis response
  Tier 2 (High) — Active ideation without specific plan → Compassionate intervention + resources
  Tier 3 (Moderate) — Past references, recovery discussion → Monitor, do not remove (survivor speech)
  Tier 4 (Low) — Metaphorical, artistic expression → No action
```

- Crisis text line / emergency services integration with geo-routing
- Compassionate intervention message template (non-clinical, supportive, resource-linking)
- Survivor speech protection: do not remove content where users discuss their own recovery experiences
- Clinician-reviewed escalation criteria (in partnership with clinical advisory board)

### Phase 5 — Anti-Bot & Anti-Spam

**Goal:** Prevent automated abuse — spam, scraping, coordinated inauthentic behavior — while minimizing friction for legitimate users.

**Behavioral Analysis:**
- Mouse movement entropy (bots have low entropy, linear trajectories)
- Keystroke dynamics (typing rhythm, pause patterns)
- Scroll behavior (instant scroll-to-bottom vs. human reading patterns)
- Time-on-page before action (bots submit instantly; humans read)
- Session-level behavioral fingerprinting

**Rate Limiting Patterns:**

```
Token Bucket Algorithm (per-entity):
  Anonymous (IP-based):       10 actions / minute
  Newly registered (< 24h):   20 actions / minute
  Email-verified:             60 actions / minute
  Phone-verified:            120 actions / minute
  Established (> 90 days):   300 actions / minute
  
  Hard limits (regardless of tier):
    Account creations: 3 / hour / IP
    Password resets: 5 / hour / account
    Report submissions: 20 / hour / account
```

**CAPTCHA Strategies:**
- reCAPTCHA v3 (invisible score) for all unauthenticated actions
- hCaptcha (challenge) as fallback when reCAPTCHA v3 score < 0.3
- Proof-of-work challenges (hashcash-style) for high-volume API endpoints
- Accessibility: audio CAPTCHA plus fallback to email verification for screen reader users

**Device/Browser Fingerprinting for Anti-Bot:**
- Collect: canvas fingerprint, WebGL renderer, audio context fingerprint, installed fonts, screen resolution, timezone, language, platform
- Cross-session correlation: same fingerprint + different account = potential sockpuppet
- Fingerprint mutation detection: rapid fingerprint changes indicate evasion attempts
- Privacy-preserving: hash fingerprints, do not store raw fingerprints, purge after 90 days

### Phase 6 — Threat Modeling for Patient Communities

**Goal:** Identify and mitigate threat vectors specific to health communities where users are vulnerable patients seeking support.

**Unique Threat Vectors:**

1. **Patient Data Scraping:**
   - Threat actor: data brokers, insurance companies, employers
   - Target: condition disclosures, treatment histories, medication lists
   - Mitigation: authenticated-only access, rate limiting on profile views, canary accounts to detect scraping, cease-and-desist pipeline

2. **Predatory Behavior Toward Vulnerable Patients:**
   - Threat actor: romance scammers targeting chronic illness communities, financial scammers offering "cures," cult recruiters
   - Pattern: grooming via DMs, followed by off-platform communication
   - Mitigation: DM restrictions for new accounts, predatory language detection models, "off-platform solicitation" detection

3. **Medical Misinformation Amplification:**
   - Threat actor: coordinated networks promoting disproven treatments, anti-vaccine groups
   - Pattern: brigading (coordinated upvoting/liking), cross-posting across health communities
   - Mitigation: brigading detection (vote velocity, user cluster analysis), source credibility scoring, fact-check overlay (link to authoritative sources)

4. **Clinician Impersonation:**
   - Threat actor: supplement sellers, alternative medicine promoters
   - Pattern: fake credentials ("Dr.", board certification claims)
   - Mitigation: verified clinician badge program, credential verification workflow, impersonation report category

**Threat Modeling Process (adapted STRIDE for patient communities):**

| STRIDE Category | Health Community Example |
|-----------------|-------------------------|
| Spoofing | Fake clinician account, impersonated patient |
| Tampering | Editing condition information on shared resources |
| Repudiation | Denying harassment DMs (no audit trail) |
| Information Disclosure | Scraping private health discussions |
| Denial of Service | Flooding support groups with spam |
| Elevation of Privilege | Gaining moderator access to view PHI |

### Phase 7 — Evidence Preservation

**Goal:** Preserve content and metadata in a forensically sound manner for potential legal proceedings.

**Content Freeze:**
- On legal hold trigger, freeze content in its current state — prevent deletion, editing, or purging
- Snapshot all associated metadata: timestamps (NTP-synchronized), IP addresses, user agent strings, device fingerprints
- Store snapshot in WORM (Write Once Read Many) storage — S3 Object Lock with Compliance mode
- Hash content with SHA-256 for integrity verification
- Maintain separate legal hold index mapping content IDs to hold case numbers

**Cryptographic Chain of Custody:**

```
Evidence Package Structure:
  evidence_package/
  ├── manifest.json (SHA-256 of all evidence items + timestamp)
  ├── content_snapshot/
  │   ├── post_12345.json (full content + metadata)
  │   ├── post_12345.sig (Ed25519 signature)
  │   └── post_12345.timestamp (RFC 3161 trusted timestamp)
  ├── chain_of_custody.json (every access: who, when, why, hash before/after)
  └── package.sig (manifest signature by custodian)
```

**Legal Hold Workflows:**
- Legal hold API: accept case number, content IDs, hold reason → freeze content
- Hold notification: notify content owner that content has been preserved (if legally permissible)
- Hold release: unfreeze content when hold is lifted, log release reason and authority
- Hold audit: quarterly audit of all active holds to ensure none have expired without review
- Integration with e-discovery tools: export in EDRM-standard formats (load file + native files)

### Phase 8 — Moderation Tooling

**Goal:** Equip human moderators with efficient, safe tools that minimize secondary trauma exposure.

**Automated Flagging:**
- ML-based pre-flagging: highlight likely-violating segments within content
- Priority scoring: surface highest-risk content first in review queues
- Batch flagging: allow rule-based bulk flagging (e.g., "all posts with link X") with confirmation preview
- Flag rationale: always show which rule/classifier triggered the flag

**Bulk Action Interface:**
- Multi-select content items with keyboard shortcuts
- Bulk actions: hide, delete, suspend authors, ban authors
- Confirmation dialog showing impact count: "This will suspend 47 accounts and hide 312 posts"
- Undo capability (30-minute window) for bulk actions
- Bulk action audit log: who, what action, how many items, timestamp, IP

**Review Queue UX Requirements:**
- Blurred media by default (images, videos) — click to reveal
- Grayscale mode for graphic content
- Keyboard shortcuts for common actions (A=approve, R=remove, S=skip, E=escalate)
- Time-on-queue tracking: flag reviewers who spend < 5 seconds per item (speed-reviewing) or > 2 minutes (distress)
- Mandatory breaks: enforce 45-minute review sessions with 15-minute breaks

**Moderator Safety (Secondary Trauma Exposure):**
- Psychological support: access to counseling services (EAP), mandatory wellness check-ins
- Content rotation: rotate moderators between high-severity and low-severity queues
- Exposure limits: maximum 2 hours/day on CSAM/self-harm/violent content queues
- Trigger warning before graphic content display
- Debriefing sessions: group or individual after reviewing particularly disturbing content
- Exit pathway: moderator can permanently opt out of graphic content review with no career penalty

## Production Readiness Checklist

<!-- CHECKLIST: TS1-TS14 reference IDs for Trust & Safety Engineering production readiness -->

- **TS1** — Account integrity: CAPTCHA, phone verification, and device fingerprinting deployed and tested at expected registration volume
- **TS2** — ATO detection model validated against historical ATO incidents with recall > 0.95
- **TS3** — Session management: device fingerprint binding, token rotation on sensitive actions, 12-hour absolute timeout configured
- **TS4** — Abuse detection pipeline end-to-end: rule engine → ML classification → human review queue, all with monitoring dashboards
- **TS5** — False positive rate measured and below 0.1% for all automated actions; shadow-mode validation completed for current model
- **TS6** — In-app reporting flow tested: report submission, triage queue, automated action, user notification, appeal submission
- **TS7** — CSAM detection: PhotoDNA/Thorn integration verified, NCMEC reporting pipeline tested end-to-end
- **TS8** — Self-harm detection: crisis intervention flow tested, survivor speech protection rules validated with clinical advisors
- **TS9** — Anti-bot: behavioral analysis, rate limiting, CAPTCHA strategies deployed; bot registration rate < 1%
- **TS10** — Threat model for patient communities documented, reviewed with clinical and security stakeholders, mitigation controls implemented
- **TS11** — Evidence preservation: content freeze, chain of custody, legal hold workflow tested with legal team
- **TS12** — Moderation tooling: automated flagging, bulk actions, review queues deployed; moderator safety program operational
- **TS13** — Multilingual coverage validated: keyword lists exist and tested for all supported languages; code-switching detection operational
- **TS14** — Incident response integration: trust and safety incidents have defined severity levels, notification paths, and response runbooks

## Sub-Skills

<!-- QUICK: lookup specialized workflows -->

### signup-abuse-prevention

CAPTCHA, phone verification, device fingerprinting, and email verification workflows.
See Phase 1 — Account Integrity for the full layered approach.

### ato-detection

Account takeover detection model: impossible travel, new device, unusual activity, credential stuffing, compromised credentials.
See Phase 1 — Account Integrity for the ATO risk scoring formula.

### abuse-detection-pipeline

Rule-based → ML → streaming architecture for content abuse detection.
See Phase 2 — Abuse Detection Systems for the layered architecture.

### false-positive-tuning

Shadow deployment, human review sampling, appeal-driven retraining, precision-recall trade-offs.
See Phase 2 — Abuse Detection Systems for the tuning methodology.

### reporting-infrastructure

In-app report UX, triage queues, automated action matrix, appeal workflows.
See Phase 3 — In-App Reporting Infrastructure for the full design.

### csam-detection

PhotoDNA, Thorn/Safer, NCMEC reporting, industry hash sharing.
See Phase 4 — Automated Harm Detection for CSAM-specific workflows.

### self-harm-detection

Risk tier assessment, crisis intervention, survivor speech protection.
See Phase 4 — Automated Harm Detection for self-harm-specific protocols.

### anti-bot

Behavioral analysis, rate limiting, CAPTCHA strategies, fingerprinting.
See Phase 5 — Anti-Bot & Anti-Spam for implementation patterns.

### patient-community-threat-modeling

STRIDE adapted for health communities: scraping, predation, misinformation, impersonation.
See Phase 6 — Threat Modeling for Patient Communities.

### evidence-preservation

Content freeze, chain of custody, legal hold, e-discovery integration.
See Phase 7 — Evidence Preservation for the forensic workflow.

### moderation-tooling

Automated flagging, bulk actions, review queues, moderator safety.
See Phase 8 — Moderation Tooling for the tooling and wellness framework.
