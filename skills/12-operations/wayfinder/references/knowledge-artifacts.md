# Knowledge Artifacts

## The Artifact-as-Currency Principle

Investigation produces knowledge. Knowledge is only valuable if it's captured in a durable, discoverable format. The artifact IS the deliverable — not the act of investigation.

## Artifact Types

| Type | Format | When to Use | Example |
|------|--------|-------------|---------|
| Decision Document | Markdown with ADR format | Technology choice, architecture decision, pattern selection | "We recommend PostgreSQL because..." |
| Benchmark Results | CSV + analysis markdown | Performance evaluation, load testing | pg-benchmark-results.csv + analysis |
| Prototype/Spike | Code in spike/ directory, never merged | Feasibility testing, API exploration | spike/kafka-poc/ with README |
| Data Analysis | Jupyter notebook or SQL + charts | Query pattern analysis, data modeling | query-patterns.ipynb |
| Landscape Survey | Comparison matrix in markdown | Tool/technology evaluation | database-comparison-matrix.md |
| Risk Assessment | Risk register in markdown | Security, compliance, reliability investigation | gdpr-compliance-risks.md |

## Artifact Quality Gate

Every artifact must pass:
1. **Answers the unknown:** A reader can identify the original unknown and the answer
2. **Actionable:** Someone can make a decision based on this artifact
3. **Reproducible:** Someone else could re-run the investigation and get similar results
4. **Traceable:** References the ticket(s) it resolves and data sources used
5. **Recommendation:** Includes explicit recommendation with confidence level (HIGH/MEDIUM/LOW)

## Artifact Template

```markdown
# [Artifact Title]

## Original Unknown
[Restate the "We don't know X" from the ticket]

## Method
[How we investigated — tools, data sources, experiments]

## Findings
[What we discovered — data, observations, insights]

## Recommendation
We recommend [X] because [reasons]. Confidence: [HIGH/MEDIUM/LOW].

## Alternatives Considered
| Alternative | Why Rejected |
|-------------|--------------|
| ... | ... |

## Limitations
[What this investigation did NOT cover, caveats, assumptions]

## References
- Ticket: [ID]
- Data sources: [files, URLs]
```

## Artifact Storage

```
tickets/
├── artifacts/
│   ├── DB-001-query-patterns.csv
│   ├── DB-001-query-patterns-analysis.md
│   ├── DB-002-pg-benchmark-results.md
│   └── capstone-database-decision.md
```
