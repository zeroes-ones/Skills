# Monitoring Setup — LLM Search Optimizer

Step-by-step GSC AI Overviews tracking, LLM brand monitoring tools, and AI referral traffic dashboards.

## Google Search Console — AI Overviews

1. Navigate to GSC → Search results → Search Appearance
2. Filter by "AI Overviews" appearance type
3. Export weekly: queries, pages, impressions, clicks, CTR, position
4. Compare: AI Overviews impressions vs. traditional search impressions
5. Track: which pages appear in AI Overviews, which queries trigger them

## Brand Mention Monitoring

### Manual Method (Free)
1. Search "[your brand]" on ChatGPT weekly
2. Search "[your brand]" on Perplexity
3. Search "[your brand] + [topic]" on Bing Copilot
4. Record: cited or not, context, competing brands mentioned

### Automated Tools
- Brand24, Mention, Talkwalker — brand monitoring with AI platform coverage
- Custom: LLM-based scraper that queries major AI platforms programmatically

## AI Referral Traffic in GA4

### Custom Segment

```
Traffic source dimensions:
- Session source contains "chat.openai.com"
- OR Session source contains "perplexity.ai"
- OR Session medium exact match "ai-search"
```

### Dashboard Metrics
- AI referral sessions (daily/weekly trend)
- AI referral engaged sessions rate
- AI referral conversion rate vs organic search
- Top landing pages from AI referrals

## Competitor Citation Tracking

1. List top 20 target queries
2. For each query, check: Google AI Overviews, ChatGPT, Perplexity, Bing Copilot
3. Record: which competitor is cited, which URL, citation context
4. Track weekly: new competitors cited, changes in citation patterns
5. Gap analysis: what does the cited competitor have that you don't (entity authority, content structure, freshness)?
