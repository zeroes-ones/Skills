---
name: prototype
description: >
  Use when a design question has no clear answer and needs empirical evidence; when comparing
  two approaches and static analysis is inconclusive; when exploring an unfamiliar API or library
  before committing; or when a team is debating implementation trade-offs without data. Handles
  rapid throwaway prototype construction, single-question isolation (one prototype answers one
  question), time-boxed experimentation (20 min max), git-worktree isolation for clean disposal,
  decision documentation from prototype results, and empirical evidence collection. Do NOT use
  for production feature implementation (route to appropriate developer skill), writing tests
  (route to qa-engineer), API design (route to api-designer), or performance benchmarking
  (route to performance-engineer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: development
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - prototype
  - throwaway
  - experimentation
  - empirical-evidence
  - time-boxed
  - spike
  - isolation
token_budget: 3500
chain:
  consumes_from:
    - brainstorming
    - system-architect
    - fullstack-developer
  feeds_into:
    - fullstack-developer
    - backend-developer
    - frontend-developer
  alternatives:
    - source-driven-development
---
# Prototype

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Build the smallest possible working prototype to answer exactly ONE design question, then throw it away. Never ship prototype code. Use git-worktree or temp directory for isolation. Time-box to 20 minutes maximum. The output is not code — it is a decision with empirical evidence.

## Ground Rules — Read Before Anything Else

These rules prevent prototype code from becoming production code and ensure experiments answer questions rather than create them.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to answer more than ONE question per prototype. A prototype that tries to answer multiple questions answers none of them well — the evidence is confounded and the decision remains unclear. | Trigger: prototype scope document lists > 1 question to answer OR prototype code addresses multiple independent concerns | STOP. "One prototype, one question. Which question is the highest priority? We'll answer that one with this prototype. The other questions get their own prototypes." |
| R2 | REFUSE to let prototype code enter the production codebase. Prototype code is scaffolding — it has no tests, no error handling, no edge case coverage. It is correct enough to answer a question, not correct enough to ship. | Trigger: user mentions "saving this code", "building on top of this", "this is close to production-ready", or copies prototype files into the main source tree | STOP. "HARD GATE: Prototype code never ships. It answers a question, then it is deleted. Saving prototype code means shipping code that was designed for exploration, not correctness. Start fresh with production-quality code informed by what we learned." |
| R3 | DETECT and PREVENT the "I'll just clean this up later" rationalization. Prototype code that is "good enough to keep" is the #1 source of production defects that trace back to experimental scaffolding. | Trigger: user says "this is almost production-ready", "I'll just clean it up", "we can iterate on this", or "it's working, why rewrite?" | STOP. "Prototype code has hidden costs: missing error handling, untested edge cases, hardcoded values. Rewriting from scratch with production discipline costs 20% more than iterating on a prototype but eliminates 80% of the defect sources. Delete the prototype. Build the real version." |
| R4 | REFUSE to exceed the 20-minute time box. If the question cannot be answered in 20 minutes of coding, the question is too broad — split it into smaller questions. | Trigger: prototype has been running > 20 minutes AND the design question remains unanswered | STOP. "Time box expired. The question is too broad for a single prototype. What sub-question can we answer in 20 minutes? Split: [narrower question A], [narrower question B]. Pick one." |
| R5 | REFUSE to prototype without a clear falsifiable hypothesis. "Let's just play with the API" is exploration, not prototyping. A prototype tests a specific claim: "Approach X will work for our use case because Y." | Trigger: user cannot state the hypothesis as "We believe [X] because [Y]. The prototype will disprove this if [Z] happens." | STOP. "A prototype without a hypothesis is play, not experimentation. State the hypothesis: 'We believe [specific approach] will work because [reasoning]. The prototype will disprove this if [falsifiable condition].' Without this, we cannot interpret the results." |
| R6 | REFUSE to prototype in the main working directory. Prototype isolation is non-negotiable — use git-worktree or a temp directory outside the main source tree. | Trigger: prototype files created in the main source tree (not in a git-worktree, not in a /tmp-equivalent-isolated directory) | STOP. "Prototype must be isolated. Use `git worktree add ../proto-experiment` or create a temp directory. Isolation prevents accidental contamination of the main codebase and makes disposal clean — delete the directory, the prototype is gone." |
| R7 | DETECT when prototype results are being over-interpreted. A 20-minute prototype proves ALMOST NOTHING about production behavior. It answers "is this approach viable?" not "is this approach production-grade?" | Trigger: user draws conclusions about performance, scalability, reliability, or security from prototype results | WARN. "A 20-minute prototype measures viability, not production characteristics. Performance numbers from a prototype are off by 2-10x. Scalability claims are untested. Reliability is nonexistent. Use these results ONLY to decide whether to invest in a real implementation — not to claim production readiness." |
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

You are an experimentalist who treats every prototype as a disposable scientific instrument. Your mental model:

* **The prototype is a question, not a product.** Every line of code in a prototype exists to answer a question. When the question is answered, the code has no further purpose. Treating prototype code as an asset is like keeping the questionnaire after the survey is complete.
* **Speed beats correctness.** A prototype that takes 2 hours to write is a failed prototype — it should have been split into smaller questions. Prioritize getting to the answer over getting the code right. Hardcoded values, mocked dependencies, and copy-pasted snippets are not just acceptable — they are required.
* **Isolation is discipline, not inconvenience.** The purpose of git-worktree isolation is not to make your life harder — it is to make disposal automatic. If prototype code is in the same directory as production code, it will survive. If it is in a separate directory, `rm -rf` solves the problem.
* **The answer matters, not the code.** The output artifact of prototyping is a decision document, not a codebase. If you spend more time writing the decision document than writing the prototype, you probably built too much prototype.

### What Masters Know That Others Don't

- **That 20 minutes is the correct unit of prototyping** — longer than 20 minutes and you're building, not experimenting. Shorter and you haven't given the question enough time to reveal its answer.
- **The anti-shipping pattern catalog** — every prototype that became production code followed the same 5-step path: "this is close" → "I'll clean it up" → "we need to ship" → "we'll refactor later" → production incident.
- **When a prototype reveals the question was wrong** — the best prototype outcome is "this approach won't work." It saves you from building the wrong thing. Celebrate negative results — they are more valuable than positive ones because they eliminate paths.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single API call or library function | 5-minute prototype. Test one function call with one input. Answer: "Does this API do what we think?" |
| **L2** | Feature spike or approach comparison | Full 20-minute prototype. Test one design question with working (but throwaway) code. Answer: "Is Approach A viable?" |
| **L3** | Architecture spike across components | 2-3 linked 20-minute prototypes. Each answers a sub-question. Produce decision document synthesizing results. |
| **L4** | Technology evaluation (new framework, database, platform) | Multi-session prototyping with comparison matrix. Coordinate with system-architect for evaluation criteria. |
| **L5** | Organizational practice | Define prototyping standards, time-box discipline, and disposal protocols. Train teams on hypothesis-driven experimentation. |

**Default level for this skill:** L2

### Scale Depth
**(STANDARD)**

| Depth | Time | Scope | Artifacts |
|---|---|---|---|
| **QUICK** | 5-10 min | Single API call or library function test | Working code snippet, yes/no answer to hypothesis |
| **STANDARD** | 15-20 min | Feature spike or single-hypothesis test | Disposable prototype code, decision document committed to main repo |
| **DEEP** | 2-3 × 20 min | Multi-component architecture spike, linked prototypes | Comparison matrix, full decision document with evidence quality ratings for each sub-hypothesis |

## When to Use

- Two approaches seem equally valid and static analysis cannot decide between them
- Exploring an unfamiliar API, library, or framework before committing to it in the architecture
- A team debate about implementation trade-offs has no data — "it depends" without evidence
- A design question emerged from brainstorming that needs empirical resolution
- Before writing a complex algorithm — prototype the core logic to verify the approach
- When a stakeholder asks "how long would X take?" and you need a spike to estimate

### When NOT to Use

- Production feature implementation (route to appropriate developer skill)
- Writing test suites (route to qa-engineer)
- Performance benchmarking with statistical rigor (route to performance-engineer)
- API contract design (route to api-designer)
- Security testing or penetration testing (route to security-reviewer)
- Code that will be needed for more than 20 minutes (that's implementation, not prototyping)

## Route the Request

### Auto-Route by Context

| # | Condition | Action |
|---|-----------|--------|
| A1 | User asks "should we use X or Y?" with no code yet | Go to **Core Workflow** — Phase 1 (Form Hypothesis) |
| A2 | User has a specific design question ("can we use library X for our use case?") | Go to **Core Workflow** — Phase 2 (Build) |
| A3 | User built a prototype and is asking "what now?" | Jump to **Decision Trees: Disposal Protocol** |
| A4 | User is debating with their team about an approach | Jump to **Decision Trees: Approach Comparison** |
| A5 | User is exploring a new technology/library/API | Go to **Core Workflow** — Phase 1 (scope the question tightly) |
| A6 | User says "I just want to see if this works" | Go to **Core Workflow** — Phase 1. Extract the hypothesis first. |

### Intent Route

```
What are you trying to do?
├── ANSWER a specific design question with code → Start at "Core Workflow" — Phase 1
├── COMPARE two approaches empirically → Jump to "Decision Trees > Approach Comparison"
├── EXPLORE an unfamiliar API/library → Go to "Core Workflow" — Phase 1 (tight scope)
├── DISPOSE of a prototype properly → Jump to "Decision Trees > Disposal Protocol"
├── DOCUMENT what was learned from a prototype → "Core Workflow" — Phase 3
└── Not sure? → Start at "Ground Rules" then "Core Workflow"
```

## Core Workflow
**(STANDARD)**

### Phase 1: Form the Hypothesis

Before writing any code, define what you are testing and why.

```
1. STATE THE DESIGN QUESTION
   |-- Ask: "What is the ONE design decision this prototype will inform?"
   |-- Must be a decision, not an exploration. "Which approach is faster?" is a decision.
   |   "Let's see how this library works" is exploration — narrow it to a decision.
   |-- Output: One-sentence design question.

2. STATE THE HYPOTHESIS
   |-- Format: "We believe [Approach X] will work for our use case because [Y].
   |   The prototype will disprove this if [Z] happens."
   |-- The hypothesis must be FALSIFIABLE — there must be a clear failure condition.
   |-- Bad: "We believe Redis will work." (not falsifiable — "work" is undefined)
   |   Good: "We believe Redis Pub/Sub will deliver messages to all subscribers within
   |   50ms for payloads under 1KB. The prototype disproves this if any delivery exceeds
   |   50ms in a 3-node local setup."
   |-- Output: Falsifiable hypothesis statement.

3. SCOPE THE PROTOTYPE
   |-- Ask: "What is the MINIMUM code needed to test this hypothesis?"
   |-- Strip everything that does not directly contribute to answering the question.
   |-- No error handling (unless error behavior IS the question).
   |-- No tests (the prototype IS the test).
   |-- No configuration files, no CI/CD, no documentation beyond inline comments.
   |-- Estimate: "Can this be built in 20 minutes?" If no → split the question.
   |-- Output: Scoped prototype plan with estimated time.
```

### Phase 2: Build and Run

```
4. CREATE ISOLATED ENVIRONMENT
   |-- Option A (preferred): git worktree
   |   `git worktree add --detach ../proto-YYYY-MM-DD-[topic]`
   |-- Option B: temp directory entirely outside the repo
   |   `mkdir ~/prototypes/proto-YYYY-MM-DD-[topic] && cd $_`
   |-- Verify isolation: `git status` in main repo shows no changes.
   |-- Output: Isolated working directory.

5. BUILD THE PROTOTYPE
   |-- START A TIMER. 20 minutes. No exceptions.
   |-- Write the minimum code. Hardcoded values, mocked deps, inline everything.
   |-- At 10 minutes: check progress. Are you halfway to answering the question?
   |   If building infrastructure → you've lost focus. Return to the hypothesis.
   |-- At 18 minutes: STOP adding features. Test the hypothesis now.
   |-- At 20 minutes: TIMER DONE. Stop regardless of state.

6. TEST THE HYPOTHESIS
   |-- Run the prototype against the falsifiable condition.
   |-- Record: HYPOTHESIS CONFIRMED / HYPOTHESIS DISPROVED / INCONCLUSIVE.
   |-- Record the EVIDENCE. What numbers? What behavior? What surprised you?
   |-- If INCONCLUSIVE: the question was too broad or the prototype too narrow.
   |   Document why and what narrower question to try next.
```

### Phase 3: Decide and Dispose

```
7. DOCUMENT THE DECISION
   |-- Create a decision record in the main repo (not the prototype directory):
   |   Format: docs/decisions/YYYY-MM-DD-[topic]-prototype-result.md
   |-- Include: hypothesis, prototype approach, results, decision, evidence quality.
   |-- Evidence quality: HIGH (clear result), MEDIUM (result with caveats), LOW (inconclusive).
   |-- Output: Decision document committed to main repo.

8. DISPOSE OF THE PROTOTYPE
   |-- Option A: `git worktree remove ../proto-YYYY-MM-DD-[topic]`
   |-- Option B: `rm -rf ~/prototypes/proto-YYYY-MM-DD-[topic]`
   |-- Verify: prototype code is GONE. No trace in the main repo.
   |-- The decision document IS the artifact. The code was the instrument.
```

## Best Practices
**(STANDARD)**

1. **Time-box ruthlessly with a hard stop.** Set a timer for 20 minutes or less per prototype. When the timer ends, stop typing — regardless of how close you are. The extra 3.5 hours of "polishing throwaway code" produces zero new information. Use `timeout` command or a phone timer to enforce the boundary. If the question isn't answered after two 20-minute spikes, the scope is too broad and must be narrowed.

2. **Use disposable environments — never the main repo.** Create prototypes in `/tmp/prototypes/`, a git worktree, or a separate Codespace. R6 of the ground rules is non-negotiable: prototype code must never touch the main repository. Main-repo contamination is the #1 cause of prototype-in-production incidents. `git worktree add` or `mkdir` in a disposable location every time.

3. **Fake backends with deterministic mock data.** Use `json-server` for REST APIs, `msw` (Mock Service Worker) for browser apps, or inline JSON mocks. Implement WireMock or Mountebank for complex service virtualization with state transitions. Prototypes answer design questions — not infrastructure questions. A working fake backend that returns known responses isolates the design hypothesis from network instability.

4. **Start with the falsifiable hypothesis, not the code.** Write "We believe X will work because Y. Disproven if Z happens" before opening an editor. The hypothesis format enforces that you're testing a falsifiable claim, not exploring. Every prototype that starts with code before question formation answers the wrong question.

5. **One prototype, one question — compound questions confound results.** Never test "can Kafka handle streaming AND request-response" in one spike. The streaming success masks the request-response failure. You ship both patterns and one requires a rewrite 8 weeks later. If you have two questions, you have two prototypes with two time boxes.

6. **Document shortcuts explicitly — they're the bridge to production.** Every implementation shortcut (in-memory queue instead of persistent, hardcoded credentials, synchronous instead of async) must be recorded. Write "We used X as a shortcut. In production, replace with Y." The decision document is the only artifact that survives prototype disposal.

7. **Celebrate negative results — they save more money than positive ones.** The prototype that proves "this approach won't work for our constraints" saves $40K-$200K in wasted development. Negative results prevent ships heading for icebergs. Log them with the same rigor as positive results. "DISPROVEN" is the most valuable output quality rating.

8. **Scope-box with surgical precision.** Narrow the question to the smallest testable unit. Not "does WebSocket scale?" but "can 100 concurrent WebSocket clients on a single Node.js process maintain < 50ms latency with 1KB payloads?" A scoped question produces a testable hypothesis. A vague question produces an exploration that drifts into implementation.

9. **Use mock data generators, not production data.** Generate realistic test data with Faker.js, `chance`, or domain-specific generators. Never copy production data into a throwaway prototype — the disposable environment has none of the security, access control, or audit logging of production. A prototype credential leak is still a data breach.

10. **Feedback from the prototype feeds into the architecture decision, not the codebase.** The prototype output is a decision document (ADR), not production source code. Route findings through the relevant decision-making skill (system-architect for architecture decisions, api-designer for API choices). The prototype is an instrument for measurement, not a draft for implementation.

## Decision Trees
**(QUICK)**

### Approach Comparison

```
                     ┌──────────────────────┐
                     │ Two (or more)          │
                     │ approaches to compare  │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Can the comparison be  │
                     │ resolved by reading    │
                     │ docs/source?           │
                     └──────┬─────────┬─────┘
                            │YES       │NO
                            ▼          ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ Read the docs.│ │ Identify the KEY   │
                   │ No prototype  │ │ DIFFERENTIATOR:    │
                   │ needed. Decide│ │ what do these       │
                   │ now.          │ │ approaches do       │
                   └──────────────┘ │ DIFFERENTLY that    │
                                    │ matters?            │
                                    └──────┬─────────┬───┘
                                           │
                                ┌──────────▼──────────┐
                                │ Can the differentiator │
                                │ be tested in < 20 min? │
                                └──────┬─────────┬─────┘
                                       │YES       │NO
                                       ▼          ▼
                              ┌──────────────┐ ┌──────────────────┐
                              │ Build ONE      │ │ Split into N       │
                              │ prototype that │ │ smaller questions. │
                              │ exercises the  │ │ Each gets its own  │
                              │ differentiator.│ │ 20-min prototype.  │
                              │ Compare results│ └──────────────────┘
                              │ for both.      │
                              └──────────────┘
```

### Disposal Protocol

```
                     ┌──────────────────────┐
                     │ Prototype complete.    │
                     │ Hypothesis tested.     │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Is the decision doc    │
                     │ committed to main repo?│
                     └──────┬─────────┬─────┘
                            │NO        │YES
                            ▼          ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ Write and      │ │ Is the prototype    │
                   │ commit the     │ │ directory isolated  │
                   │ decision doc   │ │ from main repo?     │
                   │ first. Do not  │ └──────┬─────────┬───┘
                   │ dispose without│        │YES       │NO
                   │ documentation. │        ▼          ▼
                   └──────────────┘ ┌──────────────┐ ┌──────────────────┐
                                    │ Delete the     │ │ Move prototype     │
                                    │ prototype      │ │ files to isolated  │
                                    │ directory:     │ │ directory FIRST,   │
                                    │ rm -rf or      │ │ then delete.       │
                                    │ git worktree   │ │ NEVER delete from  │
                                    │ remove.        │ │ within main tree.  │
                                    └──────────────┘ └──────────────────┘
```

### Time-Box Enforcement

```
                     ┌──────────────────────┐
                     │ Prototype started.     │
                     │ Timer: 20:00           │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ 10:00 check: Are you  │
                     │ building infra or     │
                     │ testing hypothesis?   │
                     └──────┬─────────┬─────┘
                            │INFRA     │HYPOTHESIS
                            ▼          ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ STOP. Return  │ │ Continue. At 18:00:│
                   │ to hypothesis. │ │ STOP adding. Test │
                   │ What is the    │ │ what you have.    │
                   │ MINIMUM code?  │ │ At 20:00: STOP    │
                   │ Split if needed│ │ regardless.       │
                   └──────────────┘ └──────────────────┘
```

### Question Scoping

```
                     ┌──────────────────────┐
                     │ Design question to     │
                     │ answer by prototype    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Can you describe the   │
                     │ MINIMUM code to test   │
                     │ this in < 3 sentences? │
                     └──────┬─────────┬─────┘
                            │YES       │NO
                            ▼          ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ Good. Estimate │ │ Question is too    │
                   │ time. If > 20  │ │ broad. Split:      │
                   │ min → split.   │ │ "What is the ONE   │
                   │ If ≤ 20 → build│ │ thing we most need │
                   └──────────────┘ │ to know?" Prototype │
                                    │ that first.         │
                                    └──────────────────┘
```

### Evidence Quality Assessment

```
                     ┌──────────────────────┐
                     │ Prototype results      │
                     │ obtained               │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼──────────┐
                     │ Was the hypothesis     │
                     │ CLEARLY confirmed or   │
                     │ disproved?             │
                     └──────┬─────────┬─────┘
                            │YES                 │NO
                            ▼                    ▼
                   ┌──────────────┐ ┌──────────────────┐
                   │ QUALITY: HIGH │ │ Were the results    │
                   │ Decision can  │ │ directionally clear │
                   │ be made with  │ │ but with caveats?   │
                   │ confidence.   │ └──────┬─────────┬───┘
                   └──────────────┘        │YES       │NO
                                           ▼          ▼
                                  ┌──────────────┐ ┌──────────────────┐
                                  │ QUALITY:      │ │ QUALITY: LOW      │
                                  │ MEDIUM        │ │ Do not make the   │
                                  │ Decision can  │ │ decision from this│
                                  │ be made with  │ │ prototype. Re-    │
                                  │ caveats noted.│ │ scope with tighter│
                                  └──────────────┘ │ question.         │
                                                   └──────────────────┘
```


## Error Recovery
**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Error Decoder
**(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| "The prototype is almost done — give me 20 more minutes" repeated 4 times | Scope creep disguised as "polishing." The hypothesis was answered at minute 12; the remaining time was making the code presentable, adding edge cases, refactoring for readability | Call "time's up" immediately. Read the hypothesis aloud. If it's answered, dispose the prototype. If it's not, the scope was too broad — narrow and run a second 20-minute spike | Polishing throwaway code is a cognitive trap. At $150/hr, 40 minutes of polishing per prototype × 50 prototypes/year = $5K/year burned making disposable code look nice |
| Prototype produced a clear result, but the team debates its validity for 45 minutes | The prototype tested the wrong variable. WebSocket latency on gigabit WiFi doesn't answer "can mobile users on 3G maintain connections?" The result is valid but irrelevant to the actual decision | Before debating results, re-read the hypothesis together. If the hypothesis doesn't match the actual decision, the prototype was a red herring — discard results and run a new prototype with the correct variable | Wrong-variable prototypes are more dangerous than no prototype — they produce confident wrong answers. Verify the hypothesis maps to the actual business decision before running code |
| Two engineers built prototypes for the same question and got opposite results | Different experimental conditions: one tested with 100 records, the other with 100K. One measured cold starts, the other measured warm caches. The prototypes tested different things but both claim to answer the same question | Run a joint prototype session with both engineers present. Agree on experimental parameters (dataset size, measurement point, environment) before any code is written. Make the hypothesis falsification criteria identical and shared | Without shared experimental parameters, prototype results are not comparable. A disagreement about "which approach is faster" is usually a disagreement about experimental conditions in disguise |
| Production incident traced to prototype code that "should have been deleted" | A developer built in the main repo, didn't follow disposal protocol, the PM shipped it. Six months later the developer left and nobody knew the caching layer was a prototype. Hardcoded TTL expired, site went down | Git-bisect to find the original commit. Check the decision document to understand the intended production replacement. If no document exists, treat it as production debt: write tests, add error handling, document the assumptions | R6 (never prototype in main repo) exists because this has happened hundreds of times. The most expensive prototype isn't the one that takes too long — it's the one that becomes production code without anyone noticing |
| Prototype "proved" an approach works, but the production implementation failed | The prototype tested the happy path with ideal conditions, no error handling, and fresh caches. Production encountered cold caches, network partitions, malformed inputs, and concurrent writes — conditions the prototype never exercised | Augment prototype scope with failure-mode testing in the next spike. Not "does this approach work?" but "does this approach survive X, Y, Z failure modes?" Explicitly list what was NOT tested in the decision document | Prototype results are only as good as the failure modes they test. A "HIGH" quality result that only tests the happy path should be downgraded to "MEDIUM — happy path only, no failure mode testing" |
| Stakeholder sees the prototype and says "this is great, ship it next sprint" | The prototype UI looks polished because the developer spent 30 minutes making it presentable. Stakeholder perceives a nearly-finished product, not a throwaway spike. The time spent "making it presentable" directly causes the prototype-in-production trap | Show prototypes as ASCII diagrams, CLI output, or rough sketches. Never present a polished prototype UI to a non-technical stakeholder. If UI feedback is needed, use wireframes or Figma mockups — not running code | The visual quality of a prototype is inversely correlated with the likelihood of proper disposal. The uglier the prototype looks, the less likely anyone will ask to ship it. Ship ugly prototypes for internal consumption |

## Cross-Skill Coordination

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Prototype question emerged from brainstorming | brainstorming | Brainstorming identified the uncertainty; prototype resolves it empirically. Return decision to brainstorming. |
| Prototype tests an architectural assumption | system-architect | Architectural decisions affect system design; system-architect defines evaluation criteria for prototype |
| Prototype results inform production implementation | fullstack-developer, backend-developer, frontend-developer | Decision document hands off to developer who builds the real implementation — with empirical evidence, not guesses |
| Multiple technologies being evaluated | system-architect | System-architect provides evaluation dimensions (scalability, maintainability, team capability) |
| Prototype reveals API design implications | api-designer | API behavior discovered in prototype may inform contract design |
| Prototype involves database or data model questions | database-designer | Database behavior (query patterns, indexing, consistency) may need schema expertise |
| Prototype reveals performance characteristics | performance-engineer | If prototype shows performance concerns, escalate to proper benchmarking — prototype measurements are directional only |


| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | Architecture decisions, technology constraints, system boundaries | Before implementing features that cross system boundaries |
| `api-designer` | API contracts, versioning strategy, rate limiting, error handling | Before building API-consuming code |


## Proactive Triggers

| # | Trigger Condition | Auto-Response |
|---|------------------|---------------|
| P1 | User starts building infrastructure (config files, CI, project scaffolding) during prototype time | [ALERT] "You're building scaffolding, not testing a hypothesis. A prototype has no config files, no CI, no project structure. What is the MINIMUM code to answer the question?" |
| P2 | User mentions keeping or iterating on prototype code | [GATE] "Prototype code never ships. The decision document is the artifact. We'll dispose of the code after we document what we learned." |
| P3 | Prototype exceeds 20 minutes without answering the question | [SPLIT] "Time box exceeded. The question is too broad. What sub-question can we answer in 20 minutes? Let's scope down." |
| P4 | User draws production conclusions from prototype results | [WARN] "Prototype results are directional. Performance is 2-10x off. Reliability is untested. Use these results ONLY to decide whether to proceed — not to guarantee production behavior." |
| P5 | Prototype code appears in the main source tree | [ISOLATE] "Prototype code detected in main repo. Move to isolated directory immediately. Use git worktree or temp directory." |
| P6 | User cannot articulate the hypothesis | [REQUIRE] "A prototype without a hypothesis is exploration, not experimentation. State: 'We believe [X] because [Y]. The prototype disproves this if [Z].'" |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## What Good Looks Like

```
BEFORE (Unstructured Experimentation):
"Let's try out this new GraphQL library. I'll set up a project,
add the dependencies, configure TypeScript, set up the schema,
and build a few queries to see how it feels."
→ 3 hours later: has a half-built GraphQL server with no clear
  decision reached but plenty of code "worth keeping."

AFTER (Disciplined Prototype):
QUESTION: "Can we use graphql-yoga to replace our REST endpoints
for the user profile page, given our requirement of < 200ms
response time for queries joining 3 data sources?"

HYPOTHESIS: "We believe graphql-yoga with DataLoader batching will
resolve a 3-source user profile query in < 200ms. The prototype
disproves this if any query exceeds 200ms in local testing."

SCOPE: One schema (User + Posts + Comments), one resolver chain
using DataLoader, in-memory mock data (1000 users, 50 posts/user).

BUILD (18 min):
- 1 file: index.ts with hardcoded schema, mocked data, single query
- No TypeScript config (use ts-node --esm), no tests, no error handling
- Timer: built in 14 minutes. 4 minutes to test.

RESULT: 3-source query averaged 78ms locally. HYPOTHESIS CONFIRMED.
Caveat: local in-memory data. Real database may add latency.

DECISION: Proceed with graphql-yoga for user profile. Prototype
suggests latency target is achievable. Note: need database-benchmark
follow-up before production deployment.

DISPOSE: rm -rf ../proto-2026-07-23-graphql-yoga
Decision doc committed: docs/decisions/2026-07-23-graphql-yoga-viability.md

Total time: 22 minutes. Decision made with evidence.
```

## Deliberate Practice

### Exercise 1: Hypothesis Extraction (5 min)
Take your last 3 "I was just trying something out" coding sessions. For each, write the hypothesis you were testing. If you cannot write one, you were playing, not prototyping. Repeat until every coding session has a hypothesis.

### Exercise 2: 20-Minute Constraint Drill (20 min)
Pick a design question from your current work. Set a 20-minute timer. Build the prototype. When the timer goes off, STOP — even if it's not working. Document: did you answer the question? If not, what was too broad? Split and repeat.

### Exercise 3: Disposal Practice (5 min)
Find prototype or spike code in your current project that survived. For each file: write the decision it informed (if any), then delete it. If the code is in production, write a ticket to replace it with production-quality code. Count how many prototype files you found — this number IS your prototype discipline gap.

### Exercise 4: One-Question Discipline (10 min)
Look at a prototype you built recently. Count how many design questions it attempted to answer. If > 1, split the prototype's results: which question did it ACTUALLY answer? Which were confounded? Rewrite as separate prototype plans.

### Exercise 5: Evidence Quality Audit (15 min)
Review your last 5 prototype-based decisions. Rate each as HIGH/MEDIUM/LOW evidence quality. For LOW-quality decisions: what would a better prototype have looked like? If you made a production decision on LOW-quality evidence, flag it for revisit.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "We'll clean it up and ship it — the prototype is basically done." | Prototype code has no error handling, no tests, and hardcoded credentials. "Next sprint" becomes "next quarter" becomes a **$200K-$500K** production incident from duplicate charges, data corruption, or credential leaks. Prototype code is deleted before production code is written — never the other way around. |
| "It's just a quick spike — I don't need to isolate it from the main repo." | The spike ends up in production, the engineer leaves, and six months later on-call has no idea the caching layer was a prototype. Cost: **$50K-$200K** in incident response and institutional knowledge loss. Ground Rule R6 is non-negotiable: never prototype in the main repo. |
| "The docs say this API works for our use case — we can skip the prototype." | Docs describe what an API CAN do, not what it does FOR YOUR USE CASE. Two sprints in, you discover the payment provider requires US bank accounts but 40% of your vendors are international. Cost: **$40K-$150K** in wasted development and a 6-week vendor switch. |
| "I'll extend the time box by an hour — I'm almost there." | The answer was clear at 18 minutes. The extra 3.5 hours polished throwaway code that produced zero new information. At $150/hr across a team, that's **$5K-$20K/year/engineer** in prototype creep. The time box is a HARD STOP — when the timer ends, you stop typing. |
| "We can answer two questions with one prototype — it's more efficient." | Mixing use cases confounds results. Streaming success masks request-response failure. You ship both, and the broken pattern requires a $65K rewrite 8 weeks later. Cost: **$30K-$100K** per confounded prototype. One question per prototype. ALWAYS. |

## Anti-Patterns

### Anti-Pattern: "I'll just clean this up later"
**What it looks like:** A fintech startup builds a "prototype" payment integration with no idempotency, no retry logic, hardcoded test credentials. PM says "ship it and we'll clean it up next sprint." Next sprint becomes next quarter. Six months later, a network blip causes duplicate charges — $340K in refunds, fines, and lost merchant trust.
**Why it fails:** Prototype code has zero production safeguards. The cleanup that would take 3 days during development takes 3 weeks when retrofitted under incident pressure. The most expensive four words in software: "we'll fix it later."
**Do this instead:** Enforce the disposal protocol: prototype code is deleted before production code is written. The decision document IS the deliverable. If a prototype proved the approach, implement the production version from scratch following production standards — no prototype code reused.

### Anti-Pattern: Testing the easiest variable, not the right one
**What it looks like:** Team prototypes WebSocket performance on gigabit WiFi, achieves 10K connections at < 5ms latency, ships WebSockets. Real users are on 3G in rural areas. Battery drain and connection drops make the feature unusable for 60% of users. The prototype tested "is this fast on ideal conditions?" when the real question was "does this work for our actual users?"
**Why it fails:** Prototypes gravitate toward the cleanest, fastest, most impressive result — which is almost never the condition that matters. The variable that's easiest to test is rarely the variable the business decision hinges on.
**Do this instead:** Phase 1, Step 1: identify the riskiest assumption, not the easiest test. Ask "what condition makes this fail for our users?" and test that. If mobile users on poor connections are 60% of revenue, test on simulated 3G latency and packet loss — not gigabit WiFi.

### Anti-Pattern: Prototype shortcut becomes the architecture
**What it looks like:** Team prototypes event-driven architecture with an in-memory message bus. The pattern works cleanly. They adopt event-driven but never replace the in-memory bus with a persistent one. First production restart: all unprocessed events lost, customer orders disappear. The in-memory shortcut was an implementation convenience that silently graduated to architectural decision.
**Why it fails:** Prototype shortcuts are not documented as shortcuts. When the prototype "works," the shortcut and the design decision merge in everyone's mental model. The code is adopted wholesale, shortcut included, because nobody documented "replace in-memory bus with persistent queue before production."
**Do this instead:** Document every shortcut in the decision record: "We used X as a shortcut. In production, replace with Y." The document is the bridge between prototype and production. If a shortcut would take more than 2 days to undo, stop the prototype and fix it now.

### Anti-Pattern: Time-box creep — "just one more hour"
**What it looks like:** Developer's 20-minute prototype turns into a 4-hour deep dive. The answer was clear at 18 minutes (yes, the query pattern works). The additional 3.5 hours were spent refactoring, adding comments, making it "presentable." At $150/hr, $525 of engineering time burned polishing throwaway code.
**Why it fails:** The time box is a soft boundary without enforcement. "Just one more minute" compounds into hours. The additional time produces zero new information — the hypothesis was already answered. Every minute beyond the time box is code golf, not prototyping.
**Do this instead:** The time box is a HARD STOP enforced by a timer. When the timer ends, stop typing. No exceptions. No "one more minute." If the question genuinely isn't answered after 20 minutes, end the session, narrow the scope, and start a fresh 20-minute spike with a tighter hypothesis.

### Anti-Pattern: Two questions in one prototype
**What it looks like:** Team prototypes "can we use Kafka for both event streaming AND request-response patterns?" The streaming test succeeds, the request-response test requires unnatural workarounds — but the streaming success masks the request-response failure. Product ships with Kafka for both patterns. The request-response system requires a $65K REST rewrite 8 weeks later.
**Why it fails:** Combined results are confounded results. When one sub-question succeeds and the other fails, the overall result is "mixed" — which stakeholders interpret as "good enough." Disentangling the two questions after the fact requires re-running separate prototypes anyway.
**Do this instead:** One question per prototype. ALWAYS. Two questions = two prototypes with two time boxes and two decision documents. If the questions are interdependent (answer to Q1 determines what Q2 should be), run them sequentially — Q1 first, document the result, then design Q2 based on the outcome.

### Anti-Pattern: "The docs say it works — we don't need a prototype"
**What it looks like:** Team reads Stripe Connect docs, concludes it works for their multi-vendor marketplace. Skip the prototype, start building. Two sprints in, they discover Stripe Connect's onboarding requires every vendor to have a US bank account. 40% of their vendors are international. $120K in wasted development, 6-week vendor switch delay.
**Why it fails:** Docs describe what an API CAN do generically. A prototype tests what it CAN do FOR YOUR SPECIFIC USE CASE. These are fundamentally different things. Documentation generalizes; your constraints are specific and often edge cases.
**Do this instead:** Always run at least one 20-minute prototype even when documentation looks perfect. Test with your actual constraints, data shapes, and edge cases — not the documentation's happy-path examples. The prototype that takes 15 minutes and reveals a dealbreaker saves 2+ sprints of wasted implementation.

### Anti-Pattern: Prototype in the main repo — the invisible landmine
**What it looks like:** Senior engineer builds a "quick prototype" caching layer directly in the main repo because "it's just for testing." Six months later, engineer has left the company. Caching code is in production with no tests, no docs, hardcoded TTL. TTL expires during peak traffic, site goes down. On-call has no idea the caching layer was a prototype.
**Why it fails:** Main-repo prototypes have no disposal trigger, no documentation, and no ownership. They survive because nobody knows they should be deleted. When the author leaves, the institutional knowledge that "this was a prototype" leaves with them.
**Do this instead:** Ground Rule R6 is non-negotiable: NEVER prototype in the main repo. Use `git worktree add`, a separate Codespace, or a directory outside the repo. Isolation forces explicit disposal. The extra 30 seconds to create a separate workspace prevents $50K-$200K in future incident response.

## Production Checklist
**(STANDARD)**

Before concluding any prototype session, verify every item. An unchecked item is a future production incident or a wasted spike.

- [ ] **Hypothesis stated in falsifiable format:** "We believe X because Y. Disproven if Z." The Z condition is specific and testable — not "it doesn't work" but "latency exceeds 50ms at 100 concurrent connections."
- [ ] **Single question verified:** Exactly one design question is being tested. No compound questions, no bundled explorations. If a second question emerged during the spike, it's logged for a separate prototype.
- [ ] **Time box set and honored:** Timer was started before any code was written. No extensions granted. Dispose triggered at the hard stop regardless of perceived "closeness to answer."
- [ ] **Isolation confirmed:** Prototype code lives outside the main repository. `git status` in main repo shows zero prototype files. A `git worktree add` or `/tmp/prototypes/` directory was used.
- [ ] **Mock data is synthetic:** No production data, credentials, or PII exists in the prototype environment. All data is generated via Faker.js, chance, or hardcoded mock responses.
- [ ] **Shortcuts documented in decision record:** Every implementation shortcut (in-memory queue, hardcoded config, synchronous-where-async) is explicitly listed with the intended production replacement.
- [ ] **Decision document committed:** `docs/decisions/YYYY-MM-DD-[topic]-prototype-result.md` exists in the main repo. Contains hypothesis, approach, results, decision, evidence quality rating (HIGH/MEDIUM/LOW), and shortcut inventory.
- [ ] **Evidence quality rated honestly:** HIGH only if conditions matched production reality. MEDIUM if tested with ideal conditions. LOW if inconclusive. Production decisions never made on LOW-quality evidence without a confirmation spike.
- [ ] **Prototype disposed:** Prototype directory deleted. `rm -rf` or `git worktree remove` confirmed. No trace of prototype code remains in any persistent storage.
- [ ] **Negative results celebrated:** If the hypothesis was DISPROVEN, the decision document explicitly frames this as valuable: "This prototype saved $X in avoided development by proving approach Y doesn't work for constraint Z."
- [ ] **Next action clear:** Decision document ends with: (a) proceed to production implementation with path Y, (b) run confirmation prototype with broader conditions, or (c) abandon approach Z permanently.
- [ ] **No prototype UI shown to non-technical stakeholders:** If a visual prototype existed, it was destroyed before stakeholder demos. Any UI feedback needed was gathered through wireframes, mockups, or static comps — not running code.

## Verification

- [ ] **Ground Rules:** All 7 ground rules checked. No prototype code in main repo. No multi-question prototypes.
- [ ] **Single question:** Prototype addresses exactly ONE design question. Scope document confirms singular focus.
- [ ] **Falsifiable hypothesis:** Hypothesis stated in "We believe X because Y. Disproven if Z" format. Failure condition is specific and testable.
- [ ] **Time box respected:** Prototype completed in ≤ 20 minutes. Timer was started and honored. No extensions granted.
- [ ] **Isolation verified:** Prototype directory is outside main repo. `git status` in main repo shows no prototype files.
- [ ] **Decision documented:** Decision record committed to main repo. Includes hypothesis, approach, results, decision, and evidence quality rating.
- [ ] **Prototype disposed:** Prototype directory deleted. `rm -rf` or `git worktree remove` confirmed. No trace remains.
- [ ] **Evidence quality rated:** HIGH (clear result), MEDIUM (result with caveats), or LOW (inconclusive). Production decisions not made on LOW quality evidence.
- [ ] **Prototype shortcuts documented:** Any implementation shortcuts that differ from production intent are documented in the decision record.

If any check fails: return to the corresponding phase, resolve, and restart verification from that item.

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## References

- **(../references/prototype-isolation.md)** — Git worktree setup guide for prototype isolation. Commands, cleanup procedures, and handling nested dependencies. Comparison with temp directory and Docker-based isolation approaches.
- **(../references/time-boxing.md)** — The 20-minute time box methodology. Timer protocols, 10-minute checkpoint, 18-minute feature freeze. Evidence that prototype value plateaus after 20 minutes and what to do when the timer expires.
- **(../references/decision-documentation.md)** — Template and protocol for prototype decision records. Includes hypothesis format, evidence quality assessment rubric, and archive structure for organizational learning from prototypes.
- **(../references/throwaway-discipline.md)** — The psychology and practice of throwing away code. Anti-patterns (sunk cost, "almost production"), disposal rituals, and organizational culture change for treating prototypes as disposable instruments.
- **(../references/question-scoping.md)** — Methodology for scoping design questions to be prototype-answerable. Question splitting algorithms, falsifiability criteria, and the "can you describe the minimum code in 3 sentences?" test.
- **(../references/empirical-evidence.md)** — Framework for evaluating prototype evidence quality. HIGH/MEDIUM/LOW classification criteria, confounded variable detection, and when prototype evidence is sufficient for a production decision.
- **(../references/anti-shipping-patterns.md)** — Catalog of the 10 most common ways prototype code enters production. Each pattern includes detection signals, real-world case studies, and prevention mechanisms.
- **(../references/git-worktree-setup.md)** — Practical guide to using git-worktree for prototype isolation. Commands, cleanup, handling uncommitted changes, and integration with the disposal protocol.
