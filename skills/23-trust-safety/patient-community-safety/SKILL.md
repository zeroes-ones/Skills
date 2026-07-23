---
name: patient-community-safety
description: Health community safety — threat models for patient communities, medical misinformation detection patterns, health claim verification workflows, clinical escalation protocols, and vulnerable population protection. Use when building patient communities, health forums, support groups, or any platform where patients share health experiences and medical information.
author: Sandeep Kumar Penchala
type: trust-safety
status: stable
version: 1.0.0
updated: 2026-07-22
tags:
- patient-community-safety
- trust-and-safety
- health-community
- medical-misinformation
- content-moderation
chain:
  consumes_from:
  - content-policy-manager
  - crisis-response-manager
  - medical-content-reviewer
  - trust-safety-engineer
  feeds_into:
  - community-operations-manager
  - content-policy-manager
  - crisis-response-manager
  - trust-safety-engineer
token_budget: 3800
output:
  type: document
  path_hint: docs/trust-safety/
---
# Patient Community Safety

Safety frameworks for health communities where patients discuss treatment experiences, share medical information, and support each other. Different from general social app safety — the threat model includes medical misinformation that can cause physical harm, vulnerable patient populations, and regulatory liability for platform operators.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "CSAM\|self.harm\|suicide\|crisis\|safety.incident\|patient.safety")` AND `file_contains("*", "community\|patient\|health\|forum")` | This is your skill. Jump to **Core Workflow** — Phase 1 (Threat Model). |
| A2 | `file_contains("*", "misinformation\|medical.claim\|miracle.cure\|treatment.claim")` AND `file_contains("*", "detect\|classif\|automod\|ML")` | Jump to **Core Workflow** — Phase 2 (Misinformation Detection). |
| A3 | `file_contains("*", "harassment\|abuse\|troll\|coordinated\|brigade")` AND `file_contains("*", "community\|patient\|forum\|post")` | Jump to **Core Workflow** — Phase 3 (Abuse Patterns). |
| A4 | `file_contains("*", "public.health.crisis\|pandemic\|outbreak\|emergency\|CDC\|WHO")` AND `file_contains("*", "community\|patient\|safety")` | Jump to **Core Workflow** — Phase 4 (Crisis Protocols). |
| A5 | `file_contains("*", "pediatric\|adolescent\|eating.disorder\|mental.health\|rare.disease\|vulnerable")` AND `file_contains("*", "community\|safety\|protection")` | Jump to **Core Workflow** — Phase 5 (Vulnerable Populations). |
| A6 | `file_contains("*", "content.policy\|misinformation.taxonomy\|severity.tier\|enforcement.ladder")` AND NOT `file_contains("*", "detect\|classif\|automod\|safety.incident")` | Invoke **content-policy-manager** instead. This is policy design, not safety detection. |
| A7 | `file_contains("*", "GDPR\|CCPA\|HIPAA\|privacy\|consent\|data.rights")` AND `file_contains("*", "patient\|community\|safety")` | Invoke **privacy-engineer** instead. This is privacy compliance, not community safety. |
| A8 | `file_contains("*", "abuse.detection\|classifier\|PhotoDNA\|Thorn\|NCMEC\|reporting.pipeline")` AND `file_contains("*", "platform\|infrastructure\|engineering")` | Invoke **trust-safety-engineer** instead. This is detection infrastructure, not safety protocol design. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Build a threat model for a patient community → Jump to "Core Workflow" — Phase 1 (Threat Model)
├── Detect medical misinformation in patient posts → Go to "Core Workflow" — Phase 2 (Misinformation Detection)
├── Protect against harassment and coordinated abuse → Jump to "Core Workflow" — Phase 3 (Abuse Patterns)
├── Design crisis response protocols (self-harm, suicide, CSAM) → Jump to "Core Workflow" — Phase 4 (Crisis Protocols)
├── Configure safety for vulnerable populations → Jump to "Core Workflow" — Phase 5 (Vulnerable Populations)
├── Navigate HIPAA boundaries in community safety → Jump to "Decision Trees" — Privacy Boundaries
├── Need content policy taxonomy or enforcement design? → Invoke content-policy-manager instead
├── Need privacy engineering or compliance guidance? → Invoke privacy-engineer instead
├── Need detection infrastructure or ML classifiers? → Invoke trust-safety-engineer instead
└── Not sure? → Describe your community (condition, size, vulnerability profile) and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.
## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to deploy automated crisis detection without a human-in-the-loop response protocol.** Detecting a suicidal post is step one. Deleting it is step zero — the person is now more isolated. Every crisis detection must trigger: resource surface → human review → welfare follow-up. | Trigger: generated output contains `auto.detect\|auto.flag\|crisis.detection` AND NOT `human.review\|welfare.follow.up\|crisis.team\|resource.surface` within 30 lines | STOP. Respond: "Crisis detection without human response is isolation, not intervention. Before deploying: (1) define the crisis response team (who reviews flags?), (2) define the resource surfacing protocol (which hotlines/text lines per country?), (3) define the welfare follow-up process (check-in message at 24h, 7d?). Detection without response infrastructure is dangerous." |
| **R2** | **REFUSE to remove adverse event reports as 'negative content.'** A user report of a severe drug reaction is a pharmacovigilance signal, not a moderation issue. Removing it may violate FDA/EMA regulations on adverse event reporting. | Trigger: generated output proposes removing/hiding content AND content matches `grep -cP "(severe (reaction\|side.effect)\|hospitalized\|almost died\|ER visit\|anaphylaxis)"` AND `grep -rn "pharmacovigilance\|MedWatch\|FDA.report\|adverse.event" moderation_workflow.md` returns 0 results | STOP. Respond: "This content contains a potential adverse event report. It must NOT be removed — it must be flagged for pharmacovigilance review. Route to: (1) preserve content in PV archive, (2) flag for MedWatch/FDA reporting if applicable, (3) flag for clinical safety review. Removing adverse event reports is a regulatory violation." |
| **R3** | **REFUSE to apply general-purpose abuse detection models to health communities without domain-specific fine-tuning.** A model trained on general social media will flag "I want to die" (common chemotherapy frustration) and "fuck cancer" (community bonding) as toxic content with 40%+ false positive rates. | Trigger: generated output references `pre.trained.model\|general.classifier\|off-the-shelf\|transfer.learning` AND NOT `domain.specific\|health.context\|patient.vernacular\|community.fine.tuning` within 50 lines | STOP. Respond: "General-purpose abuse classifiers fail catastrophically in health communities. Before deploying: (1) build a golden dataset of 10,000+ labeled examples from YOUR specific community, (2) include patient advocates in the labeling process, (3) measure false positive rates for health-specific phrases ('I want to die,' 'this is killing me,' 'fuck cancer'). Target <0.1% false positive rate on health-context content." |
| **R4** | **REFUSE to design pediatric or mental health community safety with the same defaults as general health communities.** Default-open communities fail vulnerable populations. Pediatric communities need: DM restrictions ON by default, contact from unknown adults blocked, enhanced privacy defaults. Mental health communities need: crisis detection with <5 minute response, trigger warnings, no algorithmic amplification of distressing content. | Trigger: generated output proposes community safety config AND `file_contains("*", "pediatric\|adolescent\|mental.health\|eating.disorder\|self.harm")` AND NOT `enhanced.defaults\|DM.restriction\|adult.contact.block\|crisis.detection\|trigger.warning` within 30 lines | STOP. Respond: "This safety configuration uses general defaults for a vulnerable population community. For [pediatric/mental health] communities, enhanced defaults are mandatory: [list specific defaults]. General community safety settings applied to vulnerable populations are inadequate by design." |
| **R5** | **DETECT and WARN about crisis detection systems without a maximum false positive budget.** A crisis system with 90% precision at 200 flags/day produces 20 false positives daily. Over months, moderator alarm fatigue destroys attention. Set max 10 crisis flags per moderator per day. | Trigger: generated output describes `crisis.detection\|self.harm.flag\|suicide.detection` AND NOT `false.positive.budget\|max.flags.per.moderator\|alarm.fatigue\|flag.cap` within 30 lines | WARN: "This crisis detection system has no false positive budget. Configure: max 10 crisis flags per moderator per day. If volume exceeds this, raise the confidence threshold. A system that flags everything catches nothing — because the human in the loop stops paying attention. Measure 'time-to-dismiss' for false positives — if it's dropping, alarm fatigue is setting in." |
| **R6** | **DETECT and WARN about block/visibility features that can be weaponized for coordinated silencing.** Block features, when used by coordinated groups, become harassment tools. Monitor for: 20+ accounts created within 48 hours all blocking the same users. Design engagement algorithms to account for 'suspicious disengagement.' | Trigger: generated output describes `block.user\|hide.content\|visibility.control\|mute` without `abuse.vector\|coordinated.block\|weaponization\|suspicious.disengagement` within 30 lines | WARN: "User-controlled visibility features are abuse vectors. Add: (1) coordinated blocking detection (20+ new accounts blocking same users within 48h → flag), (2) 'suspicious disengagement' handling in ranking algorithms, (3) appeal mechanism for users whose reach suddenly drops due to coordinated blocking. A block feature without abuse detection is a harassment tool." |
| **R7** | **STOP and ASK before collecting mental health symptom data without specific, unbundled consent.** "We may share your data for research" is not informed consent for selling de-identified datasets to pharmaceutical companies. Health data consent must specify: who, what purpose, and opt-in per use case. | Trigger: generated output proposes `data.collection\|symptom.tracking\|mood.data\|health.data` AND NOT `specific.consent\|per.purpose.opt.in\|unbundled\|pharma.disclosure` within 30 lines | STOP. Ask: "This design collects sensitive health data. The consent flow must: (1) specify each data use purpose separately, (2) disclose if data may be shared with pharmaceutical companies or researchers, (3) allow opt-in per purpose (not bundled), (4) never combine ZIP + age + gender + diagnosis in shared datasets (re-identifiable with public data). A consent that's legally compliant but feels like a betrayal is a trust breach." |
## The Expert's Mindset

Master patient community safetys operate at the intersection of trust, safety, and human experience. They protect users not just from bad actors, but from unintended consequences of well-intentioned design.

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
**Usage:** Invoke this skill with your target level, e.g., "as an L3 patient community safety, design..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use
<!-- QUICK: 30s — scan the bullet list to decide -->

- Launching a patient community or health forum — safety infrastructure before first user
- Adding user-generated content to a health app — content moderation framework needed
- Detecting medical misinformation at scale — automated claim verification patterns
- Responding to a public health crisis (pandemic, drug recall) in your community
- Building for vulnerable populations (pediatric, mental health, rare disease, elderly)
- Preparing for platform liability review — documenting safety controls for legal/regulatory
- A community member shares suicidal ideation or reports a severe adverse event

## Decision Trees
<!-- STANDARD: 3min -->

### Content Risk Classification

```
What type of health claim is being made?
├── Personal experience: "I tried X and it helped me"
│   → LOW RISK (if clearly personal, not prescriptive)
│   → Action: No removal. Consider "personal experience" label.
│
├── Treatment recommendation: "You should try X for condition Y"
│   → HIGH RISK (prescriptive, unverified)
│   → Action: Flag for clinical review. Remove if not evidence-based.
│
├── Anti-established-treatment: "Stop taking your medication, try this instead"
│   → CRITICAL RISK (direct harm potential)
│   → Action: Immediate removal. User warning. Repeat = ban.
│
├── Commercial/promotional: "Buy my supplement — cures condition Y"
│   → CRITICAL RISK (scam/fraud + health harm)
│   → Action: Immediate removal + account suspension. Report if illegal.
│
├── Crisis/emergency: "I want to end my life" or "I'm having a severe reaction"
│   → EMERGENCY — NOT a moderation decision
│   → Action: Crisis protocol. Do NOT just remove. Escalate immediately.
│
└── Question: "Has anyone tried X for Y? What was your experience?"
    → LOW RISK (information-seeking, not prescriptive)
    → Action: Allow. Monitor responses for prescriptive advice.
