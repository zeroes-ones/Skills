---
name: cross-skill-communication
description: >
  Use when designing inter-skill communication protocols, diagnosing broken skill chains,
  defining message schemas for skill-to-skill data exchange, setting up publish-subscribe
  event flows, resolving conflicts when multiple skills produce contradictory outputs,
  establishing handoff contracts, implementing feedback loops for output quality, designing
  degradation modes (timeouts, circuit breaking), or auditing chain integrity. Handles 6
  universal patterns (Request-Response, Pub-Sub, Handoff, Feedback Loop, Conflict Resolution,
  Orchestration), a universal JSON message envelope, discovery protocol, circuit breaker
  design, and confidence calibration. This is the NERVOUS SYSTEM of the skill ecosystem.
  Do NOT use for individual skill internals (route to writing-great-skills), persona fan-out
  (route to agent-persona-orchestrator), or multi-agent topologies (route to
  multi-agent-orchestration).
license: MIT
tags:
  - cross-skill-communication
  - inter-skill-protocol
  - message-schema
  - chain-integrity
  - pub-sub
  - handoff
  - conflict-resolution
  - feedback-loops
  - circuit-breaker
  - discovery
author: Sandeep Kumar Penchala
type: framework
status: stable
version: 1.0.0
updated: 2026-07-30
token_budget: 4800
chain:
  consumes_from:
    - writing-great-skills
    - using-agent-skills
    - agent-persona-orchestrator
    - agent-handoff-protocol
    - multi-agent-orchestration
    - skill-levels
  feeds_into:
    - writing-great-skills
    - using-agent-skills
    - agent-persona-orchestrator
    - agent-handoff-protocol
    - wayfinder
  alternatives:
    - agent-persona-orchestrator
    - multi-agent-orchestration
---

# Cross-Skill Communication Protocol
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

The universal nervous system for the skill ecosystem. Every inter-skill interaction — whether a trading signal flowing from technical-signals-engineer to portfolio-signal-manager, a product requirement flowing from product-manager to system-architect, or a security finding flowing from security-reviewer to code-reviewer — should conform to one of the 6 communication patterns defined here.

**NEVER guess how two skills communicate.** Always consult this protocol. Ad-hoc coordination without a declared pattern produces the 457 broken chains and 5 incompatible formats that plague this repository today. If a communication link doesn't fit one of the 6 patterns, the link doesn't exist.

Current state: 223 skills, 457 broken chains, 5+ incompatible coordination formats, zero shared message protocol. Skills were built in isolation. This protocol makes them interoperable.

## Route the Request

<!-- QUICK: 30s -->

### Auto-Route

| # | Condition | Action |
|---|-----------|--------|
| A1 | User says "skills don't talk to each other," "broken chain," "how do skills communicate," "cross-skill," "inter-skill," "handoff between skills" | This is your skill. Jump to **Core Workflow**. |
| A2 | User is building a new skill and needs to define how it coordinates with others | Jump to **Phase 2: Define Communication Contract**. |
| A3 | User is diagnosing why two skills produced conflicting outputs | Jump to **Pattern 5: Conflict Resolution**. |
| A4 | User is auditing chain integrity across the repository | Jump to **Phase 4: Chain Integrity Validation**. |
| A5 | User is setting up skill-to-skill event notifications | Jump to **Pattern 2: Publish-Subscribe**. |

### Intent Route

```

What communication problem are you solving?
├── Two skills need to exchange data during execution → Pattern 1: Request-Response
├── Multiple skills need to know when something happens → Pattern 2: Publish-Subscribe
├── Work is passing from one skill to another → Pattern 3: Handoff
├── A consumer skill needs to tell a producer skill its output was wrong → Pattern 4: Feedback Loop
├── Two skills disagree and you need to resolve it → Pattern 5: Conflict Resolution
├── One skill coordinates several others → Pattern 6: Orchestration
├── You're designing a new skill's communication contract → Phase 2
├── You're fixing broken chains across the repo → Phase 4
└── You're defining how all patterns fit together → Phase 1

```

## Ground Rules — Read Before Anything Else

<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to design a one-directional chain without verifying the downstream skill acknowledges it. A `feeds_into` without matching `consumes_from` is a broken promise — information flows into a void. 457 of these exist today. | Trigger: skill YAML has `feeds_into: [X]` but skill X's YAML does NOT have `consumes_from: [this_skill]` | STOP. "Chain integrity violation: {this_skill} feeds_into {X} but {X} does not consume_from {this_skill}. Either add consumes_from to {X} or remove feeds_into from this skill. Information cannot flow to a receiver that doesn't expect it." |
| R2 | REFUSE to use ad-hoc coordination formats. Every inter-skill interaction MUST conform to one of the 6 patterns (Request-Response, Pub-Sub, Handoff, Feedback, Conflict Resolution, Orchestration). No "I'll just mention the other skill in a paragraph" — that's how 5 incompatible formats emerged. | Trigger: Cross-Skill Coordination section does not reference any of the 6 pattern names AND does not use the standard message envelope schema | STOP. "Ad-hoc coordination detected. Map interaction to one of 6 patterns (see Core Workflow Phase 1). Standardize to the message envelope format. Unpatterned coordination is untestable coordination." |
| R3 | REFUSE to send a message without a message_id, source_skill, target_skill, schema_version, and timestamp. Messages without these 5 fields are untraceable, unversioned, and undebuggable. | Trigger: inter-skill communication JSON missing any of: message_id, source_skill, target_skill, schema_version, timestamp | STOP. "Message envelope incomplete. Required fields: message_id (UUID), source_skill, target_skill, schema_version, timestamp (ISO8601). Without these, message routing, debugging, and compatibility checking are impossible." |
| R4 | REFUSE to implement a handoff without defining what state transfers, what doesn't, and how the receiver validates state integrity. Handoffs without explicit state contracts are the #1 cause of lost context between skill invocations. | Trigger: handoff description references "passes to" or "hands off to" without explicit state_schema block | STOP. "Handoff without state contract. Define: transferred_state (exact data), excluded_state (what stays behind), validation (how receiver verifies integrity), resume_point (where execution continues). See Pattern 3: Handoff." |
| R5 | REFUSE to resolve a conflict by defaulting to one skill over another without documented rationale. "The higher-confidence skill wins" is not rationale — confidence scores from different skills are not comparable without calibration. | Trigger: conflict resolution picks winner without conflict_resolution block containing calibration_method, weights, and rationale | STOP. "Uncalibrated conflict resolution. Document: calibration method (how scores were made comparable), source weights (why one source weighted higher), resolution rationale (domain-specific reasoning). See Pattern 5: Conflict Resolution." |
| R6 | REFUSE to design a feedback loop without specifying what the producer does with the feedback. Feedback without action is noise. If the producer doesn't have a defined response to negative feedback, the loop doesn't close. | Trigger: feedback loop described as "Skill B tells Skill A its output was wrong" without corresponding producer_action field | STOP. "Open feedback loop. Define producer_action: what Skill A does when feedback score < threshold. Options: recalibrate, re-score with different parameters, deprecate methodology, escalate to human. Without producer_action, feedback is venting, not learning." |
| R7 | REFUSE to let a skill depend on another skill without a timeout, degradation mode, and circuit breaker. Every inter-skill dependency is a potential failure point. If Skill A blocks waiting for Skill B and Skill B never responds, Skill A must have a plan. | Trigger: skill dependency defined without timeout_seconds, degradation_response, and circuit_breaker_threshold | STOP. "Unprotected skill dependency. Add: timeout (max wait), degradation_response (what to do on timeout), circuit_breaker (consecutive failures before skipping this dependency). Dependencies without protection become cascading failures." |

