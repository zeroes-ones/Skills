# Technical Content Guide

> **Author:** Sandeep Kumar Penchala

A practical framework for creating technical content that developers actually want to read, watch, and share. Companion to the [DevRel Advocate SKILL.md](../SKILL.md).

---

## 1. Tutorial Structure

### The Golden Template

```markdown
# [Tutorial Title]: [What You'll Build in Under 10 Words]

## Problem
> "Have you ever [pain point]? In [N] minutes, we'll solve this by building [X]."

## Why This Solution
Why [tool/framework/approach] over alternatives? (1–2 sentences)

## Prerequisites
- [Tool] v[version] installed
- Basic familiarity with [concept]
- [Account/API key] for [service]

## Step 1: [Action-Oriented Heading]
[Explain WHY before showing HOW]

```bash
npm init -y
npm install express
```

> **What's happening:** [Explain each command or concept]

## Step 2: [Action-Oriented Heading]
```javascript
// Complete, runnable code block
const app = require('express')();
app.get('/', (req, res) => res.json({ status: 'ok' }));
```

## Step N: [Action-Oriented Heading]

## Complete Code
```javascript
// Full working file — copy-paste ready
```

## Next Steps
- [Deploy to production with X]
- [Add authentication with Y]
- [Explore the full API reference]

## Troubleshooting
| Error | Cause | Fix |
|---|---|---|
| `EADDRINUSE` | Port already in use | `kill -9 $(lsof -t -i:3000)` |
```

### Tiered Tutorials

| Level | Length | Prereqs | Code Style |
|---|---|---|---|
| **Quickstart** | 5 min, ~300 words | None | CLI + copy-paste |
| **Intro tutorial** | 15 min, ~1,500 words | Quickstart | Explained line-by-line |
| **Advanced guide** | 45 min, ~3,500 words | Intro tutorial | Architecture + patterns |
| **Production cookbook** | 60+ min, 5K+ words | Advanced guide | Full repo with tests |

---

## 2. API Documentation Standards

### OpenAPI-First Workflow
1. Design API spec in OpenAPI 3.1 YAML/JSON
2. Generate reference docs from spec (Redocly, Scalar, Mintlify)
3. Code samples auto-generated or manually curated per endpoint
4. Spec validated in CI — docs break if spec changes without update

### Code Samples: Minimum 3 Languages
```yaml
# API endpoint: POST /api/v1/users
samples:
  curl:
    command: |
      curl -X POST https://api.example.com/v1/users \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"name": "Jane", "email": "jane@example.com"}'
  python:
    code: |
      import requests
      response = requests.post(
          "https://api.example.com/v1/users",
          headers={"Authorization": f"Bearer {token}"},
          json={"name": "Jane", "email": "jane@example.com"}
      )
      print(response.json())
  javascript:
    code: |
      const response = await fetch("https://api.example.com/v1/users", {
          method: "POST",
          headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ name: "Jane", email: "jane@example.com" })
      });
      console.log(await response.json());
```

### Interactive Playground
- Embed API console (Scalar, Redocly, Stoplight) directly in docs
- Pre-fill auth tokens for logged-in users
- Show request/response in real-time
- Link playground to corresponding tutorial

---

## 3. Content SEO for Developers

### Keyword Research for Technical Terms
- **Primary:** "how to [do X] with [Y]" (high intent)
- **Secondary:** "[tool] vs [alternative]" (comparison traffic)
- **Tertiary:** "[tool] tutorial," "[tool] best practices" (long-tail)