```

### Privacy Boundary Enforcement

```
Does this content contain...
├── Full name + health condition → PHI → Remove or anonymize
├── Email/phone + "I have condition X" → PHI → Remove or anonymize
├── Location + rare disease → Potentially identifying → Warn user, offer anonymization
├── "I have hemophilia" (no identifiers) → NOT PHI → Allow
├── Photo with face + medical context → PHI → Remove or warn
└── Doctor/facility name + complaint → Not PHI but potential legal → Flag for review
```

### Escalation Decision Tree

```
Detected content issue...
├── Medical misinformation (non-urgent) → Flag → Clinical reviewer within 24h → Remove/edit/allow
├── Medical misinformation (actively harmful) → Immediate takedown → Clinical reviewer within 2h → Restore or confirm removal
├── Scam/fraud (supplement, cure) → Immediate takedown + account suspension → Report to FDA/FTC if applicable
├── Harassment/bullying of patient → Remove content → Warning → Repeat = ban → Check on targeted user
├── Self-harm/suicidal ideation → Crisis protocol: DO NOT REMOVE → Escalate to crisis team → Provide resources
├── Child safety concern → Immediate report to NCMEC (if US) → Account suspension → Legal review
└── Adverse event (drug reaction) → Flag for pharmacovigilance → Report to FDA MedWatch if applicable → Do NOT remove (regulatory requirement)
```

## Core Workflow
<!-- STANDARD: 5min -->

### Phase 1: Threat Modeling (~1 week)

Health communities have a different threat model than general social apps. Map yours specifically:

```markdown
## Health Community Threat Model for [Platform Name]