## Anti-Hallucination

<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "I listed the skill in my Cross-Skill Coordination section, so we're integrated." | Listing is not integration. Without a shared message format, versioned schema, timeout handling, and tested exchange, "integration" is a hope, not a fact. The 457 broken chains prove that listing alone doesn't work. **Cost: $0 in direct losses but incalculable in wasted context — every broken chain is a conversation where the agent manually bridges a gap that should have been automated. Multiply by hundreds of invocations per day.** |
| "Skills don't need a message schema — the agent will figure out how to pass data between them." | The agent passes unstructured text between skill invocations. Skill A outputs "The stock is undervalued by 15%." Skill B reads that and must parse 15% from prose. What if Skill A changes its output format? What if the number is in a different paragraph? The agent "figuring it out" is pattern-matching on unstructured text — brittle, unversioned, and silently wrong. **Cost: $5K-$50K per misinterpreted inter-skill data transfer. Structured envelopes with schema_version prevent silent format drift.** |
| "My skill's confidence score is 85, so it overrides the other skill's 65." | Confidence scores from different skills measure different things. A technical-signals-engineer's 85 measures indicator alignment purity. A fundamental-analyst's 65 measures valuation margin width. They are incommensurable without calibration. Assuming comparability is like comparing Celsius to Fahrenheit without conversion. **Cost: $10K-$200K in "high confidence wins" decisions where the less confident source was actually more accurate. Calibrate scores against a common accuracy baseline before comparing.** |
| "If Skill A feeds_into Skill B, then Skill B obviously consumes_from Skill A. No need to check." | The 457 broken chains say otherwise. At repository scale, manual chain maintenance is impossible. Skills get added, renamed, split. Chains rot silently. The only defense is automated validation — every chain link verified bilaterally. **Cost: Every broken chain is a runtime failure waiting to happen. When the agent routes to Skill B expecting data from Skill A and Skill B has no idea what Skill A is, the pipeline breaks mid-execution.** |
| "Handoffs are simple — just tell the next skill what to do." | A handoff that says "continue the analysis" has lost: current state, intermediate results, ruled-out approaches, assumptions made, calibration parameters, data freshness timestamps. The receiving skill starts from zero because the sending skill assumed "context is shared." Context is NOT shared between skill invocations unless explicitly serialized. **Cost: $2K-$20K per lost-context handoff. The receiving skill re-does work, re-discovers ruled-out approaches, and may reach different conclusions from the same data — creating inconsistency that looks like a bug but is actually a communication failure.** |

## Core Workflow

<!-- STANDARD: 5min -->

### Phase 1: Understand the 6 Communication Patterns