### Structured Data
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Build a REST API with Express.js",
  "description": "Step-by-step tutorial covering routing, middleware, and error handling.",
  "totalTime": "PT15M",
  "step": [
    { "@type": "HowToStep", "name": "Install dependencies", "text": "Run npm init and npm install express" },
    { "@type": "HowToStep", "name": "Create server", "text": "Write the Express app entry point" }
  ]
}
```

### Snippet Optimization
- Answer the question in first 40–50 words
- Use `<h2>` for each step (Google extracts these)
- Code blocks tagged with language (` ```python ` not ` ``` `)
- Include error messages and solutions (captures "how to fix X" searches)

### URL Structure
```
Good: /blog/build-rest-api-express-nodejs
Bad:  /blog/post?id=123
Avoid: /blog/2024/03/15/how-to-build-a-rest-api
```

---

## 4. Content Calendar Template

| Week | Theme | Format | Channel | Author | Publish Date | Promotion |
|---|---|---|---|---|---|---|
| 1 | Getting Started with [Product] | Tutorial | Blog + YouTube | Alice | Mon 10am | Twitter thread, HN, Reddit |
| 2 | Customer Story: [Company] | Case Study | Blog | Bob | Wed 9am | LinkedIn, customer socials |
| 3 | Deep Dive: [Architecture] | Long-form | Blog + Podcast | Carol | Thu 12pm | Dev.to cross-post, newsletter |
| 4 | Ship It Saturday | Live Stream | YouTube + Discord | Team | Sat 11am | Discord event, Twitter Spaces |

### Quarterly Planning
- **Month 1:** Hero launch content + awareness
- **Month 2:** Educational deep-dives + community
- **Month 3:** Case studies + social proof

---

## 5. Content Repurposing Workflow

```
┌────────────────┐
│  LONG-FORM     │  Blog post (2,500+ words), conference talk, or podcast episode
│  (Source)      │  — One piece of "hero" content per week
└───────┬────────┘
        │
        ├──► Tweet Thread (12 tweets) — Key takeaways, one insight per tweet
        │    Post same day as source content
        │
        ├──► Short Video (60 sec) — One key concept, vertical format
        │    YouTube Shorts + TikTok + Instagram Reels — 2 days after
        │
        ├──► Newsletter Tease (200 words) — Link to full post + CTA
        │    Include in weekly digest — same week
        │
        ├──► Talk Abstract (500 words) — Adapt as conference proposal
        │    Submit to 2–3 CFPs — within 2 weeks
        │
        └──► Social Carousel (5–10 slides) — Step-by-step visual
             LinkedIn + Instagram — 1 week after
```

### Repurposing Checklist
- [ ] Does the format match the platform? (LinkedIn ≠ TikTok)
- [ ] Is the call-to-action clear? (Read full post? Watch video? Try the API?)
- [ ] Are code snippets preserved? (Screenshots for image-only platforms)
- [ ] Is the branding consistent across formats?
- [ ] Did you tag relevant tools/people for amplification?

---

## 6. Writing Style for Developers

### Voice Guidelines
- **Active voice:** "The agent deploys your app" not "Your app is deployed by the agent"
- **Second person:** "You run the command" not "The user runs the command" or "One runs the command"
- **Present tense:** "The API returns a JSON object" not "The API will return a JSON object"
- **Avoid hedging:** "This is the fastest way" not "This might be one of the faster ways"
- **Embrace brevity:** Every sentence must earn its place

### Code Commenting Rules
```python
# GOOD: Explains WHY, not WHAT
# Normalize timestamps to UTC to avoid DST edge cases in aggregations
timestamp = normalize_to_utc(raw_timestamp)

# BAD: Restates the obvious
# Normalize the timestamp
timestamp = normalize_to_utc(raw_timestamp)
```

### Accessibility in Technical Content
- Alt text for all images: describe the diagram, not "screenshot.png"
- Transcripts for video content
- Semantic HTML headings (never skip from H2 to H4)
- Color contrast ratio ≥ 4.5:1 for code blocks and diagrams
- Avoid "click here" — use descriptive link text: "Read the deployment guide"

---

*Apply these templates and frameworks consistently across your content program. Measure what resonates (time on page, completion rate, social engagement) and double down on winning formats.*
