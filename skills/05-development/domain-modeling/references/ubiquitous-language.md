# Ubiquitous Language

The cornerstone of Domain-Driven Design — a shared vocabulary spoken by domain experts, developers, product managers, and QA alike. When everyone uses the same words with the same meanings, misunderstandings collapse.

## Core Principles
- **One term, one meaning** — never overload a term across bounded contexts without explicit disambiguation
- **Language lives in code** — class names, method names, and module names reflect the ubiquitous language
- **Domain experts own the language** — developers adopt the expert's terminology, not the other way around

## Maintenance
- Capture terms in `CONTEXT.md` at the project root
- Challenge any term that feels vague during sprint planning or code review
- When a term shifts meaning in conversation, update the glossary immediately

## Anti-Patterns
- Developer-invented jargon that domain experts don't recognize
- Terms that mean different things in standup vs. code vs. customer docs
- Glossary files that haven't been updated since project inception
