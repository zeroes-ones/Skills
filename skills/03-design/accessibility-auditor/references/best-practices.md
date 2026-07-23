# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Test with real users:** Automated tools and manual scripts are proxies. Real users with disabilities find issues you'll never catch. Test with at least 3 users with different disabilities.
- **Shift left:** Catch accessibility issues in design (color contrast, focus order, heading structure) before code is written.
- **Design system integration:** Build accessible components once. A button with correct focus, label, and role in the design system benefits every page.
- **Don't override semantics:** `<div onclick>` is not a button. Use `<button>`. `<span class="h2">` is not a heading. Use `<h2>`.
- **ARIA is a last resort:** If you can use native HTML, use it. ARIA adds roles/states/properties but not behavior — you must implement keyboard interaction yourself.
- **`aria-label` must start with visible text:** Voice control users say "Click [visible text]" — if the accessible name differs from visible text, voice commands fail.
