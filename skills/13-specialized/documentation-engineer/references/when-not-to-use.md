# When NOT to Use This Skill (Overkill)

- **Solo developer, internal tool, no other users**: A docs site, ADR system, style guide, and freshness automation for a solo project is effort with zero audience. README + code comments = sufficient.
- **Pre-product-market-fit with 0 users**: Invest time building, not documenting. Users will tell you what needs explanation. Don't guess.
- **The codebase is a throwaway prototype**: Don't document code you plan to delete. If you're prototyping to validate, document the learnings, not the prototype.
- **Documentation is being used to avoid fixing UX**: "We'll document this confusing behavior" is an anti-pattern. If users keep asking the same question, fix the product.
- **Your entire product is a single function/API**: A 2-page doc site for 1 API endpoint is overkill. Put everything in the README.