```

UNIVERSAL SKILL COMMUNICATION PATTERNS

PATTERN 1: REQUEST-RESPONSE (synchronous pull)
  Skill A asks Skill B for data. Skill B responds. Skill A waits.
  Use when: Skill A needs specific data from Skill B to continue its work.
  Example: portfolio-signal-manager requests signal JSON from technical-signals-engineer.
  Contract: request schema + response schema + timeout + degradation response.

  FLOW:
  Skill A ──request(ticker, params)──→ Skill B
  Skill A ←──response(signal_json)──  Skill B

  TIMEOUT BEHAVIOR:
  < 5s → Normal
  5-30s → Flag "Slow — Skill B may be overloaded"
  > 30s → TIMEOUT. Skill A proceeds with degradation_response (stale cache, skip, or escalate)

PATTERN 2: PUBLISH-SUBSCRIBE (asynchronous push)
  Skill A publishes an event. Any skill subscribed to that event type receives it.
  Use when: Multiple skills need to react to the same event, or events happen unpredictably.
  Example: market-data-engineer publishes "corporateAction" → technical-signals-engineer,
           fundamental-analyst, and portfolio-signal-manager all receive it.
  Contract: event_type taxonomy + event envelope + subscription registry + delivery guarantee.

  FLOW:
  Skill A ──publish(event_type, payload)──→ Event Bus
                                            ├──→ Skill B (subscribed to event_type)
                                            ├──→ Skill C (subscribed to event_type)
                                            └──→ Skill D (subscribed to event_type)

  SUBSCRIPTION: Defined in subscriber's YAML:
    subscribes_to:
      - event_type: "corporateAction"
        source_skills: ["market-data-engineer"]
        action: "adjustPositionSizing"

PATTERN 3: HANDOFF (state transfer)
  Skill A completes its phase and transfers execution state to Skill B.
  Use when: Work progresses through a pipeline where each phase has a different skill.
  Example: brainstorming → idea-to-spec → system-architect → backend-developer.
  Contract: state_schema (what transfers) + excluded_state (what stays) +
            validation (how receiver verifies) + resume_point (where to continue).

  FLOW:
  Skill A ──handoff(state_bundle)──→ Skill B
  Skill B validates state_bundle → resumes from resume_point

  STATE CONTRACT:
  {
    "handoff_id": "uuid",
    "from_skill": "brainstorming",
    "to_skill": "idea-to-spec",
    "transferred_state": {
      "decisions": [...],       // What was decided
      "constraints": [...],     // What limits exist
      "open_questions": [...],  // What's still unresolved
      "ruled_out": [...],       // What approaches were eliminated (and why)
      "artifacts": [...]        // File paths, data, models created
    },
    "excluded_state": ["internal_scratchpad", "exploration_dead_ends"],
    "resume_point": "Start at Phase 2: Specification Writing",
    "validation_hash": "sha256_of_transferred_state"
  }

PATTERN 4: FEEDBACK LOOP (bidirectional quality signal)
  Skill B (consumer) evaluates Skill A's (producer) output quality and sends feedback.
  Skill A incorporates feedback to improve future outputs.
  Use when: Output quality matters and should improve over time.
  Example: algorithmic-trader reports execution slippage back to portfolio-signal-manager,
           which adjusts position sizing assumptions.

  FLOW:
  Skill A ──output──→ Skill B
  Skill A ←──feedback(output_quality, issues, suggestions)── Skill B
  Skill A incorporates feedback → improved future outputs

  FEEDBACK CONTRACT:
  {
    "feedback_id": "uuid",
    "consumer_skill": "algorithmic-trader",
    "producer_skill": "portfolio-signal-manager",
    "reference_output_id": "original message_id being evaluated",
    "quality_score": 0.72,            // 0-1, calibrated against historical accuracy
    "issues": [
      {"type": "slippage_underestimate", "severity": "medium",
       "detail": "Assumed 0.05% slippage, actual was 0.18% on NASDAQ morning orders"}
    ],
    "producer_action_required": "recalibrate_slippage_model",
    "producer_action_deadline": "2026-08-06"
  }

PATTERN 5: CONFLICT RESOLUTION (multi-source reconciliation)
  Two or more skills produce contradictory outputs for the same decision.
  A resolution framework reconciles them into a single decision.
  Use when: Multiple skills analyze the same thing and reach different conclusions.
  Example: technical-signals-engineer says BUY, fundamental-analyst says SELL →
           portfolio-signal-manager resolves via weighted decision matrix.

  FLOW:
  Skill A ──output_A (direction=BUY, confidence=78)──┐
                                                       ├──→ CONFLICT DETECTED
  Skill B ──output_B (direction=SELL, confidence=62)──┘
                                                       │
                                                       ▼
                                              RESOLUTION FRAMEWORK
                                              ├── 1. Calibrate scores (make comparable)
                                              ├── 2. Apply domain weights (context-dependent)
                                              ├── 3. Compute weighted decision
                                              ├── 4. Document rationale
                                              └── 5. Output: single decision + confidence

  RESOLUTION CONTRACT (generalized):
  {
    "conflict_id": "uuid",
    "conflicting_outputs": [output_A, output_B],
    "calibration": {
      "method": "historical_accuracy_normalization",
      "skill_A_calibration_factor": 0.85,
      "skill_B_calibration_factor": 0.90
    },
    "weights": {
      "skill_A_weight": 0.65,
      "skill_B_weight": 0.35,
      "weight_rationale": "Skill A historically more accurate in trending regimes"
    },
    "decision_score": 11.2,
    "decision": "BUY_WITH_CAUTION",
    "rationale": "Calibrated and weighted. Skill A dominates in current regime."
  }

PATTERN 6: ORCHESTRATION (coordinated multi-skill execution)
  One skill coordinates multiple sub-skills in a defined workflow with merge logic.
  Use when: A task requires multiple skill perspectives combined into one result.
  Example: agent-persona-orchestrator coordinating code-reviewer + security-auditor +
           test-engineer in parallel fan-out with merge.

  FLOW:
  Orchestrator
      │
      ├──→ Skill A (parallel) ──→ Output A
      ├──→ Skill B (parallel) ──→ Output B
      └──→ Skill C (parallel) ──→ Output C
      │
      ▼
  MERGE (de-duplicate, normalize, prioritize)
      │
      ▼
  Single actionable output

  ORCHESTRATION CONTRACT: See agent-persona-orchestrator for the full specification.
  Key requirement: merge logic must be defined BEFORE fan-out. Merge is the product;
  fan-out is the supply chain.

```

### Phase 2: Define a Skill's Communication Contract

```

For any skill, define its communication contract using this template:

1. UPSTREAM DEPENDENCIES (Pattern 1: Request-Response or Pattern 2: Pub-Sub)

   For each upstream skill your skill depends on:
   | Upstream Skill | Pattern | What You Request | Message Schema | Timeout | Degradation Response |
   |---|---|---|---|---|---|
   | technical-signals-engineer | Request-Response | Signal JSON for ticker | signal_request → signal_response (v1.2) | 30s | Use last cached signal if < 60 min old; otherwise skip ticker |
   | market-data-engineer | Pub-Sub | Corporate action events | corporate_action_event (v1.0) | N/A (async) | Queue event for processing on reconnect |

2. DOWNSTREAM CONSUMERS (Pattern 1: Response, Pattern 3: Handoff, Pattern 4: Feedback)

   For each downstream skill that consumes your output:
   | Downstream Skill | Pattern | What You Provide | Message Schema | Expected Response | If No Response |
   |---|---|---|---|---|---|
   | portfolio-signal-manager | Request-Response | Signal JSON | signal_response (v1.2) | Acknowledgment within 5s | PM will timeout and use degraded mode |
   | data-scientist | Handoff | Backtest dataset | backtest_handoff (v1.0) | Validation confirmation | Retry 3x, then escalate |

3. EVENT SUBSCRIPTIONS (Pattern 2: Publish-Subscribe)

   Events your skill subscribes to:
   | Event Type | Source Skill | Trigger Condition | Your Action |
   |---|---|---|---|
   | regimeChanged | market-data-engineer | ADX crosses 25 threshold | Recalculate all signal weights with new regime |
   | dataQualityDegraded | market-data-engineer | Price feed stale > 5 min | Halt new signal generation, mark existing as stale |

4. EVENT PUBLICATIONS (Pattern 2: Publish-Subscribe)

   Events your skill publishes:
   | Event Type | Trigger Condition | Payload | Expected Subscribers |
   |---|---|---|---|
   | signalGenerated | Signal confidence > threshold computed | ticker, direction, confidence, signal_id | portfolio-signal-manager |
   | methodologyChanged | Indicator formula or parameter updated | change_description, affected_signals, version | All downstream consumers |

5. CONFLICT RESOLUTION (Pattern 5)

   If your skill's output can conflict with another skill's output:
   | Conflicting Skill | Conflict Scenario | Resolution Method | Your Weight | Escalation |
   |---|---|---|---|---|
   | fundamental-analyst | Opposite direction (BUY vs SELL) on same ticker | Weighted decision matrix | Regime-dependent (0.35-0.65) | portfolio-signal-manager |

6. FEEDBACK CONTRACTS (Pattern 4)

   If your skill receives feedback:
   | Feedback Source | What They Evaluate | Action on Score < 0.5 | Action on Score < 0.3 |
   |---|---|---|---|
   | portfolio-signal-manager | Signal accuracy (did direction prove correct?) | Review methodology for ticker class | Recalibrate confidence scoring |
   | algorithmic-trader | Execution compatibility (was signal executable?) | Adjust timing parameters | Deprecate signal type if unexecutable |

   Complete when: All 6 contract sections filled. Every upstream dependency has
   timeout + degradation. Every handoff has state schema. Every conflict has resolution method.

```