### Assets to Protect
- Patient physical safety (from bad medical advice)
- Patient emotional safety (from harassment, bullying)
- Patient privacy (PHI exposure)
- Clinical accuracy of shared information
- Community trust (platform credibility)
- Regulatory compliance (HIPAA, FDA, FTC)

### Threat Actors
1. **Well-meaning misinformer** — Patient sharing something that worked for them but is dangerous
2. **Commercial scammer** — Selling unproven treatments, supplements, "cures"
3. **Anti-medicine activist** — Organized effort to discourage evidence-based treatment
4. **Predator** — Targeting vulnerable patients for exploitation
5. **Troll/harasser** — Targeting patients based on their health conditions
6. **Data harvester** — Scraping patient community for PHI/sensitive data

### Attack Vectors
- Public forum posts (highest volume, most visible)
- Private messages (hardest to detect, highest harm potential)
- User profiles/bios (often overlooked in moderation)
- External links (can lead to harmful content off-platform)
- Images/media (medical images can be PHI, can contain harmful advice)
```

### Phase 2: Medical Misinformation Detection (~2 weeks)

Build automated detection with clinical review escalation:

```python
# app/services/misinformation_detection.py
from enum import Enum
from typing import Optional

class ClaimRisk(Enum):
    LOW = "personal_experience"
    MEDIUM = "unverified_claim"
    HIGH = "treatment_recommendation"
    CRITICAL = "anti_established_treatment"

class MisinformationDetector:
    """Pattern-based detection — AI-assisted, human-reviewed."""

    # High-risk patterns: prescriptive language about treatment
    PRESCRIPTIVE_PATTERNS = [
        r"( stop|quit|don't take|never take)\s+(your|the)\s+(medication|meds|drug|treatment)",
        r"(try|use|take)\s+(this|these)\s+(instead|rather than)\s+(your|the)\s+(medication|treatment)",
        r"(cure|heal|fix|reverse)\w*\s+(your|the)\s+(cancer|diabetes|hemophilia|condition)",
        r"(doctors?|they)\s+(don't want|won't tell|are hiding)\s+(you|patients?)",
    ]

    # Medium-risk: unverified treatment claims
    UNVERIFIED_CLAIM_PATTERNS = [
        r"(I|you|they)\s+(should|must|need to|have to)\s+(try|take|use)\s+[\w\s]+for",
        r"(studies?|research)\s+(shows?|proves?)\s+that\s+[\w\s]+(cures?|treats?|heals?)",
        r"(natural|cure|remedy)\s+for\s+(your|the)\s+(condition|disease|symptoms?)",
    ]

    def classify_risk(self, content: str) -> tuple[ClaimRisk, Optional[str]]:
        """Classify content risk level. Returns (risk, matched_pattern)."""
        for pattern in self.PRESCRIPTIVE_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return ClaimRisk.CRITICAL, pattern

        for pattern in self.UNVERIFIED_CLAIM_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return ClaimRisk.HIGH, pattern

        # Check for personal experience sharing (low risk)
        if re.search(r"(in my experience|I found that|for me personally|helped me)", content, re.IGNORECASE):
            return ClaimRisk.LOW, None

        return ClaimRisk.MEDIUM, None

    def get_moderation_action(self, risk: ClaimRisk, user_history: dict) -> str:
        """Determine moderation action based on risk and user history."""
        actions = {
            ClaimRisk.LOW: "allow_with_label",
            ClaimRisk.MEDIUM: "flag_for_clinical_review",
            ClaimRisk.HIGH: "quarantine_pending_review",
            ClaimRisk.CRITICAL: "immediate_removal",
        }

        # Escalate repeat offenders
        if risk in (ClaimRisk.HIGH, ClaimRisk.CRITICAL):
            if user_history.get('previous_warnings', 0) >= 2:
                return "suspend_account"
            if user_history.get('previous_removals', 0) >= 1:
                return "suspend_account"

        return actions[risk]
```

### Phase 3: Abuse Pattern Detection for Health Communities (~1 week)

```python
# app/services/health_community_abuse.py

class HealthCommunityAbuseDetector:
    """Detect abuse patterns specific to health communities."""

    # Predatory patterns targeting vulnerable patients
    PREDATORY_PATTERNS = [
        r"(DM|message|PM)\s+me\s+(for|if you want|to get)\s+(help|advice|treatment|cure)",
        r"(I can help you|I can cure|I can treat)\s+(your|the)\s+(condition|disease)",
        r"(contact|email|call|text)\s+me\s+(at|on)\s+\d{3}",
    ]

    # Harassment based on health condition
    CONDITION_HARASSMENT_PATTERNS = [
        r"( it's your own fault| you deserve| you brought this on)",
        r"(just exercise|just eat better|just think positive)\s+(and|to)\s+(cure|fix)",
        r"you('re| are)\s+(faking|exaggerating|pretending)",
    ]

    # Data harvesting (trying to collect PHI from community members)
    DATA_HARVESTING_PATTERNS = [
        r"(what's your|share your)\s+(diagnosis|treatment|medication|doctor|hospital)",
        r"(survey|research study|clinical trial)\s+(about|for)\s+(your|patients? with)",
        r"(email|phone|address)\s+(so I can|to)\s+(send|share|contact)",
    ]

    def detect_abuse(self, content: str, context: dict) -> dict:
        """Returns abuse classification and confidence."""
        # Check context: PM vs public post, user relationship, new account
        if context.get('channel') == 'private_message':
            confidence_multiplier = 1.5  # PMs are higher risk
        else:
            confidence_multiplier = 1.0

        results = []

        for pattern in self.PREDATORY_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                results.append({'type': 'predatory', 'confidence': 0.7 * confidence_multiplier})

        for pattern in self.CONDITION_HARASSMENT_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                results.append({'type': 'condition_harassment', 'confidence': 0.8 * confidence_multiplier})

        for pattern in self.DATA_HARVESTING_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                results.append({'type': 'data_harvesting', 'confidence': 0.6 * confidence_multiplier})

        return {'flags': results, 'action': self._determine_action(results, context)}

    def _determine_action(self, results: list, context: dict) -> str:
        if not results:
            return 'allow'
        high_conf = [r for r in results if r['confidence'] > 0.8]
        if any(r['type'] == 'predatory' for r in high_conf):
            return 'suspend_account'
        if high_conf:
            return 'remove_content_and_warn'
        return 'flag_for_review'
```

### Phase 4: Crisis Protocol Implementation (~1 week)

```python
# app/services/crisis_response.py

