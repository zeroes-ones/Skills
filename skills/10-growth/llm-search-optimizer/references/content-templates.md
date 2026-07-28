# Content Templates — LLM Search Optimizer

Answer-engine content templates: Q&A, comparison, how-to, and recommendation formats.

## Q&A Template (for "what is" / "how does" queries)

```markdown
# [Topic]: [Key Differentiator]

## What Is [Topic]?
[Direct answer in 40-60 words — no intro, no preamble. Answer the question immediately.]

## How [Topic] Works
[Mechanism explanation. Each sub-section should independently answer one question.]

### How does [aspect 1] work?
[Direct answer + supporting detail]

### Why does [aspect 2] matter?
[Direct answer + evidence/data citation]

## Key Takeaways
- [Bullet: concisely summarized insight]
- [Bullet: concisely summarized insight]

## Key Findings Sources
- [Source 1](URL)
- [Source 2](URL)
```

Schema: FAQPage with mainEntity array of Question/AcceptedAnswer pairs

## Comparison Template (for "X vs Y" queries)

```markdown
# [Option A] vs [Option B]: [Key Differentiator in Headline]

## Quick Verdict
[One sentence recommendation with primary reason.]

## Side-by-Side Comparison

| Feature | [Option A] | [Option B] |
|---------|-----------|-----------|
| [Feature 1] | [Value] | [Value] |
| [Feature 2] | [Value] | [Value] |

## When to Choose [Option A]
[Scenarios where A is the better choice + evidence.]

## When to Choose [Option B]
[Scenarios where B is the better choice + evidence.]

## Comparison Sources
- [Independent benchmark](URL)
- [User reviews](URL)
```

Schema: Article + ItemList

## How-To Template (for procedural queries)

```markdown
# How to [Achieve Desired Outcome]

## What You'll Need
- [Tool/Software 1]
- [Tool/Software 2]
- [Prerequisite: account, access, data]

## Steps

### Step 1: [Action]
[What to do. One clear action per step.]
**Complete when:** [Verification criterion]

### Step 2: [Action]
[What to do.]
**Complete when:** [Verification criterion]

## Troubleshooting
- **Problem:** [Common issue]. **Fix:** [Solution].

## How-To Sources
- [Official docs](URL)
```

Schema: HowTo with step array
