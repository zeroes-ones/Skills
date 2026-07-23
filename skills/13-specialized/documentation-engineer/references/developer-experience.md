# Developer Experience

### Quickstart Quality

- **Time-to-First-Success < 5 Minutes**: The quickstart guide should produce a working result (API response, "Hello World" app) within 5 minutes of starting.
- **One-Command Setup**: `curl -fsSL https://install.example.com | bash` or `npx create-my-app my-project`.
- **No Assumptions**: Don't assume the reader has Node.js, Python, or anything pre-installed. Include system dependency verification.

### Code Sample Testing

- **Doctest Pattern**: Embed tests in docs code blocks, then extract and run them in CI.
- **TypeScript Type Checking**: Extract `.ts` snippets, run `tsc --noEmit` in CI.
- **Rust Doc Tests**: `cargo test` verifies all code examples in Rust doc comments pass.

### Copy-Paste Button

- Every code block has a visible copy button (Docusaurus includes this by default).
- Shell command blocks have a "copy command" button (excludes output lines).
- Multi-line code blocks show line numbers for reference.

### Dark Mode

- **Automatic**: Respects `prefers-color-scheme` CSS media query on first visit.
- **Manual Toggle**: Sun/moon icon in the navbar. Choice is persisted in `localStorage`.
- **Asset Readiness**: All diagrams, screenshots, and logos have dark-mode variants.

### Mobile Responsiveness

- **Readable on Phones**: Docs must be fully readable on a 375px-wide screen (on-call engineers checking their phone).
- **Table Scroll**: Wide tables get horizontal scroll, not overflow.
- **Code Block Scroll**: Code blocks are horizontally scrollable on mobile (not wrapped -- wrapping breaks copy-paste).