### Phase 3: Universal Message Envelope

```

EVERY inter-skill message wraps its payload in this envelope. The envelope
provides routing, versioning, tracing, and quality metadata regardless of
which pattern is being used.

UNIVERSAL MESSAGE ENVELOPE (JSON Schema):

{
  "$schema": "https://skills-repo/cross-skill-message/v1",
  "envelope": {
    "message_id": "uuid-required",              // Globally unique, generated by sender
    "correlation_id": "uuid-optional",          // Links request→response, event→reaction
    "source_skill": "skill-name-required",      // Who sent this
    "target_skill": "skill-name-or-*",          // Who should receive (* for pub-sub broadcast)
    "pattern": "request|response|event|handoff|feedback|conflict_resolution|orchestration_command",
    "schema_version": "semver-required",        // Version of this message's payload schema
    "timestamp": "ISO8601-required",            // When this message was created
    "expires_at": "ISO8601-optional",           // After this, message is stale
    "priority": "low|normal|high|critical",     // Processing priority
    "idempotency_key": "uuid-optional"          // For patterns that support retry
  },
  "payload": {
    // Pattern-specific payload. Schema determined by source_skill + schema_version.
    // Every payload MUST validate against its declared schema.
  },
  "quality": {
    "confidence": 0.0-1.0,                      // How confident the sender is in this payload
    "data_freshness": "ISO8601-optional",       // When the underlying data was last updated
    "calibration_version": "semver-optional"    // Version of the sender's confidence model
  },
  "trace": {
    "parent_message_id": "uuid-optional",       // For feedback: references the output being evaluated
    "skill_chain": ["skill-a", "skill-b", "..."], // Skills this message has passed through
    "processing_time_ms": 0                     // How long the sender took to produce this
  }
}

MESSAGE LIFECYCLE:

1. CREATION: Sender constructs envelope + payload. Validates payload against schema.
2. ROUTING: target_skill determines recipient. pattern determines handling.
3. VALIDATION: Receiver validates envelope completeness (R3 check: 5 required fields).
4. PROCESSING: Receiver extracts payload, processes according to pattern.
5. ACKNOWLEDGMENT: For Request-Response, receiver sends response envelope.
   For Pub-Sub, no acknowledgment (fire-and-forget).
   For Handoff, receiver validates state bundle and confirms.
6. EXPIRATION: After expires_at, message is stale. Receivers MUST reject expired messages.
7. TRACING: Every message in a chain links back through trace.parent_message_id.

SCHEMA VERSIONING:

├── MAJOR version change (1.x → 2.x): Breaking payload changes.
│   Old consumers CANNOT process this without update.
│   Sender MUST support both versions during transition period (min 30 days).
├── MINOR version change (1.0 → 1.1): New fields added, no breaking changes.
│   Old consumers ignore new fields. New consumers handle them.
└── PATCH version change (1.0.0 → 1.0.1): Bug fix, no schema change.

TRANSITION PROTOCOL:
When schema_version increments MAJOR:
1. Sender publishes deprecation notice for old version.
2. Sender produces BOTH old and new versions for 30 days.
3. Consumers migrate to new version.
4. After 30 days + all consumers migrated, old version retired.

```

### Phase 4: Chain Integrity Validation

```

VALIDATE the entire skill chain graph. Fix broken links. This is how we
eliminate the 457 broken chains.

VALIDATION RULES:

1. BILATERAL CONSISTENCY (every chain link must be confirmed by both sides):
   For each skill S:
     For each downstream D in S.chain.feeds_into:
       ASSERT D.chain.consumes_from contains S
       IF NOT: "BROKEN: {S} → {D} (D does not consume_from {S})"

2. NO SELF-REFERENCE (skill cannot consume_from or feed_into itself):
   For each skill S:
     ASSERT S ∉ S.chain.consumes_from
     ASSERT S ∉ S.chain.feeds_into

3. NO DEAD ENDS (every feeds_into MUST have at least one consumer documented):
   For each skill S:
     ASSERT len(S.chain.feeds_into) > 0 OR S is a terminal skill AND documented as such
     IF terminal: S.description MUST state "terminal skill, no downstream consumers"

4. ALTERNATIVES ARE REAL (every alternative must exist in the registry):
   For each skill S:
     For each A in S.chain.alternatives:
       ASSERT skill_registry.contains(A)

5. CROSS-SKILL SECTION MATCHES CHAIN (documentation must match frontmatter):
   For each skill S:
     Let upstream_from_section = skills listed in Cross-Skill Coordination → Upstream
     Let downstream_from_section = skills listed in Cross-Skill Coordination → Downstream
     ASSERT upstream_from_section ⊆ S.chain.consumes_from
     ASSERT downstream_from_section ⊆ S.chain.feeds_into

   This catches: "I document that I consume from X but forgot to add it to my YAML chain"

6. COMMUNICATION PATTERN DECLARED (every chain link needs a pattern):
   For each skill S:
     For each upstream U in S.chain.consumes_from:
       ASSERT S.Cross-Skill Coordination has pattern declaration for U
       (i.e., "Pattern 1: Request-Response with timeout 30s")
     For each downstream D in S.chain.feeds_into:
       ASSERT S.Cross-Skill Coordination has pattern declaration for D

AUTOMATED FIX WORKFLOW:

1. Run chain-validator against entire repository
2. For each broken chain: determine if it's a documentation error or a real dependency
   ├── DOC ERROR: Downstream skill SHOULD consume from upstream but forgot to list it
   │   Fix: Add consumes_from entry to downstream skill. Both sides agree dependency exists.
   └── GHOST DEPENDENCY: Upstream skill claims to feed into downstream but downstream
       doesn't need it (the dependency was aspirational or outdated)
       Fix: Remove feeds_into from upstream skill. Clean up Cross-Skill Coordination section.

3. For each chain link without a pattern: add pattern declaration
4. For each terminal skill without documentation: add terminal designation
5. Re-validate. All chains must be bilateral, patterned, and documented.

[VERIFIED] chain-validator returns 0 broken chains. Every link bilateral. Every link has declared pattern.
[VERIFIED] All 6 communication patterns documented and tested with at least one skill pair each.
[VERIFIED] Message envelope schema validated against all pattern payload types.

```

## Decision Trees

