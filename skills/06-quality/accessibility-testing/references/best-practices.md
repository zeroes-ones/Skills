# Best Practices

<!-- DEEP: 10+min -->
1. **Test after every DOM mutation, not just on page load.** SPA navigation, modal opens, tab switches, and infinite scroll all change the DOM. axe-core must re-run after each of these events. A page that passes on load can fail after the user opens a menu.
2. **Never globally exclude rules.** If you must exclude a rule, do it per-component or per-page with a comment explaining why and a ticket tracking the fix. Global exclusions hide regressions.
3. **Accessibility snapshot testing is fragile but valuable.** Storing axe-core results as snapshots means any DOM change may update the snapshot — but it forces developers to consciously acknowledge accessibility changes. Use sparingly on stable components.
4. **Color contrast is the most common violation — automate it everywhere.** Axe-core catches most contrast issues, but gradient backgrounds, images with text, and CSS pseudo-elements may be missed. Supplement with visual regression testing focused on contrast ratios.
5. **Track the accessibility debt ratio.** `(open violations / total checks) × 100`. A ratio trending down means the team is fixing faster than creating. A ratio trending up means the opposite. Review monthly.
6. **Focus order testing requires real keyboard simulation.** `page.keyboard.press('Tab')` in Playwright is not the same as the browser's native Tab behavior. Use `page.locator('body').press('Tab')` and verify `document.activeElement` matches the expected next element.
7. **Prefer integration tests over unit tests for a11y.** A `<Button>` component may pass axe in isolation. But 5 `<Button>` components with conflicting aria-labels inside a `<nav>` may fail at the integration level. The most common a11y bugs are compositional, not isolated.
8. **Mobile accessibility is not "small desktop accessibility."** Touch target size (minimum 44x44 CSS pixels), screen reader swipe gestures, dynamic type/text resize support, and reduced motion preferences are unique to mobile. Test on real devices, not just responsive viewports.
