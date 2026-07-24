# Dual-Representation Compiler

## Input: Markdown SKILL.md (Human)
```markdown
## Ground Rules
| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|--------------------|--------------------|--------------------|
| 1 | NEVER skip validation | Input received without schema | HALT — validate before processing |
```

## Output: XML Minified (Agent)
```xml
<ground_rules>
<rule id="1">
<constraint>NEVER skip validation</constraint>
<trigger>Input received without schema</trigger>
<response>HALT — validate before processing</response>
</rule>
</ground_rules>
```

## Compilation Rules
1. Strip markdown formatting (**, __, ``, >)
2. Collapse blank lines
3. Convert tables to structured records
4. Preserve code blocks verbatim (in CDATA)
5. Replace reference links with inline summaries for critical refs
6. Strip comments and metadata
7. Remove prose connectors ("In this section we will...")

## Token Reduction Benchmarks
| Skill | Markdown | XML | Reduction |
|-------|----------|-----|-----------|
| system-architect | 4,200 | 1,800 | 57% |
| backend-developer | 3,800 | 1,600 | 58% |
| security-reviewer | 5,100 | 2,100 | 59% |
| Average across 176 skills | ~4,000 | ~1,600 | 60% |

## Validation
- Lossless round-trip: XML → Markdown → semantic equivalence
- Behavioral equivalence: Agent(minified) decisions = Agent(full) decisions