<!-- STANDARD: 3min -->

### DT1: Which Communication Pattern?

```

Two skills need to exchange information. Which pattern?
├── Skill A needs specific data from Skill B to continue → Pattern 1: Request-Response
│   ├── One-time query → Simple request-response
│   └── Repeated queries → Consider caching with freshness TTL
├── Multiple skills need to know when X happens → Pattern 2: Publish-Subscribe
│   ├── Known subscriber set → Direct pub-sub with subscription registry
│   └── Unknown/evolving subscriber set → Event bus with topic-based routing
├── Work progresses through pipeline, each phase different skill → Pattern 3: Handoff
│   ├── Linear pipeline → Sequential handoff (A→B→C)
│   └── Branching pipeline → Handoff with routing decision (A→B or A→C based on state)
├── Consumer wants to improve producer's output quality → Pattern 4: Feedback Loop
│   ├── One-time feedback → Single feedback message
│   └── Continuous improvement → Recurring feedback with trend tracking
├── Two skills analyzing same thing reach different conclusions → Pattern 5: Conflict Resolution
│   ├── Simple disagreement (same domain) → Direct comparison with calibration
│   └── Cross-domain disagreement (different frameworks) → Weighted matrix with domain weights
└── Multiple skills needed to complete one task → Pattern 6: Orchestration
    ├── Independent skill outputs (no dependencies) → Parallel fan-out
    ├── Sequential dependencies (B needs A's output) → Sequenced orchestration
    └── Mixed → Hybrid: fan-out independent phase → merge → fan-out dependent phase

```

### DT2: Timeout Strategy

```

Skill A requests data from Skill B. B doesn't respond. What does A do?
├── B is critical (A cannot proceed without B's data) → Wait full timeout, then:
│   ├── Cached data available AND < freshness TTL → Use cache, flag "stale data used"
│   ├── Partial data available → Proceed with partial, flag missing data
│   └── No data available → ESCALATE. Halt pipeline. Notify human.
├── B is important but not critical (A can degrade gracefully) → Wait 50% timeout, then:
│   ├── Proceed with default assumptions, flag "defaults used for {B}"
│   └── Log for post-mortem. Degradation doesn't halt pipeline.
├── B is optional (nice-to-have) → Wait 20% timeout, then:
│   └── Skip B. Proceed without B's contribution.
└── Pattern-specific:
    ├── Request-Response → Timeout = response deadline. Sender decides degradation.
    ├── Pub-Sub → No timeout. Events are fire-and-forget. If subscriber is down,
    │              it misses events (acceptable for non-critical events).
    ├── Handoff → Timeout = state validation deadline. If receiver doesn't validate
    │              within timeout, sender re-sends or escalates.
    └── Feedback → Timeout = producer acknowledgment deadline. If producer doesn't
                   acknowledge feedback, consumer escalates to human.

   For ALL patterns: after 3 consecutive timeouts from same skill →
   CIRCUIT BREAKER OPEN. Stop sending to that skill for 5 minutes.
   Test with heartbeat message before re-enabling.

```

### DT3: When NOT to Use a Formal Pattern

```

Is formal inter-skill communication overkill?
├── Both skills invoked in the same agent turn → Patterns may be heavy.
│   The agent can pass context directly. Patterns are for turn-boundary communication.
├── Skills are loosely related (e.g., both mentioned in conversation but
│   their outputs don't feed into each other) → No formal pattern needed.
│   Independent execution is fine.
├── One-off, never-repeated interaction → Document in prose, not formal pattern.
│   Patterns are for recurring interactions. One-offs don't justify the overhead.
└── Skills that will ALWAYS be invoked together in a fixed sequence →
    Consider merging into one skill with phases instead of two skills with handoff.
    If the boundary is never used independently, it's not a real boundary.

   Rule of thumb: If the interaction happens less than once per 10 agent sessions,
   formal pattern may be over-investment. If it happens daily or more, invest.

```

## Cross-Skill Coordination

<!-- STANDARD: 3min -->

### Upstream (Frameworks That Feed This One)

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `writing-great-skills` | Skill structure conventions, YAML frontmatter spec, trigger design patterns | Before designing any skill's communication contract — the contract lives within conventions set by writing-great-skills |
| `using-agent-skills` | Skill routing decision trees, multi-skill workflow composition | When designing orchestration flows — routing decisions determine which skills are in the pipeline |
| `agent-persona-orchestrator` | Parallel fan-out pattern, merge strategies, persona isolation rules | When Pattern 6 (Orchestration) involves isolated personas — persona orchestration is a stricter subset of general orchestration |
| `agent-handoff-protocol` | Progress ledger format, decision gate structure, context pruning rules | When designing Pattern 3 (Handoff) — the handoff protocol provides the state serialization mechanics |
| `multi-agent-orchestration` | Multi-agent topologies (Supervisor, Peer-to-Peer, Swarm), delegation protocol | When skill communication spans multiple agent instances rather than single-agent skill chaining |
| `skill-levels` | Competency calibration (L1-L5) for output depth expectations | When defining what "quality" means in feedback loops — L2 depth vs L4 depth have different quality expectations |

### Downstream (Who Uses This Protocol)

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `writing-great-skills` | Communication contract template for Cross-Skill Coordination sections | New skills ship with ad-hoc coordination instead of patterned contracts — delay means more broken chains to fix later |
| `using-agent-skills` | Pattern-based routing logic: detect which communication pattern a workflow needs | Agent routing stays manual, guessing which skill to invoke next instead of following declared patterns |
| `agent-persona-orchestrator` | Universal message envelope for persona-to-persona communication (currently personas share no structured data) | Personas remain isolated silos that can't exchange structured findings — merge step stays manual |
| `agent-handoff-protocol` | State schema for handoff bundles — what state transfers and how it's validated | Handoffs lose context because state schema is undefined — receiving skill starts from zero |
| `chain-validator` | Validation rules for bilateral chain integrity (the 6 rules from Phase 4) | Broken chains accumulate. Without validation rules, the validator has nothing to check |
| `wayfinder` | Communication pattern detection — wayfinder can route "how do X and Y talk?" queries to this skill | Users can't discover the protocol when they encounter coordination problems |

## Production Checklist

<!-- STANDARD: 3min -->

Before considering the cross-skill communication protocol production-ready:

