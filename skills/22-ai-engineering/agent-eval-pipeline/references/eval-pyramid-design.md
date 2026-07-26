# Agent Eval Pyramid Design

## Testing Pyramid for AI Agents

```
       ┌──────┐
       │  E2E │  5-10 full task runs, slow (15-60 min)
       ├──────┤
       │ INT  │  10-30 workflow runs, moderate (5-15 min)
       ├──────┤
       │ UNIT │  30-100 capability runs, fast (< 1 min)
       ├──────┤
       │STATIC│  Instantaneous — linting, schema checks
       └──────┘
```

## Level Details

### Static (L0) — 0 tokens, < 1s
- YAML frontmatter validation
- Section presence checks
- Reference link resolution
- Schema compliance verification

### Unit Evals (L1) — ~500 tokens/run, < 1 min
- Single capability: "Does agent follow Ground Rule #3?"
- Assertion or simple rubric grading
- 30-100 runs for statistical significance

### Integration Evals (L2) — ~2K tokens/run, 5-15 min
- Multi-step workflow: "Design → Implement → Test"
- LLM-as-judge grading
- 10-30 runs

### End-to-End Evals (L3) — ~10K tokens/run, 15-60 min
- Complete task from user request
- Multi-dimensional rubric
- 5-10 runs

### Adversarial Evals (LX) — crosses all levels
- Prompt injection, edge cases, stress
- Binary pass/fail per attack
- 100+ variants
