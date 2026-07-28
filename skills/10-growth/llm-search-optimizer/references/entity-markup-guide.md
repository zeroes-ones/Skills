# Entity Markup Guide — LLM Search Optimizer

Schema.org entity markup patterns with JSON-LD examples for Organization, Person, Product, and Article. See `core-workflow.md` for full code examples.

## Entity Types and Their AI Impact

| Entity Type | AI Citation Impact | Key Properties |
|-------------|-------------------|----------------|
| Organization | Brand recognition in AI answers | name, url, sameAs, logo, description, foundingDate, founder |
| Person | Author attribution, expert citation | name, jobTitle, worksFor, sameAs, description |
| Article | Content citation eligibility | headline, author, publisher, datePublished, dateModified, about |
| FAQPage | Q&A citation in AI Overviews | mainEntity → Question → name + acceptedAnswer → text |
| HowTo | Step-by-step citation | name, step → HowToStep → text, supply, tool |
| Product | Product citation in recommendations | name, description, brand, offers, review |
| Event | Event citation in AI answers | name, startDate, location, performer, organizer |
| Place | Local entity recognition | name, address, geo, sameAs |
| CreativeWork | Generic content citation | author, publisher, datePublished, about, mentions |

## common sameAs Patterns

### For Organizations
- Wikidata: `https://www.wikidata.org/wiki/Q{id}`
- Wikipedia: `https://en.wikipedia.org/wiki/{Page_Name}`
- Crunchbase: `https://www.crunchbase.com/organization/{slug}`
- LinkedIn: `https://www.linkedin.com/company/{slug}`
- Twitter/X: `https://twitter.com/{handle}`
- GitHub: `https://github.com/{org}`

### For People
- ORCID: `https://orcid.org/{id}`
- LinkedIn: `https://www.linkedin.com/in/{slug}`
- GitHub: `https://github.com/{username}`
- Google Scholar: `https://scholar.google.com/citations?user={id}`

## Verification Commands

```bash
# Verify sameAs links
curl -sL -o /dev/null -w "%{http_code}" "https://www.wikidata.org/wiki/Q12345"

# Validate schema markup
# Use: https://validator.schema.org/ or Google Rich Results Test

# Extract all sameAs links from a page
curl -s https://example.com | grep -oP 'sameAs.*?https://[^"]+' | head -20
```