- [ ] **Every skill's Cross-Skill Coordination section conforms to the 6-pattern taxonomy.** No ad-hoc formats remain. 221 sections to audit.
- [ ] **Chain integrity validator passes with 0 broken chains.** Currently 457 broken. Target: 0.
- [ ] **Every inter-skill dependency has a timeout, degradation response, and circuit breaker threshold.** Dependencies without protection are future cascading failures.
- [ ] **Every handoff has a state schema defining what transfers, what doesn't, and how it's validated.** Handoffs without state contracts lose context.
- [ ] **Every conflict between skills has a documented resolution method with calibration, weights, and rationale.** Conflicts resolved by "higher confidence wins" are uncalibrated.
- [ ] **Every feedback loop has a defined producer_action.** Feedback without action is noise. The loop must close.
- [ ] **Message envelope is validated at every skill invocation boundary.** Skills reject non-conforming messages rather than silently accepting malformed input.
- [ ] **Schema versions are tracked and MAJOR version transitions follow the 30-day dual-publish protocol.** Breaking changes without transition periods break consumers.
- [ ] **Circuit breakers fire after 3 consecutive timeouts and require manual reset.** Automatic reset hides persistent failures.
- [ ] **Every terminal skill (no feeds_into) is documented as terminal.** Terminal is a deliberate design choice, not an omission.

## Error Recovery

<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Skill A claims feeds_into Skill B but Skill B rejects A's messages | Schema version mismatch. Skill A sends v1.2 payload. Skill B expects v1.0. No transition period was observed | Check schema_version in rejected messages. If MAJOR mismatch: Skill A must publish v1.0 alongside v1.2 during 30-day transition. If MINOR: Skill B should accept and ignore unknown fields | **Schema version is a contract, not a suggestion.** Breaking changes without transition periods break consumers. Every MAJOR version bump requires dual-publish for 30 days. |
| Orchestration fan-out hangs because one skill never responds | Skill dependency has no timeout. Orchestrator blocks indefinitely on the slowest skill | Add per-dependency timeout. Default: 30s for data queries, 120s for analysis, 300s for computation. Mark timed-out skill as DEGRADED. Proceed with partial results | **Timeouts are not optional.** Every dependency is a potential infinite wait. Without timeouts, orchestration is a deadlock waiting to happen. |
| Handoff loses context — receiving skill starts from scratch despite "handoff complete" | Sender assumed context is shared. State bundle was "the conversation so far" with no structured state. Receiver got prose, not data | Implement structured state bundle (Pattern 3). Sender serializes: decisions made, constraints, open questions, ruled-out approaches. Receiver validates bundle hash before resuming | **"The conversation so far" is not state.** It's prose. Structured state has: decisions (what was resolved), constraints (what limits exist), open questions (what's unresolved), ruled_out (what was eliminated and why). |
| Circuit breaker opens, but no one notices because alerts go to the same broken skill | Circuit breaker notification uses the same broken dependency for alerting. The alert never delivers because the circuit is open | Circuit breaker notifications MUST use an independent alerting path. Never depend on a broken dependency to report its own breakage | **Alerting must be out-of-band.** The circuit breaker's notification channel cannot depend on any skill that the circuit breaker protects against. |

## Proactive Triggers

<!-- STANDARD: 3min -->

| Trigger | Action | Why |
|---|---|---|
| New skill added to the repository | Within 7 days: define its communication contract using Phase 2 template. Validate bilateral chain consistency with all listed upstream/downstream skills | New skills that don't declare their communication patterns immediately become broken chains. Fixing them later is 3x the work — downstream consumers have already built assumptions on ad-hoc formats |
| Skill renamed or moved to a different directory | Within 24 hours: update ALL skills that list the renamed skill in consumes_from, feeds_into, or alternatives. Run chain-validator to catch stragglers | Renames silently break chains. The old name stays in YAML frontmatter of every dependent skill. 50+ skills may reference a renamed skill — miss one and you have a phantom dependency |
| Schema version bumps MAJOR (1.x → 2.x) | Immediately: publish deprecation notice for old version. Begin 30-day dual-publish window. Notify all consumers. After 30 days: verify all consumers migrated, retire old version | Breaking changes without transition break every consumer simultaneously. The 30-day window is not bureaucracy — it's the difference between coordinated migration and cascading failure |
| Circuit breaker opens for any skill | Within 5 minutes: notify human. Investigate root cause. Do NOT reset circuit breaker until: (a) heartbeat test passes, (b) root cause identified, (c) fix deployed or accepted as known limitation | Circuit breakers that auto-reset hide persistent failures. Manual reset forces investigation. A skill that times out 3x in a row has a real problem — don't paper over it |
| chain-validator detects new broken chains (weekly automated run) | Within 48 hours: triage each broken chain. DOC ERROR → fix documentation. GHOST DEPENDENCY → remove feeds_into. REAL DEPENDENCY → add consumes_from to downstream skill | Broken chains accumulate silently. Weekly validation catches them before they become entrenched. Every broken chain is a runtime surprise waiting to happen |
| Two skills produce conflicting outputs for the same decision more than 3 times in a week | Escalate to human: the conflict resolution method is failing. Either calibration is wrong, weights need adjustment, or one skill's methodology is systematically biased | Recurring conflicts that the resolution framework "resolves" the same way every time are not resolved — they're suppressed. Pattern detection requires tracking resolution outcomes over time |
| A skill's confidence scores are consistently >20% above its actual accuracy (detected via feedback loop) | Flag skill for recalibration. confidence_calibration_factor = actual_accuracy / average_confidence. Update skill's calibration metadata. Notify all downstream consumers of calibration change | Overconfident skills poison every downstream decision. A skill that claims 85% confidence but is 60% accurate makes every consumer 25% overconfident. Calibration drift is silent and cumulative |

## Gotchas

