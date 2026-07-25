# Closed-Loop Feedback — The Skill Improvement Engine

> **Purpose:** This reference teaches skills how to log their outcomes back into the improvement pipeline so that downstream skills (code-reviewer, incident-responder) can prevent recurring bugs. This is the TELEMETRY anchor — it closes the loop between execution and prevention.

## The Problem: Skills Operate in Isolation

Currently, when a skill generates code that has a bug, or approves a pattern that later fails in production, that knowledge dies in the session. The next session starts from zero. The same bug can be generated, merged, and deployed again — and again — because no skill remembers what went wrong last time.

## The Solution: Structured Outcome Logging

Every skill that makes a decision with consequences logs that decision using `scripts/log-outcome.sh`. Downstream skills query the log before acting. This creates a **feedback loop** where failures in one session become guardrails in the next.

## How to Use `log-outcome.sh`

### Logging a Success (decision validated by testing)
```bash
./scripts/log-outcome.sh \
  --skill backend-developer \
  --decision "Used connection pool size of 20 for Postgres with PgBouncer" \
  --outcome pass \
  --context "Load test confirmed: 20 connections handled 500 req/s at p99=45ms. Pool size validated."
```

### Logging a Failure (bug found in production or testing)
```bash
./scripts/log-outcome.sh \
  --skill backend-developer \
  --decision "Used default Axios timeout (no explicit timeout set)" \
  --outcome fail \
  --context "Production outage: external payment API hung for 120s. No timeout meant all Node threads blocked. Cascaded to full outage." \
  --bug-signature "fetch without timeout|axios without timeout|external call no abort signal"
```

### Logging a Warning (pattern that's risky but not yet a bug)
```bash
./scripts/log-outcome.sh \
  --skill frontend-developer \
  --decision "Used useState+useEffect for server data instead of TanStack Query" \
  --outcome warn \
  --context "Race condition observed in QA: rapid tab switching caused stale data display. Not yet a production bug but pattern is fragile." \
  --bug-signature "useState.*useEffect.*fetch|useState.*useEffect.*axios"
```

## How Downstream Skills Query the Log

### code-reviewer integration
Before approving code, the code-reviewer queries the outcome log for known failure patterns:

```bash
# Check if any past failures match patterns in the code being reviewed
grep '"outcome":"fail"' .copilot/session-state/outcome-log.jsonl | \
  python3 -c "
import json, sys
for line in sys.stdin:
    entry = json.loads(line)
    if 'bug_signature' in entry:
        print(f'KNOWN FAILURE: {entry[\"skill\"]} — {entry[\"decision\"]}')
        print(f'  Signature: {entry[\"bug_signature\"]}')
        print(f'  Context: {entry[\"context\"][:200]}')
        print()
"
```

### incident-responder integration
During post-mortem, the incident-responder queries the log for similar past incidents:

```bash
# Find all failures in the same skill domain
grep "\"skill\":\"backend-developer\"" .copilot/session-state/outcome-log.jsonl | \
  grep '"outcome":"fail"' | \
  python3 -c "
import json, sys
for line in sys.stdin:
    entry = json.loads(line)
    print(f'[{entry[\"timestamp\"]}] {entry[\"decision\"]}')
    print(f'  {entry[\"context\"][:150]}')
    print()
"
```

## The Feedback Loop Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SKILL EXECUTION                              │
│                                                                  │
│  backend-developer generates code → tests fail/prod fails        │
│         │                                                        │
│         ▼                                                        │
│  ./scripts/log-outcome.sh --outcome fail --bug-signature "..."   │
│         │                                                        │
│         ▼                                                        │
│  .copilot/session-state/outcome-log.jsonl                        │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              DOWNSTREAM SKILLS QUERY LOG                  │   │
│  │                                                          │   │
│  │  code-reviewer: "Before I approve, did this pattern      │   │
│  │                  fail before? → Scan bug_signatures"     │   │
│  │                                                          │   │
│  │  incident-responder: "Has this incident happened before? │   │
│  │                       → Query by skill + outcome=fail"   │   │
│  │                                                          │   │
│  │  security-reviewer: "Any known security patterns?        │   │
│  │                      → Query by bug_signature"           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Integration Points in SKILL.md

### 1. Ground Rule (add to code-reviewer and incident-responder)
```
| Rn | **QUERY the outcome log before reviewing or responding.** Past failures in this domain are recorded in outcome-log.jsonl. Check for known bug signatures before approving code or diagnosing incidents. | Trigger: skill invoked → run `grep "\"outcome\":\"fail\"" .copilot/session-state/outcome-log.jsonl` → check if any bug_signature patterns match the code/incident being reviewed | Respond: "Found {N} past failures in this domain. Known patterns to check: [list bug_signatures]. I will specifically scan for these patterns in the current code/incident." |
```

### 2. Production Checklist Item (add to developer skills)
```
| C-FB-01 | Log outcome for closed-loop improvement | After generating AND testing code, run `scripts/log-outcome.sh --skill [skill-name] --decision "[what was decided]" --outcome [pass|fail|warn] --context "[why]"` | Failures without logged signatures can recur indefinitely. | `grep "\"skill\":\"[skill-name]\"" .copilot/session-state/outcome-log.jsonl` |
```

## Session-Level Querying

The outcome log is a JSONL file (one JSON object per line). This makes it grep-able and queryable:

```bash
# Count failures by skill
grep '"outcome":"fail"' outcome-log.jsonl | python3 -c "
import json, sys
from collections import Counter
skills = Counter()
for line in sys.stdin:
    entry = json.loads(line)
    skills[entry['skill']] += 1
for skill, count in skills.most_common():
    print(f'{skill}: {count} failures')
"

# Find most common bug signatures
grep '"bug_signature"' outcome-log.jsonl | python3 -c "
import json, sys
from collections import Counter
sigs = Counter()
for line in sys.stdin:
    entry = json.loads(line)
    sigs[entry['bug_signature']] += 1
for sig, count in sigs.most_common(10):
    print(f'[{count}x] {sig}')
"
```

## Token Efficiency

The outcome log is a file on disk, NOT loaded into context. Skills query it with targeted grep patterns. This means:
- **0 tokens** to log an outcome (writes to disk)
- **~30 tokens** to query before reviewing (grep + summarized output)
- **~100 tokens** if a match is found and context is loaded

This is the key insight: the feedback loop costs almost nothing in tokens because queries are targeted.