class HealthCrisisProtocol:
    """Protocols for health emergencies detected in community content."""

    CRISIS_KEYWORDS = [
        "kill myself", "end my life", "suicide", "want to die",
        "no reason to live", "better off dead", "can't go on",
        "severe allergic reaction", "anaphylaxis", "can't breathe",
        "overdose", "took too many", "severe bleeding",
        "won't stop bleeding", "hemorrhaging",
    ]

    CRISIS_RESOURCES = {
        'US': {
            'suicide': '988 Suicide & Crisis Lifeline — Call or text 988',
            'crisis_text': 'Text HOME to 741741',
            'emergency': 'Call 911 or go to nearest emergency room',
        },
        'UK': {
            'suicide': 'Samaritans — Call 116 123',
            'crisis_text': 'Text SHOUT to 85258',
            'emergency': 'Call 999 or go to nearest A&E',
        },
        'EU': {
            'suicide': 'EU emergency number: 112',
            'emergency': 'Call 112',
        },
    }

    async def handle_crisis_detection(self, content: str, user_context: dict) -> dict:
        """
        When crisis content is detected, this is NOT a moderation action.
        This is an emergency response. DO NOT simply remove the content.
        """
        crisis_type = self._classify_crisis(content)
        country = user_context.get('country', 'US')
        resources = self.CRISIS_RESOURCES.get(country, self.CRISIS_RESOURCES['US'])

        response = {
            'crisis_type': crisis_type,
            'immediate_action': 'surface_resources_in_app',
            'escalation': 'notify_crisis_team',
            'content_action': 'do_not_remove',  # Preserve for potential welfare check
            'user_message': self._craft_crisis_message(crisis_type, resources),
            'internal_actions': [
                'Log incident for compliance',
                'Notify designated crisis response team member',
                'If pediatric: follow mandatory reporting requirements',
            ]
        }
        return response

    def _craft_crisis_message(self, crisis_type: str, resources: dict) -> str:
        """Message shown to user in crisis. Must be supportive, not clinical."""
        if crisis_type == 'suicide':
            return (
                "We care about your safety. If you're thinking about suicide, "
                "please reach out for support right now:\n\n"
                f"📞 {resources['suicide']}\n"
                f"💬 {resources.get('crisis_text', '')}\n"
                f"🚨 {resources['emergency']}\n\n"
                "You are not alone. These services are free, confidential, "
                "and available 24/7."
            )
        # ... other crisis types
```

### Phase 5: Vulnerable Population Protection (~1 week)

```markdown
## Default Protections by Population

### Pediatric Patients (under 18)
- Account requires parental consent (COPPA + health privacy)
- Private messages disabled by default
- Content visibility: community members only (not searchable)
- No direct messaging from adults not in their "care circle"
- Automated detection: grooming patterns, inappropriate contact

### Mental Health Communities
- Trigger warning system for potentially distressing content
- No graphic self-harm content (remove + provide resources)
- Crisis keywords → automatic resource surface (not just flag)
- Anti-bullying protections enhanced (condition-based harassment)
- "Take a break" prompts after extended browsing of heavy content

### Rare Disease Communities
- Small community → bad actors have outsized impact
- Higher trust needed → verified patient status (self-attested + community validated)
- Misinformation more dangerous (fewer alternative information sources)
- Expert-verified content badges for clinician-reviewed posts