<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| Two skills "integrated" via Cross-Skill Coordination section but produce incompatible outputs at runtime | Integration was documented but never tested. The coordination section describes intent, not verified behavior. JSON schemas were never validated against actual outputs | Test every declared communication link: take real output from Skill A, validate it against Skill B's expected input schema. If it fails, either fix output format or fix input expectations | **Documentation is not integration.** A Cross-Skill Coordination section is a promise. Testing is the verification that the promise is kept. Every declared link needs at least one integration test |
| Orchestration pipeline runs correctly 90% of the time but fails silently 10% of the time | One skill in the fan-out has a 10% timeout rate. The orchestrator's degradation mode uses defaults, so the pipeline "succeeds" but with degraded-quality output. Nobody monitors degradation rate | Track degradation_rate per skill. Alert when >5% of pipeline runs use degraded mode for any skill. Degradation is a valid state — silent degradation is not | **Degradation must be visible.** A pipeline that "works" with degraded inputs is producing lower-quality outputs. Track it. Alert on it. Degradation is a leading indicator of impending failure |
| Feedback loop exists but producer never acts on feedback — same issues recur | Feedback contract has no producer_action_deadline. Producer receives feedback, acknowledges it, files it. No mechanism forces action | Add deadline to feedback contract. If producer_action not completed by deadline, escalate to human. Track feedback resolution rate — if <80% within deadline, feedback loop is performative | **Feedback without enforced action is theater.** The loop closes only when producer behavior changes. Deadlines + escalation + resolution tracking make feedback actionable |
| Chain integrity validator passes but skills still can't communicate at runtime | Validator only checks YAML frontmatter consistency. It doesn't verify that message schemas are compatible, that the declared pattern is actually used, or that timeouts are configured | Add schema compatibility check to validator: for each pair (A→B), validate that A's output schema is a subset of B's expected input schema. Add pattern presence check: each chain link has a declared pattern | **Chain consistency ≠ communication compatibility.** Bilateral YAML is the first gate. Schema compatibility is the second. Pattern declaration is the third. All three must pass |
| Schema versions proliferate — every skill uses a different version of the message envelope | No enforcement of envelope schema version. Skills adopt the envelope independently and never update. v1.0, v1.1, v1.2, and v2.0 coexist. Consumers must handle all versions | Standardize envelope version across repository. Envelope schema is infrastructure — it should evolve slowly and centrally. When envelope bumps MAJOR, ALL skills migrate within the 30-day window. No skill is exempt | **Infrastructure schemas must be centralized.** The message envelope is not per-skill — it's per-ecosystem. Version skew creates a compatibility matrix that grows quadratically with skill count |

## Verification Guardrails

<!-- STANDARD: 3min -->

| Guard | Test | Failure Response |
|---|---|---|
| G1: BILATERAL-CHAIN | For every skill: `feeds_into ⊆ {skills that consume_from this skill}` | "Chain integrity violation: {skill} feeds_into {X} but {X} does not consume_from {skill}. Either bidirectional link or remove feeds_into." |
| G2: ENVELOPE-COMPLETE | Every inter-skill message must have: message_id, source_skill, target_skill, schema_version, timestamp (5 required fields) | "Message rejected: envelope incomplete. Required fields: message_id, source_skill, target_skill, schema_version, timestamp." |
| G3: PATTERN-DECLARED | Every inter-skill interaction must reference one of 6 patterns in its Cross-Skill Coordination section | "Undeclared pattern: {skill_A} → {skill_B} interaction in Cross-Skill Coordination section does not declare a communication pattern. Map to one of: Request-Response, Pub-Sub, Handoff, Feedback, Conflict Resolution, Orchestration." |
| G4: TIMEOUT-CONFIGURED | Every upstream dependency in a skill's communication contract must have timeout_seconds defined | "Missing timeout: {skill} depends on {upstream} but no timeout configured. Every dependency needs: timeout_seconds, degradation_response, circuit_breaker_threshold." |
| G5: HANDOFF-HAS-STATE | Every Pattern 3 (Handoff) declaration must include state_schema (transferred_state, excluded_state, validation) | "Handoff without state contract: {skill_A} → {skill_B} handoff missing state_schema. Define: transferred_state, excluded_state, validation. See Pattern 3." |
| G6: SCHEMA-VERSION-TRACKED | Every skill that produces structured output must declare output schema version in its communication contract | "Missing schema version: {skill} produces output for downstream consumers but no schema_version declared. Schema versioning is required for compatibility checking." |
| G7: FEEDBACK-CLOSES-LOOP | Every Pattern 4 (Feedback Loop) declaration must include producer_action and producer_action_deadline | "Open feedback loop: {feedback_source} → {producer} feedback missing producer_action. Feedback without mandated action does not close the loop. See Pattern 4." |

## Anti-Rationalization

<!-- DEEP: 10+min -->

| Rationalization | Reality |
|---|---|
| "We'll add communication patterns later — right now we just need to ship the skill." | Skills without communication patterns ship with ad-hoc coordination. When 10 skills ship this way, you have 10 different coordination formats. When 50 ship, you have an unmaintainable tangle. The cost of retrofitting patterns onto 50 skills exceeds the cost of defining patterns for 1 skill by 100x. **Cost: $0 now, $50K-$200K in cumulative retrofitting across 50+ skills. Patterns are infrastructure — build them first, not last.** |
| "My skill is simple — it doesn't need all 6 contract sections." | Every skill has at minimum: inputs it depends on (upstream), outputs it produces (downstream), and quality expectations. That's 3 contract sections minimum. A skill that "doesn't need coordination" is either truly isolated (document as terminal) or has hidden dependencies it's not acknowledging. **Cost: Every "simple" skill that omitted its coordination contract becomes a runtime discovery when downstream skills can't consume its output.** |
| "The chain YAML is enough — I don't need a separate Cross-Skill Coordination section." | YAML lists names. The Cross-Skill Coordination section defines HOW: what pattern, what schema, what timeout, what degradation response. A name without a pattern is a directory entry, not an integration. The 457 broken chains exist BECAUSE YAML was treated as sufficient. **Cost: YAML-only coordination is a phonebook. You know who exists but not how to talk to them.** |
| "Confidence scores from different skills are fine to compare directly — they're both 0-100." | A technical-signals-engineer 85 means "85% of signals with this indicator alignment were profitable in backtest." A fundamental-analyst 65 means "the DCF range with these assumptions gives 65% probability of undervaluation." These are different statistical objects. Comparing them directly is like comparing batting average to on-base percentage — both are percentages, both measure performance, but they're not the same thing. **Cost: $15K-$150K per uncalibrated conflict resolution. Calibrate everything against a common accuracy baseline.** |
| "The timeout should be the same for all dependencies — keep it simple." | A data query (fetch OHLCV) completes in <2 seconds. A fundamental analysis (DCF + comparables + quality scores) takes 30-120 seconds. A uniform 30-second timeout starves fast queries and kills slow analyses. Tailor timeouts to the operation: data queries 10s, signal generation 30s, analysis 120s, computation 300s. **Cost: Uniform timeouts either waste time waiting for fast operations or kill slow operations that would have succeeded. Calibrated timeouts respect the shape of the work.** |

## What Good Looks Like

<!-- STANDARD: 3min -->

A world-class cross-skill communication ecosystem:

