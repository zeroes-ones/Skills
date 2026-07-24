# Anti-Patterns

> Common template and scaffolding failures with real cost data.

## Fork-and-Forget

**Symptom:** Team forks the base template, customizes, and never pulls upstream changes.

**Result:** 5+ "template" repos sharing nothing. Security fixes applied 5 times.

**Annual cost:** $50K-$100K in duplicated maintenance for a 50-repo org.

**Fix:** Template inheritance hierarchy. One source of truth per level.

## Over-Engineering

**Symptom:** 3-month project to build a "perfect" CLI with plugin architecture.

**Result:** Developers copy-paste from existing repos because the CLI is not ready.

**Annual cost:** $150K-$250K in platform team salary, zero adoption.

**Fix:** Start with GitHub template repo. Add tooling when simple approach hurts.

## Broken CI Templates

**Symptom:** Template CI fails on first push. Engineers debug template instead of building features.

**Result:** Trust in templates destroyed. Each engineer fixes CI locally.

**Annual cost:** $20K-$30K in trust erosion and rework.

**Fix:** Weekly automated test: scaffold repo, push, verify CI green.

## Too Many Prompts

**Symptom:** Template asks 12 questions before generating. Engineers abandon it.

**Result:** Template exists but nobody uses it. Zero ROI.

**Annual cost:** $5K-$10K in wasted template development.

**Fix:** Maximum 3-5 prompts. Everything else is organizational default.

## Unversioned CI Templates

**Symptom:** CI reusable workflow updated without versioning. All downstream repos break.

**Result:** On-call scramble. Hours of debugging. Delayed CI.

**Per-incident cost:** $10K-$20K in engineering time across 50+ repos.

**Fix:** Semantic versioning. Deprecate old versions, never break.
