# Gotchas — LLM Search Optimizer

Extended gotchas and failure patterns with case studies.

## Content Licensing Gotcha

**Pattern:** Allowing Google-Extended without understanding it controls Gemini training AND AI Overviews.

**Case:** A publisher blocked GPTBot and CCBot but allowed Google-Extended "because we might license to Google." Their content appeared in Google AI Overviews but was invisible on ChatGPT and Perplexity — losing the fastest-growing B2B research channel. When they blocked Google-Extended to negotiate, their AI Overviews citations disappeared within 72 hours.

**Lesson:** Google-Extended controls BOTH training and AI Overviews inclusion. Blocking it removes you from all Google AI search surfaces. Negotiate licensing BEFORE blocking.

## llms.txt Staleness Gotcha

**Pattern:** Creating llms.txt once and never updating it.

**Case:** A documentation site published llms.txt listing 50 key pages. Six months later, they added 30 new guides but never updated llms.txt. AI crawlers continued indexing the old 50 pages and missed all new content. When ChatGPT users asked about newly covered topics, the AI cited competitor docs that WERE in their llms.txt.

**Lesson:** Stale llms.txt is actively harmful — it tells AI crawlers your site hasn't changed. Automate updates with your CMS.