- **Every inter-skill message has a traceable envelope.** message_id → correlation_id → parent_message_id. You can trace any decision back through every skill that contributed to it. The audit trail is complete, machine-readable, and timestamped.
- **Zero broken chains.** The chain-validator runs weekly and returns 0. Every `feeds_into` has a matching `consumes_from`. Every chain link has a declared communication pattern. Every pattern has a timeout and degradation response.
- **Skills degrade gracefully, never silently.** When a dependency times out, the consumer logs it, uses degraded mode, and the degradation is visible in monitoring. Silent degradation is treated as a production incident.
- **Conflicts are resolved, not suppressed.** When two skills disagree, the conflict resolution framework produces a documented decision with calibration, weights, and rationale. Six months later, you can audit whether the resolution was correct. Recurring conflicts trigger recalibration, not repeated suppression.
- **Feedback loops close.** When a consumer rates a producer's output quality, the producer has a deadline to act on the feedback. Resolution rates are tracked. Open loops are escalated. The ecosystem learns.
- **Schema versions are boring.** MAJOR version bumps follow the 30-day dual-publish protocol. No consumer is ever surprised by a breaking change. Schema evolution is predictable, documented, and migration-tested.
- **Handoffs preserve context.** The receiving skill never starts from zero. Structured state bundles carry decisions, constraints, open questions, and ruled-out approaches. The receiving skill validates the bundle hash and resumes from the defined resume_point.
- **Circuit breakers protect the ecosystem.** A skill that fails 3 times in a row is isolated, not retried into infinity. The failure is investigated before the circuit resets. Cascading failures are contained at the first broken dependency.
- **New skills ship with communication contracts on day one.** The Phase 2 template is filled before the skill is registered. No skill enters the ecosystem without declaring how it talks to others.
- **The protocol is invisible when it works, obvious when it doesn't.** Skills communicate without the agent manually bridging gaps. When a message fails, the envelope tells you exactly why: schema mismatch, timeout, circuit open, expired. Debugging is structured, not forensic.

## References

<!-- STANDARD: 3min -->

The following reference files are loaded on demand when deeper context is needed:

### Core Protocol References

| Reference | Path | Content |
|---|---|---|
| **Message Envelope Specification** | [message-envelope.md](references/message-envelope.md) | Complete JSON Schema for the universal message envelope. Field-by-field specification with validation rules, examples for all 6 patterns, and backward compatibility requirements |
| **6 Communication Patterns** | [communication-patterns.md](references/communication-patterns.md) | Detailed specification for each pattern: sequence diagrams, state machines, error handling, implementation checklist. Includes anti-patterns and common implementation mistakes |
| **Chain Integrity Validator** | [chain-validator.md](references/chain-validator.md) | Specification for the automated chain validator tool. 6 validation rules with SQL/pseudocode, false positive handling, auto-fix capabilities, and CI integration |
| **Conflict Resolution Framework** | [conflict-resolution.md](references/conflict-resolution.md) | Generalized weighted decision matrix applicable to any domain. Calibration methods (historical accuracy, cross-validation, expert Bayesian), domain weight derivation, and escalation criteria |
| **Schema Versioning Protocol** | [schema-versioning.md](references/schema-versioning.md) | MAJOR/MINOR/PATCH semantics for skill output schemas. Dual-publish transition protocol. Consumer migration tracking. Compatibility matrix maintenance |
| **Circuit Breaker Design** | [circuit-breakers.md](references/circuit-breakers.md) | Circuit breaker state machine (Closed → Open → Half-Open → Closed). Threshold configuration per dependency type. Monitoring and alerting integration. Reset criteria |
| **Feedback Loop Mechanics** | [feedback-loops.md](references/feedback-loops.md) | How to design closed-loop feedback: producer_action types, deadline enforcement, resolution rate tracking, escalation paths. Includes calibration drift detection via feedback trends |
| **Handoff State Schema** | [handoff-state-schema.md](references/handoff-state-schema.md) | Standardized state bundle format for skill-to-skill handoffs. What to include, what to exclude, validation hash computation, resume_point conventions |

### Related Skills

| Skill | Relationship | When to Invoke |
|---|---|---|
| `writing-great-skills` | Defines the SKILL.md structure that communication contracts live within | When creating a new skill — use writing-great-skills for structure, this protocol for the Cross-Skill Coordination section |
| `using-agent-skills` | Routes agent decisions to appropriate skills based on task type | When the agent needs to decide which skill to invoke next in a multi-skill pipeline |
| `agent-persona-orchestrator` | Implements Pattern 6 (Orchestration) for persona-based workflows with tool restrictions | When orchestration involves isolated personas with tool restrictions (not general skill-to-skill coordination) |
| `agent-handoff-protocol` | Implements Pattern 3 (Handoff) mechanics — progress ledgers, decision gates, context pruning | When implementing a handoff between skills that need progress tracking and decision traceability |
| `multi-agent-orchestration` | Implements Pattern 6 for multi-agent topologies (Supervisor, Peer-to-Peer, Swarm) | When skill communication spans multiple agent instances rather than single-agent skill chaining |
| `chain-validator` | Automated tool that enforces bilateral chain consistency | Weekly or on every skill change — validates that no broken chains exist |
| `wayfinder` | Routes "how do skills X and Y communicate?" queries to this protocol | When users or agents need to discover communication patterns between specific skills |
| `skill-levels` | Calibrates output depth across L1-L5 competency levels | When defining quality expectations in feedback loops — what "good" means varies by level |

## Deliberate Practice

<!-- STANDARD: 3min -->

To build cross-skill communication instinct:

1. **Audit a broken chain.** Pick one of the 457. Trace: Skill A claims to feed_into Skill B. Read Skill B's Cross-Skill Coordination section. Does Skill B know about Skill A? If not, is this a doc error (Skill B should consume from A) or a ghost dependency (Skill A is wrong)? Fix it. This builds intuition for chain integrity.
2. **Design a handoff.** Take a real pipeline where work passes from one skill to another (e.g., brainstorming → idea-to-spec). Write the state bundle: what decisions were made, what constraints exist, what was ruled out. Have the receiving skill validate the bundle. This builds respect for context preservation.
3. **Calibrate a conflict.** Take two skills that can disagree (e.g., code-reviewer and security-reviewer on the same PR). For each, find their historical accuracy on similar PRs. Derive calibration factors. Run a weighted resolution. Did the resolution pick the right answer? This builds understanding of why uncalibrated comparison fails.
4. **Design a circuit breaker.** Pick a skill dependency. Define: what counts as a failure? How many failures before the circuit opens? What happens during open circuit? How do you test before closing? This builds instinct for protecting the ecosystem from cascading failures.
5. **Trace a message through its lifecycle.** Start with a signal from technical-signals-engineer. Follow it: message envelope created → routed to portfolio-signal-manager → validated → processed → acknowledged → feedback loop back to TSE. At each step, what could fail? What's the degradation response? This builds end-to-end communication intuition.
