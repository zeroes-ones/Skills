# Versioning

### Strategies

- **Per Major Version** (recommended): `docs/v1/`, `docs/v2/`, `docs/latest/`. Each major version has its own doc snapshot. Docusaurus supports this natively.
- **Per Minor Version**: Useful for SaaS products with frequent releases and backward-compatible changes. Use when minor versions introduce meaningful doc changes.
- **"Latest" Alias**: `/latest/` always points to the most recent stable version. `/v2/` is locked.

### Deprecation Banners

```mdx
:::caution You're reading outdated docs
This documentation is for version 1.x, which is no longer actively maintained.
View the [latest version](/latest) of this page.
:::
```

Configured globally in Docusaurus:
```js
// docusaurus.config.js
module.exports = {
  presets: [
    [
      'classic',
      {
        docs: {
          banner: 'unmaintained',
        },
      },
    ],
  ],
};
```

### Version Selector UX

- **Dropdown in Navbar**: Docusaurus adds this automatically with `lastVersion` and `versions` config.
- **URL-Based Versions**: `/docs/latest/getting-started`, `/docs/v2.0.0/getting-started`
- **Redirect**: `/docs/` -> `/docs/latest/` automates routing to current version.

### Maintenance Policy

- **Current + N-1 Maintained**: Latest version receives full updates. The previous major version receives critical bug fixes and security updates. Older versions are frozen (no updates) with deprecation banners.
- **Automation**: GitHub Action runs weekly to check doc version ages and add banners when a version falls out of maintenance.
