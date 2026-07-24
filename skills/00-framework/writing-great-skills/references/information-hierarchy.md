# Information Hierarchy

## The Ladder

```
STEPS (always loaded, high priority)
  │
  ├── Core Workflow phases
  ├── Decision Trees
  └── Route the Request tables
  │
  ▼
REFERENCE (loaded on-demand, medium priority)
  │
  ├── Ground Rules
  ├── Gotchas
  ├── Verification checklists
  └── Proactive Triggers
  │
  ▼
EXTERNAL (loaded only when explicitly referenced)
  │
  ├── references/*.md files
  └── External URLs
```

## Progressive Disclosure Principle

Material is pushed as far outward on the ladder as possible:
1. If it's procedural (do X, then Y) → steps
2. If it's definitional (X means Y) → reference or external
3. If it's rarely needed → external
4. If it's large (>50 lines) → external

## Token Cost by Position

| Position | Token Cost | When Loaded |
|----------|-----------|-------------|
| In-skill, steps section | Full cost every invocation | Always |
| In-skill, reference section | Full cost if consulted | On-demand (model chooses) |
| references/ directory | Cost of reading the file | Only when explicitly opened |
| External URL | Cost of fetching | Only when explicitly requested |

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Definitions in steps | Bloats every invocation with rarely-needed definitions | Move to references |
| Tutorials in reference | Ordered material in unordered section confuses the model | Move to steps or external |
| Everything in-skill | Token budget exhausted; model ignores half the content | Push outward aggressively |
| External for critical rules | Model never loads critical constraints | Keep ground rules in-skill |
