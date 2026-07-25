## The Skill Quality Rubric

This is how to grade ANY skill. Use it to audit existing skills and self-assess generated skills.

| Dimension | 6/10 (Adequate) | 8/10 (Good) | 10/10* (World-Class) |
|-----------|----------------|-------------|---------------------|
| **Ground Rules** | Generic rules ("Be careful with auth"), no examples, 3-4 rules | Domain-specific rules, some violation examples, 5-6 rules | Every rule has concrete violation story + mechanical trigger + exact STOP response, 6-10 rules |
| **Gotchas** | "Be careful" warnings, 3-5 entries, no dollar figures | Some dollar figures ($X,XXX+), 6-8 entries, mostly domain-specific | 10+ gotchas with breakout cost calculations from real incidents, every entry has dollar range + specific prevention |
| **Anti-Rationalization** | 2-3 generic entries ("It works on my machine"), 2-column format | 4-5 domain entries, 3-4 columns, some psychological insight | 6+ entries with 4-column format + psychological bias identified, "Why It Feels Right" is uncomfortably accurate |
| **Decision Trees** | Text-only if/else, 1-2 trees, no when-NOT-to-use guidance | Simple ASCII tree, 2 trees, some branching | 3+ multi-level ASCII trees with YES/NO branching + when-NOT-to-use at terminal nodes |
| **Error Recovery** | "Check logs" advice, 1-2 scenarios | 2-3 specific scenarios, some step-by-step commands | 5+ scenarios with exact commands, root cause analysis, escalation triggers, and prevention measures |
| **Verification** | 3-5 generic checks ("tests pass"), no prefix IDs | 7-9 domain checks, some binary, some prefix IDs | 10+ binary checks with domain-specific prefix IDs covering security, performance, accessibility, correctness |
| **Scale Depth** | Mentioned scale levels exist, no depth | Brief per-level guidance, table format | Full Solo→Enterprise matrix with transition triggers, coordination models, and domain-specific scaling concerns |
| **Cross-Skill** | Lists upstream/downstream in frontmatter only | Table with what-receives/provides, some communication triggers | Upstream table + downstream table + communication triggers + escalation path + common chains |
| **Chain Connectivity** | Connected to 1-2 skills, symmetric edges unverified | Connected to 3-4 skills, most edges symmetric | Part of 3+ meaningful chain paths, all edges symmetric, chain YAML entries created |
| **Token Efficiency** | >800 lines (bloated), redundant content, no pruning | 500-700 lines, some sediment | 400-700 lines (rich but dense — no no-op content); security/critical: 600-1000. Every line earns its token cost |
