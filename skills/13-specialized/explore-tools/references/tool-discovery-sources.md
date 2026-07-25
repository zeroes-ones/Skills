## Tool Discovery Sources

<!-- Comprehensive registry and community source catalog -->

### Registries (Package-Specific)

| Registry | Best For | Key Data Points | Query Tools |
|----------|----------|----------------|-------------|
| **npm** (npmjs.com) | JavaScript/TypeScript libraries | Weekly downloads, version history, dependency count, bundle size | npm search, npm view, npm trends, bundlephobia.com, npm-stat.com, socket.dev |
| **PyPI** (pypi.org) | Python packages | Monthly downloads, version history, Python version support, wheel availability | pip search (deprecated), pypistats.org, libraries.io, snyk.io/advisor/python |
| **crates.io** | Rust crates | Total downloads, recent downloads, version history, dependency count | cargo search, crates.io/api, lib.rs (curated rankings), blessed.rs |
| **Docker Hub** | Container images | Pull count, stars, last updated, supported architectures | docker search, hub.docker.com, docker scout (vulnerability scanning) |
| **Homebrew** (brew.sh) | macOS CLI tools and libraries | Install count (30/90/365 day), formula analytics, dependencies | brew search, brew info --analytics, brew info --json |
| **Go Module Index** (pkg.go.dev) | Go packages | Imported-by count, version history, license, documentation quality | go search, pkg.go.dev, awesome-go.com |
| **Maven Central** (search.maven.org) | Java/Kotlin libraries | Usage count, version history, vulnerability data | mvnrepository.com, mvn dependency:tree, snyk.io/advisor/maven |
| **NuGet** (nuget.org) | .NET packages | Download count, version history, .NET version support | nuget.org, dotnet list package --vulnerable |
| **GitHub Packages** | Multi-language, private packages | Download count, version history, visibility | gh api, GitHub UI |

### Community & Social Sources

| Source | What to Search | Signal Strength |
|--------|---------------|----------------|
| **GitHub Trending** | github.com/trending/[language]?since=weekly | High: real developer interest |
| **GitHub Awesome Lists** | github.com/topics/awesome, awesome-[topic] repos | Medium: curated but may be outdated |
| **Stack Overflow Tags** | stackoverflow.com/tags, tag trends over time | High for adoption velocity |
| **Stack Overflow Questions** | [topic] vs [topic] questions, answer scores | Medium: opinion-based but real experience |
| **Hacker News** | hn.algolia.com: Ask HN: best [tool type] | High: practitioner discussions with rationale |
| **Reddit** | r/programming, r/webdev, r/javascript, r/python, r/rust, r/devops, r/ExperiencedDevs | Medium: mixed quality, filter by upvotes + comments |
| **Dev.to** | dev.to/search: [tool] vs [tool] comparison posts | Low-Medium: often promotional, verify claims |
| **Medium** | medium.com/search: best [tool type] [year] | Low: heavy affiliate/sponsor bias, verify independently |
| **YouTube** | Conference talks (PyCon, RustConf, JSConf, KubeCon) about tool comparisons | Medium: good for architecture decisions, verify recency |
| **Twitter/X** | Search [tool] alternative or migrating from [tool] | Medium: real-time sentiment, verify with other sources |

### Comparison & Analysis Tools

| Tool | Purpose | URL |
|------|---------|-----|
| **bundlephobia** | npm package size + dependency tree cost | bundlephobia.com |
| **npm trends** | Compare npm package popularity over time | npmtrends.com |
| **libraries.io** | Dependency health across 30+ package managers | libraries.io |
| **bestofjs.org** | Curated JS projects by category with trends | bestofjs.org |
| **slant.co** | Community-ranked tool recommendations with pros/cons | slant.co |
| **stackshare.io** | Tech stack comparisons, company stack profiles | stackshare.io |
| **Snyk Advisor** | Package health: security, popularity, maintenance | snyk.io/advisor |
| **Socket.dev** | Supply chain security + package health + typo-squatting detection | socket.dev |
| **OpenBase** | Curated library comparisons with developer reviews | openbase.com |
| **Moiva.io** | Universal package comparison (npm, PyPI, crates) | moiva.io |
| **LibHunt** | Trending open-source projects by language | libhunt.com |
| **OSS Insight** | GitHub analytics: stars, forks, contributors, trends | ossinsight.io |
| **Star History** | Star growth comparison charts for GitHub repos | star-history.com |
| **ReposCompare** | Side-by-side GitHub repo comparison | reposcompare.com |

### Search Query Templates

```bash
# GitHub: find popular projects in a domain
# Search: "topic:react" stars:>1000 pushed:>2024-01-01 language:typescript
# Search: "awesome OR curated" [topic] stars:>500

# GitHub: find alternatives to a specific tool
# Search: "[tool-name] alternative OR replace OR migrate"
# Search: "[tool-name] vs" stars:>100

# Stack Overflow: find community consensus
# Site: stackoverflow.com "[tool] vs [tool]" OR "[tool] recommendation"

# Hacker News: find practitioner discussions
# Site: news.ycombinator.com "best [tool type]" OR "recommend [tool type]"

# Reddit: find real-world experiences
# Site: reddit.com "[tool] experience" OR "[tool] in production" OR "[tool] review"
```