### Elderly Patients
- Simplified reporting flows (one-click "this seems wrong")
- Phone-based support option (not everyone uses chat)
- Scam detection enhanced (elderly are primary targets for health scams)
- Large text, clear language in safety communications
```

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What to Expect | Communication Trigger |
|---------------|----------------|---------------------|
| `trust-safety-engineer` | Abuse detection infrastructure, automated harm detection, anti-bot measures | When building automated moderation pipelines |
| `content-policy-manager` | Community guidelines, medical misinformation definitions, escalation frameworks | When defining what content violates policy |
| `medical-content-reviewer` | Clinical accuracy review, evidence-based medicine standards, treatment claim validation | When escalating content for clinical review |
| `crisis-response-manager` | Crisis escalation frameworks, adverse event protocols, emergency response | When crisis content is detected |

| Downstream Skill | What to Deliver | Communication Trigger |
|-----------------|-----------------|---------------------|
| `community-operations-manager` | Safety protocols, moderation workflows, crisis response procedures | When operationalizing community safety |
| `content-policy-manager` | Health-specific threat models, vulnerable population protections | When writing/updating community guidelines |
| `crisis-response-manager` | Health crisis detection patterns, patient-specific response protocols | When building crisis response infrastructure |
| `trust-safety-engineer` | Health community abuse patterns, medical misinformation detection code | When implementing automated safety systems |

## Proactive Triggers
<!-- STANDARD: 2min — surface these WITHOUT being asked -->

- **Treatment recommendation without evidence** → "You should stop taking [medication] and try [alternative]." Flag immediately. Prescriptive medical advice from non-clinicians is the #1 harm vector. 🔴
- **New user sends DMs to multiple patients** → A 1-day-old account messaging 5+ community members. Classic predatory pattern. Auto-flag and rate-limit. 🔴
- **External link to supplement/treatment seller** → Links to unverified treatment products. Check against FDA warning letters, FTC actions. Quarantine pending review. 🔴
- **Self-harm language in any context** → "I can't do this anymore," "I want to end it." Not a moderation decision — this is a crisis response. Surface resources immediately. 🔴
- **"Doctors are hiding this cure" narrative** → Anti-established-medicine content. High engagement bait, high harm potential. Flag for clinical review. 🟡
- **"DM me for the real solution"** → Attempt to move conversation off-platform for predatory purposes. Auto-flag. High confidence = immediate suspension. 🟡
- **Identifiable photo in medical context** → Patient photo + condition details = PHI. Offer anonymization option. Remove if not anonymized. 🟡
- **Vulnerable population targeted** → Account targeting pediatric, mental health, or rare disease communities with unsolicited treatment advice. Enhanced scrutiny. 🟠

## Best Practices
<!-- STANDARD: 3min -->

1. **Tiered moderation: automated → clinical review → human judgment.** Automation catches patterns. Clinical reviewers validate medical accuracy. Human moderators handle nuanced cases. No single layer is sufficient.
2. **Crisis content is NEVER just removed.** A post about suicidal ideation that gets deleted by an algorithm leaves the person MORE isolated. Surface resources, escalate to crisis team, preserve the content for welfare follow-up.
3. **Personal experience ≠ medical advice.** "This worked for me" is different from "You should do this." Label personal experiences. Remove prescriptive advice from non-clinicians.
4. **Adverse events are regulatory reports, not content to moderate.** If a user reports a severe drug reaction, you have pharmacovigilance obligations. Flag for MedWatch/FDA reporting. Do NOT remove.
5. **Repeat education before punishment.** First-time well-meaning misinformers get education + content removal. Repeat offenders get escalating consequences. Scammers get banned immediately.
6. **Vulnerable populations get enhanced defaults.** Pediatric, mental health, and rare disease communities should have stricter privacy defaults, DM restrictions, and content filtering ON by default.
7. **Transparency builds trust.** When content is removed, tell the user why. "This post was removed because it made a medical claim that could not be verified. Our clinical review team determined..." Opacity breeds conspiracy theories.
8. **Safety metrics are community health metrics.** Track: misinformation prevalence, time-to-detection, crisis response time, user reports per 1K posts. These ARE your community health dashboard.

## Anti-Patterns
<!-- MACHINE-EXECUTABLE: Each row has a grep/lint pattern for detection and auto-prevention -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep/lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| "We'll use the same moderation as Reddit/Facebook" | Health communities need clinical review escalation + medical misinformation detection. General social moderation isn't sufficient for content that can cause physical harm | `grep -rn "standard.moderation\|generic\|off.the.shelf\|one.size" safety_config.yaml` → matches = flag | **Health-context lint**: CI rule `npx validate-safety-config safety_config.yaml --require "clinical_review\|misinformation_detection\|crisis_protocol"` |
| Auto-deleting crisis content without human follow-up | Crisis content gets: immediate resource surface → human review → welfare follow-up. Automation triggers response, not deletion | `grep -rn "auto.delete\|auto.remove\|auto.hide.*crisis\|auto.hide.*suicide" moderation_rules.yaml` → matches = block | **Crisis response lint**: CI rule `npx validate-moderation-rules moderation_rules.yaml --forbid-auto-delete "suicide\|self.harm\|crisis"` |
| "Free speech" absolutism in health communities | "Free speech" doesn't include telling someone to stop their chemotherapy. Health communities have a duty of care that overrides absolute free expression | `grep -rn "free.speech\|absolute.free.expression\|no.censorship" guidelines.md` → matches without `duty.of.care\|harm.prevention\|clinical.safety` = flag | **Duty-of-care lint**: CI rule `npx validate-guidelines guidelines.md --require-duty-of-care --health-context` |
| Moderating without clinical expertise available | At minimum, have a clinical advisor on retainer for content appeals. At scale, hire clinical content reviewers. Non-clinicians shouldn't make final medical accuracy determinations | `grep -rn "clinical.advisor\|medical.review\|clinical.reviewer" moderation_team.yaml` → 0 matches = fail | **Clinical expertise gate**: CI rule `npx validate-moderation-team moderation_team.yaml --require-clinical-advisor --min-advisors 1` |
| One-size-fits-all safety for all community segments | Pediatric, mental health, rare disease, and elderly communities each need tailored protections. What's safe for a general health forum may be unsafe for teens with eating disorders | `grep -rn "pediatric\|adolescent\|mental.health\|eating.disorder" safety_config.yaml` → 0 matches when `grep -rn "segment\|sub.community" community_config.yaml` shows segments exist = fail | **Segment-specific safety lint**: CI rule `npx validate-safety-config --per-segment --require "pediatric\|mental_health\|rare_disease" protections for each segment type` |
| Removing adverse event reports as "negative content" | Adverse event reports are legally required to be preserved and reported. Removing them can violate FDA regulations. Flag for pharmacovigilance, not moderation | `grep -rn "delete.*adverse\|remove.*side.effect\|hide.*reaction" moderation_rules.yaml` → matches = block | **PV-protection lint**: CI rule `npx validate-moderation-rules moderation_rules.yaml --require-pv-flag "adverse.event\|side.effect\|reaction\|hospitalized"` |
| Waiting for user reports to detect problems | By the time a user reports harmful medical advice, 100 people have already seen it. Automated detection must catch prescriptive medical claims BEFORE they spread | `grep -rn "user.report\|community.flag\|report.based" detection_strategy.md` when NOT accompanied by `automated.detection\|proactive\|pre.report` = flag | **Proactive detection gate**: CI rule `npx validate-detection-strategy detection_strategy.md --require-proactive --max-detection-latency "5 minutes"` |
| Moderator wellness treated as an HR perk rather than operational requirement | Mandatory exposure time limits (max 2 hours/day on graphic queues), content rotation, wellness check-ins, counseling access, and exit pathways with no career penalty | `grep -rn "moderator.wellness\|exposure.limit\|content.rotation\|trauma.support" moderator_program.md` → matches < 4 = fail | **Moderator safety lint**: CI rule `npx validate-moderator-program moderator_program.md --require-wellness --min-elements 4` |
## Error Decoder
<!-- MACHINE-EXECUTABLE: First column is exact grep regex for console/log matching -->

| 🖥️ Console Match (grep regex) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep -cP "crisis.flag\|suicide.detect\|self.harm.detect" crisis_queue.csv` → `daily_volume > 200` AND `grep -cP "dismiss.time\|review.duration" moderator_metrics.csv` → `avg_dismiss_ms < 500` | 200+ crisis flags/day, moderators dismissing in <500ms — alarm fatigue: real crises being dismissed along with false positives | Crisis detection threshold set to maximize recall at expense of precision. 90% precision at 200 flags/day = 20 false positives daily. Over months, moderator attention destroyed | Set max 10 crisis flags per moderator per day. Raise confidence threshold if volume exceeds this. Rotate crisis review duty weekly. Measure time-to-dismiss — if dropping, enforce mandatory review time (minimum 30 seconds per flag) | **1.** Measure crisis queue health: `npx measure-crisis-queue --metrics "daily_volume,avg_dismiss_ms,precision"`. **2.** If `daily_volume > 10 * moderator_count`: `npx raise-crisis-threshold --target-daily 10`. **3.** Enforce minimum review time: `npx enforce-min-review-time --seconds 30 --queue crisis`. **4.** Rotate reviewers: `npx rotate-crisis-reviewers --frequency weekly`. **5.** Monitor weekly: `npx monitor-alarm-fatigue --alert-on dismiss_ms_drop_20pct` |
| `grep -cP "blocked.*user\|coordinated.*block\|mass.block" incident_log.json` → `count > 0` AND `grep -cP "coordinated.block.detection\|suspicious.disengagement" safety_config.yaml` → `0` | Coordinated group mass-blocked LGBTQ+ patients — their posts disappeared from community feeds and trending algorithms | Block feature treated as personal safety tool, not abuse vector. 200 coordinated accounts blocked all active LGBTQ+ members. Trending algorithm penalized blocked users' reduced engagement | Add coordinated blocking detection. Design engagement algorithms to exclude suspicious disengagement. Provide appeal mechanism for users whose reach drops suddenly due to coordinated blocking | **1.** Detect coordinated blocks: `npx detect-coordinated-blocks --threshold 20 --window-hours 48`. **2.** If detected: `npx freeze-blocked-users-reach --incident-id $ID` → preserve their pre-block reach in ranking. **3.** Remove blocking accounts: `npx bulk-suspend --account-ids blocked_accounts.json --reason coordinated_harassment`. **4.** Restore visibility: `npx restore-reach --user-ids targeted_users.json`. **5.** Deploy detection permanently: `npx deploy-coordinated-block-detection --production` |
| `grep -cP "adverse.event\|side.effect\|reaction.*severe\|ER.visit" removed_content.csv` → `count > 0` | Adverse event reports removed as "negative content" — potential FDA regulatory violation | Moderation workflow doesn't distinguish adverse events from negative sentiment. No pharmacovigilance flagging. Content moderators making PV decisions without training | Flag all potential adverse events for PV review BEFORE any moderation action. Preserve original content in PV archive. Route to pharmacovigilance team, not moderation queue | **1.** Audit removed content for AEs: `grep -cP "(severe.reaction\|side.effect\|hospitalized\|ER.visit\|almost.died\|anaphylaxis)" removed_content.csv` → if `> 0`, flag. **2.** Restore content: `npx restore-content --ids ae_removed.csv --reason potential_adverse_event`. **3.** Route to PV: `npx route-to-pv --content-ids ae_removed.csv --priority high`. **4.** Update workflow: `npx add-pv-flag-rule --keywords "adverse.event,side.effect,reaction" --action "flag_not_remove"`. **5.** Train moderators: `npx train-moderators --module pharmacovigilance --cases 20` |
| `grep -cP "teen\|adolescent\|minor\|under.18" community_config.yaml` → `count > 0` AND `grep -cP "DM.restriction\|adult.contact\|enhanced.privacy" community_config.yaml` → `0` | Pediatric community running with adult-default safety settings — DMs open, adult contact unrestricted, privacy defaults permissive | Platform used same safety configuration for all communities. No age-appropriate defaults. Pediatric community treated identically to general health forum | Apply enhanced defaults: DM restrictions ON, adult contact from unknown users blocked, profile visibility restricted, content sharing disabled by default. Add age verification gate for adult members interacting with pediatric spaces | **1.** Audit pediatric safety: `npx audit-pediatric-safety --community-id $(cat .community_id)`. **2.** Enable DM restrictions: `npx set-defaults --community-id $(cat .community_id) --dm_restricted true --adult_contact_blocked true`. **3.** Add age verification: `npx add-age-verification-gate --community-id $(cat .community_id)`. **4.** Audit existing adult members: `npx audit-adult-members --community-id $(cat .community_id) --review-dm-history`. **5.** Publish updated safety notice to community |
| `grep -cP "I want to die\|kill myself\|end it all" auto_removed.csv` → `false_positive_rate > 0.40` | 40%+ of posts auto-removed for self-harm keywords are recovery discussions, survivor stories, or crisis counselor responses | General-purpose classifier trained on non-health social media. "I used to want to kill myself every day, but therapy saved my life" = removed. Crisis counselor replies with hotline numbers = removed | Deploy health-context classifier. Build golden dataset from YOUR community. Distinguish: active ideation (Tier 1: plan + timeframe + means), past reference (Tier 3: recovery), support/counseling (not harmful). Validate with clinical advisors before deployment | **1.** Audit false positives: `grep -cP "(used to\|recovery\|survivor\|therapy.saved\|hotline)" auto_removed.csv` → if `> 0.20`, disable classifier. **2.** Build golden dataset: `npx create-golden-dataset --community-id $(cat .community_id) --size 10000 --labels "active_ideation,past_reference,recovery,support,not_harmful"`. **3.** Train health-context model: `npx train-classifier --dataset golden_dataset.json --context health`. **4.** Validate with clinicians: `npx clinical-validation --model health_context_v1 --reviewers 3`. **5.** Deploy in shadow mode for 2 weeks before enforcement |
| `grep -cP "access.locked\|account.suspended\|ATO.block" incident_log.json` → `hospital_ip > 0` AND `grep -cP "emergency.access\|read.only.mode\|caregiver" acl_config.yaml` → `0` | Caregiver locked out of patient portal while patient in surgery — treatment decision delayed 24 hours | ATO detection treated "new device + hospital IP" as suspicious. No emergency access path for caregivers. Phone verification impossible when patient is in surgery | Distinguish "new device + hospital IP range" = caregiver in medical emergency, not attacker. Implement read-only emergency access mode: view results/meds without full account access, triggered by security questions | **1.** Audit ATO blocks at medical IPs: `grep -cP "hospital\|medical.center\|clinic" ato_block_log.json` → if `> 0`, flag. **2.** Implement emergency access: `npx add-emergency-access-mode --read-only --auth security_questions`. **3.** Whitelist medical IP ranges: `npx add-ato-exception --ip-range hospital_ranges.json --context medical_emergency`. **4.** Test: `npx test-emergency-access --scenario caregiver_hospital`. **5.** Deploy: `npx deploy-emergency-access --production` |
## Production Checklist
<!-- MACHINE-EXECUTABLE: Every item has an exact CLI validation command and auto-fix path -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **PS1** | Health community threat model documented — assets, threat actors, attack vectors | `grep -cP "threat.model\|asset\|threat.actor\|attack.vector" threat_model.md` must be `>= 4` | `npx init-threat-model --domain health_community --output threat_model.md` |
| **PS2** | Automated medical misinformation detection deployed — prescriptive claim patterns detected proactively | `curl -s http://localhost:${PORT}/api/detection/misinfo/status \| jq '.precision'` must be `>= 0.85` AND `jq '.proactive'` must be `true` | `npx deploy-misinfo-detection --mode shadow --min-precision 0.85 --health-context` |
| **PS3** | Clinical review escalation workflow active — < 24h for non-urgent, < 2h for harmful | `curl -s http://localhost:${PORT}/api/clinical-review/sla \| jq '.max_hours_harmful'` must be `<= 2` AND `jq '.max_hours_routine'` must be `<= 24` | `npx init-clinical-review --sla "harmful:2h,routine:24h" --require-advisor` |
| **PS4** | Crisis keyword detection deployed — < 5 minute response time | `curl -s http://localhost:${PORT}/api/crisis/detection/latency \| jq '.p95_seconds'` must be `<= 300` | `npx deploy-crisis-detection --max-latency 300 --keywords crisis_keywords.yaml` |
| **PS5** | Crisis protocol documented — suicide, adverse event, child safety, emergency | `grep -cP "suicide\|adverse.event\|child.safety\|emergency\|CSAM" crisis_protocol.md` must be `>= 4` | `npx init-crisis-protocol --scenarios "suicide,adverse_event,child_safety,CSAM,emergency"` |
| **PS6** | Crisis resources surfaced automatically — country-specific hotlines, text lines | `curl -s http://localhost:${PORT}/api/crisis/resources \| jq '.resources_by_country \| length'` must be `>= 5` | `npx init-crisis-resources --countries "US,UK,CA,AU,IN" --hotlines --text-lines` |
| **PS7** | Vulnerable population protections configured — pediatric, mental health, rare disease | `grep -cP "pediatric\|mental.health\|eating.disorder\|rare.disease" safety_config.yaml` must be `>= 3` AND each must have `enhanced_defaults: true` | `npx init-vulnerable-population-safety --segments "pediatric,mental_health,rare_disease" --enhanced-defaults` |
| **PS8** | Adverse event reporting pipeline integrated with FDA MedWatch | `curl -s http://localhost:${PORT}/api/pv/pipeline/status \| jq '.medwatch_integrated'` must be `true` | `npx init-pv-pipeline --medwatch --require-clinical-review` |
| **PS9** | Content removal transparency — users told WHY content was removed, with appeal process | `curl -s http://localhost:${PORT}/api/moderation/removal-notice \| jq '.includes_reason'` must be `true` AND `jq '.includes_appeal_link'` must be `true` | `npx init-removal-transparency --include-reason --include-appeal-link` |
| **PS10** | Safety metrics dashboard — misinformation prevalence, time-to-detection, crisis response time | `curl -s http://localhost:${PORT}/api/safety/dashboard \| jq '.metrics \| length'` must be `>= 5` | `npx init-safety-dashboard --metrics "misinfo_prevalence,ttd,crisis_response,false_positive_rate,appeal_rate"` |
| **PS11** | Clinical advisor retained — available for content appeals and policy decisions | `curl -s http://localhost:${PORT}/api/clinical-advisor/status \| jq '.on_retainer'` must be `true` AND `jq '.response_sla_hours'` must be `<= 24` | `npx init-clinical-advisor --sla-hours 24 --specialties "primary_care,psychiatry,oncology"` |
| **PS12** | Community guidelines published — medical misinformation, personal experience vs advice, crisis resources | `grep -cP "medical.misinformation\|personal.experience\|crisis.resource\|adverse.event" guidelines.md` must be `>= 4` | `npx init-community-guidelines --domains "misinfo,personal_experience,crisis,adverse_events" --health-context` |
| **PS13** | User reporting system tested — one-click report for medical misinformation, crisis, harassment | `curl -s -X POST http://localhost:${PORT}/api/report/test \| jq '.report_types'` must include `["misinfo","crisis","harassment"]` | `npx init-reporting-system --types "misinfo,crisis,harassment" --one-click` |
| **PS14** | Quarterly safety audit — review detection effectiveness, false positive rates, missed incidents | `grep -cP "quarterly.audit\|safety.review\|false.positive" audit_schedule.yaml` must be `>= 3` AND `curl -s http://localhost:${PORT}/api/audit/last \| jq '.days_ago'` must be `<= 90` | `npx init-safety-audit --frequency quarterly --auto-schedule --metrics "precision,recall,fpr,missed_incidents"` |
## Footguns
<!-- DEEP: 10+min — war stories from patient community safety -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| A patient in a rare disease community posted about an experimental treatment trial in Mexico — it was a stem cell scam that cost patients $35,000 and caused 3 deaths | In March 2023, a member of a rare disease support community for ALS patients posted about a clinic in Tijuana offering "curative stem cell therapy" with "92% success rate." The post included the clinic's phone number and a testimonial from a supposed patient. Over 4 months, 12 community members traveled to the clinic, paying $35,000 each. Three died from infections related to the unsterile procedure. The platform had no medical misinformation detection, no treatment claim verification process, and no policy against promoting unlicensed medical facilities. | The platform treated the community as a neutral discussion space — "we don't evaluate medical claims." But in a rare disease community, desperate patients are specifically targeted by scammers. The platform's neutrality was exploited as a marketing channel for unlicensed treatments. | **Every health community needs active fraud detection for treatment claims.** Red flags: claims of cures for incurable conditions, specific success-rate numbers without published studies, clinics in jurisdictions with weak medical regulation, requests for upfront payment. Partner with organizations like the FDA's Health Fraud Branch or NORD (National Organization for Rare Disorders) to maintain a known-scam registry. When in doubt, remove first and verify later — a deleted post can be restored; a patient who traveled to a scam clinic can't be brought back. |
| A moderator in an eating disorder recovery community was secretly promoting pro-ana content via DM to vulnerable members — the platform discovered it after 11 months when a parent sued | A 28-year-old moderator for a major eating disorder support community was privately messaging teenage members with "thinspiration" content, diet pill recommendations, and encouragement to "stay dedicated to your goals." The messages were outside the public community and invisible to the platform's content moderation tools. 11 months later, a 15-year-old's parents discovered the messages and sued the platform. The moderator had passed the platform's background check — they had no prior offenses because private DMs had never been monitored. | The platform assumed moderation risk ended at the public community boundary. Private messages between moderators and users were invisible. The background check screened for criminal history, not predatory behavior patterns — there was no behavioral monitoring for moderators who disproportionately initiated private conversations with vulnerable users. | **Monitor moderator behavior, not just moderator content.** Track: what percentage of a moderator's interactions are private DMs vs public posts? What's the age distribution of users they DM? Set alerts for moderators whose private-message ratio exceeds 3 standard deviations above the moderation team average. Conduct quarterly random audits of moderator DMs with consent (built into the moderator agreement). A moderator badge is a trust signal to vulnerable users — bad actors specifically seek moderator positions to exploit that trust. |
| A crisis detection system flagged 200 posts/day as "suicidal" — 180 were false positives. Moderators developed alarm fatigue and started ignoring ALL crisis alerts, including the 20 real ones. | A mental health community deployed an AI crisis detection system in January 2024. The system had 90% precision — meaning 20 of 200 daily flags were genuine crises. Moderators had to review all 200 flags. Within 3 months, alarm fatigue set in. Moderators started clicking "dismiss" without reading. In April, a genuine crisis post — a user posting their suicide note in real time — was dismissed along with the noise. The user made an attempt (survived). The post had been flagged and dismissed in 4 seconds by a moderator who later said "I assumed it was another false positive like all the others." | The crisis detection threshold was set to maximize recall at the expense of precision. 90% precision sounds good in isolation — but at 200 flags/day, it produces 20 false positives per day. Over months, the false positive volume destroys moderator attention. The system was optimized for the metric (recall) rather than the human workflow (sustainable review volume). | **Design crisis detection for the human who has to review it.** Set a maximum false positive budget: no more than 10 crisis flags per moderator per day. If the system produces more flags than that, raise the confidence threshold — even if it means missing some true crises. A system that flags everything catches nothing, because the human in the loop stops paying attention. Measure "time-to-dismiss" for false positives — if it's dropping over time, your moderators are developing alarm fatigue. Rotate crisis review duty weekly to prevent desensitization. |
| A patient community's "block user" feature was weaponized by coordinated groups to mass-block LGBTQ+ cancer survivors, silencing their posts from community feeds | A cancer support community had a standard block feature: if a user blocks another user, they no longer see each other's content. In June 2023, a coordinated group from an external anti-LGBTQ+ forum created 200 accounts and systematically blocked every active LGBTQ+ member in the community. The blocked users' posts no longer appeared in the feeds of the 200 accounts — but more damagingly, the community's "trending" algorithm weighted engagement, and the blocked users' posts received less engagement because 200 active-looking accounts were no longer seeing or interacting with them. The posts of LGBTQ+ survivors effectively disappeared from the community's discovery surfaces. | The platform didn't consider the block feature as a vector for coordinated harm. Standard abuse detection looked for content violations (harassment, threats) — not for coordination patterns that used legitimate features for illegitimate purposes. The trending algorithm amplified the effect by treating reduced engagement as a signal of lower quality. | **Treat any user-controlled visibility feature as a potential abuse vector.** Monitor for coordinated blocking: if 20+ accounts created within 48 hours all block the same set of users, flag for investigation. Design engagement algorithms to account for "suspicious disengagement" — if a user's engagement drops suddenly due to new accounts blocking them, don't penalize their content in rankings. A block feature that can be weaponized is a coordinated harassment tool wearing the mask of a safety feature. |
| The platform collected detailed mental health symptom data "for research" — then sold anonymized datasets to pharmaceutical companies without patient consent | A mental health tracking app collected daily mood ratings, medication adherence data, and symptom journal entries from 400,000 users. The privacy policy stated data could be used "to improve our services and for research purposes." In February 2024, an investigative journalist discovered the company had sold "anonymized" datasets to 3 pharmaceutical companies for $2.1M total. The datasets included zip code, age, gender, diagnosis, and medication history — a combination that re-identified 87% of users when cross-referenced with public voter registration data. Patients joined the app seeking support; they became unwitting participants in pharmaceutical market research. | The company interpreted "research purposes" to include commercial pharmaceutical research without separately disclosing this. The "anonymization" was pseudonymization (removing names but keeping quasi-identifiers). The consent flow bundled data-sharing permissions into a single opt-in that users clicked through without reading — it was legally compliant, but patients felt betrayed. | **Health data consent must be specific, not bundled.** "We may share your data for research" is not informed consent — specify: "We may sell de-identified data to pharmaceutical companies for drug development research." Let users opt in/out of each data use separately. Never use zip code + age + gender + diagnosis in the same dataset — this combination is re-identifiable with public data. A privacy policy that's legally compliant but feels like a betrayal when discovered IS a trust breach — the legal department may say you're fine, but your patients will say you're not. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| Your safety system is reactive — you address issues after a user reports them or a journalist writes about them | Your detection system catches 85%+ of policy violations before user reports, your false positive rate is under 5%, and your crisis response time is under 15 minutes | You've built a safety infrastructure where the community self-regulates 60%+ of minor violations through user reporting and peer moderation, freeing your team to focus on novel threat patterns |
| Your privacy policy is a template you copied from a competitor and your consent flow bundles everything into one checkbox | Your consent flows are granular (separate opt-ins for data sharing, research, marketing), your data sharing is disclosed in plain language, and your anonymization methods are validated against re-identification risk | You've designed a privacy framework that goes beyond legal compliance — your patients actively praise your data practices in app store reviews, and privacy regulators cite your consent flow as a positive example in guidance documents |
| You assume a feature designed for safety (blocking, reporting, crisis flags) can't be abused | You threat-model every safety feature for abuse vectors: "how could a coordinated group use this to silence or harm our most vulnerable users?" | You've discovered and mitigated a novel abuse vector in a patient community, published a case study, and other platforms have adopted your mitigation strategy |

