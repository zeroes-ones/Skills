# Chain Integrity Validator — Specification

## 6 Validation Rules

### R1: Bilateral Consistency

```

FOR each skill S:
  FOR each downstream D in S.feeds_into:
    IF D.consumes_from NOT contains S:
      REPORT "BROKEN: {S} → {D} (D does not consume)"

```

### R2: No Self-Reference

```

FOR each skill S:
  IF S in S.consumes_from OR S in S.feeds_into:
    REPORT "SELF-REF: {S} references itself"

```

### R3: No Dead Ends

```

FOR each skill S:
  IF S.feeds_into is empty AND S is NOT documented as terminal:
    REPORT "DEAD_END: {S} has no downstream consumers"

```

### R4: Alternatives Exist

```

FOR each skill S:
  FOR each A in S.alternatives:
    IF A NOT in skill_registry:
      REPORT "GHOST: {S} alternative {A} does not exist"

```

### R5: Section Matches Chain

```

FOR each skill S:
  Let upstream_from_section = skills in Cross-Skill → Upstream
  Let downstream_from_section = skills in Cross-Skill → Downstream
  IF upstream_from_section NOT subset of S.consumes_from:
    REPORT "DOC_MISMATCH: {S} documents upstream {X} but doesn't consume_from it"

```

### R6: Pattern Declared

```

FOR each skill S:
  FOR each U in S.consumes_from:
    IF Cross-Skill section doesn't declare pattern for U:
      REPORT "NO_PATTERN: {S} consumes from {U} without declared pattern"

```

## Auto-Fix Capabilities

| Violation | Auto-Fix? | Fix Action |
|-----------|-----------|------------|
| BROKEN (feeds_into without consume) | Semi-auto | Prompt: "Add consumes_from or remove feeds_into?" |
| SELF-REF | Auto | Remove self from list |
| DEAD_END | Manual | Mark as terminal or add downstream |
| GHOST alternative | Auto | Remove from alternatives list |
| DOC_MISMATCH | Auto | Sync section to match YAML |
| NO_PATTERN | Manual | Requires human to declare pattern |

## CI Integration

```yaml
# .github/workflows/chain-integrity.yml
on: [push, pull_request]
jobs:
  validate-chains:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/validate-chains.sh
      - if: failure()
        run: echo "Chain integrity violation — see logs"

```
