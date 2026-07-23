# Information Architecture

### Navigation Design

- **Max 3 levels deep**: Any page should be reachable in (calculating from the homepage). Deep nesting hides content.
- **Breadcrumbs**: Every page includes breadcrumb navigation indicating position in hierarchy.
- **Related Pages**: "Next Steps" or "See Also" section at page bottom linking to logically connected pages.
- **Sidebar Behavior**: Show only the current section's subtree (not the full site tree). Keeps navigation scannable.
- **Search Bar Position**: Prominent in the navbar, immediately visible on page load.

### Search Experience

- **Algolia DocSearch**: Free for open source projects. Configuration via `docusaurus.config.js`. Crawler runs on schedule or CI trigger.
- **Pagefind**: Static search index, no server needed. Works offline. Good for small-to-medium doc sites.
- **Search Relevance Tuning**: Boost page titles over body text, boost short pages, demote "glossary" type pages.
- **Search Analytics**: Track top queries, "no results" queries (identify documentation gaps), click-through rate from search results.

### Landing Page Design

- **Hero Section**: Product name, tagline, "Get Started" CTA button.
- **Quickstart Link**: Most visible link after hero -- "Get started in 5 minutes."
- **Popular Guides**: 3-4 most-visited pages with brief descriptions.
- **Search Bar**: Prominently displayed, with placeholder text encouraging search ("Search docs...").

### Content Hierarchy (Diataxis Framework)

| Category | Purpose | Audience | Example |
|---|---|---|---|
| **Tutorial** | Learning-oriented | New users | "Build your first app" |
| **How-To Guide** | Task-oriented | Experienced users | "Deploy to production" |
| **Reference** | Information-oriented | All users | "API endpoint reference" |
| **Explanation** | Understanding-oriented | Advanced users | "Architecture overview" |

### Progressive Disclosure

- **Summary -> Details -> Deep Dive**: Each page starts with a one-paragraph summary. Expand with progressively more detail. Reserve the deepest technical content for optional expandable sections or linked deep-dive pages.
- **Collapsible sections**: Use `<details>` / `<summary>` for optional deep-dives that 80% of readers don't need.