**The Litmus Test:** Spend 2 hours in your patient community as a vulnerable user — create an account, join a support group for a stigmatized condition, and post something vulnerable. How long before you encounter harmful content? How easy is it to report? Does anything happen when you do? If you can't do this because you're afraid of what you'll find, you already know the answer. A patient community's safety isn't measured by the absence of lawsuits — it's measured by whether a newly diagnosed patient, at their most vulnerable moment, finds support or exploitation. If you wouldn't let your own family member join your community unsupervised, you have work to do.

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- STANDARD: 3min -->

### Solo (1 developer, patient community MVP)
**Description:** Building MVP health community. < 100 users. No dedicated safety team.
**Approach:** Published community guidelines. Basic keyword detection (prescriptive patterns + crisis keywords). Manual review of all flagged content. Crisis protocol: surface 988/crisis resources. Clinical advisor: on-call consultant for content appeals.
**Time investment:** ~1 week to set up. ~2 hours/week ongoing.

### Small Team (2-10 developers, growing community, 1K-50K users)
**Description:** Active community. Real moderation volume. Starting to see bad actors.
**Approach:** Automated detection for all risk levels. Part-time clinical reviewer. Tiered moderation: auto-flag → clinical review → human mod. User reporting system. Crisis protocol: automated detection + human follow-up within 1 hour. Vulnerable population protections active. Safety metrics dashboard.
**Time investment:** ~1 month to set up. ~10 hours/week ongoing.

