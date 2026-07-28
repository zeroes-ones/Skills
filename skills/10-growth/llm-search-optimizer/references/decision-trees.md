# Decision Trees — LLM Search Optimizer

Extended decision trees for crawler strategy, content format selection, and entity reconciliation.

## Crawler Strategy by Content Type

| Content Type | GPTBot | CCBot | Claude-Web | PerplexityBot | Google-Extended |
|-------------|--------|-------|------------|---------------|-----------------|
| Public blog/articles | Allow | Allow | Allow | Allow | Allow |
| Documentation | Allow | Allow | Allow | Allow | Allow |
| Product pages | Allow | Allow | Disallow | Allow | Allow |
| User-generated content | Disallow | Disallow | Disallow | Disallow | Disallow |
| API endpoints | Disallow | Disallow | Disallow | Disallow | Disallow |
| Account/checkout | Disallow | Disallow | Disallow | Disallow | Disallow |
| Paywalled content | Disallow | Disallow | Disallow | Disallow | Allow* |
| Internal tools | Disallow | Disallow | Disallow | Disallow | Disallow |

*Google-Extended can be allowed for paywalled content to participate in content licensing negotiations.

## Content Format Decision Matrix

| Query Intent | Content Format | Schema Type | Key Signal |
|-------------|---------------|-------------|------------|
| "What is X?" | Definition + 60-word answer | FAQPage, Article | Directness, entity authority |
| "How does X work?" | Explanation + mechanism breakdown | Article, TechArticle | Clarity, source citations |
| "X vs Y" | Comparison table + verdict | Article, ItemList | Objectivity, data citations |
| "How to X" | Numbered steps + tools list | HowTo | Completeness, step clarity |
| "Best X for Y" | Ranked recommendations | ItemList, Product | Specificity, use-case matching |
| "Why does X happen?" | Causal explanation + evidence | Article | Evidence quality, source authority |

## Entity Reconciliation Priority

| Platform | Priority | Impact on AI Citation | Verification |
|----------|----------|----------------------|-------------|
| Wikidata | Highest | Foundation for all knowledge graphs | Check Q-ID resolves, verify all statements |
| Wikipedia | Highest | Primary entity authority signal | Verify page exists, check for disambiguation |
| Crunchbase | High | Business entity verification | Verify company profile URL, check funding data |
| LinkedIn | High | Professional entity signal | Verify company page, check employee count |
| GitHub | Medium | Technical entity signal | Verify organization profile, check repo count |
| Twitter/X | Medium | Real-time entity signal | Verify handle, check verification status |
| Medium | Medium | Publishing platform signal | Verify publication URL |
| ORCID | High (authors) | Academic author authority | Verify author ID, check publication list |
| Google Scholar | High (authors) | Academic citation authority | Verify author profile, check citation count |
