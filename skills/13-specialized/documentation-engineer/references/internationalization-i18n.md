# Internationalization (i18n)

### Translation Workflow

- **Docusaurus i18n Setup**:
  ```bash
  # Initialize i18n
  npx docusaurus write-translations --locale fr
  npx docusaurus write-translations --locale zh-CN
  ```
- **Crowdin Integration**: Docusaurus has a Crowdin plugin. Automated sync: extract English strings -> push to Crowdin -> translated content pulled back -> deploy with all locales.
- **GitLocalize**: Lighter alternative. Open source projects use GitLocalize for community translations.
- **Manual Translation**: For small teams, translators work directly on translated `.md` files in the `i18n/` directory.

### Locale-Specific Content

- **Language Switcher**: Dropdown in the navbar listing available locales.
- **Fallback to English**: If a page hasn't been translated, show the English version with a banner: "This page isn't available in [language] yet."
- **Partial Translation**: It's fine to have some pages translated and others not. Better to ship incomplete translations than none.

### URL Strategy

- `example.com/docs/` -- English (default)
- `example.com/fr/docs/` -- French
- `example.com/zh-CN/docs/` -- Simplified Chinese

### RTL Support

- **Docusaurus RTL**: Built-in RTL support for Arabic, Hebrew, Persian, Urdu. Automatically swaps layout direction.
- **CSS Mirroring**: Docusaurus automatically mirrors the UI. Custom CSS must be RTL-aware.