### Medium Team (10-50 developers, large community, 50K-500K users)
**Description:** Large, established community. Multiple conditions/segments. Regulatory scrutiny.
**Approach:** Machine learning-assisted detection. Full-time clinical review team. 24/7 crisis response. Automated adverse event reporting to FDA. Community health metrics with SLAs. Dedicated trust & safety team. Transparency reports published quarterly. External safety audit annually.
**Time investment:** Dedicated trust & safety team (2-4 FTE).

### Enterprise (50+ developers, global community, 500K+ users)
**Description:** Multi-country, multi-language health community. Multiple regulatory jurisdictions.
**Approach:** AI-powered detection with multi-language support. Global clinical review team across time zones. Country-specific crisis resources and protocols. Automated pharmacovigilance reporting to FDA, EMA, PMDA, etc. Safety research program. External safety advisory board. Real-time safety dashboards. Regulatory compliance across jurisdictions.
**Time investment:** Large trust & safety organization (10-20+ FTE).

## What Good Looks Like
<!-- STANDARD: 3min -->

A patient can share their treatment experience without fear of harassment. Medical misinformation is detected and removed before it spreads — automated systems catch prescriptive claims within minutes. When a community member is in crisis, resources surface immediately — not hours later when a moderator checks the queue. Patients know WHY content was removed because every moderation action includes a clear explanation. Vulnerable populations (pediatric, mental health, rare disease) have enhanced protections by default. The community guidelines are living documents, updated as new threat patterns emerge. Safety metrics are tracked, reviewed quarterly, and improving. Patients trust the platform because safety is visible, consistent, and fair — not because nothing bad ever happens, but because when it does, the response is swift, transparent, and compassionate.

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

## References
<!-- STANDARD: 3min -->

- **trust-safety-engineer** — Abuse detection infrastructure, automated harm detection, anti-bot measures
- **content-policy-manager** — Community guidelines, medical misinformation definitions, escalation frameworks
- **medical-content-reviewer** — Clinical accuracy review, evidence-based medicine, treatment claim validation
- **crisis-response-manager** — Crisis escalation frameworks, adverse event protocols, emergency response coordination
- **community-operations-manager** — Community health metrics, ambassador programs, operational workflows
