# When NOT to Use This Skill (Overkill)

- **Solo developer, internal tool, no users beyond yourself**: A docs site, ADRs, and style guide for a solo project is effort with zero audience. A good README + code comments = sufficient.
- **Pre-product-market-fit startup with 0-10 users**: Invest time in building, not documenting. A README + quick start is all you need. Docs site can wait until you have users who need them.
- **You're the only person who will ever touch this code**: Documentation is communication. If you're the only audience, code comments and clear naming communicate enough.
- **The codebase is a throwaway prototype**: Don't document code you plan to delete. Prototype → validate → rewrite. Document the rewrite, not the prototype.
- **Documentation is being used to avoid fixing UX**: "We'll just document this confusing behavior" is an anti-pattern. If users keep asking the same question, fix the product, not the docs.
